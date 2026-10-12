# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

`AGENTS.md` (imported above) is the mandatory operating contract: session-start reading order, spending/identity boundaries, handoff rules. This file adds only what it does not cover: commands and the shape of the code.

## Workspace orientation

This is a local film-production workspace for *Andre viajando no tempo*. The active film is `projects/andre-time-travel` ("The Table Between Centuries"); the Python tools manage production records and are not a separate application. Passing validation or tests does not imply creative, likeness, language, or spending approval.

Use one source per topic: `docs/REPEATABLE_WORKFLOW.md` for the workflow, `docs/LOCAL_AGENT_HANDOFF.md` for edit and handoff rules, and `docs/VERSION_CONTROL.md` for Git. The current episode workflow map is `projects/andre-time-travel/tasks/plans/workflow-map-v1.md`; encounter direction is `projects/andre-time-travel/docs/2026-10-09-direcao-encontros-fala-dificil.md`.

## Commands

The management tools are stdlib-only Python (3.11+). `README.md` and `docs/VERSION_CONTROL.md` use `.venv/bin/python`; the venv is created with `python3 -m venv .venv` and any `python3` works for the stdlib tools.

```bash
.venv/bin/python scripts/manage.py status        # read-only state of workspace + board
.venv/bin/python scripts/manage.py validate      # workspace integrity, exit 2 on error
.venv/bin/python scripts/manage.py lint          # hard contradictions and advisories
.venv/bin/python scripts/manage.py resume        # session-start digest (AGENTS.md step 7)
.venv/bin/python scripts/manage.py handoff check <file>    # validate a handoff and its hashes (producer: handoff ingest)
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m unittest tests.test_workflow.WorkflowTests.test_paths_cannot_escape_workspace   # one test

# Handoff inventory (SHA-256 index) and verification
.venv/bin/python scripts/workflow.py index  --output reports/workflow-v1/file-index.json
.venv/bin/python scripts/workflow.py verify --index  reports/workflow-v1/file-index.json
.venv/bin/python scripts/workflow.py new-draft --id <slug> --title "<title>" [--test-only]
.venv/bin/python scripts/workflow.py check-clean-draft --path drafts/<slug>

# Rebuild the review atlas into a NEW revision folder (refuses to overwrite). Needs Pillow,
# ReportLab, pdftoppm and DejaVu fonts; see docs/REPEATABLE_WORKFLOW.md.
python3 scripts/build_preproduction_atlas.py --source 05_storyboard/source/atlas.json \
    --output 05_storyboard/preproduction-atlas-v3 --revision v3
python3 scripts/verify_handoff.py --output reports/<name>.json

# Free local review log of images (no media generation)
python3 scripts/review_sweep.py --film andre-time-travel
python3 scripts/review_sweep.py --record <path> --verdict keep|keep-tone-only|reject|variant-needed
```

`scripts/kling_batch.py` (`--submit-only` / `--resume JOB`) and `scripts/gemini_generate.py` are producer-only paid tools. Do not run them unless you hold the producer role with a written scope and a fresh balance refresh (AGENTS.md).

Run `manage.py validate` and the unit tests after any change to management data (JSON/CSV under `projects/`, `workspace.json`, registries, scripts).

### Known environment pitfall (Mistake/Solution record)

`skills/film-*`, `skills/grounded-citations` are symlinks to `/home/athar/.hermes/skills/...` (machine-local, recorded in `skills/registry.json`). On any other machine `manage.py validate` exits 2 with `missing or broken skill source: ...` and environment-dependent validation tests can fail. That is an environment condition, not a regression: do not "fix" it by editing the registry, deleting the links, or weakening the validator. Verify the current baseline with `validate` and the full test suite; test counts change with the code.

In Claude Code cloud sessions, `.claude/hooks/session-start.sh` (registered in `.claude/settings.json`, active only when `CLAUDE_CODE_REMOTE=true`) creates `.venv` and writes a labelled placeholder `SKILL.md` at each missing link target outside the repository, so missing-link tests can run; this is not evidence that the original skills were loaded. The placeholders are not the skills: they carry no procedure, and `validate` keeps reporting `shared skill changed since linking` for them.

## Architecture

Offline production-management workspace for an AI-generated film series. The management layer is a set of validators and renderers over JSON/CSV/Markdown state. `sites/movies-demandas` is the separate Central de Demandas frontend, with its own local build and persisted site demands; its production views derive from these records. The film product remains the media and documents under `projects/`.

**Registry and layout.** `workspace.json` names the active film and the `requiredDirectories` that `manage.py validate` enforces. Each film lives in `projects/<id>/` with a numbered pipeline: `00_brief` (brief, `approvals.json`, `decisions/` with cited decision IDs), `01_script` (`script-en.md` + `dialogue-lines.csv`, kept in sync), `02_references` (raw / selected / approved / synthetic / history-eyes, never mixed), `03_bibles`, `04_audio`, `05_storyboard`, `06_pilot`, `07_generations` (requests / responses / originals / accepted / rejected), `08_edit`, `09_delivery`, plus `manifest.json`, `tasks/board.json`, `credit-ledger.csv`, `asset-registry.csv`, `memory/STATE.md`.

**Canonical state vs. derived output.** Editable sources are small text files; derived documents are rendered into a new versioned folder and never edited in place:

- `05_storyboard/source/atlas.json` + `01_script/dialogue-lines.csv` → `scripts/build_preproduction_atlas.py` (via `scripts/atlas_inputs.py`, the input contract) → `05_storyboard/preproduction-atlas-vN/` with PDFs, PNGs, gallery and `evidence/build-inputs.json` hashes. The renderer refuses unknown line IDs, missing references, external paths and existing output folders.
- `manifest.json` ↔ `05_storyboard/shot-list.csv` (durations), owned by the producer.
- `tasks/board.json` states are `pending|ready|blocked|in_progress|completed|cancelled`; `manage.py` checks `dependsOn` for unknown IDs and cycles.

**Handoffs and provenance.** Agents deliver work as `projects/<film>/agents/handoffs/<date>-<role>-<topic>.json` copied from `shared/templates/agent-handoff-v2.json`, with before/after SHA-256 hashes. `workflow.py index/verify` produces the file inventory used to detect concurrent edits. `.gitattributes` sets `* -text` so hashes survive Git, and routes all media/PDF/ZIP through Git LFS.

**Roles and skills.** `agents/registry.json` maps film roles (producer, director, continuity, historian, ...) to briefs in `agents/*.md` and to skills; only `producer` has `paidSubmissionAuthority`. `skills/andre-time-travel/SKILL.md` is the project-local procedure; `kling-cli` is vendored at `.agents/skills/kling-cli`, linked from `skills/`, `.hermes/skills/` and `.claude/skills/`. The other shared skills link to profile sources through `skills/` and `.hermes/skills/`; they are not all mirrored in `.claude/skills/`. See `docs/AGENT_CATALOG.md` for derived, inactive reviewer adapters and frontend synchronization. `docs/PARLEY_PROTOCOL.md` describes the Agent Parley lanes (`claude`, `codex`) that work in separate worktrees and return handoffs instead of editing producer-owned records.

**Series vs. episode.** `series/andre-time-travel/series.json` and `FRAMEWORK.md` hold reusable rules; `shared/templates/continuation.json` + `workflow.py new-draft` create a clean draft under `drafts/` that inherits no budget, jobs, approvals or layout (tests in `tests/test_workflow.py` guard this).

Documentation is mixed pt-BR and English; keep each file in the language it already uses.

## Local Git

The project uses `main`, Git LFS, and the private `origin` remote. Treat commit, merge, and publication as separate actions requiring task-level authorization. Preserve concurrent work, stage only assigned paths, inspect the staged diff, and do not use destructive resets or cleanup on shared checkouts. Runtime environments, caches, and credentials remain ignored.
