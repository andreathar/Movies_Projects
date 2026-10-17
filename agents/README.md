# Team map

One team, ten responsibilities, two existing Parley participant names. Roles describe **what** to do; participants identify **who** can receive an assignment. This map clarifies the existing contract; it creates no sessions, permissions, assignments or production approvals.

## People, participants and roles

| Identity | Responsibility | Boundary |
|---|---|---|
| Andre | Author/operator; likeness, voice-by-ear and final acceptance | Human gates cannot be inferred or self-approved |
| Desktop producer | Codex main/base conversation; producer + director; integrates canonical records and creates detail images | Not the Parley `codex` participant |
| `claude` | Existing Parley participant; research/continuity preparation when assigned | Actual role and allowed files come from its accepted task |
| `codex` | Existing Parley participant; editing/QC when assigned | Does not inherit desktop producer powers |
| Ad-hoc helper | Bounded review/edit support in the invoking client | No Parley identity or canonical authority by implication |

Use these existing participant names, not invented teammates such as `claude-research` or `codex-edit-qc`. Discover actual availability before dispatch. Ten briefs do **not** mean ten workers. Additional specialists are responsibilities assigned when needed, not a roster to launch. Runtime state is never inferred from registry `running` flags.

| Stable role ID / brief | Owns | Returns |
|---|---|---|
| [producer](producer.md) | Integration, scoped delegation, paid-release boundary | Verified records, charges, next owner |
| [director](director.md) | Authorized creative decisions | Scoped decisions or proposals |
| [coordinator](coordinator.md) | Bounded dispatch and delivery verification | Assignments, routing handoff; no canonical edits |
| [historian](historian.md) | Facts, sources, material culture | Claim/evidence/uncertainty |
| [continuity](continuity.md) | Identity, wardrobe, table, axis | Image/frame defects and bible proposals |
| [lighting](lighting.md) | Motivated light and matching | Per-shot light/continuity findings |
| [dialogue-sound](dialogue-sound.md) | Lines, languages, timing, foley, sync | Measured cues/tracks or findings |
| [storyboard](storyboard.md) | Framing, coverage, audio-led animatic | Candidates for approval, not approvals |
| [editor](editor.md) | Timeline, assembly, finishing | Versioned edits and exact-file checks |
| [qc](qc.md) | Independent deliverable inspection | Technical recommendation, not artistic acceptance |

Keep these IDs and brief filenames unchanged: boards, handoffs and generated adapters already reference them. Name the role separately from the participant in every assignment. Creator self-check and independent QC are not interchangeable.

## Six process names

Use these verbs in task descriptions and message subjects, not as new board statuses or task IDs:

1. **Scope** — producer defines goal, owner, inputs/hashes, mode, allowed outputs, checks and successor.
2. **Assign** — discover availability; offer the bounded task; recipient accepts scope. Until then producer owns it.
3. **Make** — accepted owner performs only assigned work, preserving originals/concurrent edits.
4. **Check** — inspect exact evidence; distinguish observed, inferred and `not_run`; independent review where required.
5. **Integrate** — desktop producer verifies one handoff/diff at a time and updates canonical records. Director records authorized decisions.
6. **Close** — record accepted successor, owned blocker/unblock condition, or closed stage. Delivered is not artistically accepted.

Production remains research/reference → measured dialogue/coverage → candidate review → separately released generation → edit → QC → human acceptance, governed by the existing board and workflow map. These names do not bypass any gate.

## Folder and file names

Keep the existing numbered episode folders; no mass rename or move. Use workspace-relative paths in assignments and management data.

| Location | Purpose |
|---|---|
| `agents/registry.json`, `agents/*.md` | Stable role index and brief sources |
| `agents/CONTRACT.md` | Shared execution modes, paths and evidence format |
| `agents/generated/` | Rebuildable, inactive catalog/reviewer adapters; never edit manually |
| `docs/PARLEY_PROTOCOL.md` | Parley identities, ownership and runtime limits |
| `docs/COORDINATOR_PROTOCOL.md` | Assignment/delivery procedure |
| `shared/templates/` | Existing handoff/review schemas; reuse, do not fork per worker |
| `projects/<episode>/00_brief/` | Brief, research, decisions and approvals |
| `projects/<episode>/01_script/` | Script/line IDs and translation proposals |
| `projects/<episode>/02_references/` | Categorized references; originals separate from candidates |
| `projects/<episode>/03_bibles/` | Continuity and historical specifications |
| `projects/<episode>/04_audio/` | Guide/final audio and stems with provenance |
| `projects/<episode>/05_storyboard/` | Source plans, candidates and animatics |
| `projects/<episode>/06_pilot/` | Pilot evidence and reviews |
| `projects/<episode>/07_generations/` | Requests, provider responses and original takes |
| `projects/<episode>/08_edit/` | Timelines, derivatives and review reports |
| `projects/<episode>/09_delivery/` | Masters, captions, stems and final QC |
| `projects/<episode>/agents/handoffs/` | Episode deliveries, not role definitions |
| `projects/<episode>/tasks/`, `memory/` | Task/specification sources and resume surface; producer-owned canonical updates |
| `reports/` | Workspace/tooling audits, not a second production board |

For **new** files: lowercase kebab-case topics; preserve stable shot/line/task IDs exactly. Prefer `<topic>-vN.<ext>` for artifacts, `<topic>-vN/` for a multi-file package with `README.md`, and `YYYY-MM-DD-<role>-<topic>-vN.json` for a handoff. No `final-final`, unversioned replacement or new `latest` file. Use existing canonical filenames where required (`review.md`, `zero-face-log.json`, `board.json`, etc.). One handoff covers one coherent delivery; a correction names `supersedes` rather than rewriting old hashes.

## Minimal working context

Complete mandatory AGENTS startup, then [CONTRACT.md](CONTRACT.md), one role, exact task and relevant evidence. Do not load all briefs or all handoffs. Review mode returns findings; an explicit edit assignment alone enables its named local outputs. Full playback, temporal face safety, sync and language gates are never replaced by text-only evidence.

Parley procedure: [PARLEY_PROTOCOL.md](../docs/PARLEY_PROTOCOL.md) and [COORDINATOR_PROTOCOL.md](../docs/COORDINATOR_PROTOCOL.md). No forge issue is required for existing local assignments. This documentation does not start Parley, send mail or enable discovery.

Generation/checks: [AGENT_CATALOG.md](../docs/AGENT_CATALOG.md). Sources are editable; adapters stay outside `.claude/agents`, `.codex/agents`, `.cursor/agents` and user configuration. Reviewers remain prepared, activation pending. No daemon, scheduler, credential store or permission change is introduced.
