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

O workflow temporário não foi tratado como parte da árvore pública e continua separado da CI pública.

## Lotes importados

### Primeiro lote — fundação e documentação pública

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
- `mdns_service.py`: `f68498bd99b9b17111e119a6323fea6798401939`.

### Quarto lote — reprodução/FFmpeg

Foi concluída a auditoria de `audio_fallback.py` e `playback_pipeline.py` e, conforme autorizado, **não foi realizado teste funcional real de FFmpeg nesta fase**. A validação funcional será feita posteriormente, depois que a árvore estiver pronta no `main`.

Os dois arquivos foram importados integralmente para `public-candidate`, preservando o conteúdo da fonte privada auditada e sem transportar o histórico Git privado:

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

**Validação funcional real fica deliberadamente pendente** e será executada somente na fase posterior em `main`, conforme definido para esta preparação.

### Correção da cópia truncada anterior

Na etapa anterior, uma cópia truncada de `audio_fallback.py` chegou a ser criada por engano. Ela foi removida imediatamente no commit `985b7291ce5b322ffc5f9015ca771f62fdcbcb2f`. A versão atualmente presente na `public-candidate` é uma nova importação integral da fonte privada auditada e não deriva daquela cópia truncada.

## Arquivos deliberadamente não importados nesta etapa

Os seguintes componentes do lote original de 24 arquivos permanecem sob revisão:

- `KryptonPlay/app.py`;
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
- importação integral de `audio_fallback.py` e `playback_pipeline.py` após recuperação direta dos blobs da fonte privada.

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

Continuar com `app.py` e, em seguida, os componentes de administração, runtime, atualização e UI. O objetivo agora é fechar as dependências da unidade executável sem realizar ainda os testes funcionais reais de FFmpeg. Quando a árvore candidata estiver completa e auditada, a validação funcional/build será executada posteriormente no `main`, antes da release.

Workflows e automações de CI continuam separados desta etapa e não serão copiados até que sejam reescritos para o ambiente público.

## Aprovação

**Status da árvore:** BLOQUEADA PARA RELEASE PÚBLICA FINAL.

A documentação foi atualizada após o quarto lote para registrar a importação integral dos componentes de reprodução, a decisão explícita de adiar os testes funcionais reais e os arquivos que ainda permanecem sob revisão.
