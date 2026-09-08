# Publicação do ProjectKrypton — Estado da Preparação

## Estado

**Em preparação — não é uma release pública final.**

A branch `public-candidate` continua sendo a área controlada de preparação. O repositório público utiliza uma raiz Git nova e não recebe o histórico, branches ou tags do repositório privado.

## Lotes já auditados/importados

Foram auditados/importados: documentação pública; `diagnostics.py`; `scanner.py`; configuração pública; `launcher.py`; `playback_info.py`; `mdns_service.py`; `audio_fallback.py`; `playback_pipeline.py`; `app.py`; `playback_ui.py`; `admin_features.py`; `update_service.py`; `updater.py`; `ui_runtime.py`; `update_api.py`; `kryptonplay_fixes.py`; `increment24_hardening.py`; `version.py`; `requirements.txt`; as cinco interfaces HTML estáticas; especificações PyInstaller; especificação Inno Setup; e os dois harnesses E2E do KryptonPlay.

O export privado de integridade `34250834831` confirmou 24 arquivos. O caminho de mídia específico do ambiente privado não é publicado; o `config.json` público usa `media`.

### Reprodução e FFmpeg

A validação real no runner Windows `PC`, run `34253339675`, confirmou AAC como `direct-play`, AC3 como `transcoding`, fallback progressivo e cache reutilizado, com `VALIDACAO_FFMPEG_FALLBACK_OK`.

### Aplicação

A validação `34255010907` executou `uvicorn app:app` e exercitou health, setup, usuários, login, Bearer token, sessão, settings, libraries, status, scan e logout: `19 passed`.

### CI / Artifacts

A execução funcional `34258418198` confirmou `Unified validation: SUCCESS` e o job de retenção condicionado aos níveis de build não interferiu na validação funcional.

## Integridade dos componentes

Quando um componente é transferido integralmente do privado, a aprovação de integridade exige coincidência de blob SHA. Essa regra foi aplicada às fontes comparadas diretamente. Exceção explícita: `update_service.py`, que foi sanitizado para usar por padrão o repositório público `wagnerjunior164-glitch/Project_Krypton`, preservando `KRYPTONPLAY_UPDATE_REPOSITORY` como override.

SHAs confirmados relevantes:

- `ui_runtime.py`: `7294415cb202c5b98759f6839ddb22375368ae6c`;
- `update_api.py`: `1f9275148027823f29e54216132631f4d26c90be`;
- `kryptonplay_fixes.py`: `ae9871530dad2ee8f4f464395335972fd59c99b0`;
- `increment24_hardening.py`: `38775df052be3f5cf9366a01a1526cbcb0e503b9`;
- `version.py`: `9c33b9e54509f3676c9c334dff1a07b0f5f8dc28`;
- `requirements.txt`: `f79def74856f0d5bfdb78a2a0c0bfb90a3851155`;
- `static/admin.html`: `1c48ec87427b271c9b13439606b67d0e4e7d1818`;
- `static/index.html`: `ceb1c6c0851e1849c8fdc03d60844c756d3eb2d1`;
- `static/player.html`: `27d96fa6d70d488729db78e9fa021df005646f08`;
- `static/settings.html`: `44a7cacf19c84d209eee666d2e50d9c9da829338`;
- `static/setup.html`: `a022f052fddd752434d6de453e01d0be4d53f6f6`;
- `KryptonPlay.spec`: `2cdbb4f4ccaca5ee88cad8d87735d3fe91687bd4`;
- `KryptonPlay-Updater.spec`: `a0e7b00b6a75959df8ddf75f31c7b7556fd56a09`;
- `installer/KryptonPlay-Windows.iss`: `904aeaaae52bcd235d4b080d2f0a10b68f2bdb80`;
- `tests/e2e_web_test.py`: `23acfbf6158532d6e82ab0027c71d9cea9847796`;
- `tests/run_e2e_server.py`: `4fd842404c5026c1fe88fec4e05533c11b136ac4`.

## Varredura independente de publicação — APROVADA

A execução final `34261465639`, job `102180192398`, examinou `39` arquivos em clone limpo da branch pública e concluiu com **SUCCESS**, registrando `VALIDACAO_INDEPENDENTE_PUBLIC_CANDIDATE_OK`. Nenhum marcador proibido de segredo, credencial, caminho privado ou IPv4 LAN fixo foi encontrado.

O relatório completo está em `docs/ProjectKrypton/PUBLICATION-BATCH-INDEPENDENT-SCAN-2026-09-08.md`.

## Validação funcional integrada — APROVADA

A execução `34261625243`, job `102180723505`, clonou novamente `public-candidate` no runner `PC`, instalou o manifesto de dependências, compilou o código e executou os testes existentes: **4 passed**.

O smoke integrado iniciou `uvicorn app:app`, validou setup/diagnóstico, criação inicial de administrador, login, Bearer token, settings, libraries e logout, registrando `INTEGRATED_APP_SMOKE_OK` e `VALIDACAO_INTEGRADA_PUBLIC_CANDIDATE_OK`.

O manifesto continua sem versões fixadas. A execução confirmou compatibilidade do estado atual com Python `3.12.10`; nenhuma versão foi alterada arbitrariamente.

## Dependências e workflows — REVISÃO CONCLUÍDA

`requirements.txt` contém apenas `fastapi`, `uvicorn[standard]` e `zeroconf`. A instalação e execução foram confirmadas no runner. A ausência de versões fixadas permanece como pendência de reprodutibilidade para a decisão final antes da release.

A árvore `public-candidate` não contém workflows GitHub Actions públicos. Portanto, no estado atual, nenhum PR público executa código não confiável no runner self-hosted privado `PC`. Os workflows temporários de auditoria ficaram exclusivamente no repositório privado.

O relatório completo está em `docs/ProjectKrypton/PUBLICATION-BATCH-DEPENDENCIES-WORKFLOWS-2026-09-08.md`.

## Build/installer — FONTES PREPARADAS; GATE PENDENTE

A árvore agora contém os specs de PyInstaller, o `.iss` do instalador e os harnesses E2E necessários para o pipeline Windows.

O workflow temporário no repositório privado para executar build + installer no `PC` foi iniciado como run `34262011642`, job `102182033615`. No momento deste registro o job está **QUEUED**, portanto ainda não há aprovação de build/installer.

O relatório está em `docs/ProjectKrypton/PUBLICATION-BATCH-BUILD-INSTALLER-2026-09-08.md`.

## Pontos de segurança ainda em revisão

A auditoria funcional anterior identificou pontos que continuam sujeitos à decisão de arquitetura antes da release: proteção/sanitização de `/api/setup/diagnostics`, tratamento deliberado de cookie de sessão HTTP local e fluxo de senha temporária/reset administrativo. Esses pontos não foram mascarados como resolvidos pela varredura de publicação ou pelo smoke integrado.

## Próximas etapas obrigatórias

1. aguardar/concluir `build` e `installer` no runner `PC`;
2. decidir e documentar o conjunto final de versões das dependências;
3. executar `full`, incluindo E2E real e integração final do updater;
4. realizar conferência final da árvore, histórico, branches e tags públicos;
5. somente então aprovar a release/merge para `main`.

Não remover testes, workflows ou branches temporários de auditoria agora. A limpeza será feita somente no encerramento da auditoria.

O procedimento operacional local documentado para iniciar o runner Windows `PC` é `cd C:\actions-runner; .\run.cmd`. Esse detalhe permanece fora da configuração pública.

## Aprovação

**Status da árvore:** BLOQUEADA PARA RELEASE PÚBLICA FINAL.

**Última etapa concluída:** varredura independente, validação funcional integrada e revisão de dependências/workflows aprovadas/concluídas; build/installer aguardando runner e `full`/auditoria final ainda pendentes.
