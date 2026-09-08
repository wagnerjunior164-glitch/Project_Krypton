"""Administrative runtime features for KryptonPlay."""
from __future__ import annotations
import json, os, sqlite3, subprocess, sys, threading, time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones
from fastapi import Depends, HTTPException
from fastapi.responses import HTMLResponse
from update_service import download_installer, latest_release

DEFAULTS={"auto_update_enabled":"true","auto_update_time":"03:00","clock_24h":"true","date_format":"DD/MM/YYYY"}
LANGUAGES=[("pt-BR","Português (Brasil)"),("pt-PT","Português (Portugal)"),("en","English"),("es","Español"),("fr","Français"),("de","Deutsch"),("it","Italiano"),("ja","日本語"),("ko","한국어"),("zh-CN","中文（简体）")]

def _db(a): return a.database_path
def _setting(a,k,d=""):
    with sqlite3.connect(_db(a)) as c:r=c.execute("SELECT value FROM server_settings WHERE key=?",(k,)).fetchone()
    return str(r[0]) if r else d
def _set(a,values):
    with sqlite3.connect(_db(a)) as c:
        for k,v in values.items():c.execute("INSERT INTO server_settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(k,str(v)))
        c.commit()
def _valid_zone(n):
    try: ZoneInfo(n); return True
    except (ZoneInfoNotFoundError,ValueError): return False
def _now(a):
    z=_setting(a,"timezone","America/Sao_Paulo")
    try:return datetime.now(ZoneInfo(z))
    except (ZoneInfoNotFoundError,ValueError):return datetime.now(timezone.utc)
def _notification_table(a):
    with sqlite3.connect(_db(a)) as c:
        c.execute("CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,kind TEXT NOT NULL,title TEXT NOT NULL,message TEXT NOT NULL,details TEXT, fixed INTEGER NOT NULL DEFAULT 1,read_at TEXT,created_at TEXT NOT NULL)");c.commit()
def _notify(a,title,message,details=None,kind="system"):
    _notification_table(a);now=datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(_db(a)) as c:
        for (uid,) in c.execute("SELECT id FROM users WHERE role='admin' AND account_status='active'").fetchall():c.execute("INSERT INTO notifications(user_id,kind,title,message,details,fixed,created_at) VALUES(?,?,?,?,?,?,?)",(uid,kind,title,message,json.dumps(details or [],ensure_ascii=False),1,now))
        c.commit()
def _summary(r):
    notes=str(r.get("release_notes") or "").strip(); lines=[x.strip(" -*") for x in notes.splitlines() if x.strip()]
    return lines[:20] or [f"Atualização do KryptonPlay para a versão {r.get('latest_version')}."]
def _start(a,r,automatic=False):
    if not getattr(sys,"frozen",False):raise RuntimeError("Atualizações instaláveis exigem a versão instalada do KryptonPlay.")
    base=Path(sys.executable).resolve().parent;updater=base/"KryptonPlay-Updater.exe"
    if not updater.is_file():raise RuntimeError("O atualizador separado não está instalado.")
    installer=download_installer();app=base/"KryptonPlay.exe"
    if not app.is_file():installer.unlink(missing_ok=True);raise RuntimeError("O executável principal do KryptonPlay não foi encontrado.")
    marker=base/"data"/"pending-update.json";marker.parent.mkdir(parents=True,exist_ok=True)
    marker.write_text(json.dumps({"from":r["current_version"],"to":r["latest_version"],"changes":_summary(r),"automatic":automatic},ensure_ascii=False),encoding="utf-8")
    subprocess.Popen([str(updater),"--installer",str(installer),"--parent-pid",str(os.getpid()),"--app",str(app)],cwd=str(base),creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0),close_fds=True)
    return {"update_started":True,"current_version":r["current_version"],"latest_version":r["latest_version"]}
def _consume(a):
    base=Path(sys.executable).resolve().parent if getattr(sys,"frozen",False) else Path(__file__).resolve().parent;marker=base/"data"/"pending-update.json"
    if not marker.is_file():return
    try:
        p=json.loads(marker.read_text(encoding="utf-8"));to=str(p.get("to",""))
        if to and to==str(a.app.version):_notify(a,f"KryptonPlay atualizado para {to}","A atualização foi concluída. As alterações realizadas permanecem fixadas até o Administrador ler esta notificação.",p.get("changes") or [],"update_completed")
        marker.unlink(missing_ok=True)
    except Exception:pass

def install(a):
    app=a.app;_notification_table(a)
    with sqlite3.connect(_db(a)) as c:
        for k,v in DEFAULTS.items():c.execute("INSERT OR IGNORE INTO server_settings(key,value) VALUES(?,?)",(k,v))
        c.commit()
    _consume(a)
    @app.get("/api/v1/admin/updates/settings")
    def get_update_settings(user=Depends(a.require_admin)):
        return {"enabled":_setting(a,"auto_update_enabled","true")=="true","time":_setting(a,"auto_update_time","03:00"),"timezone":_setting(a,"timezone","America/Sao_Paulo"),"clock_24h":_setting(a,"clock_24h","true")=="true","date_format":_setting(a,"date_format","DD/MM/YYYY")}
    @app.put("/api/v1/admin/updates/settings")
    def put_update_settings(payload:dict,user=Depends(a.require_admin)):
        enabled=bool(payload.get("enabled",True));when=str(payload.get("time","03:00"));zone=str(payload.get("timezone",_setting(a,"timezone","America/Sao_Paulo")))
        try:h,m=map(int,when.split(":",1))
        except ValueError:raise HTTPException(422,"Horário inválido. Use HH:MM.")
        if len(when)!=5 or not(0<=h<=23 and 0<=m<=59):raise HTTPException(422,"Horário inválido. Use HH:MM.")
        if not _valid_zone(zone):raise HTTPException(422,"Fuso horário inválido.")
        fmt=str(payload.get("date_format","DD/MM/YYYY"));
        if fmt not in {"DD/MM/YYYY","YYYY-MM-DD","MM/DD/YYYY"}:raise HTTPException(422,"Formato de data inválido.")
        _set(a,{"auto_update_enabled":str(enabled).lower(),"auto_update_time":when,"timezone":zone,"clock_24h":str(bool(payload.get("clock_24h",True))).lower(),"date_format":fmt});return {"status":"ok"}
    @app.get("/api/v1/admin/updates/check")
    def admin_check(user=Depends(a.require_admin)):
        try:return latest_release()
        except Exception as exc:raise HTTPException(503,f"Não foi possível verificar atualizações: {exc}") from exc
    @app.post("/api/v1/admin/updates/apply")
    def admin_apply(payload:dict|None=None,user=Depends(a.require_admin)):
        try:
            r=latest_release()
            if not r["update_available"]:return {"update_started":False,"update_available":False,"current_version":r["current_version"],"latest_version":r["latest_version"]}
            return _start(a,r,False)
        except Exception as exc:raise HTTPException(503,f"Não foi possível iniciar a atualização: {exc}") from exc
    @app.get("/api/v1/admin/notifications")
    def get_notifications(user=Depends(a.require_admin)):
        with sqlite3.connect(_db(a)) as c:
            c.row_factory=sqlite3.Row;rows=c.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY id DESC LIMIT 50",(user["id"],)).fetchall()
        return {"notifications":[dict(r)|{"details":json.loads(r["details"] or "[]")} for r in rows]}
    @app.post("/api/v1/admin/notifications/{nid}/read")
    def read_notification(nid:int,user=Depends(a.require_admin)):
        with sqlite3.connect(_db(a)) as c:c.execute("UPDATE notifications SET read_at=? WHERE id=? AND user_id=?",(datetime.now(timezone.utc).isoformat(),nid,user["id"]));c.commit()
        return {"status":"ok"}
    @app.get("/api/v1/time")
    def server_time(user=Depends(a.get_current_user)):
        n=_now(a);return {"timezone":_setting(a,"timezone","America/Sao_Paulo"),"iso":n.isoformat(),"date":n.strftime("%d/%m/%Y"),"time_24h":n.strftime("%H:%M:%S"),"time_12h":n.strftime("%I:%M:%S %p"),"clock_24h":_setting(a,"clock_24h","true")=="true","date_format":_setting(a,"date_format","DD/MM/YYYY")}
    @app.get("/api/v1/timezones")
    def timezones(user=Depends(a.get_current_user)):
        return {"timezones":sorted(z for z in available_timezones() if "/" in z or z=="UTC")}
    @app.get("/api/v1/languages")
    def languages(user=Depends(a.get_current_user)):return {"languages":[{"code":c,"name":n} for c,n in LANGUAGES]}
    @app.post("/api/v1/admin/server/restart")
    def restart_server(user=Depends(a.require_admin)):
        if not getattr(sys,"frozen",False):raise HTTPException(409,"O reinício pelo painel está disponível na instalação do KryptonPlay.")
        exe=Path(sys.executable).resolve();subprocess.Popen([str(exe),"--restart-child"],cwd=str(exe.parent),creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0),close_fds=True);return {"status":"restarting"}
    @app.middleware("http")
    async def runtime_guard(request,call_next):
        path=request.url.path
        if path.startswith("/api/") and path not in {"/api/auth/login","/api/auth/users","/api/auth/me","/api/v1/profile/custom","/api/v1/profile/password","/api/v1/profile/preferences","/api/v1/time"}:
            auth=request.headers.get("authorization","");token=auth[7:].strip() if auth.lower().startswith("bearer ") else request.cookies.get(a.SESSION_COOKIE)
            if token:
                with sqlite3.connect(_db(a)) as c:row=c.execute("SELECT users.must_change_password FROM sessions JOIN users ON users.id=sessions.user_id WHERE sessions.token=?",(token,)).fetchone()
                if row and int(row[0] or 0):return a.Response(content=json.dumps({"detail":"Senha temporária: altere sua senha antes de continuar."}),status_code=428,media_type="application/json")
        response=await call_next(request)
        if path=="/api/v1/profile/password" and response.status_code<300:
            auth=request.headers.get("authorization","");token=auth[7:].strip() if auth.lower().startswith("bearer ") else request.cookies.get(a.SESSION_COOKIE)
            if token:
                with sqlite3.connect(_db(a)) as c:
                    row=c.execute("SELECT user_id FROM sessions WHERE token=?",(token,)).fetchone()
                    if row:c.execute("UPDATE users SET must_change_password=0 WHERE id=?",(row[0],));c.commit()
        return response
    @app.middleware("http")
    async def settings_ui(request,call_next):
        if request.url.path=="/static/settings.html":
            static=a.STATIC_DIR/"settings.html"
            try:
                html=static.read_text(encoding="utf-8")
                nav='<button data-section="updates" class="admin-only">Atualizações</button><button data-section="server" class="admin-only">Servidor</button>'
                html=html.replace('<button data-section="server" class="admin-only">Servidor</button>',nav,1)
                section='''<section id="updates" class="section admin-only"><h2>Atualizações</h2><p class="description">Controle as atualizações oficiais do KryptonPlay. O horário programado usa o fuso horário configurado no servidor.</p><div class="card"><div class="row"><label><input id="auto-update" type="checkbox"> Atualizações automáticas</label></div><div class="grid"><div class="field"><label>Horário da atualização automática</label><input id="update-time" type="time" value="03:00"></div><div class="field"><label>Fuso horário do servidor</label><select id="update-timezone"></select></div></div><div class="form-actions"><button class="primary" onclick="checkKryptonUpdate()">Verificar atualização agora</button><button onclick="restartKryptonServer()">Reiniciar servidor</button></div><div id="update-result" class="status" style="margin-top:14px">Nenhuma verificação executada.</div></div><div class="card" style="margin-top:14px"><h3>Data e horário do servidor</h3><div id="server-clock" class="status">Carregando…</div><div class="grid"><div class="field"><label>Formato do relógio</label><select id="clock-format"><option value="24">24 horas</option><option value="12">12 horas</option></select></div><div class="field"><label>Formato da data</label><select id="date-format"><option value="DD/MM/YYYY">DD/MM/AAAA</option><option value="YYYY-MM-DD">AAAA-MM-DD</option><option value="MM/DD/YYYY">MM/DD/AAAA</option></select></div></div><button class="primary" onclick="saveKryptonUpdateSettings()">Salvar configurações</button></div><div id="update-notifications" style="margin-top:14px"></div></section>'''
                html=html.replace('<section id="diagnostics"',section+'<section id="diagnostics"',1)
                html=html.replace('</style>','body[data-theme="oled"]{background:#000;color:#eee}body[data-theme="oled"] .sidebar{background:#000;border-color:#222}body[data-theme="oled"] .card,body[data-theme="oled"] .library,body[data-theme="oled"] .user-row{background:#050505;border-color:#222}body[data-theme="oled"] button,body[data-theme="oled"] input,body[data-theme="oled"] select,body[data-theme="oled"] textarea{background:#000;color:#eee;border-color:#333} </style>',1)
                script='''<script>
async function loadAdminExtras(){if(!$('auto-update'))return;let u=await api('/api/auth/me');if(!u.ok)return;let me=await u.json();if(me.role!=='admin'){document.querySelector('[data-section="updates"]')?.remove();$('updates')?.remove();return}let s=await api('/api/v1/admin/updates/settings');if(s.ok){let d=await s.json();$('auto-update').checked=d.enabled;$('update-time').value=d.time;$('clock-format').value=d.clock_24h?'24':'12';$('date-format').value=d.date_format;await loadZones(d.timezone)}loadClock();loadUpdateNotifications()}
async function loadZones(selected){let r=await api('/api/v1/timezones');if(!r.ok)return;let d=await r.json();$('update-timezone').innerHTML=d.timezones.map(z=>`<option value="${esc(z)}">${esc(z)}</option>`).join('');$('update-timezone').value=selected||'America/Sao_Paulo'}
async function loadClock(){let r=await api('/api/v1/time');if(!r.ok)return;let d=await r.json();$('server-clock').textContent=`${d.date} · ${d.clock_24h?d.time_24h:d.time_12h} · ${d.timezone}`;setTimeout(loadClock,1000)}
async function saveKryptonUpdateSettings(){let r=await api('/api/v1/admin/updates/settings',{method:'PUT',body:JSON.stringify({enabled:$('auto-update').checked,time:$('update-time').value,timezone:$('update-timezone').value,clock_24h:$('clock-format').value==='24',date_format:$('date-format').value})});$('update-result').textContent=r.ok?'Configurações salvas.':'Não foi possível salvar as configurações.';if(r.ok)loadClock()}
async function checkKryptonUpdate(){let box=$('update-result');box.textContent='Verificando…';let r=await api('/api/v1/admin/updates/check');if(!r.ok){box.textContent=(await r.json().catch(()=>({}))).detail||'Falha na verificação.';return}let d=await r.json();if(!d.update_available){box.textContent=`Nenhuma atualização disponível. Versão atual: ${d.current_version}.`;return}let changes=(d.release_notes||'Nenhuma descrição publicada.').trim();box.innerHTML=`<strong>Atualização disponível: ${esc(d.current_version)} → ${esc(d.latest_version)}</strong><p>${esc(changes).replace(/\n/g,'<br>')}</p><button class="primary" id="confirm-update">Confirmar atualização</button> <button id="cancel-update">Cancelar</button>`;$('confirm-update').onclick=async()=>{if(!confirm(`Confirma explicitamente a atualização do KryptonPlay de ${d.current_version} para ${d.latest_version}?`))return;let a=await api('/api/v1/admin/updates/apply',{method:'POST',body:'{}'});box.textContent=a.ok?'Atualização iniciada. O KryptonPlay será reiniciado automaticamente.':((await a.json().catch(()=>({}))).detail||'Falha ao iniciar atualização.')};$('cancel-update').onclick=()=>{box.textContent='Atualização cancelada pelo Administrador.'}}
async function loadUpdateNotifications(){let r=await api('/api/v1/admin/notifications');if(!r.ok)return;let d=await r.json();let unread=d.notifications.filter(n=>!n.read_at);$('update-notifications').innerHTML=unread.map(n=>`<div class="card" style="border:2px solid #777;margin-bottom:10px"><h3>${esc(n.title)}</h3><p>${esc(n.message)}</p>${n.details?.length?'<ul>'+n.details.map(x=>`<li>${esc(x)}</li>`).join('')+'</ul>':''}<button onclick="readKryptonNotification(${n.id})">Marcar como lida</button></div>`).join('');}
async function readKryptonNotification(id){await api(`/api/v1/admin/notifications/${id}/read`,{method:'POST'});loadUpdateNotifications()}
async function restartKryptonServer(){if(!confirm('Reiniciar o servidor KryptonPlay agora? A interface reconectará após o reinício.'))return;await api('/api/v1/admin/server/restart',{method:'POST'});$('update-result').textContent='Servidor reiniciando…'}
setTimeout(loadAdminExtras,0);
</script>'''
                html=html.replace('</body>',script+'</body>',1)
                return HTMLResponse(html)
            except Exception:pass
        return await call_next(request)
    def scheduler():
        last=None
        while True:
            try:
                if _setting(a,"auto_update_enabled","true")=="true":
                    n=_now(a);target=_setting(a,"auto_update_time","03:00");key=f"{n.date()} {target}"
                    if n.strftime("%H:%M")==target and key!=last:
                        last=key;r=latest_release()
                        if r["update_available"]:_notify(a,f"Atualização automática {r['latest_version']}","A atualização programada foi aplicada no horário local do servidor.",_summary(r),"update_started");_start(a,r,True)
            except Exception:pass
            time.sleep(30)
    threading.Thread(target=scheduler,name="KryptonPlayUpdateScheduler",daemon=True).start()
