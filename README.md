# ProjectKrypton

O **ProjectKrypton** é um ecossistema modular para organizar, documentar e desenvolver projetos de forma estruturada, incremental e rastreável.

Este repositório é a **árvore pública oficial do produto disponibilizado**. Ele possui uma nova raiz Git e não incorpora o histórico privado de desenvolvimento.

## Módulos

- **KryptonPlay** — servidor de mídia próprio, independente do MediaStation/Jellyfin.
- **MediaStation** — gerenciamento de biblioteca de mídia baseado em Jellyfin.
- **MemoryProject** — organização, indexação, pesquisa e recuperação de conhecimento.
- **KryptonOS** — plataforma de uso geral em desenvolvimento planejado sobre Linux.
- **KryptonOS Router** — variante futura para rede e appliances baseada em OpenWrt/Linux.

## Estado da publicação

A primeira publicação pública foi **concluída e certificada**.

- Repositório público: `wagnerjunior164-glitch/Project_Krypton`.
- Branch pública: `main`.
- Commit publicado da primeira versão: `3d8e3bd762ad2a87a63cc931f51b2fa19e33f0e4`.
- Certificação técnica: **Parts 01–09 — PASS**.
- A Part 10 permanece suspensa para reavaliação futura e não é requisito da certificação pública atual.

A referência consolidada do estado de publicação é `docs/ProjectKrypton/PUBLICATION-STATUS.md`.

## Desenvolvimento privado e produto público

O projeto mantém dois ambientes relacionados, mas independentes:

- `wagnerjunior164-glitch/ProjectKrypton` — desenvolvimento e controle técnico privado;
- `wagnerjunior164-glitch/Project_Krypton` — produto público disponibilizado.

Não existe sincronização automática bidirecional entre os repositórios. O fluxo normal é:

`privado → validação → public-candidate → validação final necessária → público/main`

Correções urgentes podem ser feitas diretamente no público quando necessário, mas devem ser reproduzidas no privado depois da validação para evitar divergência técnica.

## Validação, build e atualização

A certificação pública atual termina deliberadamente na **Part 09**. A validação específica do atualizador é mantida separada e utiliza o produto real gerado pelo runner Windows `PC` como versão A, comparando-o com uma Release B pública mais recente.

A arquitetura de desenvolvimento também prevê um workflow modular separado para desenvolvimento, testes, build, installer, persistência, atualização e diagnóstico, sem alterar a cadeia oficial de certificação Parts 01–09.

Os detalhes operacionais e o histórico ficam em `docs/ProjectKrypton/`.

## Segurança

Consulte `SECURITY.md` para orientações de reporte de vulnerabilidades.

## Histórico

O histórico privado do desenvolvimento não faz parte deste repositório público. A publicação utiliza uma raiz Git independente e somente componentes aprovados foram adicionados à árvore pública.
