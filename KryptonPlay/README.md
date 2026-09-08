# KryptonPlay

Módulo do ProjectKrypton destinado ao desenvolvimento de um servidor de mídia próprio, independente do MediaStation e do Jellyfin.

## Estado atual

O KryptonPlay 0.1 está concluído, validado e encerrado. O ciclo de desenvolvimento foi encerrado no Incremento 20.

O núcleo do servidor utiliza Python, FastAPI, Uvicorn, SQLite e uma interface Web como cliente inicial. O fluxo principal foi validado em diferentes ambientes compatíveis.

O empacotamento e a distribuição para Windows possuem documentação própria, incluindo executável, instalador, Releases e estratégia de atualização. Os dados persistentes permanecem separados do programa.

O desenvolvimento pós-0.1 concluiu o **Incremento 21 — Diagnóstico de Reprodução**. O **Incremento 22 — Fallback de Áudio** foi concluído e aprovado com implementação do fallback para codecs incompatíveis, preservando o vídeo em cópia direta. A validação física da reprodução do fallback foi formalmente transferida para o Incremento 23.

O **DOC-020 — Classificação e Organização de Mídias** registra uma diretriz de planejamento para a evolução da biblioteca e não representa um novo incremento funcional.

A documentação oficial do módulo é mantida em `KryptonPlay/docs/`.

## Documentação

A porta de entrada oficial é:

`KryptonPlay/docs/00 - Índice da Documentação do KryptonPlay.md`

Os documentos numerados registram operação, planejamento, escopo, usuários, histórico de implementação, evolução do player, empacotamento/atualização e evolução pós-0.1.

## Estrutura

```text
KryptonPlay/
├── README.md
├── app.py
├── launcher.py
├── audio_fallback.py
├── playback_ui.py
├── KryptonPlay.spec
├── config/
├── docs/
└── scripts/
```

### Diretórios

- `docs/` — documentação oficial do KryptonPlay.
- `config/` — configurações que possam ser versionadas com segurança.
- `scripts/` — scripts versionados e oficialmente adotados.
- `data/` — dados persistentes locais gerados em execução; não deve ser substituído durante atualizações.

## Distribuição Windows

O KryptonPlay possui executável portátil e instalador Windows documentados na documentação específica do módulo. As versões oficiais são associadas a GitHub Releases e tags Git no formato SemVer.

A atualização deve preservar os dados persistentes e a biblioteca de mídia externa.

## Relação com o MediaStation

O KryptonPlay é um módulo independente. O MediaStation continua sendo uma solução baseada em Jellyfin durante a evolução do KryptonPlay e enquanto a substituição gradual ainda não estiver completa.

Nenhuma alteração no MediaStation deverá ser realizada apenas em razão do KryptonPlay.
