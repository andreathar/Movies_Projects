# Role contract

Shared procedure for the briefs in this folder; `AGENTS.md` remains authoritative. A brief describes a responsibility, not an installed bot, live participant or permission grant.

## Start

Complete the mandatory `AGENTS.md` startup. Load this contract, **one** assigned role brief and its named skills; then the exact task inputs. Do not load every role or every historical handoff. Read additional evidence when needed, especially for a delivery being integrated. For encounter work, apply the direction document and consult historian, lighting and dialogue-sound as required by AGENTS.

Before work identify: episode; session/participant (or `ad-hoc`, never a guessed Parley lane); role; task/package if assigned; mode; exact input paths, versions/hashes and review state; allowed output paths; checks; next owner. Missing information blocks only the affected action. Current board, approvals and decision IDs outrank dated examples.

## Modes and paths

- **review** (default): return findings to the parent; no file writes. A generated adapter is always findings-only review, regardless of a broader source brief's editable areas.
- **edit**: only an explicit local assignment permits changes to its exact allowed paths. A brief's Writes section lists possible areas, not standing permission. Reserve assigned outputs through Parley when in an identified live lane; otherwise report that reservations are unavailable. Do not impersonate a lane or start services to reserve paths.
- **governance**: producer/director powers apply only in the identified authorized desktop/base session. Assigning that role name to a reviewer or lane grants no canonical-write or paid authority. Coordinator proposals go through a handoff.

All machine records and assignments use workspace-relative paths: `projects/<episode>/...`. Briefs' numbered folders are shorthand relative to that episode root. Root `agents/` contains role sources; episode `projects/<episode>/agents/handoffs/` contains deliveries. `shared/`, `skills/`, `scripts/`, `tests/` and `docs/` in these briefs are workspace-root paths. Preserve stable IDs, filenames and delivered versions; use the [team map](README.md) for new names.

## Evidence and capabilities

Separate observed facts, inference, uncertainty and `not_run` checks. Never invent source access, playback, approval, IDs or results. A provider completion or existing file is not acceptance. Inspect exact hashes/versions, not a similarly named export.

A text-only reviewer can assess supplied reports but cannot certify full media decode, normal-speed playback, listening, facial safety or language validation from text. If tools/evidence are missing, mark the specific check `not_run`, name the owner and unblock condition, and continue independent review. Do not request broader permissions automatically or weaken the full-media gate. Qualified language review and Andre's likeness/voice/final acceptance remain separate.

## Output

Return: scope/mode; input paths/hashes; findings; checks actually run and limitations; dependencies/open decisions; next owner or blocker. Each finding: severity, claim, artifact path/hash, line or timestamp/frame where applicable, evidence, uncertainty and recommended action. Keep the summary short; do not repeat the film history.

In edit/governance mode deliver `shared/templates/agent-handoff-v2.json` under the episode handoff directory, with base/output hashes and allowed paths. Preserve concurrent changes per `docs/LOCAL_AGENT_HANDOFF.md`. The parent packages findings from a review-only adapter; that adapter does not write a handoff. Closure requires an accepted successor, a named blocker/unblock condition, or an explicitly closed stage. Sent, acknowledged, delivered, verified and artistically accepted are different states.

## Production boundaries

No reviewer spends, dispatches new work, edits canonical records, generates substitutes or writes externally. Do not change hooks, permissions, credentials, model/provider configuration or runtime activation. Commit, merge, push, publication and purchases require their own authority.

Before proposing Kling models, prompts, references, audio or QC, consult `shared/kling-capabilities.json` and `docs/kling-manual/19-kling4-migration.md`. Listed, tested and approved are different states. Preserve companions, wardrobe/table provenance and hashes; no automatic model switch or reference removal. Paid submission is producer-only via `scripts/kling_batch.py` with the applicable `kling_job_release` in episode `00_brief/approvals.json`, fresh live balance and current CLI schemas. A `scope.json` alone is insufficient; no auto-retries, paid probes or background generation.
