# Kling CLI

Official Kling AI command-line tool for image/video generation, reusable Elements, and motion control.

- **Thin MCP client**: CLI commands map 1:1 to backend MCP tools such as `text_to_image` and `query_tasks`. The CLI handles argument translation, login, polling, and file upload.
- **Cross-platform**: macOS, Linux, and Windows. Requires Node.js 18+.
- **Agent-friendly**: stdout is JSON by default, and non-interactive environments never block on prompts.

## Installation

Kling has separate packages for different account regions. Both install the same `kling` command.

```bash
# Global site
npm i -g @klingai/cli-global

kling <command>
```

Use `@klingai/cli-cn` instead if your account belongs to the China site.

## Upgrade

```bash
npm i -g @klingai/cli-global@latest

kling --version
```

## Quick Start

```bash
# 1. Log in with OAuth in your browser.
kling login

# 2. Discover identity, models, and parameter specs.
kling who_am_i

# 3. Replace MODEL with a text_to_image model returned by who_am_i; wait up to 60 seconds.
kling text_to_image --model MODEL "a shiba inu sitting by a cafe window" --poll 60

# 4. Or submit first, then query with the returned generationId.
kling text_to_image --model MODEL "a shiba inu sitting by a cafe window"
kling query_tasks <generationId> --poll
```

Generated assets are returned in `works[].url`. Watermark-free URLs, when available, are returned in `works[].urlWithoutWatermark`.

## Commands

Generation and query commands use the same names as the backend MCP tools. There are no aliases.

| Command | Description |
|---|---|
| `who_am_i` | Return current identity plus available models and parameter specs. |
| `text_to_image --model MODEL <prompt>` | Submit text-to-image generation. |
| `image_to_image --model MODEL [options] [prompt]` | Generate from one or more reference images. |
| `text_to_video --model MODEL <prompt>` | Submit text-to-video generation. |
| `image_to_video --model MODEL [options] [prompt]` | Submit image-to-video generation. |
| `omni_ref_video --model MODEL <prompt>` | Mix images, videos, audio, and Elements into a new video. |
| `query_tasks <generationId>` | Query generation status and result URLs. |
| `file_upload <filePath>` | Upload a local file and return a public URL. |
| `element_create` | Create a reusable image or video Element. |
| `element_list` / `element_get` | List Elements or retrieve full details. |
| `element_update` / `element_delete` | Update selected fields or delete an Element; the CLI preserves image covers automatically. |
| `motion_library_list` | List saved motion assets. |
| `motion_control` | Generate video from a subject image plus a motion video or motionId. |
| `feedback` | Report a stuck task, billing anomaly, or unexpected result. |
| `account` | Query membership and available credits. |
| `tool_list` | List tools advertised by the backend MCP server. |
| `login` | Browser OAuth login. |
| `logout` | Revoke and clear saved login state. |

Options (`--model` and `--poll` apply only to commands that support them; the rest are global):

| Flag | Description |
|---|---|
| `--model <name>` | Select a model from `who_am_i` (required for generation commands). |
| `--skill-name <n>` / `--skill-version <v>` | Optional telemetry: identify the calling skill (forwarded to the server; on `login` it also picks the DCR `client_name` suffix `_skill`/`_cli`; never changes behavior). |
| `--poll [N]` | Poll for up to N seconds. Bare `--poll` defaults to 60. |
| `--quiet`, `-q` | Output compact single-line JSON. |
| `--help`, `-h` | Show top-level or per-command help. |
| `--version`, `-v` | Print CLI version. |

Run `kling <command> --help` for command-specific usage. For MCP-backed commands, generation help reads live model arguments and inputs from `who_am_i`; other MCP help reads `tools/list` (description + input schema) and falls back to local static usage when offline or not logged in.

## Models And Parameters

Available models, required arguments, defaults, and allowed values are declared by the server. Run `kling who_am_i` for the authoritative spec. Generation commands require an explicit `--model <name>` (the old `--omni` / `--flash` shorthands were removed). Other parameters you omit are filled by the server. Unknown parameters or invalid values are rejected before billing.

## Examples

### Text To Image

```bash
kling text_to_image --model kling-image-v3_0 "cyberpunk city at night" \
  --aspectRatio 16:9 --imgResolution 2k --imageCount 4 --poll 120

kling text_to_image --model kling-image-v3_0 "Mount Fuji in watercolor style" --poll
kling text_to_image --model kling-image-v3_0 "Mount Fuji in watercolor style" --poll
```

### Image To Image

```bash
kling image_to_image --model kling-image-v3_0 --image ./cat.jpg --image ./style.png \
  "Turn the cat in image 1 into the style of image 2" --poll 120
```

### Text To Video

```bash
kling text_to_video --model kling-video-v4_0 "drone shot flying over a snowy mountain peak" \
  --duration 10 --aspectRatio 16:9 --poll 300
```

### Image To Video

```bash
kling image_to_video --model kling-video-v4_0 --image ./first.jpg --tailImage ./last.jpg \
  "slow camera push-in" --duration 6 --poll 300

# Flash is first-frame only; --tailImage is rejected
kling image_to_video --model kling-video-v4_0_flash --image ./first.jpg --prompt "" --poll 300
```

Both `--image` and `--tailImage` fill slots **by name** as declared in `who_am_i` (`--image` fills the
non-tail slots in order, `--tailImage` always fills `tail_image`), so `--tailImage` on its own is a
valid tail-only job.

To place keyframes anywhere other than the first frame (tail only, middle only, first + middle +
tail, …), address each slot with `--input <name>=<url|path>`. Slot names are declared by the chosen
model in `who_am_i`, and `--input` cannot be combined with `--image` / `--tailImage`:

```bash
kling who_am_i                                 # see which input slots the model declares
kling image_to_video --model kling-video-v4_0 \
  --input tail_image=./last.png "end on this frame" --poll 300

# Standard V4: combine first, intermediate and tail frames, up to 10 images total
kling image_to_video --model kling-video-v4_0 \
  --input first_image=./first.jpg --input keyframe_1=./middle.jpg \
  --input tail_image=./last.jpg --prompt "" --poll 300

# When every frame is optional, the CLI allows text-only requests; the server validates the combination
# Use text_to_video for ordinary text-only generation
kling text_to_video --model kling-video-v4_0 "neon street push-in on a rainy night" --poll 300
```

Supplying more files than the model declares slots for (e.g. two images to first-frame-only Flash)
fails before anything is uploaded.

Standard V4 Preview supports `text_to_video`, `image_to_video`, and `omni_ref_video`.
The current declaration allows 3–30 seconds and 720p/1080p (subject to account access); Flash allows 3–20 seconds and 720p.
Use `who_am_i` as the authority. For standard V4 keyframes, `first_image`, `tail_image`, and `keyframe_1..10`
are optional, with a combined limit of 10 images. The CLI checks `combinedItemCap` before upload.
With a first frame, omit `--aspectRatio` unless explicitly requested; this entry does not accept `auto`.

### Omni-Ref

```bash
kling omni_ref_video --model kling-video-v4_0_flash --image ./ref.jpg --video ./clip.mp4 \
  "mix the image and video into a new shot" --poll 300

# Standard V4 mixed references; retaining source sound disables newly generated audio
kling omni_ref_video --model kling-video-v4_0 --image ./ref.jpg --video ./clip.mp4 \
  --keepOriginalSound true --enableAudio false "follow the reference camera movement" --poll 300

# Text-only example: no required references still means following model argument constraints
kling omni_ref_video --model kling-video-v3_0_omni --aspectRatio 16:9 "a long take of a seaside sunset" --poll 300

# Bind an existing Element; replace ELEMENT_ID and type with element_get values
kling element_get ELEMENT_ID
kling omni_ref_video --model kling-video-v4_0 \
  --elements '[{"id":"ELEMENT_ID","bindName":"Alice","type":"image"}]' \
  --aspectRatio 16:9 "<<<ELEMENT_ID>>> walks along the beach" --poll 300
```

Find subjects with `element_list`. `--elements` takes a JSON array string of `{id, bindName, type}`;
reference the same ID as `<<<id>>>` in the prompt. Elements can accompany `--image` and `--video`.
With Elements alone, choose an explicit ratio if the model's `auto` requires an image/video input.
See `kling omni_ref_video --help` for the full format and model-specific limits.

V4 Omni-Ref is billed per second, including input video duration. Its current declaration accepts up to
10 images, 5 videos, and 7 Elements (up to 3 video Elements), with 15 references combined.
Standalone audio depends on the live `audio_N` slots: the new standard 4.0 declaration supports up to
3 audio references; Flash declares none. Connections without audio slots reject `--audio`.
Local audio is automatically uploaded and counted toward the declared combined cap.
`enable_audio` and `keepOriginalSound` cannot both be true.
Confirm current limits and Element types with `who_am_i` and `element_get` before submitting.

### Task Query And Upload

```bash
kling query_tasks <generationId>
kling query_tasks <generationId> --poll 120
kling file_upload ./photo.jpg
kling account
```

### Elements And Motion Control

```bash
kling element_create --name "Alice" --description "red-haired detective" --tag 角色 \
  --cover ./front.png --secondary ./side.png
kling element_list
kling element_get <elementId>
kling element_update <elementId> --description "new description" # Other fields and the original cover are preserved

kling motion_library_list
kling motion_control --model <model> --image ./subject.png --motionId <id> \
  --motionDirection image_direction "跟随参考动作，保持主体外观" --poll 300
```

## Output And Exit Codes

stdout is formatted JSON by default. `--quiet` prints compact single-line JSON. Progress and diagnostics are written to stderr.

Exit codes: `0` for success, `1` for failure, and `130` for user cancellation.

Credentials are saved locally under `~/.kling/`. The CLI never prints tokens or secrets.

In a real terminal, `element_update` prompts for a missing `elementId` first; `motion_control` prompts for a missing model, motion source, and server-declared required generation arguments before uploading files. Non-interactive environments (agents, pipes, CI) never stop for prompts; missing values fail with a non-zero exit code.

## License

See `LICENSE` in the package.
