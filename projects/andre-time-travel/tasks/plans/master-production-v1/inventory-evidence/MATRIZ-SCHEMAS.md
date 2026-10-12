# Matriz dos contratos arquivados — não é descoberta ao vivo

Fonte: `docs/kling-manual/snapshots/who_am_i.sanitized.json`, 2026-10-12 04:07:41 UTC, MCP 1.3.3. `tool_list.json`: 2026-10-09. Nenhuma consulta remota nesta tarefa.

`*` = obrigatório. Ausência de controle no schema não prova ausência de som no resultado. Listagem não comprova qualidade, preço nem autorização.

| Ferramenta | Modelo exato | Inputs (* obrigatório) | Argumentos, defaults e limites |
|---|---|---|---|
| motion_control | kling-video-v2_6 | image*, video | prompt*; motionId; motionDirection* {image_direction, motion_direction}; resolution=720p {720p, 1080p}; keepOriginalSound=true {true, false} |
| motion_control | kling-video-v3_0 | image*, video | prompt*; motionId; motionDirection* {image_direction, motion_direction}; resolution=720p {720p, 1080p}; keepOriginalSound=true {true, false}; elements max=1 |
| image_to_video | kling-video-v2_5 | first_image*, tail_image | prompt*; duration=5 {5, 10}; imageCount=1 {1, 2, 3, 4}; resolution=1080p {720p, 1080p}; enable_audio=true {true, false}; enable_asmr=false {true, false}; audio_prompt; music_prompt |
| image_to_video | kling-video-v2_6 | first_image*, tail_image | prompt*; duration=5 {5, 10}; imageCount=1 {1, 2, 3, 4}; resolution=1080p {720p, 1080p}; enable_audio=true {true, false} |
| image_to_video | kling-video-o1 | image_1*, image_2, image_3, image_4, image_5, image_6, image_7 | prompt*; duration=5 {3, 4, 5, 6, 7, 8, 9, 10}; aspect_ratio=16:9 {16:9, 9:16, 1:1}; resolution=1080p {720p, 1080p}; imageCount=1 {1, 2, 3, 4}; elements max=7 |
| image_to_video | kling-video-v3_0_omni | image_1*, image_2, image_3, image_4, image_5, image_6, image_7 | prompt*; duration=5 {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}; aspect_ratio=16:9 {16:9, 9:16, 1:1}; resolution=1080p {720p, 1080p, 4k}; imageCount=1 {1, 2, 3, 4}; prefer_multi_shots=false {true, false}; enable_audio=true {true, false}; elements max=7 |
| image_to_video | kling-video-v3_0 | first_image*, tail_image | prompt*; duration=5 {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}; resolution=1080p {720p, 1080p, 4k}; imageCount=1 {1, 2, 3, 4}; prefer_multi_shots=true {true, false}; enable_audio=true {true, false}; elements max=3 |
| image_to_video | kling-video-v3_0_turbo | first_image* | prompt*; duration=5 {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}; resolution=1080p {720p, 1080p}; imageCount=1 {1, 2, 3, 4} |
| text_to_video | kling-video-v2_5 | nenhum | prompt*; duration=5 {5, 10}; aspect_ratio=16:9 {16:9, 9:16, 1:1}; imageCount=1 {1, 2, 3, 4}; resolution=1080p {720p, 1080p}; enable_audio=true {true, false}; enable_asmr=false {true, false}; audio_prompt; music_prompt |
| text_to_video | kling-video-v2_6 | nenhum | prompt*; duration=5 {5, 10}; aspect_ratio=16:9 {16:9, 9:16, 1:1}; imageCount=1 {1, 2, 3, 4}; resolution=1080p {720p, 1080p}; enable_audio=true {true, false} |
| text_to_video | kling-video-o1 | nenhum | prompt*; duration=5 {3, 4, 5, 6, 7, 8, 9, 10}; aspect_ratio=16:9 {16:9, 9:16, 1:1}; resolution=1080p {720p, 1080p}; imageCount=1 {1, 2, 3, 4} |
| text_to_video | kling-video-v3_0_omni | nenhum | prompt*; duration=5 {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}; aspect_ratio=16:9 {16:9, 9:16, 1:1}; resolution=1080p {720p, 1080p, 4k}; imageCount=1 {1, 2, 3, 4}; prefer_multi_shots=false {true, false}; enable_audio=true {true, false} |
| text_to_video | kling-video-v3_0 | nenhum | prompt*; duration=5 {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}; aspect_ratio=16:9 {16:9, 9:16, 1:1}; resolution=1080p {720p, 1080p, 4k}; imageCount=1 {1, 2, 3, 4}; prefer_multi_shots=true {true, false}; enable_audio=true {true, false} |
| text_to_video | kling-video-v3_0_turbo | nenhum | prompt*; duration=5 {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}; resolution=1080p {720p, 1080p}; imageCount=1 {1, 2, 3, 4}; aspect_ratio=16:9 {16:9, 9:16, 1:1} |
| image_to_image | gemini-3.1-flash-image | image_1*, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9, image_10 | prompt*; img_resolution=2k {0.5k, 1k, 2k, 4k}; aspect_ratio {1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| image_to_image | gpt-image2 | image_1*, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9, image_10 | prompt*; img_resolution=2k {1k, 2k, 4k}; quality=medium {low, medium, high}; aspect_ratio=1:1 {1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| image_to_image | gemini-3-pro-image | image_1*, image_2 | prompt*; aspect_ratio=16:9 {1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9}; img_resolution* {1k, 2k, 4k}; image_count=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| image_to_image | kling-image-v3_0_omni | image_1*, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9, image_10 | prompt*; img_resolution=4k {1k, 2k, 4k}; aspect_ratio=3:4 {auto, 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9}; imageCount=1 {-1, 1, 2, 3, 4, 5, 6, 7, 8, 9}; story_mode=false {true, false}; elements max=10 |
| image_to_image | kling-image-o1 | image_1*, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9, image_10 | prompt*; img_resolution=2k {1k, 2k}; aspect_ratio=3:4 {auto, 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9}; elements max=10 |
| image_to_image | kling-image-v3_0 | image_1*, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9, image_10 | prompt*; img_resolution=1k {1k, 2k}; aspect_ratio=3:4 {auto, 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9}; elements max=10 |
| image_to_image | kling-image-v2_1 | subject_image_0, subject_image_1, subject_image_2, subject_image_3, scene_image, style_image | prompt*; aspect_ratio=1:1 {9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| text_to_image | gemini-3.1-flash-image | nenhum | prompt*; img_resolution=2k {0.5k, 1k, 2k, 4k}; aspect_ratio=16:9 {1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| text_to_image | gpt-image-2 | nenhum | prompt*; img_resolution=2k {1k, 2k, 4k}; quality=medium {low, medium, high}; aspect_ratio=1:1 {1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| text_to_image | gemini-3-pro-image | nenhum | prompt*; aspect_ratio=1:1 {1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9}; img_resolution* {1k, 2k, 4k}; image_count=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| text_to_image | kling-image-v3_0_omni | nenhum | prompt*; img_resolution=2k {1k, 2k, 4k}; aspect_ratio=auto {auto, 9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| text_to_image | kling-image-o1 | nenhum | prompt*; img_resolution=2k {1k, 2k}; aspect_ratio=1:1 {9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| text_to_image | kling-image-v3_0 | nenhum | prompt*; img_resolution=2k {1k, 2k}; aspect_ratio=1:1 {9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| text_to_image | kling-image-v2_1 | nenhum | prompt*; img_resolution=2k {1k, 2k}; aspect_ratio=3:4 {9:16, 2:3, 3:4, 1:1, 4:3, 3:2, 16:9, 21:9}; imageCount=1 {1, 2, 3, 4, 5, 6, 7, 8, 9} |
| omni_ref_video | kling-video-o1 | image_1, image_2, image_3, image_4, image_5, image_6, image_7, video_1 | prompt*; elements max=7; duration=5 {3, 4, 5, 6, 7, 8, 9, 10}; aspect_ratio=16:9 {16:9, 9:16, 1:1}; resolution=1080p {720p, 1080p}; imageCount=1 {1, 2, 3, 4} |
| omni_ref_video | kling-video-v3_0_omni | image_1, image_2, image_3, image_4, image_5, image_6, image_7, video_1 | prompt*; elements max=7; duration=5 {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}; aspect_ratio=auto {auto, 16:9, 9:16, 1:1}; resolution=1080p {720p, 1080p, 4k}; imageCount=1 {1, 2, 3, 4}; prefer_multi_shots=false {true, false}; enable_audio=true {true, false}; keepOriginalSound=false {true, false} |

## Restrições textuais por modelo

### motion_control / kling-video-v2_6
Apply an uploaded or saved motion to a subject image with precise action and expression control. To use motion control, refer to the tool motion_control. If no motion‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.
- `prompt`: Prompt describing the desired scene, motion, or expression. Required; empty string is allowed for no text guidance.
- `motionId`: Positive decimal motion ID returned by motion_library_list. Provide either motionId or a video input, but not both.
- `motionDirection`: Direction reference. image_direction follows the subject image and only supports motions from 3 to 10 seconds; motion_direction follows the motion video.
- `resolution`: Output quality. 720p maps to std; 1080p maps to pro.
- `keepOriginalSound`: Whether to retain the original sound from the motion video.
- `image`: Subject image URL containing a clear person or animal.
- `video`: Motion-source video URL. Provide either this input or motionId, but not both.
### motion_control / kling-video-v3_0
Apply an uploaded or saved motion to a subject image using Kling 3.0 for precise action and expression control. To use motion control, refer to the tool motion_control. If no motion‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.
- `prompt`: Prompt describing the desired scene, motion, or expression. Required; empty string is allowed for no text guidance. To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times).
- `motionId`: Positive decimal motion ID returned by motion_library_list. Provide either motionId or a video input, but not both.
- `motionDirection`: Direction reference. image_direction follows the subject image and only supports motions from 3 to 10 seconds; motion_direction follows the motion video.
- `resolution`: Output quality. 720p maps to std; 1080p maps to pro.
- `keepOriginalSound`: Whether to retain the original sound from the motion video.
- `elements`: Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times).
- `image`: Subject image URL containing a clear person or animal.
- `video`: Motion-source video URL. Provide either this input or motionId, but not both.
### image_to_video / kling-video-v2_5
This model is a great value and generate videos quickly
- `prompt`: Text prompt describing the desired motion / scene. The input image is the primary driver. Required; empty string is allowed for pure image animation.
- `duration`: Video duration in seconds, support only 5s or 10s.
- `imageCount`: Number of videos to generate per request, max to 4.
- `resolution`: Output resolution tier. 720p = std, 1080p = pro
- `enable_audio`: Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio.
- `enable_asmr`: Whether to enable ASMR mode for enhanced detail sound effects; suited to highly immersive content. Takes effect when enable_audio is 'true'.
- `audio_prompt`: Sound-effect description, e.g. 木船吱呀声 (a creaking wooden boat). Takes effect when enable_audio is 'true'.
- `music_prompt`: Background-music description, e.g. 悠远长笛旋律 (a distant flute melody). Takes effect when enable_audio is 'true'.
- `first_image`: Source image URL used as the first frame to animate. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.)
- `tail_image`: Optional tail (last-frame) image URL; when provided, the generated video transitions toward this frame. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.)
### image_to_video / kling-video-v2_6
Video and sound generation model
- `prompt`: Text prompt describing the desired motion / scene. The input image is the primary driver. Required; empty string is allowed for pure image animation.
- `duration`: Video duration in seconds. only support 5s or 10s
- `imageCount`: Number of videos to generate per request, max to 4.
- `resolution`: Quality tier. 720p=std, 1080p=pro. Tail image requires 1080p.
- `enable_audio`: Produce a work that includes audio. Only at resolution=1080p; not supported with a tail image.
- `first_image`: Source image URL used as the first frame to animate. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.)
- `tail_image`: Tail (last-frame) image URL; when provided, the generated video transitions toward this frame. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.)
### image_to_video / kling-video-o1
Unified video model with all-in-one multimodal instructions and exceptional consistency. To use features related to subject/element, refer to tools such as element_create. If no element‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.
- `prompt`: Text prompt describing the video to generate. To reference an input image, write 图片X in the prompt (图片1 = image_1, 图片2 = image_2, ...). up to 7 images are supported. To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times).
- `duration`: Video duration in seconds, support 3s to 10s.
- `aspect_ratio`: Output video aspect ratio.
- `resolution`: Quality tier (member: up to 1080p).
- `imageCount`: Number of videos to generate per request, max to 4.
- `elements`: Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times).
- `image_1`: Reference image #1 (required). Up to 7 reference images are supported, named image_1 .. image_7, indexed from 1. Reference it in the prompt as 图片1.
- `image_2`: Reference image #2 (optional). Up to 7 reference images (image_1 .. image_7). Reference it in the prompt as 图片2.
- `image_3`: Reference image #3 (optional). Reference it in the prompt as 图片3.
- `image_4`: Reference image #4 (optional). Reference it in the prompt as 图片4.
- `image_5`: Reference image #5 (optional). Reference it in the prompt as 图片5.
- `image_6`: Reference image #6 (optional). Reference it in the prompt as 图片6.
- `image_7`: Reference image #7 (optional, max). Reference it in the prompt as 图片7.
### image_to_video / kling-video-v3_0_omni
All-in-one multimodal input, voice-driven characters, and native audio output. Default model for multi-image to video generation (first-tail and multi image ref). For single-image to video generation, use kling3.0-turbo instead. Image-to-video only — no video input. For video-to-video (v2v), use omni_ref_video.
- `prompt`: Text prompt describing the video to generate. To reference an input image, write 图片X in the prompt (图片1 = image_1, 图片2 = image_2, ...). up to 7 images are supported. To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times).
- `duration`: Video duration in seconds, support 3s to 15s
- `aspect_ratio`: Output video aspect ratio.
- `resolution`: Quality tier. 720p=std, 1080p=pro. 4k for members.
- `imageCount`: Number of videos to generate per request. max to 4
- `prefer_multi_shots`: Whether to enable smart multi-shot splitting (intelligent shot composition).
- `enable_audio`: Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio.
- `elements`: Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times).
- `image_1`: Reference image #1 (required). Up to 7 reference images are supported, named image_1 .. image_7, indexed from 1. Reference it in the prompt as 图片1.
- `image_2`: Reference image #2 (optional). Up to 7 reference images (image_1 .. image_7). Reference it in the prompt as 图片2.
- `image_3`: Reference image #3 (optional). Reference it in the prompt as 图片3.
- `image_4`: Reference image #4 (optional). Reference it in the prompt as 图片4.
- `image_5`: Reference image #5 (optional). Reference it in the prompt as 图片5.
- `image_6`: Reference image #6 (optional). Reference it in the prompt as 图片6.
- `image_7`: Reference image #7 (optional, max). Reference it in the prompt as 图片7.
### image_to_video / kling-video-v3_0
Enhanced native audio, improved element consistency, and support for multi-shot storytelling. To use features related to subject/element, refer to tools such as element_create. If no element‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.
- `prompt`: Text prompt describing the desired motion / scene. The input image is the primary driver. Required; empty string is allowed for pure image animation. To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times).
- `duration`: Video duration in seconds, support 3s to 15s. Longer durations may require prefer_multi_shots.
- `resolution`: Quality tier (member: up to 4k).
- `imageCount`: Quality tier (member: up to 4).
- `prefer_multi_shots`: Whether to enable smart multi-shot splitting (intelligent shot composition).
- `enable_audio`: Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio.
- `elements`: Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times).
- `first_image`: Source image URL used as the first frame to animate. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.)
- `tail_image`: Optional tail (last-frame) image URL; when provided, the generated video transitions toward this frame. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.)
### image_to_video / kling-video-v3_0_turbo
Consistently excellent results, with even better value. First choice for single-image to video generation. For multi-image to video generation, use kling3.0-omni instead.
- `prompt`: Text prompt describing the desired motion / scene. The input image is the primary driver. Required; empty string is allowed for pure image animation.
- `duration`: Video duration in seconds, support 3s to 15s.
- `resolution`: Output resolution tier. 720p, 1080p
- `imageCount`: Number of videos to generate per request, max to 4.
- `first_image`: Source image URL used as the first frame to animate. (Must be url returned by file_upload tool, or a publicly accessible external file URL. No local file path.)
### text_to_video / kling-video-v2_5
This model is a great value and generate videos quickly
- `prompt`: Text prompt describing the video to generate.
- `duration`: Video duration in seconds, support only 5s or 10s.
- `aspect_ratio`: Output aspect ratio.
- `imageCount`: Number of videos to generate per request, max to 4.
- `resolution`: Output resolution tier. 720p = std, 1080p = pro
- `enable_audio`: Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio.
- `enable_asmr`: Whether to enable ASMR mode for enhanced detail sound effects; suited to highly immersive content. Takes effect when enable_audio is 'true'.
- `audio_prompt`: Sound-effect description, e.g. 木船吱呀声 (a creaking wooden boat). Takes effect when enable_audio is 'true'.
- `music_prompt`: Background-music description, e.g. 悠远长笛旋律 (a distant flute melody). Takes effect when enable_audio is 'true'.
### text_to_video / kling-video-v2_6
Video and sound generation model
- `prompt`: Text prompt describing the video to generate.
- `duration`: Video duration in seconds.
- `aspect_ratio`: Output aspect ratio.
- `imageCount`: Number of videos to generate per request, max to 4.
- `resolution`: Quality tier. 720p=std, 1080p=pro. Tail image requires 1080p.
- `enable_audio`: Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio.
### text_to_video / kling-video-o1
Unified video model with all-in-one multimodal instructions and exceptional consistency.
- `prompt`: Text prompt describing the video to generate.
- `duration`: Video duration in seconds.
- `aspect_ratio`: Output video aspect ratio.
- `resolution`: Quality tier (member: up to 1080p).
- `imageCount`: Number of videos to generate per request, max to 4.
### text_to_video / kling-video-v3_0_omni
All-in-one multimodal input, voice-driven characters, and native audio output.
- `prompt`: Text prompt describing the video to generate.
- `duration`: Video duration in seconds, support 3s to 15s
- `aspect_ratio`: Output video aspect ratio.
- `resolution`: Quality tier. 720p=std, 1080p=pro. 4k for members.
- `imageCount`: Number of videos to generate per request. max to 4
- `prefer_multi_shots`: Whether to enable smart multi-shot splitting (intelligent shot composition).
- `enable_audio`: Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio.
### text_to_video / kling-video-v3_0
Enhanced native audio, improved element consistency, and support for multi-shot storytelling.
- `prompt`: Text prompt describing the video to generate.
- `duration`: Video duration in seconds, support 3s to 15s.
- `aspect_ratio`: Output aspect ratio.
- `resolution`: Quality tier (member: up to 4k).
- `imageCount`: Quality tier (member: up to 4).
- `prefer_multi_shots`: Whether to enable smart multi-shot splitting (intelligent shot composition).
- `enable_audio`: Whether to enable audio-video sync. When 'true', the model directly produces a work that includes audio.
### text_to_video / kling-video-v3_0_turbo
Consistently excellent results, with even better value.
- `prompt`: Text prompt describing the video to generate.
- `duration`: Video duration in seconds, support 3s to 15s.
- `resolution`: Output resolution tier. 720p, 1080p
- `imageCount`: Number of videos to generate per request, max to 4.
- `aspect_ratio`: Output video aspect ratio.
### image_to_image / gemini-3.1-flash-image
Nano Banana 2 Flash (Gemini 3.1 Flash) image-to-image; single or multi-image reference (up to 10 via URL).
- `prompt`: Prompt for editing or composition.
- `img_resolution`: Output resolution. max to 4k
- `aspect_ratio`: Output aspect ratio. Omit to keep the reference image ratio (auto).
- `imageCount`: Number of images per request (max 9).
- `image_1`: Reference image #1 (required). Up to 10 via URL.
- `image_2`: Reference image #2 (optional; triggers multi-image mode).
- `image_3`: Reference image #3 (optional; triggers multi-image mode).
- `image_4`: Reference image #4 (optional; triggers multi-image mode).
- `image_5`: Reference image #5 (optional; triggers multi-image mode).
- `image_6`: Reference image #6 (optional; triggers multi-image mode).
- `image_7`: Reference image #7 (optional; triggers multi-image mode).
- `image_8`: Reference image #8 (optional; triggers multi-image mode).
- `image_9`: Reference image #9 (optional; triggers multi-image mode).
- `image_10`: Reference image #10 (optional; triggers multi-image mode).
### image_to_image / gpt-image2
GPT-Image2 image-to-image; single or multi-image reference (up to 10, total ≤ 50 MB).
- `prompt`: Prompt for editing or composition.
- `img_resolution`: Output resolution.
- `quality`: Image quality tier; affects pricing.
- `aspect_ratio`: Output aspect ratio.
- `imageCount`: Number of images per request (max 9).
- `image_1`: Reference image #1 (required). Up to 10 total, ≤ 50 MB.
- `image_2`: Reference image #2 (optional; triggers multi-image mode).
- `image_3`: Reference image #3 (optional; triggers multi-image mode).
- `image_4`: Reference image #4 (optional; triggers multi-image mode).
- `image_5`: Reference image #5 (optional; triggers multi-image mode).
- `image_6`: Reference image #6 (optional; triggers multi-image mode).
- `image_7`: Reference image #7 (optional; triggers multi-image mode).
- `image_8`: Reference image #8 (optional; triggers multi-image mode).
- `image_9`: Reference image #9 (optional; triggers multi-image mode).
- `image_10`: Reference image #10 (optional; triggers multi-image mode).
### image_to_image / gemini-3-pro-image
Higher-fidelity edit / blend / restyle from reference images with Gemini 3 Pro (Nano Banana Pro). Supports up to 4K.
- `prompt`: Describe the edits / target image.
- `aspect_ratio`: Output aspect ratio. Omit to keep the reference image ratio (auto).
- `img_resolution`: Output resolution tier (up to 4K).
- `image_count`: Number of images to generate (1-9).
- `image_1`: Reference image #1 (required).
- `image_2`: Reference image #2 (optional) — switches to multi-image mode.
### image_to_image / kling-image-v3_0_omni
Enhanced narrative expression, native 2K/4K ultra-high definition output, and image series generation. Default model for image to image generation (single or multi image ref). To use features related to subject/element, refer to tools such as element_create. If no element‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.
- `prompt`: Prompt describing the target image or edits. To reference an input image, write 图片X in the prompt (图片1 = image_1, 图片2 = image_2, ...). To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times).
- `img_resolution`: Output resolution (member: up to 4k).
- `aspect_ratio`: Output image aspect ratio. Set to 'auto' to let the model infer the aspect ratio from the input image.
- `imageCount`: Number of images to generate per request (max 9). Default set to `-1` when `story_mode` is `true` and to let the model infer the count from the prompt.
- `story_mode`: Story / group-image mode. Generate multiple image series which may be different depends on the prompt. (Different from imageCount, which will generate same contents.) When 'true', the model infers the number of output images from the prompt and imageCount is ignored; defaults to 'false' (single composition).
- `elements`: Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times).
- `image_1`: Reference image #1 (required). Up to 10 reference images are supported, named image_1 .. image_10, indexed from 1. Reference it in the prompt as 图片1. (Must be url returned by file_upload tool, no local file path or external url allowed.)
- `image_2`: Reference image #2 (optional). Up to 10 reference images (image_1 .. image_10). Reference it in the prompt as 图片2. (Must be url returned by file_upload tool, no local file path or external url allowed.)
- `image_3`: Reference image #3 (optional). Reference it in the prompt as 图片3.
- `image_4`: Reference image #4 (optional). Reference it in the prompt as 图片4.
- `image_5`: Reference image #5 (optional). Reference it in the prompt as 图片5.
- `image_6`: Reference image #6 (optional). Reference it in the prompt as 图片6.
- `image_7`: Reference image #7 (optional). Reference it in the prompt as 图片7.
- `image_8`: Reference image #8 (optional). Reference it in the prompt as 图片8.
- `image_9`: Reference image #9 (optional). Reference it in the prompt as 图片9.
- `image_10`: Reference image #10 (optional, max). Reference it in the prompt as 图片10.
### image_to_image / kling-image-o1
High feature consistency with precise detail editing and accurate style transfer. To use features related to subject/element, refer to tools such as element_create. If no element‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.
- `prompt`: Prompt describing the target image or edits. To reference an input image, write 图片X in the prompt (图片1 = image_1, 图片2 = image_2, ...). To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times).
- `img_resolution`: Output image resolution tier.
- `aspect_ratio`: Output image aspect ratio.
- `imageCount`: Number of images to generate per request.
- `elements`: Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times).
- `image_1`: Reference image #1 (required). Up to 10 reference images are supported, named image_1 .. image_10, indexed from 1. Reference it in the prompt as 图片1. (Must be url returned by file_upload tool, no local file path or external url allowed.)
- `image_2`: Reference image #2 (optional). Up to 10 reference images (image_1 .. image_10). Reference it in the prompt as 图片2. (Must be url returned by file_upload tool, no local file path or external url allowed.)
- `image_3`: Reference image #3 (optional). Reference it in the prompt as 图片3.
- `image_4`: Reference image #4 (optional). Reference it in the prompt as 图片4.
- `image_5`: Reference image #5 (optional). Reference it in the prompt as 图片5.
- `image_6`: Reference image #6 (optional). Reference it in the prompt as 图片6.
- `image_7`: Reference image #7 (optional). Reference it in the prompt as 图片7.
- `image_8`: Reference image #8 (optional). Reference it in the prompt as 图片8.
- `image_9`: Reference image #9 (optional). Reference it in the prompt as 图片9.
- `image_10`: Reference image #10 (optional, max). Reference it in the prompt as 图片10.
### image_to_image / kling-image-v3_0
Strengthen consistency, free multi-reference images, comprehensive effect upgrade. To use features related to subject/element, refer to tools such as element_create. If no element‑related tools appear in tool/lists, reconnect to the MCP server to refresh most updated tools by instruct the user to restart the current host and start a new session.
- `prompt`: Image generation prompt. Use 图片1/图片N (image 1/N) to refer to the input reference image(s); describe the target image or the edits to apply. To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times).
- `img_resolution`: Output image resolution tier.
- `aspect_ratio`: Output aspect ratio.
- `imageCount`: Number of images to generate per request.
- `elements`: Optional reusable subjects (Elements). JSON array string of {id, bindName}, e.g. [{"id":"12345","bindName":"Alice"}]. 'id' from element_create/element_list. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times).
- `image_1`: Reference image #1 (required). Up to 10 reference images are supported, named image_1 .. image_10, indexed from 1. Reference it in the prompt as 图片1. (Must be url returned by file_upload tool, no local file path or external url allowed.)
- `image_2`: Reference image #2 (optional). Up to 10 reference images (image_1 .. image_10). Reference it in the prompt as 图片2. (Must be url returned by file_upload tool, no local file path or external url allowed.)
- `image_3`: Reference image #3 (optional). Reference it in the prompt as 图片3.
- `image_4`: Reference image #4 (optional). Reference it in the prompt as 图片4.
- `image_5`: Reference image #5 (optional). Reference it in the prompt as 图片5.
- `image_6`: Reference image #6 (optional). Reference it in the prompt as 图片6.
- `image_7`: Reference image #7 (optional). Reference it in the prompt as 图片7.
- `image_8`: Reference image #8 (optional). Reference it in the prompt as 图片8.
- `image_9`: Reference image #9 (optional). Reference it in the prompt as 图片9.
- `image_10`: Reference image #10 (optional, max). Reference it in the prompt as 图片10.
### image_to_image / kling-image-v2_1
Superb prompt adherence & reliable output.
- `prompt`: Text prompt describing the desired composition or edits. Required; empty string is allowed if no text guidance is needed.
- `aspect_ratio`: Output image aspect ratio.
- `imageCount`: Number of images to generate per request.
- `subject_image_0`: Subject reference image #0 (main subject to preserve). Subject images support indices 0-3 (up to 4).
- `subject_image_1`: Subject reference image #1 (optional additional subject, indices 0-3, up to 4).
- `subject_image_2`: Subject reference image #2 (optional additional subject, indices 0-3, up to 4).
- `subject_image_3`: Subject reference image #3 (optional additional subject, indices 0-3, up to 4).
- `scene_image`: Scene reference image (background / scene to compose into). Across all reference types (subject / scene / style), at least 2 reference images in total are required.
- `style_image`: Style reference image (visual style to apply). Across all reference types (subject / scene / style), at least 2 reference images in total are required.
### text_to_image / gemini-3.1-flash-image
Nano Banana 2 Flash (Gemini 3.1 Flash) text-to-image generation.
- `prompt`: Text prompt describing the image to generate.
- `img_resolution`: Output resolution.
- `aspect_ratio`: Output aspect ratio. Omit to keep the reference image ratio (auto).
- `imageCount`: Number of images per request (max 9).
### text_to_image / gpt-image-2
GPT-Image-2 text-to-image generation.
- `prompt`: Text prompt describing the image to generate.
- `img_resolution`: Output resolution.
- `quality`: Image quality tier; affects pricing.
- `aspect_ratio`: Output aspect ratio.
- `imageCount`: Number of images per request (max 9).
### text_to_image / gemini-3-pro-image
Google Gemini 3 Pro image model (Nano Banana Pro). Higher fidelity and complex-scene/text rendering. Supports up to 4K.
- `prompt`: Text prompt describing the image to generate.
- `aspect_ratio`: Output image aspect ratio.
- `img_resolution`: Output resolution tier (up to 4K).
- `image_count`: Number of images to generate (1-9).
### text_to_image / kling-image-v3_0_omni
Enhanced narrative expression, native 2K/4K ultra-high definition output, and image series generation.
- `prompt`: Text prompt describing the image to generate.
- `img_resolution`: Output resolution (member: up to 4k).
- `aspect_ratio`: Output image aspect ratio. Set to 'auto' to let the model infer the aspect ratio from the prompt.
- `imageCount`: Number of images to generate per request. max to 9
### text_to_image / kling-image-o1
High feature consistency with precise detail editing and accurate style transfer.
- `prompt`: Text prompt describing the image to generate.
- `img_resolution`: Output image resolution tier, e.g. 1k / 2k.
- `aspect_ratio`: Output image aspect ratio.
- `imageCount`: Number of images to generate per request.
### text_to_image / kling-image-v3_0
Strengthen consistency, free multi-reference images, comprehensive effect upgrade.
- `prompt`: Text prompt describing the image to generate.
- `img_resolution`: Output image resolution, e.g. 1k / 2k
- `aspect_ratio`: Output image aspect ratio, e.g. 1:1 / 3:4 / 16:9
- `imageCount`: Number of images to generate, max to 9
### text_to_image / kling-image-v2_1
Superb prompt adherence & reliable output.
- `prompt`: Text prompt describing the image to generate.
- `img_resolution`: Output image resolution tier.
- `aspect_ratio`: Output image aspect ratio.
- `imageCount`: Number of images to generate, max 9.
### omni_ref_video / kling-video-o1
mix text, images, one reference video and image Element ids. Without video_1: up to 7 images, images+elements ≤7. With video_1: count provided image_* (any slots), images+elements ≤4. 1 video max. Image Elements ≤7; no video type Elements.
- `prompt`: Text prompt. Reference an input image as 图片X (图片1=image_1, ...), the reference video as 视频1 (video_1). To reference a reusable image subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times). Video subjects are not supported.
- `elements`: Optional reusable image subjects (Elements). JSON array string of {id, bindName, type}, e.g. [{"id":"12345","bindName":"Alice","type":"image"}]. 'id' and 'type' from element_get; type must be image (video subjects are not supported). At most 7 image subjects. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times). Without video_1, images+elements ≤7; with video_1, images+elements ≤4 (counted by how many image_* are provided, any slots). 
- `duration`: Output video duration in seconds (3 to 10). With a base/edit reference video, output duration may follow the input video (enforced downstream).
- `aspect_ratio`: Output video aspect ratio.
- `resolution`: Quality tier (member: up to 1080p).
- `imageCount`: Number of videos to generate per request, max to 4.
- `image_1`: Reference image #1. Counted toward images+elements (≤7 without video_1, ≤4 with video_1). Any image_* slots may be used; the limit is the number provided, not the highest index. Ref as 图片1.
- `image_2`: Reference image #2. Ref as 图片2.
- `image_3`: Reference image #3. Ref as 图片3.
- `image_4`: Reference image #4. Ref as 图片4.
- `image_5`: Reference image #5. Ref as 图片5. Counted toward images+elements (≤7 without video_1, ≤4 with video_1).
- `image_6`: Reference image #6. Ref as 图片6. Counted toward images+elements (≤7 without video_1, ≤4 with video_1).
- `image_7`: Reference image #7. Ref as 图片7. Counted toward images+elements (≤7 without video_1, ≤4 with video_1).
- `video_1`: Reference video #1 (max 1). This is the v2v input — use omni_ref_video, not image_to_video. MP4/MOV, 3–10s, ≤200MB, 720–2160px, 24–60fps (duration/size/aspect enforced downstream). With this video, images+elements ≤4 (count of provided image_* plus elements, any slots). Ref as 视频1.
- `combinedItemCap`: `{"maxItems": 8, "arguments": ["elements"], "inputPrefixes": ["image_", "video_"]}`
- `combinedItemCaps`: `[{"maxItems": 4, "arguments": ["elements"], "inputPrefixes": ["image_"], "whenAnyInputPrefixes": ["video_"]}, {"maxItems": 7, "arguments": ["elements"], "inputPrefixes": ["image_"], "whenNoneInputPrefixes": ["video_"]}]`
- `elementSupport`: `{"imageElements": true, "videoElements": false, "maxImageElements": 7, "maxTotalElements": 7}`
### omni_ref_video / kling-video-v3_0_omni
mix text, images, one reference video and image/video Element ids. Without video_1: up to 7 images, images+elements ≤7, video subjects ≤3. With video_1: count provided image_* (any slots), images+elements ≤4; video subjects allowed only when there are no images or image subjects, at most 1. 1 video max. Image+video Elements ≤7. Audio-video sync and multi-shot supported.
- `prompt`: Text prompt. Reference an input image as 图片X (图片1=image_1, ...), the reference video as 视频1 (video_1). To reference a reusable subject (Element), write <<<id>>> in the prompt and list that id in the 'elements' argument (an id may be referenced multiple times).
- `elements`: Optional reusable subjects (Elements). JSON array string of {id, bindName, type}, e.g. [{"id":"12345","bindName":"Alice","type":"image"}]. 'id' and 'type' from element_get (type is image or video). At most 7 image+video subjects combined; at most 3 may be video. Without video_1, images+elements ≤7. With video_1, images+elements ≤4 (count of provided image_* plus elements, any slots); video subjects are allowed only when there are no images or image subjects, at most 1. Write <<<id>>> in the prompt where each subject should appear (an id may be referenced multiple times).
- `duration`: Output video duration in seconds (3 to 15). With video_1, the official panel typically limits duration to 3–10 (11–15 may be grey-gated downstream). With a base/edit reference video, output duration may follow the input video (enforced downstream).
- `aspect_ratio`: Output video aspect ratio. Use auto when at least one image_* is provided (follow the input), or for a video-edit task whose video_1 is the base video. When video_1 is a reference video, pass a specific ratio: 16:9, 9:16 or 1:1. For text-only, pass 16:9, 9:16 or 1:1.
- `resolution`: Quality tier. 720p=std, 1080p=pro. 4k for members.
- `imageCount`: Number of videos to generate per request. max to 4
- `prefer_multi_shots`: Whether to enable smart multi-shot splitting (intelligent shot composition). Downstream may force false for base-video edit and true for reference-video.
- `enable_audio`: Generate new synced audio (音画同步). Only one of enable_audio and keepOriginalSound may be true. For new audio use enable_audio=true and keepOriginalSound=false. When video_1 is provided, enable_audio must be false.
- `keepOriginalSound`: Keep the original sound of the reference video. Only one of enable_audio and keepOriginalSound may be true. To keep the source sound use keepOriginalSound=true and enable_audio=false.
- `image_1`: Reference image #1. Counted toward images+elements (≤7 without video_1, ≤4 with video_1). Any image_* slots may be used; the limit is the number provided, not the highest index. Video-only v2v is allowed. Ref as 图片1.
- `image_2`: Reference image #2. Ref as 图片2.
- `image_3`: Reference image #3. Ref as 图片3.
- `image_4`: Reference image #4. Ref as 图片4.
- `image_5`: Reference image #5. Ref as 图片5. Counted toward images+elements (≤7 without video_1, ≤4 with video_1).
- `image_6`: Reference image #6. Ref as 图片6. Counted toward images+elements (≤7 without video_1, ≤4 with video_1).
- `image_7`: Reference image #7. Ref as 图片7. Counted toward images+elements (≤7 without video_1, ≤4 with video_1).
- `video_1`: Reference video #1 (max 1). This is the v2v input — use omni_ref_video, not image_to_video. MP4/MOV, 3–10s, ≤200MB, 720–2160px, 24–60fps (duration/size/aspect enforced downstream). With this video, images+elements ≤4 (count of provided image_* plus elements, any slots), and enable_audio must be false. Video subjects are allowed only when there are no images or image subjects, at most 1. Ref as 视频1.
- `combinedItemCap`: `{"maxItems": 8, "arguments": ["elements"], "inputPrefixes": ["image_", "video_"]}`
- `combinedItemCaps`: `[{"maxItems": 4, "arguments": ["elements"], "inputPrefixes": ["image_"], "whenAnyInputPrefixes": ["video_"]}, {"maxItems": 7, "arguments": ["elements"], "inputPrefixes": ["image_"], "whenNoneInputPrefixes": ["video_"]}]`
- `elementSupport`: `{"imageElements": true, "videoElements": true, "maxImageElements": 7, "maxVideoElements": 3, "maxTotalElements": 7, "voiceConsistency": true, "maxVideoElementsWithVideoInput": 1}`
