# Registro de Preparação Pública — Lote 004

## Estado

Preparação em andamento. Este registro não representa aprovação para publicação final.

## Correção do lote anterior

Os quatro arquivos de reprodução adicionados no lote 003 foram retirados do candidato público porque a cópia disponível não pôde ser comprovada integralmente contra os arquivos-fonte completos do repositório privado.

Arquivos retirados:

- `KryptonPlay/playback_ui.py`
- `KryptonPlay/playback_pipeline.py`
- `KryptonPlay/playback_info.py`
- `KryptonPlay/audio_fallback.py`

A retirada foi deliberada: código não comprovadamente fiel ao original não deve permanecer no candidato público apenas para completar a árvore.

## Auditoria do núcleo KryptonPlay

A auditoria prosseguiu sobre `KryptonPlay/app.py`, `KryptonPlay/launcher.py`, `KryptonPlay/scanner.py` e as dependências importadas pelo launcher.

Constatações atuais:

- `app.py` possui uma cadeia significativa de autenticação, banco SQLite, configuração, bibliotecas de mídia, sessões, preferências e administração; portanto sua importação deve ser feita integralmente e não por cópia truncada.
- `launcher.py` depende de vários módulos adicionais de runtime, incluindo atualização, descoberta local, recursos administrativos, endurecimento e UI.
- `scanner.py` é uma dependência pequena e diretamente verificável.
- `requirements.txt` do projeto privado contém atualmente `fastapi`, `uvicorn[standard]` e `zeroconf` sem versões fixadas. O candidato público não deve fixar versões arbitrariamente antes da validação de compatibilidade.

## Runner local — procedimento operacional documentado

O procedimento manual utilizado para abrir o GitHub Actions Runner neste PC é:

```powershell
cd C:\actions-runner
.\run.cmd
```

Esse procedimento é uma referência operacional local e **não deve ser copiado para workflows públicos nem para documentação que revele detalhes privados do ambiente**. A configuração do runner self-hosted continua excluída do candidato público.

## Regra de importação deste lote

Somente arquivos obtidos integralmente, comparados com a fonte privada e validados entram no candidato público. Arquivos cuja obtenção seja truncada, incompleta ou ambígua permanecem retidos.

## Próxima etapa

Concluir a unidade executável mínima do KryptonPlay a partir das fontes completas, incluindo suas dependências diretas e arquivos estáticos necessários, seguida de varredura de segurança, validação funcional, revisão de workflows e auditoria histórica antes da aprovação da publicação.
