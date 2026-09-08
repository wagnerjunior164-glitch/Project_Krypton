# Lote de publicação — revisão de segurança

Data: 2026-09-08

## Resultado

A revisão de segurança foi aplicada na `public-candidate` e aguarda somente a validação real no runner `PC` antes de ser considerada encerrada.

### 1. Diagnóstico de configuração — HARDENED

`POST /api/setup/diagnostics` continua disponível durante a configuração inicial, quando ainda não existe uma conta autenticada. Depois que `setup_completed=true`, o middleware de `increment24_hardening.py` exige administrador autenticado e retorna `401` para acesso não autenticado.

A resposta do diagnóstico continua limitada ao propósito de setup: estado do banco, disponibilidade de FFmpeg/FFprobe, existência/tipo/permissões dos caminhos fornecidos e diretório de dados.

### 2. Cookie de sessão — HARDENED

O comportamento HTTP local continua compatível por padrão. Foi adicionado o controle `KRYPTONPLAY_SECURE_COOKIES`; quando definido como `true`, `1`, `yes` ou `on`, o middleware adiciona `Secure` aos cookies emitidos.

Assim, o modo HTTP local não é quebrado por uma mudança cega para `Secure`, enquanto uma implantação HTTPS pode exigir explicitamente o atributo seguro. FastAPI/Starlette suporta `secure`, `httponly` e `samesite` no cookie de resposta. citeturn0search0

### 3. Reset administrativo de senha — HARDENED

O fluxo foi alterado no middleware para não devolver mais uma senha temporária gerada pelo servidor na resposta HTTP.

O administrador autenticado deve enviar `new_password` com 8–200 caracteres. O servidor grava somente o hash, invalida as sessões anteriores e responde com estado e ID, sem incluir `temporary_password`.

O workflow E2E foi ampliado para criar um usuário, executar o reset e confirmar login com a nova senha, além de verificar explicitamente que `temporary_password` não aparece na resposta.

### 4. Dependências — PINNED

O manifesto agora fixa:

- `fastapi==0.141.1`;
- `uvicorn[standard]==0.52.4`;
- `zeroconf==0.151.3`.

As versões foram escolhidas a partir das releases publicadas no PyPI em 2026 e serão validadas integralmente no runner antes da aprovação final. FastAPI 0.141.1 é a release mais recente indicada pelo PyPI consultado; Uvicorn 0.52.4 e zeroconf 0.151.3 também são releases atuais no período da auditoria. citeturn1search3turn1search1turn1search0

## Validação disparada

Após as alterações, a branch `public-candidate` recebeu o commit `fe068e4241658614bf884a0175daf38db45c07b7`, que disparou:

- run `34284379831` — E2E público com regressões de segurança;
- run `34284379902` — Full Validation diretamente sobre `public-candidate`.

Ambos estão atualmente **QUEUED**, aguardando o runner self-hosted `PC` aceitar os jobs. Os jobs foram roteados com `[self-hosted, windows, x64]`.

A validação não será considerada aprovada enquanto esses runs não concluírem com sucesso. O uso de runner self-hosted em repositório público permanece deliberadamente temporário e controlado; o GitHub recomenda self-hosted runners principalmente para repositórios privados devido ao risco de execução de código não confiável. citeturn0search1turn0search2

## Critério de encerramento

Depois que os runs `34284379831` e `34284379902` concluírem, ainda será necessário repetir a varredura independente da árvore final e realizar a conferência final de histórico, branches, tags e conteúdo privado antes da liberação de `main`.

Até essas etapas, `public-candidate` permanece bloqueada para release pública final.
