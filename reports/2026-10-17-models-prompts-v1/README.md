# Kling 4.0 + Higgsfield — models, tools and scene prompts

**Checked 2026-10-17 · research only · episode `andre-time-travel`.**

## Deliverables

1. **[Complete CLI inventory](catalog.md)** — every discovered model ID, workflow and registered command, with exact names and snapshot links.
2. **[Kling 4.0 / Higgsfield practical guide](kling4-and-higgsfield.md)** — official documentation, current limits, important UI/API/CLI differences and proposed project applications.
3. **[16 structured scene prompts](prompts.md)** — Galileo first, then Caesar/Khan/Napoleon/Oppenheimer coverage, opening, table transitions, ending, Foley and ambience. Includes reference-binding template, exact fictional dialogue, framing/sound/timing direction, safety constraints and checks. These are drafts, not executable jobs or canonical shot revisions.

| Surface | Latest public CLI verified | Dated discovery |
|---|---|---|
| Kling | `@klingai/cli-global` **0.2.3**, same as installed | **15 exact model-ID spellings**, 6 generation routes, **18 server tools**, 20 top-level client commands |
| Higgsfield | `@higgsfield/cli` **1.2.2**; installed remains **1.1.24** | **107 model/operation entries**, **22 workflows**, 16 functional top-level command groups/commands; complete 124-path non-root help tree |

The Higgsfield breakdown is 42 video, 38 image, 15 3D, 8 audio, 3 data and 1 text operations. These include upscaling/editing/analysis wrappers; they are not 107 independent foundation models. The Kling count deliberately preserves `gpt-image2` versus `gpt-image-2` as different route-specific ID spellings, not a claim of two separate OpenAI model families.

## Key conclusions

- **Kling 4.0 is not the same interface as Higgsfield Cinema Studio 4.0.** The former appears as `kling-video-v4_0` in Kling. Higgsfield lists Cinema4 as workflow `cinematic_studio_video_4_0`; its direct model list does not list Kling 4.0.
- Kling V4 currently declares **3–30 s**, **720p/1080p**, up to **10 total keyframe images**, or **15 combined Omni references**. The official UI articles' 4K/HDR/Flash/extension wording must not be treated as supported CLI arguments. Omni V4's smart multishot cannot simply be turned off—important for historical-eye crop safety.
- Higgsfield Cinema4 exposes different reference, sound and mode rules, including a 50-item reference cap/30-image cap and a video-extension mode. Neither schema presence nor a matching version number proves the same engine, price, output quality or account access.
- Static Higgsfield docs lag behind live discovery. CLI, public API and web UI inventories must stay separate.
- **Project priority remains G-L03/G-L04 and proposed first speaking test G-P04**, after reference/timing gates. No source plan or approved route was changed; the prompt library is not a new production batch.

## Official sources

- [Kling 4.0 launch](https://kling.ai/blog/kling40-kling-visual-realism-creative-control-introducing-storytelling?tab=all)
- [Kling 4.0 complete guide](https://kling.ai/blog/kling-4-ai-video-model)
- [Higgsfield CLI documentation](https://github.com/higgsfield-ai/cli) and [1.2.2 release](https://github.com/higgsfield-ai/cli/releases/tag/v1.2.2)
- [Higgsfield API discovery policy](https://docs.higgsfield.ai/docs/llms.txt) — useful comparison, not a substitute CLI catalog.

[Source URLs/hashes](sources.json), sanitized CLI discovery and schemas live beside this report in `snapshots/`. Rebuild the inventory **offline** with `python3 -B reports/2026-10-17-models-prompts-v1/build_catalog.py`; this renders only `catalog.md` from saved snapshots and does not refresh providers.

## Scope, verification and successor

Role: independent research/helper session, not a Parley lane or desktop producer. Public documentation, npm metadata, local public help and read-only official CLI discovery were consulted. No source-code implementation visibility is claimed for the private/unavailable Higgsfield Go source repository. The latest official Higgsfield binary was checksum-verified and inspected from `/tmp`; **no global upgrade, lifecycle script, login/account switch, credential extraction, upload, generation, training, pricing/cost query, mutation, service start, commit or publication** was performed. Catalog access used existing CLI-managed sessions; private identity fields were excluded from shared Kling snapshots. No account resource inventories or secrets are included.

Version/model/tool/schema evidence and documentary checks are summarized in [verification.json](verification.json). Text-only role-perspective review does not certify media, history beyond supplied reviewed sources, language, voice, listening, likeness, playback or artistic acceptance. Snapshot models are declared/visible, not generated or entitlement-tested.

**Research stage closed on delivery; no production is started.** Producer owns any later evaluation assignment, reference acceptance, route/cost/schema check and provider-specific spending/upload release; historian, lighting and dialogue/sound owners review the proposed encounter cards. Andre retains likeness/voice/artistic acceptance. A file existing does not mean anyone has accepted the successor task. See [handoff.json](handoff.json) for scope, file hashes, actual checks and open decisions.
