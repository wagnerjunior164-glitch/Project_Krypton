# MemoryProject

O **MemoryProject** é um sistema genérico de **organização, indexação, pesquisa e recuperação de conhecimento**, independente de projeto e de fonte.

Seu objetivo é permitir que conhecimento existente em diferentes fontes seja organizado e encontrado de forma estruturada, mantendo a rastreabilidade até sua origem.

> **A fonte original é a autoridade. O MemoryProject organiza, indexa, pesquisa e recupera o conhecimento proveniente dessa fonte.**

Registros, índices, metadados derivados e cache são representações auxiliares e não substituem a fonte original.

## Versão

`0.1.0` — em desenvolvimento.

## Objetivo da versão 0.1.0

A primeira versão estabelece uma base funcional para:

- representar projetos e fontes;
- acessar fontes GitHub;
- localizar e ler arquivos Markdown;
- identificar unidades de conhecimento;
- criar registros estruturados;
- preservar referências à origem;
- criar um índice derivado;
- realizar pesquisa textual;
- recuperar resultados rastreáveis.

## Arquitetura

```text
                         MEMORYPROJECT
                              │
                              ▼
                           PROJETO
                              │
                         ┌────┴────┐
                         ▼         ▼
                       FONTES   CONHECIMENTO
                         │         │
                         ▼         ▼
                    IMPORTAÇÃO  REGISTROS
                         │         │
                         └────┬────┘
                              ▼
                           ÍNDICE
                              │
                              ▼
                           PESQUISA
                              │
                              ▼
                         RECUPERAÇÃO
```

### Estrutura física

```text
MemoryProject/
├── app/
├── core/
├── adapters/
├── storage/
├── tests/
├── README.md
└── .gitignore
```

### Responsabilidades

- `app/` — entrada e coordenação das operações de alto nível.
- `core/` — regras de negócio do MemoryProject.
- `adapters/` — comunicação com fontes externas.
- `storage/` — artefatos derivados mantidos localmente.
- `tests/` — testes dos componentes e funcionalidades.

O `core` não deverá depender diretamente de uma fonte específica.

## Primeira fonte

A primeira fonte implementada é um repositório GitHub contendo arquivos Markdown. O GitHub é uma implementação de fonte, não uma dependência arquitetural exclusiva do MemoryProject.

Outras fontes poderão ser adicionadas futuramente por meio de adapters.

## Entidades fundamentais

- **Projeto** — contexto ao qual o conhecimento está relacionado.
- **Fonte** — origem onde o conhecimento existe originalmente.
- **Conhecimento** — unidade relevante de informação existente dentro de uma fonte.
- **Registro** — representação estruturada de uma unidade identificável de conhecimento.
- **Índice** — estrutura derivada utilizada para pesquisa.
- **Cache** — armazenamento auxiliar e não oficial de conteúdo obtido das fontes.

## Rastreabilidade

O resultado deverá permitir seguir a cadeia:

```text
Resultado
   ↓
Registro
   ↓
Fonte
   ↓
Arquivo
   ↓
Origem
```

Quando houver conflito entre a fonte original e qualquer representação derivada, **a fonte original terá prioridade**.

## Escopo da 0.1.0

### Incluído

- Projeto;
- Fonte;
- adapter GitHub;
- Markdown;
- Registros;
- Metadados básicos;
- Referência à origem;
- Índice simples;
- Pesquisa textual;
- Recuperação básica.

### Não incluído inicialmente

- busca semântica;
- embeddings;
- inteligência artificial;
- interface gráfica completa;
- API pública;
- serviço Windows;
- cloud;
- outras fontes além das implementações explicitamente suportadas.

Recursos futuros deverão ser avaliados individualmente e somente quando houver necessidade validada.

## Princípios de desenvolvimento

```text
Implementar
    ↓
Testar
    ↓
Validar
    ↓
Documentar
    ↓
Prosseguir
```

Alterações arquiteturais relevantes deverão seguir necessidade, proposta, documentação, aprovação e implementação.

## Documentação oficial

A documentação oficial e vigente está em:

`MemoryProject/docs/00 - Índice da Documentação do MemoryProject.md`

## Status

**Em desenvolvimento — versão `0.1.0`.**
