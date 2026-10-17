Scope: independent, read-only documentation audit for `andre-time-travel` and workspace entry points. I’ll compare current files and any existing worktree consolidation, without changing files or treating historical material as unused merely because it is old.

The main issue is competing authority labels, not proven disposable files: the README still calls the historical plan canonical, and the linked visual bible repeats retired wardrobe rules. The earlier consolidation report is absent from both registered lane worktrees, but I recovered it from Git commit `bed91ad` and compared its findings with current files. Current status/lint pass, with warnings; they do not catch these prose conflicts.
## Audit result

**Prioritize authority labels and navigation—not deletion.** I found stale instructions and historical documents presented too actively, but no file proven safe to delete.

Scope: independent read-only auditor; active episode `andre-time-travel`. Baseline Git HEAD: `35f84474377f86876fcf691dee16036b8601a495`.

### Existing consolidation reused

The report requested by `projects/andre-time-travel/tasks/plans/project-cleanup-plan-v1.md:17` is absent from both registered lane worktrees. I recovered and read it from:

`bed91ad:docs/consolidation-2026-10-09/consolidation-report.md`

Its authority map is at lines 13–27; its README finding at line 137 remains unresolved. Current versions of its six edited documents differ from that commit—**do not replay its patches wholesale**.

Report SHA-256: `2f5a3b952e5c672d74e7e60404ffa2a2c617f3b1d38556a6be3719576531cf6b`.

## Findings and bounded replacements

### 1. Wrong canonical-plan entry — high confidence

`README.md:14` calls the historical Markdown plan:

> `canonical production plan`

But `projects/andre-time-travel/docs/production-plan.md:3` labels itself **DERIVED**, and line 5 retains a Hermes-specific delegation instruction.

Current authority is explicit:

- `workspace.json:17` selects `projects/andre-time-travel/05_storyboard/source/production-plan.json`.
- `docs/PRODUCTION_PLAN.md:7` defines that source’s responsibility.
- `projects/andre-time-travel/05_storyboard/source/production-plan.json:808–828` defines `activeBaseline` and first speaking shot `G-P04`.

**Recommendation:** point README’s current-plan entry to the workspace-selected JSON and its operational documentation. Retain the old Markdown plan as historical supporting material.

Also add the current visual-plan source to `START_HERE.md:33–35`; its editing table currently exposes atlas/manifest/shot-list sources without the newer canonical visual plan.

### 2. Linked visual bible contradicts current decisions — high confidence

`START_HERE.md:17` prominently links `docs/master_production_visual_bible.md`.

That document contains:

- `docs/master_production_visual_bible.md:6`: identity, wardrobe and screenplay “remain unapproved.”
- `docs/master_production_visual_bible.md:30,69`: charcoal shirt/navy blazer as invariant wardrobe.
- `docs/master_production_visual_bible.md:31,93`: exclusive eyes/below-neck coverage.

These conflict with or omit subsequent authority:

- `projects/andre-time-travel/00_brief/decisions/D02-wardrobe.json:10`: grey pinstripe jacket/striped white shirt; navy/charcoal retired.
- `projects/andre-time-travel/00_brief/approvals.json:4–13`: several creative gates are true, while others remain false.
- `projects/andre-time-travel/memory/STATE.md:19`: current behind-the-figure coverage and scene-specific reactions.

**Recommendation:** label this as a historical R1/R2 review compilation, not a governing bible. Preserve its images and text; route current decisions to decision records and the production plan.

### 3. Startup consolidation is incomplete — high confidence

The primary entry points are mostly corrected:

- `AGENTS.md:17` declares STATE the single resume surface.
- `START_HERE.md:1,26` defers to AGENTS.
- `CLAUDE.md:5` imports AGENTS.

Remaining competing or stale instructions:

| Evidence | Recommended replacement |
|---|---|
| `projects/andre-time-travel/memory/STATE.md:9–13` repeats a read sequence containing old checkpoints | Link to AGENTS; make checkpoint consultation explicitly task-dependent |
| `docs/OPERATIONS.md:3–10` offers another operating sequence; line 8 allows canonical-record updates without naming the producer | Replace overlapping rules with AGENTS/LOCAL_AGENT_HANDOFF pointers |
| `docs/MEMORY_AND_AGENTS.md:7` separates producer and coordinator write authority | Align terminology with the identified producer/coordinator in `AGENTS.md:7` |
| `CLAUDE.md:23` references nonexistent “AGENTS.md step 7” | Link to the current session-start section |
| `CLAUDE.md:36–37` demonstrates rendering into existing atlas v3 | Use an unused revision placeholder; `START_HERE.md:19` explicitly says v3 already exists |

### 4. Historical checkpoints still invite obsolete decisions — high confidence

`projects/andre-time-travel/docs/checkpoint-2026-10-09-galileo-retomada.md:8` presents a general 1.5–2-second eye rule.

`projects/andre-time-travel/03_bibles/scene-bibles/scene-bibles-v3-integrada.md:41` similarly specifies a universal range and maximum, although lines 3 and 38 explicitly keep the document/D19 proposed.

Current qualification:

`projects/andre-time-travel/memory/STATE.md:19` says the two-second choice belongs to the Galileo candidate, **not a universal rule**.

**Recommendation:** retain these as historical/proposed documents; prevent their timing language from becoming an implicit production default. Do not promote the integrated proposal merely because its filename says “integrada.”

### 5. Scene-bible timing still reproduces the motivating-line problem — high confidence

`projects/andre-time-travel/03_bibles/scene-bibles/galileo.md:46–47` places:

```text
G-05: eye reaction at “settle a question”
G-06: “…Silencing a person does not settle a question.”
```

The canonical wording is different at `projects/andre-time-travel/01_script/dialogue-lines.csv:14`:

```text
Your observations. And one lesson from your trial that people keep relearning:
silencing a man does not settle a question.
```

The current plan explicitly places reaction after the whole line at `projects/andre-time-travel/05_storyboard/source/production-plan.json:742`.

**Recommendation:** a producer-integrated new bible revision using line IDs, current timing and verified input hashes. Preserve existing versions. The integrated proposal’s line-ID approach is useful (`projects/andre-time-travel/03_bibles/scene-bibles/scene-bibles-v3-integrada.md:14`), but its other proposed rules still require reconciliation.

### 6. Genghis wardrobe needs scope labels, not global replacement — high confidence

- `projects/andre-time-travel/03_bibles/scene-bibles/genghis.md:32` describes lamellar armour.
- `projects/andre-time-travel/03_bibles/detail-planning/art-choices-v1.md:9` selects no armour for the new studies.
- `projects/andre-time-travel/00_brief/decisions/D20-detail-studies-art.json:18` limits D20 to new built-in detail studies.

**Recommendation:** identify old-armour references versus D20 studies explicitly. Do not rewrite historical references or treat D20 as approval for every existing take.

### 7. README publication statement is stale — high confidence

`README.md:41` says there is no remote or GitHub publication.

`docs/VERSION_CONTROL.md:3–5` records private `origin`, tracking and the authorized initial publication.

**Recommendation:** replace the duplicated status paragraph with a short link to VERSION_CONTROL. This grants no new publication authority.

## Dead-link results

Checked **218 Markdown files**, covering root entry documents, `docs/`, and episode Markdown:

- **187 local Markdown links:** three missing targets.
- **28 image links:** two intentional `<Base64-Image-Removed>` placeholders in preserved research snapshots.

Missing links:

1. `docs/archive/AGENTS-full-2026-10-13.md:46` → `docs/SHARED_MEDIA.md` resolves incorrectly from the archive directory.  
   **Treatment:** preserve archived bytes; provide navigation outside the snapshot.

2. `projects/andre-time-travel/08_edit/reviews/detail-planning-v2/source-historical-review.md:37` → `historical-review-evidence.json`.  
   Existing relocated evidence is `source-historical-review-evidence.json` in that directory.

3. The same line links a missing `2026-10-09-editor-historical-details-review-v1.json`. It was not found in the three checked handoff directories.  
   **Treatment:** record unresolved provenance; do not invent a replacement.

Importantly, `projects/andre-time-travel/08_edit/reviews/detail-planning-v2/producer-review.md:14` already explains that copied review references describe the original lane layout. Prefer a companion navigation note over altering preserved source evidence.

## Logical archival candidates

Retain paths and provenance; remove these from current-instruction routes:

- `projects/andre-time-travel/docs/production-plan.md:3–5,46,75` — historical plan and obsolete operational assumptions.
- `docs/master_production_visual_bible.md:6,30,69` — historical visual compilation.
- `projects/andre-time-travel/docs/budget-plan-v2.md:3,7,22–23` — dated balance, pre-video assertion and completed “next batch.”
- `projects/andre-time-travel/docs/decision-sheet-andre-v1.md:3,9–20` — old decision questionnaire; current decisions must come from recorded IDs.
- `projects/andre-time-travel/docs/status-report-2026-10-09.md:3,15–16` — explicitly dated snapshot; retain, not current status.

The cleanup inventory itself is historical: `docs/CLEANUP-INVENTORY-2026-10-09.md:21` says Kling’s registry source remains Hermes, whereas `skills/registry.json:8–9` now records `.agents/skills/kling-cli` / `project_vendored`.

## Checks and handoff

Actually performed:

- Read contract, requested cleanup inputs, recovered consolidation and relevant current documents/records.
- Inspected Git HEAD, registered worktrees and scoped diffs/status.
- Ran local `manage.py status`, `resume`, `lint`: **status OK; zero hard lint findings; ten advisories**.
- Status reported **three**, not the four historically documented skill-hash warnings.
- No unit tests, services, provider calls, media playback or comprehensive dependency/deletion proof.

**No files changed by this auditor.** Final status showed concurrent `sites/movies-demandas` changes and a new `reports/2026-10-17-cleanup-audit/` directory; neither was created or inspected by me.

**Next owner: parent producer.** Integrate a bounded navigation/banner correction first, preserve historical artifacts and hashes, then assign bible reconciliation separately. No deletion, move, commit or acceptance is recommended as an implicit next action.