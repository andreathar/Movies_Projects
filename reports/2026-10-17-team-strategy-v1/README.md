# Team strategy delivery

2026-10-17 · episode `andre-time-travel` · ad-hoc implementation helper, not a Parley lane or desktop producer. Authorization: Andre's direct request to optimize existing briefs/prepared adapters (option 1), keep them inactive, and clarify team/process/folder/file/Parley naming. No activation, spend, services, publication or commit authorized or performed.

## Start here

- [Team map](../../agents/README.md): people vs participants vs stable role IDs; six process names; folder purposes and new-file naming.
- [Role contract](../../agents/CONTRACT.md): review/edit/governance modes, path roots, evidence and capability limits.
- [Coordination procedure](../../docs/COORDINATOR_PROTOCOL.md): bounded assignment, acceptance, checks, integration, successor and escalation.
- [Parley protocol](../../docs/PARLEY_PROTOCOL.md): existing lane identities, reservations and runtime restrictions.

**Team:** Andre is author/operator. Desktop Codex is producer/director, distinct from the Parley `codex` participant. Existing participants `claude` and `codex` receive a named role per accepted assignment. A helper gets no lane identity by implication. The ten roles remain producer, director, coordinator, historian, continuity, lighting, dialogue-sound, storyboard, editor and qc; ten responsibilities do not imply ten processes/workers to launch.

**Process vocabulary:** Scope → Assign → Make → Check → Integrate → Close. These are message/task-description verbs, not new board statuses. Stable IDs, numbered episode folders and existing canonical filenames are unchanged. New artifacts use `<topic>-vN`; handoffs use `YYYY-MM-DD-<role>-<topic>-vN.json`, preserving existing shot/task/line IDs.

## Implemented

1. Replaced duplicate/ambiguous role instructions with focused missions and one shared execution contract. Corrected storyboard approval contradiction. Named input versions rather than assuming script/research v2.
2. Removed all-handoff startup scanning from coordinator/producer; mandatory AGENTS startup and relevant integration evidence remain required. Coordinator is a routing responsibility, not a fabricated live teammate; no timers, automatic wakes or external notifications.
3. Moved coordination procedure to one maintained document. Marked the older proposed Parley roster and supervision settings as unactivated historical proposals, not current routing or permission grants. Updated the paid-release reference: `scope.json` alone is insufficient.
4. Shortened display names without changing role IDs, file paths, skills, registry authority flags, autostart or running state.
5. Changed adapter generation to include only reviewer Reads/Review/May not sections plus a findings-only completion contract, instead of inheriting file-writing and full-media completion instructions. Parent owns handoff packaging and missing media/language checks. Shared contract hash is now a generation input.
6. Regenerated seven prepared artifacts. No client discovery directory or configuration was modified. Claude tool list remains Read/Glob/Grep; Codex prompt wording remains an operating rule, not tool enforcement.
7. Expanded scoped tests from 8 to 14: review-only rendering, required/duplicate sections, contract hash drift, stable adapter identity, bounded Mission parsing, and real storyboard/registry invariants. Fixed the empty-Mission parser case exposed by the new test. Independent reviewer caught an escaped-word-boundary test bug; corrected it and added a positive control before final tests.

Ten role briefs decreased from **4,014 to 2,338 whitespace-separated words (41.8%)** against captured input copies. The new shared contract/team map/procedure also contain necessary instructions: this is a per-brief reduction, **not** a total-loaded-context, model-token, speed or cost benchmark. No model behavior/runtime effectiveness test is claimed.

## Verification

- Full stdlib suite: **257 tests passed** (`unit-tests.log`).
- Catalog generation: 7 outputs; subsequent `--check` OK, no drift, activation pending (`catalog-check.json`).
- `manage.py validate`: exit 0 (`validate.json`).
- `manage.py resume`: exit 0 (`resume.json`).
- Scoped `git diff --check`: passed.
- Independent read-only reviewer: one test issue, corrected as described above. Earlier research review also completed; no delegate failure remains outstanding.

### Open integration blockers — not a fully green workspace

- **`manage.py lint`: exit 2.** The preserved `2026-10-17-maintenance-cleanup-v2.json` snapshots old versions of the 20 agent/generator/test files that this newly authorized revision changes. Lint reports their SHA-256 mismatches. Its old hashes were not rewritten, and this delivery does not supersede that broader maintenance package (which contains unrelated work). Desktop producer owns evidence reconciliation/integration preserving both deliveries. See `lint.json` for exact findings and existing advisories.
- **Frontend freshness check: exit 1**, `Snapshot desatualizado: .../sites/movies-demandas/data/workspace-reference.json` (`frontend-catalog-check.log`). The nested repository already has concurrent changes. It was not overwritten, exported or built here. Frontend owner must regenerate/review derived snapshots against the accepted catalog without losing that work. No new frontend incompatibility or rendering failure is established by this freshness result.
- Shared-skill drift remains an existing review gate, not an automatic rehash or approval.

No media, board, approvals, decisions, STATE, session log, historical handoff, frontend file, credential, hook or model/provider permission was edited. No Parley dispatch or native adapter activation was performed. Unrelated concurrent edits remain untouched.

## Successor

Implementation/check stage closed; integration pending. Desktop producer owns reviewing this delivery, reconciling historical handoff evidence without losing the maintenance package, and assigning frontend refresh to its owner. No successor acceptance is claimed; no live work starts merely because this report exists. Authoritative production/approval records remain unchanged. See the versioned episode handoff for source/output hashes, checks and blockers.
