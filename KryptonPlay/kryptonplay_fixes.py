import base64, hashlib, json, secrets, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from fastapi import Depends, HTTPException
from fastapi.responses import HTMLResponse


SCRYPT_MAXMEM = 128 * 1024 * 1024


def install(app_module):
    app = app_module.app
    db = app_module.database_path

    # Shared administrative authorization dependency for runtime extensions.
    if not hasattr(app_module, 'require_admin'):
        def require_admin(user=Depends(app_module.get_current_user)):
            if user.get('role') != 'admin' or user.get('account_status', 'active') != 'active':
                raise HTTPException(403, 'Acesso de administrador necessário.')
            return user
        app_module.require_admin = require_admin

    def migrate():
        with sqlite3.connect(db) as c:
            cols={r[1] for r in c.execute('PRAGMA table_info(users)').fetchall()}
            if 'must_change_password' not in cols:
                c.execute('ALTER TABLE users ADD COLUMN must_change_password INTEGER NOT NULL DEFAULT 0')
            c.commit()
    migrate()

    def hash_password(password, salt=None):
        salt=salt or secrets.token_bytes(16)
        n,r,p=32768,8,3
        digest=hashlib.scrypt(password.encode(),salt=salt,n=n,r=r,p=p,maxmem=SCRYPT_MAXMEM)
        return f'scrypt${n}${r}${p}${salt.hex()}${digest.hex()}'

    def verify_password(password, stored):
        try:
            parts=stored.split('$')
            if parts[0]=='scrypt' and len(parts)==6:
                _,n,r,p,salt_hex,digest_hex=parts
                candidate=hashlib.scrypt(password.encode(),salt=bytes.fromhex(salt_hex),n=int(n),r=int(r),p=int(p),maxmem=SCRYPT_MAXMEM)
                return secrets.compare_digest(candidate.hex(),digest_hex)
            if parts[0]=='pbkdf2_sha256' and len(parts)==4:
                _,iterations,salt_hex,digest_hex=parts
                candidate=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt_hex),int(iterations))
                return secrets.compare_digest(candidate.hex(),digest_hex)
        except (ValueError,TypeError):
            return False
        return False

    app_module.hash_password=hash_password
    app_module.verify_password=verify_password

    def user_preferences(user_id):
        with sqlite3.connect(db) as c:
            return dict(c.execute("SELECT key,value FROM user_preferences WHERE user_id=?",(user_id,)).fetchall())

    @app.get('/api/v1/profile/custom')
    def custom_profile(user=Depends(app_module.get_current_user)):
        p=user_preferences(user['id'])
        return {'id':user['id'],'username':user['username'],'role':user['role'],'display_name':p.get('display_name') or user['username'],'avatar':p.get('avatar')}

    @app.put('/api/v1/profile/custom')
    def update_custom_profile(payload:dict,user=Depends(app_module.get_current_user)):
        name=str(payload.get('display_name','')).strip()
        avatar=payload.get('avatar')
        if not name or len(name)>100: raise HTTPException(422,'Nome de exibição inválido.')
        if avatar is not None:
            if not isinstance(avatar,str) or len(avatar)>2100000 or not avatar.startswith('data:image/'):
                raise HTTPException(422,'Imagem de perfil inválida ou grande demais.')
        now=datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(db) as c:
            c.execute("INSERT INTO user_preferences(user_id,key,value,updated_at) VALUES(?,?,?,?) ON CONFLICT(user_id,key) DO UPDATE SET value=excluded.value,updated_at=excluded.updated_at",(user['id'],'display_name',name,now))
            if avatar is not None:
                c.execute("INSERT INTO user_preferences(user_id,key,value,updated_at) VALUES(?,?,?,?) ON CONFLICT(user_id,key) DO UPDATE SET value=excluded.value,updated_at=excluded.updated_at",(user['id'],'avatar',avatar,now))
            c.commit()
        return {'status':'ok','display_name':name,'avatar':avatar}

    @app.post('/api/v1/admin/users/temporary')
    def create_temporary_user(payload:dict,user=Depends(app_module.require_admin)):
        username=str(payload.get('username','')).strip()
        role=str(payload.get('role','user'))
        if not username or role not in {'user','admin'}: raise HTTPException(422,'Usuário ou função inválidos.')
        temporary=secrets.token_urlsafe(12)
        now=datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(db) as c:
            try:
                cur=c.execute('INSERT INTO users(username,password_hash,role,account_status,must_change_password,created_at) VALUES(?,?,?,?,?,?)',(username,hash_password(temporary),role,'active',1,now))
            except sqlite3.IntegrityError: raise HTTPException(409,'Nome de usuário já existe.')
            c.commit()
        return {'status':'ok','id':cur.lastrowid,'temporary_password':temporary}

    @app.get('/api/v1/status/fast')
    def fast_status(user=Depends(app_module.require_admin)):
        return app_module.api_status()

    @app.middleware('http')
    async def settings_overlay(request, call_next):
        if request.url.path=='/static/settings.html':
            static=app_module.STATIC_DIR/'settings.html'
            try:
                html=static.read_text(encoding='utf-8')
                html=html.replace("$('theme').value=p.theme||'system'","$('theme').value=p.theme||'dark'")
                html=html.replace('<option value="system">Usar configuração do sistema</option><option value="dark">Escuro</option><option value="light">Claro</option>','<option value="dark">Escuro</option><option value="oled">OLED / Preto</option><option value="dim">Escuro suave</option><option value="system">Usar configuração do sistema</option><option value="light">Claro</option>')
                langs='<option value="pt-BR">Português (Brasil)</option><option value="pt-PT">Português (Portugal)</option><option value="en">English</option><option value="es">Español</option><option value="fr">Français</option><option value="de">Deutsch</option><option value="it">Italiano</option><option value="ja">日本語</option>'
                html=html.replace('<option value="pt-BR">Português (Brasil)</option><option value="en">English</option><option value="es">Español</option>',langs,1)
                html=html.replace('<select id="server_language"><option value="pt-BR">Português (Brasil)</option><option value="en">English</option><option value="es">Español</option></select>','<select id="server_language">'+langs+'</select>')
                zones=['America/Sao_Paulo','America/New_York','America/Chicago','America/Denver','America/Los_Angeles','America/Mexico_City','America/Argentina/Buenos_Aires','America/Santiago','America/Bogota','UTC','Europe/London','Europe/Lisbon','Europe/Paris','Europe/Berlin','Europe/Madrid','Europe/Rome','Europe/Moscow','Africa/Cairo','Africa/Johannesburg','Asia/Dubai','Asia/Kolkata','Asia/Bangkok','Asia/Shanghai','Asia/Tokyo','Asia/Seoul','Australia/Sydney','Pacific/Auckland']
                opts=''.join(f'<option value="{z}">{z}</option>' for z in zones)
                html=html.replace('<input id="timezone">',f'<select id="timezone">{opts}</select>')
                html=html.replace('<option value="local">Somente local</option><option value="lan">Rede local</option>','<option value="local">Somente este computador</option><option value="lan">Rede local (LAN privada)</option>')
                account='<section id="account" class="section active"><h2>Minha conta</h2><p class="description">Perfil atualmente autenticado.</p><div class="grid"><article class="card"><h3>Perfil</h3><div class="field"><label>Usuário</label><input id="account-username" readonly></div><div class="field"><label>Função</label><input id="account-role" readonly></div></article>'
                replacement='<section id="account" class="section active"><h2>Minha conta</h2><p class="description">Todo usuário, inclusive o Administrador, pode editar o próprio nome e foto.</p><div class="grid"><article class="card"><h3>Perfil</h3><div class="field"><label>Usuário</label><input id="account-username" readonly></div><div class="field"><label>Nome de exibição</label><input id="display-name" maxlength="100"></div><div class="field"><label>Foto de perfil</label><input id="avatar-file" type="file" accept="image/png,image/jpeg,image/webp"><small class="meta">Até 1,5 MB.</small></div><div class="savebar"><button class="primary" onclick="saveProfile()">Salvar perfil</button><span id="profile-message" class="message"></span></div><input id="account-role" type="hidden"></article>'
                html=html.replace(account,replacement,1)
                html=html.replace('<input id="new-user-password" type="password" autocomplete="new-password"><small class="meta">Mínimo de 8 caracteres.</small>','<input id="new-user-password" type="text" readonly><button type="button" onclick="generateTemporaryPassword()">Gerar senha temporária</button><button type="button" onclick="copyTemporaryPassword()">Copiar</button>',1)
                html=html.replace('<div id="diagnostics-status" class="status">Carregando...</div>','<div id="diagnostics-status" class="status">Pronto para executar.</div><div class="form-actions"><button onclick="loadDiagnostics()">Executar diagnóstico</button></div>',1)
                html=html.replace("$('avatar').textContent=(u.username||'?').charAt(0).toUpperCase();","$('avatar').textContent=(u.display_name||u.username||'?').charAt(0).toUpperCase();if(u.avatar){$('avatar').style.backgroundImage=`url(${u.avatar})`;$('avatar').style.backgroundSize='cover';}")
                html=html.replace("async function init(){let r=await api('/api/auth/me');if(!r.ok)return;let u=await r.json();", "async function init(){let r=await api('/api/v1/profile/custom');if(!r.ok)return;let u=await r.json();")
                html=html.replace("async function createUser(){let username=$('new-username').value.trim(),password=$('new-user-password').value;if(!username||password.length<8){showMessage('user-message','Informe usuário e senha com pelo menos 8 caracteres.',true);return}let r=await api('/api/v1/admin/users'", "async function createUser(){let username=$('new-username').value.trim();if(!$('new-user-password').value)generateTemporaryPassword();let r=await api('/api/v1/admin/users/temporary'")
                html=html.replace("body:JSON.stringify({username,password,role:'user'})","body:JSON.stringify({username,role:'user'})")
                html=html.replace("$('new-username').value='';$('new-user-password').value='';showMessage('user-message','Usuário criado.');loadUsers()}","$('new-username').value='';$('new-user-password').value=d.temporary_password||'';navigator.clipboard.writeText($('new-user-password').value).catch(()=>{});showMessage('user-message','Usuário criado. Senha temporária copiada.');loadUsers()}")
                html=html.replace("async function resetUser(id){if(!confirm('Gerar uma senha temporária para este usuário?'))return;let r=await api(`/api/v1/admin/users/${id}/reset-password`", "async function resetUser(id){if(!confirm('Gerar uma senha temporária para este usuário?'))return;let r=await api(`/api/v1/admin/users/${id}/reset-password`")
                html=html.replace("alert(`Senha temporária: ${d.temporary_password}\\n\\nEntregue-a de forma segura ao usuário e solicite a troca no próximo acesso.`);loadUsers()}","navigator.clipboard.writeText(d.temporary_password).catch(()=>{});showMessage('user-message',`Senha temporária: ${d.temporary_password} — copiada.`);loadUsers()}")
                marker='function showSection(name)'
                helpers="""async function saveProfile(){const name=$('display-name').value.trim();if(!name){showMessage('profile-message','Informe um nome.',true);return}const file=$('avatar-file').files[0];let avatar=null;if(file){if(file.size>1572864){showMessage('profile-message','Foto acima de 1,5 MB.',true);return}avatar=await new Promise((ok,fail)=>{const fr=new FileReader();fr.onload=()=>ok(fr.result);fr.onerror=fail;fr.readAsDataURL(file)})}const r=await api('/api/v1/profile/custom',{method:'PUT',body:JSON.stringify({display_name:name,avatar})});if(!r.ok){showMessage('profile-message','Falha ao salvar perfil.',true);return}showMessage('profile-message','Perfil salvo.')}\nfunction generateTemporaryPassword(){const chars='ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%';const a=new Uint32Array(16);crypto.getRandomValues(a);$('new-user-password').value=Array.from(a,n=>chars[n%chars.length]).join('')}\nasync function copyTemporaryPassword(){if(!$('new-user-password').value)generateTemporaryPassword();await navigator.clipboard.writeText($('new-user-password').value);showMessage('user-message','Senha copiada.')}\n"""
                html=html.replace(marker,helpers+marker,1)
                html=html.replace("async function loadDiagnostics(){let r=await api('/api/v1/status');if(!r.ok)return;let d=await r.json();$('diagnostics-status').textContent=", "async function loadDiagnostics(){const box=$('diagnostics-status');box.textContent='Executando diagnóstico…';const c=new AbortController();const t=setTimeout(()=>c.abort(),8000);try{let r=await api('/api/v1/status/fast',{signal:c.signal});if(!r.ok)throw new Error('HTTP '+r.status);let d=await r.json();box.textContent=")
                html=html.replace("`Estado: ${d.status||'desconhecido'} · Banco: ${d.components?.database||'—'} · Biblioteca: ${d.components?.library||'—'} · Armazenamento: ${d.components?.storage||'—'} · FFmpeg: ${d.components?.ffmpeg||'—'}`}","`Estado: ${d.status||'desconhecido'} · Banco: ${d.components?.database||'—'} · Biblioteca: ${d.components?.library||'—'} · Armazenamento: ${d.components?.storage||'—'} · FFmpeg: ${d.components?.ffmpeg||'—'}`}catch(e){box.textContent=e.name==='AbortError'?'Diagnóstico expirou após 8 segundos. Tente novamente.':'Falha no diagnóstico: '+e.message}finally{clearTimeout(t)}}")
                return HTMLResponse(html)
            except Exception:
                pass
        return await call_next(request)
