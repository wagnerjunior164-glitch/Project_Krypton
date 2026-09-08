# MediaStation

Módulo do ProjectKrypton responsável pelo servidor de mídia baseado em Jellyfin.

## Estrutura administrativa

```text
MediaStation/
├── README.md
├── config/
├── docs/
└── scripts/
```

### Diretórios

- `docs/` — documentação oficial do MediaStation.
- `config/` — configurações que possam ser versionadas com segurança.
- `scripts/` — scripts versionados e oficialmente adotados pelo projeto.

## Biblioteca de mídia

A biblioteca de mídia permanece separada da administração e deve ser configurada no ambiente de execução. Caminhos locais, nomes de dispositivos e demais detalhes específicos da máquina não fazem parte da configuração pública do projeto.

## Dados internos do Jellyfin

Os dados internos do Jellyfin não fazem parte desta estrutura administrativa. Não devem ser versionados neste repositório credenciais, segredos, dados pessoais, banco de dados, cache, logs ou estado específico do computador.
