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

## Primeiro lote importado após a verificação

Foi importado e sanitizado um primeiro lote de documentação pública básica:

- `README.md` raiz;
- `KryptonPlay/README.md`;
- `MediaStation/README.md`;
- `MemoryProject/README.md`;
- `KryptonOS Router/README.md`.

Durante a importação, foram removidos ou generalizados detalhes específicos do ambiente, como o caminho local da biblioteca de mídia e referências a equipamento de laboratório. O conteúdo não foi importado cegamente.

O `KryptonOS/README.md` não foi importado neste lote porque a leitura disponível não permitiu verificar integralmente o documento; ele permanece para uma importação posterior com conteúdo completo.

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

Continuar a importação em lotes pequenos, começando pelos componentes de documentação e configuração que possam ser classificados como `PUBLICAR` ou `HIGIENIZAR`, e tratar workflows, scripts, testes e código somente após inspeção individual.
