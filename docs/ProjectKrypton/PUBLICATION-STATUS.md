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

## Arquivos deliberadamente não importados nesta etapa

Os seguintes componentes do lote de 24 arquivos permanecem sob revisão e **não devem ser considerados aprovados** apenas por terem sido recuperados pelo runner:

- `app.py`;
- `audio_fallback.py`;
- `playback_pipeline.py`;
- `playback_ui.py`;
- `admin_features.py`;
- `ui_runtime.py`;
- `update_api.py`;
- `update_service.py`;
- `updater.py`;
- `kryptonplay_fixes.py`;
- `increment24_hardening.py`;
- `version.py`;
- `requirements.txt`;
- `static/admin.html`;
- `static/index.html`;
- `static/player.html`;
- `static/settings.html`;
- `static/setup.html`.

A razão é controle de acoplamento e segurança: vários desses arquivos participam de autenticação, administração, atualização automática, execução de subprocessos, UI dinâmica ou distribuição. Eles serão importados somente depois da análise de suas dependências e de sua compatibilidade com a árvore pública.

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
- preservação do bloqueio de release até a conclusão da auditoria integral.

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

Continuar a importação em lotes pequenos, priorizando a unidade executável do KryptonPlay. Antes de importar o restante, devem ser resolvidas as dependências de `app.py`, reprodução/FFmpeg, administração, atualização automática e arquivos estáticos. Workflows e automações de CI continuam separados desta etapa e não serão copiados até que sejam reescritos para o ambiente público.

## Aprovação

**Status da árvore:** BLOQUEADA PARA RELEASE PÚBLICA FINAL.

A documentação foi atualizada após o terceiro lote para registrar exatamente o que foi importado, o que foi sanitizado, o que permanece bloqueado e os critérios que ainda impedem a publicação.
