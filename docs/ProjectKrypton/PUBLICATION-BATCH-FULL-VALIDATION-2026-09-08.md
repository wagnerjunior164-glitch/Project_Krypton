# Lote de publicação — validação FULL no runner `PC`

Data: 2026-09-08

## Objetivo

Executar a validação integrada de nível `full` no runner Windows `PC`, usando o test-runner unificado existente, sem alterar `main` e sem criar um novo mecanismo permanente de validação.

## Execução

- Repositório de execução: `wagnerjunior164-glitch/ProjectKrypton` (privado);
- workflow temporário: `.github/workflows/tmp-final-full-validation-2026-09-08.yml`;
- branch: `tmp-final-full-validation-2026-09-08`;
- commit validado: `433bcdcc9624a0f21afc7967b377c5f9f3598f21`;
- run: `34276601584`;
- job: `102236534720`;
- parâmetros: `Scope=all`, `Level=full`, `Module=all`;
- runner: `PC`;
- conclusão: **SUCCESS**.

O workflow usa `runs-on: [self-hosted, windows, x64]`, portanto a execução foi encaminhada ao runner Windows x64 disponível com esses labels. O GitHub roteia jobs para runners que atendem cumulativamente aos labels especificados.

## Cobertura confirmada

A execução FULL concluiu com sucesso as etapas de documentação, MemoryProject, testes KryptonPlay, Web E2E, build Windows, PyInstaller, updater e instalador Windows, além da geração do relatório unificado.

Resultados observados no job:

- documentação: **72 Markdown — PASS**;
- MemoryProject: **15 passed**;
- KryptonPlay: **20 passed**;
- Web E2E: **PASS**;
- Windows build: **PASS**;
- PyInstaller: **PASS**;
- Windows Installer: **PASS**;
- relatório unificado: **CONCLUIDO**.

## Relação com a árvore pública candidata

Esta execução FULL foi feita no repositório privado, na branch temporária criada para validar o conjunto integrado de fontes e o test-runner. Ela **não é, isoladamente, uma prova de que o commit atual de `public-candidate` foi submetido ao FULL**.

A árvore pública candidata permanece validada pelos gates específicos já executados: export/integridade, FFmpeg fallback, smoke funcional, varredura independente, build/installer e E2E real diretamente contra `public-candidate`.

Antes da liberação final, a conferência deverá garantir que as alterações deliberadas do candidato público estejam presentes e documentadas, especialmente:

- `KryptonPlay/installer/KryptonPlay-Windows.iss` com `RunOnceId: "KryptonPlayTaskKill"` (SHA público atual `bbf7e26cf3aceee3d6515082edb9d88c8d4dbda2`);
- workflow temporário E2E público endurecido com `-NoProfile -ExecutionPolicy Bypass` e senha gerada em runtime;
- `updater.py` presente com SHA público confirmado `15cc16f492edb1e8819160b5183cd8e6643b3da5`;
- documentação de publicação coerente com os resultados efetivamente obtidos.

## Conclusão

O gate **FULL integrado do repositório privado foi aprovado** no runner `PC`. Isso confirma a saúde do pipeline completo de validação e build, mas não substitui a conferência final específica da árvore `public-candidate`.

Os workflows e branches temporários permanecem durante a auditoria e não devem ser removidos neste momento.
