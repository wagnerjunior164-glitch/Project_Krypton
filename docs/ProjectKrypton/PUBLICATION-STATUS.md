# Publicação do ProjectKrypton — Estado da Preparação

## Estado

**Em preparação — não é uma release pública final.**

A branch `public-candidate` continua sendo a área controlada de preparação. O repositório público utiliza uma raiz Git nova e não recebe o histórico, branches ou tags do repositório privado `ProjectKrypton`.

## Lotes já auditados/importados

### Fundação e componentes anteriores

Foram auditados/importados: documentação pública; `diagnostics.py`; `scanner.py`; testes de diagnostics/scanner; configuração pública; `launcher.py`; `playback_info.py`; `mdns_service.py`; `audio_fallback.py`; `playback_pipeline.py`; `app.py`; `playback_ui.py`; `admin_features.py`; `update_service.py`; `updater.py`.

O export privado de integridade `34250834831` confirmou 24 arquivos. O caminho privado `D:\Midia` foi bloqueado para publicação e o `config.json` público usa `media`.

### Reprodução e FFmpeg

`audio_fallback.py` e `playback_pipeline.py` foram importados integralmente. A validação real no runner Windows `PC`, run `34253339675`, confirmou AAC como `direct-play`, AC3 como `transcoding`, fallback progressivo e cache reutilizado, com `VALIDACAO_FFMPEG_FALLBACK_OK`.

### Aplicação

A validação `34255010907` executou `uvicorn app:app` e exercitou health, setup, usuários, login, Bearer token, sessão, settings, libraries, status, scan e logout: `19 passed`.

### CI / Artifacts

O job de retenção foi condicionado aos níveis `build`, `installer` e `full`. A execução funcional `34258418198` confirmou `Unified validation: SUCCESS` e `Enforce KryptonPlay artifact retention: SKIPPED`, eliminando o falso bloqueio de housekeeping em `functional`.

## Lote atual — runtime, atualização e hardening

### `playback_ui.py`

Fonte privada e versão pública têm SHA idêntico `c55c10f4ac7df172fa26a8442062531a7961ab1d`. Conteúdo integral confirmado; sem credenciais, tokens, caminhos privados, comandos externos ou infraestrutura específica.

### `admin_features.py`

Importação integral confirmada, SHA público `d1abac473336b22a2f52fa094ccc90de84608a25`. Endpoints administrativos usam `require_admin`; configurações administrativas e atualização exigem autenticação apropriada. A integração foi exercitada na execução `34259372972` no runner `PC` e terminou com **SUCCESS**.

### `update_service.py`

Auditado e importado. Usa Releases oficiais do GitHub, verifica digest `sha256:` de 64 hexadecimais e revalida o arquivo baixado. O padrão privado `wagnerjunior164-glitch/ProjectKrypton` foi sanitizado para `wagnerjunior164-glitch/Project_Krypton`; `KRYPTONPLAY_UPDATE_REPOSITORY` permanece como override controlado.

### `updater.py`

Auditado e importado. Verifica instalador/aplicativo, aguarda o processo pai, executa o instalador com opções silenciosas, remove o temporário e só relança o aplicativo após retorno zero. A validação integrada do instalador real permanece para `build/installer/full`.

### `ui_runtime.py`

Fonte privada auditada e importada integralmente para `public-candidate` no commit `47f03a9b27f46313e262b7d0539c36c55b880922`. Implementa status de segurança da conta, bloqueio de APIs para senha temporária, reinício administrativo apenas em instalação congelada e overlays de UI. Não foram identificadas credenciais ou caminhos domésticos fixos.

### `update_api.py`

Fonte privada auditada e importada integralmente no commit `ca59a1cdde33054a9f5a97bc3eb47d782967df12`. O endpoint de aplicação exige usuário autenticado, usa o serviço de atualização e inicia o `KryptonPlay-Updater.exe` somente quando os componentes instalados necessários existem.

### `kryptonplay_fixes.py`

Fonte privada auditada e importada integralmente no commit `b69f8431f4cea043d65ac441ee53c481f38b4d52`. O módulo cria/migra `must_change_password`, fornece hashing scrypt para novas senhas, mantém verificação de PBKDF2 legado, protege operações administrativas e implementa as extensões de perfil/status/UI.

### `increment24_hardening.py`

Fonte privada auditada e importada integralmente no commit `39c8af2fd276d7cc8fb4afbd89cd0ec02d1a2bb8`. Enforce a troca obrigatória de senha temporária na fronteira HTTP, preservando os endpoints necessários para concluir a troca e atualizando o estado após sucesso.

## Resultado do lote

Os quatro componentes foram auditados e colocados na árvore pública candidata sem publicar credenciais, tokens, cookies, IPs domésticos ou caminhos privados identificados. A integração é referenciada pelo `app.py`, que instala `update_api`, `kryptonplay_fixes`, `increment24_hardening`, `admin_features` e `ui_runtime`.

A execução `34259372972` terminou com **SUCCESS** no runner Windows `PC`; o job de retenção permaneceu **SKIPPED** para `functional`. Isso valida o acoplamento básico do lote na suíte existente, mas não substitui a validação integrada final.

## Próximos componentes sob revisão

- `KryptonPlay/version.py`;
- `KryptonPlay/requirements.txt`;
- `KryptonPlay/static/admin.html`;
- `KryptonPlay/static/index.html`;
- `KryptonPlay/static/player.html`;
- `KryptonPlay/static/settings.html`;
- `KryptonPlay/static/setup.html`.

Depois desses arquivos: varredura independente de segredos/ambiente, revisão de dependências e workflows, validação funcional integrada e, por último, `build/installer/full` e conferência final da árvore/histórico antes da primeira release.

## Bloqueios permanentes da release

A release pública final continua bloqueada até concluir toda a auditoria, resolver diferenças documentação/implementação, revisar autenticação/administração/atualização, dependências e workflows, executar varredura independente, concluir validação integrada, gerar build/installer final e conferir a árvore pública e o histórico Git.

Não remover testes temporários ou resíduos de auditoria agora. A limpeza será feita somente no encerramento da auditoria.

O runner Windows `PC` continua disponível para validações reais controladas. O caminho operacional documentado para iniciá-lo é `cd C:\actions-runner; .\run.cmd`, mantido fora da configuração pública.

## Aprovação

**Status da árvore:** BLOQUEADA PARA RELEASE PÚBLICA FINAL.

**Última validação documentada:** `34259372972` — lote runtime/atualização/hardening integrado com sucesso no runner `PC`.