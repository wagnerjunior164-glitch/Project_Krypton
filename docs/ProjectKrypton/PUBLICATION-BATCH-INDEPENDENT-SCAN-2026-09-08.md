# Lote de publicação — varredura independente da árvore candidata

Data: 2026-09-08

## Objetivo

Executar uma conferência independente da branch `public-candidate` antes da validação integrada, procurando segredos, credenciais, chaves, caminhos de ambiente privado, endereços LAN fixos e arquivos de credenciais.

## Método

A verificação foi executada no runner Windows `PC` por um workflow temporário mantido exclusivamente no repositório privado. O workflow fez clone limpo da branch pública e examinou todos os arquivos fora de `.git`.

O gate procurou, entre outros indicadores, chaves privadas, tokens GitHub/AWS, credenciais literais, arquivos `.env`/`.pem`/`.key`/`.pfx`/`.p12`, credenciais de teste previamente identificadas, caminhos de usuário e endereços IPv4 privados fixos.

## Primeira execução

A primeira execução funcional chegou ao clone da árvore pública e encontrou apenas duas classes de informação ambiental em documentação histórica:

- referência a um caminho de mídia específico do ambiente privado;
- referência explícita ao repositório privado.

Não foram encontrados tokens, chaves privadas, credenciais funcionais ou arquivos de segredo.

As referências ambientais desnecessárias foram removidas da documentação pública. A identificação do repositório privado também foi retirada das passagens que não precisam dela para explicar o processo de auditoria.

## Correção

A documentação `PUBLICATION-BATCH-STATIC-2026-09-08.md` foi atualizada para descrever o ambiente privado de forma genérica, sem reproduzir caminhos locais ou identificadores de infraestrutura privada.

O `update_service.py` já utiliza como padrão o repositório público `wagnerjunior164-glitch/Project_Krypton`, mantendo `KRYPTONPLAY_UPDATE_REPOSITORY` apenas como override configurável.

## Resultado

A primeira execução não representa uma falha de segurança do código: foi um achado de higiene de publicação na documentação. A etapa final deve ser repetida sobre a árvore pública após a sanitização e somente será considerada aprovada quando o runner registrar `VALIDACAO_INDEPENDENTE_PUBLIC_CANDIDATE_OK`.

## Gate de release

A release pública continua bloqueada até a confirmação desse gate, seguida da revisão de dependências/workflows, validação funcional integrada e `build/installer/full` no runner `PC`, e conferência final de árvore e histórico.

Os artefatos e testes temporários da auditoria não serão removidos nesta etapa.
