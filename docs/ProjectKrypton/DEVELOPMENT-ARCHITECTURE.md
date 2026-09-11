# Arquitetura pública de desenvolvimento, build e diagnóstico

Data: 2026-09-11
Status: **ARQUITETURA DEFINIDA**

## Objetivo

Descrever, em nível público, a arquitetura que orienta desenvolvimento, testes, build, installer, persistência, atualização e diagnóstico sem transformar a certificação pública Parts 01–09 em um pipeline monolítico.

## Separação das responsabilidades

O projeto utiliza três linhas de validação relacionadas, porém independentes:

1. **Certificação pública — Parts 01–09:** comprova o estado certificado de um candidato público.
2. **Desenvolvimento/build/diagnóstico:** verifica alterações e módulos com execução modular e evidências detalhadas.
3. **Atualizador operacional:** verifica o cenário Release A → Release B.

A Part 10 da certificação pública continua suspensa e não é reativada por esta arquitetura.

## Execução modular

A arquitetura de desenvolvimento deve permitir selecionar:

- `module=all` ou um módulo individual;
- `mode=all` para todas as Parts;
- `mode=part` para uma Part específica;
- `mode=from` para uma Part e todas as seguintes.

A execução não deve depender de uma lista fixa de módulos. O mecanismo deve descobrir módulos compatíveis com as convenções do ProjectKrypton e determinar suas capacidades.

Exemplos conceituais:

```text
module=all, mode=all
module=KryptonPlay, mode=all
module=MediaStation, mode=part, part=02
module=MemoryProject, mode=from, part=04
```

Os nomes acima são exemplos de módulos atuais; módulos futuros devem poder ser incorporados sem exigir uma nova cópia do workflow universal.

## Matriz módulo × Part

Cada módulo pode possuir capacidades diferentes. Entre elas:

- documentação;
- unit/functional;
- integração;
- Web E2E;
- build;
- executável;
- installer;
- instalação/desinstalação;
- persistência;
- atualização;
- diagnóstico específico.

Quando uma capacidade não se aplicar a um módulo, o resultado correto é `NOT_APPLICABLE`, não `PASS` artificial.

Quando uma execução seletiva não possuir uma pré-condição necessária, o resultado deve ser classificado explicitamente, por exemplo, como `PRECONDITION_FAILED` ou `INCOMPLETE_EVIDENCE`.

## Camada universal e camada do módulo

### Camada universal

Responsável por:

- descoberta de módulos;
- seleção de módulo e Part;
- preparação do ambiente;
- descoberta de runtimes;
- execução e captura de comandos;
- logs e métricas;
- classificação de resultados;
- hashes;
- preservação de evidências;
- relatórios globais, por módulo e por Part.

### Camada específica do módulo

Responsável por:

- testes próprios;
- comandos de build;
- artefatos específicos;
- installer quando aplicável;
- estratégia de instalação/desinstalação;
- persistência específica;
- atualização;
- diagnósticos próprios.

Um módulo pode declarar essas capacidades por um manifesto, quando isso for útil, sem obrigar todos os módulos a implementar todas as Parts.

## Runtime

Quando Node.js for aplicável, a baseline da arquitetura é **Node 24.x LTS**.

A versão de patch efetivamente usada deve ser registrada durante a execução. O objetivo é acompanhar a linha LTS suportada sem depender de um patch antigo fixado artificialmente.

O runtime de um módulo continua sendo determinado pela própria capacidade do módulo; Node 24.x não substitui Python ou outras runtimes necessárias ao produto.

## Evidências e diagnóstico

Uma execução de desenvolvimento deve preservar evidências suficientes para reproduzir e investigar um resultado. O relatório deve registrar, conforme aplicável:

- identificação da execução e commit;
- módulo e Part;
- sistema operacional e runtimes;
- início, fim e duração;
- comando executado;
- exit code;
- stdout/stderr relevantes;
- resultado classificado;
- versões e hashes;
- artefatos de build e installer;
- estado de instalação/desinstalação;
- estado de persistência;
- diagnóstico da falha, quando houver.

A infraestrutura física do runner privado e seus caminhos locais não fazem parte da interface pública desta documentação.

## Relação com a certificação pública

A existência do workflow de desenvolvimento não substitui a certificação pública.

Quando uma alteração for candidata à publicação, ela deve seguir o fluxo de promoção controlada:

```text
ProjectKrypton privado
        ↓
workflow de desenvolvimento
        ↓
public-candidate
        ↓
validação final proporcional ao impacto
        ↓
Project_Krypton/main
```

Uma mudança pequena não exige automaticamente a repetição integral de Parts 01–09. Uma mudança que afete diretamente componentes críticos ou o escopo certificado pode exigir ampliação da validação.

## Relação com o updater

O updater é validado separadamente no cenário:

```text
Release A
   ↓
detecção de Release B
   ↓
SHA-256
   ↓
KryptonPlay-Updater
   ↓
instalação B
   ↓
reinício
   ↓
update_completed
```

A ausência de uma Release B pública é uma pré-condição do teste do updater, não uma falha das Parts 01–09.

## Princípio de evolução

A arquitetura deve permitir adicionar módulos e capacidades sem multiplicar workflows equivalentes. O objetivo é ter uma camada universal de execução e diagnóstico e manter no módulo apenas aquilo que é realmente específico dele.
