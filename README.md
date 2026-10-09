# Movies_Projects

Workspace local da série **Andre viajando no tempo**. Filme ativo: **The Table Between Centuries**.

**[COMECE AQUI — materiais, fontes editáveis e retomada por agentes](START_HERE.md).**

O workflow repetível está em [docs/REPEATABLE_WORKFLOW.md](docs/REPEATABLE_WORKFLOW.md).
O registro da série está em [series/andre-time-travel/series.json](series/andre-time-travel/series.json).

## Start here

- [`AGENTS.md`](AGENTS.md): project boundaries and agent startup instructions.
- [`workspace.json`](workspace.json): film registry and expected layout.
- [`projects/andre-time-travel/docs/production-plan.md`](projects/andre-time-travel/docs/production-plan.md): canonical production plan.
- [`projects/andre-time-travel/01_script/script-en.md`](projects/andre-time-travel/01_script/script-en.md): sourced fictional English draft.
- [`projects/andre-time-travel/tasks/board.json`](projects/andre-time-travel/tasks/board.json): live production tasks.
- [`projects/andre-time-travel/memory/STATE.md`](projects/andre-time-travel/memory/STATE.md): resume point.

## Drop your materials here

- `inbox/andre-reference-photos/` — front, both three-quarter views, both profiles, seated waist-up.
- `inbox/andre-voice/` — approved voice-clone test exports; no keys/tokens.
- `inbox/failed-clips/` — the earlier broken-face take and a note with its exact generation ID.

Inbox files are not automatically uploaded, registered, or approved. Original media stays unchanged.

## Safe local commands

```bash
.venv/bin/python scripts/manage.py status
.venv/bin/python scripts/manage.py validate
.venv/bin/python -m unittest discover -s tests -v
```

As ferramentas de gestão e inventário usam apenas a biblioteca padrão do Python. Status, validação, inventário e criação de rascunho são locais e não chamam serviços. O gerador de PDFs/cartões usa Pillow, ReportLab, Poppler e fontes locais; veja as dependências no workflow. Validação administrativa não significa aceite criativo ou filme concluído.

## Organization

`projects/` holds each film; `agents/` holds role briefs; `skills/` holds the project procedure and links to existing canonical skills; `memory/` indexes local film memory; `scripts/` contains safe management tools; `docs/` explains operations; `shared/templates/` holds review templates.

O projeto agora usa Git local na branch `main`, com Git LFS para mídias e um snapshot inicial. Não há remoto nem publicação no GitHub. Veja [docs/VERSION_CONTROL.md](docs/VERSION_CONTROL.md). Os links de skills continuam locais à máquina, sem copiar código de fornecedores. Nenhum serviço pago ou dataset Cognee foi criado.
