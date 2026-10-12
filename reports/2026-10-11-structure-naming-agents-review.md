# Structure, naming, and agents review

Date: 2026-10-11

Implementation note: this file is the review, not a claim that the findings were already fixed. The same branch applies the non-canonical changes. Producer-owned files (`AGENTS.md`, `CLAUDE.md`, `workspace.json`, `00_brief/approvals.json`, `memory/STATE.md`, `memory/session-log.json`, `memory/mistakes.jsonl`) are proposed in `reports/2026-10-11-canonical-records.patch` because the canonical-guard hook refused those writes from this session.

## Scope

Read-only review of folder structure, naming, and agent settings in Movies_Projects, active film `andre-time-travel` (*The Table Between Centuries*). This report does not change media, approvals, manifests, the board, scripts, skills, or workflow rules. It does not record new approvals, quotations, charges, or job results.

Operating rules stay in `AGENTS.md`. This report only points at contradictions that make a clean resume unreliable.

Review base: `e1b5eb43cf7c76bb3fd837363ea818610951fd48` (`origin/main` at review time). Local `main` was two commits behind; it was fast-forwarded before this branch was cut. Those two commits are part of the findings below.

## Method

Read:

- `workspace.json`, `projects/andre-time-travel/memory/STATE.md`, `manifest.json` (header, chapters, budget, `approvals`), `tasks/board.json` (through T12, then via `resume`), `00_brief/approvals.json`
- `skills/andre-time-travel/SKILL.md`, `skills/registry.json`, `skills/README.md`, `skills-lock.json`
- `agents/registry.json`, `agents/README.md`, `agents/*.md`, `projects/andre-time-travel/agents/bindings.json`
- `docs/PARLEY_PROTOCOL.md`, `docs/COORDINATOR_PROTOCOL.md`, `docs/REPEATABLE_WORKFLOW.md`, `docs/VERSION_CONTROL.md`, `docs/LOCAL_AGENT_HANDOFF.md`, `docs/FOLDER_STRUCTURE.md`, `docs/WORKSPACE.md`, `docs/MEMORY_AND_AGENTS.md`, `docs/CLEANUP-INVENTORY-2026-10-09.md`, `docs/PLAN-parley-integration-v1.md` (status header only)
- `START_HERE.md`, `shared/templates/agent-handoff.json`, `shared/templates/agent-handoff-v2.json`, `memory/projects.json`, `projects/andre-time-travel/memory/decisions.json` (banner), decision files `D16` and `D20`
- `.claude/settings.json` and the opening of `.claude/hooks/canonical-guard.py` and `kling-preflight.py`
- `.agents/plugins/agent-parley/plugin.json`
- One placeholder skill body: `/home/athar/.hermes/skills/creative/film-editing-qc/SKILL.md` (outside the repo; created so links resolve)

Commands actually run:

| Command | Exit | Outcome |
|---|---|---|
| `git fetch origin main` then `git merge --ff-only origin/main` | 0 | Fast-forward `5dbd641` → `e1b5eb4` |
| `.venv/bin/python scripts/manage.py status` | 2 | `{"status":"error","errors":["duplicate agent role IDs"],"warnings":[],"projects":[]}` |
| `.venv/bin/python scripts/manage.py validate` | 2 | Same error. Skill checks never run. |
| `.venv/bin/python scripts/manage.py lint` | 2 | Two hard hash mismatches on `2026-10-11-claude-repo-cleanup-v1.json` for `agents/registry.json`. Advisories: duplicated approval flags (R06), that handoff not ingested, session-log offsets `+0000` and `-0300`. |
| `.venv/bin/python scripts/manage.py resume` | 0 | Digest still prints. Task counts: 7 completed, 3 in progress, 11 blocked. `andreOnlyGates` is `[]`. Embedded lint: 2 hard, 3 advisory. Balance snapshot 6981, `isLive` false, observed 2026-10-09. |

Not run: unit tests, `workflow.py verify`, atlas rebuild, `scripts/parley_setup.sh`, Kling CLI, LFS fetch, playback.

## Current shape

`workspace.json` names one film, `projects/andre-time-travel`, and lists 69 `requiredDirectories`. Every required directory exists. The numbered pipeline `00_brief` through `09_delivery` is present. Many of those directories contain only `.gitkeep`.

Live creative state sits beside that scaffold and is not what the required-directory list describes: `00_brief/decisions/`, `05_storyboard/source/atlas.json`, three atlas revisions, `08_edit/reviews/`, `03_bibles/detail-planning/`, and `02_references/keyframes/andre/`.

Workspace-level roles live in `agents/`. Episode deliveries live in `projects/andre-time-travel/agents/handoffs/` (34 JSON files). Skills are a mix of the project-local `skills/andre-time-travel/` and symlinks. Mirrors exist under `.hermes/skills/`, `.claude/skills/`, and `.agents/skills/`.

`manage.py status` and `validate` do not currently describe the film. They stop on a duplicate role id introduced when two coordinator registrations were merged.

## Findings

### 1. Duplicate `coordinator` id blocks validate and status

**What is true.** `agents/registry.json` contains two role objects with `"id": "coordinator"` (first object near the top of `roles`, second object at the end). `scripts/manage.py` rejects that with `duplicate agent role IDs` before it checks briefs, skills, or the film. `status` therefore returns an empty `projects` list.

The two objects are not copies:

| | First object | Second object |
|---|---|---|
| Origin | `5dbd641` inserted it at the start of `roles` | `52a5355` appended it; merge `e1b5eb4` kept both |
| `skills` | `["coordinate"]` | `[]` |
| Extra authority fields | `dispatchAuthority: true`, `notes` | `canonicalWriteAuthority: false`, `note` |
| `paidSubmissionRequiresApprovedShot` | `false` | `true` |

`projects/andre-time-travel/agents/bindings.json` lists nine roles and omits `coordinator`. `agents/README.md` and `docs/MEMORY_AND_AGENTS.md` still say seven role briefs. There are ten role brief files plus `agents/README.md`. `agents/producer.md` is still titled "Producer / coordinator".

**Why it hurts.** Session start step 5 cannot show pending state. Any tool that builds a map from role id will keep one coordinator and drop the other, and the two definitions disagree about dispatch and canonical writes. The producer title still claims the coordinator name the new role was added to separate.

**Do now.** None inside the registry. Editing it changes authority fields.

**Needs producer decision.** Keep one `coordinator` object. Decide which fields survive (`dispatchAuthority`, `canonicalWriteAuthority`, `skills`, `paidSubmissionRequiresApprovedShot`). Point `bindings.json`, `agents/README.md`, and `docs/MEMORY_AND_AGENTS.md` at that single list. Rename the producer brief title so only one role is called coordinator.

### 2. The coordinator skill link is broken, and the brief mislabels decision IDs

**What is true.** The first registry object names a skill `coordinate`. That name is not in `skills/registry.json`. The link chain is broken:

- `skills/coordinate` → `../.agents/skills/coordinate`
- `.agents/skills/coordinate` → `../plugins/agent-parley/skills/coordinate`
- `.agents/plugins/agent-parley/skills` → `../../../../agent-parley/plugins/agent-parley/skills` (outside the repo; target missing)
- `.claude/skills/coordinate` points at the same broken `.agents` link

`.agents/plugins/agent-parley/plugin.json` says the skill is a live symlink to `/mnt/data/Projects_SSD/agent-parley/...` at install commit `5fd888f`. `agent-parley` is not on `PATH` in this environment.

`agents/coordinator.md` tells the role to use the `coordinate` skill, then in the example sequence says it updates `tasks/board.json`, then later says it never writes the board. The same brief lists "D16 (likeness approval)" and "D20 (final picture)". On disk, `00_brief/decisions/D16-galileo-pilot-v2-phase-a.json` is a relayed Phase A spend ceiling of 23 credits, and `D20-detail-studies-art.json` is a producer art selection for detail studies, with likeness and final picture explicitly not approved. `D17`–`D19` files are absent. `STATE.md` already says those three are proposed topics only.

**Why it hurts.** A coordinator session cannot load the skill it is told to use, and `validate` will not notice, because the skill is outside the registry. The brief can send a dispatcher after the wrong gate.

**Do now.** Correct the D16/D20 labels in `agents/coordinator.md` to match the decision files, and remove the example step that writes `board.json`. That aligns the brief with the later "May not" section and with `docs/PARLEY_PROTOCOL.md`. It does not grant dispatch authority.

**Needs producer decision.** Whether `coordinate` is required. If it is, vendor it or record a registry entry whose target exists on a clean machine. If it is not, remove it from the role and from `agents/coordinator.md`. Do not point the registry at the broken `/mnt/data` path.

### 3. Handoff entry points disagree, and the newest handoff fails lint

**What is true.** `AGENTS.md` requires `shared/templates/agent-handoff-v2.json`. Role briefs and `.claude/hooks/handoff-check.py` cite v2. These still tell the agent to copy `shared/templates/agent-handoff.json` (schema 1.0):

- `CLAUDE.md`
- `docs/LOCAL_AGENT_HANDOFF.md`
- `docs/REPEATABLE_WORKFLOW.md` (local-edit step 2)
- `agents/README.md`

Of 34 files in `projects/andre-time-travel/agents/handoffs/`, 32 are `schemaVersion` `1.0` and 2 are `2.0`:

- `2026-10-10-claude-parley-implementation-v1.json` — ingest `ingested`
- `2026-10-11-claude-repo-cleanup-v1.json` — ingest `pending`, `reviewStatus` `pending_producer_review`

`lint` hard-fails on that pending file: `changedFiles` and `claims` SHA-256 for `agents/registry.json` do not match the file after merge `e1b5eb4`. The handoff was written against the single coordinator row from `52a5355`. The merge then changed the registry again.

`resume` still lists the handoff as recent and pending. `STATE.md` does not mention it.

**Why it hurts.** A new session can follow `CLAUDE.md` or `LOCAL_AGENT_HANDOFF.md` and deliver a v1 handoff that `AGENTS.md` no longer accepts. The one delivery that tried to register the coordinator cannot pass `lint` until a producer reconciles the hash. `resume` exiting 0 does not mean the workspace is clean; the digest only counts lint errors.

**Do now.** Change the four v1 citations above so they name `agent-handoff-v2.json`, matching `AGENTS.md`. Leave historical v1 handoff files in place.

**Needs producer decision.** Reconcile or supersede `2026-10-11-claude-repo-cleanup-v1.json` after the registry has one coordinator. Ingest is a producer action (`manage.py handoff ingest` is not part of this report). Do not rewrite the stored hashes to match a file the handoff did not actually deliver.

### 4. Resume pointers still advertise superseded or empty gate lists

**What is true.**

- `AGENTS.md` says decisions are cited only from `00_brief/decisions/`. `projects/andre-time-travel/memory/decisions.json` is marked `status: superseded` and uses `LEGACY-D01`–`LEGACY-D05`. `memory/projects.json` still sets that file as the film's `decisions` path.
- `resume` reads `andreOnlyGates` from `approvals.json`. That key is absent, so the digest reports `[]`. The open relay is `D16` plus the prose list in `STATE.md`.
- `manifest.json` `budget.verifiedBalanceSnapshot` is 6981 on 2026-10-09 with `snapshotIsLiveBalance: false`. `STATE.md` records a later read of 5813 at 2026-10-09T12:28:25-03:00 and says to refresh before paid work. `resume` surfaces 6981.
- `manifest.json` `approvals` matches `00_brief/approvals.json` `creativeApprovals` today. `lint` still warns that the flags are duplicated (R06). `STATE.md` already notes the duplicate.
- `STATE.md` is 65 lines and still says four shared-skill hash warnings from `validate` are known, and that memory/handoff phases await design review. On this commit, `validate` errors on the duplicate role before any skill warning. Handoff v2, `resume`, and `lint` already exist. This report did not line-check every historical sentence in `STATE.md`.
- `skills/README.md` says the workspace is not Git-initialized. `docs/VERSION_CONTROL.md` documents `origin` and the 2026-10-10 publication.

**Why it hurts.** The shortest resume tools (`resume`, `memory/projects.json`, the coordinator brief) do not name the gate that actually blocks spending. Two balance figures can be quoted as if one were live.

**Do now.** Correct the Git sentence in `skills/README.md`. It is false and it does not change authority.

**Needs producer decision.** Point `memory/projects.json` `decisions` at `00_brief/decisions/`, or mark the key as legacy in that index. Add a machine-readable `andreOnlyGates` list only if the producer wants `resume` to carry it; until then, treat `STATE.md` and `D16` as the list. Refresh `STATE.md` so it no longer claims the current `validate` result is four skill warnings. Keep both approval copies until the producer picks the single source; values match today, so this is drift risk, not a current flag conflict.

### 5. The required-directory list is the scaffold, not the canonical tree

**What is true.** Every path in `workspace.json` `requiredDirectories` exists. These live directories are not in that list, so `validate` would still pass if they disappeared (once finding 1 is fixed):

- `projects/andre-time-travel/00_brief/decisions/` (D01–D16 and D20)
- `projects/andre-time-travel/05_storyboard/source/`
- `05_storyboard/preproduction-atlas-v1/`, `preproduction-atlas-v2/`, `preproduction-atlas-v3/`
- `08_edit/reviews/` including `holistic-staging-v1/snapshots/`, which copies `memory/STATE.md`, `docs/`, bibles, and timelines into the film tree
- `03_bibles/detail-planning/`
- `02_references/keyframes/`, `02_references/inserts/`, `02_references/_review/`
- `07_generations/plans/`, `07_generations/downloads/`, `07_generations/batches/`
- `09_delivery/posters/`
- `inbox/Photos-Andre-Suit/` (15 files) and `inbox/instagram-andreathar/` (20 files)
- Top level: `drafts/`, `series/`, `.claude/`, `.agents/`, `docs/kling-manual/`, `docs/superpowers/`

`docs/FOLDER_STRUCTURE.md` is an older snapshot. It does not list `drafts/`, `series/`, `.claude/`, `.agents/`, or those extra film directories. `docs/WORKSPACE.md` describes `05_storyboard/` as keyframes, contact sheets, shot list, and animatics, and does not mention `source/` or the atlas revisions.

Root `tasks/` holds only `tasks/README.md` and is required because `workspace.json` says so. The board is `projects/andre-time-travel/tasks/board.json`. Root `memory/` holds `projects.json` and a README. Film memory is `projects/andre-time-travel/memory/`. That split is documented. The hazard is the extra copies that look like a second `STATE.md`:

- `reports/workflow-v1/before/memory/STATE.md`
- `reports/preproduction-atlas-v1-before-state/memory/STATE.md`
- `projects/andre-time-travel/08_edit/reviews/holistic-staging-v1/snapshots/memory/STATE.md`

The report copies still tell a reader to resume from `decisions.json`. The snapshot inside `08_edit/reviews/` is inside the film tree.

Atlas catalogs (v1 created 2026-10-09T08:23, v2 08:44, v3 09:23, all `-03:00`) each report 16 boards, 41 shots, 22 performance cards, 79 card images, and top-level `approved: false`. `START_HERE.md` documents v1 and v2 only. `docs/REPEATABLE_WORKFLOW.md` shows a build command whose `--output` is `05_storyboard/preproduction-atlas-v3`, and the renderer refuses an existing folder. The next free revision name is not v3.

`08_edit/picture-lock/galileo-en-preview-v1.mp4` is the Galileo preview. `manifest.json` calls it `assembled_pending_full_playback_and_dubbing`. The folder name says picture-lock. In this checkout the path is a Git LFS pointer (`oid sha256:b008ed2b…`) and `.git/lfs/objects/` does not contain that object. Playback was not verified.

`07_generations/accepted/` is empty (`.gitkeep` only). `07_generations/originals/` has 205 files and `rejected/` has 10. Chapter `acceptedTakeId` values in the manifest are null. The era stills D12 names are 12 JPEGs under `02_references/keyframes/andre/`. The per-chapter folders `05_storyboard/keyframes/{caesar,galileo,genghis,napoleon,oppenheimer}/` are `.gitkeep` only. Populated storyboard image sets are `05_storyboard/keyframes/detail-studies-v1/` and `chatgpt-in-out-v1/`.

**Why it hurts.** Integrity checks guard empty stage folders and do not guard the decision records or the atlas source. Derived atlases, review snapshots, and a preview named as a lock sit where a later session can treat them as current canon. The documented atlas command cannot be run as written.

**Do now.** In `START_HERE.md` and `docs/REPEATABLE_WORKFLOW.md`, state that v3 already exists and that a new render needs a new folder name. In `docs/FOLDER_STRUCTURE.md`, label the tree as a historical scaffold snapshot and add the live directories above, without moving files.

**Needs producer decision.** Whether `requiredDirectories` should include `00_brief/decisions`, `05_storyboard/source`, and `08_edit/reviews`. That changes `workspace.json` and therefore `validate`. Whether holistic snapshots should stay inside `08_edit/` or be cited only from `reports/`. Whether a non-accepted preview may remain under `picture-lock/`. Whether `inbox/Photos-Andre-Suit` and `inbox/instagram-andreathar` are additional intake categories or should be recorded under the existing `inbox/andre-reference-photos` rules. This review did not hash-compare those inbox trees.

### 6. Skill registry, link targets, and mirrors do not describe one installation

**What is true.** `skills/registry.json` records five `machine_local_symlink` skills with `source` under `/home/athar/.hermes/skills/...`.

| Skill | Registry `source` | Actual link | On this machine |
|---|---|---|---|
| `kling-cli` | `/home/athar/.hermes/skills/kling-cli` | `../.agents/skills/kling-cli` (files in-repo, not a symlink) | Real skill text, version 0.2.0. SHA-256 of `SKILL.md` does not match `sourceSha256`. |
| `film-character-continuity`, `film-dialogue-localization`, `film-editing-qc`, `grounded-citations` | matching `/home/athar/.hermes/skills/...` paths | relative links that resolve to those paths | All four targets exist and their hashes do not match `sourceSha256`. Only `film-editing-qc/SKILL.md` was inspected and confirmed as a cloud placeholder; the other three bodies were not read. |

`docs/CLEANUP-INVENTORY-2026-10-09.md` already says the Kling origin must be reconciled and that hashes must not be rewritten just to clear warnings.

`.hermes/skills/` links back into `skills/` except `kling-cli`, which links to `.agents/skills/kling-cli`. `.claude/skills/kling-cli` does the same. `.agents/` is not in `workspace.json` or `docs/FOLDER_STRUCTURE.md`. `skills-lock.json` records only `kling-cli` from GitHub `klingai-tech/skills`, a third origin beside the registry path and the `.agents` copy.

Because `validate` aborts on finding 1, this run did not observe the warning `shared skill changed since linking`. The mismatch is still true: each registered `SKILL.md` hash differs from `sourceSha256`. On a machine without `/home/athar/.hermes/skills`, the four film/research links break and `validate` exits 2 with `missing or broken skill source`. That remains an environment condition. Do not delete the links, edit the registry hashes from these placeholders, or weaken the check.

**Why it hurts.** A cloud session can "validate" against placeholder procedures and believe continuity, dialogue, and QC skills were followed. A laptop session follows different bytes than `sourceSha256` records. Kling's recorded source path is not the path Git actually checks out.

**Do now.** None that rewrites hashes or copies placeholder text into the repo.

**Needs producer decision.** Reconcile `kling-cli` so registry `source`, the symlink, and `skills-lock.json` name the same tree, then rehash from that tree on the owner's machine. Keep the film skills as machine-local links if that is still the contract; document `.agents/` as the Kling checkout location so it stops looking like an untracked mirror.

### 7. Lane protocol and hooks describe authority the current tree does not have

**What is true.** `docs/PARLEY_PROTOCOL.md` line 7 says forge issues and PRs do not apply because there is no Git remote. `docs/VERSION_CONTROL.md` records `origin` as the private GitHub repository and `main` tracking `origin/main`. The smoke test still launches lanes with `--repo /mnt/data/Projects_SSD/Movies_Projects`.

The section "Lane roster v2" says it was implemented on branch `claude/wizardly-clarke-23j2kj` as a proposal and becomes active only when Andre merges it and runs Phase 0 (`scripts/parley_setup.sh`). That work is on `main` (`e1b5eb4`). `scripts/parley_setup.sh` exists. This review did not run it. `agent-parley` is not installed here. `docs/PLAN-parley-integration-v1.md` still says status PROPOSED and tells the reader to use that feature branch at `dfec3be`.

`.claude/settings.json` registers SessionStart, PreToolUse, PostToolUse, and Stop hooks. `AGENTS.md` already says those hooks are refusals, covered by dry-run tests, and that they never approve, spend, commit, or merge. This checkout has no `.cursor/` hook config. Nothing in this session showed the hooks running.

`docs/PARLEY_PROTOCOL.md` also still assigns the producer as "Codex in the main desktop conversation" and says lanes return handoffs instead of editing canonical records. That ownership table matches `AGENTS.md`. The stale sentences are the "no Git remote" line, the absolute machine path, and the "not active until merged" line after the merge.

**Why it hurts.** One protocol file contains an active assignment and a roster that calls itself inactive. An agent can either ignore the roster or treat hooks and dispatch as already in force. Neither reading is reliable, and this environment cannot execute Parley.

**Do now.** Replace the "no Git remote" sentence with a pointer to `docs/VERSION_CONTROL.md`. State that the roster text landed on `main` and that Phase 0 has not been recorded in this review.

**Needs producer decision.** Declare lane roster v2 active or keep it proposed until Phase 0 evidence exists (`parley_setup.sh` output, smoke test, hook proof in `docs/parley-smoke-test.md`). Update or archive `docs/PLAN-parley-integration-v1.md` so it does not send readers to a superseded branch. Do not describe `.claude/hooks/` as protection for Cursor or other runtimes until that is implemented and tested.

### 8. Names that collide or hide which tree is canonical

Documentation language is mixed pt-BR and English on purpose. These names are the ones that hide ownership:

- Chapter key `galileo` versus plans and handoffs `piloto-galileu` and `piloto-galileu-v2` (`07_generations/plans/2026-10-09-piloto-galileu-v2.md`, cited by D16). Same chapter, two slugs.
- `keyframes` means three different sets: empty per-chapter folders under `05_storyboard/keyframes/`, study sets in sibling folders there, and the 12 era stills under `02_references/keyframes/andre/`.
- `08_edit/reviews/2026-10-09-revisao-nova-direcao/` versus later English review folders such as `detail-planning-v2/`. Search for "review" misses the Portuguese slug.
- `agents/lighting.md` is the only role brief written in Portuguese. The other briefs are English. A dispatcher reading English briefs only will miss the lighting constraints.
- `picture-lock` holds a preview candidate. `accepted` under `07_generations/` is empty while prose in decisions calls candidates accepted.
- Decision files are `Dnn-slug.json` under `00_brief/decisions/`. The legacy bundle `memory/decisions.json` reuses D01–D05 under `LEGACY-` ids. The filename `decisions.json` still looks like the index.
- Templates are `shared/templates/agent-handoff.json` and `agent-handoff-v2.json`. Instances are dated handoffs. Schema version is inside the file; the filename does not say v1 or v2.
- `tasks/README.md` now says new film-task files are `YYYY-MM-DD-topic-vN`. Older live files (`workflow-map-v1.md`, `scene-detail-assets-v1.md`, `production-tasks.md`) predate that rule. Both patterns are in `projects/andre-time-travel/tasks/`.

**Why it hurts.** A search or a handoff path can attach evidence to the wrong slug, or treat an empty `accepted/` or `keyframes/<chapter>/` folder as the set that was reviewed.

**Do now.** When adding a new file, use the film chapter key (`galileo`, not `galileu`) and the `tasks/README.md` date pattern. Do not rename existing decision, plan, or handoff files in a cleanup pass; those names are cited.

**Needs producer decision.** A short alias note, in one place the producer already owns (`STATE.md` or the workflow map), that `piloto-galileu*` is the Galileo chapter and that era stills live in `02_references/keyframes/andre/`. A folder move of the preview out of `picture-lock/` is a layout change and stays with the producer.

## Non-findings

These look messy and are intentional. Do not "clean" them as part of acting on this report.

- Empty `.gitkeep` directories under the numbered pipeline, `inbox/failed-clips/`, and `drafts/workflow-rehearsal/` are the scaffold. `drafts/workflow-rehearsal` is test-only and must not inherit budget, jobs, or approvals.
- `series/andre-time-travel/` holds reusable rules. Episode choices stay under `projects/andre-time-travel/`. `shared/templates/continuation.json` starts a clean draft.
- `memory/decisions.json` already says it is superseded and prefixes legacy ids. The defect is the live pointer in `memory/projects.json`, not the history file.
- Atlas catalogs set `approved: false`. That is the derived-document contract. Do not edit PDFs or PNGs in `preproduction-atlas-v1` through `v3` in place.
- `07_generations/accepted/` empty, with null `acceptedTakeId`, matches "candidate is not an accepted take."
- D17–D19 have no decision files because they are still proposals.
- Mixed pt-BR and English prose in `START_HERE.md`, `docs/REPEATABLE_WORKFLOW.md`, `docs/VERSION_CONTROL.md`, and `docs/LOCAL_AGENT_HANDOFF.md` is the existing language of those files.
- Root `tasks/README.md` correctly says the board is not in that folder.
- `coordinator/web/package.json` was removed in `52a5355`. No `coordinator/` directory remains.
- Film gate hooks are refusals. `AGENTS.md` already limits what they guarantee. Do not turn them into approvals or disable them to get past a block.
- Do not delete `skills/film-*` or `skills/grounded-citations`, and do not weaken `validate`, to make this machine pass.
- Approval flags in `manifest.json` and `approvals.json` match today. The lint advisory is the dual-write risk.
- `docs/CLEANUP-INVENTORY-2026-10-09.md` and `projects/andre-time-travel/tasks/project-cleanup-plan-v1.md` already exist as inventories. This report does not replace them and does not execute them.

## Priority

1. Producer: reduce `agents/registry.json` to one `coordinator` and choose its authority fields. Until that lands, `validate` and `status` do not describe the film.
2. Producer: after that edit, repair the pending cleanup handoff so `lint` can pass, then ingest or supersede it on purpose.
3. Hygiene: point `CLAUDE.md`, `docs/LOCAL_AGENT_HANDOFF.md`, `docs/REPEATABLE_WORKFLOW.md`, and `agents/README.md` at handoff v2. Fix D16/D20 labels and the board-write example in `agents/coordinator.md`. Fix the "not a Git repo" sentence in `skills/README.md` and the "no Git remote" sentence in `docs/PARLEY_PROTOCOL.md`.
4. Producer: decide whether `coordinate` is in-repo, machine-local, or unused. Do not leave the role requiring a broken link.
5. Producer: update `STATE.md` and the `memory/projects.json` decisions pointer so resume no longer prefers legacy ids or a validate result this tree does not produce.
6. Producer: declare whether lane roster v2 is active before Phase 0 evidence. Record that decision in `docs/PARLEY_PROTOCOL.md`.
7. Hygiene, then a producer call if the check should fail when they vanish: document `00_brief/decisions/`, `05_storyboard/source/`, atlas v3, and `08_edit/reviews/` as canonical or derived, and stop advertising v3 as the next empty output folder.
8. Producer, on the owner's machine: reconcile the Kling skill source and rehash. Leave placeholder film-skill hashes untouched.

## Not verified

- Unit tests (`python -m unittest`) were not run. The repository-backed success assertions for `status` and `validate` in `tests/test_manage.py` are expected to fail on the duplicate role before skill-link checks run; tests that intentionally expect validation errors are not necessarily failures.
- Shared-skill hash warnings were not printed by `validate` on this commit. Hashes were compared directly and do not match.
- Placeholder bodies were confirmed for `film-editing-qc` only. The other three `/home/athar` targets exist and mismatch the registry hash; their full text was not read.
- Git LFS media was not fetched. The Galileo preview object is absent locally. No playback, loudness, or frame inspection was done.
- `agent-parley` was not installed and `scripts/parley_setup.sh` was not run. Phase 0 completion on the owner's machine was not checked.
- Inbox photo sets were not compared by hash. Log files under `projects/andre-time-travel/logs/` were not read.
- `STATE.md` was not diffed sentence-by-sentence against every handoff after 2026-10-09. Claims above are the ones checked against files or command output.
