# Lote de publicação — versão, dependências e interface estática

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

A fonte privada contém `VERSION = "0.1.0"` e `version_info()`. SHA privado confirmado: `9c33b9e54509f3676c9c334dff1a07b0f5f8dc28`. A mesma versão está presente na árvore pública candidata.

### `requirements.txt`

Manifesto privado confirmado:

```text
fastapi
uvicorn[standard]
zeroconf
```

SHA privado: `f79def74856f0d5bfdb78a2a0c0bfb90a3851155`. O manifesto foi importado para `public-candidate`.

Não foram identificados tokens, URLs privadas, credenciais ou dependências locais no manifesto.

### `static/index.html`

Importado para `public-candidate`. SHA público confirmado igual ao privado: `ceb1c6c0851e1849c8fdc03d60844c756d3eb2d1`.

O fluxo usa somente origens fornecidas pelo navegador/usuário e referências locais documentadas (`kryptonplay.local`, `127.0.0.1`); não contém caminhos de mídia específicos de ambiente privado.

### `static/admin.html`

Importado para `public-candidate`. SHA público confirmado igual ao privado: `1c48ec87427b271c9b13439606b67d0e4e7d1818`.

A página exige autenticação administrativa antes de consultar settings/libraries e não contém credenciais ou infraestrutura privada.

### `static/player.html`

A fonte privada foi recuperada integralmente para auditoria, SHA privado `27d96fa6d70d488729db78e9fa021df005646f08`. A cópia pública atual foi posteriormente corrigida e o SHA público agora coincide exatamente com o privado.

### `static/settings.html`

A fonte privada foi recuperada integralmente para auditoria, SHA privado `44a7cacf19c84d209eee666d2e50d9c9da829338`. A cópia pública atual foi posteriormente corrigida e o SHA público agora coincide exatamente com o privado.

### `static/setup.html`

A fonte privada foi recuperada integralmente para auditoria, SHA privado `a022f052fddd752434d6de453e01d0be4d53f6f6`. A cópia pública atual foi posteriormente corrigida e o SHA público agora coincide exatamente com o privado.

## Varredura independente

Após a correção da documentação para remover referências ambientais específicas, foi executada uma varredura independente da árvore `public-candidate` no runner Windows `PC`, com clone limpo da branch pública e análise de todos os arquivos fora de `.git`.

A primeira execução encontrou apenas referências históricas em documentação, incluindo um caminho de mídia privado e a identificação do repositório privado. Essas ocorrências foram tratadas como informação ambiental desnecessária para publicação e removidas da documentação pública. Não houve descoberta de credenciais, tokens, chaves ou arquivos de segredo.

A execução final da varredura, após essa sanitização, é o gate de aprovação da etapa e deve registrar `VALIDACAO_INDEPENDENTE_PUBLIC_CANDIDATE_OK`.

## Decisão do lote

Este lote **não libera a árvore para release pública**. `public-candidate` continua sendo apenas área de preparação.

Pendências obrigatórias antes de prosseguir:

1. confirmar o resultado final da varredura independente no runner `PC`;
2. concluir revisão completa de dependências e workflows/permissões;
3. executar validação funcional integrada e `build/installer/full` no runner `PC`;
4. realizar conferência final da árvore e do histórico público antes de qualquer release.

Os testes e resíduos temporários de auditoria permanecem intactos, conforme a regra de limpeza somente no encerramento.
