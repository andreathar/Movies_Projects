# Structural inventory and retirement decisions · 17 October 2026

Full-tree metadata only, no symlink traversal; logicalBytes regular file payload, allocatedBytes includes directory/symlink blocks; hardlinks counted per path. No credentials or runtime contents read.

Sizes below were captured before continuation changes. Root and film/site tables overlap by design; do not add them together. Logical bytes measure regular-file payload; allocated bytes include directory blocks. No age/text-match rule was used to decide retention.

## Every root directory

| Path | Files | Logical bytes | Allocated bytes | Role / retirement evidence |
|---|---:|---:|---:|---|
| `.agents/` | 6 | 29,552 | 65,536 | Vendored Kling skill and plugin manifest; skill/client links resolve here. |
| `.claude/` | 21 | 136,989 | 200,704 | Registered hook handlers/helpers and linked skill; preserve safety/client surface. |
| `.codex/` | 1 | 105 | 8,192 | Existing tracing/client configuration. |
| `.git/` | 1,857 | 1,951,611,037 | 1,962,987,520 | Git, LFS originals and worktree relationships; never prune in this cleanup. |
| `.github/` | 2 | 4,357 | 20,480 | Client instructions referenced by existing tooling. |
| `.hermes/` | 0 | 0 | 12,288 | Skill and production-plan symlinks; bindings, not media copies. |
| `.mypy_cache/` | 371 | 15,396,081 | 16,306,176 | Regenerable type-check cache; no exclusive-owner/idle evidence, retain. |
| `.opencode/` | 3,651 | 54,895,220 | 65,409,024 | Client configuration and installed dependencies; preserve user runtime. |
| `.ruff_cache/` | 5 | 505 | 28,672 | Shared checker cache; no cleanup during potential active use. |
| `.serena/` | 17 | 2,850,629 | 2,912,256 | Deliberate navigation memories, configuration and symbol caches; retain. |
| `.venv/` | 8,000 | 511,751,093 | 534,401,024 | Existing Python runtime/dependencies; validators and tests use it. |
| `.vllm/` | 1 | 286,735 | 294,912 | Existing runtime log/configuration; no retention authority to erase. |
| `.vscode/` | 1 | 266 | 8,192 | Workspace/editor test and environment settings. |
| `agents/` | 19 | 68,342 | 118,784 | Registry/briefs and seven derived adapters consumed by frontend. |
| `docs/` | 71 | 1,354,930 | 1,536,000 | Current contracts/manuals, historical procedures and preflight tools. |
| `drafts/` | 35 | 14,781 | 212,992 | Active visualRestart scope plus explicit workflow rehearsal; not production garbage. |
| `inbox/` | 411 | 495,322,349 | 496,189,440 | Original photos/voice, approved and unapproved intake/provenance. |
| `memory/` | 2 | 1,248 | 12,288 | Required root project-memory index. |
| `projects/` | 1,766 | 1,551,395,691 | 1,556,054,016 | Canonical episode pipeline, media, approvals, provenance and handoffs. |
| `reports/` | 371 | 5,651,298 | 6,713,344 | Historical validation, backups and audits; hash-linked evidence. |
| `scripts/` | 54 | 893,912 | 1,015,808 | Documented/dynamic entry points, local renderers and producer wrappers. |
| `series/` | 2 | 10,940 | 24,576 | Reusable framework consumed by workflow/continuation tooling. |
| `shared/` | 11 | 25,261 | 65,536 | Capabilities and active request/handoff/continuation contracts. |
| `sites/` | 51,068 | 1,002,984,232 | 1,170,558,976 | Separate dirty frontend repository with runtime source and derived exports. |
| `skills/` | 3 | 9,355 | 40,960 | Project skill, registry and links to canonical shared sources. |
| `tasks/` | 1 | 1,765 | 8,192 | Required root navigation consumed by frontend. |
| `tests/` | 36 | 630,786 | 712,704 | Active stdlib test suite discovered by parley_verify; retain verification. |

Root files (AGENTS, workspace, README/START_HERE/CLAUDE, pyproject, lock/attributes/ignore and client configs) are current contract/configuration/navigation surfaces. Credential contents were not read. `.hermes` regular-file count is zero because it is a symlink view, not an unused empty folder.

## Immediate episode directories

| Path under projects/andre-time-travel | Files | Logical bytes | Allocated bytes | Consumers / retention |
|---|---:|---:|---:|---|
| `02_references/` | 176 | 404,568,549 | 405,041,152 | Catalog/production-plan/atlas consumers; originals, approved/pending and synthetic roles remain distinct. |
| `memory/` | 10 | 98,126 | 131,072 | STATE/session/mistake/decision history used by resume/lint. |
| `03_bibles/` | 29 | 473,900 | 544,768 | Continuity and scene proposals with review provenance; delivered versions retained. |
| `05_storyboard/` | 379 | 305,550,534 | 306,483,200 | Active visual plan/atlas sources, shot list, delivered v1–v3 atlases and keyframes. |
| `08_edit/` | 140 | 96,608,288 | 97,046,528 | Timelines, reviews, delivered candidate picture and hash snapshots. |
| `00_brief/` | 45 | 631,365 | 757,760 | Approvals/decisions/research: manage.py, exporters and release validators. |
| `04_audio/` | 46 | 21,036,654 | 21,184,512 | Voice provenance, tests, stems, pilot/animatic consumers. |
| `01_script/` | 10 | 63,705 | 98,304 | Canonical script/CSV: consistency validation, atlas, dialogue and timing consumers. |
| `06_pilot/` | 13 | 9,385,832 | 9,428,992 | Actual pilot and speech-test evidence. |
| `07_generations/` | 719 | 680,288,016 | 682,156,032 | Requests, responses, originals, results and both canonical experiment batches. |
| `agents/` | 70 | 1,724,886 | 1,875,968 | manage.py loads handoff/supersession chain; producer reviews stay pending. |
| `tasks/` | 33 | 1,187,044 | 1,273,856 | Board/specs/plans/workflow map; exporters derive statuses. |
| `docs/` | 29 | 335,328 | 401,408 | Film direction, historical production-plan.md required by validator, review/procedure docs. |
| `logs/` | 17 | 239,674 | 290,816 | Hook/provenance records; live hook helper writes logs here. |
| `09_delivery/` | 46 | 28,989,594 | 29,110,272 | Versioned poster/caption/QC/stem outputs; file existence is not final acceptance. |

Immediate episode files manifest.json, asset-registry.csv and credit-ledger.csv are validated canonical records. Required empty `.gitkeep` stage directories are enforced by workspace.json.requiredDirectories. Do not remove them based on zero media count.

## Frontend immediate directories

| Directory under sites/movies-demandas | Files | Logical bytes | Allocated bytes |
|---|---:|---:|---:|
| `dist/` | 74 | 2,213,603 | 2,506,752 |
| `node_modules/` | 50,392 | 996,875,115 | 1,161,338,880 |
| `scripts/` | 25 | 113,106 | 176,128 |
| `app/` | 50 | 168,060 | 323,584 |
| `examples/` | 2 | 2,165 | 32,768 |
| `hooks/` | 1 | 565 | 8,192 |
| `qa/` | 5 | 178,924 | 192,512 |
| `public/` | 4 | 2,104 | 20,480 |
| `.github/` | 1 | 3 | 16,384 |
| `.sites-runtime/` | 5 | 969,649 | 999,424 |
| `.wrangler/` | 13 | 226,332 | 303,104 |
| `drizzle/` | 3 | 1,644 | 20,480 |
| `data/` | 2 | 195,946 | 204,800 |
| `.superpowers/` | 1 | 2 | 12,288 |
| `.openai/` | 1 | 91 | 8,192 |
| `components/` | 69 | 216,565 | 409,600 |
| `vendor/` | 2 | 17,104 | 24,576 |
| `docs/` | 1 | 75,649 | 90,112 |
| `db/` | 2 | 722 | 12,288 |
| `.vinext/` | 1 | 202 | 12,288 |
| `build/` | 5 | 17,332 | 32,768 |
| `tests/` | 19 | 69,661 | 118,784 |
| `.tsupgrader/` | 0 | 0 | 8,192 |
| `.git/` | 356 | 632,901 | 2,555,904 |
| `.next/` | 1 | 1,046 | 12,288 |
| `lib/` | 17 | 49,947 | 102,400 |

`app/`, `components/`, `lib/`, `scripts/`, `build/` and `tests/` are maintained sources. In particular, `vite.config.ts` imports modules from `build/`; its name does not mean disposable build output. `dist/`/`.next/` are reproducible build outputs, while `.sites-runtime/` and `.wrangler/` include runtime ownership/state. node_modules and client settings are existing dependencies, not obsolete source. Optional examples/d1 and API tests are documented starter capabilities; no complete caller/feature retirement was established.

## Actual obsolete/unused candidates and disposition

| Candidate | Evidence | Decision |
|---|---|---|
| Unused math import in build_galileo_animatic.py | Whole-source/AST check: no load/reflection | Removed 12 source bytes in phase1; no behavior/performance claim |
| Wrong v2 gallery presentation joins | Differently ordered arrays zipped; corrected by verified asset IDs and source hashes | Current navigation now uses v3 metadata-only presentation; preserve v1/v2 historical evidence byte-for-byte |
| Stale export HEAD envelopes | Full generated semantic comparison was empty; snapshots cited629c23d while current HEAD35f8447 | Refresh current derived envelopes and reviewed gallery navigation only; preserve dirty originals in external backup |
| Stale active plan/private-remote/CLI/count/build references | workspace.json, VERSION_CONTROL, current capabilities and catalog prove current sources | Correct navigation, label snapshot counts/version references as historical; retain provenance |
| scripts/andre_cinematic_spec.json | Unique historical R2 prompts, source paths and approval IDs; no filename caller alone proves nothing | Retain historical request evidence |
| Generated adapters and .agents/agents surfaces | Registry generator and frontend consume them; skill surfaces are linked | Retain; no consolidation by directory name |
| .mypy_cache/.ruff_cache/Python caches | Reproducible but shared tooling/agents may use them | Do not remove: active/exclusive ownership not established |
| dist/.next outputs | Existing local build/start paths consume them; reproducible artifacts | Retain for usable project; no meaningful benefit demonstrated by removing |
| Duplicate media / delivered atlas snapshots | Exact bytes can serve distinct original, curated, request and review identities | Retain; no path-role migration or deletion justified |
| Historical handoffs, reports, prompt/results, Serena notes | Explicit hash/provenance and resume consumers | Retain; supersession changes current inventory only, never approval/ingestion |

**No entire folder or complete source/media file was proven safe to remove.** The structure itself supports the production pipeline. This delivery fixes demonstrable live defects and improves navigation; it does not manufacture file-count reductions. No permanent deletion, cache purge or duplicate media tree was created.
