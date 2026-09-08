"""Runtime UI overlays and first-login enforcement."""
from __future__ import annotations
import json,re,sqlite3,subprocess,sys,threading,time,os
from pathlib import Path
from fastapi import Depends
from fastapi.responses import HTMLResponse

def install(app_module):
    app=app_module.app;db=app_module.database_path
    @app.get('/api/v1/account/security-status')
    def security_status(user=Depends(app_module.get_current_user)):
        with sqlite3.connect(db) as c:r=c.execute('SELECT must_change_password FROM users WHERE id=?',(user['id'],)).fetchone()
        return {'must_change_password':bool(r and r[0])}
    @app.middleware('http')
    async def ui_runtime(request,call_next):
        path=request.url.path;uid=None;reset_uid=None
        if path=='/api/v1/profile/password' or re.fullmatch(r'/api/v1/admin/users/\d+/reset-password',path):
            auth=request.headers.get('authorization','');token=auth[7:].strip() if auth.lower().startswith('bearer ') else request.cookies.get(app_module.SESSION_COOKIE)
            if token:
                with sqlite3.connect(db) as c:r=c.execute('SELECT user_id FROM sessions WHERE token=?',(token,)).fetchone();uid=r[0] if r else None
            if path.startswith('/api/v1/admin/users/'):reset_uid=int(path.split('/')[5])
        if path=='/api/v1/admin/server/restart' and request.method=='POST':
            auth=request.headers.get('authorization','');token=auth[7:].strip() if auth.lower().startswith('bearer ') else request.cookies.get(app_module.SESSION_COOKIE);role=None
            if token:
                with sqlite3.connect(db) as c:r=c.execute('SELECT users.role FROM sessions JOIN users ON users.id=sessions.user_id WHERE sessions.token=?',(token,)).fetchone();role=r[0] if r else None
            if role!='admin':return app_module.Response(content=json.dumps({'detail':'Acesso administrativo necessário.'}),status_code=403,media_type='application/json')
            if not getattr(sys,'frozen',False):return app_module.Response(content=json.dumps({'detail':'O reinício pelo painel está disponível na instalação do KryptonPlay.'}),status_code=409,media_type='application/json')
            exe=Path(sys.executable).resolve();subprocess.Popen([str(exe),'--restart-child'],cwd=str(exe.parent),creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),close_fds=True);threading.Thread(target=lambda:(time.sleep(1),os._exit(0)),daemon=True).start();return app_module.Response(content=json.dumps({'status':'restarting'}),media_type='application/json')
        if path.startswith('/api/') and path not in {'/api/auth/login','/api/auth/users','/api/auth/me','/api/v1/profile/custom','/api/v1/profile/password','/api/v1/profile/preferences','/api/v1/time','/api/v1/account/security-status'}:
            auth=request.headers.get('authorization','');token=auth[7:].strip() if auth.lower().startswith('bearer ') else request.cookies.get(app_module.SESSION_COOKIE)
            if token:
                with sqlite3.connect(db) as c:r=c.execute('SELECT users.must_change_password FROM sessions JOIN users ON users.id=sessions.user_id WHERE sessions.token=?',(token,)).fetchone()
                if r and int(r[0] or 0):return app_module.Response(content=json.dumps({'detail':'Senha temporária: altere sua senha antes de continuar.'}),status_code=428,media_type='application/json')
        response=await call_next(request)
        if path=='/api/v1/profile/password' and response.status_code<300 and uid:
            with sqlite3.connect(db) as c:c.execute('UPDATE users SET must_change_password=0 WHERE id=?',(uid,));c.commit()
        if reset_uid and response.status_code<300:
            with sqlite3.connect(db) as c:c.execute('UPDATE users SET must_change_password=1 WHERE id=?',(reset_uid,));c.commit()
        if path in {'/static/player.html','/static/settings.html'} and response.status_code==200:
            try:
                body=b''.join([chunk async for chunk in response.body_iterator]);html=body.decode('utf-8')
                if path.endswith('player.html'):
                    html=html.replace("let preferences={theme:'system'","let preferences={theme:'dark'").replace("theme:p.theme||'system'","theme:p.theme||'dark'");html=html.replace('</style>','body[data-theme="oled"]{background:#000;color:#eee}body[data-theme="oled"] header{border-color:#222}body[data-theme="oled"] .panel,body[data-theme="oled"] .card,body[data-theme="oled"] .modal-card{background:#050505;border-color:#222}body[data-theme="oled"] input,body[data-theme="oled"] select,body[data-theme="oled"] button{background:#000;color:#eee;border-color:#333}</style>',1);script='''<script>const _kpShowApp=showApp;showApp=async function(){try{const r=await api('/api/v1/account/security-status');if(r.ok){const d=await r.json();if(d.must_change_password){showPasswordGate();return}}}catch(e){}await _kpShowApp()};function showPasswordGate(){if(document.getElementById('temporary-password-gate'))return;const m=document.createElement('div');m.id='temporary-password-gate';m.className='modal';m.innerHTML='<article class="modal-card"><h2>Senha temporária</h2><p>Sua senha atual é temporária e precisa ser alterada antes de continuar usando o KryptonPlay.</p><button class="primary" id="go-password-settings">Alterar minha senha</button></article>';document.body.appendChild(m);document.getElementById('go-password-settings').onclick=()=>location.href='/static/settings.html#security'}</script>'''
                else:
                    html=html.replace('</style>','body[data-theme="oled"]{background:#000;color:#eee}body[data-theme="oled"] .sidebar{background:#000;border-color:#222}body[data-theme="oled"] .card,body[data-theme="oled"] .library,body[data-theme="oled"] .user-row{background:#050505;border-color:#222}</style>',1);script='''<script>(function(){const langs=[['pt-BR','Português (Brasil)'],['pt-PT','Português (Portugal)'],['en','English'],['es','Español'],['fr','Français'],['de','Deutsch'],['it','Italiano'],['ja','日本語'],['ko','한국어'],['zh-CN','中文（简体）']];for(const id of ['language','server_language']){const s=document.getElementById(id);if(s){const old=s.value;s.innerHTML=langs.map(x=>`<option value="${x[0]}">${x[1]}</option>`).join('');s.value=old||'pt-BR'}}const theme=document.getElementById('theme');if(theme){theme.innerHTML='<option value="dark">Escuro</option><option value="oled">OLED / Preto</option><option value="light">Claro</option>';theme.value=theme.value||'dark'}const pw=document.getElementById('new-user-password');if(pw){pw.type='text';pw.readOnly=true;pw.placeholder='Gere uma senha temporária';const g=document.createElement('button');g.type='button';g.textContent='Gerar senha temporária';g.onclick=()=>{const chars='ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%';const a=new Uint32Array(18);crypto.getRandomValues(a);pw.value=Array.from(a,n=>chars[n%chars.length]).join('')};pw.parentElement.appendChild(g)}window.createUser=async function(){const name=document.getElementById('new-username').value.trim();const p=document.getElementById('new-user-password');if(!name){showMessage('user-message','Informe o usuário.',true);return}if(!p.value)p.parentElement.querySelector('button')?.click();const r=await api('/api/v1/admin/users/temporary',{method:'POST',body:JSON.stringify({username:name,role:'user'})});const d=await r.json().catch(()=>({}));if(!r.ok){showMessage('user-message',d.detail||'Não foi possível criar o usuário.',true);return}p.value=d.temporary_password||'';navigator.clipboard?.writeText(p.value).catch(()=>{});showMessage('user-message','Usuário criado. Senha temporária copiada.');if(typeof loadUsers==='function')loadUsers()};if(location.hash==='#security'&&typeof showSection==='function')setTimeout(()=>showSection('security'),100)})();</script>'''
                html=html.replace('</body>',script+'</body>',1);headers=dict(response.headers);headers.pop('content-length',None);return HTMLResponse(html,status_code=response.status_code,headers=headers)
            except Exception:return response
        return response
