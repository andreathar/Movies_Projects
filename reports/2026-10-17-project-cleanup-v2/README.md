# Cleanup implementation and structure audit — 17 October 2026

The two incorrect current gallery associations are fixed, and both current frontend exports now pass freshness checks. The complete root/film/frontend inventory and retirement evidence are in [STRUCTURE.md](STRUCTURE.md) and [checks.json](checks.json). This continues the [initial bounded cleanup](../2026-10-17-project-cleanup-v1/README.md), whose report and backups remain historical evidence.

## Corrected current presentation

[Experiment gallery v3](../../projects/andre-time-travel/07_generations/downloads/2026-10-17-element-experiments-v3/index.html) and [current lessons/reconciliation](../../projects/andre-time-travel/docs/kling-element-experiments-20261017-v3.md) replace only the active presentation links. The historical v2 builder zipped observations and analyses in different orders. The maintained `scripts/experiment_gallery.py` joins manifest resources, analysis and observations by stable asset ID, verifies source path/hash and frame-sheet coverage, and links the matching video, audio, ASR and sheets. Six regression tests cover ordering, missing/duplicate IDs, path/hash contradictions, frame counts and HTML media associations. `--check` reproduces the metadata without writing.

The original review observations already had the correct IDs and remain unchanged. Independent inspection of the two opening sheets confirmed broad setting/cast associations; no full playback/listening or new artistic review is claimed. Independent read-only verification of the installed page confirmed all five cards, all 45 sheets/1,636 represented frames, four audio/ASR pairs, all five costume-resource links and all 114 local HTML links. 269 historical gallery/evidence/original paths still match the prior inventory hashes. V1/V2 and all original media remain byte-for-byte preserved; v3 is a metadata-only revision and contains no copied/generated media.

## Export reconciliation without losing concurrent work

Before changing navigation, a reproducible read-only evaluation of both actual exporters proved zero semantic payload differences. Their stored Git provenance cited `629c23d`, while current main is `35f8447`. The exporter intentionally treats that envelope as stale even with matching source hashes/content fingerprints. Current dirty JSON and exporter source bytes were backed up, not replaced with Git versions.

Both snapshots were regenerated through the existing local exporters. Production changed **only** `collectedAt` and `provenance.repositoryHead`; its contentVersion remains `ce387212f9e78f723a1c11cde805caa705f70760494b05a8e29c858672080219`. Workspace changed only those envelope fields, the two reviewed navigation paths, its content fingerprint and one added `gallery.json` source/hash. Exact JSON difference paths are recorded in checks.json. No board, approval, asset registry, film plan, ledger, persisted product workspace, ingestion or dispatch changed. All other preexisting frontend source modifications/untracked files are retained. One mutable frontend runtime log changed during the continuation; it was retained, is excluded from source-integrity assertions and is not part of either rollback manifest. No log was cleaned or restored. The final launcher read reports running=false/ready=false.

README/START_HERE point here. SHARED_MEDIA now labels 318 as a historical count and asks the validator for the current count rather than maintaining another total. The manual index exposes guides 19/20 and 16 tests, distinguishes historical CLI 0.2.1 from recorded 0.2.3, and preserves dated snapshots. Upstream skill telemetry 0.2.1 remains intentional.

## Structure: what can actually be retired

Full metadata tables cover every root directory, all 15 immediate film directories and frontend immediate directories, with regular-file counts, logical/allocated bytes and consumers. The largest retained areas before continuation were `.git`≈1.96GB allocated, frontend/dependencies≈1.17GB, film sources≈1.56GB, Python environment≈534MB and inbox≈496MB. Nested tables overlap; do not sum them as independent storage.

**No whole directory or complete source/media file was proven safe to remove.** The only demonstrated unused implementation detail was the 12-byte math import removed in phase1. The numbered pipeline, required empty stage slots, shared skill bindings, generated adapters, delivered atlases, historical prompt/results, pending handoffs and original/curated media have direct consumers or provenance obligations. Cache/build folders are regenerable but shared/runtime use was not proven absent, and removing them would not make this working project more usable. `sites/movies-demandas/build/` is imported source. Optional D1 examples remain documented capabilities, not proven dead scaffolding. This conclusion follows dependency checks, not age, filename or zero textual matches.

No files were archived or permanently deleted; no net storage, performance, runtime-memory or token saving is claimed. New metadata/report/code bytes are measured in the external manifest. No duplicate media tree was created. Existing concurrent `reports/2026-10-17-cleanup-audit/` and this task's first report remain untouched.

## Validation and handoff continuity

Targeted checks pass: six gallery regressions, deterministic gallery --check, both exporter --checks, five existing export tests and check:data. Follow-up full checks passed **251 Python tests, 16 manual-tool tests and 87 frontend tests**, frontend lint, type check and local build. Workspace validate/lint/resume, assets, production-plan --verify-media and seven-file agent catalog --check pass. The new schema2.0 handoff passes with errors=[]/advisory=[].

The new maintenance-v2 handoff carries the **entire** previous 429-file runtime-v3 inventory and phase1 cleanup inventory, preserving attribution, historical claims, original pending review/ingest states and unresolved obligations. Only intentionally changed current hashes are reconciled. Both prior handoff files remain unchanged and pending; supersession affects the current inventory, and grants no ingestion or creative acceptance. Prior claims are explicitly inherited evidence, not tests repeated here. Visible blockers/next actions retain the missing fight/history association, human playback/listening and film pricing/identity/table/wardrobe gates. The provenance-only export blocker is resolved by the recorded refresh. The obsolete historical statement that the preview was running is not presented as current; the launcher was stopped and no service was started/restarted.

Remaining uncertainties are film/source-history gates, not blockers to these implementation fixes: candidate fight ProduceID versus web history, full playback/listening, table `_4_alt` versus D04 `_2`, wardrobe/identity/voice and V4 price/quality/FPS/Flash. G-IN/G-OUT stay composition-only approved; the five other baseline references remain pending.

## Backups and selective recovery

External phase2 backups, exact before/after hashes, commands, JSON diffs, full metadata structure inventory, rollback manifest and recovery instructions:

`/home/athar/Documents/Codex/2026-10-17/task/continuation-2026-10-17/`

Phase1 originals remain at the sibling `audit-2026-10-17/`. Recovery is selective and hash-guarded: phase2 restores the current dirty bytes captured before this continuation, not Git HEAD versions. Added metadata/code/report/handoff files are moved to an external rollback archive instead of deleted. Restore phase2 before phase1 if intentionally rolling back the complete task. Both phase2 and phase1 backups remain intact. The phase2 selective rollback dry-run passes for all 17 owned paths; no rollback was applied. Final hash comparison preserves all 1,125 baseline media/PDF/ZIP files (2,036,752,866 bytes), all 13 symlinks, registered worktree states, main HEAD, canonical records and the separate concurrent audit. No commits, pushes, provider calls, uploads, paid/media generation, permissions changes or service restarts occurred.
