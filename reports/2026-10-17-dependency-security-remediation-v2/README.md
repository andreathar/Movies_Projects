Remaining-high dependency remediation — verified 2026-10-17

Eight of the sixteen previously remaining high package entries are remediated and tested. The eight still high all derive from one unpatched Braces issue. Audit is now 15 affected package names: 0 critical, 8 high, 6 moderate, 1 low (previously 27/16 high). These counts include inherited/meta findings, not independent exploit counts. No total-security claim.

Installed changes: React/React-DOM/direct RSC 19.2.8; plugin-rsc 0.5.30 with vendored RSC 19.2.8; Cloudflare Vite plugin 1.43.1, Wrangler 4.107.1, workers-types 4.20260702.1 and Miniflare 4.20260702.0; ws 8.21.0; undici 7.29.1; image-size 2.0.4; brace-expansion 1.1.21/5.0.12; js-yaml 4.3.2; browserslist 4.29.3; source-map-js 1.2.2. Next 16.4.1, Vite 8.1.6, Sharp 0.35.5 and Vinext 1.0.0-beta.5 stay as previously validated.

The only new overrides are parent-scoped miniflare→undici 7.29.1 and vinext→image-size 2.0.4. Existing miniflare→Sharp override remains. No blanket override, vendor edit, unsupported framework migration, credential/security setting change or peer conflict. Official-registry archives/metadata and exact lock delta are retained externally. A first staged candidate exposed residual Undici/image-size findings; its evidence is preserved in candidate1/, and only the fully checked final candidate was promoted.

| Previous high package | Outcome | Evidence / concrete blocker |
|---|---|---|
| @next/eslint-plugin-next | Blocked upstream | Braces3.0.3/GHSA-vfj7-8cjw-p6xm remains unpatched; inherited through the existing Braces/micromatch/fast-glob lint or Vinext commonjs transform chain. |
| brace-expansion | Fixed | Both affected nodes patched within parent ranges:1.1.14→1.1.21 and5.0.6→5.0.12. |
| braces | Blocked upstream | Braces3.0.3/GHSA-vfj7-8cjw-p6xm remains unpatched; this is the vulnerable parser. |
| browserslist | Fixed | 4.28.2→4.29.3 within declared range; target metadata dependency closure updated. |
| eslint-config-next | Blocked upstream | Braces3.0.3/GHSA-vfj7-8cjw-p6xm remains unpatched; inherited through the existing Braces/micromatch/fast-glob lint or Vinext commonjs transform chain. |
| fast-glob | Blocked upstream | Braces3.0.3/GHSA-vfj7-8cjw-p6xm remains unpatched; inherited through the existing Braces/micromatch/fast-glob lint or Vinext commonjs transform chain. |
| image-size | Fixed | 2.0.2→2.0.4 via parent-scoped vinext override. Keeps beta5 framework instead of upgrading/migrating it. Same imageSize consumer API; all 7 canonical references parsed and full build passed. |
| js-yaml | Fixed | 4.1.1→4.3.2 within ESLint parent range; fixes the recorded merge/omap CPU advisories. |
| micromatch | Blocked upstream | Braces3.0.3/GHSA-vfj7-8cjw-p6xm remains unpatched; inherited through the existing Braces/micromatch/fast-glob lint or Vinext commonjs transform chain. |
| react-server-dom-webpack | Fixed | React/React-DOM/direct RSC 19.2.6→19.2.8; plugin-rsc 0.5.26→0.5.30 also replaces vendored RSC 19.2.6 with19.2.8. Fits existing Vinext peers; no vendor edits. |
| source-map-js | Fixed | 1.2.1→1.2.2 within existing parent ranges. |
| undici | Fixed | 7.24.8→7.29.1 via parent-scoped miniflare override. Stable Miniflare 4 otherwise pins7.28.0, which still has later advisories. Same Node engine/API major; focused integration and full compatibility checks pass. |
| vinext | Blocked upstream | Braces3.0.3/GHSA-vfj7-8cjw-p6xm remains unpatched; inherited through the existing Braces/micromatch/fast-glob lint or Vinext commonjs transform chain. |
| vite-plugin-commonjs | Blocked upstream | Braces3.0.3/GHSA-vfj7-8cjw-p6xm remains unpatched; inherited through the existing Braces/micromatch/fast-glob lint or Vinext commonjs transform chain. |
| vite-plugin-dynamic-import | Blocked upstream | Braces3.0.3/GHSA-vfj7-8cjw-p6xm remains unpatched; inherited through the existing Braces/micromatch/fast-glob lint or Vinext commonjs transform chain. |
| ws | Fixed | 8.18.0→8.21.0 through Cloudflare plugin 1.43.1/Wrangler 4.107.1/Miniflare 4.20260702.0, with matching workers-types 4.20260702.1; no runtime major migration. |

Braces blocking paths: eslint-config-next→@next/eslint-plugin-next→fast-glob→micromatch→braces; and vinext→vite-plugin-commonjs→vite-plugin-dynamic-import→fast-glob→micromatch→braces. Published Braces latest is 3.0.3 and every published version is inside the recorded affected range<=3.0.3. Current fast-glob/micromatch releases retain it. Vinext 1.2.1 still depends on the same commonjs plugin and requires React 19.3.1, so framework migration does not remove this root issue.

Recommended next decision: retain the supported tested toolchain pending an official parser/consumer fix; optionally scope a maintained parser or build/lint replacement separately. Local vendor patching, downgrades or broad tool removal were not performed. Owner:producer/upstream maintainers. Unblock:an official fixed compatible parser/consumer release or a separately authorized replacement. [Affected upstream parser](https://github.com/micromatch/braces/blob/3.0.3/lib/compile.js),[advisory](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm).

RSC GHSA-wx67-qw84-cm4g is addressed in both direct and bundled copies; metadata peers fit existing Vinext and actual npm peer checks pass. [Official React advisory](https://github.com/react/react/security/advisories/GHSA-wx67-qw84-cm4g). Undici7.29.1 includes the later BalancedPool TLS and WebSocket fixes; [official release](https://github.com/nodejs/undici/releases/tag/v7.29.1). The image-size parser fixes address GHSA-5p2g-fcmc-qvqq and GHSA-w3rx-r6r6-pgpr; ws 8.21.0 addresses GHSA-58qx-3vcg-4xpx and GHSA-96hv-2xvq-fx4p. Raw advisory IDs/ranges remain in the before/after audit JSON.

Validation:87 tests, lint, TypeScript, production build and peer tree pass for final candidate. Focused tests pass for Undici HTTP fetch, Undici WebSocket↔ws echo, Miniflare worker+ephemeral D1, and dimensions for all 7 preserved canonical references. No crafted exploit traffic. Canonical build and final validate/lint/resume/catalog, both export checks and check:data pass.

Only package.json/package-lock.json were edited in existing sources; new delivery reports/handoff are additive. Guarded promotion refreshed only the owned loopback frontend once in 7.278 seconds:PID4169251→20952. Readiness/Vite return 200; favicon and both data snapshots exactly match disk. Persisted D1 is unchanged:revision 9/one row/same row hash. Every baseline path remains; media, approvals, production data, prior snapshots/backups, PR12, HEAD and concurrent work are preserved. No commit, push, generation, upload, spend or unrelated restart.

Current serving mode is the documented development launcher; production dist was built successfully. Browser visual QA remains unverified from the previously observed zero-width Chrome surface; no post-refresh console/screenshot claim. User action if visual QA is desired:put the Movies tab at http://127.0.0.1:5173/ in a visible non-minimized Chrome window, select it, and restore extension control; then request visual QA without another restart.

Recovery: exact current-before manifests/runtime and a consistent private SQLite backup are outside the repo in /home/athar/Documents/Codex/2026-10-17/task/remaining-high-remediation-20261017. Old dependencies/build outputs are at /mnt/data/Projects_SSD/.movies-remaining-high-remediation-20261017/rollback/. Earlier first-pass backups remain intact. See external ROLLBACK.md; no rollback executed. Producer review/ingestion pending; no film approval or production-stage transition.
