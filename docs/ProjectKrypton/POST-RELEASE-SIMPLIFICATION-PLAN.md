# Plano de Simplificação Pós-Release do ProjectKrypton

Data: 2026-09-08

## Objetivo

Depois da primeira publicação pública estável, transformar a infraestrutura criada durante a auditoria de release em um CI/CD permanente, menor, previsível e fácil de manter.

A regra principal é: **preservar os mecanismos que protegem a qualidade e remover tudo que existe apenas para esta primeira publicação.**

## 1. O que permanece permanentemente

### CI oficial

Manter um fluxo oficial de validação com níveis progressivos:

`quick → functional → build → installer → full`

O workflow unificado existente deve ser a base. A nomenclatura e os níveis podem ser simplificados durante a limpeza, mas não devem existir vários pipelines permanentes fazendo a mesma coisa.

### Testes

Manter:

- compilação/sintaxe;
- testes unitários e funcionais;
- E2E;
- validação de FFmpeg/fallback;
- build Windows;
- PyInstaller;
- instalador;
- verificações essenciais de segurança.

### Runner Windows `PC`

Manter o runner próprio para as validações que dependem do ambiente Windows real, FFmpeg, PyInstaller, Inno Setup e demais componentes específicos do produto.

A configuração permanente deve evitar que código arbitrário de forks ou workflows públicos inseguros consiga executar no runner.

## 2. O que deve ser removido depois do release

Somente após todos os gates finais e a publicação confirmada, remover:

- `tmp-public-candidate-e2e.yml`;
- `tmp-public-candidate-full-validation.yml`;
- workflows temporários equivalentes criados para a auditoria;
- branches temporárias de auditoria;
- scripts de diagnóstico que não tenham utilidade permanente;
- artefatos/documentos duplicados ou exclusivamente operacionais da primeira publicação.

**Nenhuma limpeza temporária deve ocorrer antes da aprovação final.**

## 3. Separar CI de auditoria de release

### CI permanente

Pergunta respondida:

> O código novo continua funcionando?

Fluxo esperado:

`push/PR → compile → testes → E2E → resultado`

Build/installer pode ser executado nos níveis apropriados.

### Auditoria de release

Pergunta respondida:

> Esta versão específica pode ser publicada?

Fluxo esperado:

`release candidate → security scan → dependency review → full validation → build → installer → revisão final de árvore/histórico → tag → publicação`

A auditoria de release não precisa ser executada integralmente a cada commit.

## 4. Simplificação dos scripts

Objetivo aproximado para `.github/scripts/`:

```text
.github/
├── workflows/
│   ├── validation.yml
│   ├── build.yml
│   └── release.yml
└── scripts/
    ├── prepare-e2e.ps1
    ├── test-runner.ps1
    └── build-windows.ps1
```

Cada script deve ter uma responsabilidade clara. Evitar duplicação e scripts criados somente para contornar falhas históricas do primeiro release.

## 5. Simplificação do uso do runner

O runner `PC` deve ser reservado para tarefas que realmente precisam dele.

Quando segurança, disponibilidade e arquitetura permitirem, testes genéricos podem usar runners GitHub-hosted e somente Windows/E2E/build específicos devem depender do `PC`.

Não usar `windows-latest` como substituto de uma validação que explicitamente exige o ambiente real do `PC`.

## 6. Destino da `public-candidate`

`public-candidate` deve ser tratada como área de preparação, não como branch permanente obrigatória.

Após o release, a operação normal deve voltar para:

```text
feature branch → PR → main → release/tag
```

Para releases futuros, branches de release ou tags RC podem ser criadas temporariamente quando necessário e removidas após o ciclo.

## 7. Simplificação documental

Os documentos detalhados da primeira auditoria devem ser preservados como histórico, mas a documentação operacional principal deve ser reduzida para algo próximo de:

```text
docs/
├── RELEASE.md
├── SECURITY.md
└── DEVELOPMENT.md
```

Os relatórios específicos da primeira publicação podem ser arquivados, por exemplo:

```text
docs/archive/release-2026-09-08.md
```

Não apagar evidências de auditoria; apenas impedir que o histórico operacional polua a documentação cotidiana.

## 8. Regra para falhas do CI

Depois do release, uma falha deve ser investigada nesta ordem:

1. o produto está errado?
2. o teste está errado?
3. o ambiente está errado?
4. somente então o pipeline deve ser alterado.

Evitar acumular workarounds no CI para fazer um teste vermelho parecer verde.

## 9. Estado desejado

O fluxo operacional final deve ser simples:

```text
commit
  ↓
CI
  ↓
passou
  ↓
merge
  ↓
release
  ↓
build + security + validation
  ↓
tag vX.Y.Z
  ↓
publicação
```

O objetivo é que a complexidade excepcional desta primeira publicação não vire dívida operacional permanente.

## 10. Critério de encerramento da limpeza

A simplificação pós-release estará concluída quando:

- workflows temporários tiverem sido removidos;
- branches temporárias tiverem sido removidas;
- CI oficial estiver consolidado;
- scripts duplicados tiverem sido eliminados;
- documentação operacional estiver enxuta;
- histórico da primeira auditoria estiver preservado;
- runner `PC` estiver protegido e reservado às tarefas apropriadas;
- um novo release puder ser executado sem repetir a infraestrutura especial criada para 2026-09-08.

## Relação com o release atual

Este documento é um **plano futuro**. O release público atual continua bloqueado até que os critérios registrados em `PUBLICATION-STATUS.md` sejam satisfeitos. Em particular, o FULL e o E2E/security finais precisam ser executados diretamente sobre `public-candidate` no ambiente elegível.
