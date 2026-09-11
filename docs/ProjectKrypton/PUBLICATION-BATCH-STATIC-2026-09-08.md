# Lote de publicação — versão, dependências e interface estática

Data original: 2026-09-08
Status: **HISTÓRICO — encerrado**

## Escopo original

Revisão dos componentes finais previstos antes da varredura independente:

- `KryptonPlay/version.py`
- `KryptonPlay/requirements.txt`
- `KryptonPlay/static/admin.html`
- `KryptonPlay/static/index.html`
- `KryptonPlay/static/player.html`
- `KryptonPlay/static/settings.html`
- `KryptonPlay/static/setup.html`

## Resultado histórico da auditoria

Este documento registra o estado da árvore durante a preparação pública de 2026-09-08. Os hashes abaixo identificam o estado auditado naquele momento e não devem ser tratados como hashes atuais sem nova consulta à árvore.

### `version.py`

A fonte privada continha `VERSION = "0.1.0"` e `version_info()`. SHA privado confirmado naquele lote: `9c33b9e54509f3676c9c334dff1a07b0f5f8dc28`.

### `requirements.txt`

Naquele momento o manifesto ainda estava sem pins:

```text
fastapi
uvicorn[standard]
zeroconf
```

Posteriormente, o estado certificado passou a usar versões fixadas, conforme documentado em `PUBLICATION-STATUS.md`.

### Interfaces estáticas

As páginas `index.html`, `admin.html`, `player.html`, `settings.html` e `setup.html` foram auditadas e corrigidas durante o processo de preparação pública. As versões finais foram incorporadas ao candidato certificado.

## Varredura independente

Após a correção da documentação para remover referências ambientais específicas, foi executada uma varredura independente da árvore `public-candidate` no runner Windows `PC`, com clone limpo da branch pública e análise dos arquivos fora de `.git`.

A primeira execução encontrou referências históricas em documentação. Essas ocorrências foram tratadas como informação ambiental desnecessária para publicação e removidas da documentação pública. Não houve descoberta de credenciais, tokens, chaves ou arquivos de segredo no estado final certificado.

A execução final da varredura foi posteriormente concluída como parte dos gates de publicação.

## Decisão histórica do lote

Este lote **não liberava a árvore para release pública naquele momento**. As pendências listadas abaixo eram válidas somente em 2026-09-08:

1. confirmar o resultado final da varredura independente no runner `PC`;
2. concluir revisão completa de dependências e workflows/permissões;
3. executar validação funcional integrada e `build/installer/full` no runner `PC`;
4. realizar conferência final da árvore e do histórico público antes de qualquer release.

Todas essas pendências foram posteriormente encerradas por validações específicas e pela certificação pública Parts 01–09.

Para o estado atual, consultar `docs/ProjectKrypton/PUBLICATION-STATUS.md`.
