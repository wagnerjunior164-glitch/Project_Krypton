# Publicação do ProjectKrypton — Estado Atual

Data da revisão: 2026-09-11

## Estado atual

**PUBLICADO — versão pública inicial do ProjectKrypton disponível em `main`.**

A certificação técnica do candidato público foi concluída para as Parts 01–09 e o conteúdo certificado de `public-candidate` foi publicado diretamente na branch `main` do repositório público `wagnerjunior164-glitch/Project_Krypton`.

A publicação preserva o repositório privado `wagnerjunior164-glitch/ProjectKrypton` separadamente. O repositório público mantém sua raiz Git própria e não recebeu o histórico, branches ou tags privadas.

## Publicação realizada

- Repositório público: `wagnerjunior164-glitch/Project_Krypton`.
- Branch pública publicada: `main`.
- Commit publicado: `3d8e3bd762ad2a87a63cc931f51b2fa19e33f0e4`.
- Branch de origem preservada: `public-candidate`.
- O `main` público foi atualizado para o mesmo commit certificado presente em `public-candidate`.
- O repositório privado `ProjectKrypton` não foi alterado pela publicação.

## Certificação técnica

O workflow oficial `.github/workflows/public-candidate-final-validation.yml` foi concluído com sucesso sobre o candidato público. Ele clona diretamente `wagnerjunior164-glitch/Project_Krypton`, confirma a identidade do commit, calcula hashes e executa sequencialmente as Parts 01–09 no runner Windows `PC`.

**Resultado: Parts 01–09 certificadas.**

A execução oficial termina deliberadamente na Part 09. A Part 10 permanece suspensa para reavaliação futura e não representa uma falha ou pendência da publicação atual.

Não há necessidade de repetir Parts 01–09 apenas por causa da publicação. Eventuais problemas encontrados após a disponibilização pública serão tratados como correções normais do projeto, com validações específicas quando necessário.

## Validações aprovadas anteriormente

### Preparação e segurança

- Export privado de integridade: run `34250834831`, execução #4 — 24 arquivos, SHA-256 conferido.
- FFmpeg/fallback real no runner `PC`: run `34253339675` — `VALIDACAO_FFMPEG_FALLBACK_OK`.
- Smoke integrado público: run `34255010907` — 19 testes.
- Retenção de artefatos: run `34258418198` — comportamento validado.
- Varredura independente: run `34261465639`, job `102180192398` — **SUCCESS**, 39 arquivos, `VALIDACAO_INDEPENDENTE_PUBLIC_CANDIDATE_OK`.
- Validação funcional integrada: run `34261625243`, job `102180723505` — **SUCCESS**.

### Build e execução pública

- Build/installer público: run `34262011642`, job `102188593169` — **SUCCESS**.
- E2E público real: run `34275672859`, job `102227956236` — **SUCCESS**, runner `PC`.
- Full integrado histórico: run `34276601584`, job `102236534720` — **SUCCESS** no repositório privado; permanece como evidência histórica e não substitui a certificação direta do candidato público.

## Estado das correções de segurança

As correções aplicadas durante a preparação pública fazem parte do estado publicado e certificado:

1. `POST /api/setup/diagnostics` exige administrador autenticado após `setup_completed=true`.
2. `KRYPTONPLAY_SECURE_COOKIES` permite habilitar `Secure` nos cookies sem quebrar o modo HTTP local por padrão.
3. O reset administrativo de senha recebe `new_password`, armazena somente o hash, invalida sessões anteriores e não retorna `temporary_password`.
4. `KryptonPlay/requirements.txt` está fixado em `fastapi==0.141.1`, `uvicorn[standard]==0.52.4` e `zeroconf==0.151.3`.
5. O fluxo E2E de segurança verifica diagnóstico autenticado/não autenticado, reset de senha e login com a nova senha.

Essas alterações foram incorporadas ao candidato certificado antes da publicação.

## Documentação histórica

Os documentos de lotes datados de 2026-09-08 preservam o estado e as decisões daquela fase da auditoria. Quando algum deles disser que FULL/E2E/security, dependências ou release ainda estavam pendentes, essa afirmação deve ser interpretada como **histórica**.

Em especial:

- `PUBLICATION-BATCH-SECURITY-REVIEW-2026-09-08.md` registra a segurança antes da certificação final.
- `PUBLICATION-BATCH-INTEGRATED-VALIDATION-2026-09-08.md` registra a validação funcional daquele lote.
- `PUBLICATION-BATCH-FULL-VALIDATION-2026-09-08.md` registra o FULL histórico executado no repositório privado.
- `PUBLICATION-BATCH-INDEPENDENT-SCAN-2026-09-08.md` registra a varredura independente daquele momento.
- `PUBLICATION-LOG-003.md` e `PUBLICATION-LOG-004.md` registram decisões históricas de composição da árvore.

Este arquivo é a referência consolidada para o estado atual da publicação.

## Modelo oficial de desenvolvimento privado e público

A partir da publicação inicial, o ProjectKrypton passa a operar com **dois ambientes de desenvolvimento relacionados, porém independentes**:

### 1. Repositório privado — desenvolvimento e controle

`wagnerjunior164-glitch/ProjectKrypton` é o ambiente principal de desenvolvimento e controle técnico.

É nele que devem ocorrer, preferencialmente:

- desenvolvimento de novas funcionalidades;
- refatorações e correções ainda em elaboração;
- testes exploratórios e preparação de mudanças;
- evolução da documentação interna;
- preparação de uma nova versão candidata à publicação.

O repositório privado não deve ser tratado como um espelho automático do repositório público.

### 2. Repositório público — produto oficial disponibilizado

`wagnerjunior164-glitch/Project_Krypton` é o ambiente oficial do produto publicado.

A branch `main` representa o estado público disponibilizado aos usuários. Alterações que cheguem a `main` devem estar prontas para uso público e receber a validação proporcional ao seu impacto.

O repositório público também pode receber correções urgentes diretamente quando isso for necessário para resolver um problema já disponibilizado aos usuários.

### 3. Fluxo normal de promoção

O fluxo preferencial para novas evoluções é:

`ProjectKrypton (privado)` → `validação` → `public-candidate` → `validação final necessária` → `Project_Krypton/main`

A branch `public-candidate` funciona como ponto de preparação e confirmação do conteúdo que será promovido ao ambiente público.

Não existe sincronização automática bidirecional entre os dois repositórios. Uma mudança só deve ser promovida ao público quando estiver pronta para isso.

### 4. Correções urgentes no público

Se um problema crítico exigir uma correção direta no repositório público:

1. corrigir o problema no `Project_Krypton`;
2. executar a validação proporcional ao impacto;
3. publicar a correção em `main`;
4. reproduzir a mesma correção no `ProjectKrypton` privado, mantendo os ambientes alinhados quanto à correção.

A correção pública não deve permanecer apenas no repositório público, pois isso criaria divergência técnica entre os ambientes.

### 5. Regra de validação após mudanças

A validação futura deve ser proporcional à mudança:

- mudança localizada e de baixo impacto: validação específica;
- mudança funcional relevante: testes do módulo e fluxos afetados;
- mudança que atinja diretamente escopo certificado ou componentes críticos: ampliar a validação conforme o impacto;
- não reexecutar automaticamente toda a cadeia Parts 01–09 para toda alteração, salvo quando houver justificativa técnica.

As certificações anteriores permanecem como evidência do estado certificado e não precisam ser invalidadas por mudanças que não afetem seu escopo.

### 6. Regra de independência dos ambientes

Os dois repositórios compartilham a evolução do produto, mas **não compartilham automaticamente histórico Git, branches ou alterações**.

O privado continua sendo a referência de desenvolvimento/controladoria. O público continua sendo a referência do produto efetivamente disponibilizado.

Essa separação é intencional e deve ser preservada.

## Teste operacional automatizado do atualizador

O teste do atualizador foi deliberadamente separado da certificação Parts 01–09 e não altera o workflow unificado.

O runner Windows `PC` já preserva localmente os três binários produzidos pela Part 09 em:

`C:\Users\Public\ProjectKryptonRunner\reports\public-candidate-final\<run-id>-<attempt>\part09-artifacts\`

A validação operacional reutiliza diretamente esse produto gerado pelo runner, confere os SHA-256 e instala o `KryptonPlay-Windows-Setup.exe` como versão A.

Foi criado no repositório privado o workflow:

`.github/workflows/updater-operational-validation.yml`

Ele automatiza:

1. localização da evidência Part 09 mais recente no runner;
2. conferência dos três binários e seus SHA-256;
3. validação de que a Release pública alvo é a `latest` e possui `KryptonPlay-Windows-Setup.exe` com digest SHA-256;
4. proteção contra sobrescrever uma instalação externa já existente;
5. instalação da versão A;
6. habilitação da atualização automática e confirmação de que uma versão mais nova foi detectada;
7. fechamento da versão A;
8. novo lançamento do KryptonPlay, exercitando o caminho automático do launcher;
9. espera pela execução do `KryptonPlay-Updater.exe` e pela instalação da versão B;
10. confirmação da nova versão e da notificação `update_completed`;
11. desinstalação e limpeza da instalação de teste;
12. preservação de evidência no diretório persistente do runner.

O workflow exige somente a identificação da Release B (`target_tag`). A Release pública precisa existir previamente; o workflow não cria nem altera Releases públicas automaticamente, evitando transformar o produto publicado em uma Release de teste sem decisão explícita.

Esse teste valida o **fluxo operacional real do updater**, mas não transforma o teste em requisito das Parts 01–09 nem reativa a Part 10.

### Limitação importante

A validação automatizada acima testa a atualização automática disparada pelo launcher na inicialização. O horário programado de atualização é uma capacidade distinta e pode receber uma validação temporal específica posteriormente, caso seja necessário certificar também esse comportamento.

## Pós-publicação

A partir deste ponto, o projeto entra em manutenção pública normal. Não existe um novo gate obrigatório antes de continuar o desenvolvimento.

Se surgir algum problema real após a publicação:

1. o problema será reproduzido e isolado;
2. será aplicada uma correção mínima e rastreável;
3. será executada somente a validação necessária para a alteração;
4. a correção será publicada em novo commit.

Não se deve reabrir automaticamente toda a cadeia Parts 01–09 para cada correção futura, salvo quando uma alteração modificar diretamente o escopo coberto por essas certificações e justificar nova validação completa.

## Part 10

A Part 10 continua **suspensa para reavaliação futura**. Ela não é requisito da certificação atual nem condição para a publicação realizada em `main`.

## Decisão atual

**PUBLICAÇÃO PÚBLICA: CONCLUÍDA.**

**CERTIFICAÇÃO TÉCNICA: APROVADA — PARTS 01–09.**

**REPOSITÓRIO PÚBLICO: `main` em `3d8e3bd762ad2a87a63cc931f51b2fa19e33f0e4`.**

**MODELO DE DESENVOLVIMENTO: PRIVADO COMO AMBIENTE PRINCIPAL; PÚBLICO COMO PRODUTO OFICIAL; PROMOÇÃO CONTROLADA ENTRE OS DOIS, SEM SINCRONIZAÇÃO AUTOMÁTICA.**

A partir de agora, correções e evoluções podem ser feitas normalmente nos dois ambientes, respeitando o fluxo e as regras documentados acima.
