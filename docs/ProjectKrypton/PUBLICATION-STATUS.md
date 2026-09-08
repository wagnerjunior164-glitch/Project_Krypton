# Publicação do ProjectKrypton — Estado da Preparação

Data da revisão: 2026-09-08

## Estado

**Em preparação — BLOQUEADO para release pública final.**

A branch `public-candidate` continua sendo a área controlada de preparação. O repositório público utiliza uma raiz Git nova e não recebe o histórico, branches ou tags do repositório privado.

## Validações já aprovadas

- Export privado de integridade: run `34250834831`, execução #4 — 24 arquivos, SHA-256 conferido.
- FFmpeg/fallback real no runner `PC`: run `34253339675` — AAC `direct-play`, AC3 `transcoding`, fallback progressivo e cache reutilizado; `VALIDACAO_FFMPEG_FALLBACK_OK`.
- Smoke integrado público: run `34255010907` — 19 testes.
- Retenção de artefatos: run `34258418198` — comportamento validado e retenção condicionada aos níveis de build/installer/full.
- Varredura independente: run `34261465639`, job `102180192398` — **SUCCESS**, 39 arquivos, `VALIDACAO_INDEPENDENTE_PUBLIC_CANDIDATE_OK`.
- Validação funcional integrada: run `34261625243`, job `102180723505` — **SUCCESS**, 4 testes e smoke integrado.
- Build/installer público: run `34262011642`, job `102188593169` — **SUCCESS**, PyInstaller, updater e Inno Setup; `VALIDACAO_BUILD_INSTALLER_PUBLIC_CANDIDATE_OK`.
- E2E público real: run `34275672859`, job `102227956236` — **SUCCESS**, runner `PC`, clone limpo, FFmpeg/FFprobe, login, biblioteca, scan, status e `tests/e2e_web_test.py`; `VALIDACAO_E2E_PUBLIC_CANDIDATE_OK`.
- Full integrado: run `34276601584`, job `102236534720` — **SUCCESS**, mas executado no repositório privado, na branch temporária `tmp-final-full-validation-2026-09-08`. Portanto não é prova de FULL diretamente sobre `public-candidate`.

## Correções finais aplicadas após essas validações

A revisão de segurança posterior endureceu a árvore pública:

1. `POST /api/setup/diagnostics` continua utilizável durante setup inicial, mas após `setup_completed=true` exige administrador autenticado.
2. Foi adicionado `KRYPTONPLAY_SECURE_COOKIES`; quando habilitado, o middleware adiciona `Secure` aos cookies.
3. O reset administrativo de senha passou a receber `new_password`, armazenar somente o hash, invalidar sessões anteriores e não retornar `temporary_password`.
4. `requirements.txt` foi fixado em:
   - `fastapi==0.141.1`
   - `uvicorn[standard]==0.52.4`
   - `zeroconf==0.151.3`
5. O E2E temporário foi ampliado para testar explicitamente diagnóstico não autenticado, diagnóstico autenticado, reset de senha e login com a nova senha.

Essas alterações estão documentadas em `docs/ProjectKrypton/PUBLICATION-BATCH-SECURITY-REVIEW-2026-09-08.md` e aguardam validação real no runner antes de serem consideradas encerradas.

## Integridade atual da árvore

SHAs relevantes confirmados na `public-candidate`:

- `increment24_hardening.py`: `19027f81d9c8558c76c2ffb3fe949484fa0187dd`;
- `requirements.txt`: `066763becc2f5474d0021ccf1625d628553ba5c2`;
- `installer/KryptonPlay-Windows.iss`: `bbf7e26cf3aceee3d6515082edb9d88c8d4dbda2`;
- `KryptonPlay.spec`: `2cdbb4f4ccaca5ee88cad8d87735d3fe91687bd4`;
- `KryptonPlay-Updater.spec`: `a0e7b00b6a75959df8ddf75f31c7b7556fd56a09`;
- `updater.py`: `15cc16f492edb1e8819160b5183cd8e6643b3da5`;
- `tests/e2e_web_test.py`: `23acfbf6158532d6e82ab0027c71d9cea9847796`;
- `tests/run_e2e_server.py`: `4fd842404c5026c1fe88fec4e05533c11b136ac4`.

O `.iss` inclui `RunOnceId` após a correção do aviso do Inno Setup. O aviso operacional do PyInstaller sobre execução como administrador foi registrado como característica do ambiente do runner e não mascarado por alteração de código.

## Histórico e branches

`public-candidate` está 100 commits à frente de `main` e 0 atrás. A árvore pública permanece separada do histórico privado.

Branches temporárias de auditoria e workflows temporários **não devem ser removidos ainda**. A limpeza ocorrerá somente depois da validação final e da conferência de histórico, árvore, branches e tags.

## Validação pendente por indisponibilidade de escopo do runner

Após as últimas alterações, foram disparados:

- run `34284493321` — Temporary public-candidate E2E;
- run `34284493313` — Temporary public-candidate Full Validation.

Ambos estão aguardando um runner elegível no escopo do repositório público. O workflow usa `[self-hosted, windows, x64]`. O runner `PC` executa normalmente no repositório privado, mas precisa estar disponível também para `Project_Krypton` para que esses jobs sejam atribuídos.

Esta pendência é operacional; não deve ser tratada como aprovação de validação.

## Trabalho que pode ser concluído sem o runner

A auditoria estática e documental pode continuar: revisão final de árvore, referências ao ambiente privado, SHAs, workflows, documentação, histórico, branches e tags. Nenhuma dessas atividades substitui o FULL/E2E final diretamente sobre `public-candidate`.

## Critérios obrigatórios para release

1. Runner `PC` elegível para `Project_Krypton`.
2. FULL diretamente sobre `public-candidate` com sucesso.
3. E2E/security diretamente sobre `public-candidate` com sucesso.
4. Nova varredura independente após todas as alterações finais.
5. Conferência final da árvore, histórico, branches e tags.
6. Confirmação final de ausência de dados específicos do ambiente privado.
7. Atualização final desta documentação com os resultados reais.
8. Somente depois: remoção dos workflows/branches temporários de auditoria e decisão sobre merge/release para `main`.

## Estado de aprovação

**RELEASE PÚBLICA FINAL: BLOQUEADA.**

Nenhuma alteração nesta documentação deve ser interpretada como aprovação do FULL final. O próximo ponto crítico é executar as validações diretamente sobre a árvore pública depois que o runner `PC` estiver elegível no repositório `Project_Krypton`.

Procedimento operacional local do runner Windows `PC`: `cd C:\actions-runner; .\run.cmd`. Esse detalhe não pertence à configuração pública.
