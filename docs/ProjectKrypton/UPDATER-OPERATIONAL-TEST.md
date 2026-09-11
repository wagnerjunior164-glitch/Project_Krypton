# Teste Operacional do Atualizador do KryptonPlay

Data: 2026-09-11
Status: **ESTRATÉGIA DOCUMENTADA — EXECUÇÃO PRÁTICA PENDENTE DE RELEASE B**

## Objetivo

Documentar a estratégia oficial para validar o atualizador automático do KryptonPlay sem alterar a certificação já concluída das Parts 01–09.

## Princípio

O workflow unificado de certificação deve permanecer como está. As Parts 01–09 constituem a cadeia oficial de certificação e não devem passar a depender do funcionamento do atualizador para serem consideradas aprovadas.

O atualizador é validado separadamente, usando o produto real gerado pelo runner Windows `PC`.

## Relação com a certificação Parts 01–09

O fluxo oficial permanece:

`Part 01 → Part 02 → ... → Part 08 → Part 09 → PASS`

A geração do `KryptonPlay-Windows-Setup.exe` pelo runner faz parte do processo já certificado. Esse produto pode ser utilizado como a versão instalada inicial do teste operacional do atualizador.

O teste do atualizador não reabre, modifica ou acrescenta etapas às Parts 01–09.

## Estratégia Release A → Release B

O teste utiliza duas versões controladas:

- **Release A:** versão atualmente instalada no Windows, obtida a partir do produto gerado pela Part 09 no runner `PC`.
- **Release B:** versão posterior, disponibilizada como GitHub Release pública e contendo o instalador `KryptonPlay-Windows-Setup.exe`.

A Release B deve possuir versão superior à Release A para que o serviço reconheça `update_available=true`.

A `main` pública não deve ser transformada em uma versão de teste apenas para exercitar o atualizador.

## Automação existente

Foi criado no repositório privado o workflow:

`.github/workflows/updater-operational-validation.yml`

O workflow possui três entradas opcionais:

- `target_tag` — tag da Release B; quando vazia e `auto=true`, usa a Release pública `latest`;
- `source_run` — run Part 09 de origem; quando vazio e `auto=true`, localiza a evidência Part 09 mais recente no runner;
- `auto` — ativa a descoberta automática quando os campos anteriores estiverem vazios.

A automação executa, quando todas as pré-condições estão disponíveis:

1. localizar a evidência Part 09;
2. localizar os três binários persistidos;
3. calcular e registrar SHA-256;
4. resolver a Release B pública;
5. confirmar `KryptonPlay-Windows-Setup.exe` e digest SHA-256;
6. recusar sobrescrever uma instalação externa existente;
7. instalar a Release A silenciosamente;
8. iniciar A e habilitar atualização automática;
9. confirmar que B é detectada como mais nova;
10. reiniciar o launcher para exercitar o caminho automático;
11. aguardar `KryptonPlay-Updater.exe` e a instalação de B;
12. confirmar a versão final e `update_completed`;
13. desinstalar e preservar evidências.

O workflow **não cria nem altera GitHub Releases**. A Release B precisa existir previamente.

## Primeira execução automatizada

A primeira tentativa automatizada foi o run `34595843491`, job `103251274143`.

Resultado: **FAIL por pré-condição ausente, antes da instalação**.

O run confirmou:

- modo automático reconhecido;
- descoberta automática da evidência Part 09 do run `34558412881`;
- localização dos três binários;
- cálculo dos SHA-256.

A execução parou ao consultar a Release pública `latest`, porque o repositório `wagnerjunior164-glitch/Project_Krypton` ainda não possuía nenhuma GitHub Release.

Portanto, esse resultado **não é falha do runner, da Part 09 ou do mecanismo do updater**. A pré-condição ausente é uma Release B pública controlada.

## Fluxo do teste

1. Gerar ou selecionar o produto Windows validado pela Part 09.
2. Tratar esse produto como Release A.
3. Disponibilizar uma Release B controlada com versão superior.
4. Executar o workflow automatizado em modo `auto`.
5. Confirmar detecção de B.
6. Confirmar asset e SHA-256.
7. Confirmar execução do updater.
8. Confirmar instalação de B.
9. Confirmar reinício e versão B em execução.
10. Confirmar `update_completed`.
11. Confirmar ausência de resíduos relevantes.
12. Preservar o relatório e as evidências.

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

Uma falha de pré-condição, como ausência de Release B, deve ser classificada separadamente de uma falha funcional do updater.

## Separação da Part 10

Este teste não constitui reativação da Part 10.

A Part 10 de certificação pública continua suspensa para reavaliação futura e permanece fora da cadeia oficial de certificação atual.

O teste aqui documentado é uma **validação operacional específica do atualizador já implementado**, independente da certificação suspensa da Part 10.

## Componentes envolvidos

O mecanismo atualmente implementado utiliza, entre outros componentes:

- `KryptonPlay/update_service.py` — consulta a GitHub Release, identifica atualização, baixa o instalador e verifica SHA-256;
- `KryptonPlay/updater.py` — executa a atualização silenciosa, aguardando o encerramento do processo pai e reiniciando o aplicativo;
- `KryptonPlay/admin_features.py` — integra configurações administrativas, verificação/aplicação e o marcador de conclusão da atualização.

## Regra para o futuro

O teste operacional do atualizador deve permanecer separado da cadeia Parts 01–09. Uma alteração futura no updater deve receber validação proporcional ao impacto. Somente quando uma alteração afetar diretamente componentes cobertos pelas certificações existentes deverá ser considerada a ampliação da validação correspondente.

## Limitação

A validação automatizada testa a atualização automática disparada pelo launcher na inicialização. O horário programado de atualização é uma capacidade distinta e pode receber uma validação temporal específica posteriormente, caso seja necessário certificar também esse comportamento.
