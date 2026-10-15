# Movies_Projects — Core

- Film-production workspace (not an app). Active film: `andre-time-travel` = "The Table Between Centuries" (`projects/andre-time-travel/`), registered in `workspace.json` (`activeFilm`, manifest/board/STATE/productionPlan pointers, `requiredDirectories` enforced by validate).
- Mandatory contract: `AGENTS.md` (imported by `CLAUDE.md`). Session start: `workspace.json` + film `memory/STATE.md` (single resume surface) + `manifest.json` + `tasks/board.json` + `00_brief/approvals.json` + `skills/andre-time-travel/SKILL.md`; then `.venv/bin/python scripts/manage.py status`. Decisions cited only by `00_brief/decisions/` IDs.
- Python layer = offline validators/renderers over JSON/CSV/Markdown state in `scripts/`; film product = media/docs under `projects/`. Validation/tests passing ≠ creative, likeness, language, or spend approval.
- Layout: `projects/<id>/` numbered pipeline `00_brief` (approvals, decisions/) → `01_script` (`script-en.md` + `dialogue-lines.csv`, kept in sync) → `02_references` (raw/selected/approved/synthetic/history-eyes, never mixed) → `03_bibles` → `04_audio` → `05_storyboard` → `06_pilot` → `07_generations` (requests/responses/originals/accepted/rejected) → `08_edit` → `09_delivery`; plus `manifest.json`, `tasks/board.json`, `credit-ledger.csv`, `asset-registry.csv`, `memory/STATE.md`.
- Canonical vs derived: editable sources are small text files; derived docs render into a NEW versioned folder, never edited in place (atlas: `05_storyboard/source/atlas.json` + dialogue CSV → `scripts/build_preproduction_atlas.py` via `scripts/atlas_inputs.py` → `preproduction-atlas-vN/`, refuses unknown line IDs/external paths/existing output). `manifest.json` ↔ `05_storyboard/shot-list.csv` durations, producer-owned.
- Roles/skills: `agents/registry.json` maps roles (`agents/*.md` briefs) to skills; only `producer` has `paidSubmissionAuthority`. Parley lanes `claude`/`codex` work in separate worktrees, return handoffs, never edit producer records (`docs/PARLEY_PROTOCOL.md`).
- Series vs episode: `series/andre-time-travel/series.json` + `FRAMEWORK.md` = reusable rules; `scripts/workflow.py new-draft` drafts under `drafts/` inherit no budget/jobs/approvals/layout.
- Separate frontend: `sites/movies-demandas` (Central de Demandas, Next.js) derives views from these records; own build/data checks there.

## Invariants (non-negotiable)

- Andre likeness consistent; other historical figures: full face in zero frames (eyes-only/below-neck OK), check reflections/every frame.
- Never invent quotes, task IDs, charges, job results, accepted takes, media files, or language validation. Factual anchors keep sources; all dialogue fictional.
- Kling only via installed CLI + `scripts/kling_batch.py`, producer-only, requires `kling_job_release` in `00_brief/approvals.json` + fresh credit refresh (7,741 snapshot is history, not balance). No HTTP/MCP bypass, auto-retries, or paid probes. ElevenLabs/other fees need own scope.
- No credentials in assets/logs/prompts/skills/memory. Preserve originals/provenance/concurrent work; relative paths in management data; never silently overwrite, move/delete legacy Elements, commit/push without separate authorization.
- Every delivery chains a next task (accepted owner / blocker+owner+unblock condition / closed stage) per `docs/REPEATABLE_WORKFLOW.md`.

## Focused memories

- Refactored frontend entry points and persistence/review boundaries: `mem:frontend_architecture`
- Canonical data ownership and Python validation/export paths: `mem:production_architecture`

- Stack, versions, dependencies: `mem:tech_stack`
- Runnable commands (manage/workflow/atlas/site): `mem:suggested_commands`
- Code/data style, handoff & provenance rules: `mem:conventions`
- Done-gates per change type: `mem:task_completion`
