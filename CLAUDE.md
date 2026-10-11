# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

`AGENTS.md` is the binding operating contract (session-start reads, spending/identity/approval boundaries, ownership). Everything below is Claude-specific orientation and does not override it.

## What this repo is

A local film-production workspace (pt-BR docs, English film script) for the series *Andre viajando no tempo*; the active film is `projects/andre-time-travel` ("The Table Between Centuries"). It is **not** a software product: the Python in `scripts/` is small stdlib-only management tooling around production records. Many tasks here are editing documents/JSON/CSV, not code. Creative acceptance, spending and likeness approval are never implied by passing validation or tests.

## Commands

Always use the repo venv (`.venv/bin/python`), run from the repo root.

```bash
.venv/bin/python scripts/manage.py status          # read-only, offline: actual pending state
.venv/bin/python scripts/manage.py validate        # cross-checks manifest/board/approvals/registry consistency
.venv/bin/python -m unittest discover -s tests -v  # workspace tests (stdlib unittest, no pytest)
.venv/bin/python -m unittest tests.test_manage -v  # one test module
.venv/bin/python -m unittest tests.test_manage.WorkspaceValidationTests.test_validate_checks_workspace_integrity  # one test
.venv/bin/python -m unittest discover -s docs/kling-manual/tools -p 'test_*.py'  # tests for the Kling preflight/model-sheet tools
.venv/bin/python scripts/workflow.py verify --index reports/workflow-v1/file-index.json  # hash-check delivered files
.venv/bin/python scripts/workflow.py new-draft --id <id> --title <t> --test-only         # clean continuation draft under drafts/
```

Lint config is `ruff` (line length 99, py311) in `pyproject.toml`; there is no build step. `validate` currently reports ok with a few shared-skill hash warnings — a known baseline, not a regression. Run `validate` + tests after any change to `scripts/`, JSON registries or management data.

Scripts that call external services or need extra deps — treat as gated, do not run casually:
- `scripts/kling_batch.py` — producer-only paid Kling runner (`--submit-only` submits exactly one job; `--resume JOB` queries once, never submits). Writes intent/ledger before submitting; never retried. Needs explicit written spend scope and a live balance refresh (see AGENTS.md).
- `scripts/build_preproduction_atlas.py` — renders the review atlas/PDFs; needs Pillow, ReportLab, Poppler and local fonts (not in the stdlib-only set). Output goes to a **new** versioned folder, never over `preproduction-atlas-v1`.
- `scripts/gemini_generate.py` — uses `GEMINI_API_KEY` from `.env` (git-ignored; see `.env.example`).
- `docs/kling-manual/tools/kling_preflight.py` — offline check of a request JSON against the `who_am_i` snapshot; safe, no credits.

## Architecture (the big picture)

**Registry chain.** `workspace.json` → per-film `manifest.json` + `tasks/board.json` + `00_brief/approvals.json` (+ `credit-ledger.csv`, `asset-registry.csv`) → `memory/STATE.md` (the single resume surface). `scripts/manage.py` (`validate`/`status`) is what keeps these records mutually consistent; `scripts/workflow.py` produces hash indexes and clean continuation drafts from `shared/templates/continuation.json`; `series/andre-time-travel/series.json` separates reusable series rules from episode choices. Decisions live as `00_brief/decisions/Dnn-*.json` and are cited by ID.

**Film pipeline layout** (`projects/<film>/`): numbered stage folders `00_brief` → `01_script` → `02_references` → `03_bibles` → `04_audio` → `05_storyboard` → `06_pilot` → `07_generations` (originals/requests/responses/accepted/rejected) → `08_edit` → `09_delivery`. `workspace.json.requiredDirectories` is the layout `validate` expects. Editable **sources** (`01_script/script-en.md` + `dialogue-lines.csv` kept in sync, `05_storyboard/source/atlas.json`, `03_bibles/`) generate **derived** deliverables (atlas HTML/PDF, cards). Fix sources and re-render to a new version; never hand-edit PDFs/PNGs or delivered V1/V2 folders.

**Roles and ownership.** `agents/*.md` + `agents/registry.json` define film roles (producer, director, historian, continuity, lighting, dialogue-sound, storyboard, editor, qc). Role limits are real: only the producer submits paid jobs; reviewers never spend. Multi-agent work follows `docs/PARLEY_PROTOCOL.md` (lanes `claude`/`codex`, each in its own worktree/branch, advisory file reservations, one handoff per finished task). Canonical records (manifest, board, approvals, ledgers, STATE, session-log) are producer-owned — lanes propose via handoff and write only new files in their assigned path.

**Skills.** `skills/andre-time-travel/SKILL.md` is the canonical film procedure. Other entries in `skills/` and `.claude/skills/`/`.hermes/skills/` are symlinks to machine-local skills (`~/.hermes/...`) or to `.agents/skills/`; they are tracked as links, never copied.

**Docs map** (one source per subject, per `docs/TOKEN_EFFICIENCY.md` — don't duplicate or add new global summaries): `docs/REPEATABLE_WORKFLOW.md` (procedure, closure/successor rule), `docs/LOCAL_AGENT_HANDOFF.md` (edit/handoff contract), `docs/VERSION_CONTROL.md`, `docs/kling-manual/` (live-schema Kling guide + CLI help snapshots), `projects/andre-time-travel/tasks/workflow-map-v1.md` (task owners/dependencies), `projects/andre-time-travel/docs/2026-10-09-direcao-encontros-fala-dificil.md` (mandatory dramatic direction).

## Git specifics

- Branch `main`; media (png/jpg/webp/mp3/wav/mp4/mov/pdf/zip, etc.) is stored in **Git LFS** via `.gitattributes`, and `* -text` disables EOL conversion so provenance hashes stay valid. Don't normalize line endings or re-encode tracked files.
- `origin` is a private GitHub repo; pushing, committing and merging each need task-level authorization (AGENTS.md). Stage only your own paths, review `git diff --cached`, no `reset --hard`/clean on shared checkouts. Keep empty dirs via `.gitkeep`.
- `.venv/`, caches, `.env*` (except `.env.example`) and credentials are ignored.
