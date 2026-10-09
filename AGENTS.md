# AGENTS.md — Movies_Projects

This is a film production workspace, not the TransfereGov application. Do not modify or invoke that project's code, databases, services, output conventions, or virtual environment for film production.

## Session start

1. Read `workspace.json` and the active film's `memory/STATE.md` — the single resume surface. `CONTINUE_HERE.md`, `START_HERE.md` and `docs/checkpoint-*.md` are detail, not alternatives. Decisions are cited only by `00_brief/decisions/` IDs (`memory/decisions.json` is superseded history).
2. Read that film's `manifest.json`, `tasks/board.json`, and `00_brief/approvals.json`.
3. Read `skills/andre-time-travel/SKILL.md` for this film's operating procedure.
4. Load existing `kling-cli`, `film-character-continuity`, `film-dialogue-localization`, and `film-editing-qc` skills when relevant. Their links are in `skills/`; do not copy vendor/profile skills here.
5. Run `.venv/bin/python scripts/manage.py status` to inspect actual pending state.

## Non-negotiable boundaries

- Andre's own approved likeness stays consistent. Other historical figures' full faces appear in zero frames; eyes-only reactions and below-neck details are allowed. Inspect reflections and every frame of risky shots.
- Real photographs, synthetic variants, style references, historical casting and UI screenshots are separate categories. No inbox reference is automatically approved. Preserve originals.
- All dialogue is fictional; factual anchors retain sources. Never invent quotations, task IDs, charges, job results, accepted takes, media files, or language validation.
- The historical 7,741-credit snapshot is not a live balance. Refresh through the CLI before paid work. Whole-film spending authorization is a ceiling, not batch approval.
- Kling interactions use only the installed CLI and live schemas. No direct HTTP/MCP bypass, credential access, login churn, automatic retries, or paid setup probes.
- Only the producer/parent agent can submit approved paid requests. Reviewer agents have no spending or external-write authority. No background generation or schedules are enabled.
- ElevenLabs/other fees require their own scope; never buy credits or services automatically.
- No credentials or private tokens in assets, logs, prompts, skills or memory. Use existing secure authentication/vault routes.
- Store project state in local film memory, not global user memory. These files are not a claimed remote Cognee integration.
- Use relative project paths in management data. Never silently overwrite user files, move/delete legacy Elements, commit, push, or create media outside approved scope.

## Verification

Run the project's stdlib unit tests and `manage.py validate` after management changes. Workspace validity is not film acceptance. Full final-file playback, technical inspection, user likeness approval and language review are separate gates. Keep canonical task/approval/manifest states consistent; update session memory after material verified changes.

## Local editing and series continuation

Read `START_HERE.md`, `docs/REPEATABLE_WORKFLOW.md` and `docs/LOCAL_AGENT_HANDOFF.md` for the local handoff. The user authorizes agents to edit assigned sources locally. Coordinate file ownership, record base hashes, preserve concurrent edits, and render derived documents into a new revision. Do not overwrite delivered atlases or treat an inventory as creative acceptance.

`series/andre-time-travel/series.json` separates reusable rules from episode-specific choices. `shared/templates/continuation.json` creates clean planning drafts through `scripts/workflow.py`; it does not register a new production or inherit budget, jobs, takes, runtime, chapter count or approvals. The rehearsal in `drafts/workflow-rehearsal` is test-only.

## Local version control

The user requested local Git versioning on 2026-10-09. The workspace uses `main` and repository-local Git LFS; no remote or publication is configured by that request. Read `docs/VERSION_CONTROL.md`. Preserve media and approvals, stage only your assigned changes, inspect the staged diff, and coordinate with agents sharing this checkout. A commit does not grant production approval. Runtime environments, caches and credentials remain ignored. Keep necessary empty directories through `.gitkeep`; track symlinks without copying external skill contents.

## Direção dramática compartilhada do filme ativo
Antes de planejar, gerar ou revisar encontros, todos os agentes e subagentes devem ler `projects/andre-time-travel/docs/2026-10-09-direcao-encontros-fala-dificil.md`. A fala difícil motiva a reação; preservar a perspectiva pessoal de Andre, sua identidade e zero rostos históricos completos. Humor é liberdade dramática, não dispensa de verificar cultura material. Consultar os papéis historian, lighting e dialogue-sound; iluminação será detalhada depois. Estas instruções não iniciam agentes nem autorizam gasto.
