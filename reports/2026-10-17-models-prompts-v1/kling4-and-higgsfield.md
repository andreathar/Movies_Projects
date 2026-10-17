# Kling 4.0 and Higgsfield: what is documented versus exposed

Research date: **2026-10-17**. This is a proposal/reference document, not production acceptance, a pricing quote or permission to submit. Sources are linked below and captured in [sources.json](sources.json).

## 1. The most important distinction

**Kling 4.0** is the model family advertised by Kling. **Higgsfield** is a creative platform exposing multiple vendors, its own products and workflow wrappers. **Cinema Studio 4.0** is a Higgsfield workflow with its own schema; its name does not establish that it is the Kling 4.0 model or that their controls are interchangeable.

The current Kling CLI explicitly advertises `kling-video-v4_0`. Higgsfield's live `model list` does **not** list a Kling 4.0 model ID; it lists Kling 2.6, 3.0, 3.0 Turbo and three 3.0 Omni-related operations. Its **workflow** catalog separately exposes `cinematic_studio_video_4_0` (Cinema Studio 4.0). Do not silently route a Kling 4.0 request through a differently named Higgsfield operation.

## 2. Official Kling 4.0 documentation

Official launch article, Sep 30, 2026:
https://kling.ai/blog/kling40-kling-visual-realism-creative-control-introducing-storytelling?tab=all

Official complete guide, Sep 30, 2026:
https://kling.ai/blog/kling-4-ai-video-model

These describe stronger motion/camera continuity, realism, lip sync and stereo sound; native 3–30-second generation; up to 10 flexible keyframes; multimodal references; longer prompts; targeted editing; 21:9 output; expanded language support. They advertise up to 15 combined references, including images, videos and subjects. References should each have a job: identity, costume/product, scene layout, lighting/style, motion, camera, timing or voice.

**Rollout language matters:** the pages describe gradual availability. 10-bit HDR is explicitly **coming soon**; the launch page also describes repeated video extension up to two minutes as **coming soon**. Flash access is mentioned for certain subscribers, but that is not a distinct Flash model ID in our current CLI discovery. The guide advertises 4K output; this account's CLI explicitly says **4K is not enabled**. Marketing/UI coverage is not a CLI contract.

The guide's prompt structure is useful: **Subject + Action + Setting + Camera + Lighting + Pacing + Sound**. Its recommendation to review the whole sequence, rather than a beautiful first frame, is especially important for this project's facial-safety gate.

## 3. Kling 4.0 — exact live CLI differences

Source: [sanitized discovery](snapshots/kling-capabilities.json), official installed CLI 0.2.3, server `mcpVersion` 1.3.3. Listed/declared is not generated/tested/artistically approved.

| Control | `text_to_video` | `image_to_video` | `omni_ref_video` |
|---|---|---|---|
| Model | `kling-video-v4_0` | `kling-video-v4_0` | `kling-video-v4_0` |
| Duration | 3–30 s, default 10 | 3–30 s, default 10 | 3–30 s, default 10 |
| Output resolution | 720p / 1080p | 720p / 1080p | 720p / 1080p |
| Number of outputs | `imageCount` 1–4 | `imageCount` 1–4 | `imageCount` 1–4 |
| Aspect ratios | 16:9, 9:16, 1:1, 21:9 | Same; normally follow first frame and omit override | auto, 21:9, 16:9, 9:16, 1:1 |
| Reference control | No media slots | `first_image`, `tail_image`, `keyframe_1`…`keyframe_10` | `image_1`…`image_10`, `video_1`…`video_5`, `audio_1`…`audio_3`, `elements` |
| Combined limit | N/A | **10 total images**, not 10 middle frames plus endpoints | **15 total** across image/video/audio/Element items |
| New/retained audio switches | Not declared in this route | Not declared in this route | `enable_audio`, `keepOriginalSound`; never both true |
| Smart multishot | No declared switch | No declared switch | `prefer_multi_shots` **must remain true** |

Additional limits on the Omni route:

- Up to **7 Elements**, of which at most **3 video-based**. These consume the combined cap; do not count them as free extra references.
- Each image ≤30 MB. Declared video slots: 3–30 s each, ≤300 MB; all referenced videos **plus video subjects** share a combined 3–30 s duration constraint. Audio slots: 5–30 s, ≤50 MB each. Aspect and downstream validation also apply.
- **Input video duration is included in billable duration**, in addition to output; do not present output seconds alone as a price estimate. No cost quote or account balance was requested here.
- Image references are addressed as `图片1`, `图片2`; video as `视频1`; audio as `音频1`. Elements require the actual returned ID in `<<<id>>>` plus a matching entry in `elements`. These are Kling binding conventions, not portable Higgsfield syntax. Never paste an invented ID.
- The schema exposes ordered keyframe slots, **not timestamp parameters**. A prompt may describe timing intent, but exact timestamp anchoring is not established by these fields.
- The T2V aspect-ratio description mentions auto, while its enum/default advertise 16:9 and exclude auto. Use the explicit supported enum, not the contradictory prose.

**Project consequence:** Omni V4's mandatory smart multishot is a risk for a tightly cropped historical-eye shot. “Single continuous shot” in a prompt does not disable a server-required mode or guarantee safe framing. Prefer a reviewed safe first-frame route as a *proposal*, then inspect every frame; do not replace a currently approved model/route automatically. No prompt or model upgrade grants facial-safety approval.

## 4. Higgsfield — current CLI versus platform API

Official distribution/docs: https://github.com/higgsfield-ai/cli

Latest release verified: https://github.com/higgsfield-ai/cli/releases/tag/v1.2.2

Static model documentation: https://github.com/higgsfield-ai/cli/blob/main/MODELS.md

Developer API discovery: https://docs.higgsfield.ai/docs/llms.txt and https://docs.higgsfield.ai/docs/models.md

The CLI has a Go executable distributed by an npm launcher. The implementation repository linked in its README returned 404 publicly; public distribution and documentation were accessible. We inspected **registered help**, not speculative hidden binary symbols. Installed 1.1.24 was left unchanged. A checksum-verified 1.2.2 binary was extracted in `/tmp`, with no installation/lifecycle scripts, and used only for help and read-only catalogs/schema discovery through the existing session. An isolated no-session catalog attempt required authentication; we did not log in or change accounts.

The **1.2.2** live surface returned **107 model/operation entries + 22 workflows**. Static MODELS.md is older/incomplete and even has a mismatched image heading count. Developer API endpoint counts and `vendor/model/operation` identifiers use a different surface. Do not concatenate those counts or infer one catalog's limits from another. The [exhaustive inventory](catalog.md) is the dated CLI listing.

### Cinema Studio 4.0: verified workflow schema

Exact workflow ID: `cinematic_studio_video_4_0`; inspect with `workflow get`, not by assuming it is a direct model. [Captured schema](snapshots/higgsfield-cinema4.json).

| Control | Declared values / rules |
|---|---|
| `mode` | `t2v`, `omni_reference`, `video_edit`, `video_extension`; default `t2v` |
| `prompt` | Required |
| `duration` | Integer, default 5; no minimum/maximum was supplied in this snapshot—**do not infer 30 s** |
| `resolution` | 480p / 720p / 1080p; default 720p; no 4K enum |
| `aspect_ratio` | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16; default 16:9 |
| `generate_audio` | Boolean, default true; not Kling's `enable_audio` name |
| `bitrate_mode` | standard / high; not proof of HDR |
| Reference inputs | `image_references`, `video_references`, `audio_references`, `start_image`, `end_image` |
| Total reference rule | ≤50 media items; ≤30 images counting start/end images; these are Cinema4 rules, **not Kling Omni's 15-item rule** |
| `t2v` | No reference media allowed |
| `omni_reference` | Requires at least one reference item; start/end images only allowed in this mode |
| `video_edit` | Exactly one video reference |
| `video_extension` | At least one video; `extension_mode` required, forward/backward; forbidden in other modes |
| Creative metadata | camera model/lens/aperture IDs, era, genre, pacing, light controls, color palette |

Light constraints require valid custom arrays or real preset IDs and disallow contradictory custom/preset combinations. Do not invent IDs from brand/lens names or translate a prompt adjective into an undocumented flag. No published reference-duration/byte limits or exact camera preset roster are established by this one workflow schema. Catalog presence does not establish access or billable outcome.

### Other useful, inspected Higgsfield controls

- `kling3_0`: start/end-frame objects, prompt, duration/mode, sound as `on|off`. [Schema](snapshots/higgsfield-kling3_0.json).
- `kling_o3_image_reference`: its own image/Element/multishot schema, **not V4 Omni**. [Schema](snapshots/higgsfield-kling_o3_image_reference.json).
- `nano_banana_pro`: ordered image references and model-specific resolution/aspect controls. [Schema](snapshots/higgsfield-nano_banana_pro.json). Live ID is not automatically the older docs' `nano_banana_2`.
- `text2image_soul_v2`: Soul/identity references have dedicated controls. A typed likeness description alone is not proof of Andre continuity. [Schema](snapshots/higgsfield-text2image_soul_v2.json).
- There is **no universal negative-prompt flag** established across these clients. Put project restrictions in the actual prompt and QC contract; use a separate negative field only when the exact model schema supports it.
- `generate create` and `generate workflow` accept local media paths and **auto-upload** them. A local path is not an offline operation. All commands in this research were discovery/help; no generation/cost workflow, upload, Soul training or marketing/website/project mutation was run.

## 5. Proposed routing for our scenes — not an automatic migration

| Need | Candidate direction | Important limit / gate |
|---|---|---|
| Approved Andre likeness keyframe | Existing approved image workflow; optionally evaluate a reference-image model listed in catalog | Producer creates detail images; upload scope and identity review first |
| Historical eyes or below-neck reaction | Reviewed frame + conservative image-to-video | Crop must remain safe every frame; mandatory multishot route is a risk |
| Andre delivers a fictional line | Reference-driven video with scratch voice/performance direction | Exact text, measured delivery length, visible sync; final voice separate |
| Room/wardrobe/table continuity | Explicit role for each approved reference | More references is not automatically better; preserve material provenance |
| Motion performance | Motion-control route, only with an authorized reference | Original audio, direction and duration constraints differ by route |
| Multi-scene transition | Make separate safe shots; edit through table texture | No face morph, no inherited approval; no need to force a 30-second generation |
| Fine edit or extension | Higgsfield Cinema4 schema is a research candidate | New provider spending/upload scope required; do not bypass Kling-only project policy |
| Foley or scratch audio | Text-to-audio/TTS catalog may support a separately scoped proposal | Fees, voice/likeness consent, language review and final mix all separate |

No current production-plan model, prompt, approved reference, wardrobe, shot or audio route was changed. Native full-film timing, shot approval and actual language validation remain unresolved by research. The [prompt library](prompts.md) is draft creative material only.
