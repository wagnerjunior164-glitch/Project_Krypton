# Teste Operacional do Atualizador do KryptonPlay

Data: 2026-09-11

## Objetivo

Documentar a estratégia oficial para validar o atualizador automático do KryptonPlay sem alterar a certificação já concluída das Parts 01–09.

## Princípio

O workflow unificado de certificação deve permanecer como está. As Parts 01–09 constituem a cadeia oficial de certificação e não devem passar a depender do funcionamento do atualizador para serem consideradas aprovadas.

O atualizador será validado separadamente, usando o produto real gerado pelo runner Windows `PC`.

## Relação com a certificação Parts 01–09

O fluxo oficial permanece:

`Part 01 → Part 02 → ... → Part 08 → Part 09 → PASS`

A geração do `KryptonPlay-Windows-Setup.exe` pelo runner faz parte do processo já certificado. Esse produto pode ser utilizado como a versão instalada inicial do teste operacional do atualizador.

O teste do atualizador não reabre, modifica ou acrescenta etapas às Parts 01–09.

## Estratégia Release A → Release B

O teste deve utilizar duas versões controladas:

- **Release A:** versão atualmente instalada no Windows, obtida a partir do produto gerado pelo runner `PC`.
- **Release B:** versão posterior, disponibilizada de forma controlada como GitHub Release e contendo o instalador `KryptonPlay-Windows-Setup.exe`.

A Release B deve possuir uma versão superior à Release A para que o serviço de atualização reconheça `update_available=true`.

A `main` pública não deve ser transformada em uma versão de teste apenas para exercitar o atualizador.

## Fluxo do teste

1. Gerar o produto Windows pelo runner `PC` através do processo normal de build.
2. Selecionar o instalador correspondente como Release A.
3. Instalar e iniciar a Release A no Windows.
4. Disponibilizar uma Release B controlada com versão superior.
5. Solicitar a verificação de atualização.
6. Confirmar que o serviço identifica a Release B como mais recente.
7. Confirmar a disponibilidade do asset `KryptonPlay-Windows-Setup.exe`.
8. Baixar o instalador da Release B.
9. Conferir o SHA-256 antes de aplicar a atualização.
10. Iniciar `KryptonPlay-Updater.exe`.
11. Confirmar o encerramento do aplicativo pai.
12. Confirmar a execução silenciosa do instalador.
13. Confirmar a instalação da Release B.
14. Confirmar o reinício do KryptonPlay.
15. Confirmar que a versão em execução corresponde à Release B.
16. Confirmar o consumo de `pending-update.json` e a notificação de atualização concluída quando aplicável.
17. Registrar o resultado e as evidências do teste.

## Critérios de aprovação

O teste será considerado **PASS** somente quando todos os pontos essenciais forem confirmados:

- versão B é reconhecida como superior à A;
- atualização é detectada;
- instalador correto é localizado;
- SHA-256 do instalador é validado;
- `KryptonPlay-Updater.exe` é executado;
- aplicativo é atualizado sem intervenção manual durante a instalação;
- KryptonPlay reinicia corretamente;
- versão B fica efetivamente instalada;
- mecanismo de conclusão da atualização funciona;
- não são introduzidos resíduos ou falhas relevantes no aplicativo.

Qualquer falha deve ser registrada como falha do teste operacional do atualizador, sem ser confundida automaticamente com falha da certificação Parts 01–09.

## Separação da Part 10

Este teste não constitui reativação da Part 10.

A Part 10 continua suspensa para reavaliação futura e permanece fora da cadeia oficial de certificação atual.

O teste aqui documentado é uma **validação operacional específica do atualizador já implementado**, independente da certificação suspensa da Part 10.

## Componentes envolvidos

O mecanismo atualmente implementado utiliza, entre outros componentes:

- `KryptonPlay/update_service.py` — consulta a GitHub Release, identifica atualização, baixa o instalador e verifica SHA-256;
- `KryptonPlay/updater.py` — executa a atualização silenciosa, aguardando o encerramento do processo pai e reiniciando o aplicativo;
- `KryptonPlay/admin_features.py` — integra configurações administrativas, verificação/aplicação e o marcador de conclusão da atualização.

## Regra para o futuro

O teste operacional do atualizador deve permanecer separado da cadeia Parts 01–09. Uma alteração futura no updater deve receber validação proporcional ao impacto. Somente quando uma alteração afetar diretamente componentes cobertos pelas certificações existentes deverá ser considerada a ampliação da validação correspondente.

## Estado

**ESTRATÉGIA DOCUMENTADA — TESTE OPERACIONAL SEPARADO DA CERTIFICAÇÃO PARTS 01–09.**

A execução prática do cenário Release A → Release B ainda deve ser realizada e registrada como evidência própria quando houver uma Release B controlada disponível.
