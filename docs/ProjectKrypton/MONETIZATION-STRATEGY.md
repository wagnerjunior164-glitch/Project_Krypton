# Estratégia Inicial de Monetização do KryptonPlay

Data: 2026-09-08
Status: planejamento pós-release

## Objetivo

Definir uma estratégia de geração de receita para o KryptonPlay sem comprometer a confiança, a privacidade e a proposta de controle do usuário sobre sua própria biblioteca de mídia.

Este documento é estratégico. Não representa uma decisão de preços, licença comercial ou modelo definitivo. Essas decisões devem ser tomadas depois que a versão pública estiver estável e houver evidência de uso real.

## Princípio central

O KryptonPlay não deve ser monetizado simplesmente por esconder funcionalidades básicas atrás de uma cobrança.

A estratégia recomendada é criar uma versão gratuita realmente útil e cobrar por valor adicional: recursos avançados, administração, servidor, automação, suporte e serviços profissionais.

## Modelo recomendado

```text
                         KRYPTONPLAY
                              │
             ┌────────────────┼────────────────┐
             ↓                ↓                ↓
        Community          Premium          Server Pro
         gratuito            💰                💰💰
             │                │                │
             └────────────────┼────────────────┘
                              ↓
                         Ecossistema
                              │
                       ┌──────┴──────┐
                       ↓             ↓
                    Suporte      Instalação
                       💰             💰
```

## 1. Community — gratuita

A versão Community deve permitir que um usuário comum descubra o produto e obtenha valor sem pagamento.

Possíveis recursos:

- biblioteca de mídia;
- scanner;
- player;
- reprodução local/rede;
- gerenciamento básico;
- atualização;
- distribuição Windows.

O objetivo é criar adoção, feedback e confiança.

## 2. Premium — recursos avançados

A versão Premium pode cobrar por recursos que economizem tempo ou ofereçam capacidades administrativas adicionais.

Possibilidades a validar com usuários:

- múltiplas bibliotecas avançadas;
- gerenciamento avançado de usuários;
- acesso remoto simplificado;
- sincronização;
- organização e automação avançadas;
- dashboards;
- backup/configuração;
- transcoding avançado;
- recursos administrativos adicionais;
- suporte prioritário.

O recurso só deve ser candidato a Premium quando houver valor perceptível para o usuário.

## 3. Server Pro — foco em servidor

Uma oportunidade potencialmente forte é posicionar o KryptonPlay como servidor pessoal de mídia:

```text
PC/NAS
  ↓
KryptonPlay Server
  ↓
TV / celular / navegador / outro PC
```

Recursos potenciais:

- múltiplos usuários;
- permissões;
- acesso remoto;
- administração centralizada;
- backup;
- atualizações;
- monitoramento;
- gerenciamento de biblioteca em servidor;
- suporte técnico.

A disposição de pagamento deve ser validada antes de transformar esse conjunto em produto comercial.

## 4. Serviços — receita desde cedo

Serviços podem gerar receita antes de existir uma grande base de usuários.

Possíveis serviços:

- instalação do KryptonPlay;
- configuração da biblioteca;
- configuração de FFmpeg;
- configuração de rede;
- criação de usuários e permissões;
- configuração de servidor/NAS;
- atualização;
- backup;
- treinamento;
- suporte técnico.

Esse modelo também permite aprender quais problemas reais os usuários estão dispostos a pagar para resolver.

## 5. O que evitar

Não é recomendado, especialmente no início:

- publicidade invasiva dentro do aplicativo;
- venda de dados do usuário;
- telemetria invasiva como requisito para uso;
- bloqueio artificial de funcionalidades essenciais;
- cobrança obrigatória apenas para continuar usando uma biblioteca local;
- modelo de assinatura sem valor recorrente claro.

A confiança e a privacidade podem ser diferenciais competitivos do produto.

## 6. Estratégia de entrada no mercado

A ordem sugerida é:

1. publicar uma versão Community estável;
2. observar downloads, instalações e uso;
3. coletar feedback;
4. identificar as funcionalidades pelas quais usuários realmente pediriam suporte ou pagariam;
5. oferecer serviços de instalação/configuração;
6. testar recursos Premium com um grupo pequeno;
7. somente depois definir preços e modelo comercial permanente.

## 7. Pergunta estratégica mais importante

Antes de definir preços, o projeto precisa responder:

> **Por que alguém escolheria KryptonPlay em vez das alternativas existentes?**

A monetização deve nascer dessa resposta, e não o contrário.

Possíveis diferenciais a investigar:

- simplicidade;
- controle local da biblioteca;
- privacidade;
- integração com Windows;
- qualidade do scanner;
- fallback/transcoding;
- facilidade de instalação;
- administração;
- experiência em rede local;
- custo total inferior a soluções comerciais.

Nenhum desses diferenciais deve ser considerado comprovado sem validação com usuários reais.

## 8. Métricas para a primeira fase

Depois do release, acompanhar pelo menos:

- número de downloads;
- instalações concluídas;
- usuários ativos, quando houver mecanismo de medição compatível com privacidade;
- problemas mais frequentes;
- pedidos de suporte;
- funcionalidades mais solicitadas;
- conversão de serviços pagos;
- disposição declarada a pagar;
- retenção de usuários.

Não criar telemetria invasiva apenas para obter essas métricas. Sempre avaliar primeiro alternativas que preservem a privacidade.

## 9. Hipótese inicial de negócio

A hipótese a testar é:

> **KryptonPlay Community gratuito + recursos Premium avançados + Server Pro + serviços de instalação/configuração e suporte.**

Essa hipótese é deliberadamente flexível. O produto deve orientar a estratégia comercial por meio de evidências de uso real.

## 10. Relação com o primeiro release

A monetização não deve atrasar nem substituir a preparação técnica atual.

O primeiro objetivo continua sendo uma publicação pública segura, reproduzível e confiável. Depois do release, a prioridade comercial deve ser validar o problema, o diferencial e a disposição de pagamento antes de investir pesadamente em uma camada comercial.

## Próxima fase

Após o release público, criar um pequeno plano de descoberta de mercado contendo:

1. posicionamento do KryptonPlay;
2. comparação com alternativas;
3. perfil dos primeiros usuários;
4. funcionalidades Premium candidatas;
5. proposta de Server Pro;
6. tabela experimental de preços;
7. política de licença;
8. canais de aquisição;
9. suporte;
10. métricas e critérios para decidir se a monetização deve avançar.
