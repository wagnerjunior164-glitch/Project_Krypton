# Registro de Preparação Pública — Lote 004

## Estado histórico

Este registro documenta uma decisão da fase de preparação inicial do candidato público. Ele não representa o estado atual de certificação.

## Correção do lote anterior

Os quatro arquivos de reprodução adicionados no lote 003 foram retirados do candidato público porque a cópia disponível não pôde ser comprovada integralmente contra os arquivos-fonte completos do repositório privado.

Arquivos retirados:

- `KryptonPlay/playback_ui.py`
- `KryptonPlay/playback_pipeline.py`
- `KryptonPlay/playback_info.py`
- `KryptonPlay/audio_fallback.py`

A retirada foi deliberada: código não comprovadamente fiel ao original não deveria permanecer no candidato público apenas para completar a árvore.

## Auditoria do núcleo KryptonPlay

A auditoria prosseguiu sobre `KryptonPlay/app.py`, `KryptonPlay/launcher.py`, `KryptonPlay/scanner.py` e dependências importadas pelo launcher.

## Runner local

O procedimento manual do runner Windows `PC` foi registrado na documentação histórica para rastreabilidade operacional. Esse detalhe continua sendo privado e não pertence à configuração pública.

## Atualização do estado atual

As decisões deste lote foram posteriormente incorporadas à cadeia de preparação e validação do candidato. A certificação oficial atual é realizada pelo workflow `.github/workflows/public-candidate-final-validation.yml`, que valida diretamente `public-candidate` e conclui as Parts 01–09.

Portanto, a seção de “próxima etapa” do registro original — concluir a unidade executável mínima e depois iniciar as validações — deve ser lida como **etapa já superada**.

## Regra permanente

Somente arquivos obtidos integralmente, comparados com a fonte privada e validados devem entrar no candidato público. Essa regra continua válida para qualquer manutenção futura.

## Referência atual

Para o estado real da publicação, consultar `docs/ProjectKrypton/PUBLICATION-STATUS.md`. Este registro permanece como evidência histórica da decisão tomada no Lote 004.
