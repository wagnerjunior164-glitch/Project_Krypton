# Lote de publicação — dependências e workflows

Data: 2026-09-08

## Dependências

`KryptonPlay/requirements.txt` contém somente:

```text
fastapi
uvicorn[standard]
zeroconf
```

A validação integrada no runner `PC` confirmou a instalação e execução dessas dependências com Python `3.12.10`.

Não foram fixadas versões arbitrariamente durante a auditoria. A ausência de pins reduz a reprodutibilidade entre ambientes e permanece como ponto de decisão antes da release final: fixar versões somente após uma revisão de compatibilidade/segurança e atualizar o teste integrado para validar o conjunto fixado.

Não foram encontrados tokens, URLs privadas, dependências por caminho local ou artefatos de ambiente no manifesto.

## Workflows públicos

A árvore `public-candidate` auditada não contém workflows GitHub Actions públicos. Isso significa que, no estado atual, nenhum workflow público executa código de PR não confiável em um runner self-hosted privado.

Os workflows temporários usados nesta auditoria permaneceram exclusivamente no repositório privado e apenas fizeram clone controlado da branch pública para validação. Eles não foram publicados na árvore candidata.

Antes da release final, se workflows forem adicionados ao repositório público, devem usar `permissions` mínimas, evitar `pull_request_target` para executar código não confiável, não expor o runner self-hosted `PC` a PRs públicos e manter segredos fora do processo de validação pública.

## Decisão

A revisão de dependências/workflows está **CONCLUÍDA para o estado atual da árvore**.

Pendência de release: decidir e documentar o conjunto de versões das dependências e desenhar os workflows públicos finais sem acesso ao runner privado.

A release permanece bloqueada até `build`, `installer`, `full` e auditoria final da árvore/histórico.
