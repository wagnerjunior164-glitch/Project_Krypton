# Estratégia de Licenciamento do KryptonPlay

Data: 2026-09-08  
Status: planejamento — não é a licença jurídica definitiva do projeto

## Objetivo

Definir uma direção de licenciamento para o KryptonPlay que seja compatível com:

- publicação pública do projeto;
- preservação das liberdades do software Community;
- possibilidade de receita com Premium, Server Pro e serviços;
- proteção da confiança dos usuários;
- eventual contribuição de terceiros;
- possibilidade de licenciamento comercial futuro, se juridicamente possível.

Este documento é uma decisão de produto/engenharia em preparação. **Não substitui revisão jurídica.** Antes do release público, a licença definitiva deve ser escolhida somente depois da auditoria de autoria, copyright e licenças de terceiros.

## 1. Recomendação inicial

A hipótese recomendada para estudo é:

> **KryptonPlay Community sob GNU Affero General Public License v3.0 (AGPL-3.0), com possibilidade de uma licença comercial separada para usos que não possam ou não queiram cumprir a AGPL, desde que o titular dos direitos autorais tenha autoridade para concedê-la.**

A AGPL-3.0 é uma licença copyleft aprovada pela Open Source Initiative e foi desenhada especialmente para software que interage com usuários por rede. Ela exige, em determinadas situações, disponibilização do código-fonte correspondente de versões modificadas oferecidas por rede. citeturn0search2turn0search3

Essa escolha é uma **hipótese estratégica**, não uma decisão jurídica final.

## 2. Por que AGPL pode fazer sentido para o KryptonPlay

O KryptonPlay possui características que tornam a questão de software servido por rede relevante: além do aplicativo Windows, há componentes de servidor, autenticação, biblioteca e acesso via navegador.

A AGPL foi criada justamente para evitar que uma versão modificada de um software coberto seja executada em um servidor acessível pela rede sem que as condições de disponibilização do código aplicáveis sejam respeitadas. citeturn0search2

Isso pode ajudar a preservar o princípio:

```text
Código Community
      ↓
uso / modificação / distribuição
      ↓
liberdade para a comunidade
      ↓
melhorias retornam ao ecossistema quando as condições da licença exigirem
```

Ao mesmo tempo, a AGPL permite cobrar por cópias, suporte e garantia; o fato de o software ser livre não significa que ele precise ser distribuído gratuitamente. citeturn0search2

## 3. O que a AGPL não faz

A AGPL **não** impede:

- uso gratuito;
- criação de forks;
- modificação do código;
- distribuição por terceiros dentro das condições da licença;
- cobrança por distribuição permitida;
- cobrança por suporte e serviços.

Portanto, a licença não deve ser tratada como mecanismo para impedir concorrência.

O valor comercial precisa vir de algo que possa ser oferecido legitimamente além dos direitos básicos da Community, por exemplo:

- suporte profissional;
- instalação e configuração;
- Server Pro, se sua implementação e licenciamento forem estruturados de modo compatível;
- recursos adicionais cujo código/licença sejam juridicamente separados e sustentáveis;
- builds e serviços oficiais;
- SLA e suporte empresarial;
- documentação e implantação profissional.

## 4. Modelo comercial possível

Uma arquitetura a estudar seria:

```text
                         KRYPTONPLAY
                              │
                ┌─────────────┴─────────────┐
                ↓                           ↓
        Community / AGPL-3.0          Oferta Comercial
                │                           │
        código aberto                  Premium / Pro
        uso e modificação              suporte / serviços
                │                           │
                └─────────────┬─────────────┘
                              ↓
                         Ecossistema
```

A parte comercial não pode simplesmente pegar código AGPL e retirar os direitos concedidos pela AGPL. A arquitetura jurídica e técnica precisa separar claramente o que permanece coberto pela licença Community e o que é desenvolvido/licenciado de forma independente.

## 5. Licenciamento duplo

Uma possibilidade futura é o **dual licensing**: o mesmo código controlado pelo titular dos direitos pode ser oferecido sob AGPL e também sob uma licença comercial diferente para determinados clientes ou usos.

Esse modelo existe no mercado de software, mas aumenta a complexidade e exige controle claro sobre os direitos autorais e sobre as contribuições de terceiros. Material de referência da FSFE descreve dual licensing como distribuição sob dois conjuntos de condições potencialmente incompatíveis e destaca tanto a flexibilidade quanto a possibilidade de confusão para clientes. citeturn0search25

### Condição crítica

Só é possível conceder uma segunda licença para código quando o projeto possui os direitos necessários para fazê-lo.

Se terceiros contribuírem com código sem uma concessão de direitos adequada, poderá deixar de ser possível relicenciar aquele código livremente.

Por isso, **a política de contribuição precisa ser definida antes de aceitar contribuições externas significativas.**

## 6. Alternativas consideradas

### MIT

Vantagem: extremamente simples e permissiva.  
Problema estratégico: terceiros podem incorporar o código em produtos proprietários sem obrigação geral de compartilhar modificações.

### Apache-2.0

Vantagem: permissiva, conhecida e com tratamento explícito de patentes.  
Problema estratégico: também permite derivados proprietários, portanto oferece menos proteção copyleft à comunidade.

### GPL-3.0

Vantagem: copyleft forte para distribuição de software.  
Problema estratégico: o requisito específico de interação por rede que motivou a AGPL não é o foco da GPL.

### AGPL-3.0

Vantagem: copyleft forte e adequado a software com interação por rede.  
Problema: maior complexidade de compliance para empresas e derivados.

A OSI mantém uma lista oficial de licenças aprovadas e seus identificadores SPDX; AGPL-3.0 corresponde ao identificador SPDX `AGPL-3.0`. citeturn0search0turn0search3

## 7. Recomendação para o KryptonPlay neste momento

Não adicionar ainda uma licença definitiva apenas para cumprir formalidade.

Antes disso, executar esta auditoria:

1. identificar todos os autores e titulares dos direitos do código próprio;
2. verificar se existe código recebido de terceiros;
3. procurar cabeçalhos de copyright e avisos de licença;
4. mapear todas as dependências Python e demais componentes distribuídos;
5. registrar as licenças das dependências;
6. verificar compatibilidade das dependências com AGPL-3.0;
7. decidir como contribuições externas serão aceitas;
8. definir política de copyright e atribuição;
9. decidir se haverá dual licensing;
10. somente então criar `LICENSE` definitivo e avisos correspondentes.

## 8. Política de contribuições

Antes de abrir contribuições públicas, o projeto deve escolher uma política formal.

Alternativas a avaliar:

- contribuição sob os termos da licença do projeto, mantendo o copyright do autor;
- DCO para assinatura de origem das contribuições;
- CLA, caso seja necessária uma concessão adicional de direitos para relicenciamento/comercialização.

A escolha deve ser feita de acordo com a estratégia de copyright e com revisão jurídica.

## 9. Dependências e componentes de terceiros

A licença do KryptonPlay não substitui as licenças dos componentes de terceiros.

O release deve manter um inventário mínimo contendo:

| Componente | Tipo | Versão | Licença | Uso no produto | Ação |
|---|---|---|---|---|---|
| FastAPI | dependência | 0.141.1 | a auditar | servidor/API | confirmar licença |
| Uvicorn | dependência | 0.52.4 | a auditar | servidor ASGI | confirmar licença |
| zeroconf | dependência | 0.151.3 | a auditar | descoberta de rede | confirmar licença |
| FFmpeg | componente externo | conforme distribuição | a auditar | mídia/transcoding | confirmar termos da distribuição |
| PyInstaller | ferramenta/build | 6.22.2 | a auditar | empacotamento | registrar no inventário |
| Inno Setup | ferramenta/build | 6.7.3 | a auditar | instalador | registrar no inventário |

As versões acima refletem o estado atualmente documentado do candidato; o inventário jurídico ainda precisa ser concluído.

## 10. O que deve aparecer no release

Quando a licença definitiva for aprovada, o repositório público deverá ter, no mínimo:

```text
LICENSE
README.md
THIRD-PARTY-NOTICES.md
CONTRIBUTING.md
```

Quando aplicável, arquivos-fonte relevantes também devem possuir cabeçalhos SPDX/copyright consistentes com a política adotada.

## 11. Relação com a monetização

A estratégia de monetização já documentada prevê Community gratuita, Premium, Server Pro e serviços de instalação/configuração e suporte.

A política de licença deve proteger a Community sem criar uma promessa comercial que a própria licença não permita sustentar.

A pergunta correta não é:

> "Como usar a licença para impedir que alguém use o KryptonPlay de graça?"

A pergunta é:

> "Como oferecer liberdade real na Community e, ao mesmo tempo, criar valor comercial legítimo em torno do produto?"

Essa abordagem é mais compatível com a proposta de confiança e privacidade definida para o projeto.

## 12. Gate de release

A licença pública definitiva deve ser um item explícito do checklist final de release.

Antes de publicar `main`/tag de release:

- [ ] autoria e copyright auditados;
- [ ] licença de cada componente de terceiros mapeada;
- [ ] compatibilidade das dependências revisada;
- [ ] estratégia Community/Commercial decidida;
- [ ] política de contribuição decidida;
- [ ] `LICENSE` definitivo criado;
- [ ] `THIRD-PARTY-NOTICES.md` criado/atualizado;
- [ ] documentação de contribuição atualizada;
- [ ] avisos de copyright/SPDX revisados;
- [ ] revisão jurídica realizada quando necessária;
- [ ] licença publicada junto ao release.

## 13. Decisão provisória

**Estado atual: AGPL-3.0 é a recomendação técnica/estratégica para investigação, mas ainda NÃO é a licença definitiva do KryptonPlay.**

A decisão final fica bloqueada até a auditoria de autoria e terceiros.

Isso é deliberado: é preferível atrasar a escolha da licença do que publicar o projeto sob uma licença incompatível com direitos de terceiros ou com o futuro modelo comercial.

## Fontes de referência

- Open Source Initiative — AGPL-3.0: https://opensource.org/license/agpl-3-0
- Open Source Initiative — lista de licenças aprovadas: https://opensource.org/licenses
- GNU / Free Software Foundation — documentação sobre GPL/AGPL

## Relação com o release atual

Este documento é planejamento e não desbloqueia `public-candidate`. O release continua condicionado às validações técnicas, segurança, runner público, auditoria final de árvore/histórico e demais gates já registrados em `PUBLICATION-STATUS.md`.
