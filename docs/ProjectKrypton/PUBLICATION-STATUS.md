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

## Lote runtime, atualização e hardening

### `playback_ui.py`

Fonte privada e versão pública têm SHA idêntico `c55c10f4ac7df172fa26a8442062531a7961ab1d`. Conteúdo integral confirmado; sem credenciais, tokens, caminhos privados, comandos externos ou infraestrutura específica.

### `admin_features.py`

Importação integral confirmada, SHA `d1abac473336b22a2f52fa094ccc90de84608a25`. Endpoints administrativos usam `require_admin`; configurações administrativas e atualização exigem autenticação apropriada. A integração foi exercitada na execução `34259372972` no runner `PC` e terminou com **SUCCESS**.

### `update_service.py`

Auditado e importado. Usa Releases oficiais do GitHub, verifica digest `sha256:` de 64 hexadecimais e revalida o arquivo baixado. O padrão privado `wagnerjunior164-glitch/ProjectKrypton` foi sanitizado para `wagnerjunior164-glitch/Project_Krypton`; `KRYPTONPLAY_UPDATE_REPOSITORY` permanece como override controlado.

### `updater.py`

Auditado e importado. Verifica instalador/aplicativo, aguarda o processo pai, executa o instalador com opções silenciosas, remove o temporário e só relança o aplicativo após retorno zero. A validação integrada do instalador real permanece para `build/installer/full`.

### `ui_runtime.py`

A primeira cópia pública havia sido reconstruída manualmente e não correspondia ao blob privado. Isso foi corrigido nesta etapa: o arquivo público foi substituído pelo blob privado exato `7294415cb202c5b98759f6839ddb22375368ae6c` e o SHA público agora coincide exatamente.

### `update_api.py`

Verificação independente confirmou que o SHA público `1f9275148027823f29e54216132631f4d26c90be` já coincidia com o blob privado. Nenhuma alteração adicional foi necessária.

### `kryptonplay_fixes.py`

Verificação independente confirmou que o SHA público `ae9871530dad2ee8f4f464395335972fd59c99b0` já coincidia com o blob privado. Nenhuma alteração adicional foi necessária.

### `increment24_hardening.py`

O SHA público `38775df052be3f5cf9366a01a1526cbcb0e503b9` coincide com o blob privado. O componente permanece integral.

## Lote de versão, dependências e interface estática

### `version.py`

SHA público e privado: `9c33b9e54509f3676c9c334dff1a07b0f5f8dc28`. Integridade confirmada; versão centralizada permanece `0.1.0`.

### `requirements.txt`

SHA público e privado: `f79def74856f0d5bfdb78a2a0c0bfb90a3851155`. Dependências declaradas: `fastapi`, `uvicorn[standard]` e `zeroconf`. Nenhum pacote adicional foi introduzido nesta transferência.

### Interfaces HTML

A conferência por árvore Git encontrou inicialmente três divergências de blob:

- `static/player.html`: público `94b9123194499fdd534267fb73de59eb7e76ffe5` → corrigido para o privado `27d96fa6d70d488729db78e9fa021df005646f08`;
- `static/settings.html`: público `7237b30f5b798d1c5e4ea52f8e579879bbab722e` → corrigido para o privado `44a7cacf19c84d209eee666d2e50d9c9da829338`;
- `static/setup.html`: público `60b4d612b53d257ec1e61e8e4174c4532af1f7e1` → corrigido para o privado `a022f052fddd752434d6de453e01d0be4d53f6f6`.

`static/admin.html` e `static/index.html` já tinham os mesmos SHAs do privado: respectivamente `1c48ec87427b271c9b13439606b67d0e4e7d1818` e `ceb1c6c0851e1849c8fdc03d60844c756d3eb2d1`.

Após as correções, a árvore pública confirma os sete componentes estáticos/versionamento/dependências com os SHAs privados correspondentes.

## Correção de integridade — importante

A revisão deste lote também corrigiu uma inconsistência da documentação anterior: não é suficiente afirmar que um arquivo foi “importado integralmente” quando a transferência foi feita por reconstrução manual. A partir desta etapa, a integridade dos componentes copiados do privado é considerada confirmada somente quando o blob SHA público coincide com o SHA privado, salvo casos explicitamente sanitizados como `update_service.py`.

## Resultado atual

A árvore `public-candidate` está novamente consistente nos arquivos que puderam ser comparados diretamente. O commit de correção mais recente é `70b1206c66c7d2e03a391175b537c44f94cedc23`; a árvore confirma `player.html`, `settings.html`, `setup.html` e `ui_runtime.py` com os SHAs privados esperados.

A release pública final **continua bloqueada**. Ainda faltam a varredura independente de segredos/ambiente sobre a árvore candidata, revisão completa de dependências e workflows, validação funcional integrada e `build/installer/full`, seguida da conferência final de árvore e histórico.

Não remover testes temporários ou resíduos de auditoria agora. A limpeza será feita somente no encerramento da auditoria.

O runner Windows `PC` continua disponível para validações reais controladas. O caminho operacional documentado para iniciá-lo é `cd C:\actions-runner; .\run.cmd`, mantido fora da configuração pública.

## Aprovação

**Status da árvore:** BLOQUEADA PARA RELEASE PÚBLICA FINAL.

**Última etapa concluída:** correção e confirmação de integridade dos arquivos de versão, dependências e interface estática, além da confirmação independente dos blobs de runtime/update/hardening.
