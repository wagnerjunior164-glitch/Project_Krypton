# Registro de Preparação Pública — Lote 003

## Estado

Preparação em andamento. Este registro não representa aprovação para publicação final.

## Escopo do lote

Foi feita inspeção individual do núcleo de reprodução do KryptonPlay e foram adicionados ao candidato público:

- `KryptonPlay/playback_ui.py`
- `KryptonPlay/playback_pipeline.py`
- `KryptonPlay/playback_info.py`
- `KryptonPlay/audio_fallback.py`

Os componentes trabalham com caminhos fornecidos pela biblioteca e procuram FFmpeg/ffprobe por configuração do ambiente, sem incluir credenciais ou identificadores pessoais no código.

## Itens deliberadamente retidos

`KryptonPlay/app.py` e `KryptonPlay/launcher.py` foram inspecionados, mas não foram publicados neste lote. Eles concentram inicialização, autenticação, banco de dados, configuração, UI, descoberta de rede, atualização e integração de módulos.

Também continuam retidos workflows, scripts operacionais, configuração de runner, arquivos de staging e outros componentes com dependências de ambiente.

## Validação de segurança

A inclusão continua sendo tratada como candidata, não como aprovação. A árvore pública deve passar por uma varredura final completa antes da publicação.

Buscas direcionadas dos indicadores de risco já identificados anteriormente não encontraram ocorrências na árvore pública até esta etapa.

## Próxima ação

Montar a unidade executável mínima do KryptonPlay, auditando primeiro as dependências diretas de `app.py`, os arquivos estáticos necessários e os testes associados. A publicação final permanece bloqueada até a conclusão da auditoria integral, validação funcional e revisão dos workflows.
