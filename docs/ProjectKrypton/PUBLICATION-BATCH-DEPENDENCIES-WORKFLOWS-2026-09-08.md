# Lote de publicação — dependências e workflows

Data original: 2026-09-08
Status da revisão: **HISTÓRICO — encerrado**

## Objetivo original

Registrar a revisão de dependências e workflows realizada durante a preparação inicial da publicação pública.

## Dependências

Na fase inicial, `KryptonPlay/requirements.txt` ainda não possuía pins. A ausência de versões fixadas era registrada como ponto de decisão antes da release final.

Posteriormente, o estado certificado passou a usar:

```text
fastapi==0.141.1
uvicorn[standard]==0.52.4
zeroconf==0.151.3
```

A instalação e execução dessas dependências foram validadas no runner `PC` durante a certificação pública. Portanto, a pendência de pins registrada neste lote foi encerrada.

## Workflows públicos

Na árvore pública auditada originalmente não havia workflows GitHub Actions públicos permanentes. Os workflows temporários usados na auditoria permaneceram no repositório privado e fizeram clone controlado da árvore pública para validação.

Essa separação evitou expor o runner self-hosted `PC` a execução de código não confiável durante a auditoria.

A ausência de workflows públicos não deve ser interpretada como falha do produto. O desenvolvimento, build e certificação continuam podendo ser executados por workflows privados/controlados, enquanto o repositório público mantém a árvore do produto.

Caso workflows sejam adicionados futuramente ao repositório público, devem manter permissões mínimas, não executar código não confiável em runners self-hosted privados e manter segredos fora do processo público.

## Decisão histórica

A revisão de dependências/workflows foi concluída como gate da publicação inicial. As pendências de release registradas no documento original foram posteriormente encerradas pela build, installer, validação final Parts 01–09 e publicação em `main`.

Este arquivo não representa um bloqueio atual.

Para o estado atual, consultar `docs/ProjectKrypton/PUBLICATION-STATUS.md`.
