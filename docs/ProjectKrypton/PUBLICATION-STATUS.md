# Publicação do ProjectKrypton — Estado da Preparação

## Estado

**Em preparação — não é uma release pública final.**

A branch `public-candidate` continua sendo a área controlada de preparação. O repositório público utiliza uma raiz Git nova e não recebe o histórico, branches ou tags do repositório privado.

## Lotes já auditados/importados

Foram auditados/importados: documentação pública; `diagnostics.py`; `scanner.py`; configuração pública; `launcher.py`; `playback_info.py`; `mdns_service.py`; `audio_fallback.py`; `playback_pipeline.py`; `app.py`; `playback_ui.py`; `admin_features.py`; `update_service.py`; `updater.py`; `ui_runtime.py`; `update_api.py`; `kryptonplay_fixes.py`; `increment24_hardening.py`; `version.py`; `requirements.txt`; e as cinco interfaces HTML estáticas.

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
- `static/setup.html`: `a022f052fddd752434d6de453e01d0be4d53f6f6`.

## Varredura independente de publicação

Foi criado um workflow temporário no repositório privado para clonar a branch pública em ambiente limpo no runner `PC` e examinar todos os arquivos fora de `.git`.

A primeira execução funcional, `34261206634`, chegou ao clone da árvore e encontrou somente referências ambientais em documentação histórica: um caminho de mídia específico e a identificação do repositório privado. Não foram encontrados tokens, chaves privadas, credenciais funcionais ou arquivos de segredo.

As referências ambientais desnecessárias foram removidas da documentação pública. O relatório completo está em `docs/ProjectKrypton/PUBLICATION-BATCH-INDEPENDENT-SCAN-2026-09-08.md`.

A execução final do mesmo gate ainda precisa concluir após a sanitização. Até esse registro ser confirmado pelo runner com `VALIDACAO_INDEPENDENTE_PUBLIC_CANDIDATE_OK`, a varredura permanece pendente.

## Pontos de segurança ainda em revisão

A auditoria funcional anterior identificou pontos que continuam sujeitos à decisão de arquitetura antes da release: proteção/sanitização de `/api/setup/diagnostics`, tratamento deliberado de cookie de sessão HTTP local e fluxo de senha temporária/reset administrativo. Esses pontos não foram mascarados como resolvidos pela varredura de publicação.

## Próximas etapas obrigatórias

1. confirmar a execução final da varredura independente no runner `PC`;
2. revisar completamente dependências e workflows/permissões, mantendo PRs não confiáveis fora de runners privados;
3. executar validação funcional integrada;
4. executar `build`, `installer` e `full`, incluindo integração real do instalador/updater;
5. realizar conferência final da árvore, histórico, branches e tags públicos;
6. somente então aprovar a release/merge para `main`.

Não remover testes, workflows ou branches temporários de auditoria agora. A limpeza será feita somente no encerramento da auditoria.

O procedimento operacional local documentado para iniciar o runner Windows `PC` é `cd C:\actions-runner; .\run.cmd`. Esse detalhe permanece fora da configuração pública.

## Aprovação

**Status da árvore:** BLOQUEADA PARA RELEASE PÚBLICA FINAL.

**Última etapa registrada:** varredura independente executada em clone limpo, identificação e remoção de referências ambientais desnecessárias da documentação pública; confirmação final do gate ainda pendente.
