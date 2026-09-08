# Publicação do ProjectKrypton — Estado da Preparação

## Estado

**Em preparação — não é uma release pública final.**

Este repositório utiliza uma raiz Git nova. O histórico do repositório privado de desenvolvimento não faz parte desta árvore.

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

A próxima etapa é importar os componentes aprovados do projeto em lotes controlados, sanitizando cada lote antes de adicioná-lo à árvore pública.
