# Skill Sources

`andre-time-travel/` is the canonical project procedure. `kling-cli` is vendored in `.agents/skills/kling-cli`; `skills/kling-cli`, `.claude/skills/kling-cli` and `.hermes/skills/kling-cli` resolve to that same tree. Its current SHA-256 in `registry.json` describes this effective source. Earlier profile provenance is retained as history.

The other skills link to machine-local profile sources, also exposed in `.hermes/skills/`. They are not all mirrored in `.claude/skills/`. Preserve those links and their recorded hashes; a changed shared skill requires review, not an automatic rehash. Missing links or placeholders do not count as usable skills. The English Kling translation and technical contracts remain intact.

`coordinate` is external to this registry. Its sibling source and installed Parley plugin were verified in the coordination audit; availability to a specific session requires that client's actual loaded tool/skill inventory. Removed project-local links are not recreated, and this catalog does not claim discovery or active sessions.

See [AGENT_CATALOG.md](../docs/AGENT_CATALOG.md) for derived metadata, drift checks and the frontend update procedure. Git and publication rules remain in [VERSION_CONTROL.md](../docs/VERSION_CONTROL.md). No global configuration or trust changes are needed for catalog generation.
