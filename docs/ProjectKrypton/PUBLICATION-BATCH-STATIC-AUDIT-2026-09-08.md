# Lote de publicação — auditoria estática final pré-runner

Data original: 2026-09-08
Status da revisão: **HISTÓRICO — encerrado**

## Objetivo original

Registrar as verificações que podiam ser concluídas sem execução no runner Windows `PC`, separando as pendências que ainda exigiam validação real naquele momento.

## Estado atual

Este documento pertence à fase de auditoria de 2026-09-08. A redação original dizia que `public-candidate` estava bloqueada para release e que várias validações ainda precisavam ser executadas. **Essas pendências foram posteriormente encerradas pela certificação final do candidato público e pela publicação em `main`.**

Portanto, este arquivo deve ser lido como registro histórico e não como uma lista de bloqueios atuais.

## Integridade da árvore na época

A árvore `public-candidate` continha os componentes KryptonPlay, especificações de build/installer, testes E2E, documentação de publicação e os workflows temporários usados durante a auditoria.

SHAs relevantes conferidos naquele momento:

- `KryptonPlay/increment24_hardening.py`: `19027f81d9c8558c76c2ffb3fe949484fa0187dd`;
- `KryptonPlay/requirements.txt`: `066763becc2f5474d0021ccf1625d628553ba5c2`;
- `KryptonPlay/installer/KryptonPlay-Windows.iss`: `bbf7e26cf3aceee3d6515082edb9d88c8d4dbda2`;
- `KryptonPlay/KryptonPlay.spec`: `2cdbb4f4ccaca5ee88cad8d87735d3fe91687bd4`;
- `KryptonPlay/KryptonPlay-Updater.spec`: `a0e7b00b6a75959df8ddf75f31c7b7556fd56a09`;
- `KryptonPlay/updater.py`: `15cc16f492edb1e8819160b5183cd8e6643b3da5`;
- `KryptonPlay/tests/e2e_web_test.py`: `23acfbf6158532d6e82ab0027c71d9cea9847796`;
- `KryptonPlay/tests/run_e2e_server.py`: `4fd842404c5026c1fe88fec4e05533c11b136ac4`.

Esses SHAs identificam o estado auditado naquele lote e não devem ser usados como hashes atuais sem nova consulta à árvore.

## Dependências

Na fase inicial, `requirements.txt` ainda estava sem pins e a instalação das versões finais precisava ser repetida no runner. Posteriormente, o estado certificado passou a usar:

- `fastapi==0.141.1`;
- `uvicorn[standard]==0.52.4`;
- `zeroconf==0.151.3`.

Essa evolução foi incorporada à certificação final e é descrita na documentação consolidada de publicação.

## Segurança

As alterações de endurecimento descritas neste lote foram posteriormente executadas e cobertas pela certificação pública final:

- diagnóstico após setup exige administrador autenticado;
- `KRYPTONPLAY_SECURE_COOKIES` permite habilitar `Secure` de forma explícita;
- reset administrativo aceita `new_password`, invalida sessões e não retorna `temporary_password`.

A cobertura E2E correspondente passou na certificação oficial Parts 01–09.

## Workflows temporários

Os workflows temporários citados neste documento pertenciam à fase de auditoria e não devem ser interpretados como parte da arquitetura pública permanente. A certificação atual utiliza o workflow oficial definido no repositório privado e termina na Part 09.

## Histórico e separação público/privado

A árvore pública foi publicada com uma raiz Git própria. O histórico privado, seus branches e suas tags não foram transferidos para o repositório público.

As branches e workflows temporários da auditoria pertencem ao processo histórico e não constituem requisito permanente do produto público.

## Pendências que existiam em 2026-09-08

As pendências abaixo eram válidas naquele momento:

1. executar FULL diretamente sobre `public-candidate`;
2. executar E2E/security diretamente sobre `public-candidate`;
3. repetir a varredura independente depois das alterações finais;
4. confirmar build/installer após as alterações de segurança e dependências;
5. fazer a conferência final de árvore/histórico/branches/tags.

Posteriormente, essas atividades foram encerradas por etapas específicas de validação e pela certificação final do candidato público.

## Conclusão histórica

A auditoria estática cumpriu sua função como gate preliminar da publicação de 2026-09-08. O bloqueio operacional registrado naquele momento foi superado posteriormente.

Para o estado atual, consultar `docs/ProjectKrypton/PUBLICATION-STATUS.md`.

**Decisão histórica:** nenhuma release/merge para `main` era permitido até a conclusão dos gates finais. Essa decisão foi posteriormente superada pela certificação e publicação concluídas.
