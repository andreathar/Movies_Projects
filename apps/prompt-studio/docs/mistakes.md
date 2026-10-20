# Mistake / Solution record — Prompt Studio

| # | Date | Mistake | Cause | Solution | Rule |
|---|---|---|---|---|---|
| 1 | 2026-10-20 | `server.mjs` crashed: `Cannot set properties of undefined (setting 'PromptEngine')` | `package.json` had `"type": "module"`, so Node loaded the browser/Node UMD `engine.js` as ESM (no `module`, no `this`). | Removed `"type"`; server and tests use `.mjs` and load the engine via `createRequire`. | A UMD file shared with the browser must not live under a `"type": "module"` package. |
| 2 | 2026-10-20 | Dialogue prompts ended with `…table?".` (double punctuation) | Template appended `.` after the quoted line. | Add the period only when the line has no terminal punctuation. | Never alter punctuation of an exact script line; only append after it. |
| 3 | 2026-10-20 | Host-header test passed with a 200 | `fetch` silently ignores a custom `Host`. | Use `http.request` for header-spoofing tests. | Test security headers with a client that lets you set them. |
| 4 | 2026-10-20 | Asset-name test expected `char-mia-front` | `assetName` joins parts with `_`; subject/variant are separate parts. | Fixed expectation to `char-mia_front`. | Names are `<project>_<kind>_<subject>_<variant>_vNN.<ext>`; test against the helper's contract. |
