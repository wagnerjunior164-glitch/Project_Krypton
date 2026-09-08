import hashlib,json,logging,os,secrets,shutil,sqlite3,sys
from datetime import datetime,timedelta,timezone
from mimetypes import guess_type
from pathlib import Path
from fastapi import Cookie,Depends,FastAPI,Header,HTTPException,Query,Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field
from scanner import scan_library
IS_FROZEN=getattr(sys,"frozen",False);BASE_DIR=Path(sys.executable).resolve().parent if IS_FROZEN else Path(__file__).resolve().parent;RESOURCE_DIR=Path(getattr(sys,"_MEIPASS",BASE_DIR));CONFIG_PATH=RESOURCE_DIR/"config"/"config.json";STATIC_DIR=RESOURCE_DIR/"static";DATA_DIR=BASE_DIR/"data";LOG_PATH=DATA_DIR/"kryptonplay.log";SESSION_HOURS=24;SESSION_COOKIE="kryptonplay_session";DATA_DIR.mkdir(parents=True,exist_ok=True)
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s %(message)s",handlers=[logging.FileHandler(LOG_PATH,encoding="utf-8"),logging.StreamHandler()]);logger=logging.getLogger("kryptonplay")
def load_config():
    with CONFIG_PATH.open(encoding="utf-8") as f:return json.load(f)
def hash_password(password,salt=None):
    salt=salt or secrets.token_bytes(16);digest=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,200_000);return f"pbkdf2_sha256$200000${salt.hex()}${digest.hex()}"
def verify_password(password,stored):
    try:
        algorithm,iterations,salt_hex,digest_hex=stored.split("$")
        if algorithm!="pbkdf2_sha256":return False
        candidate=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt_hex),int(iterations));return secrets.compare_digest(candidate.hex(),digest_hex)
    except (ValueError,TypeError):return False
def initialize_database(config):
    database_path=BASE_DIR/config["database"]["path"];database_path.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(database_path) as c:
        c.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL)");c.execute("INSERT INTO schema_version(version) SELECT 1 WHERE NOT EXISTS(SELECT 1 FROM schema_version)")
        c.execute("CREATE TABLE IF NOT EXISTS media_items (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,media_type TEXT NOT NULL,file_path TEXT NOT NULL UNIQUE,file_size INTEGER,modified_at TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS playback_progress (media_id INTEGER PRIMARY KEY,position_seconds REAL NOT NULL DEFAULT 0,duration_seconds REAL,completed INTEGER NOT NULL DEFAULT 0,updated_at TEXT NOT NULL,FOREIGN KEY(media_id) REFERENCES media_items(id) ON DELETE CASCADE)")
        c.execute("CREATE TABLE IF NOT EXISTS playback_stats (media_id INTEGER PRIMARY KEY,play_count INTEGER NOT NULL DEFAULT 0,watched_seconds REAL NOT NULL DEFAULT 0,updated_at TEXT NOT NULL,FOREIGN KEY(media_id) REFERENCES media_items(id) ON DELETE CASCADE)")
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL UNIQUE,password_hash TEXT NOT NULL,role TEXT NOT NULL DEFAULT 'user',created_at TEXT NOT NULL)")
        user_columns={r[1] for r in c.execute("PRAGMA table_info(users)").fetchall()}
        if "account_status" not in user_columns:c.execute("ALTER TABLE users ADD COLUMN account_status TEXT NOT NULL DEFAULT 'active'")
        c.execute("CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY,user_id INTEGER NOT NULL,expires_at TEXT NOT NULL,FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE)")
        c.execute("CREATE TABLE IF NOT EXISTS user_preferences (user_id INTEGER NOT NULL,key TEXT NOT NULL,value TEXT NOT NULL,updated_at TEXT NOT NULL,PRIMARY KEY(user_id,key),FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE)")
        c.execute("CREATE TABLE IF NOT EXISTS server_settings (key TEXT PRIMARY KEY,value TEXT NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS media_libraries (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL UNIQUE,library_type TEXT NOT NULL DEFAULT 'movie',created_at TEXT NOT NULL,updated_at TEXT NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS media_library_locations (id INTEGER PRIMARY KEY AUTOINCREMENT,library_id INTEGER NOT NULL,path TEXT NOT NULL,is_primary INTEGER NOT NULL DEFAULT 0,created_at TEXT NOT NULL,UNIQUE(library_id,path),FOREIGN KEY(library_id) REFERENCES media_libraries(id) ON DELETE CASCADE)")
        password=os.getenv("KRYPTONPLAY_ADMIN_PASSWORD")
        if password and c.execute("SELECT id FROM users WHERE username='admin'").fetchone() is None:c.execute("INSERT INTO users(username,password_hash,role,created_at) VALUES(?,?,?,?)",("admin",hash_password(password),"admin",datetime.now(timezone.utc).isoformat()))
        user_exists=c.execute("SELECT 1 FROM users LIMIT 1").fetchone() is not None
        setup_flag=c.execute("SELECT value FROM server_settings WHERE key='setup_completed'").fetchone()
        if user_exists and setup_flag is None:c.execute("INSERT INTO server_settings(key,value) VALUES('setup_completed','true')")
        library_setup=c.execute("SELECT value FROM server_settings WHERE key='library_setup_explicit'").fetchone()
        if user_exists and library_setup is None:
            legacy_path=config["media"].get("library_path") if not os.getenv("KRYPTONPLAY_TEST_LIBRARY") else None
            libraries=c.execute("SELECT id,name FROM media_libraries ORDER BY id").fetchall()
            migrated=False
            if legacy_path and len(libraries)==1:
                legacy_id,legacy_name=libraries[0]
                locations=c.execute("SELECT path FROM media_library_locations WHERE library_id=? ORDER BY id",(legacy_id,)).fetchall()
                if legacy_name=="Filmes" and len(locations)==1 and Path(locations[0][0]).resolve()==Path(legacy_path).resolve():
                    c.execute("DELETE FROM media_libraries WHERE id=?",(legacy_id,));migrated=True
                    logger.info("Removed legacy implicit media library path=%s during setup-state migration",legacy_path)
            if not libraries or migrated:c.execute("INSERT INTO server_settings(key,value) VALUES('library_setup_explicit','true')")
            else:c.execute("INSERT INTO server_settings(key,value) VALUES('library_setup_explicit','true')")
        c.commit()
class LoginRequest(BaseModel):username:str=Field(min_length=1,max_length=100);password:str=Field(min_length=1,max_length=200)
class SetupLibrary(BaseModel):name:str=Field(min_length=1,max_length=100);library_type:str=Field(default="movie",pattern="^(movie|series|documentary|other)$");locations:list[str]=Field(default_factory=list,max_length=20)
class SetupRequest(BaseModel):
    username:str=Field(min_length=1,max_length=100);password:str=Field(min_length=8,max_length=200);language:str=Field(default="pt-BR",min_length=2,max_length=20);region:str=Field(default="BR",min_length=2,max_length=20);timezone:str=Field(default="America/Sao_Paulo",min_length=1,max_length=100);server_name:str=Field(default="KryptonPlay",min_length=1,max_length=100);network_access:str=Field(default="local",pattern="^(local|lan)$");indexing_mode:str=Field(default="later",pattern="^(later|incremental)$");playback_mode:str=Field(default="automatic",pattern="^(automatic|local_first)$");libraries:list[SetupLibrary]=Field(default_factory=list,max_length=20)
class SetupLocationsRequest(BaseModel):paths:list[str]=Field(default_factory=list,max_length=100)
class LibraryCreate(BaseModel):name:str=Field(min_length=1,max_length=100);library_type:str=Field(default="movie",pattern="^(movie|series|documentary|other)$");locations:list[str]=Field(default_factory=list,max_length=20)
class LibraryUpdate(BaseModel):name:str|None=Field(default=None,min_length=1,max_length=100);library_type:str|None=Field(default=None,pattern="^(movie|series|documentary|other)$");locations:list[str]|None=Field(default=None,max_length=20)
class ProgressUpdate(BaseModel):position_seconds:float=Field(ge=0);duration_seconds:float|None=Field(default=None,gt=0);completed:bool=False
class PlaybackEvent(BaseModel):watched_seconds:float=Field(default=0,ge=0);started:bool=False
class PreferencesUpdate(BaseModel):preferences:dict[str,str]=Field(default_factory=dict)
class PasswordChange(BaseModel):current_password:str=Field(min_length=1,max_length=200);new_password:str=Field(min_length=8,max_length=200)
class ServerSettingsUpdate(BaseModel):settings:dict[str,str]=Field(default_factory=dict)
class AdminUserCreate(BaseModel):username:str=Field(min_length=1,max_length=100);password:str=Field(min_length=8,max_length=200);role:str=Field(default="user",pattern="^(user|admin)$")
class AdminUserUpdate(BaseModel):role:str|None=Field(default=None,pattern="^(user|admin)$");account_status:str|None=Field(default=None,pattern="^(active|disabled|blocked)$")
config=load_config();server_config=config["server"];database_path=BASE_DIR/config["database"]["path"];library_path=Path(os.getenv("KRYPTONPLAY_TEST_LIBRARY",config["media"]["library_path"]));initialize_database(config)
app=FastAPI(title="KryptonPlay",version="0.1.0");app.mount("/static",StaticFiles(directory=STATIC_DIR),name="static")
def setup_completed():
    with sqlite3.connect(database_path) as c:
        row=c.execute("SELECT value FROM server_settings WHERE key='setup_completed'").fetchone()
        if row is not None:return row[0].lower()=="true"
        return c.execute("SELECT 1 FROM users LIMIT 1").fetchone() is not None
def has_users():return setup_completed()
def get_current_user(authorization:str|None=Header(default=None),session_cookie:str|None=Cookie(default=None,alias=SESSION_COOKIE)):
    token=authorization[7:].strip() if authorization and authorization.lower().startswith("bearer ") else session_cookie.strip() if session_cookie else None
    if not token:raise HTTPException(401,"Autenticação necessária.")
    with sqlite3.connect(database_path) as c:
        c.row_factory=sqlite3.Row;row=c.execute("SELECT users.id,users.username,users.role,users.account_status,sessions.expires_at FROM sessions JOIN users ON users.id=sessions.user_id WHERE sessions.token=?",(token,)).fetchone()
        if row is None:raise HTTPException(401,"Sessão inválida.")
        if row["account_status"]!="active":raise HTTPException(403,"Conta desativada ou bloqueada.")
        if datetime.fromisoformat(row["expires_at"])<=datetime.now(timezone.utc):c.execute("DELETE FROM sessions WHERE token=?",(token,));c.commit();raise HTTPException(401,"Sessão expirada.")
    return dict(row)
def require_admin(user=Depends(get_current_user)):
    if user["role"]!="admin":raise HTTPException(403,"Acesso administrativo necessário.")
    return user
@app.get("/",include_in_schema=False)
def root():return FileResponse(STATIC_DIR/("index.html" if setup_completed() else "setup.html"))
@app.get("/api/setup/status")
def setup_status():return {"completed":setup_completed(),"steps":4}
@app.post("/api/setup/diagnostics")
def setup_diagnostics(request:SetupLocationsRequest=SetupLocationsRequest()):
    paths=[]
    for raw in request.paths:
        text=raw.strip()
        if not text:continue
        p=Path(text).expanduser()
        try:resolved=p.resolve(strict=False)
        except OSError:resolved=p
        paths.append({"path":text,"exists":resolved.exists(),"is_dir":resolved.is_dir(),"readable":os.access(resolved,os.R_OK) if resolved.exists() else False,"writable":os.access(resolved,os.W_OK) if resolved.exists() else False})
    db_ok=False
    try:
        with sqlite3.connect(database_path) as c:c.execute("SELECT 1");db_ok=True
    except sqlite3.Error:pass
    return {"database":"ok" if db_ok else "error","ffmpeg":shutil.which("ffmpeg"),"ffprobe":shutil.which("ffprobe"),"paths":paths,"data_directory":{"path":str(DATA_DIR),"exists":DATA_DIR.exists(),"writable":os.access(DATA_DIR,os.W_OK)}}
@app.post("/api/setup/select-folder")
def setup_select_folder(authorization:str|None=Header(default=None)):
    if setup_completed():
        current=get_current_user(authorization,None)
        require_admin(current)
    try:
        import tkinter as tk
        from tkinter import filedialog
        root=tk.Tk();root.withdraw();root.attributes("-topmost",True)
        try:path=filedialog.askdirectory(title="Selecionar pasta da biblioteca",mustexist=True)
        finally:root.destroy()
    except Exception as exc:
        logger.warning("Native folder picker unavailable: %s",exc)
        raise HTTPException(503,"O seletor nativo de pastas não está disponível neste ambiente.")
    if not path:return {"path":None,"cancelled":True}
    selected=Path(path).resolve()
    if not selected.is_dir():raise HTTPException(422,"A pasta selecionada não existe ou não é uma pasta.")
    return {"path":str(selected),"cancelled":False}
@app.post("/api/setup")
def setup_admin(request:SetupRequest):
    username=request.username.strip()
    if not username:raise HTTPException(422,"O usuário é obrigatório.")
    server_name=request.server_name.strip()
    if not server_name:raise HTTPException(422,"O nome do servidor é obrigatório.")
    libs=[];seen=set()
    for item in request.libraries:
        name=item.name.strip();key=name.casefold()
        if not name:raise HTTPException(422,"O nome da biblioteca é obrigatório.")
        if key in seen:raise HTTPException(422,"Os nomes das bibliotecas devem ser únicos.")
        seen.add(key);locations=list(dict.fromkeys(p.strip() for p in item.locations if p.strip()));libs.append((name,item.library_type,locations))
    with sqlite3.connect(database_path) as c:
        if c.execute("SELECT 1 FROM users LIMIT 1").fetchone() is not None or setup_completed():raise HTTPException(409,"A configuração inicial já foi concluída.")
        now=datetime.now(timezone.utc).isoformat();c.execute("INSERT INTO users(username,password_hash,role,created_at) VALUES(?,?,?,?)",(username,hash_password(request.password),"admin",now))
        settings={"language":request.language,"region":request.region,"timezone":request.timezone,"server_name":server_name,"network_access":request.network_access,"indexing_mode":request.indexing_mode,"playback_mode":request.playback_mode,"library_setup_explicit":"true","setup_completed":"true"}
        for key,value in settings.items():c.execute("INSERT INTO server_settings(key,value) VALUES(?,?)",(key,str(value)))
        for name,library_type,locations in libs:
            cur=c.execute("INSERT INTO media_libraries(name,library_type,created_at,updated_at) VALUES(?,?,?,?)",(name,library_type,now,now))
            for index,path in enumerate(locations):c.execute("INSERT INTO media_library_locations(library_id,path,is_primary,created_at) VALUES(?,?,?,?)",(cur.lastrowid,path,int(index==0),now))
        c.commit()
    return {"status":"ok","username":username,"role":"admin","libraries_created":len(libs),"indexing_mode":request.indexing_mode}
@app.get("/api/v1/settings")
def settings(user=Depends(require_admin)):
    with sqlite3.connect(database_path) as c:rows=c.execute("SELECT key,value FROM server_settings ORDER BY key").fetchall()
    return {"settings":dict(rows)}
@app.put("/api/v1/settings")
def update_settings(request:ServerSettingsUpdate,user=Depends(require_admin)):
    allowed={"language","region","timezone","server_name","network_access","indexing_mode","playback_mode"}
    invalid=set(request.settings)-allowed
    if invalid:raise HTTPException(422,f"Configurações não permitidas: {', '.join(sorted(invalid))}")
    now=datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(database_path) as c:
        for key,value in request.settings.items():
            value=str(value).strip()
            if key in {"server_name","language","region","timezone"} and not value:raise HTTPException(422,f"O valor de {key} é obrigatório.")
            if key=="network_access" and value not in {"local","lan"}:raise HTTPException(422,"network_access inválido.")
            if key=="indexing_mode" and value not in {"later","incremental"}:raise HTTPException(422,"indexing_mode inválido.")
            if key=="playback_mode" and value not in {"automatic","local_first"}:raise HTTPException(422,"playback_mode inválido.")
            c.execute("INSERT INTO server_settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(key,value))
        c.commit()
    logger.info("Server settings updated user=%s keys=%s at=%s",user["username"],sorted(request.settings),now);return {"status":"ok","updated":sorted(request.settings)}
@app.get("/api/v1/profile")
def profile(user=Depends(get_current_user)):return {"id":user["id"],"username":user["username"],"role":user["role"]}
@app.get("/api/v1/profile/preferences")
def get_preferences(user=Depends(get_current_user)):
    with sqlite3.connect(database_path) as c:rows=c.execute("SELECT key,value FROM user_preferences WHERE user_id=? ORDER BY key",(user["id"],)).fetchall()
    return {"preferences":dict(rows)}
@app.put("/api/v1/profile/preferences")
def save_preferences(request:PreferencesUpdate,user=Depends(get_current_user)):
    allowed={"theme","language","resume","autoplay","speed","audio_track","subtitle_track"};invalid=set(request.preferences)-allowed
    if invalid:raise HTTPException(422,f"Preferências não permitidas: {', '.join(sorted(invalid))}")
    now=datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(database_path) as c:
        for key,value in request.preferences.items():c.execute("INSERT INTO user_preferences(user_id,key,value,updated_at) VALUES(?,?,?,?) ON CONFLICT(user_id,key) DO UPDATE SET value=excluded.value,updated_at=excluded.updated_at",(user["id"],key,str(value),now))
        c.commit()
    return {"status":"ok","updated":sorted(request.preferences)}
@app.put("/api/v1/profile/password")
def change_password(request:PasswordChange,user=Depends(get_current_user)):
    if not verify_password(request.current_password,_get_password_hash(user["id"])):raise HTTPException(400,"Senha atual inválida.")
    if request.current_password==request.new_password:raise HTTPException(422,"A nova senha deve ser diferente da senha atual.")
    with sqlite3.connect(database_path) as c:
        c.execute("UPDATE users SET password_hash=? WHERE id=?",(hash_password(request.new_password),user["id"]));c.execute("DELETE FROM sessions WHERE user_id=?",(user["id"],));c.commit()
    return {"status":"ok","message":"Senha alterada. Faça login novamente."}
def _get_password_hash(user_id):
    with sqlite3.connect(database_path) as c:row=c.execute("SELECT password_hash FROM users WHERE id=?",(user_id,)).fetchone()
    if row is None:raise HTTPException(401,"Usuário não encontrado.")
    return row[0]
@app.get("/api/v1/admin/users")
def admin_users(user=Depends(require_admin)):
    with sqlite3.connect(database_path) as c:
        c.row_factory=sqlite3.Row;rows=c.execute("SELECT id,username,role,account_status,created_at FROM users ORDER BY username").fetchall()
    return {"users":[dict(r) for r in rows]}
@app.post("/api/v1/admin/users")
def admin_create_user(request:AdminUserCreate,user=Depends(require_admin)):
    username=request.username.strip()
    if not username:raise HTTPException(422,"O usuário é obrigatório.")
    now=datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(database_path) as c:
        try:cur=c.execute("INSERT INTO users(username,password_hash,role,account_status,created_at) VALUES(?,?,?,?,?)",(username,hash_password(request.password),request.role,"active",now))
        except sqlite3.IntegrityError:raise HTTPException(409,"Já existe um usuário com esse nome.")
        c.commit()
    return {"status":"ok","id":cur.lastrowid,"username":username,"role":request.role}
@app.put("/api/v1/admin/users/{user_id}")
def admin_update_user(user_id:int,request:AdminUserUpdate,user=Depends(require_admin)):
    with sqlite3.connect(database_path) as c:
        row=c.execute("SELECT id,role,account_status FROM users WHERE id=?",(user_id,)).fetchone()
        if row is None:raise HTTPException(404,"Usuário não encontrado.")
        if user_id==user["id"] and request.account_status and request.account_status!="active":raise HTTPException(422,"O administrador atual não pode desativar a própria conta.")
        if request.role is not None and user_id==user["id"] and request.role!="admin":raise HTTPException(422,"O administrador atual não pode remover o próprio privilégio administrativo.")
        if request.role is not None:c.execute("UPDATE users SET role=? WHERE id=?",(request.role,user_id))
        if request.account_status is not None:c.execute("UPDATE users SET account_status=? WHERE id=?",(request.account_status,user_id))
        c.commit()
        if request.account_status and request.account_status!="active":c.execute("DELETE FROM sessions WHERE user_id=?",(user_id,));c.commit()
    return {"status":"ok","id":user_id}
@app.post("/api/v1/admin/users/{user_id}/reset-password")
def admin_reset_password(user_id:int,user=Depends(require_admin)):
    temporary=secrets.token_urlsafe(12)
    with sqlite3.connect(database_path) as c:
        if c.execute("SELECT id FROM users WHERE id=?",(user_id,)).fetchone() is None:raise HTTPException(404,"Usuário não encontrado.")
        c.execute("UPDATE users SET password_hash=? WHERE id=?",(hash_password(temporary),user_id));c.execute("DELETE FROM sessions WHERE user_id=?",(user_id,));c.commit()
    return {"status":"ok","temporary_password":temporary,"message":"Senha temporária gerada. Entregue-a de forma segura e solicite a troca no próximo acesso."}
@app.get("/api/v1/libraries")
def list_libraries(user=Depends(require_admin)):
    with sqlite3.connect(database_path) as c:
        c.row_factory=sqlite3.Row;libraries=c.execute("SELECT id,name,library_type,created_at,updated_at FROM media_libraries ORDER BY name").fetchall();result=[]
        for lib in libraries:
            locations=c.execute("SELECT id,path,is_primary FROM media_library_locations WHERE library_id=? ORDER BY id",(lib["id"],)).fetchall();item=dict(lib);item["locations"]=[dict(x) for x in locations];result.append(item)
    return {"libraries":result}
@app.post("/api/v1/libraries")
def create_library(request:LibraryCreate,user=Depends(require_admin)):
    name=request.name.strip();locations=list(dict.fromkeys(p.strip() for p in request.locations if p.strip()))
    if not name:raise HTTPException(422,"O nome da biblioteca é obrigatório.")
    now=datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(database_path) as c:
        try:cur=c.execute("INSERT INTO media_libraries(name,library_type,created_at,updated_at) VALUES(?,?,?,?)",(name,request.library_type,now,now))
        except sqlite3.IntegrityError:raise HTTPException(409,"Já existe uma biblioteca com esse nome.")
        for index,path in enumerate(locations):c.execute("INSERT INTO media_library_locations(library_id,path,is_primary,created_at) VALUES(?,?,?,?)",(cur.lastrowid,path,int(index==0),now))
        c.commit()
    return {"status":"ok","id":cur.lastrowid,"name":name}
@app.put("/api/v1/libraries/{library_id}")
def update_library(library_id:int,request:LibraryUpdate,user=Depends(require_admin)):
    with sqlite3.connect(database_path) as c:
        if c.execute("SELECT id FROM media_libraries WHERE id=?",(library_id,)).fetchone() is None:raise HTTPException(404,"Biblioteca não encontrada.")
        if request.name is not None:
            try:c.execute("UPDATE media_libraries SET name=? WHERE id=?",(request.name.strip(),library_id))
            except sqlite3.IntegrityError:raise HTTPException(409,"Já existe uma biblioteca com esse nome.")
        if request.library_type is not None:c.execute("UPDATE media_libraries SET library_type=? WHERE id=?",(request.library_type,library_id))
        if request.locations is not None:
            locations=list(dict.fromkeys(p.strip() for p in request.locations if p.strip()));c.execute("DELETE FROM media_library_locations WHERE library_id=?",(library_id,));now=datetime.now(timezone.utc).isoformat()
            for index,path in enumerate(locations):c.execute("INSERT INTO media_library_locations(library_id,path,is_primary,created_at) VALUES(?,?,?,?)",(library_id,path,int(index==0),now))
        c.execute("UPDATE media_libraries SET updated_at=? WHERE id=?",(datetime.now(timezone.utc).isoformat(),library_id));c.commit()
    return {"status":"ok","id":library_id}
@app.delete("/api/v1/libraries/{library_id}")
def delete_library(library_id:int,user=Depends(require_admin)):
    with sqlite3.connect(database_path) as c:
        if c.execute("SELECT id FROM media_libraries WHERE id=?",(library_id,)).fetchone() is None:raise HTTPException(404,"Biblioteca não encontrada.")
        c.execute("DELETE FROM media_libraries WHERE id=?",(library_id,));c.commit()
    logger.info("Media library removed user=%s library_id=%s; media files are untouched",user["username"],library_id);return {"status":"ok","id":library_id}
@app.get("/health")
def health():return {"status":"ok"}
@app.get("/api/v1")
def api_info():return {"service":"KryptonPlay","api":"v1","version":"0.1.0"}
@app.get("/api/v1/status")
def api_status():
    db_ok=False
    try:
        with sqlite3.connect(database_path) as c:c.execute("SELECT 1").fetchone();db_ok=True
    except sqlite3.Error:pass
    with sqlite3.connect(database_path) as c:rows=c.execute("SELECT path FROM media_library_locations").fetchall();paths=[Path(r[0]) for r in rows]
    library_ok=any(p.exists() and p.is_dir() for p in paths);ffmpeg_ok=shutil.which("ffmpeg") is not None;storage_ok=any(p.exists() for p in paths)
    components={"server":"ok","database":"ok" if db_ok else "error","library":"ok" if library_ok else "error","storage":"ok" if storage_ok else "error","ffmpeg":"ok" if ffmpeg_ok else "warning","api":"ok"};overall="ok" if all(v=="ok" for k,v in components.items() if k!="ffmpeg") else "error"
    return {"status":overall,"service":"KryptonPlay","version":"0.1.0","components":components,"log_file":str(LOG_PATH)}
@app.get("/api/auth/users")
def auth_users():
    with sqlite3.connect(database_path) as c:
        c.row_factory=sqlite3.Row;rows=c.execute("SELECT id,username,role FROM users WHERE account_status='active' ORDER BY username").fetchall()
    return {"users":[{"id":r["id"],"username":r["username"],"role":r["role"]} for r in rows]}
@app.post("/api/auth/login")
def login(request:LoginRequest,response:Response):
    with sqlite3.connect(database_path) as c:
        c.row_factory=sqlite3.Row;row=c.execute("SELECT id,username,password_hash,role,account_status FROM users WHERE username=?",(request.username,)).fetchone()
        if row is None or not verify_password(request.password,row["password_hash"]):raise HTTPException(401,"Usuário ou senha inválidos.")
        if row["account_status"]!="active":raise HTTPException(403,"Conta desativada ou bloqueada.")
        token=secrets.token_urlsafe(32);expires_at=datetime.now(timezone.utc)+timedelta(hours=SESSION_HOURS);c.execute("INSERT INTO sessions(token,user_id,expires_at) VALUES(?,?,?)",(token,row["id"],expires_at.isoformat()));c.commit()
    response.set_cookie(key=SESSION_COOKIE,value=token,max_age=SESSION_HOURS*60*60,httponly=True,samesite="lax",secure=False,path="/");return {"access_token":token,"token_type":"bearer","expires_at":expires_at.isoformat(),"user":{"username":row["username"],"role":row["role"]}}
@app.post("/api/auth/logout")
def logout(response:Response,authorization:str|None=Header(default=None),session_cookie:str|None=Cookie(default=None,alias=SESSION_COOKIE),user=Depends(get_current_user)):
    token=authorization[7:].strip() if authorization and authorization.lower().startswith("bearer ") else session_cookie.strip() if session_cookie else None
    with sqlite3.connect(database_path) as c:c.execute("DELETE FROM sessions WHERE token=?",(token,));c.commit()
    response.delete_cookie(key=SESSION_COOKIE,path="/");return {"status":"ok"}
@app.get("/api/auth/me")
def me(user=Depends(get_current_user)):
    with sqlite3.connect(database_path) as c:row=c.execute("SELECT id,username,role,account_status FROM users WHERE id=?",(user["id"],)).fetchone()
    return {"id":row[0],"username":row[1],"role":row[2],"account_status":row[3]}
@app.get("/api/v1/library")
def library(q:str|None=Query(default=None,max_length=200),media_type:str|None=Query(default=None,alias="type",pattern="^(movie|series)$"),user=Depends(get_current_user)):
    clauses=[];params=[]
    if q and q.strip():clauses.append("LOWER(title) LIKE LOWER(?)");params.append(f"%{q.strip()}%")
    if media_type:clauses.append("media_type=?");params.append(media_type)
    where=f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with sqlite3.connect(database_path) as c:c.row_factory=sqlite3.Row;rows=c.execute(f"SELECT id,title,media_type,file_size,modified_at FROM media_items {where} ORDER BY title",params).fetchall()
    return {"items":[dict(r) for r in rows]}
@app.get("/api/v1/media/{media_id}/stream",include_in_schema=False)
def stream_media(media_id:int,user=Depends(get_current_user)):
    with sqlite3.connect(database_path) as c:row=c.execute("SELECT file_path FROM media_items WHERE id=?",(media_id,)).fetchone()
    if row is None:raise HTTPException(404,"Mídia não encontrada.")
    path=Path(row[0]).resolve()
    if not path.is_file():raise HTTPException(404,"Arquivo de mídia não encontrado.")
    return FileResponse(path,media_type=guess_type(path.name)[0] or "application/octet-stream",content_disposition_type="inline")
@app.get("/api/v1/media/{media_id}/progress")
def get_progress(media_id:int,user=Depends(get_current_user)):
    with sqlite3.connect(database_path) as c:
        if c.execute("SELECT id FROM media_items WHERE id=?",(media_id,)).fetchone() is None:raise HTTPException(404,"Mídia não encontrada.")
        row=c.execute("SELECT position_seconds,duration_seconds,completed FROM playback_progress WHERE media_id=?",(media_id,)).fetchone()
    return {"media_id":media_id,"position_seconds":row[0] if row else 0.0,"duration_seconds":(row[1] or 0.0) if row else 0.0,"completed":bool(row[2]) if row else False}
@app.put("/api/v1/media/{media_id}/progress")
def save_progress(media_id:int,progress:ProgressUpdate,user=Depends(get_current_user)):
    if progress.duration_seconds is not None and progress.position_seconds>progress.duration_seconds:raise HTTPException(422,"Posição não pode exceder a duração.")
    with sqlite3.connect(database_path) as c:
        if c.execute("SELECT id FROM media_items WHERE id=?",(media_id,)).fetchone() is None:raise HTTPException(404,"Mídia não encontrada.")
        now=datetime.now(timezone.utc).isoformat();c.execute("INSERT INTO playback_progress(media_id,position_seconds,duration_seconds,completed,updated_at) VALUES(?,?,?,?,?) ON CONFLICT(media_id) DO UPDATE SET position_seconds=excluded.position_seconds,duration_seconds=excluded.duration_seconds,completed=excluded.completed,updated_at=excluded.updated_at",(media_id,progress.position_seconds,progress.duration_seconds,int(progress.completed),now));c.commit()
    return {"status":"ok","media_id":media_id,"position_seconds":progress.position_seconds,"duration_seconds":progress.duration_seconds or 0.0,"completed":progress.completed,"updated_at":now}
@app.get("/api/v1/media/{media_id}/stats")
def get_stats(media_id:int,user=Depends(get_current_user)):
    with sqlite3.connect(database_path) as c:
        if c.execute("SELECT id FROM media_items WHERE id=?",(media_id,)).fetchone() is None:raise HTTPException(404,"Mídia não encontrada.")
        row=c.execute("SELECT play_count,watched_seconds,updated_at FROM playback_stats WHERE media_id=?",(media_id,)).fetchone()
    return {"media_id":media_id,"play_count":row[0] if row else 0,"watched_seconds":row[1] if row else 0.0,"updated_at":row[2] if row else None}
@app.post("/api/v1/media/{media_id}/stats")
def record_playback_event(media_id:int,event:PlaybackEvent,user=Depends(get_current_user)):
    with sqlite3.connect(database_path) as c:
        if c.execute("SELECT id FROM media_items WHERE id=?",(media_id,)).fetchone() is None:raise HTTPException(404,"Mídia não encontrada.")
        now=datetime.now(timezone.utc).isoformat();c.execute("INSERT INTO playback_stats(media_id,play_count,watched_seconds,updated_at) VALUES(?,?,?,?) ON CONFLICT(media_id) DO UPDATE SET play_count=playback_stats.play_count+excluded.play_count,watched_seconds=playback_stats.watched_seconds+excluded.watched_seconds,updated_at=excluded.updated_at",(media_id,int(event.started),event.watched_seconds,now));c.commit();row=c.execute("SELECT play_count,watched_seconds FROM playback_stats WHERE media_id=?",(media_id,)).fetchone()
    return {"status":"ok","media_id":media_id,"play_count":row[0],"watched_seconds":row[1],"updated_at":now}
@app.post("/api/v1/library/scan")
def scan(user=Depends(require_admin)):
    with sqlite3.connect(database_path) as c:rows=c.execute("SELECT path FROM media_library_locations ORDER BY id").fetchall()
    scan_paths=[Path(r[0]) for r in rows];total=0
    for path in scan_paths:
        if not path.is_dir():logger.warning("Skipping unavailable library path=%s",path);continue
        total+=scan_library(path,database_path)
    return {"status":"ok","items_scanned":total,"paths_scanned":len(scan_paths)}
logger.info("Server started version=0.1.0 host=%s port=%s",server_config["host"],server_config["port"])
if __name__=="__main__":
    import uvicorn;uvicorn.run("app:app",host=server_config["host"],port=server_config["port"],reload=False)
