# Tech Stack

- Python >=3.11, stdlib-only management tools (`pyproject.toml`: no dependencies, name `movies-projects`). Ruff: line-length 99, target py311. Venv at `.venv/` (`python3 -m venv .venv`); any python3 works for stdlib tools.
- Exceptions (non-stdlib, local-only): atlas/PDF renderer `scripts/build_preproduction_atlas.py` needs Pillow, ReportLab, Poppler (`pdftoppm`), DejaVu fonts. Paid producer tools: `scripts/kling_batch.py` (Kling CLI), `scripts/gemini_generate.py`.
- Data formats: JSON registries/board/approvals/manifest, CSV (`dialogue-lines.csv`, `asset-registry.csv`, `credit-ledger.csv`, `shot-list.csv`), Markdown STATE/docs. `.gitattributes`: `* -text` (hashes survive Git), media/PDF/ZIP via repo-local Git LFS.
- Git: branch `main`, private `origin`; commit/merge/publish are separate authorizations (`docs/VERSION_CONTROL.md`).
- Frontend `sites/movies-demandas`: Next 16.3 / React 19.2 / TypeScript, Drizzle ORM, vinext/Wrangler local dev, Node >=22.13. Own `package.json` scripts; data checked via `npm run check:data` (prebuild).
- Skills are symlinks, not copies: `skills/film-*`, `skills/grounded-citations` → `/home/athar/.hermes/skills/...` (machine-local, in `skills/registry.json`); `kling-cli` vendored at `.agents/skills/kling-cli`, linked from `skills/`, `.hermes/skills/`, `.claude/skills/`. On other machines `manage.py validate` exits 2 `missing or broken skill source` — environment condition, not a regression; never fix by editing registry/deleting links/weakening validator.
- Serena: `.serena/project.yml` language_servers `[python, typescript]` (python = `scripts/`+`tests/`, typescript = `sites/`).
