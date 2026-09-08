# Lote de publicação — validação funcional integrada

Data: 2026-09-08

## Escopo

Validação da árvore `public-candidate` em clone limpo, executada no runner Windows `PC`, após a varredura independente de publicação.

## Método

O workflow temporário permaneceu no repositório privado e clonou diretamente a branch pública candidata. O ambiente utilizou Python 3.12, instalou exatamente o manifesto `KryptonPlay/requirements.txt`, compilou o código Python e executou os testes existentes antes de iniciar o servidor.

A etapa de aplicação iniciou `uvicorn app:app` em loopback temporário e verificou o fluxo de setup, diagnóstico, criação inicial do administrador, login, autenticação Bearer, settings, libraries e logout.

## Resultado

Run: `34261625243`

Job: `102180723505`

Resultado: **SUCCESS**

Indicadores do log:

- Python `3.12.10`;
- dependências do manifesto resolvidas com sucesso;
- `compileall` concluído;
- testes existentes: **4 passed**;
- `INTEGRATED_APP_SMOKE_OK`;
- `VALIDACAO_INTEGRADA_PUBLIC_CANDIDATE_OK`.

Nenhuma falha funcional foi encontrada nessa etapa.

## Dependências

O manifesto continua sem versões fixadas (`fastapi`, `uvicorn[standard]`, `zeroconf`). A instalação e execução no runner confirmaram compatibilidade do estado atual com Python 3.12. Não foi feita alteração arbitrária de versões; a decisão de fixação permanece para a revisão de reprodutibilidade antes da release final.

## Decisão

A validação funcional integrada está **APROVADA para a etapa atual**.

Isso ainda não libera a release final: permanecem `build`, `installer` e `full`, incluindo integração real do instalador/updater, e a conferência final da árvore, histórico, branches e tags públicos.

Os workflows e scripts temporários usados para esta auditoria permanecem fora da árvore pública e não serão removidos antes do encerramento da auditoria.
