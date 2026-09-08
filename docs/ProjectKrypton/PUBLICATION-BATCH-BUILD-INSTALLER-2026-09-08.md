# Lote de publicação — preparação de build e installer

Data: 2026-09-08

## Descoberta

A revisão da árvore candidata mostrou que a validação integrada anterior estava funcional, mas o conjunto público ainda não continha os componentes necessários para executar o pipeline Windows de `build/installer` previsto no validador privado.

Foram auditadas as fontes privadas correspondentes e importadas para `public-candidate`:

- `KryptonPlay/KryptonPlay.spec` — SHA privado/público confirmado: `2cdbb4f4ccaca5ee88cad8d87735d3fe91687bd4`;
- `KryptonPlay/KryptonPlay-Updater.spec` — SHA privado/público confirmado: `a0e7b00b6a75959df8ddf75f31c7b7556fd56a09`;
- `KryptonPlay/installer/KryptonPlay-Windows.iss` — SHA privado/público confirmado: `904aeaaae52bcd235d4b080d2f0a10b68f2bdb80`;
- `KryptonPlay/tests/e2e_web_test.py` — SHA privado/público confirmado: `23acfbf6158532d6e82ab0027c71d9cea9847796`;
- `KryptonPlay/tests/run_e2e_server.py` — SHA privado/público confirmado: `4fd842404c5026c1fe88fec4e05533c11b136ac4`.

Não foi feita sanitização de conteúdo nesses cinco arquivos porque os blobs foram conferidos exatamente. O spec principal resolve FFmpeg/FFprobe por configuração, bundle, PATH ou Chocolatey; não contém caminho de mídia do ambiente privado.

## Validação solicitada ao runner

Foi criado no repositório privado um workflow temporário que clona `public-candidate`, instala as dependências, instala PyInstaller, executa os dois builds PyInstaller e compila o instalador com Inno Setup 6.

Run: `34262011642`

Job: `102182033615`

No momento do registro deste documento, o job permanece **QUEUED** aguardando o runner Windows `PC`. Portanto, **não há aprovação de build/installer ainda**.

## Decisão

A árvore agora contém as fontes necessárias para o pipeline Windows, mas o gate permanece pendente até o runner concluir com:

- `WINDOWS_BUILD_OK`;
- `WINDOWS_INSTALLER_OK`;
- `VALIDACAO_BUILD_INSTALLER_PUBLIC_CANDIDATE_OK`.

Depois desse gate, ainda será necessário executar `full`, incluindo E2E real e integração final do updater, e então fazer a auditoria final de árvore/histórico.

Os workflows/scripts temporários permanecem exclusivamente no repositório privado e não fazem parte da publicação.
