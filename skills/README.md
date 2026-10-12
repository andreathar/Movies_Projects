# Skill Sources

`andre-time-travel/` is the canonical project-specific procedure. Other entries link to the existing active-profile skills; no vendor skill or profile workflow is copied. `registry.json` records link provenance and machine-local targets. `.hermes/skills/` exposes the same sources without a second copy.

This workspace is a Git repository. `origin` is the private GitHub remote and `main` tracks `origin/main`; see `docs/VERSION_CONTROL.md`. Automatic slash-command discovery is not claimed. `AGENTS.md` routes the agent to the local procedure. Do not change global configuration or trust a directory merely to make a status report appear complete.

`skills/kling-cli` links to the in-repo checkout `.agents/skills/kling-cli`. `skills/registry.json` still records the owner source `/home/athar/.hermes/skills/kling-cli` and that tree's `sourceSha256`. Rehash only on the owner's machine from the tree that should be trusted. Do not rewrite hashes from cloud placeholders, and do not delete `skills/film-*` or `skills/grounded-citations` to clear a warning.

The `coordinate` skill is not in the registry. The links `skills/coordinate`, `.agents/skills/coordinate`, `.claude/skills/coordinate` and `.agents/plugins/agent-parley/skills` pointed outside this checkout at a missing target and were removed. The coordinator role does not require that skill until a real target is vendored or registered.
