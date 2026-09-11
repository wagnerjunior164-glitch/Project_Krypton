# Índice da documentação pública do ProjectKrypton

Data da revisão: 2026-09-11

Este índice organiza a documentação transversal do repositório público. Documentos datados da primeira auditoria permanecem preservados como histórico e não substituem `PUBLICATION-STATUS.md`.

## Referências atuais

### Estado da publicação

- `PUBLICATION-STATUS.md` — referência consolidada do estado atual da publicação, certificação Parts 01–09 e modelo privado/público.
- `DEVELOPMENT-ARCHITECTURE.md` — arquitetura conceitual de desenvolvimento, build, diagnóstico e execução modular.
- `UPDATER-OPERATIONAL-TEST.md` — estratégia e automação do teste operacional Release A → Release B.
- `POST-RELEASE-SIMPLIFICATION-PLAN.md` — plano de evolução e simplificação pós-publicação.

### Estratégia do produto

- `LICENSING-STRATEGY.md` — estratégia e decisões pendentes relacionadas a licenciamento e componentes de terceiros.
- `MONETIZATION-STRATEGY.md` — estratégia de monetização futura.

## Registros históricos da primeira publicação

Os documentos abaixo registram etapas específicas da auditoria de 2026-09-08. Eles devem ser consultados para reconstruir decisões e evidências daquele ciclo, não para determinar se o produto está atualmente bloqueado:

- `PUBLICATION-BATCH-BUILD-INSTALLER-2026-09-08.md`
- `PUBLICATION-BATCH-DEPENDENCIES-WORKFLOWS-2026-09-08.md`
- `PUBLICATION-BATCH-FULL-VALIDATION-2026-09-08.md`
- `PUBLICATION-BATCH-INDEPENDENT-SCAN-2026-09-08.md`
- `PUBLICATION-BATCH-INTEGRATED-VALIDATION-2026-09-08.md`
- `PUBLICATION-BATCH-SECURITY-REVIEW-2026-09-08.md`
- `PUBLICATION-BATCH-STATIC-2026-09-08.md`
- `PUBLICATION-BATCH-STATIC-AUDIT-2026-09-08.md`
- `PUBLICATION-LOG-003.md`
- `PUBLICATION-LOG-004.md`

## Regra de interpretação

Quando um documento histórico registrar frases como `release bloqueada`, `runner pendente`, `FULL pendente`, `E2E pendente` ou `dependências ainda não fixadas`, essas afirmações pertencem ao estado daquele momento.

Para o estado atual, sempre usar `PUBLICATION-STATUS.md` como autoridade documental.

## Separação entre documentação pública e privada

A documentação pública descreve o produto, suas regras de operação e a arquitetura em nível suficiente para entendimento e manutenção.

Detalhes internos de runner, caminhos físicos de máquinas privadas, credenciais de teste, infraestrutura administrativa e procedimentos exclusivos de controle permanecem documentados no repositório privado quando necessário.

## Regra de atualização

Toda mudança relevante no estado público deve atualizar primeiro a documentação consolidada apropriada. Registros históricos não devem ser reescritos apenas para fazer o passado parecer igual ao estado atual; quando necessário, devem receber uma indicação explícita de que são históricos.
