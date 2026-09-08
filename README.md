# ProjectKrypton

O **ProjectKrypton** é um ecossistema modular para organizar, documentar e desenvolver projetos de forma estruturada, incremental e rastreável.

Este repositório é a **árvore pública preparada para distribuição**. Ele possui uma nova raiz Git e não incorpora o histórico privado de desenvolvimento.

## Módulos

- **KryptonPlay** — servidor de mídia próprio, independente do MediaStation/Jellyfin.
- **MediaStation** — gerenciamento de biblioteca de mídia baseado em Jellyfin.
- **MemoryProject** — organização, indexação, pesquisa e recuperação de conhecimento.
- **KryptonOS** — plataforma de uso geral em desenvolvimento planejado sobre Linux.
- **KryptonOS Router** — variante futura para rede e appliances baseada em OpenWrt/Linux.

## Estado da publicação

A árvore pública ainda está **em preparação** e não representa uma release final.

Antes da primeira release serão concluídos:

- revisão arquivo por arquivo;
- remoção de informações específicas de ambientes privados;
- remoção de credenciais, tokens e outros segredos;
- substituição de valores fixos de teste por valores seguros;
- revisão de workflows e permissões do `GITHUB_TOKEN`;
- garantia de que Pull Requests não executem código não confiável em runners privados;
- revisão de dependências e reprodutibilidade;
- revisão da documentação e exemplos;
- varredura independente de segurança;
- validação funcional e de build;
- aprovação formal da primeira release pública.

Consulte `docs/ProjectKrypton/PUBLICATION-STATUS.md` para o estado atual da preparação.

## Segurança

Consulte `SECURITY.md` para orientações de reporte de vulnerabilidades.

## Histórico

O histórico privado do desenvolvimento não faz parte deste repositório público. A publicação utiliza uma raiz Git independente e somente componentes aprovados serão adicionados à árvore.
