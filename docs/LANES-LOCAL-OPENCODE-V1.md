# Local lane providers: `opencode` and `lmstudio` (v1)

Status: **prepared, not incorporated into the canonical policy documents.** Prepared 2026-10-18 in
an OpenCode session, outside a Parley lane and without a Parley participant identity.

This document adds no session, permission, assignment, authority or approval. It records how to run
two additional native CLIs as Parley lanes and how they map to the existing model policy.

## Why this is a separate document

`docs/MODEL_POLICY.md`, `docs/PARLEY_PROTOCOL.md`, `docs/COORDINATOR_PROTOCOL.md` and
`agents/README.md` are recorded with `sha256After` hashes in the still-pending handoff
`projects/andre-time-travel/agents/handoffs/2026-10-17-coordinator-skills-readiness-repair-v1.json`.
`manage.py lint` hard-checks those hashes until the handoff is ingested or superseded, so editing any
of the four out-of-band would create the same drift it reports. The producer incorporates the section
below by editing those files and re-recording the handoff; a lane does not.

## What already exists (no change needed)

`agent-parley` ships a built-in `opencode` provider preset:

```
Adapter: opencode · Command: opencode · Config home variable: OPENCODE_CONFIG_DIR
Hooks unavailable: SessionEnd · Delivery: hooks
```

That means an OpenCode lane is already runnable; only the policy text is missing:

```bash
# from the base checkout, as the operator, one terminal per lane
source scripts/lane_env.sh opencode-<label> <film-role> <scene-id>
agent-parley run opencode-<label> --provider opencode --repo "$PWD"
```

`scripts/lane_env.sh` is lane-name agnostic, so it already exports `MOVIES_LANE_NAME`,
`MOVIES_LANE_ROLE` and the Respan tags for these lanes.

## What was added for the local lane

Machine-level only, outside the repository:

| Where | What |
|---|---|
| `~/.local/state/agent-parley/providers.json` | New provider `lmstudio`: `adapter: opencode`, `command: opencode`, `home_env: OPENCODE_CONFIG_DIR`, `env: {OPENCODE_CONFIG_DIR: /home/athar/.config/opencode-lmstudio}`, `require_env: []`. |
| `~/.config/opencode-lmstudio/opencode.json` | Dedicated OpenCode config pinning the `lmstudio` provider (`@ai-sdk/openai-compatible`, `baseURL http://127.0.0.1:1234/v1`, dummy `apiKey`) and `model`/`small_model` to the local Gemma build. |

Why the dedicated config directory: `agent-parley` copies the provider's `OPENCODE_CONFIG_DIR` into
each lane as a private overlay (`OPENCODE_CONFIG_DIR` becomes the lane's config home). Pointing that
variable at `/home/athar/.config/opencode-lmstudio` gives the local lane its own model without
changing the default model of the cloud `opencode` lane.

```bash
# local lane, LM Studio's server must be running on 127.0.0.1:1234
source scripts/lane_env.sh lmstudio-<label> <film-role> <scene-id>
agent-parley run lmstudio-<label> --provider lmstudio --repo "$PWD"
```

Local models present on this machine: `lmstudio-community/gemma-4-E4B-it-GGUF` (Q4_K_M, selected) and
`lmstudio-community/gemma-4-E2B-it-GGUF`. LM Studio `http-server-config.json` listens on port 1234,
`127.0.0.1`, CORS on, just-in-time model loading on, no API key. A different model is chosen by
editing `model`/`small_model` and the `models` key in the config above.

## Serena

Serena is reached two more ways here:

- Local OpenAI-compatible model: Serena's `oaicompat-agent` context is the intended fit; the
  client-specific contexts (`claude-code`, `codex`) do not apply.
- OpenCode lanes: the lane overlay carries every non-Parley key of the source `opencode.json`
  unchanged. The repository's `.opencode/opencode.json` sets `"mcp": {}` deliberately
  (`docs/TOKEN_SPEND_AUDIT_2026-10-13.md`, action S2, measured −12.8k tokens/turn). Enabling a Serena
  MCP server for OpenCode lanes is therefore a separate, deliberate token-budget decision, not part
  of this change.

## Verification actually performed

| Check | Result |
|---|---|
| `agent-parley provider list` | lists `lmstudio` and `opencode` |
| `agent-parley provider show lmstudio` | adapter `opencode`, config home `OPENCODE_CONFIG_DIR`, env pinned as above |
| `agent-parley provider show opencode` | built-in preset, no overrides |
| `roster.providers()` resolution | both entries load; `codex-film` preserved |
| Local config JSON | parses; requires LM Studio's server for a live call |

**Not performed:** an end-to-end `agent-parley run` for either lane. That launches a real CLI session
and needs the Parley service up (`agent-parley up`) plus LM Studio's server running; it is the
operator's action, one terminal per lane, per `docs/PARLEY_PROTOCOL.md`.

## Text for the producer to incorporate

`docs/MODEL_POLICY.md` —— add after the existing `opencode` row:

| Lane (Parley participant) | Provider | Model | Where it is pinned | Why |
|---|---|---|---|---|
| `lmstudio` | `lmstudio` (`~/.local/state/agent-parley/providers.json`) | `lmstudio/lmstudio-community/gemma-4-E4B-it-GGUF` | `~/.config/opencode-lmstudio/opencode.json`, reached through the provider's `OPENCODE_CONFIG_DIR` | $0 local; nothing leaves the machine. Needs LM Studio's server on `127.0.0.1:1234`. |

`docs/PARLEY_PROTOCOL.md` —— extend "Gives: lanes (`claude`, `codex`)" to
"lanes (`claude`, `codex`, `opencode`, `lmstudio`)"; `agents/README.md` and
`docs/COORDINATOR_PROTOCOL.md` —— state that `opencode` and `lmstudio` are lanes/participants like
`claude` and `codex`, that the `opencode` preset is built in and `lmstudio` is a local provider, and
that neither inherits producer authority.

## Next action

Producer: incorporate the rows above into the four documents and re-record the handoff, or reject this
draft. Until then this file is the only place the two lanes are documented.
