# Quick reference: MCP tool response fields

Full protocol and examples: **`api-examples.md`** in this directory. The CLI returns `{ ok, status, body }`, where `body` is the tool result (JSON text blocks already parsed).

> Response fields are uniformly **camelCase** (the server contract); older servers may still return snake_case synonyms (e.g. `generation_id`). The CLI parses both; read them as the same field in the output.

For MCP-backed commands, `kling <command> --help` tries to show that tool's live `tools/list` declaration (tool description + inputSchema); on failure it falls back to local static usage. The full model catalog and parameter specs are under `who_am_i` below.

## who_am_i (capability discovery)

- **`user.userId`**: current user ID (from the JWT).
- **`availableModels`**: tool name → model capability catalog; an empty `{}` means the server has not configured it yet.
  - **`[].model`**: model name (the valid values for the generation commands' `--model`).
  - **`[].alias`**: public alias (may be absent).
  - **`[].description`**: model description — **the agent's primary basis for model selection** (applicable scenarios, whether recommended, etc.; may be absent).
  - **`[].arguments[]`**: `{ name, required, default?, allowedValues?, description? }`.
  - **`[].inputs[]`**: `{ name, required, description? }` (reference-resource declarations).
- **`authMode`**: auth mode (`oauth` under an OAuth login).

## After a successful async generation submission (text_to_image / image_to_image / text_to_video / image_to_video / motion_control)

The subject library (`element_*`) is synchronous — see "Subject library (Element tools)" below; creating a subject returns a persistent subject `id` and does not use `generationId` or `query_tasks` polling.

- **`generationId`**: opaque generation ID used to poll `query_tasks`.
- **`status`**: initial status (downstream pass-through, e.g. `submitted` / `QUEUING`).
- **`creditsConsumed`**: credits consumed by this submission (may be absent).

## query_tasks

- **`generationId`**: echoes the queried ID.
- **`status`**: overall task status (downstream pass-through string, **treat case-insensitively**):
  - Intermediate: `QUEUING` / `RUNNING` / `submitted` / `processing`
  - Successful terminal: `COMPLETED` / `PARTIAL_COMPLETED` / `succeed`
  - Failed terminal: `FAILED` / `CANCELLED`, etc.
- **`createTime`** / **`finishTime`**: millisecond timestamps (`finishTime` is 0 while unfinished).
- **`works[]`**: list of outputs:
  - **`status`**: status of the individual output.
  - **`contentType`**: `image` / `video`.
  - **`url`**: asset URL (watermarked, shown by default).
  - **`urlWithoutWatermark`**: watermark-free asset URL (shown when the user asks).
  - **`coverUrl`** / **`coverUrlWithoutWatermark`**: cover URLs.

## file_upload (two-step)

- Step one (MCP tool) returns: **`ticket`** (one-time ticket), **`uploadUrl`** (upload address), **`expireAt`** (expiry timestamp).
- Step two is done automatically by the CLI: multipart POST (`ticket` + `file`) to `uploadUrl`; the CLI normalizes the file URL from the response into `body.url`.

## Subject library (Element tools)

- **`element_create`**: returns a persistent Element `id`; image resources are `cover` + 1–3 `secondary[]`, video resources are `video`, both with optional `voice`.
- **`element_list`**: each item has only `id` / `name`; the full type and resources require a follow-up `element_get`.
- **`element_get`**: returns the full `name` / `description` / `resource` / `tags`.
- **`element_update`**: the CLI reads the existing Element first, then merges the user-supplied optional fields into a full payload; image Elements have the original `resource.cover` force-restored and `--cover` is not accepted.
- **`element_delete`**: deletes the persistent Element by `id`.

## motion_library_list / motion_control

- **`motion_library_list`**: each item has `id`, `name`, the motion URL, an optional cover, the duration in milliseconds, and whether it has audio.
- **`motion_control`**: returns the same `generationId` / `status` / `creditsConsumed` as the other generation tools; follow up with `query_tasks`.

## feedback

- Returns the server's acknowledgment; this tool only records feedback — it does not retry, refund, or fix the original task.
- The request's `extra` may carry related `generationId[]` / `modelVersion[]` / `taskTraceId[]`, coming from the repeatable `--generationId` / `--modelVersion` / `--relatedTaskTraceId` flags respectively; do not assume the server response echoes these fields.

## logout

- Calls the server-side MCP `logout` first; on success, clears the local login state. On a server-side failure, the local login state is kept and the error is returned — login does not continue.

## account (pass-through to query_membership_and_credits)

- **`userId`**: user ID.
- **`membershipType`**: membership status (`NORMAL` / `VIP` / `SVIP` / `SSVIP` / `SSSVIP`).
- **`availableRemainCredits`**: available credits (the user-visible value, no conversion). When `0` or too low, guide the user to top up per "Insufficient balance and top-up".
- **Top-up / membership link**: not in the response body — provided dynamically by the server in the tool's **description (`tools/list` metadata)**. When guiding a top-up, use that link; **never hardcode it locally** (see SKILL "Insufficient balance and top-up").

## tool_list (MCP tools/list)

- **`body.tools[]`**: the tools the backend MCP server currently exposes.
- **`name`**: tool name; the CLI's canonical business commands usually map 1:1 to backend MCP tool names.
- **`description`**: the server-provided tool description; commerce links and other dynamic notes are governed by this — never hardcode them locally.
- **`inputSchema`**: the tool's JSON Schema input declaration, for troubleshooting or confirming which parameters the server actually supports.

## CLI polling results (--poll / query_tasks --poll)

- **`body.polled`**: true means this is an aggregated polling result.
- **`body.timedOut`**: whether it timed out (after a timeout you can keep going with `query_tasks <generationId>`).
- **`body.generations[]`**: `{ generationId, status, result }`, where `result` is the body of the last `query_tasks` response.
