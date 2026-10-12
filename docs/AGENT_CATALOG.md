# Agent catalog and frontend sources

Edit `agents/registry.json`, the briefs it references, and `skills/registry.json`. Brief Mission sections supply role summaries. Skill descriptions and hashes come from their effective `SKILL.md`. Do not maintain separate role summaries or copied skill instructions in the frontend.

## Rebuild local derived metadata

From Movies_Projects:

```bash
python3 scripts/agent_catalog.py
python3 scripts/agent_catalog.py --check
cd sites/movies-demandas
node scripts/export-workspace.mjs ../..
node scripts/export-production.mjs ../..
node scripts/export-workspace.mjs ../.. --check
node scripts/export-production.mjs ../.. --check
node --test tests/model.test.ts tests/export.test.mjs
npm run lint
node node_modules/typescript/bin/tsc --noEmit
npm run build
```

Generation validates every input before writing its outputs. Duplicate IDs, missing briefs, broken skill links, unknown role references and adapter drift fail checks. Shared skill hash differences remain visible and require review; exporting metadata does not approve a changed skill. Preserve its recorded provenance until that review.

`agents/generated/catalog.json` and reviewer adapters are derived. They are intentionally outside `.claude/agents`, `.codex/agents` and user configuration. Only historian, continuity and QC are prepared; producer, director and coordinator remain governance roles. No MCP, model, provider, permission, hook, grant or runtime configuration is changed.

Claude files use the native frontmatter shape found in installed Claude Code 2.1.296 plugins and limit tools to Read/Glob/Grep. Codex 0.162.1 exposes role loading, but automatic project discovery and precedence were not verified through a running client. Both sets remain **prepared, activation pending**. TOML/metadata validation is not client execution. The parent must verify client compatibility, unique registration and exact scope before any future activation. Codex adapters contain no security or tool grants; their review-only wording is an operating rule, not enforcement. Existing briefs may describe editing assignments; these prepared adapters are limited to returning findings.

## Frontend update contract

`workspace.json` points to the active visual planning scope through the film's `visualRestart` path. Its source hashes must still match. Changing the script or another pinned input requires review of that scope before export. Existing board and approval records retain their original meanings; a visual draft does not reopen deliveries or approve new media.

The two exporters copy selected management metadata only, with a content fingerprint, source hashes, collection time and base Git revision. Unchanged inputs retain identical output bytes. `--check` detects drift without writing; an unavailable source fails, rather than using cached metadata as current evidence. No media or private profile paths are exported. Human-facing labels and layout may live in the frontend; source responsibilities and workflow states come from records.

The site is a separate repository tracked here as a gitlink without a `.gitmodules` mapping. Keep changes and review evidence separately for both repositories; this work does not migrate that structure. Local generation does not publish the site. A deployed site changes only after separately authorized publication. Existing persisted production snapshots require the site's review/import action; they never silently overwrite demands or comments. Catalog inventory is not live agent status. Import is not review, acceptance or execution.

A build validates the bundled production package, while freshness against the local Movies workspace requires the explicit export `--check` commands above. Remote builds without the source workspace cannot establish live freshness.
