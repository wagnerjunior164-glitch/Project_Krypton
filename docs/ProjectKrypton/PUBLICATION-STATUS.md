# Publicação do ProjectKrypton — Estado da Preparação

## Estado

**Em preparação — não é uma release pública final.**

Este repositório utiliza uma raiz Git nova. O histórico do repositório privado de desenvolvimento não faz parte desta árvore.

## Verificação da etapa anterior

A etapa de fundação da árvore pública foi conferida diretamente no GitHub antes da continuação.

Verificações realizadas:

- `Project_Krypton` permanece público e com `main` como branch padrão.
- A branch `public-candidate` existe e está apontando para a sequência de commits da preparação pública.
- A árvore da `public-candidate` contém somente os elementos de fundação inicialmente previstos antes da importação controlada, sem histórico privado do `ProjectKrypton`.
- `SECURITY.md`, `.gitignore` e `docs/ProjectKrypton/PUBLICATION-STATUS.md` estão presentes.
- O README inicial foi substituído por uma versão voltada à publicação pública, sem referências ao histórico privado como conteúdo versionado.
- O repositório privado `ProjectKrypton` continua privado e não foi reescrito nem teve seu histórico exposto.

A verificação confirmou que a etapa anterior foi executada corretamente como **fundação**. Ela, porém, não significava que o código do projeto já tivesse sido importado; essa importação ainda não estava concluída.

## Constatações que permanecem bloqueadoras

A revisão do repositório privado confirmou que a importação integral ainda não pode ser feita sem sanitização adicional. Entre os pontos já identificados estão:

- workflow de validação com `runs-on: [self-hosted, windows, x64]`;
- credenciais fixas de teste/demonstração em arquivos do projeto;
- caminhos específicos de ambiente, incluindo infraestrutura local do Windows;
- documentação operacional privada e arquivos de staging/runner;
- dependências Python sem versionamento completo;
- necessidade de revisão das permissões dos workflows e de referências das Actions;
- necessidade de revisão histórica independente antes de qualquer release pública.

A documentação privada de publicação permanece a fonte do checklist detalhado; esta árvore pública não deve transformar um item pendente em item aprovado apenas porque um arquivo foi copiado.

## Lotes importados

### Primeiro lote — fundação e documentação pública

Foi importado e sanitizado um primeiro lote de documentação pública básica:

- `README.md` raiz;
- `KryptonPlay/README.md`;
- `MediaStation/README.md`;
- `MemoryProject/README.md`;
- `KryptonOS Router/README.md`.

Durante a importação, foram removidos ou generalizados detalhes específicos do ambiente, como o caminho local da biblioteca de mídia e referências a equipamento de laboratório. O conteúdo não foi importado cegamente.

### Segundo lote — componentes KryptonPlay de baixo risco

Após nova inspeção individual, foi importado um segundo lote pequeno e controlado:

- `KryptonPlay/diagnostics.py`;
- `KryptonPlay/scanner.py`;
- `KryptonPlay/tests/test_diagnostics.py`;
- `KryptonPlay/tests/test_scanner_library.py`;
- `KryptonPlay/config/README.md`;
- `KryptonPlay/config/config.json`.

O `config.json` foi **higienizado**, substituindo o caminho absoluto específico de ambiente por `media`. Nenhum segredo ou credencial foi incluído.

Este lote não inclui ainda `app.py`, `launcher.py`, workflows, scripts operacionais, arquivos de staging ou demais componentes de alto acoplamento. Esses itens continuam sujeitos a inspeção individual.

## Verificações após o segundo lote

Foi realizada uma busca direcionada na árvore pública por indicadores que já haviam sido identificados na auditoria privada:

- `D:\Midia` — não encontrado;
- `TestPassword-123!` — não encontrado;
- `Demo-KryptonPlay-2026` — não encontrado;
- `self-hosted` — não encontrado;
- `C:\Users\wagner` — não encontrado.

Essas buscas são evidências de uma varredura direcionada, não substituem a varredura final completa.

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

Continuar a importação em lotes pequenos. O próximo grupo deve priorizar código necessário para formar uma unidade executável do KryptonPlay, mas somente depois da inspeção completa de suas dependências e da remoção de qualquer referência privada. Workflows e automações de CI continuam separados dessa etapa e não serão copiados até que tenham sido reescritos para o ambiente público.
