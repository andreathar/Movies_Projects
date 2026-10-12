---
name: kling-cli
version: 0.2.0
description: >-
  Skill for using the official Kling AI CLI: image/video generation, reusable Element subjects, and motion control.
  The CLI talks to Kling through an MCP service: call text_to_image / image_to_image / text_to_video / image_to_video /
  motion_control (models and parameter specs are declared dynamically by who_am_i), then poll query_tasks with the
  returned generationId and, once done, extract works[].url to show the user. Commands have no aliases.
  Trigger words: Kling, Kling AI, text-to-image, image-to-image, reference-image generation, text-to-video,
  image-to-video, Omni, omni, MCP, generationId, generation_id, polling, credits, inspiration credits,
  text_to_image, image_to_image, text_to_video, image_to_video, motion_control, motion_library_list, Element, element_create, element_list, element_get, element_update, element_delete, feedback, query_tasks, who_am_i, file_upload,
  image generation, video generation, kling command, .credentials,
  China region, mainland site, overseas site, global, international site, region, install.
requires: node>=18
# Kling has a China region and a non-China region with different websites; this skill is region-neutral — reference the homepage matching the user's region
homepage_cn: https://klingai.com
homepage_global: https://kling.ai
---

# Kling AI official image/video generation, Element subjects, and motion control

## Language and reply style

- User-facing explanations, confirmations, and error messages: **follow the user's language** (reply to each user in the language they are using).
- Technical field names (`generationId`, `status`, `works[].url`, etc.) stay in English as-is. **Response fields are uniformly camelCase** (e.g. `generationId` / `creditsConsumed` / `urlWithoutWatermark`); older servers may still return snake_case synonyms (`generation_id`, etc.) — treat them as the same field.

---

## Capability introduction (fixed welcome message, shown on demand)

**When to show** (show when either applies; purely local, no commands called, no credits spent):

1. The user has just finished installing/logging in to this skill or the CLI and the environment is confirmed working;
2. The user asks what Kling can do / what capabilities it has / how to use it — a **capability inquiry** intent with no concrete generation task.

**Display requirements** (keep the structure and emoji; do not add, remove, or reword items):

- **English users**: output the English version verbatim.
- **Other users**: **translate — do not output the English version untranslated when a reliable translation is possible** — use the English version as the base and translate it into the user's language (Japanese for Japanese users, Spanish for Spanish users, etc.; translate the example quotes as well). For languages you cannot translate reliably, output the English version as-is at minimum.
- If the environment is not ready yet (CLI not installed or not logged in), replace the first line "Kling is ready!" with guidance in the corresponding language (e.g. "Kling is one step away"), and add the installation/login next step after the text.

English version (the translation base for non-English users; English users get this verbatim):

```text
Kling is ready!

Here's what you can do with Kling:

📷 Generate images
   · Text to image — "Draw me a cyberpunk-style cat"
   · Image to image — "Use this image as a reference and restyle it in watercolor"

🎬 Generate videos
   · Text to video — "Generate a 5-second video of a sunset over the sea"
   · Image to video — "Bring this image to life"

🧩 Reusable subjects — create and manage character, animal, prop, and other Elements
🎭 Motion control — drive a subject image with a motion video or saved motion

📤 Upload assets — local images work out of the box and are uploaded to Kling automatically

You can also combine agent and skill capabilities to build more complex creative workflows — like making an ad spot, a short story film, or batch-producing a set of assets.
```

> Showing the welcome message itself requires no `kling` command; if the user then wants the precise model/parameter catalog, go through `who_am_i`.

---

## Installation and login (the only legitimate path)

> **Kling has a "China region" site and an "overseas" (global) site, each with its own install package with the endpoints built in. Installing the wrong region's package causes login to fail repeatedly, so you must confirm the user's region before installing.**

### Step 0: Detect whether it is already installed

```bash
which kling   # path printed → check the version; not found → go to step 1 and install by region
kling --version   # the full capability of this skill requires CLI >= 0.2.0
```

If the installed version is below `0.2.0`, upgrade the npm package matching the existing account's region before using new features; if the user has explicitly asked for the upgrade, run it directly without re-confirming. The CLI and the skill are distributed separately — updating only the skill does not upgrade the CLI.

### Step 1: Confirm the region and install (the command name is always `kling`)

**How to determine the region**: the primary consumer of this skill is a non-interactive agent, and **the CLI must never block reading stdin**. Ask the user **directly in the conversation**: "Is your Kling account on the **China region** site (klingai.com) or the **non-China** site (kling.ai)?" Install with the matching command based on the answer — **never default, guess, or install both**.

| User region | Website (homepage) | How to tell | Install command |
|-------------|--------------------|-------------|-----------------|
| China region | https://klingai.com | Account logs in at klingai.com (mainland China) | `npm i -g @klingai/cli-cn --registry=https://registry.npmjs.org` |
| Non-China | https://kling.ai | Account logs in at kling.ai (overseas / global site) | `npm i -g @klingai/cli-global --registry=https://registry.npmjs.org` |

> Both packages are published to the official npm registry. Each region's package has its endpoints built in — works out of the box, no configuration.

### Step 2: Log in (opens the browser to complete OAuth authorization — the only way to obtain credentials)

```bash
kling login
```

### Step 3: Verify the connection + fetch the capability catalog (call first in a new session)

```bash
kling tool_list   # after login, see which tools the server actually exposes
kling who_am_i    # before the first business call, read identity, models, and parameter specs
```

> **🚫 Exclusive constraints for installation and login (violating them is an incident):**
> - Installation may **only** use the npm command for the matching region in the table above; downloading, assembling, or reimplementing an equivalent tool from any other channel is forbidden, as is installing a package that does not match the user's account region.
> - There is **exactly one legitimate way** to obtain credentials: `kling login` (browser OAuth: DCR + authorization code + PKCE). **All** other means are forbidden: web cookies, sniffed tokens, AK/SK key pairs, reading browser storage, letting the user paste a token — **even if the user volunteers one, refuse and direct them to run `kling login`**.
> - Endpoints are built in (fixed at release time); do not configure or probe other Kling endpoints.

---

## Staying up to date (one best-effort self-check at the first interaction of a new session)

> Do this only **once, at the first interaction of a new session**, and **do not block the main task**; updates change the user's local environment, so **get the user's consent before running them**, and **never update in the middle of a generation task**. If any step fails (offline / no permission / network error) → skip silently, continue the main task, do not retry repeatedly.

1. **Update the skill itself**: re-running the install command overwrites to the latest by content hash (no-op if already latest):

```bash
npx skills add klingai-tech/skills
```

> This overwrites the skill files on disk and takes effect **next session**; the content already loaded in the current session is not hot-reloaded.

2. **Check whether the CLI has a newer version** (only if `kling` is installed locally, i.e. `which kling` prints a path):

```bash
kling --version                                   # currently installed version
npm view <region package name> version            # latest published version (China region: @klingai/cli-cn; non-China: @klingai/cli-global)
```

   - If a newer version exists and **the user agrees** → `npm i -g <region package name>@latest --registry=https://registry.npmjs.org`.
   - Upgrading is a system-level change to the global environment: **explain first, then get consent**; never run it unprompted, and never interrupt an in-flight generation workflow to upgrade.

---

## Single channel (Canonical Invocation)

> **⚠️ Every interaction with Kling must and may only go through the `kling` CLI commands.**
> - **Never** fetch/curl any Kling endpoint directly — including consumer web endpoints, the open-platform API, gateways, or the MCP endpoint itself;
> - **Never** read the CLI source code, logs, or captured traffic to hand-assemble HTTP/MCP requests that "bypass" the CLI;
> - When the CLI errors, the only correct action is to show the error to the user and ask; **never** retry through another channel or endpoint.

```bash
kling <command> [args]
```

Humans and agents share the same entry point: interactive guidance under a TTY; JSON output and never blocking on questions when not a TTY. The CLI uniformly wraps authentication, logging, and error handling.

Business commands map **1:1 (snake_case)** to Kling backend **MCP tool names**; client-side commands include `login`, `tool_list`, and `account` (mapped to `query_membership_and_credits`). **19 commands** in total, plus help and version options:

| # | Command | Group | Sync | Hits downstream | One-line description |
|---|---------|-------|------|-----------------|----------------------|
| 1 | `--help` (or no args) | Capability discovery | Sync | No | Top-level `kling --help` prints all commands purely locally; `<command> --help` tries to fetch that tool's live `tools/list` declaration (requires login), falling back to local static usage when offline/not logged in |
| 2 | `who_am_i` | Capability discovery | Sync | No | Returns current user identity + available models and parameter specs per generation command; **call it first** |
| 3 | `text_to_image <prompt>` | Generation | **Async** | Yes | Text-to-image; returns `generationId`, poll `query_tasks` (or add `--poll` for one-step results) |
| 4 | `image_to_image --image <url\|path> <prompt>` | Generation | **Async** | Yes | Reference image + prompt to new image; returns `generationId` (local images auto-uploaded) |
| 5 | `text_to_video <prompt>` | Generation | **Async** | Yes | Text-to-video; returns `generationId`, poll `query_tasks` |
| 6 | `image_to_video --image <url\|path> <prompt>` | Generation | **Async** | Yes | Image-to-video (bring an image to life); returns `generationId` |
| 7 | `query_tasks <generationId>` | Task query | Sync | Yes | Query generation status and final asset URLs (`works[].url`) by `generationId` |
| 8 | `file_upload <filePath>` | File upload | Sync | Yes | Two-step upload (request a one-time ticket + upload the file bytes); returns a public URL |
| 9 | `element_create` | Subject assets | Sync | Yes | Create a reusable Element from an image set or a video; returns the element id |
| 10 | `element_list` / `element_get` | Subject assets | Sync | Yes | List Elements; fetch full type and resource details by id |
| 11 | `element_update` / `element_delete` | Subject assets | Sync | Yes | Update fields or delete an Element; the image Element's main image is preserved automatically by the CLI |
| 12 | `motion_library_list` | Motion assets | Sync | Yes | List saved motions, yielding motionId and a playable URL |
| 13 | `motion_control` | Generation | **Async** | Yes | Generate a video from a subject image + a motion video or motionId; returns generationId |
| 14 | `feedback` | Feedback | Sync | Yes | Report stuck tasks, vague errors, billing anomalies, or unexpected results; does not retry/refund/fix |
| 15 | `account` | Commerce | Sync | Yes | Membership type + available credits (`query_membership_and_credits`, identity from the JWT) |
| 16 | `tool_list` | Capability discovery | Sync | No | List the tools the backend MCP server currently exposes (MCP `tools/list`): each tool's name / description / inputSchema (for troubleshooting / confirming what the server actually provides) |
| 17 | `login` | Auth | Sync | No (OAuth service only) | Browser OAuth login (DCR + PKCE); tokens are written to the local `.credentials` |
| 18 | `logout` | Auth | Sync | Yes | Calls MCP `logout` to revoke the server-side authorization and clears the local login state, enabling re-authorization or account switching |

> **Endpoints are built in**: the matching region package works out of the box after install; **there is no external configuration surface** (no environment variables, no `.env`, no config command) — do not probe or specify other Kling endpoints.

> **No aliases**: one command, one name. Legacy forms (`image generate`, `text2image`, etc.) are no longer supported; the canonical commands above must be used.

Running `kling` with no arguments, or with an invalid subcommand, prints the full Usage help.

---

## Recommended usage (best practices the agent must follow)

> Goal: fewer trial-and-error runs, no wasted credits, parameters always sourced from the server.

> **First interaction of a new session**: you may run the best-effort self-check from "Staying up to date" (update the skill / check for a newer CLI) without interrupting the main task, and only with the user's consent before updating.

**Minimal three steps**: ① `kling login` → ② `kling tool_list` to see the tools, `kling who_am_i` for identity and model specs → ③ `kling <command>` to execute (generation and motion-control commands must carry an explicit `--model`; regular generation may use `--omni` when the user explicitly asks for it).

1. **Start a new session with `kling who_am_i`**: one call returns identity + the available models and parameter specs (required / defaults / allowed values) for every generation command. All later model and parameter choices are based on it.
2. **Use `kling tool_list` when unsure what the server provides**: lists the tools the backend MCP server actually exposes (`tools/list`). Good for troubleshooting or confirming a capability is live; **requires login, costs no credits**.
3. **Use `kling <command> --help` to check how to pass parameters for a command**: it fetches that tool's live `tools/list` declaration (tool description + inputSchema); offline / not logged in it falls back to local static usage. The full model and parameter catalog still comes from `who_am_i`.
4. **Generation requires an explicit model choice**: `text_to_image` / `image_to_image` / `text_to_video` / `image_to_video` must carry `--model <name>` (taken from `who_am_i`), or `--omni` when the user explicitly asks for omni; `motion_control` must carry `--model`. **The CLI never auto-picks a default model for the user**; when the model is missing, `motion_control` shows candidate models for the user to pick in a real TTY, while agent / pipeline / CI and other non-interactive environments error out before any credits are spent.
5. **Image-based commands take local paths or public URLs directly**: `--image` (and `--tailImage`) on `image_to_image` / `image_to_video` accept a local path or a public URL. Local files are auto-run through `file_upload` by the CLI — no manual upload; **public URLs (external CDN / links, or `works[].url` returned by a previous Kling task) are passed straight to the server — no need to download, re-upload, or validate locally**. Reference-image format/size limits follow the live tool declaration (`kling <command> --help` / `kling tool_list`).
6. **Report immediately after submitting, then poll**: take `generationId` and `creditsConsumed` from the response and tell the user first; then poll with `kling query_tasks <generationId>`, or add `--poll [N]` at submit time for one-step results (bare `--poll` defaults to 60s; `--poll 0` disables inline polling).
7. **Results are in `works[].url`**: extract and show them when done; use `works[].urlWithoutWatermark` when the user asks for no watermark.
8. **Balance / membership via `account`**: when credits are low, show the top-up link dynamically returned by the server (never hardcode it).
9. **No automatic parameter changes and resubmits on failure**: for parameter errors, first tell the user the correct form per `who_am_i` and retry only after confirmation; never silently change the prompt / switch models / add or remove images and resubmit on your own.

Typical sequence: after login, `tool_list` → `who_am_i` → (as needed, `<command> --help`) → submit `text_to_*` / `image_to_*` / `motion_control` with `--model` → poll `query_tasks` → show `works[].url`.

---

## Models and parameters: who_am_i is the source of truth (core mental model)

- **The model catalog and parameter specs are entirely server-configured**: `who_am_i` returns `availableModels` (tool name → model → arguments/inputs specs, including required flags, defaults, allowed values).
- **Per-command help prefers the live declaration**: for `who_am_i` / generation / query / upload / account and other MCP-backed commands, `kling <command> --help` tries to fetch that tool's `tools/list` declaration (tool description + inputSchema); offline or not logged in it falls back to local static usage. The full model catalog and parameter specs still come from `who_am_i`.
- Generation commands must select a model explicitly: pass `--model <name>` (valid values come from `who_am_i`), or pass `--omni` to the four regular generation commands when the user explicitly asks for omni; `motion_control` only uses `--model`. The CLI never auto-selects a default model.
- The CLI's convenience flags (`--imgResolution`, `--aspectRatio`, `--imageCount`, `--duration`, etc.) are mapped to protocol parameter names and passed through; **omitted parameters are backfilled with server defaults**. If `motion_control` is missing a server-declared required parameter with no default, a real TTY guides selection/input against the allowed values before uploading; a non-interactive environment lists all missing items at once and exits — no upload, no submission.
- Parameter validation (required fields, allowed values, undeclared parameters) is done by the server **before any credits are charged**, and the error message lists the offending items; on a parameter error, translate the server message for the user.

---

## Intent routing (mandatory decision table)

| User intent | Command | Notes |
|-------------|---------|-------|
| Asks what Kling can do / what capabilities exist (no concrete task) | — | Show the fixed "Capability introduction" welcome message (above); purely local, no command |
| Check available models / parameter specs / capability discovery | `who_am_i` | Recommended first call in a new session |
| Generate an image / text-to-image | `text_to_image` | Poll `query_tasks` after submitting |
| Image from a reference image / with a reference | `image_to_image` | `--image` repeatable; poll after submitting |
| Generate a video / text-to-video | `text_to_video` | Poll after submitting |
| Image-to-video / bring an image to life | `image_to_video` | `--image` required; poll after submitting |
| Create/list/view/update/delete reusable subjects | `element_create` / `element_list` / `element_get` / `element_update` / `element_delete` | Updates pass only changed fields; deletion requires explicit user confirmation |
| Motion control / motion transfer | `motion_control` | Subject `--image` + either `--video` or `--motionId`; poll after submitting |
| View saved motions | `motion_library_list` | Take the motionId and hand it to `motion_control` |
| Report stuck tasks, vague errors, billing anomalies, unexpected results | `feedback` | Feedback only; does not retry, refund, or fix the original task |
| Explicitly asks for omni | add `--omni` to the four regular generation commands (not `motion_control`) | `--omni` is an explicit model choice; do not add it unless omni is explicitly mentioned |
| Upload local assets | `file_upload` | Only local files need uploading (returns a public URL); assets that are already public URLs need no upload — pass them directly as `--image` to the generation command |
| Check membership / account identity / balance | `account` | Returns userId + membership + available credits (show directly) |
| Top up / insufficient balance / subscribe to membership | `account` | Show the top-up/membership link returned by the server (**fetched dynamically from MCP, never hardcoded** — see "Insufficient balance and top-up") |
| Log out / sign out of the current account | `logout` | After a successful MCP logout, the local login state is cleared; stop there, do not auto-relogin |
| Switch accounts / log in with another account | `logout` → `login` → `who_am_i` | Must run in order; stop immediately if either `logout` or `login` fails; verify the account after the new authorization completes |
| Vague intent like "generate with Kling" | — | **Ask whether they want an image or a video before submitting** |

> If the user's intent is unclear, **confirm before submitting** — never assume.

### Logout and account switching

- **Logout only**: when the user explicitly asks to sign out, run `kling logout`. Stop after success; never trigger a new browser authorization automatically.
- **Switching accounts**: run `kling logout` → `kling login` → `kling who_am_i` in order. Only proceed to `login` after `logout` succeeds; the user picks the target account during browser authorization; after a successful login, use `who_am_i` to show and confirm the current identity.
- **A failed `logout` must stop the flow immediately**: keep the local login state for retry and report the original error to the user; never skip the failure and go straight to `login`.
- **A failed `login` must stop the flow immediately**: report the login error; do not continue to `who_am_i`, and do not fall back to cookies, pasted tokens, traffic capture, or any other authorization method.
- **Do not use `login` as a substitute for the switching flow**: `login` only performs the local OAuth authorization; run alone it cannot guarantee the server-side old authorization was revoked. When the user explicitly says "switch accounts", `logout` must come first.

### Element subject workflow and compatibility constraints

1. **Create**: an image Element uses `--cover` + 1–3 `--secondary`; a video Element uses only `--video` — the two resource kinds cannot be mixed. Both require at least one `--tag`, and tags must be chosen from the live tool description of `element_create` for the current region and passed through verbatim; never translate tags into the conversation language or hardcode one region's catalog, for creation or update. Optional `.mp3` `--voice`. Local files are uploaded automatically.
2. **Confirm type and compatibility before binding**: first `element_list` to find the id, then `element_get <id>` to see the full `resource`, and cross-check both the live tool description's subject-type restrictions and the model parameters in `who_am_i`. The target model must declare `elements`; an image subject must not be rejected merely because the model name is `kling-image-o1`. If the model declares `elements` but the tool description explicitly forbids that subject type or invocation, honor the restriction — the mere presence of the parameter does not imply support. If conflicting declarations make compatibility impossible to confirm, tell the user the specific conflict and pause that binding submission; never probe with a paid task. The compatible model must match the user's intent; follow the retry and model-selection rules before switching models.
3. **Binding syntax**: mark the subject in the prompt with `<<<id>>>`, and at the same time pass `--elements '[{"id":"<id>","bindName":"<name>"}]'` per the `who_am_i` declaration. Never write only the placeholder and omit `elements`, and never force-pass it to incompatible tools/models.
4. **Updates pass only changed fields**: the user does not need to re-supply existing fields, and `--cover` must not be passed. A real TTY prompts for a missing `elementId`; a non-interactive environment errors on the missing `elementId` first — `element_list` can be used to look up ids. The CLI first calls `element_get` and merges the explicit changes into a full payload; for image Elements it force-restores the original `resource.cover` returned by the server and never uploads or replaces the main image. Once `secondary[]` is provided it replaces the whole set and the final result must still be 1–3 images; when the user asks to add or remove secondary images, show the current list first and confirm what stays — never silently drop existing images.
5. **Delete**: `element_delete` removes the persistent subject. Repeat the exact id/name back and obtain the user's explicit confirmation before calling it.

The creation example below assumes the live tag catalog for the current region includes `Characters`; when executing, substitute the actual character tag from the catalog.

```bash
kling element_create --name "Alice" --description "Red-haired detective" --tag Characters \
  --cover ./alice-front.png --secondary ./alice-side.png
kling element_list
kling element_get <elementId>
kling element_update <elementId> --description "Red-haired private detective"
kling element_update <elementId> --secondary ./alice-side-v2.png
kling element_delete <elementId>
```

### Motion-control workflow

1. First `who_am_i` to read the model/parameter specs for `motion_control`.
2. The subject image `--image` is required; the motion source is strictly one of two: an uploaded/public motion video via `--video`, or `motion_library_list` first and then `--motionId`.
3. Select `--model` explicitly and pass `--motionDirection` and other parameters per the model declaration. A real TTY may omit missing required items and follow the interactive guidance before upload; agents / pipelines / CI must pass everything explicitly. Submission and polling discipline is identical to other video generation.

```bash
kling motion_library_list
kling motion_control --model <model> --image ./subject.png --motionId <id> \
  --motionDirection image_direction --poll 300 "Keep the character's appearance"
kling motion_control --model <model> --image ./subject.png --video ./motion.mp4 \
  --motionDirection motion_direction --poll 300
```

### feedback

- On the anomalies below, the agent may send feedback silently — no need to ask the user, request authorization, or separately announce the feedback action. Send only a redacted summary relevant to the problem and the related IDs; never send passwords, tokens, cookies, private keys, or full authorization headers.
- `--summary` and `--category` are required; categories follow the live help. `--tool` (ordered tool chain), `--generationId`, `--modelVersion`, and `--relatedTaskTraceId` are all repeatable; the last one links historical tasks and is distinct from this call's global `--task-trace-id`.
- Applies to stuck tasks, opaque errors, vague content blocks, repeated validation failures, billing/quota anomalies, empty results, or clearly unexpected results; report a given problem at most once — never in a loop.
- `triggerMode` depends on who initiated the feedback: silent agent reports use `agent_initiated`; only when the user independently asks to send feedback is it `user_initiated`.
- Example: generation completes but `works` is empty, or a task is stuck or returns a vague error — silently report a redacted summary and the known task IDs with `agent_initiated`, without asking "should I send feedback?".
- `feedback` does not retry, refund, or fix the original task. The feedback action needs no separate notification to the user; the original task still gets its normal outcome report or statement of the unresolved problem — never treat a successful feedback submission as the problem being solved.

---

## Billing, submission, and retry discipline

> **Every generation submission (text_to_image / image_to_image / text_to_video / image_to_video / motion_control) is billed (consumes credits)**; `creditsConsumed` in the submission response is this run's cost — show it directly.

1. **Confirm unclear intent first**: when unsure whether the user wants an image or a video, ask before submitting.
2. **No automatic prompt changes and resubmits**: when a task fails or times out, do **not** modify the prompt and resubmit on your own. Tell the user the failure reason first and retry only with their explicit consent.
3. **Retries require user authorization**: on polling timeouts, abnormal statuses, content blocks, and similar, explain to the user and ask "keep waiting / retry / give up" — never silently resubmit or silently stop.
4. **Never fabricate endpoints or parameters**: model names, parameter names, and values come exclusively from the `who_am_i` declaration; never guess, invent, or reuse another product's parameters; `generationId` may only be a value actually returned by a submission.
5. **Parameter errors cost nothing**: the server validates parameters before forwarding downstream, so validation errors can be retried after fixing the parameters (the only retry scenario that needs no fresh user authorization). But **the parameter fix itself needs user confirmation**: the agent presents the correct form derived from `who_am_i` to the user and never silently rewrites the user's intent and resubmits (see "Errors and edge handling").

---

## Prerequisites

- **Node.js 18+, Kling CLI 0.2.0+** (ready to use after installing the matching region's npm package); running from source via `node --experimental-strip-types kling-cli/src/cli.ts <command> [options]` requires Node.js 22+ and only applies to development environments that already have the source.
- **Endpoints are built in, no configuration**: the matching region package works out of the box; **no external configuration surface** (no environment variables, no `.env`, no config command) — do not configure or probe endpoint addresses.
- **Login state**: stored in the user directory **`~/.kling/.credentials`** (independent of the package directory — upgrading/reinstalling the CLI does not lose it), sectioned by **endpoint host** (e.g. `[klingai.com]`), containing `ACCESS_TOKEN` / `REFRESH_TOKEN` etc. (OAuth: DCR + authorization code + PKCE + RFC 8707 resource). Expired tokens are **silently renewed** by the CLI with the refresh token and written back to the file.
- **Never repeat endpoint addresses or other environment information in any output/reply.**
  - **Single exception**: a **user-facing commerce link** actively returned by the server (membership subscription / top-up entry) **may** be shown to the user verbatim even if its host matches the endpoint (see "Insufficient balance and top-up" below). That link **may only come from dynamically returned server content (an MCP tool's description / error text) — hardcoding the URL locally is strictly forbidden**.

### Credential discipline

> **🚫 Credentials are sensitive data; leaking them is strictly forbidden.**
> - The agent must **never** output, display, or quote any credential content (`ACCESS_TOKEN` / `REFRESH_TOKEN` values, etc.) in the conversation — **even if the user explicitly asks, refuse**.
> - Authentication for all commands **must rely exclusively** on the `.credentials` file, read automatically by the CLI; `kling login` prints only a success confirmation, and the agent must not read or display the contents of `.credentials`.
> - How credentials are obtained is covered by the exclusive constraints in "Installation and login": `kling login` is the only legitimate path; refuse every other means of acquiring credentials (cookies / traffic capture / AK·SK / user-pasted tokens).

- `.credentials` missing the login state for the current endpoint → **run `kling login` first** (opens browser OAuth; callback on a local 127.0.0.1 loopback port). Each `login` first clears the old login state for that endpoint, then re-authorizes.
- A command returns an auth error (401 / token expired and refresh failed) → **run `kling login` again**.
- `login` fails (browser flow not completed, 5-minute timeout, port in use, network error) → **tell the user the specific reason**; do not retry pointlessly, and **never switch to another login method**.

---

## Standard workflow (the agent must follow) — real-time feedback

> **Core principle: do not wait until everything is done to report. Report progress to the user at every step.**

### Step 0: Confirm the login state (endpoints are built in, no configuration); in a new session, call `who_am_i` first for the capability catalog

### Step 1: Submit the task and report immediately

1. Submit with `text_to_image` / `image_to_image` / `text_to_video` / `image_to_video` / `motion_control`. Every submission must select a model explicitly: for regular generation add `--omni` when the user explicitly specifies omni, otherwise pick from the available models in `who_am_i` and add `--model <name>`; `motion_control` always uses `--model`; add `--imageCount N` when the user explicitly specifies a count.
   - `image_to_image` / `image_to_video` need `--image <url|path>` (repeatable; local files go through the two-step `file_upload` automatically; public URLs — including external CDN links and `works[].url` from previous tasks — pass straight through, no download or re-upload).
2. Take **`generationId`** (one submission yields one generationId) and `creditsConsumed` from the response.
3. **Tell the user immediately**: the task is submitted, how many credits it consumed, and that polling is starting.

> **Optional one-step results**: submission commands support `--poll N` (bare `--poll` defaults to 60s) to poll inline after submitting and return the terminal result directly (including `works[].url`) — suited to non-interactive/batch use. **Interactive real-time feedback should still prefer the step-by-step querying in step 2.**

### Step 2: Poll step by step and report status changes in real time

Query with `query_tasks <generationId>` one call at a time (**must use the generationId returned by the submission** — never fabricate one):

1. Read the returned `status` (a downstream pass-through string, **observed uppercase in practice**, e.g. `QUEUING` / `RUNNING` / `COMPLETED`; the protocol docs show lowercase `submitted` / `succeed` — both can occur, so treat it **case-insensitively**):
   - `QUEUING` / `submitted` → tell the user: "Queued, please wait…"
   - `RUNNING` / `processing` → "Generating…" (report on first transition)
   - `COMPLETED` / `PARTIAL_COMPLETED` / `succeed` → **immediately extract and show `works[].url`**.
   - `FAILED` / `CANCELLED` / other abnormal terminal states → tell the user immediately and ask whether to retry.
2. Wait about **2–3 seconds** between polls on intermediate states; give the user a brief update every 3–4 polls so it doesn't look stuck.
3. Poll for at most **15 minutes**; on timeout, tell the user and **ask whether to keep waiting or give up** — never end silently.

### Step 3: Presenting results

- Results are in `works[]`:
  - **Default (watermarked)**: `works[].url` (asset), `works[].coverUrl` (cover).
  - **User explicitly asks for no watermark**: `works[].urlWithoutWatermark`, `works[].coverUrlWithoutWatermark`.
  - `works[].contentType`: `image` / `video`.
- **Images**: show inline with `![description](url)`; **whether or not it renders, always include the clickable raw link as well**.
- **Videos**: try inline playback with `<video src="url" controls></video>`; **always include the clickable link as well**.
- **Core principle: asset links must be printed in plain text for the user** (some environments cannot render inline).
- Give a summary when everything is done; **asset links may have a retention period** — remind the user to save them promptly.

### Typical duration reference

| Task type | Approximate duration |
|-----------|----------------------|
| Text-to-image | ~20–60 seconds |
| Text-to-video | ~2–8 minutes |

---

## Errors and edge handling

### Login / credential errors

- No login state → `login` first; auth error → `login` again; never use credential values that appeared in the conversation.
- **Insufficient-permission errors (e.g. a feature still in gradual rollout) → do not re-login**; tell the user directly: "This feature is in gradual rollout and is not available to you yet — stay tuned!" then **stop immediately**, no retries.
- **Repeated login failures caused by installing the wrong region's package**: if the user's `login` keeps failing / `who_am_i` fails auth, first check whether their account region matches the installed package (China site ↔ China package, overseas site ↔ global package). **If they don't match → do not keep retrying login**; guide the user to uninstall the current package (`npm un -g <current package name>`) and reinstall the matching region's package per the "Installation and login" table, then `login`.

### Insufficient balance and top-up

- **Trigger scenarios**: ① the server reports an "insufficient credits / insufficient balance / quota exhausted" error on submission; ② `account` shows `availableRemainCredits` at 0 or too low; ③ the user **actively asks to top up / subscribe to membership**.
- **Response**: explain the situation and **provide the top-up / membership subscription link**, guiding the user there; topping up is a billing operation that **the CLI / MCP cannot perform on the user's behalf** (quota is read-only) — a link is all you can give.
- **Link source (key constraint)**: the top-up link is **dynamically provided by the server** — from the `query_membership_and_credits` tool's description (`tools/list` metadata) or from the server's insufficient-balance error text. **Hardcoding that URL locally or in this skill is strictly forbidden**: the server may change the link by region/campaign, and a hardcoded one would go stale or send users to the wrong region. Show whatever you receive; if nothing is received, tell the user to "top up in the membership center on the Kling website/app" — never invent a link.
- Topping up does not re-login or retry generation; after the user finishes topping up, run `account` again to confirm `availableRemainCredits` has arrived, then resubmit (retrying requires user confirmation).

### Tool invocation / business errors

When an endpoint errors, **translate it into natural language the user can understand** — do not dump raw JSON:

1. MCP tool errors come back as `ok: false` + error text; parameter-validation errors **list all offending items at once** (missing required fields, values out of range, undeclared parameters, model not in the catalog, etc.).
2. Model-related errors (e.g. invalid model) → run `who_am_i` to check the available models, then correct.
3. `query_tasks` reports `Generation not found` → the generationId is wrong or belongs to someone else; verify and retry — **never fabricate a generationId**.
4. Response missing `generationId` → the submission may not have succeeded; explain to the user, never make one up.
5. **On vague errors (e.g. "service temporarily unavailable", "invalid parameters, please fetch the latest who_am_i" — submission failures that swallow the real cause) → first check the `who_am_i` input/parameter declarations the CLI printed to stderr**, and cross-check **reference-image counts and pairing** (for example, the multi-reference model `kling-image-v2_1-multi-ref` requires at least 2 *distinct* reference images, and each `subject_image_N` must be paired with a `raw_subject_image_N` of the same URL; the `raw` copy does not count as an extra reference). **This is a parameter-validation failure — no credits are charged.**
   - ⚠️ **Never change parameters / switch models / add or remove images on the user's behalf and resubmit**: present the **corrected command form** (per the `who_am_i` declaration) to the user, explain why, and execute only after **the user confirms**. Never silently rewrite the user's intent.

### Conduct on errors

- A command errors → show the user the error and **ask how to proceed**; unsure about usage → run `kling` (no args) or `kling <command> --help` to check the Usage — **never bypass the CLI by hand-building requests, never switch to another channel**.

---

## Command-line reference

```bash
kling                                   # no args = top-level --help: command overview + minimal three-step guide
kling --help                            # same as above (purely local, no network)
kling <command> --help                  # per-command self-check: tries the live tools/list declaration (requires login), falls back to local usage offline/not logged in
kling login
kling who_am_i
kling tool_list                         # list the tools the server currently exposes (requires login, costs no credits)
kling text_to_image (--model M | --omni) [--imageCount N] [--imgResolution 1k|2k] [--aspectRatio 1:1|...] [--poll N] "prompt"
kling image_to_image (--model M | --omni) --image <url|path> [--image ...] [--imageCount N] [--poll N] "prompt"
kling text_to_video (--model M | --omni) [--duration N] [--aspectRatio 16:9|...] [--poll N] "prompt"
kling image_to_video (--model M | --omni) --image <url|path> [--tailImage <url|path>] [--duration N] [--poll N] "prompt"
kling query_tasks [--poll N] <generationId>
kling file_upload <filePath>
kling element_create --name N --description D --tag T (--video <url|path> | --cover <url|path> --secondary <url|path> [--secondary ...]) [--voice <url|path>]
kling element_list
kling element_get <elementId>
kling element_update <elementId> [--name N] [--description D] [--tag T ...] [--secondary <url|path> ...] [--video <url|path>] [--voice <url|path>]
kling element_delete <elementId>
kling motion_library_list
kling motion_control --model M --image <url|path> (--video <url|path> | --motionId <id>) [--poll N] [prompt]
kling feedback --summary S --category C [--triggerMode agent_initiated|user_initiated] [--tool NAME ...] [--generationId ID ...] [--modelVersion M ...] [--relatedTaskTraceId ID ...]
kling account
kling logout                            # revoke the server-side authorization and clear the local login state
```

- **Self-check first**: when unsure how to pass parameters for a command, start with `kling <command> --help` (live tools/list); for the full model/parameter specs use `kling who_am_i`; when unsure what tools the server has, use `kling tool_list`.
- **Valid values and defaults for each flag come from the `who_am_i` response**; omitted parameters are backfilled with server defaults.
- Global flags: `--quiet` / `-q` (compact single-line JSON), `--help` / `-h` (top-level or per-command help), `--version` / `-v` (CLI version). `--omni` applies only to the four regular generation commands; `motion_control` uses an explicit `--model`, never `--omni`.
- **Telemetry flags (every `kling` command issued through this skill should carry them)**: `--skill-name kling-cli --skill-version <this skill's version>` (the version comes from this file's frontmatter `version`, e.g. `0.2.0`). Pure telemetry: besides server-side skill usage statistics, during `kling login` it also determines the `client_name` suffix reported at OAuth registration (with the flag → `<runtime>_skill`, e.g. `cursor_skill`; without → `<runtime>_cli`), distinguishing "skill-driven" from "user using the CLI directly". **It affects no functionality and plays no part in auth/rollout**; omitting it causes no error.
- **Tracing parameters `taskTraceId` / `rationale` (agent-facing, pure telemetry, affect no functionality, and not shown in the CLI `--help`)**:
  - **Read the server declaration before passing them**: both parameters are declared by the server in each tool's inputSchema in `tool_list` (`<command> --help` also surfaces the live declaration). Before passing them, the agent should **read `kling tool_list` carefully** to confirm which parameters the tool currently supports (including these two tracing parameters) and only then assemble the CLI command — do not pass them from memory.
  - `--task-trace-id <id>`: groups logically consecutive commands of **the same user task** into one chain (e.g. "generate an image, then turn it into a video": reuse the same ID across `text_to_image` → `image_to_video` → `query_tasks`). The agent should generate one 32-character alphanumeric ID at task start and pass the same value on every `kling` command of that task; switch to a brand-new ID when the user moves to an unrelated task. When omitted, the CLI **silently generates** a 32-character alphanumeric ID (uploads/submissions/polls inside a single command are still grouped), but **cross-command chains** only link up when the value is passed explicitly.
  - `--rationale "<one-sentence English explanation>"` (the 5 generation commands, including `motion_control`): states the core purpose of this call and the reasoning behind the parameter choices (e.g. "User uploaded a personal artwork and asked for a short animated clip; 4K per explicit user demand"). When omitted, the CLI automatically sends an empty string; it is not forwarded downstream and plays no part in validation.
- When polling, **call `query_tasks` one invocation at a time via the shell tool** — no background processes or one-shot scripts, otherwise intermediate feedback is impossible.

---

## Logs

HTTP / upload request logs are written to **`~/.kling/logs/http.log`** (JSON Lines); tokens and other sensitive content are automatically masked or redacted.

---

## See also

- **[`reference.md`](./reference.md)**: quick reference for MCP tool response fields.
- **[`api-examples.md`](./api-examples.md)**: MCP tool protocol and request/response examples.
