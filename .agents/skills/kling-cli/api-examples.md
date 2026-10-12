# Kling MCP tool protocol and examples

The CLI is a thin client over Kling's backend MCP server: business calls are uniformly wrapped by the CLI and sent to the backend MCP tools (transport and auth details are handled by the CLI and need no attention). This document is a quick reference for the tool protocol; for the field quick reference see [`reference.md`](./reference.md).

## Tool list

| # | Tool name | Group | Sync | Hits downstream | One-line description |
|---|-----------|-------|------|-----------------|----------------------|
| 1 | `who_am_i` | Capability discovery | Sync | No | Identity + available models and parameter specs per generation tool; **call first in a new session** |
| 2 | `text_to_image` | Generation | **Async** | Yes | Text-to-image; returns `generationId`, poll `query_tasks` |
| 3 | `image_to_image` | Generation | **Async** | Yes | Reference image + prompt to image (needs inputs); returns `generationId` |
| 4 | `text_to_video` | Generation | **Async** | Yes | Text-to-video; returns `generationId`, poll `query_tasks` |
| 5 | `image_to_video` | Generation | **Async** | Yes | Image-to-video (needs inputs); returns `generationId` |
| 6 | `query_tasks` | Task query | Sync | Yes | Query generation status and final asset URLs by `generationId` |
| 7 | `file_upload` | File upload | Sync | Yes | Request a one-time upload ticket; the caller uploads the file bytes itself (two-step, see below) |
| 8 | `element_create` / `element_list` / `element_get` / `element_update` / `element_delete` | Subject assets | Sync | Yes | Full lifecycle of reusable Elements |
| 9 | `motion_library_list` | Motion assets | Sync | Yes | List the motions the current user has saved |
| 10 | `motion_control` | Generation | **Async** | Yes | Generate a video from a subject image + a motion video or motionId |
| 11 | `feedback` | Feedback | Sync | Yes | Report stuck tasks, billing anomalies, or unexpected results |
| 12 | `query_membership_and_credits` | Commerce | Sync | Yes | Query membership status and available credits (identity from the JWT, no parameters) |

> For the MCP-backed commands above, `kling <command> --help` tries to read that tool's live `tools/list` declaration (tool description + inputSchema); the full model catalog and parameter specs still come from `who_am_i`. Example: `kling image_to_image --help`.

The client also exposes `login`, `tool_list`, and `account` (mapped to `query_membership_and_credits`); `logout` calls the MCP tool of the same name and clears the local credentials on success. The full set of 19 CLI commands is in [SKILL.md](./SKILL.md). The JSON below documents the protocol — do not bypass the CLI and send requests directly.

## who_am_i

Request parameters: none (identity comes from the JWT). Example response:

```json
{
  "user": { "userId": 10000001 },
  "availableModels": {
    "text_to_image": [
      {
        "model": "kling-image-v3_0",
        "arguments": [
          { "name": "prompt", "required": true, "description": "Text prompt describing the image to generate" },
          { "name": "kolors_version", "required": false, "default": "3.0" },
          { "name": "img_resolution", "required": false, "default": "2k" },
          { "name": "aspect_ratio", "required": false, "default": "3:4" },
          { "name": "imageCount", "required": false, "default": "1", "description": "Number of images, max 9" }
        ],
        "inputs": []
      }
    ]
  },
  "authMode": "oauth"
}
```

- Model names, parameters, and defaults are all governed by the **runtime response** (server-side configuration).
- `arguments[]`: `required` fields never have defaults; an absent `allowedValues` means unrestricted; the server backfills `default` for omitted optional fields.

## Common protocol for generation tools

The 5 generation tools (including `motion_control`) share the same input envelope and response structure:

```json
{
  "model": "kling-image-v3_0",
  "arguments": [
    { "name": "prompt", "value": "two kids singing while running" },
    { "name": "imageCount", "value": "1" }
  ],
  "inputs": [
    { "name": "input", "inputType": "URL", "url": "https://cdn.example.com/ref.png" }
  ]
}
```

- `model` is required and must come from that tool's catalog in who_am_i.
- `arguments[].value` is **always a string**; omitted optional items are backfilled with server defaults.
- `inputs[].inputType` is currently only `"URL"`; `url` must be publicly reachable: external public URLs (CDN / external links, `works[].url` returned by previous tasks) are used directly, and local files go through `file_upload` first to obtain a URL. `text_to_*` usually has no inputs.
- Optional tracing parameters (pure telemetry — not validated, not forwarded downstream; governed by the inputSchema declarations in `tool_list`): `taskTraceId` (all tools; CLI global flag `--task-trace-id` — reuse the same ID across one task chain; when omitted, the CLI silently generates a 32-character alphanumeric ID) and `rationale` (the 5 generation tools; CLI flag `--rationale` — states the creative intent and parameter reasoning; when omitted, the CLI automatically sends an empty string).

The server validates locally before forwarding downstream (where billing happens); any failure yields a parameter error (**all offending items listed in aggregate**): the model is in the catalog, argument names are non-empty / unique / declared, required fields are present, values are in range — and the same for inputs.

Response (GenerationSubmitResult):

```json
{
  "generationId": "Qk1Zb3VyT3BhcXVlR2VuZXJhdGlvbklkRXhhbXBsZQ",
  "status": "submitted",
  "creditsConsumed": 10,
  "message": "Generation submitted. Poll query_tasks with this generationId to get the result."
}
```

## query_tasks

Request: `{ "generationId": "<the generationId verbatim>" }`. Response (completed; statuses observed uppercase in practice):

```json
{
  "generationId": "AIUbOyYx...",
  "status": "COMPLETED",
  "createTime": 1781164986117,
  "finishTime": 1781165014373,
  "works": [
    {
      "status": "COMPLETED",
      "contentType": "image",
      "url": "https://cdn.example.com/.../out.png",
      "urlWithoutWatermark": "https://.../out_clean.png",
      "coverUrl": "https://.../cover.jpg",
      "coverUrlWithoutWatermark": "https://.../cover_clean.jpg"
    }
  ]
}
```

- `status` is a downstream pass-through string — **treat it case-insensitively**; intermediate states `QUEUING`/`RUNNING`/`submitted`/`processing`, success `COMPLETED`/`PARTIAL_COMPLETED`/`succeed`.
- Invalid `generationId`, or one that belongs to another user → `Generation not found. Please verify the generationId.`

## file_upload (two-step)

Step one (MCP tool; all parameters optional but recommended):

```json
{ "filename": "photo.png", "contentType": "image/png", "size": 102400 }
```

Returns `{ "ticket": "...", "uploadUrl": "...", "expireAt": 1733900000 }`.

Step two (performed by the caller; already wrapped by the CLI): send a `multipart/form-data` POST to `uploadUrl` with the fields `ticket` (the ticket) + `file` (the file bytes). The upload response contains the file URL, usable as `inputs[].url`. Tickets are single-use and void after expiry.

## Element subjects

Image Element creation example (local paths are auto-uploaded by the CLI first): tags are chosen from the live tool description of `element_create` for the current region and passed through verbatim — never translated into the conversation language. The example below assumes the catalog contains `Characters`; when executing, replace the tags in the CLI command and payload with the actual character tags from the catalog.

```bash
kling element_create --name "Alice" --description "Red-haired detective" --tag Characters \
  --cover ./front.png --secondary ./side.png
```

Corresponding MCP payload:

```json
{
  "name": "Alice",
  "description": "Red-haired detective",
  "resource": {
    "cover": "https://cdn.example/front.png",
    "secondary": [
      { "inputType": "URL", "name": "secondary_1", "url": "https://cdn.example/side.png" }
    ]
  },
  "tags": ["Characters"]
}
```

A video Element replaces `resource` with `{ "video": "https://..." }`, with optional `voice`. `element_list` takes no parameters; `element_get` / `element_delete` take `{ "id": "..." }`. The CLI's `element_update` accepts optional changed fields and internally calls `element_get` first to compose the full payload; image Elements always keep the original `cover` returned by `element_get`, and the user does not pass `--cover`.

## Motion library and motion control

```bash
kling motion_library_list
kling motion_control --model <model from who_am_i> --image ./subject.png --motionId <ID from the motion library> \
  --motionDirection image_direction --poll 300
```

The `motion_control` envelope is the same as the other generation tools. The first item of `inputs` is the subject image; when using a motion video, the second item is the motion video, with the exact input names determined by the model declaration in `who_am_i`; when using the motion library, pass `motionId` in `arguments`. The two motion sources are strictly mutually exclusive — pick one.

## feedback

```bash
kling feedback --summary "Generation completed with an empty works list" \
  --category EMPTY_OR_PARTIAL_RESULT --triggerMode user_initiated \
  --tool image_to_video --tool query_tasks --generationId <id>
```

On stuck tasks, opaque errors, vague content blocks, repeated validation failures, billing/quota anomalies, empty results, or clearly unexpected results, the agent may send feedback silently — no need to ask the user, request authorization, or separately announce the feedback action. The `user_initiated` above applies only when the user actively asks to send feedback; silent agent reports use `agent_initiated`. `--category` follows the live tool declaration. Send only redacted summaries; `--modelVersion` and `--relatedTaskTraceId` are repeatable to link models and historical tasks. This tool only reports feedback — it does not retry, refund, or fix the original task; never report the same problem in a loop.

## query_membership_and_credits

Request parameters: none (identity comes from the JWT). Example response:

```json
{ "userId": 10000001, "membershipType": "NORMAL", "availableRemainCredits": 0 }
```

`membershipType`: `NORMAL` / `VIP` / `SVIP` / `SSVIP` / `SSSVIP`; `availableRemainCredits` is the user-visible credit amount — no conversion needed.

> The CLI's `account` command is a pass-through call to this tool.

## Tool discovery (CLI `tool_list`)

Used to inspect the tool metadata the backend MCP server actually exposes (`tools/list`) — for troubleshooting, confirming gradually rolled-out capabilities, or reading the dynamic notes in a tool's description.

```bash
kling tool_list
```

Response shape (inputSchema simplified; actual fields, required items, and value ranges follow the live result):

```json
{
  "ok": true,
  "status": 200,
  "body": {
    "tools": [
      {
        "name": "text_to_image",
        "description": "Submit text-to-image generation.",
        "inputSchema": { "type": "object", "properties": { "model": { "type": "string" }, "arguments": { "type": "array", "items": { "type": "object" } }, "inputs": { "type": "array", "items": { "type": "object" } } } }
      }
    ]
  }
}
```

## Authentication

Authentication is fully wrapped by `kling login` (browser OAuth); tokens are managed and renewed automatically by the CLI. **The only legitimate way** to obtain credentials is `kling login` — the agent has no need to, and must not, hand-build any auth request or read credential contents.
