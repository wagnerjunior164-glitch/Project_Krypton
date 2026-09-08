# Estratégia de Licenciamento do KryptonPlay

Data: 2026-09-08  
Status: planejamento — não é a licença jurídica definitiva do projeto

## Objetivo

Definir uma direção de licenciamento para o KryptonPlay que seja compatível com publicação pública, preservação das liberdades da Community, futura monetização, confiança dos usuários, contribuições externas e eventual licenciamento comercial.

Este documento é uma decisão de produto/engenharia em preparação. **Não substitui revisão jurídica.**

## Recomendação inicial

A hipótese recomendada para estudo é:

> **KryptonPlay Community sob GNU Affero General Public License v3.0 (AGPL-3.0), com possibilidade de licença comercial separada quando juridicamente possível.**

A escolha continua provisória. Nenhuma licença definitiva deve ser publicada antes da auditoria de autoria, copyright e componentes de terceiros.

## O que a AGPL resolve

A AGPL oferece copyleft forte e é especialmente relevante para software que interage com usuários pela rede. Ela pode preservar as condições de liberdade da Community também em cenários de uso como serviço, conforme os termos aplicáveis da licença.

Ela não significa que o software tenha de ser gratuito e não impede cobrança por suporte, serviços ou outras ofertas compatíveis com a licença.

## O que a AGPL não resolve

A licença do KryptonPlay não concede direitos sobre código ou conteúdo pertencente a terceiros.

A AGPL também não impede, por si só:

- concorrentes;
- forks;
- produtos semelhantes;
- uso gratuito;
- distribuição permitida pela licença.

O projeto deve permanecer independente em código, documentação, identidade visual e marcas.

## Jellyfin e similaridade funcional

O fato de o KryptonPlay possuir funcionalidades semelhantes às de outros media servers, inclusive Jellyfin, não significa por si só que exista infração de copyright.

A regra operacional do projeto é:

> **Similaridade funcional pode existir; cópia de implementação, conteúdo ou identidade não deve existir.**

Antes do release deve ser verificado, em particular:

- ausência de código copiado do Jellyfin;
- ausência de testes ou documentação copiados;
- ausência de elementos de marca que criem associação indevida;
- identidade própria do KryptonPlay;
- histórico público sem introdução acidental de conteúdo de terceiros protegido.

Qualquer dúvida concreta sobre origem de um trecho deve ser tratada antes da publicação.

## Dependências e FFmpeg

A licença do KryptonPlay **não substitui** a licença das dependências.

O FFmpeg deve ser auditado separadamente. A licença efetiva depende da distribuição/build utilizada e dos componentes habilitados. Antes de distribuir o instalador Windows, devemos identificar exatamente:

1. versão do FFmpeg;
2. origem do binário;
3. configuração/build;
4. componentes habilitados;
5. licença aplicável;
6. avisos e código-fonte correspondente que precisem acompanhar a distribuição.

A mesma regra vale para FastAPI, Uvicorn, zeroconf, Python, PyInstaller, Inno Setup e demais componentes efetivamente distribuídos.

As dependências Python atualmente fixadas no candidato são FastAPI 0.141.1, Uvicorn 0.52.4 e zeroconf 0.151.3; suas licenças ainda fazem parte da auditoria futura.

## Auditoria futura de licenciamento

A auditoria será executada posteriormente, como atividade formal do projeto, e deverá:

1. identificar autores e titulares dos direitos do código próprio;
2. verificar contribuições e código recebido de terceiros;
3. procurar cabeçalhos de copyright e avisos de licença;
4. procurar referências e possíveis componentes originados de projetos como Jellyfin;
5. mapear todas as dependências Python;
6. identificar componentes incluídos no instalador;
7. auditar o FFmpeg efetivamente distribuído;
8. verificar PyInstaller e demais ferramentas/componentes redistribuídos;
9. confirmar compatibilidade das licenças;
10. preparar `THIRD-PARTY-NOTICES.md`;
11. definir política de contribuições;
12. somente depois decidir e publicar a licença definitiva.

**Essa auditoria fica deliberadamente pendente e não será substituída por uma suposição baseada apenas nos nomes das dependências.**

## Autoria, copyright e contribuições

Antes de aceitar contribuições públicas significativas, o projeto deve definir como os direitos sobre contribuições serão tratados.

Devem ser avaliadas:

- DCO;
- CLA;
- manutenção de copyright individual;
- concessão necessária para eventual dual licensing.

A estratégia comercial futura só deve prometer relicenciamento quando o projeto possuir os direitos necessários sobre o código envolvido.

## Modelo comercial compatível a estudar

Uma hipótese é:

```text
Community
   AGPL-3.0
      │
      ├── uso livre conforme a licença
      ├── modificações conforme a licença
      └── ecossistema aberto

Oferta comercial
      │
      ├── suporte profissional
      ├── instalação/configuração
      ├── Server Pro
      ├── recursos adicionais juridicamente separados
      └── serviços empresariais
```

Um produto comercial não pode simplesmente pegar código AGPL e remover os direitos concedidos pela licença. Qualquer arquitetura Community/Pro ou dual licensing deverá ser desenhada com separação técnica e jurídica adequada.

## Arquivos esperados para o release definitivo

Quando a licença for aprovada, espera-se pelo menos:

```text
LICENSE
README.md
THIRD-PARTY-NOTICES.md
CONTRIBUTING.md
```

Quando aplicável, cabeçalhos SPDX/copyright também deverão ser consistentes com a política adotada.

## Gate obrigatório antes do release

- [ ] auditoria de autoria concluída;
- [ ] copyright confirmado;
- [ ] código/documentação/testes de terceiros auditados;
- [ ] independência em relação ao Jellyfin confirmada;
- [ ] dependências mapeadas;
- [ ] FFmpeg efetivamente distribuído auditado;
- [ ] componentes do instalador auditados;
- [ ] compatibilidade das licenças confirmada;
- [ ] política de contribuições definida;
- [ ] estratégia Community/Commercial definida;
- [ ] `LICENSE` definitivo criado;
- [ ] `THIRD-PARTY-NOTICES.md` criado/atualizado;
- [ ] `CONTRIBUTING.md` atualizado;
- [ ] revisão jurídica realizada quando necessária.

## Decisão provisória

**AGPL-3.0 permanece a recomendação estratégica, mas a licença definitiva fica adiada até a auditoria de terceiros.**

Essa decisão é intencional. É mais seguro concluir a auditoria antes de publicar uma licença do que assumir que todas as partes do produto possuem o mesmo regime jurídico.

## Relação com o release atual

Este documento não desbloqueia `public-candidate`. O release continua condicionado aos gates técnicos, de segurança, runner, histórico, árvore e demais critérios registrados em `PUBLICATION-STATUS.md`.

A auditoria de licenciamento descrita neste documento será realizada posteriormente.
