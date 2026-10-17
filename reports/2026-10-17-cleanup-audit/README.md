# Workspace cleanup audit — 2026-10-17

## Scope and conclusion

Andre requested a review of unused folders, deprecated code and references, and a cleaner working project. Session role: independent audit assistant, not the desktop producer or a Parley lane. Active episode: `andre-time-travel`. Authorized output: this audit folder only. No existing project file was edited, moved or deleted; no dependencies uninstalled, services started, provider calls made, approvals changed, or commits created.

**Prioritize navigation and stale instructions before deleting files.** The numbered production pipeline is useful; most apparent duplication serves provenance, review snapshots or delivered revisions. No production script has yet been proven safe to delete. Existing cleanup plans and earlier reviews were reused as leads, not accepted as current facts.

## Measured baseline

- Whole checkout: approximately **5.3 GiB allocated**, including Git, dependencies and runtimes (`du -sh .`). These are rounded observations, not proposed savings.
- Filtered metadata inventory: **3,046 files**, **2,057,809,685 logical bytes**. Includes untracked frontend files; excludes Git, environments, dependency trees, caches and runtime directories listed in `summary.json`, and `.env*` files. Does not follow directory symlinks. This is not a line-by-line review of every file.
- **67 exact media/PDF duplicate groups**, SHA-256 checked; **324,647,689 bytes (309.6 MiB)** redundant-byte upper bound. This is NOT reclaimable space approval: paths often intentionally separate generated originals from curated references. Git LFS retention and hardlinks/filesystem sharing affect actual savings.
- **No broken symlinks** in the filtered walk. External skill links resolve on this machine, but remain portability dependencies.
- Existing local frontend work is extensive: modified tracked files and untracked application modules, review tooling and tests. See `git-baseline.txt`. Parent Git status alone understates it. Treat the entire nested checkout as concurrent work, not disposable scaffolding.

## Cleanup categories and decisions

| Paths/category | Evidence | Recommendation |
|---|---|---|
| `.mypy_cache/`, `.ruff_cache/`, `scripts/__pycache__/`, `tests/__pycache__/` | About 17 MiB allocated combined; already ignored by root `.gitignore` | Disposable cache candidates when no checker/test process uses them. Not removed in this audit; they will regenerate. |
| `.serena/cache/` | About 2.7 MiB allocated | Tool cache candidate only after confirming tool idle and rebuild behavior. Do not equate with `.serena/memories/` or configuration. |
| `sites/movies-demandas/dist/` | About 2.4 MiB, ignored; package build script exists | Rebuildable output candidate, but an active preview may depend on it. Confirm no service consumer before removal. |
| `sites/movies-demandas/node_modules/`, `.venv/` | About 948 MiB and 510 MiB | Installed dependencies, not dead code. Retain for a working project; removing them trades space for reinstall/network/setup costs. |
| `.git/lfs/` | About 1.9 GiB | Keep. Not a generic cache cleanup target; no pruning or history rewrite proposed. |
| `.sites-runtime/`, `.wrangler/`, `.vllm/`, `.serena/` logs/memories | Runtime/configuration boundaries, not content-audited | No deletion without tool-specific ownership and retention review. No private runtime database or credential contents were inspected. |
| `projects/andre-time-travel/02_references/` and `07_generations/originals/` | Many exact-byte pairs; curated reference IDs cite original provenance | Preserve both categories and their paths. Future storage deduplication needs catalog/caller analysis and an explicit migration manifest, not `rm` based on hashes. |
| `08_edit/reviews/holistic-staging-v1/snapshots/galileo-en-preview-v1.mp4` | Exact duplicate of `08_edit/picture-lock/galileo-en-preview-v1.mp4`, 17,495,835 bytes | Historical review evidence. Keep unless producer approves snapshot-policy migration and updates consumers. |
| `07_generations/requests/AB-MIN-shared-keyframe.png` | Same bytes as `02_references/keyframes/andre/KF-galileo-listening.jpg` and `07_generations/originals/R3-galileo-listening-o1_1.jpg` | Preserve request evidence; note misleading extension separately. Do not rename a hash/path-bound historical input. |
| `05_storyboard/preproduction-atlas-v1/` through `v3/`; `reports/`; historical handoffs | Delivered revisions, snapshots and rollback evidence | Keep immutable. Make current entry points clear instead of flattening or deleting history. |
| Required `.gitkeep` folders, root `tasks/` and `memory/`, `drafts/workflow-rehearsal/` | Explicit workspace scaffold and test-only separation | Keep. Empty does not mean unused. |
| `skills/film-*`, `.hermes/skills/`, `.claude/skills/` | Symlink bindings, not copied skill trees | Keep dependencies and adapters. Review three skill-version warnings; never update hashes merely to silence them or uninstall shared tools globally. |
| `sites/movies-demandas/build/` | `vite.config.ts` imports maintained plugin/worker sources | Keep: despite its name, this is source code, not generated build output. |
| `sites/movies-demandas/examples/d1/`, `tests/api.test.mjs` | README describes local D1/API test; default package test script does not include API test | Potential optional starter surface, NOT proven dead. Decide whether optional D1 support is maintained before retiring files/dependencies. No frontend dependency removal recommended from import guesses. |

## Highest-priority stale-reference fixes

Detailed evidence and bounded replacements: `documentation-findings.md`. Checked key findings directly against audit-time files; the recovered earlier consolidation was not replayed.

**Concurrent changes observed before handoff:** another writer modified `README.md`, `START_HERE.md`, `CLAUDE.md` and `scripts/build_galileo_animatic.py` after this audit began. The observed diff already corrects the README plan/publication entries, adds an active-plan entry, fixes the nonexistent AGENTS step, and changes the atlas example to v4. These are NOT this audit's edits. Findings 1, 3 and 4 below describe the captured baseline and are partly/fully addressed in that working diff. A new link points at a separate `reports/2026-10-17-project-cleanup-v1/README.md`; delivery of that other audit is not claimed here. Do not reapply our suggestions blindly. `git-final-observed.txt` and `concurrent-changes.patch` capture the observation; unit-test results below precede these concurrent changes.

1. **Wrong canonical plan:** `README.md:14` labels `projects/andre-time-travel/docs/production-plan.md` canonical, although it is marked DERIVED. Current locator is `workspace.json:17` → `projects/andre-time-travel/05_storyboard/source/production-plan.json`; use `docs/PRODUCTION_PLAN.md` for operating guidance.
2. **Retired wardrobe exposed as current:** `START_HERE.md:17` links `docs/master_production_visual_bible.md`; `docs/master_production_visual_bible.md:30,69` specifies navy/charcoal wardrobe, conflicting with `projects/andre-time-travel/00_brief/decisions/D02-wardrobe.json:10`. Label the compilation historical and route current wardrobe to D02; preserve its evidence and images.
3. **False publication status:** `README.md:41` says no remote/GitHub publication; `docs/VERSION_CONTROL.md:3–5` records the private remote and initial publication. Replace duplicate prose with the canonical reference.
4. **Invalid startup/build examples:** `CLAUDE.md:23` refers to nonexistent AGENTS step 7; `CLAUDE.md:36–37` renders into already-existing atlas v3. Correct the section link and use a new revision placeholder, not an overwrite.
5. **Stale bible reaction order:** `projects/andre-time-travel/03_bibles/scene-bibles/galileo.md:46–47` puts the eye reaction before its motivating sentence. Current plan at `projects/andre-time-travel/05_storyboard/source/production-plan.json:742` places it after the line. Create a reconciled bible revision separately; do not silently rewrite a delivered version.
6. **Historical copied-review links:** the documentation auditor checked 187 local Markdown links across 218 files and found three missing targets (one archived-contract relative link, one renamed copied evidence file and one unresolved handoff). Preserve snapshot bytes; add companion navigation where needed. See detailed report for exact paths and provenance limits. Backtick paths/JSON/CSV references are not covered by that Markdown-link count.

Other logical-retirement candidates are dated budget plans, decision questionnaires and status snapshots listed in `documentation-findings.md`. They should leave current-instruction routes, not disappear from history. The integrated scene-bible proposal is still a proposal; D20 no-armour studies do not retroactively supersede all Genghis footage.

## Technical code/configuration findings

Detailed read-only results: `technical-findings.md`. No production script/test was proven safe to delete; 45 Python files parsed successfully and inspected shell scripts passed syntax checks.

- `scripts/andre_cinematic_spec.json` is a historical dark-wardrobe request with a recorded ledger job and retirement handoff. No executable caller was found. Label historical rather than reusable, but preserve request provenance and check path/hash consumers before any move.
- `.claude/hooks/session-start.sh:25–59` creates placeholder skill files outside the project when external targets are missing. This is active behavior, not dead code; review it as a separately assigned hook change. **No hook/permission trust was changed here.**
- Three external skill hashes differ from the registry. All 13 inspected symlinks resolve. Review source changes; don't automatically rehash, delete external targets or treat path existence as proof of usable skill discovery.
- `scripts/parley_verify.py:12–15` and `.vscode/settings.json:5` discover only `tests/`; offline tests in `docs/kling-manual/tools/test_kling_tools.py` are outside that gate. Keep them and explicitly decide their verification route. That separate suite was not run during this audit.
- Two `.serena/logs/health-checks/*.log` files are tracked. Decide retention with their owner and add a narrow future-log ignore policy if appropriate; do not retroactively delete evidence based on extension.
- `scripts/verify_handoff.py` verifies atlas/rehearsal artifacts, while `manage.py handoff` handles management handoffs. Clarify the command index before considering a compatibility-preserving rename.
- `scripts/respan_smoke.py` makes a provider call. It was not executed and must not be presented as a cost-free cleanup test.

## Target structure (preserve current paths)

- Root: concise entry documents and tool configuration.
- `docs/`: current procedures; `docs/archive/`: explicitly superseded procedures, with old-to-new references if moved.
- `projects/andre-time-travel/`: episode-specific numbered pipeline; `memory/STATE.md` remains the only episode resume surface.
- `series/`, `shared/`, `agents/`, `skills/`: reusable grammar, templates, role sources and tool bindings; not alternate episode state stores.
- `reports/<dated-delivery>/`: immutable audit evidence, not startup instructions.
- `sites/movies-demandas/`: separate frontend checkout with its own ignore/build/test lifecycle. Do not bulk-clean from the parent repository.

Avoid another global status document, a blanket reorganization, or a new archive folder for every old filename. Current-vs-historical authority should be explicit at entry points; path moves come last.

## Checks actually run

| Check | Result |
|---|---|
| `manage.py status` | Pass; 21 tasks, 11 recorded takes, final movie not verified; three shared-skill drift warnings |
| `manage.py validate` | Exit 0; details in `validate.json` |
| `manage.py assets validate` | Exit 0; details in `assets-validation.json` |
| `manage.py resume` | Exit 0; details in `resume.json` |
| `manage.py lint` | Exit 0, no hard errors; advisories remain in `lint.json` |
| `.venv/bin/python -m unittest discover -s tests` | Exit 0; **245 tests passed**. Captured output includes deliberately failing nested fixture tests and expected parser rejection; final suite is OK. |
| Metadata/symlink walk and duplicate hashing | Complete within documented exclusions; `inventory.json`, `symlinks.json`, `exact-duplicates.json`, `summary.json` |

Lint still reports six undocumented input-role bindings, duplicate manifest/approval flags, four un-ingested handoffs, 27 superseded historical handoffs and mixed session-log offsets. Superseded handoffs are not deletion candidates. Validity does not imply film acceptance. No frontend build/tests, playback, browser review, LFS maintenance or paid/provider checks were performed.

`base-hashes.json` records selected canonical input versions. `inventory-method.py` records the scan algorithm (a snapshot, not an installed maintenance command). No media/catalog/code changes occurred, so no rebuild or media acceptance is claimed.

## Successor and blocking boundary

Both read-only audits are incorporated; the review stage is closed with no deletions. No cleanup successor has accepted work, and no cleanup execution is started by this report. Concurrent source edits belong to their unidentified author, not this audit. The desktop producer owns canonical-document integration and any production path migration; Andre owns destructive/global cleanup authorization. Small reversible navigation fixes should be integrated as one reviewed change set once those source edits are assigned. For removal, first require a per-path keep/remove/migrate manifest, recovery method, consumer checks and confirmation that concurrent tools are idle. This audit is not approval to delete media, caches in use, runtime state, or shared installations.
