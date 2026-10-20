# Prompt Studio

Local app that turns **headshots + location images + a script + outfit references** into everything you need to start prompting **Kling** and **Higgsfield**: character sheets, Kling Element specs, scene reference plates, outfit sheets, and per-shot keyframe and video prompts — all with the exact token and file naming each platform expects.

No dependencies. Node 18+ only.

```bash
cd apps/prompt-studio
node server.mjs          # http://127.0.0.1:4317   (PORT=… to change)
npm test                 # 15 tests: engine + server
```

Data (projects, uploads, exports) lives in `apps/prompt-studio/data/` (git-ignored; override with `PROMPT_STUDIO_DATA`). The server listens on `127.0.0.1` only and rejects non-local `Host`/`Origin`.

## Workflow (sidebar)

1. **Project setup** — title, style preset (photoreal-unretouched, editorial, anime, 3D, game concept), aspect, default camera, platform models, and the likeness-rights confirmation (prompts using faces stay locked until ticked).
2. **Characters** — front + side headshot (+ up to 2 extra angles), appearance fields, pronouns (default *they/them*, never inferred), outfits with reference images, optional Kling Element id.
3. **Locations** — reference images (up to 6), description, time, mood, palette.
4. **Script** — `INT./EXT. PLACE - TIME`, `NAME (paren): line`, Fountain speaker lines, action paragraphs. Scenes, cast and shots are detected; pick location/outfit per scene.
5. **Character sheets** — split-screen, turnaround, expression, face-angles, single-portrait; Higgsfield + Kling CLI + Kling app prompts, token table, `element_create` spec.
6. **Scene references** — five plates per location (wide / medium / reverse / detail / vertical) and a costume sheet per outfit.
7. **Shot prompts** — keyframe + video per shot for Kling (CLI and app syntax) and Higgsfield; duration/camera overrides; live prompt linter.
8. **Naming guide** — tokens, tags, file names.
9. **Connect & export** — read-only Kling CLI checks (`who_am_i`, `account`, `tool_list`, `element_list`), Higgsfield notes, export to disk (Markdown, JSON, Kling request drafts, Higgsfield request drafts, renamed uploads).

## Platform naming the generator applies

| | Kling CLI / MCP | Kling app | Higgsfield |
|---|---|---|---|
| Input image N | `图片N` (= `image_N`, order of `--image`) | `@ImageN` | media roles `image_references` / `start_image` / `end_image` |
| Saved character | `<<<ID>>>` **and** `--elements '[{"id","bindName"}]'` | `@ElementName` | reference element `char_<slug>_vN` |
| Element tags | `Characters Animals Items Costumes Scenes Effects Others`; image = 1 cover + 1–3 secondary | | |
| Exclusions | in prompt body (no `negative_prompt` on v3/o1) | same | negative tail |

Sources: `docs/kling-manual/05-elements.md`, `18-guia-de-prompts.md`, `.agents/skills/kling-cli`, the Higgsfield `character-sheet` workflow and live `models_explore` model ids/roles (checked 2026-10-20). Model lists change — confirm with `kling who_am_i` / Higgsfield `models_explore` before pasting.

## Spend and safety

The app **never submits a generation, upload or delete**. The server's Kling endpoint is a whitelist of read-only commands. Exported Kling drafts carry `submissionBlocked` and a placeholder `auth`, matching this workspace's producer-only spend gate (`AGENTS.md`). Paste a prompt, or hand `requests-draft.json` to the Higgsfield connector, after you have checked your balance.

## Layout

```
server.mjs            local HTTP server (stdlib), storage, uploads, export, CLI checks
public/engine.js      pure prompt engine (browser + Node): parser, naming, sheets, plates, shots, linter
public/app.js|css     UI
test/                 node:test suites
docs/mistakes.md      Mistake/Solution record
```

## Next step (hook)

Run a real project end to end: create the Kling Element for your main character, paste its id on the character card, regenerate shot prompts, and check them with `kling who_am_i` before the first paid job. Record anything the platforms reject in `docs/mistakes.md`.
