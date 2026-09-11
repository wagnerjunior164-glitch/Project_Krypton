# Plano de Simplificação Pós-Release do ProjectKrypton

Data original: 2026-09-08
Status: **PLANO FUTURO / ARQUITETURA EM EVOLUÇÃO**

## Objetivo

Depois da primeira publicação pública estável, transformar a infraestrutura criada durante a auditoria de release em uma operação permanente, previsível, modular e fácil de manter.

A regra principal permanece: **preservar os mecanismos que protegem a qualidade e remover ou arquivar o que existe apenas para uma auditoria histórica específica.**

A primeira publicação já foi concluída. Portanto, este documento não é mais um plano para desbloquear a release inicial; ele orienta a evolução pós-publicação.

## 1. O que permanece permanentemente

### Certificação pública

Manter a cadeia oficial de certificação Parts 01–09. Ela comprova o estado certificado do produto público e não deve ser alterada para incorporar o teste específico do updater.

### Desenvolvimento, build e diagnóstico

Manter uma arquitetura modular separada para desenvolvimento que possa executar:

- todos os módulos;
- um módulo individual;
- todas as Parts;
- uma Part específica;
- uma Part e todas as seguintes.

A execução deve preservar logs e evidências completas e classificar corretamente `PASS`, `FAIL`, `SKIPPED`, `NOT_APPLICABLE`, `PRECONDITION_FAILED` e `INCOMPLETE_EVIDENCE`.

### Teste operacional do updater

Manter o teste Release A → Release B separado da certificação Parts 01–09. Ele valida o comportamento operacional do atualizador sem transformar o updater em requisito automático de toda certificação.

### Testes

Manter, conforme aplicabilidade do módulo:

- compilação/sintaxe;
- testes unitários e funcionais;
- E2E;
- integração;
- FFmpeg/fallback quando aplicável;
- build Windows;
- PyInstaller;
- instalador;
- persistência;
- verificações essenciais de segurança;
- atualização operacional.

### Runner Windows `PC`

Manter o runner próprio para validações que dependem do ambiente Windows real, FFmpeg, PyInstaller, Inno Setup e demais componentes específicos do produto.

O runner não deve executar código arbitrário de forks ou workflows públicos inseguros.

## 2. O que deve ser removido ou arquivado

Os workflows e branches temporários usados exclusivamente na auditoria de 2026-09-08 devem ser tratados como histórico. Não devem ser recriados como pipelines permanentes apenas para repetir a primeira publicação.

Também devem ser arquivados ou eliminados, quando comprovadamente sem utilidade futura:

- scripts temporários de auditoria;
- artefatos duplicados;
- documentos operacionais redundantes da primeira publicação.

As evidências necessárias devem ser preservadas antes de qualquer limpeza.

## 3. Separar certificação, desenvolvimento e updater

### Certificação pública

Pergunta respondida:

> O estado público certificado atende à cadeia oficial Parts 01–09?

Fluxo:

`candidato público → Parts 01–09 → resultado`

### Desenvolvimento/build/diagnóstico

Pergunta respondida:

> Esta alteração ou módulo funciona, pode ser construído e pode ser diagnosticado com evidência suficiente?

Fluxo modular:

`módulo + modo → preparação → testes → build → installer → persistência → diagnóstico → relatório`

### Atualizador

Pergunta respondida:

> Uma instalação A consegue detectar, baixar, validar e instalar uma versão B mais nova?

Fluxo:

`Release A → Release B → detecção → SHA-256 → updater → reinício → versão B → update_completed`

## 4. Simplificação dos scripts

Os scripts devem ser reutilizáveis e possuir responsabilidades claras. A implementação universal deve descobrir módulos e capacidades em vez de manter uma lista fixa de módulos no workflow.

Quando um módulo declarar uma capacidade específica, a camada universal a executa. Quando a capacidade não for aplicável, o resultado deve ser `NOT_APPLICABLE`.

## 5. Simplificação do uso do runner

O runner `PC` deve ser reservado para tarefas que realmente precisam do ambiente Windows real.

Quando segurança, disponibilidade e arquitetura permitirem, testes genéricos podem usar runners GitHub-hosted. Validações que exigem o ambiente real do `PC` devem continuar explicitamente vinculadas a ele.

## 6. Destino da `public-candidate`

`public-candidate` continua sendo uma área de preparação para promoções controladas. Não é necessário tratá-la como uma branch de desenvolvimento permanente do produto público.

Fluxo normal:

```text
ProjectKrypton privado
        ↓
validação
        ↓
public-candidate
        ↓
validação final necessária
        ↓
Project_Krypton/main
```

Correções urgentes feitas diretamente em `main` público devem ser reproduzidas no privado após validação.

## 7. Simplificação documental

A documentação operacional principal deve apontar para uma referência consolidada de estado e para documentos específicos de arquitetura e operação.

Os documentos datados de 2026-09-08 devem permanecer preservados como histórico da primeira publicação, mas não devem ser interpretados como estado atual quando contiverem gates ou pendências já encerrados.

## 8. Regra para falhas

Depois da publicação, uma falha deve ser investigada nesta ordem:

1. o produto está errado?
2. o teste está errado?
3. o ambiente está errado?
4. somente então o pipeline deve ser alterado.

Evitar acumular workarounds no CI para fazer um teste vermelho parecer verde.

## 9. Runtime de referência

A arquitetura universal de desenvolvimento adota **Node 24.x LTS** como baseline quando Node for aplicável.

A versão de patch efetivamente utilizada deve ser registrada em cada execução. Não se deve fixar um patch antigo quando uma versão 24.x LTS mais recente estiver disponível e compatível.

## 10. Estado desejado

```text
alteração
  ↓
workflow de desenvolvimento
  ↓
testes + build + diagnóstico
  ↓
evidências preservadas
  ↓
validação proporcional
  ↓
public-candidate
  ↓
certificação Parts 01–09 quando necessária
  ↓
publicação
```

O updater permanece como validação operacional específica e separada.

## Relação com a primeira publicação

A primeira publicação pública **não está bloqueada**. Os gates FULL, E2E/security, build, installer e certificação final foram concluídos posteriormente ao estado registrado neste documento.

Este plano orienta a simplificação e evolução pós-release; não constitui requisito adicional para manter a publicação inicial válida.
