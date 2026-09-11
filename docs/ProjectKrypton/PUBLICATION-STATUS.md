# Publicação do ProjectKrypton — Estado Atual

Data da revisão: 2026-09-11

## Estado atual

**Candidato público validado — fase de consolidação e preparação da publicação.**

A branch `public-candidate` continua sendo a área controlada de preparação. O repositório público utiliza uma raiz Git nova e não recebe o histórico, branches ou tags do repositório privado.

A pendência operacional registrada em 2026-09-08 foi encerrada: o workflow oficial `.github/workflows/public-candidate-final-validation.yml` foi executado e concluído com sucesso sobre o candidato público. Esse workflow é a autoridade atual para a certificação das Parts 01–09; a Part 10 permanece fora da validação oficial, conforme documentação específica.

## Validações aprovadas

### Preparação e segurança

- Export privado de integridade: run `34250834831`, execução #4 — 24 arquivos, SHA-256 conferido.
- FFmpeg/fallback real no runner `PC`: run `34253339675` — AAC `direct-play`, AC3 `transcoding`, fallback progressivo e cache reutilizado; `VALIDACAO_FFMPEG_FALLBACK_OK`.
- Smoke integrado público: run `34255010907` — 19 testes.
- Retenção de artefatos: run `34258418198` — comportamento validado.
- Varredura independente: run `34261465639`, job `102180192398` — **SUCCESS**, 39 arquivos, `VALIDACAO_INDEPENDENTE_PUBLIC_CANDIDATE_OK`.
- Validação funcional integrada: run `34261625243`, job `102180723505` — **SUCCESS**.

### Build e execução pública

- Build/installer público: run `34262011642`, job `102188593169` — **SUCCESS**, PyInstaller, updater e Inno Setup; `VALIDACAO_BUILD_INSTALLER_PUBLIC_CANDIDATE_OK`.
- E2E público real: run `34275672859`, job `102227956236` — **SUCCESS**, runner `PC`, clone limpo, FFmpeg/FFprobe, login, biblioteca, scan, status e `tests/e2e_web_test.py`; `VALIDACAO_E2E_PUBLIC_CANDIDATE_OK`.
- Full integrado histórico: run `34276601584`, job `102236534720` — **SUCCESS** no repositório privado. Esse run permanece como evidência histórica do pipeline completo e não substitui a certificação atual do candidato público.

### Certificação oficial atual

O workflow `.github/workflows/public-candidate-final-validation.yml` foi concluído com sucesso após a integração das Parts 01–09. O workflow clona diretamente `wagnerjunior164-glitch/Project_Krypton`, na ref solicitada (`public-candidate` por padrão), confirma a identidade do commit, calcula hashes e executa sequencialmente as Parts 01–09 no runner Windows `PC`.

Resultado atual: **Parts 01–09 certificadas.**

A execução oficial termina deliberadamente na Part 09. A documentação de Part 10 continua sendo de reavaliação futura e não representa uma falha ou pendência da certificação atual.

## Estado das correções de segurança

As correções aplicadas após os primeiros lotes de publicação fazem parte do estado validado atual:

1. `POST /api/setup/diagnostics` permanece disponível durante o setup inicial e, após `setup_completed=true`, exige administrador autenticado.
2. `KRYPTONPLAY_SECURE_COOKIES` permite habilitar `Secure` nos cookies sem quebrar o modo HTTP local por padrão.
3. O reset administrativo de senha recebe `new_password`, armazena somente o hash, invalida sessões anteriores e não retorna `temporary_password`.
4. `KryptonPlay/requirements.txt` está fixado em `fastapi==0.141.1`, `uvicorn[standard]==0.52.4` e `zeroconf==0.151.3`.
5. O fluxo E2E de segurança foi ampliado para verificar diagnóstico autenticado/não autenticado, reset de senha e login com a nova senha.

Essas alterações não estão mais pendentes de validação: foram incorporadas ao candidato que passou pela certificação oficial atual.

## Integridade e rastreabilidade

SHAs anteriormente confirmados na `public-candidate` permanecem registrados nos lotes históricos. O `.iss` contém `RunOnceId` após a correção do aviso do Inno Setup. O aviso operacional do PyInstaller sobre execução como administrador foi tratado como característica do ambiente do runner e não como falha mascarada de código.

A certificação atual deve ser considerada superior aos registros históricos que ainda descrevem a árvore como pendente.

## Documentação histórica

Os documentos de lotes datados de 2026-09-08 preservam o estado e as decisões daquela fase da auditoria. Quando algum deles disser que FULL/E2E/security, dependências ou release ainda estão pendentes, essa afirmação deve ser interpretada como **histórica**, não como estado atual.

Em especial:

- `PUBLICATION-BATCH-SECURITY-REVIEW-2026-09-08.md` registra a segurança antes da certificação final atual.
- `PUBLICATION-BATCH-INTEGRATED-VALIDATION-2026-09-08.md` registra a validação funcional daquele lote.
- `PUBLICATION-BATCH-FULL-VALIDATION-2026-09-08.md` registra o FULL histórico executado no repositório privado.
- `PUBLICATION-BATCH-INDEPENDENT-SCAN-2026-09-08.md` registra a varredura independente daquele momento.
- `PUBLICATION-LOG-003.md` e `PUBLICATION-LOG-004.md` são registros históricos das decisões de composição da árvore.

Este arquivo é a referência consolidada para o estado atual.

## O que ainda não está concluído

A certificação técnica Parts 01–09 está concluída. Restam atividades de **consolidação pós-certificação**, não novos gates funcionais:

1. conferir a árvore pública final, histórico Git, branches e tags;
2. confirmar que não existem dados específicos do ambiente privado introduzidos depois da última varredura;
3. alinhar os documentos históricos para que não produzam uma leitura equivocada de que a certificação ainda está bloqueada;
4. decidir e executar a limpeza dos workflows/branches temporários de auditoria, preservando antes as evidências necessárias;
5. fazer a decisão final de publicação/merge para a branch pública principal somente depois dessa conferência;
6. tratar licenciamento como decisão jurídica/documental separada, pois `LICENSING-STRATEGY.md` é uma estratégia e não uma aprovação jurídica.

## Part 10

A Part 10 continua **suspensa para reavaliação futura**. Ela não é requisito da certificação atual e não deve ser adicionada ao workflow oficial sem nova decisão documentada.

## Próxima etapa recomendada

A partir deste estado, não devemos repetir Parts 01–09. O próximo trabalho deve ser uma **conferência final de release e limpeza controlada**: revisar árvore/histórico/branches/tags, revisar a documentação de publicação, preservar as evidências da certificação e só então decidir a publicação final.

## Decisão atual

**CERTIFICAÇÃO TÉCNICA DO CANDIDATO PÚBLICO: APROVADA — PARTS 01–09.**

**RELEASE/PUBLICAÇÃO FINAL: em fase de consolidação pós-certificação; não repetir os gates já aprovados.**

A ausência de um identificador de run específico nesta página não invalida o resultado: o registro atual usa como autoridade o workflow oficial concluído. O identificador exato da execução final deve ser acrescentado quando estiver disponível no histórico de Actions, sem inventar um número.
