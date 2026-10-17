# Skill Sources

`andre-time-travel/` is the canonical project procedure (reading order, task-to-document map, gates, hooks, closing checklist). `kling-cli` is vendored in `.agents/skills/kling-cli`; `skills/kling-cli`, `.claude/skills/kling-cli` and `.hermes/skills/kling-cli` resolve to that same tree. Its current SHA-256 in `registry.json` describes this effective source. Earlier profile provenance is retained as history.

The other skills link to machine-local profile sources, also exposed in `.hermes/skills/`. They are not all mirrored in `.claude/skills/` (links outside the repo are machine-local). Preserve those links and their recorded hashes; a changed shared skill requires review, not an automatic rehash: record the review in `provenanceHistory` as the 2026-10-17 entries do. Missing links or placeholders do not count as usable skills. The English Kling translation and technical contracts remain intact.

## Which skill, when

| Task | Skill (read by path if the client did not load it) | Auto-loaded in Claude Code |
|---|---|---|
| Anything on this film; what to read next | `andre-time-travel` | yes (`.claude/skills`) |
| Kling CLI, requests, Elements, motion control | `kling-cli` | yes |
| Face/wardrobe/table continuity, references, pilots | `film-character-continuity` | no, read `skills/film-character-continuity/SKILL.md` |
| Script, dialogue, translation, voice, lip-sync | `film-dialogue-localization` | no |
| Take review, edit, audio, delivery QC | `film-editing-qc` | no |
| Sourced history, quotations | `grounded-citations` | no |

Shared skills are written for the Hermes agent: load `andre-time-travel/references/shared-skills-adapter.md` with them (precedence, Claude Code tool mapping, project ledger path). Roles map to skills in `agents/registry.json`; load one role brief and only its skills.

## Not part of this registry

- `coordinate` is external. Its sibling source and installed Parley plugin were verified in the coordination audit; availability to a specific session requires that client's actual loaded tool/skill inventory.
- **Higgsfield** skills (`higgsfield-generate`, `-brandkit`, `-product-photoshoot`, `-marketplace-cards`, `-soul-id`, `-video-explainer`, `-websites`, `-youtube-thumbnail`) were installed at user level (`~/.claude/skills`, from `higgsfield-ai/skills`), not into this repository, and are not film procedures. They know nothing of this project's rules: paid and write calls are producer-only behind `.claude/hooks/higgsfield-gate.py` (scope template `shared/templates/higgsfield-scope.json`, policy `docs/MODEL_POLICY.md`). Read-only calls (`account status`, `model`, `generate cost`) are free. Removed project-local links are not recreated, and this catalog does not claim discovery or active sessions.

See [AGENT_CATALOG.md](../docs/AGENT_CATALOG.md) for derived metadata, drift checks and the frontend update procedure. Git and publication rules remain in [VERSION_CONTROL.md](../docs/VERSION_CONTROL.md). No global configuration or trust changes are needed for catalog generation.
