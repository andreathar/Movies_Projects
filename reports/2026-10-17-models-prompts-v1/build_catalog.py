"""Render this dated research inventory from captured, sanitized CLI discovery.

Offline only. Does not call providers, read credentials or modify canonical records.
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNAP = ROOT / 'snapshots'


def load(name):
    return json.loads((SNAP / name).read_text())


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def render():
    caps = load('kling-capabilities.json')['body']
    tools = load('kling-tools.json')['body']['tools']
    models = load('higgsfield-models.json')
    workflows = load('higgsfield-workflows.json')
    help_rows = load('higgsfield-command-help.json')
    model_ids = {m['model'] for r in caps['availableModels'].values() for m in r['models']}
    counts = collections.Counter(m['type'] for m in models)
    out = [
        '# Exhaustive CLI inventory — 2026-10-17', '',
        'Scope: public commands registered by the inspected clients, the Kling live model/tool declarations, and the Higgsfield live model/workflow catalogs visible through the existing session. Not a universal account-entitlement list, private asset inventory or a promise that every listed operation can run. Models and operation wrappers are counted separately from foundation-model families.', '',
        '## Version provenance', '',
        '| Client | Installed | Latest public version checked | Inspected |',
        '|---|---|---|---|',
        '| `@klingai/cli-global` | 0.2.3 | 0.2.3 | Installed official CLI; live capability discovery |',
        '| `@higgsfield/cli` | 1.1.24 | 1.2.2 | Official 1.2.2 Linux binary downloaded/verified in `/tmp`; no global installation or lifecycle script |', '',
        'Latest means npm `latest` checked on this date, not a permanent claim. Higgsfield release: https://github.com/higgsfield-ai/cli/releases/tag/v1.2.2. npm: https://www.npmjs.com/package/@klingai/cli-global and https://www.npmjs.com/package/@higgsfield/cli. Executable, skill and server versions are independent.', '',
        '## Kling — every live model ID by route', '',
        f'{len(caps["availableModels"])} generation routes; {len(model_ids)} distinct **ID spellings**. The GPT Image 2 spelling differs across routes and must not be normalized blindly. Server declaration: `{caps.get("mcpVersion", "unknown")}`.', '',
        '| Route | Exact available IDs |', '|---|---|'
    ]
    for route, spec in caps['availableModels'].items():
        out.append('| `' + route + '` | ' + '<br>'.join('`'+m['model']+'`' for m in spec['models']) + ' |')
    out += ['', 'Full model-specific arguments, required fields, enums, input slots and combined caps: [kling-capabilities.json](snapshots/kling-capabilities.json). Do not infer route parity, defaults, prices or supported references from a shared family name.', '',
            '### All 18 advertised server tools', '', '| Tool | Declared purpose (excerpt) |', '|---|---|']
    for t in tools:
        purpose=t.get('description', '').split('\n')[0].strip()
        # Keep the table readable; complete description/schema remains in the snapshot.
        if len(purpose)>210:
            purpose=purpose[:207]+'…'
        out.append('| `'+t['name']+'` | '+cell(purpose)+' |')
    out += ['', 'Exact complete descriptions and input schemas: [kling-tools.json](snapshots/kling-tools.json). `element_update` is destructive at the raw tool level (unset fields can clear); CLI preservation behaviour is not a general API guarantee.', '',
            '### All 20 top-level Kling commands', '',
            '`who_am_i`, `text_to_image`, `image_to_image`, `text_to_video`, `image_to_video`, `omni_ref_video`, `query_tasks`, `file_upload`, `element_create`, `element_list`, `element_get`, `element_update`, `element_delete`, `motion_library_list`, `motion_control`, `feedback`, `logout`, `account`, `tool_list`, `login`.', '',
            '`account` is the client alias for `query_membership_and_credits`. `tool_list` and `login` are client discovery/auth operations rather than additional generation models. `--help` and `--version` are flags. [Captured help](snapshots/kling-cli-help.txt). No dedicated `video_extend`, timeline, Canvas, HDR, Flash-specific model or 4K command appears in this discovery.', '',
            '## Higgsfield — every live model/operation', '',
            f'**{len(models)} entries**: ' + ', '.join(f'{counts[k]} {k}' for k in sorted(counts)) + '. Several names are utility jobs or wrappers, not distinct foundation models. Duplicated display names are intentional; exact `job_type` determines the operation.', '',
            'Retrieved with the verified **1.2.2 binary**, `model list --json`, through the existing session; [snapshot](snapshots/higgsfield-models.json). The installed 1.1.24 client returned the same total during this audit. Listing is not a successful-generation/entitlement test.', '']
    for category in ('video','image','audio','3d','data','text'):
        out += ['### '+category+' ('+str(counts[category])+')', '', '| Display name | Exact `job_type` |', '|---|---|']
        for m in models:
            if m['type']==category:
                out.append('| '+cell(m['display_name'])+' | `'+m['job_type']+'` |')
        out.append('')
    out += ['## Higgsfield — every live workflow', '',
            f'**{len(workflows)} entries**, independently discovered by `workflow list --json`; not added to the model count as if they were foundation models. [Snapshot](snapshots/higgsfield-workflows.json). Execute nothing merely because an ID is listed.', '',
            '| Display name | Exact workflow ID | Type |', '|---|---|---|']
    for w in workflows:
        out.append('| '+cell(w['display_name'])+' | `'+w['job_type']+'` | '+w['type']+' |')
    out += ['', 'Schema lookup is `workflow get <ID>`; the creation interface is `generate workflow <ID>`, not automatically `generate create <ID>`. Hyphenated prose/example aliases (`voice-change`) must not silently replace the discovered `voice_change` ID.', '',
            '## Higgsfield — complete registered command tree', '',
            f'**16 top-level functional commands/groups** (including `version`; excluding the generic `help` command), **{len(help_rows)-1} non-root command paths** including intermediate groups. This is CLI registration, not a claim of 124 distinct AI tools. [Every captured help page](snapshots/higgsfield-command-help.json).', '',
            '| Parent command | Direct subcommands |', '|---|---|']
    for r in help_rows:
        if r['children']:
            out.append('| `'+r['command']+'` | '+', '.join('`'+c+'`' for c in r['children'])+' |')
    out += ['',
            'Leaf top-level commands such as `version` and server passthrough generation calls are included by their parent row; generic `help`, global `--json`, `--no-color`, `--help` and root `--version` are interface conveniences, not model/tool entries.', '',
            '### Server-managed presets and assets', '',
            '`preset list` documents four preset types: `marketing-studio-v2`, `soul-v2`, `video-explainer`, `animation-action`. Entries and action pages change server-side; `animation-action` supports pagination. Model/workflow schemas and presets are different catalogs. Voices, personal uploads, Soul IDs, projects, workspaces, website databases/secrets and generation histories were **not enumerated**: they are account resources, not omitted model families. No account/credit query was needed for this documentation work.', '',
            '### Live catalog wins over stale prose', '',
            'The official static MODELS.md is incomplete relative to this live catalog. Examples include names/IDs for Nano Banana Pro (`nano_banana_2` in older docs versus `nano_banana_pro` in live discovery) and game/website features in README versus the actual command tree. Do not call a docs-only ID deprecated without a successful discovery/schema check. The developer API catalog uses endpoint IDs (for example `bytedance/seedance-2.5/reference-to-video`) and a different counting surface; it must not be merged into these CLI IDs.', '',
            'Official sources and local input hashes: [sources.json](sources.json); [Kling 4.0 and Cinema Studio 4.0 guide](kling4-and-higgsfield.md). No hidden/internal symbols are promoted to registered public commands.', ''
    ]
    (ROOT / 'catalog.md').write_text('\n'.join(out))
    return {'klingRoutes':len(caps['availableModels']), 'klingModelIdSpellings':len(model_ids), 'klingServerTools':len(tools), 'higgsfieldModelOperations':len(models), 'higgsfieldWorkflows':len(workflows), 'higgsfieldHelpEntriesIncludingRoot':len(help_rows)}


if __name__ == '__main__':
    print(json.dumps(render(), sort_keys=True))
