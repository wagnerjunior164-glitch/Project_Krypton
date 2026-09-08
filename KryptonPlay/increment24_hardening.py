import sqlite3
from fastapi.responses import JSONResponse


def install(app_module):
    """Enforce the temporary-password lifecycle at the HTTP boundary."""
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
    async def enforce_temporary_password(request, call_next):
        path = request.url.path
        if not path.startswith("/api/") or path in allowed_while_forced:
            return await call_next(request)
        token = request.headers.get("authorization", "")
        if token.lower().startswith("bearer "):
            token = token[7:].strip()
        else:
            token = request.cookies.get(app_module.SESSION_COOKIE, "").strip()
        if not token:
            return await call_next(request)
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
        if path == "/api/v1/profile/password" and 200 <= response.status_code < 300 and token:
            try:
                with sqlite3.connect(db) as c:
                    c.execute("UPDATE users SET must_change_password=0 WHERE id IN (SELECT user_id FROM sessions WHERE token=?)", (token,))
                    c.commit()
            except sqlite3.Error:
                pass
        return response
