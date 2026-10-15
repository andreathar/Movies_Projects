# Task Completion

- Management data or scripts change: `.venv/bin/python -m unittest discover -s tests -v` + `.venv/bin/python scripts/manage.py validate` (exit 2 = error; broken-skill-link failures on foreign machines are environmental — see `mem:tech_stack`).
- Media catalog change: `.venv/bin/python scripts/manage.py assets validate` + traceability per `docs/SHARED_MEDIA.md`.
- Visual plan change: `.venv/bin/python scripts/production_plan.py check --verify-media`; proposal/technical-check/director-approval/artistic-incorporation are distinct states per version.
- Before closing any delivery: `.venv/bin/python scripts/manage.py resume` + `.venv/bin/python scripts/manage.py lint`. Film gate hooks `.claude/hooks/` are refusals only (tested in `tests/test_hooks.py`); they never approve/spend/commit/merge.
- Role briefs/registries changed: regenerate derived adapters/frontend metadata and check them (`agents/registry.json`, `docs/AGENT_CATALOG.md`).
- Site change (`sites/movies-demandas`): `npm run check:data`, `npm run lint`, `npm test`, `npm run build`.
- Serena memories changed: `serena memories check` from project root.
- Never claim: playback/technical inspection/likeness/language approval from workspace validity — separate gates. Commit/push/spend need separate explicit authorization; verify staged diff before any commit.
