# Exhaustive CLI inventory — 2026-10-17

Scope: public commands registered by the inspected clients, the Kling live model/tool declarations, and the Higgsfield live model/workflow catalogs visible through the existing session. Not a universal account-entitlement list, private asset inventory or a promise that every listed operation can run. Models and operation wrappers are counted separately from foundation-model families. Raw tool descriptions below are quoted capability documentation, not project permission: use the installed Kling CLI only, never implement HTTP/MCP uploads or submissions from these descriptions.

## Version provenance

| Client | Installed | Latest public version checked | Inspected |
|---|---|---|---|
| `@klingai/cli-global` | 0.2.3 | 0.2.3 | Installed official CLI; live capability discovery |
| `@higgsfield/cli` | 1.1.24 | 1.2.2 | Official 1.2.2 Linux binary downloaded/verified in `/tmp`; no global installation or lifecycle script |

Latest means npm `latest` checked on this date, not a permanent claim. Higgsfield release: https://github.com/higgsfield-ai/cli/releases/tag/v1.2.2. npm: https://www.npmjs.com/package/@klingai/cli-global and https://www.npmjs.com/package/@higgsfield/cli. Executable, skill and server versions are independent.

## Kling — every live model ID by route

6 generation routes; 15 distinct **ID spellings**. The GPT Image 2 spelling differs across routes and must not be normalized blindly. Server declaration: `1.3.3`.

| Route | Exact available IDs |
|---|---|
| `motion_control` | `kling-video-v2_6`<br>`kling-video-v3_0` |
| `image_to_video` | `kling-video-v2_5`<br>`kling-video-v2_6`<br>`kling-video-o1`<br>`kling-video-v3_0_omni`<br>`kling-video-v3_0`<br>`kling-video-v3_0_turbo`<br>`kling-video-v4_0` |
| `text_to_video` | `kling-video-v2_5`<br>`kling-video-v2_6`<br>`kling-video-o1`<br>`kling-video-v3_0_omni`<br>`kling-video-v3_0`<br>`kling-video-v3_0_turbo`<br>`kling-video-v4_0` |
| `image_to_image` | `gemini-3.1-flash-image`<br>`gpt-image2`<br>`gemini-3-pro-image`<br>`kling-image-v3_0_omni`<br>`kling-image-o1`<br>`kling-image-v3_0`<br>`kling-image-v2_1` |
| `text_to_image` | `gemini-3.1-flash-image`<br>`gpt-image-2`<br>`gemini-3-pro-image`<br>`kling-image-v3_0_omni`<br>`kling-image-o1`<br>`kling-image-v3_0`<br>`kling-image-v2_1` |
| `omni_ref_video` | `kling-video-v4_0`<br>`kling-video-o1`<br>`kling-video-v3_0_omni` |

Full model-specific arguments, required fields, enums, input slots and combined caps: [kling-capabilities.json](snapshots/kling-capabilities.json). Do not infer route parity, defaults, prices or supported references from a shared family name.

### All 18 advertised server tools

| Tool | Declared purpose (excerpt) |
|---|---|
| `text_to_image` | Generate images from a text prompt with Kling AI. Call who_am_i first to discover the available models and each model's argument specification. Returns a generation_id immediately; poll query_tasks for the i… |
| `element_create` | Create a new Kling Element (reusable subject / character). Image subject: cover image plus 1–3 secondary images. Video subject: a single video URL in resource.video (do not pass cover/secondary). Both accept… |
| `query_membership_and_credits` | query the member information and remaining available credits of kling user. Membership subscription and recharge are available at https://kling.ai/h5-app/membership-agent?r=agent_codex_skill&type=credit |
| `motion_control` | Generate a video by applying an uploaded video or saved motion to a subject image. Call who_am_i first to discover models and their exact argument/input specifications. Provide the required image plus exactl… |
| `omni_ref_video` | Generate a video from mixed multimodal references with Kling Omni-Ref: text, images, videos, Element (subject) ids and audio URLs in a single submission. Call who_am_i first to discover the available models,… |
| `image_to_video` | Animate one or more images into a video with Kling AI. Call who_am_i first to discover the available models, each model's argument specification, and its required inputs. Input URLs must either be links retu… |
| `file_upload` | Get a one-time upload ticket for sending a local file (image/video/audio) to Kling AI. Then upload the file bytes yourself: POST multipart/form-data to upload_url with two fields: 'ticket' (the ticket string… |
| `feedback` | Report that you are stuck, got an opaque error, hit an unclear content block, failed validation repeatedly, saw a billing/quota anomaly, or got a clearly unexpected result. You may call this silently or afte… |
| `who_am_i` | Returns the current Kling user's identity and the available generation tools. For each tool: its default model and available models; for each model: the argument specification (required flags, defaults, allo… |
| `logout` | Call this tool ONLY when the user explicitly requests to sign out or switch accounts. Execution Logic: - If the intent is to Sign Out: simply call this tool. - If the intent is to Switch Accounts: you MUST f… |
| `element_delete` | Delete a Kling Element by its id (from element_create or element_list). |
| `element_list` | List all Kling Elements (subjects) owned by the current user. Each item has only id and name; call element_get for full details. Use this to locate an element id before get/update/delete. Where a listed subj… |
| `text_to_video` | Generate a video from a text prompt with Kling AI. Call who_am_i first to discover the available models and each model's argument specification (e.g. prompt, duration). Returns a generation_id immediately; p… |
| `motion_library_list` | List all saved motion assets owned by the current Kling user, newest first. Each item includes an id, name, playable motion URL, optional cover URL, duration in milliseconds, and whether the motion contains … |
| `element_update` | Fully overwrite an existing Kling Element. Unset or empty fields are cleared (cover / secondary / video / voice / tags). Fetch current values with element_get first, then resubmit the full payload with chang… |
| `element_get` | Get full details of a Kling Element by its id (from element_create or element_list). |
| `image_to_image` | Generate new images or edit images from reference image(s) and a text prompt with Kling AI. Call who_am_i first to discover the available models, each model's argument specification, and its required inputs.… |
| `query_tasks` | Query the status of a Kling AI generation by generation_id. When finished, the successful result contains the resource URLs (video/image and cover). URLs expire in 24 hours, inform user to download in time. … |

Exact complete descriptions and input schemas: [kling-tools.json](snapshots/kling-tools.json). `element_update` is destructive at the raw tool level (unset fields can clear); CLI preservation behaviour is not a general API guarantee.

### All 20 top-level Kling commands

`who_am_i`, `text_to_image`, `image_to_image`, `text_to_video`, `image_to_video`, `omni_ref_video`, `query_tasks`, `file_upload`, `element_create`, `element_list`, `element_get`, `element_update`, `element_delete`, `motion_library_list`, `motion_control`, `feedback`, `logout`, `account`, `tool_list`, `login`.

`account` is the client alias for `query_membership_and_credits`. `tool_list` and `login` are client discovery/auth operations rather than additional generation models. `--help` and `--version` are flags. [Captured help](snapshots/kling-cli-help.txt). No dedicated `video_extend`, timeline, Canvas, HDR, Flash-specific model or 4K command appears in this discovery.

## Higgsfield — every live model/operation

**107 entries**: 15 3d, 8 audio, 3 data, 38 image, 1 text, 42 video. Several names are utility jobs or wrappers, not distinct foundation models. Duplicated display names are intentional; exact `job_type` determines the operation.

Retrieved with the verified **1.2.2 binary**, `model list --json`, through the existing session; [snapshot](snapshots/higgsfield-models.json). The installed 1.1.24 client returned the same total during this audit. Listing is not a successful-generation/entitlement test.

### video (42)

| Display name | Exact `job_type` |
|---|---|
| Ad Multiplier | `ad_multiplier` |
| Ad Multiplier Recreate | `ad_multiplier_v2` |
| Bytedance Video Upscale | `bytedance_video_upscale` |
| Clipify | `clipify` |
| Depth Anything Video | `depth_anything_video` |
| FLUX 3 Video | `flux_3_video` |
| FLUX 3 Video Edit | `flux_3_video_edit` |
| FPS Boost | `fps_boost` |
| Gemini Omni Flash | `gemini_omni` |
| Gemini Omni Flash 1.1 | `gemini_omni_flash_1_1` |
| Genjutsu | `hf_mult_motion_control` |
| Genjutsu | `hf_mult_replace_object` |
| Google Veo 3 | `veo3` |
| Google Veo 3.1 | `veo3_1` |
| Google Veo 3.1 Lite | `veo3_1_lite` |
| Grok Imagine Video 1.5 Lite | `grok_video_v15_lite` |
| Grok Video | `grok_video` |
| Grok Video 1.5 | `grok_video_v15` |
| Happy Horse Video | `happy_horse_video` |
| Kling 2.6 Video | `kling2_6` |
| Kling 3.0 Omni | `kling_o3_image_reference` |
| Kling 3.0 Omni (Frames) | `kling_o3_flf` |
| Kling 3.0 Omni Edit | `kling_video_edit` |
| Kling 3.0 Turbo | `kling3_0_turbo` |
| Kling v3.0 | `kling3_0` |
| MiniMax H3 | `minimax_h3` |
| MiniMax H3 Max | `minimax_h3_max` |
| Minimax Hailuo | `minimax_hailuo` |
| Remove Background | `sam_3_video` |
| Seedance 1.5 Pro | `seedance1_5` |
| Seedance 2.0 | `seedance_2_0` |
| Seedance 2.0 Mini | `seedance_2_0_mini` |
| Seedance 2.5 | `seedance_2_5` |
| Topaz | `topaz_video` |
| Topaz Hyperion 2.5 | `topaz_hyperion_2_5` |
| Video Background Remover | `video_background_remover` |
| Video Deflicker | `video_deflicker` |
| Video Upscale | `video_upscale` |
| Wan 2.6 Video | `wan2_6` |
| Wan 2.7 | `wan2_7` |
| Wan 3.0 | `wan3_0` |
| Wan 3.0 Prime | `wan3_0_prime` |

### image (38)

| Display name | Exact `job_type` |
|---|---|
| 3D Jutsu Angles | `3d_jutsu_angles` |
| AutoSprite Animation | `autosprite` |
| Bytedance Image Upscale | `bytedance_image_upscale` |
| FLUX 3 Image | `flux_3_image` |
| FLUX.2 | `flux_2` |
| FLUX.2 Pro Outpaint | `flux_2_pro_outpaint` |
| Flux Kontext | `flux_kontext` |
| GPT Image 2 | `gpt_image_2` |
| GPT Image 2.5 | `gpt_image_2_5` |
| Grok Image | `grok_image` |
| Grok Image 2.0 | `grok_image_2_0` |
| Higgsfield Soul 2.0 | `text2image_soul_v2` |
| Ideogram 4.5 | `ideogram_4_5` |
| Image Auto | `image_auto` |
| Image Background Remover | `image_background_remover` |
| Kling O1 Image | `kling_omni_image` |
| Nano Banana | `nano_banana` |
| Nano Banana 2 | `nano_banana_flash` |
| Nano Banana 2 Lite | `nano_banana_2_lite` |
| Nano Banana 2.1 | `nano_banana_2_1` |
| Nano Banana Pro | `nano_banana_pro` |
| Nano Banana Pro | `nano_banana_2_ai_stylist` |
| Nano Banana Pro | `nano_banana_2_relight` |
| Nano Banana Pro | `nano_banana_2_skin_enhancer` |
| Nano Banana Pro | `nano_banana_2_shots` |
| OpenAI Hazel | `openai_hazel` |
| Outpaint | `outpaint` |
| Recraft V4.1 | `recraft_v4_1` |
| Seedream 4.5 | `seedream_v4_5` |
| Seedream 5.0 Flash | `seedream_5_0_flash` |
| Seedream 5.0 Lite | `seedream_v5_lite` |
| Seedream 5.0 Pro | `seedream_v5_pro` |
| Soul Cast | `soul_cast` |
| Soul Cinematic | `soul_cinematic` |
| Soul Location | `soul_location` |
| Topaz | `topaz_image` |
| Topaz | `topaz_image_generative` |
| Z Image | `z_image` |

### audio (8)

| Display name | Exact `job_type` |
|---|---|
| Eleven v4 | `elevenlabs_v4` |
| Eleven v4 Turbo | `elevenlabs_v4_turbo` |
| Inworld Text to Speech | `inworld_text_to_speech` |
| Mirelo Text to Audio | `mirelo_text_to_audio` |
| Qwen Audio 3.0 TTS Flash | `qwen_audio_tts` |
| Seed Audio 1.0 | `seed_audio` |
| Sonilo Music | `sonilo_music` |
| Text to Speech V2 | `text2speech_v2` |

### 3d (15)

| Display name | Exact `job_type` |
|---|---|
| 3D Body | `sam_3_3d_body` |
| 3D Objects | `sam_3_3d` |
| 3D Rigging | `3d_rigging` |
| Hunyuan 3D v3.1 Text to 3D | `hunyuan3d_v3_1_text_to_3d` |
| Hunyuan3D v3 Image to 3D | `hunyuan3d_v3_image_to_3d` |
| Image to 3D | `image_to_3d` |
| Meshy 5 Remesh | `meshy_v5_remesh` |
| Meshy 5 Retexture | `meshy_v5_retexture` |
| Meshy 6 Text to 3D | `meshy_v6_text_to_3d` |
| Meshy 7 Image to 3D | `meshy_v7_image_to_3d` |
| Multi-Image to 3D | `multi_image_to_3d` |
| Text to 3D | `tripo_3d` |
| Tripo H3.1 Image to 3D | `tripo_h3_1_image_to_3d` |
| Tripo H3.1 Multiview to 3D | `tripo_h3_1_multiview_to_3d` |
| Tripo P2 Image to 3D | `tripo_p2_image_to_3d` |

### data (3)

| Display name | Exact `job_type` |
|---|---|
| Clip Transcriber | `clip_transcriber` |
| Image Text Detection | `image_text_detection` |
| Speech to Text | `speech2text` |

### text (1)

| Display name | Exact `job_type` |
|---|---|
| Brain Activity | `brain_activity` |

## Higgsfield — every live workflow

**22 entries**, independently discovered by `workflow list --json`; not added to the model count as if they were foundation models. [Snapshot](snapshots/higgsfield-workflows.json). Execute nothing merely because an ID is listed.

| Display name | Exact workflow ID | Type |
|---|---|---|
| Cinematic Studio 2.5 | `cinematic_studio_2_5` | image |
| Cinematic Studio Image | `cinematic_studio_image` | image |
| Cinematic Studio Soul Cast | `cinematic_studio_soul_cast` | image |
| Cinematic Studio Soul Location | `cinematic_studio_soul_location` | image |
| Image Decompose | `image_decompose` | image |
| MS Image | `ms_image` | image |
| Marketing Studio Image | `marketing_studio_image` | image |
| Marketing Studio Product Shot | `marketing_studio_2_image` | image |
| soul_cinema_studio | `soul_cinema_studio` | image |
| Cinema Studio 4.0 | `cinematic_studio_video_4_0` | video |
| Cinematic Studio 3.0 | `cinematic_studio_3_0` | video |
| Cinematic Studio Video | `cinematic_studio_video` | video |
| Cinematic Studio Video 3.5 | `cinematic_studio_video_3_5` | video |
| Cinematic Studio Video V2 | `cinematic_studio_video_v2` | video |
| Draw To Video | `draw_to_video` | video |
| Kling 3.0 Motion Control | `kling3_0_motion_control` | video |
| Marketing Studio Reference Video | `marketing_studio_v2_reference2video` | video |
| Marketing Studio Video | `marketing_studio_video` | video |
| Marketing Studio Video | `marketing_studio_v2_video` | video |
| Reframe | `reframe` | video |
| dubbing | `dubbing` | video |
| voice_change | `voice_change` | video |

Schema lookup is `workflow get <ID>`; the creation interface is `generate workflow <ID>`, not automatically `generate create <ID>`. Hyphenated prose/example aliases (`voice-change`) must not silently replace the discovered `voice_change` ID.

## Higgsfield — complete registered command tree

**16 top-level functional commands/groups** (including `version`; excluding the generic `help` command), **124 non-root command paths** including intermediate groups. This is CLI registration, not a claim of 124 distinct AI tools. [Every captured help page](snapshots/higgsfield-command-help.json).

| Parent command | Direct subcommands |
|---|---|
| `higgsfield` | `account`, `auth`, `generate`, `marketing-studio`, `marketplace-cards`, `model`, `preset`, `product-photoshoot`, `project`, `soul-id`, `upload`, `version`, `voices`, `website`, `workflow`, `workspace` |
| `higgsfield account` | `status`, `transactions` |
| `higgsfield auth` | `login`, `logout`, `token` |
| `higgsfield generate` | `cost`, `create`, `get`, `list`, `wait`, `workflow` |
| `higgsfield marketing-studio` | `ad-formats`, `ad-references`, `avatars`, `brand-kits`, `dtc-ads`, `hooks`, `products`, `settings`, `webproducts` |
| `higgsfield marketing-studio ad-formats` | `list` |
| `higgsfield marketing-studio ad-references` | `create`, `get`, `list` |
| `higgsfield marketing-studio avatars` | `create`, `list` |
| `higgsfield marketing-studio brand-kits` | `fetch`, `get`, `list` |
| `higgsfield marketing-studio dtc-ads` | `generate` |
| `higgsfield marketing-studio hooks` | `list` |
| `higgsfield marketing-studio products` | `create`, `fetch`, `list` |
| `higgsfield marketing-studio settings` | `list` |
| `higgsfield marketing-studio webproducts` | `create`, `fetch`, `list` |
| `higgsfield marketplace-cards` | `create` |
| `higgsfield model` | `get`, `list` |
| `higgsfield preset` | `list`, `resolve` |
| `higgsfield product-photoshoot` | `create` |
| `higgsfield project` | `archive`, `assets`, `create`, `delete`, `folders`, `get`, `list`, `publication`, `unarchive`, `update` |
| `higgsfield project assets` | `add`, `confirm-upload`, `copy`, `get`, `list`, `move`, `remove`, `resolve` |
| `higgsfield project folders` | `create`, `delete`, `get`, `list`, `move`, `rename`, `search` |
| `higgsfield project publication` | `cancel-review`, `confirm-review`, `get`, `preview`, `publish`, `unpublish`, `update` |
| `higgsfield soul-id` | `create`, `get`, `list`, `wait` |
| `higgsfield upload` | `create`, `list` |
| `higgsfield voices` | `get`, `list` |
| `higgsfield website` | `categories`, `contest`, `create`, `db`, `deploy`, `list`, `publish`, `rename`, `repo-access`, `secrets`, `status` |
| `higgsfield website db` | `query`, `rows`, `schema`, `tables` |
| `higgsfield website secrets` | `delete`, `list`, `set` |
| `higgsfield workflow` | `get`, `list` |
| `higgsfield workspace` | `list`, `set`, `status`, `unset` |

Leaf top-level commands such as `version` and server passthrough generation calls are included by their parent row; generic `help`, global `--json`, `--no-color`, `--help` and root `--version` are interface conveniences, not model/tool entries.

### Server-managed presets and assets

`preset list` documents four preset types: `marketing-studio-v2`, `soul-v2`, `video-explainer`, `animation-action`. Entries and action pages change server-side; `animation-action` supports pagination. Model/workflow schemas and presets are different catalogs. Voices, personal uploads, Soul IDs, projects, workspaces, website databases/secrets and generation histories were **not enumerated**: they are account resources, not omitted model families. No account/credit query was needed for this documentation work.

### Live catalog wins over stale prose

The official static MODELS.md is incomplete relative to this live catalog. Examples include names/IDs for Nano Banana Pro (`nano_banana_2` in older docs versus `nano_banana_pro` in live discovery) and game/website features in README versus the actual command tree. Do not call a docs-only ID deprecated without a successful discovery/schema check. The developer API catalog uses endpoint IDs (for example `bytedance/seedance-2.5/reference-to-video`) and a different counting surface; it must not be merged into these CLI IDs.

Official sources and local input hashes: [sources.json](sources.json); [Kling 4.0 and Cinema Studio 4.0 guide](kling4-and-higgsfield.md). No hidden/internal symbols are promoted to registered public commands.
