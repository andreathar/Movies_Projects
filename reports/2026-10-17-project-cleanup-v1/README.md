# Project cleanup audit — 17 October 2026

Scope: delegated local maintenance for The Table Between Centuries. No film production or artistic decisions. Main is `35f84474377f86876fcf691dee16036b8601a495`; earlier `629c23d` is historical. This is an audit record, not a replacement for the film STATE, board or approvals.

## Inventory and ownership checkpoint

Filtered baseline: **2,996 files, 2,059,702,748 bytes**, plus 13 resolving symlinks. Full checkout allocated size was 5,647,646,720 bytes. Excluded trees are enumerated in the external inventory: Git internals, virtual environments, node_modules, Python/tool caches and frontend build/runtime directories. Examples: root .git ≈1.96 GB, .venv ≈534 MB, frontend node_modules ≈994 MB. They are retained, not unused-file candidates.

| Area | Files | Logical bytes | Classification |
|---|---:|---:|---|
| Film projects | 1,765 | 1,551,386,623 | Sources, references, production records and historical deliveries |
| Inbox | 411 | 495,322,349 | Original inputs and provenance; preserve |
| Reports | 351 | 4,877,156 | Historical checks and handoff evidence; preserve |
| Frontend, excluding listed runtime/dependencies | 232 | 3,035,235 | Separate dirty repository, runtime consumers and derived exports |
| Scripts | 23 | 256,963 | Management, producer tools, dynamic imports and rendering |
| Tests | 16 | 185,306 | Active verification |

Read current AGENTS, workspace, STATE, manifest, board, approvals, local procedure, workflow map, ownership/handoff/Git/token policies and earlier cleanup inventories/plan. The referenced old Claude consolidation directory was absent in the registered worktrees; no missing delivery was assumed integrated. Read-only support audits checked backend dependencies and frontend/provenance separately; one owner applied edits.

Parley status: server not ready, both retained lanes stopped, zero reservations/claims. The read initially needed its existing external events lock; it succeeded outside the sandbox. No coordination service was started, and no identity, grant or role was changed. Two registered lane worktrees were preserved. The frontend launcher reported running=false/ready=false. Its existing dirty/untracked sources were recorded before work and preserved.

A concurrent read-only audit appeared in [the separate audit folder](../2026-10-17-cleanup-audit/README.md) after this baseline. Its files and captured observations were preserved as another contributor’s work; they are excluded from this cleanup’s ownership/rollback manifest. Its inventory uses different runtime exclusions, so its file count is not directly comparable. Its observed four-file concurrent diff is this cleanup’s work, not that auditor’s edits.

## Risk-ranked result and changes

| Risk | Decision | Evidence / action |
|---|---|---|
| Low | Applied | README now points to the workspace-selected visual JSON plan rather than calling the old prose plan canonical; private-origin wording matches VERSION_CONTROL. START_HERE separates current planning from delivered visual history and links current CLI/V4 guidance. |
| Low | Applied | CLAUDE closing-check reference uses AGENTS step 5; atlas example uses an unused v4 revision and an explicit matching workspace-relative verifier target. Inventory example chooses a fresh report path, preserving old indexes. |
| Low | Applied | Removed only unused `import math` from build_galileo_animatic.py. AST/full-source review found no load or reflective consumer. Independent diff review found no problems. |
| Medium | Retain | Scripts, historical prompt JSON, generated adapters, build outputs and caches have active, dynamic, historical or shared consumers. No complete file was proven safely removable. |
| High | Preserve / producer review | Media, variants, approvals, historical prompts/results, original experiment batches, pending handoffs and unresolved reference identities. No move, deduplication or deletion. |

Exact existing paths changed: `README.md`, `START_HERE.md`, `CLAUDE.md`, `scripts/build_galileo_animatic.py`. New audit paths: this README, `checks.json`, and `projects/andre-time-travel/agents/handoffs/2026-10-17-maintenance-cleanup-v1.json`.

## Dependency and provenance findings

- `.agents/skills/kling-cli` is the canonical vendored skill. `skills/`, `.claude/skills/` and `.hermes/skills/` expose links, not duplicate copies. Other shared skills resolve to profile sources. Skill telemetry 0.2.1 and executable 0.2.3 are deliberately separate versions.
- Agent briefs/registries and skill registry derive seven catalog/adapters; frontend validates and consumes the catalog. All prepared adapters remain inactive; no generation or activation was performed.
- `manage.py` dynamically loads shared_media/production_plan; production_plan/manual preflight and Kling contract/batch/release consumers remain active. All hook helpers are registered/imported. Preserve `scripts/andre_cinematic_spec.json`: unique historical R2 prompts, photo paths and approval IDs remain valuable even without a filename caller.
- 154 exact nonempty content-hash groups represent 325,839,230 bytes beyond the first copies. These are **not reclaimable-space claims**: role identity, delivered copies and provenance differ. No media tree was copied or deduplicated.
- Catalog: 324 unique asset IDs, no duplicate IDs. Independent audit checked all 15 frontend navigation paths, both experiment galleries' relative links, seven baseline reference hashes and 34 experiment resource records. All resolve/match. Variant names are not interchangeable.

## Preserved unresolved findings and next owner

1. **Producer: experiment gallery identity mismatch.** In `projects/andre-time-travel/07_generations/downloads/2026-10-15-element-experiments-v2/index.html:16`, label `KEXP-W323866270650569-result` loads `KEXP-W323869015528491-result.mp4`; line 44 reverses these IDs. Archived `evidence/build_catalog.py:173` zips differently ordered observations/analyses. Video/contact sheets follow analysis IDs, audio follows observation IDs. Preserve the original gallery, review/analysis, lessons and hashes; review the actual clip/observation associations before publishing a corrected revision. File existence/link validity did not detect this defect. No observation or approval was silently reassigned.
2. **Producer: existing frontend freshness failure.** Both unmodified export `--check` commands fail before and after cleanup. Their snapshots cite HEAD `629c23d`; all 47 production and 33 workspace source hashes match current sources. Current HEAD is `35f8447`. A complete semantic rerender was not performed; no snapshot or persisted workspace was overwritten. `check:data`, tests, lint, types and build pass. The cleanup touches no exporter input or frontend source, so it introduces no navigation/catalog drift. Refreshing exports must preserve the preexisting dirty site and pending handoff inventory.
3. **Producer: pinned documentation drift.** `docs/SHARED_MEDIA.md:40` calls 318 IDs current; actual count is 324. Active lessons-v2 mentions historical CLI 0.2.1. The manual README mixes dated snapshot instructions with the current 0.2.3 guide. These files are hash-pinned by the pending Kling4 v3 inventory; corrections require a new provenance reconciliation, without rewriting old hash evidence or blanket supersession that hides pending work.
4. **Producer/Andre: creative reference conflicts.** G-IN/G-OUT remain composition-only approvals; the five other baseline references remain pending. Preserve table `_4_alt` versus D04 `_2`, wardrobe companions and both experiment batches. Kling4 runtime-v3 remains pending producer review and not ingested; all older handoff bytes and status are preserved. This cleanup handoff supersedes none of them.
5. Baseline advisories remain: three shared-skill hash warnings, undocumented input-role bindings, duplicated approval flags, pending producer handoffs and mixed historical timezone offsets. These are not cleanup permission to mutate approvals/registries or ingest deliveries.
6. Relative-link scan found nine preexisting missing targets in historical snapshots/backups, imported review evidence or removed-base64 placeholders. They are listed externally; no historical content was rewritten merely to make a link check green. Active entry/navigation links added here are checked separately.

## Verification, measurements and rollback

[Command results and preservation evidence](checks.json) record baseline and final checks. Required full suites passed **245 Python, 16 manual-tool and 87 frontend tests**, plus frontend lint, type check and local build. Workspace validate/lint/resume, assets, production-plan `check --verify-media`, seven-file agent catalog `--check` and frontend `check:data` pass. Expected failing child fixture output in the Python verifier tests is intentional; the enclosing 245-test suite passes. No provider calls, paid probes, uploads, media generation, commits, pushes or service restarts occurred. Earlier seven vendor-validator probes remain dated evidence; no changed runtime logic justified repeating them.

Preservation comparison: **2,988 baseline content hashes unchanged**, four intended content edits, four metadata-only entries unchanged; no missing baseline file or unexpected content change. All 13 symlink bindings, base HEAD, original media, production records and existing frontend Git status are preserved. No complete file archived/removed; **zero net storage reclaimed**. Unused source text reduced by 12 bytes; the four existing edited files together grew by 1,091 bytes, plus these audit records. This is navigational/maintenance simplification; no measured speed, runtime-memory or token reduction is claimed.

Backups, full filtered inventory, duplicate-content groups, baseline/final logs, source-integrity report, selective rollback manifest and instructions live outside the repo at:

`/home/athar/Documents/Codex/2026-10-17/task/audit-2026-10-17/`

`before/` contains only four small original text files. `rollback-manifest.json` retains original paths, SHA-256 before/after, modes and byte counts; `rollback.py` defaults to a read-only dry-run and refuses drift before writes. Selective `--path` restores are supported. Added audit/handoff files are moved to `rollback-archived/` during a requested rollback rather than permanently deleted. Review `ROLLBACK.md` first. No rollback was applied.

Next owner is the desktop producer: review this bounded cleanup and reconcile the experiment identities, pending Kling4 inventory and export freshness as one explicit follow-up. No film task or artistic gate was advanced.
