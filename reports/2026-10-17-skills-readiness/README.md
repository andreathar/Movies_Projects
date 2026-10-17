# Skill readiness for agents — 2026-10-17

Scope: make every skill-related file usable by an agent without guessing (read order, references, gates, tool mapping), and put Higgsfield under the same producer-only spend discipline as Kling. Requested by Andre in chat ("check all skill related files… implement all"). No media, spend, commit, merge or push.

## Findings → changes

| # | Finding | Change |
|---|---|---|
| 1 | Claude Code could auto-load only `kling-cli`; the project skill was unreachable | `.claude/skills/andre-time-travel` → `../../skills/andre-time-travel` (project-local, safe). Shared skills stay path-read (their links are machine-local). |
| 2 | `andre-time-travel` omitted most of `AGENTS.md` (workflow map, encounter doc, handoff, resume/lint, mistakes, roles, hooks); vague description | Rewritten: specific trigger description, read order, task→document map (root vs episode paths explicit), roles, spend gates, hooks, closing checklist. Original rules kept. |
| 3 | `kling-cli` lacked the project spend gate and hook behaviour; body still said CLI 0.2.1 | New "Portão de gasto" section (release → scope.json → runner), load map, hook false-positive note, update warning; CLI 0.2.3 folded in. |
| 4 | Three `film-*` skills changed after linking (unreviewed hashes) | Full content read; hashes recorded in `skills/registry.json` with `provenanceHistory` review entries (old hashes kept). Producer to confirm at ingest. Files in `~/.hermes` were **not** edited. |
| 5 | Shared skills assume Hermes tools/paths (`vision_analyze`, `~/.hermes`) | `skills/andre-time-travel/references/shared-skills-adapter.md` (tool map, path fixes, verified grounded-citations command, ledger rule). `agents/CONTRACT.md` points every role to it. |
| 6 | No precedence between shared skills and `AGENTS.md` | Precedence table in the adapter; `film-editing-qc` "act as producer" case called out. |
| 7 | `skills-lock.json` hash is upstream's | Not a defect (it records the upstream install); documented in `kling-cli` and that `skills update` would overwrite the adaptation. |
| 8 | Higgsfield not covered by any rule or hook | `.claude/hooks/higgsfield-gate.py` (CLI + MCP, deny-by-default except read-only, producer lane + fresh scope for spend, `auth token` always refused), registered in `.claude/settings.json`, template `shared/templates/higgsfield-scope.json`, policy in `docs/MODEL_POLICY.md`, 7 tests. |
| 9 | Nothing kept skills honest over time | `tests/test_skills_readiness.py` (7 tests: referenced files exist, frontmatter, registry hash, Claude discoverability, router coverage, role/registry/contract, Higgsfield wiring). |

## Verification actually run
- `manage.py validate`: ok, warnings `[]` (was 3 "shared skill changed" warnings).
- `agent_catalog.py --check`: ok after regenerating `agents/generated/catalog.json`.
- Unit tests: 258 → 272 (baseline 258 OK before edits; all green after). New: 7 Higgsfield-gate + 7 readiness.
- Hook tests prove: read-only Higgsfield commands pass; create/upload/soul-id/project-write/auth-login, wrapped (`cd … &&`, `bash -c`, `npx`, `env`) and chained forms are denied outside the producer lane; producer needs a fresh scope (stale, naive timestamp, relayed grant, ceiling > balance, job type not listed all denied); MCP generate/upload/publish denied even for the producer; `hf download` (Hugging Face) untouched.
- `lint`: see handoff — the pending coordinator handoff `2026-10-17-coordinator-team-strategy-review-v1.json` recorded hashes for five files this work legitimately changed; the new handoff lists it in `supersedes` (hash currency only; its other content stands).

## Needs the producer / Andre (not done here)
1. **Apply `canonical-docs.proposed.patch`** (AGENTS.md + CLAUDE.md). `canonical-guard` refuses these edits outside the producer lane and I did not bypass it. From the base checkout as producer: `git apply reports/2026-10-17-skills-readiness/canonical-docs.proposed.patch` (verified with `git apply --check`).
2. **Site snapshots are stale** (`sites/movies-demandas/data/workspace-reference.json`, `production.json` still carry the old `kling-cli` hash). Both files already contain someone else's uncommitted changes in the site repo, so they were not overwritten. Re-run the two exporters (docs/AGENT_CATALOG.md) once that work is settled.
3. **Higgsfield live use**: to generate, the producer lane copies `shared/templates/higgsfield-scope.json` to `projects/andre-time-travel/00_brief/higgsfield-scope.json` with Andre's direct grant and a fresh `higgsfield account status` balance. `generate cost` is free for estimates. This gate is an operating rule plus hook, not a system lock; `!`-prefixed user commands bypass hooks by design.
4. **Optional hook hygiene** (not changed): `kling-preflight` treats any command containing `kling_batch.py` as a submission, so read-only `grep`/`sed` on the script is refused for non-producers. The skill now says to use Read/Glob; narrowing the hook to real invocations is a trust change for the producer to decide.
5. Review the three `film-*` hashes recorded here; if the 2026-10-09 edits are unwanted, they live in `~/.hermes/skills` (outside this repo).
