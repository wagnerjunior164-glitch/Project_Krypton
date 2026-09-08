# Lote de publicação — revisão de segurança

Data: 2026-09-08

## Escopo

Revisão direcionada dos pontos de segurança já identificados durante a auditoria de publicação da branch `public-candidate`, sem declarar como resolvido aquilo que não foi alterado e revalidado.

## Resultado

A revisão foi **concluída com pendências explícitas**. A árvore permanece bloqueada para release pública final.

### 1. Diagnóstico de configuração

O endpoint `POST /api/setup/diagnostics` é usado durante a configuração inicial e, no estado atual, pode receber caminhos fornecidos pelo cliente e retornar existência, tipo e permissões, além de informações sobre diretório de dados e disponibilidade de `ffmpeg`/`ffprobe`.

Durante a configuração inicial, essa capacidade precisa permanecer utilizável antes da existência de uma conta autenticada. Depois que a configuração é concluída, entretanto, a mesma superfície não deve permanecer aberta para exposição LAN/pública sem uma barreira administrativa ou equivalente.

**Decisão para release:** pendência obrigatória. Restringir o diagnóstico após a configuração inicial ao administrador autenticado, ou substituir o endpoint por uma interface autenticada equivalente, e então repetir smoke/E2E e varredura independente.

### 2. Cookie de sessão

O login cria uma sessão persistida no banco e emite o cookie `kryptonplay_session` com `HttpOnly` e `SameSite=Lax`, mas `secure=False`.

Isso é coerente com o cenário HTTP local atualmente validado no runner `PC`. Não deve ser alterado cegamente para `Secure`, porque isso poderia impedir o funcionamento do modo HTTP local. Para qualquer exposição por HTTPS/LAN, a política de transporte precisa ser explícita e o cookie deve ser protegido de acordo com o transporte efetivamente usado.

**Decisão para release:** pendência arquitetural. Documentar o modo de transporte suportado e, se houver suporte oficial a HTTPS, tornar a política de `Secure` dependente de uma configuração de transporte seguro ou equivalente. Revalidar login/logout após a decisão.

### 3. Reset administrativo de senha

`POST /api/v1/admin/users/{user_id}/reset-password` exige administrador autenticado, gera senha aleatória, invalida as sessões do usuário e retorna a senha temporária na resposta.

O mecanismo não contém uma credencial fixa e foi preservado como fluxo funcional. O risco está no canal de entrega: qualquer cliente capaz de observar a resposta do administrador poderia obter a senha temporária.

**Decisão para release:** pendência de modelo de segurança. Se o fluxo permanecer, documentar que a resposta só deve ser consumida por uma interface administrativa autenticada e entregue por transporte seguro; preferencialmente considerar um fluxo de redefinição que não revele uma senha reutilizável na resposta HTTP.

## O que já foi validado

- Varredura independente da árvore pública: run `34261465639`, job `102180192398`, **SUCCESS**.
- Validação funcional integrada diretamente sobre `public-candidate`: run `34261625243`, job `102180723505`, **SUCCESS**, 4 testes.
- E2E real diretamente sobre `public-candidate`: run `34275672859`, job `102227956236`, **SUCCESS**.
- Build/installer diretamente sobre `public-candidate`: run `34262011642`, job `102188593169`, **SUCCESS**.
- Full integrado: run `34276601584`, job `102236534720`, **SUCCESS**, mas executado no repositório privado na branch temporária `tmp-final-full-validation-2026-09-08`; portanto não é prova de `full` diretamente sobre `public-candidate`.

## Critério de encerramento

A revisão de segurança somente será considerada encerrada quando os três pontos acima tiverem sido resolvidos ou formalmente aprovados para o modelo de implantação escolhido, e as alterações finais tiverem passado por nova varredura independente e validação funcional apropriada.

Até lá, `public-candidate` permanece bloqueada para merge/release em `main`.
