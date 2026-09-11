# Lote de publicação — revisão de segurança

Data original: 2026-09-08

## Estado histórico e encerramento

Este documento registra a revisão de segurança aplicada ao candidato público durante a auditoria de 2026-09-08. A redação original dizia que a validação real no runner ainda estava pendente. **Essa pendência foi encerrada posteriormente pela certificação oficial do candidato público.**

As alterações descritas abaixo fazem parte do estado atualmente certificado das Parts 01–09.

### 1. Diagnóstico de configuração — HARDENED

`POST /api/setup/diagnostics` continua disponível durante a configuração inicial, quando ainda não existe uma conta autenticada. Depois que `setup_completed=true`, o middleware de `increment24_hardening.py` exige administrador autenticado.

### 2. Cookie de sessão — HARDENED

Foi adicionado o controle `KRYPTONPLAY_SECURE_COOKIES`; quando habilitado, o middleware adiciona `Secure` aos cookies emitidos. O modo HTTP local não é quebrado por uma mudança cega para `Secure`.

### 3. Reset administrativo de senha — HARDENED

O fluxo passou a receber `new_password`, armazenar somente o hash, invalidar sessões anteriores e não retornar `temporary_password`. O fluxo E2E foi ampliado para confirmar o reset e o login com a nova senha.

### 4. Dependências — PINNED

O manifesto atual fixa:

- `fastapi==0.141.1`;
- `uvicorn[standard]==0.52.4`;
- `zeroconf==0.151.3`.

A documentação anterior que descrevia essas dependências como não fixadas é histórica e não representa mais o estado do candidato.

## Validação posterior

As execuções `34284379831` e `34284379902`, registradas originalmente como aguardando o runner, foram superadas pelo workflow oficial `.github/workflows/public-candidate-final-validation.yml`. Esse workflow clona diretamente `wagnerjunior164-glitch/Project_Krypton`, valida a ref `public-candidate` e conclui as Parts 01–09.

**Estado atual: alterações de segurança incorporadas e cobertas pela certificação oficial Parts 01–09.**

## Conclusão

A revisão de segurança deste lote está **ENCERRADA** como etapa histórica da auditoria. Não deve mais ser tratada como bloqueio de release.

A próxima etapa é a consolidação pós-certificação: conferência final de árvore/histórico/branches/tags, alinhamento da documentação histórica, preservação das evidências e decisão final de publicação.
