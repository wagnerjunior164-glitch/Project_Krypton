# Publicação do ProjectKrypton — Estado da Preparação

## Estado

**Em preparação — não é uma release pública final.**

Este repositório utiliza uma raiz Git nova. O histórico do repositório privado de desenvolvimento não faz parte desta árvore.

## Verificação da etapa anterior

A etapa de fundação da árvore pública foi conferida diretamente no GitHub antes da continuação.

Verificações realizadas:

- `Project_Krypton` permanece público e com `main` como branch padrão.
- A branch `public-candidate` existe e está apontando para a sequência de commits da preparação pública.
- A árvore da `public-candidate` foi alimentada por commits controlados, sem importar o histórico privado do `ProjectKrypton`.
- `SECURITY.md`, `.gitignore` e `docs/ProjectKrypton/PUBLICATION-STATUS.md` estão presentes.
- O README inicial foi substituído por uma versão voltada à publicação pública, sem referências ao histórico privado como conteúdo versionado.
- O repositório privado `ProjectKrypton` continua preservado.

## Auditoria do lote de exportação do runner

A execução de auditoria `34250834831` foi usada como fonte de integridade para o lote KryptonPlay. O runner Windows exportou 24 arquivos e produziu SHA-256 localmente, permitindo que a importação fosse feita por seleção e comparação, em vez de copiar a árvore privada cegamente.

O workflow temporário de exportação não foi tratado como parte da árvore pública e continua separado da CI pública.

## Lotes importados

### Primeiro lote — fundação e documentação pública básica

Foi importado e sanitizado um primeiro lote de documentação pública básica:

- `README.md` raiz;
- `KryptonPlay/README.md`;
- `MediaStation/README.md`;
- `MemoryProject/README.md`;
- `KryptonOS Router/README.md`.

Durante a importação, foram removidos ou generalizados detalhes específicos do ambiente. O conteúdo não foi importado cegamente.

### Segundo lote — componentes KryptonPlay de baixo risco

Após inspeção individual, foram mantidos/importados:

- `KryptonPlay/diagnostics.py`;
- `KryptonPlay/scanner.py`;
- `KryptonPlay/tests/test_diagnostics.py`;
- `KryptonPlay/tests/test_scanner_library.py`;
- `KryptonPlay/config/README.md`;
- `KryptonPlay/config/config.json`.

O `config.json` foi higienizado: o caminho privado `D:\\Midia` da exportação original foi substituído por `media`, e não foi transportado nenhum segredo.

### Terceiro lote — núcleo de execução e descoberta

Foi realizada nova inspeção e foram adicionados à `public-candidate`:

- `KryptonPlay/launcher.py`;
- `KryptonPlay/playback_info.py`;
- `KryptonPlay/mdns_service.py`.

`launcher.py` foi aceito porque o código usa caminhos derivados do próprio executável/projeto e não contém credenciais nem caminhos domésticos fixos no conteúdo auditado. O endereço de abertura utilizado pelo aplicativo é o hostname neutro `kryptonplay.local`.

`playback_info.py` foi aceito como camada de diagnóstico de reprodução autenticada e não contém segredos ou infraestrutura privada.

`mdns_service.py` foi aceito porque anuncia somente o serviço local `KryptonPlay` e usa descoberta do endereço LAN em tempo de execução; não transporta IP doméstico fixo.

Os SHA-256 observados no exportador para este lote foram registrados antes da importação:

- `launcher.py`: `19f7608a01c6ac22696725cd323f15332546ccfb`;
- `playback_info.py`: `0f6c138d14e34adfe3716c53f4b6c1863cdb81a9`;
- `mdns_service.py`: `f68498bd99b9b17111e119a6323fea679840193`.

### Quarto lote — reprodução/FFmpeg

Foi concluída a auditoria de `audio_fallback.py` e `playback_pipeline.py`. Os dois arquivos foram importados integralmente para `public-candidate`, preservando o conteúdo da fonte privada auditada e sem transportar o histórico Git privado:

- `KryptonPlay/audio_fallback.py` — blob público `b2ed6fa841c2df9d2c12544a6cdb640300c293a0`;
- `KryptonPlay/playback_pipeline.py` — blob público `d1b35a4b732f5126290ab2e40699dc35605b045a`.

A análise estática deste lote confirmou:

- uso de FFmpeg/FFprobe por argumentos estruturados, sem execução via shell;
- descoberta de ferramentas por variável de ambiente, empacotamento ou PATH;
- uso de `-nostdin` nos processos FFmpeg;
- tratamento explícito de processos, stderr, timeouts e limpeza de recursos;
- cache derivado de caminho/tamanho/mtime/stream, sem nomear armazenamento doméstico específico;
- ausência de credenciais, tokens ou IP doméstico fixo no conteúdo auditado;
- integração direta com o endpoint `/api/v1/media/{media_id}/stream`.

### Validação funcional real no runner Windows

Após a autorização para usar o runner sempre que necessário, foi executado um smoke test funcional real no runner Windows `PC`, usando a própria árvore pública `Project_Krypton/public-candidate` como fonte de código.

A execução efetivamente validada foi a `34253339675`, no repositório privado, por meio de um workflow temporário isolado. O workflow fez checkout do commit público `7f40e1793da013fcc3102109c316f93102382c46` da `public-candidate` e executou no Windows os componentes `audio_fallback.py` e `playback_pipeline.py`.

O teste cobriu, de forma efetiva:

- localização de `ffmpeg` e `ffprobe` pelo mecanismo usado pelo projeto;
- geração real de mídia curta H.264 + AAC;
- geração real de mídia curta H.264 + AC3;
- análise real via FFprobe;
- classificação AAC como compatível, sem fallback;
- decisão de AAC como `direct-play`;
- classificação AC3 como incompatível;
- decisão de AC3 como `transcoding`, com razão `audio_codec_incompatible`;
- execução real do fallback progressivo, convertendo o áudio AC3 para AAC;
- geração e existência do cache `.m4a`;
- leitura posterior do mesmo cache como `cache_hit`.

Resultado observado no runner:

- `FFMPEG_FALLBACK_SMOKE_OK`;
- `AAC mode=direct-play`;
- `AC3 mode=transcoding reason=audio_codec_incompatible`;
- `progressive_bytes=84242`;
- `cache_bytes=40068`;
- `VALIDACAO_FFMPEG_FALLBACK_OK`.

A execução terminou com **sucesso** no job do runner `PC`.

Houve duas correções somente no workflow temporário de teste antes do sucesso: a primeira execução encontrou a política de execução do PowerShell do runner; a segunda completou a lógica funcional, mas falhou apenas por uma saída de diagnóstico incompatível com o parsing do PowerShell. Nenhuma dessas ocorrências indicou falha do código KryptonPlay. A terceira execução foi a válida e terminou aprovada.

O workflow temporário usado no repositório privado não faz parte da árvore pública. A tentativa inicial de workflow diretamente na `public-candidate` ficou sem runner público disponível e foi removida; o teste válido foi então executado no runner privado `PC`, fazendo checkout explícito da árvore pública. O workflow público temporário também foi removido após a validação.

Portanto, a validação funcional real de FFmpeg deste lote **não está mais pendente**: ela foi executada e aprovada para os cenários cobertos acima. Isso não substitui a validação E2E completa da aplicação nem a validação final de build/installer.

### Correção da cópia truncada anterior

Na etapa anterior, uma cópia truncada de `audio_fallback.py` chegou a ser criada por engano. Ela foi removida imediatamente no commit `985b7291ce5b322ffc5f9015ca771f62fdcbcb2f`. A versão atualmente presente na `public-candidate` é uma nova importação integral da fonte privada auditada e não deriva daquela cópia truncada.

### Validação de `app.py` contra a árvore pública candidata

Foi executada a validação funcional da aplicação candidata no runner Windows `PC` por meio da execução `34255010907` do workflow privado `Unified validation`.

A execução foi feita em `main` do repositório privado, no commit `2a3924eda0b0ec1eb3b041df66d411a19a443316`, e o teste temporário clona explicitamente `wagnerjunior164-glitch/Project_Krypton`, branch `public-candidate`, em um diretório temporário. Assim, o processo não testou uma cópia privada de `app.py`: ele iniciou o `app.py` efetivamente presente na árvore pública candidata.

O smoke test usa HTTP real contra um processo `uvicorn app:app` iniciado no próprio Windows runner, sem `TestClient`/`httpx`. Foram exercitados:

- inicialização real do `app.py`;
- `GET /health`;
- `GET /api/setup/status`;
- `GET /api/auth/users`;
- login do usuário `admin` com senha efêmera exclusiva do runner;
- autenticação por Bearer token;
- `GET /api/auth/me`;
- `GET /api/v1/settings`;
- `GET /api/v1/libraries`;
- `GET /api/v1/library`;
- `GET /api/v1/status`;
- `POST /api/v1/library/scan`;
- `POST /api/auth/logout`;
- confirmação de `401` após logout em `/api/auth/me`.

A implementação do teste temporário registra explicitamente `PUBLIC_CANDIDATE_APP_SMOKE_OK` somente depois de todos esses asserts passarem. O código do teste confirma essa marca de sucesso e também confirma o uso de `public-candidate`, `uvicorn`, `urllib` e `sys.executable`. fileciteturn189file0L2-L6

No run `34255010907`, a etapa `Run unified validation` registrou:

- arquivo alterado selecionado: `KryptonPlay/tests/test_public_candidate_app.py`;
- `19 passed in 25.29s`;
- `KryptonPlay unit/functional tests — PASS`;
- `KryptonPlay Web E2E — PASS`;
- `Resultado: CONCLUIDO`.

O log do runner não reproduz a linha `PUBLIC_CANDIDATE_APP_SMOKE_OK` porque a execução é feita pelo pytest e a saída de `print` do teste não é exibida nesse nível de captura. Portanto, a evidência decisiva é a combinação do teste presente no commit executado e o resultado de `19 passed`, não uma alegação baseada apenas no nome da etapa. O teste só chega ao `print` final depois dos asserts descritos acima. fileciteturn189file0L2-L6

O upload do relatório JSON falhou posteriormente por quota de armazenamento de artefatos do GitHub (`Artifact storage quota has been hit`). Isso ocorreu depois de `Run unified validation` ter concluído com sucesso e não invalida os testes executados. O próprio job registrou que o relatório existia localmente antes da tentativa de upload.

**Conclusão desta etapa:** `app.py` está **validado funcionalmente contra a árvore pública candidata**, incluindo inicialização, autenticação, endpoints principais, scan e invalidação de sessão no runner Windows `PC`. Essa validação não constitui ainda aprovação de release, pois permanecem a auditoria dos demais arquivos, a reconciliação da documentação de hash/scrypt versus PBKDF2-SHA256, a varredura final independente e a validação final de build/installer.

## Arquivos deliberadamente não importados nesta etapa

Os seguintes componentes do lote original de 24 arquivos permanecem sob revisão:

- `KryptonPlay/playback_ui.py`;
- `KryptonPlay/admin_features.py`;
- `KryptonPlay/ui_runtime.py`;
- `KryptonPlay/update_api.py`;
- `KryptonPlay/update_service.py`;
- `KryptonPlay/updater.py`;
- `KryptonPlay/kryptonplay_fixes.py`;
- `KryptonPlay/increment24_hardening.py`;
- `KryptonPlay/version.py`;
- `KryptonPlay/requirements.txt`;
- `KryptonPlay/static/admin.html`;
- `KryptonPlay/static/index.html`;
- `KryptonPlay/static/player.html`;
- `KryptonPlay/static/settings.html`;
- `KryptonPlay/static/setup.html`.

A razão é controle de acoplamento e segurança: vários desses arquivos participam de autenticação, administração, atualização automática, UI dinâmica, instalação ou distribuição. Eles serão importados somente depois da análise de suas dependências e compatibilidade com a árvore pública.

## Constatação específica de configuração

A exportação privada original continha o caminho absoluto:

`D:\\Midia`

Esse valor foi explicitamente bloqueado pela auditoria pública. A versão presente na `public-candidate` usa `media` e não expõe a estrutura de armazenamento doméstica.

## Verificações realizadas

Foram conferidos, entre outros pontos:

- ausência do caminho privado `D:\\Midia` no `config.json` público;
- ausência de credenciais e tokens nos arquivos importados deste lote;
- ausência de IP doméstico fixo no `mdns_service.py`;
- uso de `kryptonplay.local` como hostname neutro;
- manutenção da branch `public-candidate` como área de preparação;
- preservação do bloqueio de release até a conclusão da auditoria integral;
- remoção da cópia truncada anterior de `audio_fallback.py`;
- importação integral de `audio_fallback.py` e `playback_pipeline.py` após recuperação direta dos blobs da fonte privada;
- execução funcional real de FFmpeg/FFprobe no runner Windows `PC` contra a árvore pública candidata;
- execução funcional real de `app.py` no runner Windows `PC` contra a branch pública `public-candidate`.

Essas verificações são direcionadas e não substituem a varredura final completa.

## Critérios obrigatórios antes da release

- revisar a árvore completa arquivo por arquivo;
- remover ou generalizar qualquer informação específica do ambiente de desenvolvimento;
- remover credenciais, tokens, cookies, chaves e valores secretos;
- garantir que testes usem valores efêmeros ou fictícios;
- garantir que workflows de Pull Request não executem código não confiável em runners privados;
- revisar permissões do `GITHUB_TOKEN` e referências das Actions;
- revisar dependências e reprodutibilidade;
- revisar documentação, índices e exemplos;
- executar uma varredura independente após a higienização;
- executar validação funcional e de build da árvore pública;
- somente então aprovar a primeira release pública.

## Regra de histórico

A árvore pública não deve receber branches, tags ou commits do repositório privado. A remoção de um arquivo da árvore privada não é usada como mecanismo de sanitização da publicação.

## Regra de segurança

Nenhum segredo deve ser considerado aceitável apenas por ser destinado a testes. Valores de teste devem ser gerados no momento da execução, fornecidos por ambiente seguro ou claramente não reutilizáveis.

## Próxima etapa

Continuar com `playback_ui.py` e, em seguida, os componentes de administração, runtime, atualização e UI. `app.py` agora possui validação funcional específica aprovada contra a árvore pública candidata no runner Windows. A partir deste ponto, os próximos arquivos devem ser auditados considerando o acoplamento já confirmado com `app.py`.

Quando a árvore candidata estiver completa e auditada, a validação funcional integrada, build e installer serão executadas no `main`, antes da release. Workflows e automações de CI continuam separados desta etapa e não serão copiados até que sejam reescritos para o ambiente público.

## Aprovação

**Status da árvore:** BLOQUEADA PARA RELEASE PÚBLICA FINAL.

A documentação foi atualizada após a validação funcional de `app.py` para registrar a execução `34255010907`, o commit privado de teste, a confirmação de que o teste clona e executa a `public-candidate`, os endpoints cobertos, o resultado de `19 passed` e a limitação posterior de quota de artefatos. 
