import json
import os
import sqlite3
from fastapi.responses import JSONResponse


def _token_from_request(request, app_module):
    token = request.headers.get("authorization", "")
    if token.lower().startswith("bearer "):
        return token[7:].strip()
    return request.cookies.get(app_module.SESSION_COOKIE, "").strip()


def _admin_user_id(token, db):
    if not token:
        return None
    try:
        with sqlite3.connect(db) as c:
            row = c.execute(
                "SELECT users.id, users.role, users.account_status, sessions.expires_at "
                "FROM sessions JOIN users ON users.id=sessions.user_id WHERE sessions.token=?",
                (token,),
            ).fetchone()
        if not row or row[1] != "admin" or row[2] != "active":
            return None
        return int(row[0])
    except sqlite3.Error:
        return None


def install(app_module):
    """Apply publication hardening at the HTTP boundary."""
    app = app_module.app
    db = app_module.database_path

    with sqlite3.connect(db) as c:
        cols = {row[1] for row in c.execute("PRAGMA table_info(users)").fetchall()}
        if "must_change_password" not in cols:
            c.execute("ALTER TABLE users ADD COLUMN must_change_password INTEGER NOT NULL DEFAULT 0")
        c.commit()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    allowed_while_forced = {
        "/api/auth/me",
        "/api/v1/profile/custom",
        "/api/v1/profile/preferences",
        "/api/v1/profile/password",
    }

    @app.middleware("http")
    async def enforce_publication_hardening(request, call_next):
        path = request.url.path
        token = _token_from_request(request, app_module)

        # Diagnostics are intentionally available during first-run setup, but
        # become administrator-only once setup has completed.
        if path == "/api/setup/diagnostics" and app_module.setup_completed():
            admin_id = _admin_user_id(token, db)
            if admin_id is None:
                return JSONResponse(status_code=401, content={"detail": "Autenticação administrativa necessária."})

        # Do not return a generated password in an HTTP response. The caller
        # supplies the new password over the authenticated admin channel.
        if path == "/api/v1/admin/users/1/reset-password" or (
            path.startswith("/api/v1/admin/users/") and path.endswith("/reset-password")
        ):
            if request.method != "POST":
                return await call_next(request)
            admin_id = _admin_user_id(token, db)
            if admin_id is None:
                return JSONResponse(status_code=401, content={"detail": "Autenticação administrativa necessária."})
            try:
                user_id = int(path.split("/")[5])
                payload = await request.json()
                new_password = str(payload.get("new_password", ""))
            except (ValueError, TypeError, json.JSONDecodeError):
                return JSONResponse(status_code=422, content={"detail": "new_password é obrigatório."})
            if len(new_password) < 8 or len(new_password) > 200:
                return JSONResponse(status_code=422, content={"detail": "A nova senha deve ter entre 8 e 200 caracteres."})
            with sqlite3.connect(db) as c:
                row = c.execute("SELECT id FROM users WHERE id=?", (user_id,)).fetchone()
                if row is None:
                    return JSONResponse(status_code=404, content={"detail": "Usuário não encontrado."})
                hashed = app_module.hash_password(new_password)
                c.execute("UPDATE users SET password_hash=?, must_change_password=0 WHERE id=?", (hashed, user_id))
                c.execute("DELETE FROM sessions WHERE user_id=?", (user_id,))
                c.commit()
            return JSONResponse(status_code=200, content={"status": "ok", "id": user_id, "message": "Senha redefinida. As sessões anteriores foram invalidadas."})

        if path.startswith("/api/") and path not in allowed_while_forced and token:
            try:
                with sqlite3.connect(db) as c:
                    row = c.execute(
                        "SELECT users.id, users.must_change_password "
                        "FROM sessions JOIN users ON users.id=sessions.user_id "
                        "WHERE sessions.token=?",
                        (token,),
                    ).fetchone()
                if row and int(row[1]) == 1:
                    return JSONResponse(
                        status_code=428,
                        content={
                            "detail": "Troca de senha obrigatória antes de utilizar o KryptonPlay.",
                            "code": "must_change_password",
                        },
                    )
            except sqlite3.Error:
                pass

        response = await call_next(request)

        # Keep local HTTP compatibility by default. Deployments using HTTPS can
        # opt into the Secure cookie attribute without changing application code.
        if os.getenv("KRYPTONPLAY_SECURE_COOKIES", "false").strip().lower() in {"1", "true", "yes", "on"}:
            cookies = response.headers.getlist("set-cookie")
            if cookies:
                response.headers.delete("set-cookie")
                for cookie in cookies:
                    if "secure" not in cookie.lower():
                        cookie = cookie + "; Secure"
                    response.headers.append("set-cookie", cookie)

        if path == "/api/v1/profile/password" and 200 <= response.status_code < 300 and token:
            try:
                with sqlite3.connect(db) as c:
                    c.execute("UPDATE users SET must_change_password=0 WHERE id IN (SELECT user_id FROM sessions WHERE token=?)", (token,))
                    c.commit()
            except sqlite3.Error:
                pass
        return response
