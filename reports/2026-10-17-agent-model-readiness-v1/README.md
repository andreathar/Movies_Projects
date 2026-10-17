# Agent files: model-readiness review

Date: 2026-10-17. Scope: `agents/`, its generator/tests and applicable governance. Role: independent reviewer, active episode `andre-time-travel`. Authorization: inspect and report; no brief, registry, adapter, permission or client configuration changed. Other writers' concurrent workspace changes were preserved.

## Verdict

**Useful, reasonably concise role briefs; not yet fully optimized for reliable model execution.** The main problems are conflicting authority language, tool/task mismatch and unnecessary context expansion—not Markdown formatting or a need for a different model.

Most briefs already have clear mission, inputs, output locations, prohibited actions and completion criteria. Provenance, paid-work separation and version-aware evidence requirements are valuable and should stay. Generated adapters are reproducible and deliberately inactive. These are strengths.

This is a static prompt/configuration review, not a measured model-performance benchmark. No client/model was activated, media played, provider called or additional permissions granted. File size does not establish model quality, and no percentage token/cost improvement is claimed.

## Findings, ranked

### 1. High: storyboard directly contradicts itself about approval

- `agents/storyboard.md:4`: “Approve keyframes and an audio-first animatic”.
- `agents/storyboard.md:10`: deliverable is “Shot-specific approved keyframes”.
- `agents/storyboard.md:25`: the role may not “approve keyframes”.

A model receives an impossible instruction set. The mission is especially consequential because `scripts/agent_catalog.py:86–88` derives the displayed role summary directly from it. Fix the mission/deliverable to propose and review candidate keyframes, leaving artistic acceptance to the actual authorized approver. Keep the prohibition. Regenerate dependent metadata after an assigned source correction.

### 2. High: prepared reviewer adapters cannot complete their own stated workflows

- `agents/generated/claude/movies-qc.md:4` allows only Read, Glob, Grep.
- `agents/generated/claude/movies-qc.md:8` correctly says findings only, no file edits.
- `agents/generated/claude/movies-qc.md:30–31` nevertheless includes a Writes section requiring reports and logs, inherited from the source brief.
- `agents/generated/claude/movies-qc.md:36–37` requires full decoding/playback and risky-frame inspection.
- `agents/generated/claude/movies-historian.md:4,30–31` has the same file-writing mismatch; there is also no configured external research tool in that adapter.
- `scripts/agent_catalog.py:97–104` prepends a restricted-review wrapper but then appends the entire source brief, including editing workflows. Codex prompts inherit the same contradictory text, without an adapter-defined tool security boundary.

Read/Glob/Grep do not provide a full video/audio decode/playback workflow or file-writing route. The wrapper does say to report unavailable tools, which reduces risk, but the definition of done should also be attainable in the selected mode.

**Recommended design:** retain strict findings-only adapters; explicitly distinguish their permitted evidence review from a parent-run media verification. Render editing steps as proposed outputs for the parent, not actions the adapter must perform. Mark unperformed checks as `not_run` with an owner. Do not solve this by automatically expanding tool grants. Any later full-media role needs separately reviewed capabilities and runtime verification.

### 3. Medium: review vs edit mode and path roots are not explicit enough

`agents/continuity.md:13,21–22`, `agents/historian.md:13,21–22`, `agents/editor.md:13,21–22` and other briefs say read-only by default but also list editable folders. `agents/README.md:7` supplies the missing rule: only an explicit local editing assignment enables source edits. That is valid in the documentation set, but a parent passing only one brief can omit it.

Paths such as `03_bibles/`, `08_edit/` and `agents/handoffs/` are often film-relative, while the workspace also has a real root `agents/`. `agents/coordinator.md:95–96` does not itself disambiguate its handoff output from the root role directory. `docs/LOCAL_AGENT_HANDOFF.md` provides the correct episode path, but model prompts should not depend on guessing that convention.

**Recommendation:** each assignment declares `workspaceRoot`, `episodeRoot`, mode (`review` or explicitly assigned local edit), input paths/hashes and exact allowed outputs. Add one short local rule explaining that Writes lists possible areas, not standing permission. Findings-only adapters should not require Parley reservations or writes to finish a review. Preserve the mandatory AGENTS startup gates.

### 4. Medium: coordinator context loading is disproportionately expensive and stale-prone

- `agents/coordinator.md:12,23` calls for reading existing/all handoffs; the episode handoff directory currently contains **69 files**.
- `agents/producer.md:19` also requests every handoff.
- `agents/coordinator.md:24,71–82,113` embeds dated decision ranges, work-package examples and a historical spend-ceiling explanation inside a reusable role definition.
- `agents/coordinator.md:33` asks for periodic reports; `agents/coordinator.md:118–124` contains an external Telegram/email escalation route without an assignment-specific destination or authorization gate.

These instructions can make each startup a broad re-audit and mix old episode status with current role behavior. Periodic reports should not be read as permission for timers or schedules; external escalation needs explicit authorization and a real configured route.

**Recommendation:** keep one brief dispatch algorithm and boundaries; resolve current decisions from the assigned records; inspect only new/relevant handoffs and dependency evidence, expanding when necessary. Move examples to the coordinator protocol. Make status/escalation event-driven and default to reporting the blocker to the parent. This does not relax evidence checks for a handoff actually being integrated.

### 5. Medium: producer brief does not restate the current paid-submission route accurately enough

`agents/producer.md:13,22,25` refers to Kling CLI, `scope.json`, fresh balance and written scope. Those are not a substitute for the stricter current contract in `AGENTS.md:29`: producer-owned submission via `scripts/kling_batch.py` with an applicable `kling_job_release` in `00_brief/approvals.json`.

The brief loads AGENTS, so it does not override that restriction. However, a short producer prompt should point directly to the current release gate instead of presenting an incomplete shortcut. No paid command was run in this review.

### 6. Medium: tests validate artifacts, not instruction consistency

`tests/test_agent_catalog.py` has useful tests for determinism, duplicate IDs, missing inputs, path escape, drift, authority flags and Portuguese mission extraction. All **8 tests pass**. None detects the storyboard contradiction, a read-only adapter retaining a Writes workflow, media verification without the necessary tools, or stale role inputs.

**Recommendation:** extend static validation for explicit mode, rooted output paths, role-specific tool prerequisites and required report fields. Use a small human-reviewed scenario set for semantic behavior: unapproved keyframe, missing media tool, changed input hash, blocked dependency and ambiguous episode path. Passing a text linter still would not prove model compliance or security.

### 7. Lower: output shape and version pointers can be more deterministic

The generic handoff template is strong, but reviewer briefs do not provide a common compact findings record. `agents/historian.md:19`, `agents/director.md:16` and `agents/dialogue-sound.md:19,28` hard-code “Script v2”/“research v2” instead of requiring the explicitly assigned source version/hash.

**Recommendation:** use a concise per-finding structure: severity, claim, artifact path/hash, timestamp/frame or line, observed evidence, interpretation/uncertainty, recommended action, next owner. Distinguish observed vs inferred vs not checked. Keep authoritative decisions and no-fabrication rules. Resolve current inputs from the assignment rather than assuming a filename or version remains current forever.

### 8. Lower: modest boilerplate duplication, not a massive prompt-size problem

Whitespace-separated word counts (not model tokens):

| Source | Words |
|---|---:|
| `agents/coordinator.md` | 1,311 |
| `agents/dialogue-sound.md` | 386 |
| `agents/historian.md` | 349 |
| `agents/producer.md` | 316 |
| `agents/qc.md` | 298 |
| `agents/lighting.md` | 284 |
| `agents/editor.md` | 280 |
| `agents/continuity.md` | 278 |
| `agents/storyboard.md` | 268 |
| `agents/director.md` | 244 |
| **Ten role briefs** | **4,014** |

All ten include the identical 46-word Kling contract paragraph, plus its heading. This is maintenance duplication, but **not 460 words of per-request savings** when only one relevant role is loaded. Likewise, generated copies do not cost model context merely by existing on disk. Do not remove a self-contained critical boundary merely to shorten a file. The better optimization is one common contract, one relevant role, the exact assignment and required evidence—not the whole registry/catalog/all role briefs.

Mixed English/Portuguese is not itself a defect. Standardizing section keys could help tooling, but translation alone is not a demonstrated performance improvement. No need to convert all Markdown to JSON or create ten new prompt frameworks.

## Verification and limits

Executed during this review:

- `.venv/bin/python -B scripts/agent_catalog.py --check` → status OK, seven generated artifacts unchanged, activation pending.
- `.venv/bin/python -B -m unittest discover -s tests -p test_agent_catalog.py` → 8 tests passed.
- `.venv/bin/python -B scripts/manage.py status` → OK; three shared-skill hash warnings remain (continuity, dialogue localization, editing QC).
- Inspected every role brief, registry, generator, catalog tests, documentation and representative generated QC adapters. Counted role text and handoff files; no model-token estimator used.

`docs/AGENT_CATALOG.md:27–29` correctly states that native adapters are prepared, not proven active. No discovery/runtime compatibility test was performed here. Metadata validity does not prove the model received a role, loaded its skills or can execute its workflow. Three recorded skill hash differences require review, not an automatic registry rehash. No other agents' live sessions were inspected or contacted.

## Proposed successor

Review stage closed. No edits to `agents/` or generator are included. Desktop producer owns review/assignment of any governance wording change. First assign the storyboard contradiction and generated-adapter mode/tool mismatch; then narrow coordinator context and clarify path roots. Preserve spend/identity/temporal gates, regenerate sources' derivatives only after approved edits, and check the scoped tests. No successor has accepted this proposal, and no role activation or new model/provider permission is authorized by it.
