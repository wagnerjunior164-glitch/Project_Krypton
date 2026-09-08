# Lote de publicação — auditoria estática final pré-runner

Data: 2026-09-08
Branch: `public-candidate`

## Objetivo

Registrar as verificações que podem ser concluídas sem execução no runner Windows `PC`, deixando separadas as pendências que exigem validação real.

## Resultado

A árvore `public-candidate` permanece **BLOQUEADA PARA RELEASE FINAL**. A auditoria estática não substitui os testes finais diretamente sobre a árvore pública.

## Integridade da árvore

A árvore atual contém os componentes KryptonPlay, especificações de build/installer, testes E2E, documentação de publicação e os dois workflows temporários de validação pública.

SHAs relevantes conferidos:

- `KryptonPlay/increment24_hardening.py`: `19027f81d9c8558c76c2ffb3fe949484fa0187dd`;
- `KryptonPlay/requirements.txt`: `066763becc2f5474d0021ccf1625d628553ba5c2`;
- `KryptonPlay/installer/KryptonPlay-Windows.iss`: `bbf7e26cf3aceee3d6515082edb9d88c8d4dbda2`;
- `KryptonPlay/KryptonPlay.spec`: `2cdbb4f4ccaca5ee88cad8d87735d3fe91687bd4`;
- `KryptonPlay/KryptonPlay-Updater.spec`: `a0e7b00b6a75959df8ddf75f31c7b7556fd56a09`;
- `KryptonPlay/updater.py`: `15cc16f492edb1e8819160b5183cd8e6643b3da5`;
- `KryptonPlay/tests/e2e_web_test.py`: `23acfbf6158532d6e82ab0027c71d9cea9847796`;
- `KryptonPlay/tests/run_e2e_server.py`: `4fd842404c5026c1fe88fec4e05533c11b136ac4`.

## Dependências

`requirements.txt` está fixado em:

- `fastapi==0.141.1`
- `uvicorn[standard]==0.52.4`
- `zeroconf==0.151.3`

A instalação real dessas versões ainda precisa ser repetida no runner após as últimas alterações.

## Segurança

As últimas alterações implementaram três endurecimentos que ainda precisam de execução real:

- diagnóstico após setup exige administrador autenticado;
- `KRYPTONPLAY_SECURE_COOKIES` permite habilitar `Secure` de forma explícita;
- reset administrativo aceita `new_password`, invalida sessões e não retorna `temporary_password`.

A cobertura E2E correspondente está presente no workflow temporário público.

## Workflows temporários

Permanecem na árvore, deliberadamente:

- `.github/workflows/tmp-public-candidate-e2e.yml`
- `.github/workflows/tmp-public-candidate-full-validation.yml`

Eles devem ser removidos somente após a conclusão da auditoria, para não perder a capacidade de repetir a validação final.

## Histórico e separação público/privado

A comparação de refs confirma que `public-candidate` está 100 commits à frente de `main` e 0 atrás. A árvore pública é uma linha própria a partir da raiz pública e não recebe o histórico privado.

Branches temporárias de auditoria também permanecem preservadas até o encerramento.

## Pendências que exigem o PC

1. executar FULL diretamente sobre `public-candidate`;
2. executar E2E/security diretamente sobre `public-candidate`;
3. repetir a varredura independente depois das alterações finais;
4. confirmar build/installer após as alterações de segurança e dependências;
5. fazer a conferência final de árvore/histórico/branches/tags.

## Conclusão

A parte estática/documental que não depende do runner foi concluída e registrada. O bloqueio restante é operacional: os workflows finais estão enfileirados aguardando um runner elegível no repositório público.

**Decisão:** nenhuma release/merge para `main` até que as pendências acima sejam concluídas.
