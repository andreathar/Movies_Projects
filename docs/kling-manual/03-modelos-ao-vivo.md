# 03 · Modelos observados [SNAPSHOT]

> Atualização 16/10/2026: consultar [contrato V4 por interface](19-kling4-migration.md) e `shared/kling-capabilities.json` antes de escolher rota/custo. Tabelas e pilotos anteriores abaixo são evidência datada, sem liberação nova.

> Gerado por `tools/kling_model_sheet.py` — **não editar à mão**.
> Fonte: `snapshots/who_am_i.sanitized.json` (sha256 `3323ae5e3718bcd1585de6e59690be5e8f23e7e43780cec7fc1d0b4f9ae0e577`), capturado em 2026-10-12T04:07:41.305068+00:00 via `kling who_am_i`; `mcpVersion` 1.3.3.
> Snapshot datado, não cotação nem promessa de acesso futuro. Antes de produzir, consulte `kling who_am_i`, remova identidade e segredos e gere nova ficha.

## Índice rápido

| Ferramenta | Modelo padrão | Modelos disponíveis |
|---|---|---|
| `motion_control` | `kling-video-v3_0` | `kling-video-v2_6`, `kling-video-v3_0` |
| `image_to_video` | `kling-video-v3_0` | `kling-video-v2_5`, `kling-video-v2_6`, `kling-video-o1`, `kling-video-v3_0_omni`, `kling-video-v3_0`, `kling-video-v3_0_turbo` |
| `text_to_video` | `kling-video-v3_0_omni` | `kling-video-v2_5`, `kling-video-v2_6`, `kling-video-o1`, `kling-video-v3_0_omni`, `kling-video-v3_0`, `kling-video-v3_0_turbo` |
| `image_to_image` | `—` | `gemini-3.1-flash-image`, `gpt-image2`, `gemini-3-pro-image`, `kling-image-v3_0_omni`, `kling-image-o1`, `kling-image-v3_0`, `kling-image-v2_1` |
| `text_to_image` | `kling-image-v3_0_omni` | `gemini-3.1-flash-image`, `gpt-image-2`, `gemini-3-pro-image`, `kling-image-v3_0_omni`, `kling-image-o1`, `kling-image-v3_0`, `kling-image-v2_1` |
| `omni_ref_video` | `kling-video-v3_0_omni` | `kling-video-o1`, `kling-video-v3_0_omni` |

## `motion_control`

Padrão: `kling-video-v3_0`. **Sempre passe `--model` explicitamente.**

### `kling-video-v2_6`

- Alias: 可灵 2.6 动作控制, Kling 2.6 Motion Control
- Descrição (Kling): Apply an uploaded or saved motion to a subject image with precise action and expression control. To use motion control, refer to the tool motion_control. If no motion‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Prompt describing the desired scene, motion, or expression. Required; empty string is allowed for no text guidance. |
| `motionId` | não |  |  | Positive decimal motion ID returned by motion_library_list. Provide either motionId or a video input, but not both. |
| `motionDirection` | sim |  | image_direction, motion_direction | Direction reference. image_direction follows the subject image and only supports motions from 3 to 10 seconds; motion_direction follows the motion video. |
| `resolution` | não | 720p | 720p, 1080p | Output quality. 720p maps to std; 1080p maps to pro. |
| `keepOriginalSound` | não | true | true, false | Whether to retain the original sound from the motion video. |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image` | sim | Subject image URL containing a clear person or animal. |
| `video` | não | Motion-source video URL. Provide either this input or motionId, but not both. |

### `kling-video-v3_0`

- Alias: 可灵 3.0 动作控制, Kling 3.0 Motion Control
- Descrição (Kling): Apply an uploaded or saved motion to a subject image using Kling 3.0 for precise action and expression control. To use motion control, refer to the tool motion_control. If no motion‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Prompt describing the desired scene, motion, or expression. Required; empty string is allowed for no text guidance. To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times). |
| `motionId` | não |  |  | Positive decimal motion ID returned by motion_library_list. Provide either motionId or a video input, but not both. |
| `motionDirection` | sim |  | image_direction, motion_direction | Direction reference. image_direction follows the subject image and only supports motions from 3 to 10 seconds; motion_direction follows the motion video. |
| `resolution` | não | 720p | 720p, 1080p | Output quality. 720p maps to std; 1080p maps to pro. |
| `keepOriginalSound` | não | true | true, false | Whether to retain the original sound from the motion video. |
| `elements` | não |  |  | Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times). |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image` | sim | Subject image URL containing a clear person or animal. |
| `video` | não | Motion-source video URL. Provide either this input or motionId, but not both. |

## `image_to_video`

Padrão: `kling-video-v3_0`. **Sempre passe `--model` explicitamente.**

### `kling-video-v2_5`

- Alias: 可灵2.5, Video2.5, v2.5Turbo
- Descrição (Kling): This model is a great value and generate videos quickly

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the desired motion / scene. The input image is the primary driver. Required; empty string is allowed for pure image animation. |
| `duration` | não | 5 | 5, 10 | Video duration in seconds, support only 5s or 10s. |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request, max to 4. |
| `resolution` | não | 1080p | 720p, 1080p | Output resolution tier. 720p = std, 1080p = pro |
| `enable_audio` | não | true | true, false | Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio. |
| `enable_asmr` | não | false | true, false | Whether to enable ASMR mode for enhanced detail sound effects; suited to highly immersive content. Takes effect when enable_audio is 'true'. |
| `audio_prompt` | não |  |  | Sound-effect description, e.g. 木船吱呀声 (a creaking wooden boat). Takes effect when enable_audio is 'true'. |
| `music_prompt` | não |  |  | Background-music description, e.g. 悠远长笛旋律 (a distant flute melody). Takes effect when enable_audio is 'true'. |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `first_image` | sim | Source image URL used as the first frame to animate. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.) |
| `tail_image` | não | Optional tail (last-frame) image URL; when provided, the generated video transitions toward this frame. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.) |

### `kling-video-v2_6`

- Alias: 可灵2.6, Video2.6, v2.6
- Descrição (Kling): Video and sound generation model

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the desired motion / scene. The input image is the primary driver. Required; empty string is allowed for pure image animation. |
| `duration` | não | 5 | 5, 10 | Video duration in seconds. only support 5s or 10s |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request, max to 4. |
| `resolution` | não | 1080p | 720p, 1080p | Quality tier. 720p=std, 1080p=pro. Tail image requires 1080p. |
| `enable_audio` | não | true | true, false | Produce a work that includes audio. Only at resolution=1080p; not supported with a tail image. |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `first_image` | sim | Source image URL used as the first frame to animate. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.) |
| `tail_image` | não | Tail (last-frame) image URL; when provided, the generated video transitions toward this frame. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.) |

### `kling-video-o1`

- Alias: omni1, 可灵o1, o1-omni, video-o1
- Descrição (Kling): Unified video model with all-in-one multimodal instructions and exceptional consistency. To use features related to subject/element, refer to tools such as element_create. If no element‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the video to generate. To reference an input image, write 图片X in the prompt (图片1 = image_1, 图片2 = image_2, ...). up to 7 images are supported. To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times). |
| `duration` | não | 5 | 3, 4, 5, 6, 7, 8, 9, 10 | Video duration in seconds, support 3s to 10s. |
| `aspect_ratio` | não | 16:9 | 16:9, 9:16, 1:1 | Output video aspect ratio. |
| `resolution` | não | 1080p | 720p, 1080p | Quality tier (member: up to 1080p). |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request, max to 4. |
| `elements` | não |  |  | Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times). |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image_1` | sim | Reference image #1 (required). Up to 7 reference images are supported, named image_1 .. image_7, indexed from 1. Reference it in the prompt as 图片1. |
| `image_2` | não | Reference image #2 (optional). Up to 7 reference images (image_1 .. image_7). Reference it in the prompt as 图片2. |
| `image_3` | não | Reference image #3 (optional). Reference it in the prompt as 图片3. |
| `image_4` | não | Reference image #4 (optional). Reference it in the prompt as 图片4. |
| `image_5` | não | Reference image #5 (optional). Reference it in the prompt as 图片5. |
| `image_6` | não | Reference image #6 (optional). Reference it in the prompt as 图片6. |
| `image_7` | não | Reference image #7 (optional, max). Reference it in the prompt as 图片7. |

### `kling-video-v3_0_omni`

- Alias: kling3.0-omni, 可灵o3, v3-omni, omni3, video-o3
- Descrição (Kling): All-in-one multimodal input, voice-driven characters, and native audio output. Default model for multi-image to video generation (first-tail and multi image ref). For single-image to video generation, use kling3.0-turbo instead. Image-to-video only — no video input. For video-to-video (v2v), use omni_ref_video.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the video to generate. To reference an input image, write 图片X in the prompt (图片1 = image_1, 图片2 = image_2, ...). up to 7 images are supported. To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times). |
| `duration` | não | 5 | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Video duration in seconds, support 3s to 15s |
| `aspect_ratio` | não | 16:9 | 16:9, 9:16, 1:1 | Output video aspect ratio. |
| `resolution` | não | 1080p | 720p, 1080p, 4k | Quality tier. 720p=std, 1080p=pro. 4k for members. |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request. max to 4 |
| `prefer_multi_shots` | não | false | true, false | Whether to enable smart multi-shot splitting (intelligent shot composition). |
| `enable_audio` | não | true | true, false | Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio. |
| `elements` | não |  |  | Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times). |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image_1` | sim | Reference image #1 (required). Up to 7 reference images are supported, named image_1 .. image_7, indexed from 1. Reference it in the prompt as 图片1. |
| `image_2` | não | Reference image #2 (optional). Up to 7 reference images (image_1 .. image_7). Reference it in the prompt as 图片2. |
| `image_3` | não | Reference image #3 (optional). Reference it in the prompt as 图片3. |
| `image_4` | não | Reference image #4 (optional). Reference it in the prompt as 图片4. |
| `image_5` | não | Reference image #5 (optional). Reference it in the prompt as 图片5. |
| `image_6` | não | Reference image #6 (optional). Reference it in the prompt as 图片6. |
| `image_7` | não | Reference image #7 (optional, max). Reference it in the prompt as 图片7. |

### `kling-video-v3_0`

- Alias: kling3.0, 可灵3.0, 视频3.0
- Descrição (Kling): Enhanced native audio, improved element consistency, and support for multi-shot storytelling. To use features related to subject/element, refer to tools such as element_create. If no element‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the desired motion / scene. The input image is the primary driver. Required; empty string is allowed for pure image animation. To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times). |
| `duration` | não | 5 | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Video duration in seconds, support 3s to 15s. Longer durations may require prefer_multi_shots. |
| `resolution` | não | 1080p | 720p, 1080p, 4k | Quality tier (member: up to 4k). |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Quality tier (member: up to 4). |
| `prefer_multi_shots` | não | true | true, false | Whether to enable smart multi-shot splitting (intelligent shot composition). |
| `enable_audio` | não | true | true, false | Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio. |
| `elements` | não |  |  | Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times). |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `first_image` | sim | Source image URL used as the first frame to animate. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.) |
| `tail_image` | não | Optional tail (last-frame) image URL; when provided, the generated video transitions toward this frame. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.) |

### `kling-video-v3_0_turbo`

- Alias: kling3.0-turbo, video-3.0-turbo, v3-turbo, v3-fast, 3.0-fast
- Descrição (Kling): Consistently excellent results, with even better value. First choice for single-image to video generation. For multi-image to video generation, use kling3.0-omni instead.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the desired motion / scene. The input image is the primary driver. Required; empty string is allowed for pure image animation. |
| `duration` | não | 5 | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Video duration in seconds, support 3s to 15s. |
| `resolution` | não | 1080p | 720p, 1080p | Output resolution tier. 720p, 1080p |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request, max to 4. |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `first_image` | sim | Source image URL used as the first frame to animate. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.) |

## `text_to_video`

Padrão: `kling-video-v3_0_omni`. **Sempre passe `--model` explicitamente.**

### `kling-video-v2_5`

- Alias: 可灵2.5, Video2.5, v2.5Turbo
- Descrição (Kling): This model is a great value and generate videos quickly

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the video to generate. |
| `duration` | não | 5 | 5, 10 | Video duration in seconds, support only 5s or 10s. |
| `aspect_ratio` | não | 16:9 | 16:9, 9:16, 1:1 | Output aspect ratio. |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request, max to 4. |
| `resolution` | não | 1080p | 720p, 1080p | Output resolution tier. 720p = std, 1080p = pro |
| `enable_audio` | não | true | true, false | Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio. |
| `enable_asmr` | não | false | true, false | Whether to enable ASMR mode for enhanced detail sound effects; suited to highly immersive content. Takes effect when enable_audio is 'true'. |
| `audio_prompt` | não |  |  | Sound-effect description, e.g. 木船吱呀声 (a creaking wooden boat). Takes effect when enable_audio is 'true'. |
| `music_prompt` | não |  |  | Background-music description, e.g. 悠远长笛旋律 (a distant flute melody). Takes effect when enable_audio is 'true'. |

_Sem slots de input declarados._

### `kling-video-v2_6`

- Alias: 可灵2.6, Video2.6, v2.6
- Descrição (Kling): Video and sound generation model

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the video to generate. |
| `duration` | não | 5 | 5, 10 | Video duration in seconds. |
| `aspect_ratio` | não | 16:9 | 16:9, 9:16, 1:1 | Output aspect ratio. |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request, max to 4. |
| `resolution` | não | 1080p | 720p, 1080p | Quality tier. 720p=std, 1080p=pro. Tail image requires 1080p. |
| `enable_audio` | não | true | true, false | Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio. |

_Sem slots de input declarados._

### `kling-video-o1`

- Alias: omni1, 可灵o1, o1-omni, video-o1
- Descrição (Kling): Unified video model with all-in-one multimodal instructions and exceptional consistency.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the video to generate. |
| `duration` | não | 5 | 3, 4, 5, 6, 7, 8, 9, 10 | Video duration in seconds. |
| `aspect_ratio` | não | 16:9 | 16:9, 9:16, 1:1 | Output video aspect ratio. |
| `resolution` | não | 1080p | 720p, 1080p | Quality tier (member: up to 1080p). |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request, max to 4. |

_Sem slots de input declarados._

### `kling-video-v3_0_omni`

- Alias: kling3.0-omni, 可灵o3, v3-omni, omni3, video-o3
- Descrição (Kling): All-in-one multimodal input, voice-driven characters, and native audio output.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the video to generate. |
| `duration` | não | 5 | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Video duration in seconds, support 3s to 15s |
| `aspect_ratio` | não | 16:9 | 16:9, 9:16, 1:1 | Output video aspect ratio. |
| `resolution` | não | 1080p | 720p, 1080p, 4k | Quality tier. 720p=std, 1080p=pro. 4k for members. |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request. max to 4 |
| `prefer_multi_shots` | não | false | true, false | Whether to enable smart multi-shot splitting (intelligent shot composition). |
| `enable_audio` | não | true | true, false | Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio. |

_Sem slots de input declarados._

### `kling-video-v3_0`

- Alias: kling3.0, 可灵3.0, 视频3.0
- Descrição (Kling): Enhanced native audio, improved element consistency, and support for multi-shot storytelling.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the video to generate. |
| `duration` | não | 5 | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Video duration in seconds, support 3s to 15s. |
| `aspect_ratio` | não | 16:9 | 16:9, 9:16, 1:1 | Output aspect ratio. |
| `resolution` | não | 1080p | 720p, 1080p, 4k | Quality tier (member: up to 4k). |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Quality tier (member: up to 4). |
| `prefer_multi_shots` | não | true | true, false | Whether to enable smart multi-shot splitting (intelligent shot composition). |
| `enable_audio` | não | true | true, false | Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio. |

_Sem slots de input declarados._

### `kling-video-v3_0_turbo`

- Alias: kling3.0-turbo, video-3.0-turbo, v3-turbo, v3-fast, 3.0-fast
- Descrição (Kling): Consistently excellent results, with even better value.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the video to generate. |
| `duration` | não | 5 | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Video duration in seconds, support 3s to 15s. |
| `resolution` | não | 1080p | 720p, 1080p | Output resolution tier. 720p, 1080p |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request, max to 4. |
| `aspect_ratio` | não | 16:9 | 16:9, 9:16, 1:1 | Output video aspect ratio. |

_Sem slots de input declarados._

## `image_to_image`

Padrão: `(nenhum — escolha explícita)`. **Sempre passe `--model` explicitamente.**

### `gemini-3.1-flash-image`

- Alias: Nano Banana 2
- Descrição (Kling): Nano Banana 2 Flash (Gemini 3.1 Flash) image-to-image; single or multi-image reference (up to 10 via URL).

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Prompt for editing or composition. |
| `img_resolution` | não | 2k | 0.5k, 1k, 2k, 4k | Output resolution. max to 4k |
| `aspect_ratio` | não |  | 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9 | Output aspect ratio. Omit to keep the reference image ratio (auto). |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images per request (max 9). |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image_1` | sim | Reference image #1 (required). Up to 10 via URL. |
| `image_2` | não | Reference image #2 (optional; triggers multi-image mode). |
| `image_3` | não | Reference image #3 (optional; triggers multi-image mode). |
| `image_4` | não | Reference image #4 (optional; triggers multi-image mode). |
| `image_5` | não | Reference image #5 (optional; triggers multi-image mode). |
| `image_6` | não | Reference image #6 (optional; triggers multi-image mode). |
| `image_7` | não | Reference image #7 (optional; triggers multi-image mode). |
| `image_8` | não | Reference image #8 (optional; triggers multi-image mode). |
| `image_9` | não | Reference image #9 (optional; triggers multi-image mode). |
| `image_10` | não | Reference image #10 (optional; triggers multi-image mode). |

### `gpt-image2`

- Alias: GPT-Image2
- Descrição (Kling): GPT-Image2 image-to-image; single or multi-image reference (up to 10, total ≤ 50 MB).

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Prompt for editing or composition. |
| `img_resolution` | não | 2k | 1k, 2k, 4k | Output resolution. |
| `quality` | não | medium | low, medium, high | Image quality tier; affects pricing. |
| `aspect_ratio` | não | 1:1 | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | Output aspect ratio. |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images per request (max 9). |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image_1` | sim | Reference image #1 (required). Up to 10 total, ≤ 50 MB. |
| `image_2` | não | Reference image #2 (optional; triggers multi-image mode). |
| `image_3` | não | Reference image #3 (optional; triggers multi-image mode). |
| `image_4` | não | Reference image #4 (optional; triggers multi-image mode). |
| `image_5` | não | Reference image #5 (optional; triggers multi-image mode). |
| `image_6` | não | Reference image #6 (optional; triggers multi-image mode). |
| `image_7` | não | Reference image #7 (optional; triggers multi-image mode). |
| `image_8` | não | Reference image #8 (optional; triggers multi-image mode). |
| `image_9` | não | Reference image #9 (optional; triggers multi-image mode). |
| `image_10` | não | Reference image #10 (optional; triggers multi-image mode). |

### `gemini-3-pro-image`

- Alias: Nano Banana Pro, Gemini 3 Pro Image
- Descrição (Kling): Higher-fidelity edit / blend / restyle from reference images with Gemini 3 Pro (Nano Banana Pro). Supports up to 4K.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Describe the edits / target image. |
| `aspect_ratio` | não | 16:9 | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | Output aspect ratio. Omit to keep the reference image ratio (auto). |
| `img_resolution` | sim |  | 1k, 2k, 4k | Output resolution tier (up to 4K). |
| `image_count` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images to generate (1-9). |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image_1` | sim | Reference image #1 (required). |
| `image_2` | não | Reference image #2 (optional) — switches to multi-image mode. |

### `kling-image-v3_0_omni`

- Alias: kling3.0-omni, 可灵o3, v3-omni, omni3, image-o3
- Descrição (Kling): Enhanced narrative expression, native 2K/4K ultra-high definition output, and image series generation. Default model for image to image generation (single or multi image ref). To use features related to subject/element, refer to tools such as element_create. If no element‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Prompt describing the target image or edits. To reference an input image, write 图片X in the prompt (图片1 = image_1, 图片2 = image_2, ...). To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times). |
| `img_resolution` | não | 4k | 1k, 2k, 4k | Output resolution (member: up to 4k). |
| `aspect_ratio` | não | 3:4 | auto, 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9 | Output image aspect ratio. Set to 'auto' to let the model infer the aspect ratio from the input image. |
| `imageCount` | não | 1 | -1, 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images to generate per request (max 9). Default set to `-1` when `story_mode` is `true` and to let the model infer the count from the prompt. |
| `story_mode` | não | false | true, false | Story / group-image mode. Generate multiple image series which may be different depends on the prompt. (Different from imageCount, which will generate same contents.) When 'true', the model infers the number of output images from the prompt and imageCount is ignored; defaults to 'false' (single composition). |
| `elements` | não |  |  | Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times). |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image_1` | sim | Reference image #1 (required). Up to 10 reference images are supported, named image_1 .. image_10, indexed from 1. Reference it in the prompt as 图片1. (Must be url returned by file_upload tool, no local file path or external url allowed.) |
| `image_2` | não | Reference image #2 (optional). Up to 10 reference images (image_1 .. image_10). Reference it in the prompt as 图片2. (Must be url returned by file_upload tool, no local file path or external url allowed.) |
| `image_3` | não | Reference image #3 (optional). Reference it in the prompt as 图片3. |
| `image_4` | não | Reference image #4 (optional). Reference it in the prompt as 图片4. |
| `image_5` | não | Reference image #5 (optional). Reference it in the prompt as 图片5. |
| `image_6` | não | Reference image #6 (optional). Reference it in the prompt as 图片6. |
| `image_7` | não | Reference image #7 (optional). Reference it in the prompt as 图片7. |
| `image_8` | não | Reference image #8 (optional). Reference it in the prompt as 图片8. |
| `image_9` | não | Reference image #9 (optional). Reference it in the prompt as 图片9. |
| `image_10` | não | Reference image #10 (optional, max). Reference it in the prompt as 图片10. |

### `kling-image-o1`

- Alias: omni1, 可灵o1, o1-omni, image-o1
- Descrição (Kling): High feature consistency with precise detail editing and accurate style transfer. To use features related to subject/element, refer to tools such as element_create. If no element‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Prompt describing the target image or edits. To reference an input image, write 图片X in the prompt (图片1 = image_1, 图片2 = image_2, ...). To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times). |
| `img_resolution` | não | 2k | 1k, 2k | Output image resolution tier. |
| `aspect_ratio` | não | 3:4 | auto, 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9 | Output image aspect ratio. |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images to generate per request. |
| `elements` | não |  |  | Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times). |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image_1` | sim | Reference image #1 (required). Up to 10 reference images are supported, named image_1 .. image_10, indexed from 1. Reference it in the prompt as 图片1. (Must be url returned by file_upload tool, no local file path or external url allowed.) |
| `image_2` | não | Reference image #2 (optional). Up to 10 reference images (image_1 .. image_10). Reference it in the prompt as 图片2. (Must be url returned by file_upload tool, no local file path or external url allowed.) |
| `image_3` | não | Reference image #3 (optional). Reference it in the prompt as 图片3. |
| `image_4` | não | Reference image #4 (optional). Reference it in the prompt as 图片4. |
| `image_5` | não | Reference image #5 (optional). Reference it in the prompt as 图片5. |
| `image_6` | não | Reference image #6 (optional). Reference it in the prompt as 图片6. |
| `image_7` | não | Reference image #7 (optional). Reference it in the prompt as 图片7. |
| `image_8` | não | Reference image #8 (optional). Reference it in the prompt as 图片8. |
| `image_9` | não | Reference image #9 (optional). Reference it in the prompt as 图片9. |
| `image_10` | não | Reference image #10 (optional, max). Reference it in the prompt as 图片10. |

### `kling-image-v3_0`

- Alias: kling3.0, 可灵3.0, image3.0
- Descrição (Kling): Strengthen consistency, free multi-reference images, comprehensive effect upgrade. To use features related to subject/element, refer to tools such as element_create. If no element‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Image generation prompt. Use 图片1/图片N (image 1/N) to refer to the input reference image(s); describe the target image or the edits to apply. To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times). |
| `img_resolution` | não | 1k | 1k, 2k | Output image resolution tier. |
| `aspect_ratio` | não | 3:4 | auto, 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9 | Output aspect ratio. |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images to generate per request. |
| `elements` | não |  |  | Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times). |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image_1` | sim | Reference image #1 (required). Up to 10 reference images are supported, named image_1 .. image_10, indexed from 1. Reference it in the prompt as 图片1. (Must be url returned by file_upload tool, no local file path or external url allowed.) |
| `image_2` | não | Reference image #2 (optional). Up to 10 reference images (image_1 .. image_10). Reference it in the prompt as 图片2. (Must be url returned by file_upload tool, no local file path or external url allowed.) |
| `image_3` | não | Reference image #3 (optional). Reference it in the prompt as 图片3. |
| `image_4` | não | Reference image #4 (optional). Reference it in the prompt as 图片4. |
| `image_5` | não | Reference image #5 (optional). Reference it in the prompt as 图片5. |
| `image_6` | não | Reference image #6 (optional). Reference it in the prompt as 图片6. |
| `image_7` | não | Reference image #7 (optional). Reference it in the prompt as 图片7. |
| `image_8` | não | Reference image #8 (optional). Reference it in the prompt as 图片8. |
| `image_9` | não | Reference image #9 (optional). Reference it in the prompt as 图片9. |
| `image_10` | não | Reference image #10 (optional, max). Reference it in the prompt as 图片10. |

### `kling-image-v2_1`

- Alias: kling2.1, 可灵2.1, image2.1
- Descrição (Kling): Superb prompt adherence & reliable output.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the desired composition or edits. Required; empty string is allowed if no text guidance is needed. |
| `aspect_ratio` | não | 1:1 | 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9 | Output image aspect ratio. |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images to generate per request. |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `subject_image_0` | não | Subject reference image #0 (main subject to preserve). Subject images support indices 0-3 (up to 4). |
| `subject_image_1` | não | Subject reference image #1 (optional additional subject, indices 0-3, up to 4). |
| `subject_image_2` | não | Subject reference image #2 (optional additional subject, indices 0-3, up to 4). |
| `subject_image_3` | não | Subject reference image #3 (optional additional subject, indices 0-3, up to 4). |
| `scene_image` | não | Scene reference image (background / scene to compose into). Across all reference types (subject / scene / style), at least 2 reference images in total are required. |
| `style_image` | não | Style reference image (visual style to apply). Across all reference types (subject / scene / style), at least 2 reference images in total are required. |

## `text_to_image`

Padrão: `kling-image-v3_0_omni`. **Sempre passe `--model` explicitamente.**

### `gemini-3.1-flash-image`

- Alias: Nano Banana 2
- Descrição (Kling): Nano Banana 2 Flash (Gemini 3.1 Flash) text-to-image generation.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the image to generate. |
| `img_resolution` | não | 2k | 0.5k, 1k, 2k, 4k | Output resolution. |
| `aspect_ratio` | não | 16:9 | 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9 | Output aspect ratio. Omit to keep the reference image ratio (auto). |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images per request (max 9). |

_Sem slots de input declarados._

### `gpt-image-2`

- Alias: GPT-Image-2
- Descrição (Kling): GPT-Image-2 text-to-image generation.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the image to generate. |
| `img_resolution` | não | 2k | 1k, 2k, 4k | Output resolution. |
| `quality` | não | medium | low, medium, high | Image quality tier; affects pricing. |
| `aspect_ratio` | não | 1:1 | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | Output aspect ratio. |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images per request (max 9). |

_Sem slots de input declarados._

### `gemini-3-pro-image`

- Alias: Nano Banana Pro, Gemini 3 Pro Image
- Descrição (Kling): Google Gemini 3 Pro image model (Nano Banana Pro). Higher fidelity and complex-scene/text rendering. Supports up to 4K.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the image to generate. |
| `aspect_ratio` | não | 1:1 | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | Output image aspect ratio. |
| `img_resolution` | sim |  | 1k, 2k, 4k | Output resolution tier (up to 4K). |
| `image_count` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images to generate (1-9). |

_Sem slots de input declarados._

### `kling-image-v3_0_omni`

- Alias: kling3.0-omni, 可灵o3, v3-omni, omni3, image-o3
- Descrição (Kling): Enhanced narrative expression, native 2K/4K ultra-high definition output, and image series generation.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the image to generate. |
| `img_resolution` | não | 2k | 1k, 2k, 4k | Output resolution (member: up to 4k). |
| `aspect_ratio` | não | auto | auto, 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9 | Output image aspect ratio. Set to 'auto' to let the model infer the aspect ratio from the prompt. |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images to generate per request. max to 9 |

_Sem slots de input declarados._

### `kling-image-o1`

- Alias: omni1, 可灵o1, o1-omni, image-o1
- Descrição (Kling): High feature consistency with precise detail editing and accurate style transfer.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the image to generate. |
| `img_resolution` | não | 2k | 1k, 2k | Output image resolution tier, e.g. 1k / 2k. |
| `aspect_ratio` | não | 1:1 | 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9 | Output image aspect ratio. |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images to generate per request. |

_Sem slots de input declarados._

### `kling-image-v3_0`

- Alias: kling3.0, 可灵3.0, image3.0
- Descrição (Kling): Strengthen consistency, free multi-reference images, comprehensive effect upgrade.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the image to generate. |
| `img_resolution` | não | 2k | 1k, 2k | Output image resolution, e.g. 1k / 2k |
| `aspect_ratio` | não | 1:1 | 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9 | Output image aspect ratio, e.g. 1:1 / 3:4 / 16:9 |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images to generate, max to 9 |

_Sem slots de input declarados._

### `kling-image-v2_1`

- Alias: kling2.1, 可灵2.1, image2.1
- Descrição (Kling): Superb prompt adherence & reliable output.

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt describing the image to generate. |
| `img_resolution` | não | 2k | 1k, 2k | Output image resolution tier. |
| `aspect_ratio` | não | 3:4 | 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9 | Output image aspect ratio. |
| `imageCount` | não | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | Number of images to generate, max 9. |

_Sem slots de input declarados._

## `omni_ref_video`

Padrão: `kling-video-v3_0_omni`. **Sempre passe `--model` explicitamente.**

### `kling-video-o1`

- Alias: omni1, 可灵o1, o1-omni, video-o1
- Descrição (Kling): mix text, images, one reference video and image Element ids. Without video_1: up to 7 images, images+elements ≤7. With video_1: count provided image_* (any slots), images+elements ≤4. 1 video max. Image Elements ≤7; no video type Elements.
- `combinedItemCap`: `{"maxItems": 8, "arguments": ["elements"], "inputPrefixes": ["image_", "video_"]}`
- `combinedItemCaps`: `[{"maxItems": 4, "arguments": ["elements"], "inputPrefixes": ["image_"], "whenAnyInputPrefixes": ["video_"]}, {"maxItems": 7, "arguments": ["elements"], "inputPrefixes": ["image_"], "whenNoneInputPrefixes": ["video_"]}]`
- `elementSupport`: `{"imageElements": true, "videoElements": false, "maxImageElements": 7, "maxTotalElements": 7}`

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt. Reference an input image as 图片X (图片1=image_1, ...), the reference video as 视频1 (video_1). To reference a reusable image subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times). Video subjects are not supported. |
| `elements` | não |  |  | Optional reusable image subjects (Elements). JSON array string of {id, bindName, type}, e.g. [{"id":"12345","bindName":"Alice","type":"image"}]. 'id' and 'type' from element_get; type must be image (video subjects are not supported). At most 7 image subjects. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times). Without video_1, images+elements ≤7; with video_1, images+elements ≤4 (counted by how many image_* are provided, any slots).  |
| `duration` | não | 5 | 3, 4, 5, 6, 7, 8, 9, 10 | Output video duration in seconds (3 to 10). With a base/edit reference video, output duration may follow the input video (enforced downstream). |
| `aspect_ratio` | não | 16:9 | 16:9, 9:16, 1:1 | Output video aspect ratio. |
| `resolution` | não | 1080p | 720p, 1080p | Quality tier (member: up to 1080p). |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request, max to 4. |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image_1` | não | Reference image #1. Counted toward images+elements (≤7 without video_1, ≤4 with video_1). Any image_* slots may be used; the limit is the number provided, not the highest index. Ref as 图片1. |
| `image_2` | não | Reference image #2. Ref as 图片2. |
| `image_3` | não | Reference image #3. Ref as 图片3. |
| `image_4` | não | Reference image #4. Ref as 图片4. |
| `image_5` | não | Reference image #5. Ref as 图片5. Counted toward images+elements (≤7 without video_1, ≤4 with video_1). |
| `image_6` | não | Reference image #6. Ref as 图片6. Counted toward images+elements (≤7 without video_1, ≤4 with video_1). |
| `image_7` | não | Reference image #7. Ref as 图片7. Counted toward images+elements (≤7 without video_1, ≤4 with video_1). |
| `video_1` | não | Reference video #1 (max 1). This is the v2v input — use omni_ref_video, not image_to_video. MP4/MOV, 3–10s, ≤200MB, 720–2160px, 24–60fps (duration/size/aspect enforced downstream). With this video, images+elements ≤4 (count of provided image_* plus elements, any slots). Ref as 视频1. |

### `kling-video-v3_0_omni`

- Alias: kling3.0-omni, 可灵o3, v3-omni, omni3, video-o3
- Descrição (Kling): mix text, images, one reference video and image/video Element ids. Without video_1: up to 7 images, images+elements ≤7, video subjects ≤3. With video_1: count provided image_* (any slots), images+elements ≤4; video subjects allowed only when there are no images or image subjects, at most 1. 1 video max. Image+video Elements ≤7. Audio-video sync and multi-shot supported.
- `combinedItemCap`: `{"maxItems": 8, "arguments": ["elements"], "inputPrefixes": ["image_", "video_"]}`
- `combinedItemCaps`: `[{"maxItems": 4, "arguments": ["elements"], "inputPrefixes": ["image_"], "whenAnyInputPrefixes": ["video_"]}, {"maxItems": 7, "arguments": ["elements"], "inputPrefixes": ["image_"], "whenNoneInputPrefixes": ["video_"]}]`
- `elementSupport`: `{"imageElements": true, "videoElements": true, "maxImageElements": 7, "maxVideoElements": 3, "maxTotalElements": 7, "voiceConsistency": true, "maxVideoElementsWithVideoInput": 1}`

| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |
|---|---|---|---|---|
| `prompt` | sim |  |  | Text prompt. Reference an input image as 图片X (图片1=image_1, ...), the reference video as 视频1 (video_1). To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times). |
| `elements` | não |  |  | Optional reusable subjects (Elements). JSON array string of {id, bindName, type}, e.g. [{"id":"12345","bindName":"Alice","type":"image"}]. 'id' and 'type' from element_get (type is image or video). At most 7 image+video subjects combined; at most 3 may be video. Without video_1, images+elements ≤7. With video_1, images+elements ≤4 (count of provided image_* plus elements, any slots); video subjects are allowed only when there are no images or image subjects, at most 1. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times). |
| `duration` | não | 5 | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Output video duration in seconds (3 to 15). With video_1, the official panel typically limits duration to 3–10 (11–15 may be grey-gated downstream). With a base/edit reference video, output duration may follow the input video (enforced downstream). |
| `aspect_ratio` | não | auto | auto, 16:9, 9:16, 1:1 | Output video aspect ratio. Use auto when at least one image_* is provided (follow the input), or for a video-edit task whose video_1 is the base video. When video_1 is a reference video, pass a specific ratio: 16:9, 9:16 or 1:1. For text-only, pass 16:9, 9:16 or 1:1. |
| `resolution` | não | 1080p | 720p, 1080p, 4k | Quality tier. 720p=std, 1080p=pro. 4k for members. |
| `imageCount` | não | 1 | 1, 2, 3, 4 | Number of videos to generate per request. max to 4 |
| `prefer_multi_shots` | não | false | true, false | Whether to enable smart multi-shot splitting (intelligent shot composition). Downstream may force false for base-video edit and true for reference-video. |
| `enable_audio` | não | true | true, false | Generate new synced audio (音画同步). Only one of enable_audio and keepOriginalSound may be true. For new audio use enable_audio=true and keepOriginalSound=false. When video_1 is provided, enable_audio must be false. |
| `keepOriginalSound` | não | false | true, false | Keep the original sound of the reference video. Only one of enable_audio and keepOriginalSound may be true. To keep the source sound use keepOriginalSound=true and enable_audio=false. |

| Input (slot) | Obrig. | Descrição |
|---|---|---|
| `image_1` | não | Reference image #1. Counted toward images+elements (≤7 without video_1, ≤4 with video_1). Any image_* slots may be used; the limit is the number provided, not the highest index. Video-only v2v is allowed. Ref as 图片1. |
| `image_2` | não | Reference image #2. Ref as 图片2. |
| `image_3` | não | Reference image #3. Ref as 图片3. |
| `image_4` | não | Reference image #4. Ref as 图片4. |
| `image_5` | não | Reference image #5. Ref as 图片5. Counted toward images+elements (≤7 without video_1, ≤4 with video_1). |
| `image_6` | não | Reference image #6. Ref as 图片6. Counted toward images+elements (≤7 without video_1, ≤4 with video_1). |
| `image_7` | não | Reference image #7. Ref as 图片7. Counted toward images+elements (≤7 without video_1, ≤4 with video_1). |
| `video_1` | não | Reference video #1 (max 1). This is the v2v input — use omni_ref_video, not image_to_video. MP4/MOV, 3–10s, ≤200MB, 720–2160px, 24–60fps (duration/size/aspect enforced downstream). With this video, images+elements ≤4 (count of provided image_* plus elements, any slots), and enable_audio must be false. Video subjects are allowed only when there are no images or image subjects, at most 1. Ref as 视频1. |

