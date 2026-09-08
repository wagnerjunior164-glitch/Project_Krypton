# Publicação do ProjectKrypton — Estado da Preparação

## Estado

**Em preparação — não é uma release pública final.**

A branch `public-candidate` continua sendo a área controlada de preparação. O repositório público utiliza uma raiz Git nova e não recebe o histórico, branches ou tags do repositório privado `ProjectKrypton`.

## Fundamento da auditoria

A execução privada `34250834831` foi usada como fonte de integridade para o lote KryptonPlay. O runner Windows `PC` exportou 24 arquivos e produziu hashes SHA-256 para permitir importação controlada, em vez de copiar cegamente a árvore privada.

O caminho privado `D:\\Midia` foi bloqueado para publicação e o `config.json` público usa `media`.

## Lotes já auditados/importados

### Fundação e documentação

Foram preparados e sanitizados os documentos públicos básicos:

- `README.md`;
- `KryptonPlay/README.md`;
- `MediaStation/README.md`;
- `MemoryProject/README.md`;
- `KryptonOS Router/README.md`.

### Componentes de baixo risco

- `KryptonPlay/diagnostics.py`;
- `KryptonPlay/scanner.py`;
- `KryptonPlay/tests/test_diagnostics.py`;
- `KryptonPlay/tests/test_scanner_library.py`;
- `KryptonPlay/config/README.md`;
- `KryptonPlay/config/config.json`.

### Núcleo de execução e descoberta

- `KryptonPlay/launcher.py`;
- `KryptonPlay/playback_info.py`;
- `KryptonPlay/mdns_service.py`.

Os componentes auditados não apresentaram credenciais, tokens, IP doméstico fixo ou caminhos domésticos indevidos. O hostname local usado pelo projeto é `kryptonplay.local`.

### Reprodução e FFmpeg

- `KryptonPlay/audio_fallback.py` — blob público `b2ed6fa841c2df9d2c12544a6cdb640300c293a0`;
- `KryptonPlay/playback_pipeline.py` — blob público `d1b35a4b732f5126290ab2e40699dc35605b045a`.

A auditoria confirmou uso de FFmpeg/FFprobe por argumentos estruturados, `-nostdin`, timeouts, limpeza de processos e ausência de credenciais ou infraestrutura privada.

Uma cópia truncada anterior de `audio_fallback.py` foi removida no commit `985b7291ce5b322ffc5f9015ca771f62fdcbcb2f`. A versão atual é uma importação integral da fonte privada auditada.

## Validação funcional real de FFmpeg

A execução `34253339675`, no runner Windows `PC`, fez checkout explícito da árvore pública candidata e testou realmente H.264 + AAC e H.264 + AC3.

Resultados:

- `FFMPEG_FALLBACK_SMOKE_OK`;
- AAC: `direct-play`;
- AC3: `transcoding`, razão `audio_codec_incompatible`;
- fallback progressivo executado;
- cache `.m4a` criado e reutilizado como `cache_hit`;
- `VALIDACAO_FFMPEG_FALLBACK_OK`.

A validação foi aprovada. As duas falhas intermediárias foram exclusivamente ajustes do workflow temporário (política do PowerShell e saída de diagnóstico), não falhas do código KryptonPlay.

## Validação funcional de `app.py`

A execução `34255010907` validou `app.py` contra a branch pública `public-candidate` no runner Windows `PC`.

O smoke test iniciou `uvicorn app:app` e exercitou health, setup, usuários, login, Bearer token, sessão, settings, libraries, status, scan e logout. O resultado registrado foi `19 passed`, com `KryptonPlay unit/functional tests — PASS`, `KryptonPlay Web E2E — PASS` e `Resultado: CONCLUIDO`.

A limitação de armazenamento de Artifacts ocorreu depois da execução dos testes e não invalida a validação funcional.

## Correção da retenção de Artifacts da CI

### Problema identificado

O job `Enforce KryptonPlay artifact retention` era uma rotina de housekeeping. Ele tentava listar e apagar artefatos `KryptonPlay-Windows`, mantendo somente os dois mais recentes depois de atingir cinco artefatos.

Em execuções `functional`, entretanto, os entregáveis Windows não são produzidos. Mesmo assim, o job de retenção era iniciado e podia aparecer como falha de infraestrutura antes de executar qualquer step. Isso fazia uma execução funcional válida parecer globalmente problemática, apesar de `Unified validation` estar verde.

### Correção aplicada

O workflow privado `.github/workflows/projectkrypton-validation.yml` foi alterado no commit:

`dcc61c0dc715a84132c891d5a4d7aad4a57dee82`

O job de retenção passou a executar somente quando o nível de validação é um dos que podem produzir `KryptonPlay-Windows`:

- `build`;
- `installer`;
- `full`.

Execuções `quick` e `functional` não iniciam mais esse job.

A rotina de retenção continua protegida contra falhas de API e exclusão individual: problemas de housekeeping não devem invalidar os testes funcionais.

## Confirmação da correção

O push do commit de correção gerou a execução:

`34258418198` — `ProjectKrypton Unified Validation`, run #156.

Resultado final:

| Job/etapa | Resultado |
|---|---|
| `Unified validation` | **SUCCESS** |
| Checkout | SUCCESS |
| Validate runner | SUCCESS |
| Prepare functional E2E environment | SUCCESS |
| Run unified validation | **SUCCESS** |
| Publish validation summary | SUCCESS |
| Upload validation report | SUCCESS |
| Upload Windows deliverables | SKIPPED — correto para `functional` |
| Report artifact quota limitation | SUCCESS |
| `Enforce KryptonPlay artifact retention` | **SKIPPED — comportamento esperado** |

O job de retenção não possui steps executados porque foi corretamente impedido pela condição do job. Portanto, o erro anterior de infraestrutura deixou de ocorrer nessa execução.

A execução não retornou artefatos disponíveis pela API, apesar de o step de upload do relatório ter terminado com sucesso. Isso é tratado como uma limitação de armazenamento/disponibilidade de Artifacts e não como falha da validação funcional.

## Auditoria de `admin_features.py`

A fonte privada de `KryptonPlay/admin_features.py` foi recuperada e analisada antes da importação pública.

Pontos verificados:

- não foram identificadas credenciais, tokens, IPs domésticos ou caminhos privados no conteúdo auditado;
- endpoints administrativos usam `require_admin`;
- configurações de atualização, notificações, fuso horário, relógio e reinício estão protegidas por autenticação apropriada;
- a lógica de `must_change_password` está relacionada ao fluxo de alteração obrigatória de senha e será validada em conjunto com `increment24_hardening.py` e `kryptonplay_fixes.py` antes da publicação;
- atualização instalável depende do executável separado `KryptonPlay-Updater.exe` e da instalação congelada, devendo ser validada junto com os componentes de atualização.

**Importação pública de `admin_features.py`: pendente de validação de acoplamento e teste funcional.** Nenhum código foi reconstruído ou inventado.

## Próximos componentes sob revisão

Permanecem sob auditoria/importação controlada:

- `KryptonPlay/playback_ui.py`;
- `KryptonPlay/admin_features.py`;
- `KryptonPlay/ui_runtime.py`;
- `KryptonPlay/update_api.py`;
- `KryptonPlay/update_service.py`;
- `KryptonPlay/updater.py`;
- `KryptonPlay/kryptonplay_fixes.py`;
- `KryptonPlay/increment24_hardening.py`;
- `KryptonPlay/version.py`;
- `KryptonPlay/requirements.txt`;
- `KryptonPlay/static/admin.html`;
- `KryptonPlay/static/index.html`;
- `KryptonPlay/static/player.html`;
- `KryptonPlay/static/settings.html`;
- `KryptonPlay/static/setup.html`.

Antes da conclusão de `playback_ui.py`, a cópia pública deve ser comparada novamente com a fonte privada para garantir importação integral e eliminar qualquer risco de reconstrução/truncamento.

## Bloqueios ainda existentes

A release pública final continua bloqueada até:

- concluir a auditoria arquivo por arquivo;
- resolver qualquer diferença entre documentação e implementação, incluindo a referência documentada a scrypt versus o uso efetivo de PBKDF2-SHA256 com 200.000 iterações;
- revisar autenticação, administração e atualização;
- revisar dependências e reprodutibilidade;
- revisar permissões e segurança dos workflows;
- executar varredura independente de segredos e informações de ambiente;
- concluir validação funcional integrada;
- executar build/installer final;
- conferir a árvore pública final e o histórico Git antes da primeira release.

## Regras permanentes da publicação

- Não publicar histórico, branches ou tags privados.
- Não publicar credenciais, tokens, cookies, chaves ou valores secretos.
- Valores de teste devem ser efêmeros ou claramente não reutilizáveis.
- Workflows de Pull Request não devem executar código não confiável em runners privados.
- O runner Windows `PC` pode ser usado para validações reais controladas.
- O runner é iniciado pelo caminho documentado `cd C:\actions-runner; .\run.cmd`; esse detalhe permanece fora da configuração pública do workflow.
- Testes temporários e seus resíduos de auditoria permanecem até o encerramento da auditoria; a limpeza final será feita somente ao término.

## Aprovação

**Status da árvore:** BLOQUEADA PARA RELEASE PÚBLICA FINAL.

**Última validação documentada:** `34258418198` — validação funcional aprovada e retenção de Artifacts corretamente ignorada para o nível `functional`.
