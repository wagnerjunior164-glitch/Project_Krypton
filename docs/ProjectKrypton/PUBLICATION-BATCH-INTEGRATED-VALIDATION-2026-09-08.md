# Lote de publicação — validação funcional integrada

Data original: 2026-09-08

## Escopo

Este documento registra a validação funcional integrada inicial da árvore `public-candidate`, executada no runner Windows `PC` após a varredura independente.

## Resultado histórico

Run: `34261625243`

Job: `102180723505`

Resultado: **SUCCESS**

Indicadores registrados:

- Python `3.12.10`;
- dependências resolvidas;
- `compileall` concluído;
- testes existentes: **4 passed**;
- `INTEGRATED_APP_SMOKE_OK`;
- `VALIDACAO_INTEGRADA_PUBLIC_CANDIDATE_OK`.

## Atualização do estado

A redação original deste documento dizia que as dependências estavam sem versões fixadas e que ainda permaneciam build, installer e full como gates de release. Isso corresponde ao estado de 2026-09-08 e é mantido aqui como registro histórico.

Posteriormente, as dependências foram fixadas no estado público e a certificação oficial `.github/workflows/public-candidate-final-validation.yml` foi concluída com sucesso, cobrindo as Parts 01–09 diretamente sobre o candidato público.

Portanto:

- esta validação funcional continua **APROVADA**;
- os gates posteriores que eram pendentes neste lote foram posteriormente concluídos;
- não há necessidade de repetir esta validação isoladamente.

## Decisão atual

A validação funcional integrada é uma evidência histórica válida e está incorporada à cadeia de certificação do candidato. O estado consolidado deve ser consultado em `PUBLICATION-STATUS.md`.
