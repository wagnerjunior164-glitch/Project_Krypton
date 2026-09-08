# Lote de publicação — version, dependencies e interface estática

Data: 2026-09-08

## Escopo

Revisão dos componentes finais previstos antes da varredura independente:

- `KryptonPlay/version.py`
- `KryptonPlay/requirements.txt`
- `KryptonPlay/static/admin.html`
- `KryptonPlay/static/index.html`
- `KryptonPlay/static/player.html`
- `KryptonPlay/static/settings.html`
- `KryptonPlay/static/setup.html`

## Resultado da auditoria

### `version.py`

A fonte privada contém `VERSION = "0.1.0"` e `version_info()`. SHA privado confirmado: `9c33b9e54509f3676c9c334dff1a07b0f5f8dc28`. A mesma versão já está presente na árvore pública candidata.

### `requirements.txt`

Manifesto privado confirmado:

```text
fastapi
uvicorn[standard]
zeroconf
```

SHA privado: `f79def74856f0d5bfdb78a2a0c0bfb90a3851155`. O manifesto foi importado para `public-candidate` no commit `f4e2856370c64797d0d94894b5ca30b699bc4694`.

Não foram identificados tokens, URLs privadas, credenciais ou dependências locais no manifesto.

### `static/index.html`

Importado para `public-candidate`. SHA público confirmado igual ao privado: `ceb1c6c0851e1849c8fdc03d60844c756d3eb2d1`.

O fluxo usa somente origens fornecidas pelo navegador/usuário e referências locais documentadas (`kryptonplay.local`, `127.0.0.1`); não contém o caminho privado de mídia `D:\Midia`.

### `static/admin.html`

Importado para `public-candidate`. SHA público confirmado igual ao privado: `1c48ec87427b271c9b13439606b67d0e4e7d1818`.

A página exige autenticação administrativa antes de consultar settings/libraries e não contém credenciais ou infraestrutura privada.

### `static/player.html`

A fonte privada foi recuperada integralmente para auditoria, SHA privado `27d96fa6d70d488729db78e9fa021df005646f08`.

**Bloqueio de integridade:** a tentativa de importação automática pela API de conteúdo não produziu um blob público com SHA idêntico; a cópia atualmente presente em `public-candidate` não deve ser considerada importação integral confirmada. Ela permanece explicitamente bloqueada para release final e deverá ser substituída por uma transferência de blob exata antes da validação final.

### `static/settings.html`

A fonte privada foi recuperada integralmente para auditoria, SHA privado `44a7cacf19c84d209eee666d2e50d9c9da829338`.

A página contém somente configuração de conta, aparência, reprodução, segurança e funções administrativas. Não foram identificados segredos ou caminhos domésticos fixos. A cópia pública foi criada, mas a confirmação final por SHA deve ser feita antes da release, pois a API de conteúdo pode normalizar escapes de JavaScript durante a reconstrução.

### `static/setup.html`

A fonte privada foi recuperada integralmente para auditoria, SHA privado `a022f052fddd752434d6de453e01d0be4d53f6f6`.

O fluxo de setup usa `America/Sao_Paulo` como valor padrão de fuso, permite escolher bibliotecas no dispositivo servidor e não contém credenciais. A cópia pública atual foi criada, porém seu SHA não coincide com o privado (`60b4d612b53d257ec1e61e8e4174c4532af1f7e1`); portanto **não é considerada importação integral confirmada** e permanece bloqueada para release.

## Decisão do lote

Este lote **não libera a árvore para release pública**. `public-candidate` continua sendo apenas área de preparação.

Pendências obrigatórias antes de prosseguir:

1. substituir `static/player.html` por blob integral com SHA `27d96fa6d70d488729db78e9fa021df005646f08`;
2. substituir/confirmar `static/settings.html` com SHA privado `44a7cacf19c84d209eee666d2e50d9c9da829338`;
3. substituir `static/setup.html` com SHA privado `a022f052fddd752434d6de453e01d0be4d53f6f6`;
4. só então executar varredura independente de segredos/ambiente e revisão final de dependências/workflows;
5. executar validação funcional integrada e `build/installer/full` no runner `PC`;
6. realizar conferência final da árvore e do histórico público antes de qualquer release.

Os testes e resíduos temporários de auditoria permanecem intactos, conforme a regra de limpeza somente no encerramento.
