I’ll audit the current `andre-time-travel` workspace as an independent reviewer, tracing references before labeling files unused. I’ll keep to reads and static checks; integration and any cleanup remain with the parent.
## Conclusion

**No script or test is proven safe to delete.** One historical request spec is a strong archival candidate. The clearest cleanup opportunities are configuration hygiene, misleading naming, and test-gate coverage.

### Findings

| Confidence | Evidence | Narrowly scoped recommendation |
|---|---|---|
| **High** | `scripts/andre_cinematic_spec.json:1–20` contains a dark-wardrobe request; its job is recorded in `projects/andre-time-travel/credit-ledger.csv:65`. Dark wardrobe was logically retired, preserving originals: `projects/andre-time-travel/agents/handoffs/2026-10-09-dark-wardrobe-archive.json:5–7`. No executable caller found. | Classify as historical request/provenance, not reusable configuration. Propose archival relocation only after checking recorded hashes/path references. **Do not delete.** |
| **High** | `.claude/hooks/session-start.sh:25–59` creates placeholder skills at external profile paths. `scripts/manage.py:157–165` checks existence and hash mismatch, not usability. | Replace external placeholder creation with an explicit “unavailable external skill” diagnostic or isolated test fixtures. This hook is active configuration, not dead code. |
| **High** | All **13 inspected symlinks resolve**. Three skill hashes differ from `skills/registry.json:55–79`: continuity, dialogue localization, editing QC. Kling and grounded-citations hashes match. | Review those three source changes; do not automatically rehash or remove external targets. No broken filesystem binding found; session discovery remains unverified. |
| **High** | `docs/CLEANUP-INVENTORY-2026-10-09.md:17–21` still describes unreconciled Kling provenance. Current `skills/registry.json:6–10` records the vendored source and its matching hash. | Preserve the inventory as dated history; add a current-status pointer rather than repeating the old consolidation. |
| **High** | `scripts/parley_verify.py:12–15` discovers only `tests/`; `.vscode/settings.json:5` does likewise. Offline preflight tests also exist at `docs/kling-manual/tools/test_kling_tools.py:1–18`. | Explicitly include that separate suite in verification, or integrate it without losing fixtures. It is **not unused** merely because standard discovery misses it. |
| **High** | `git ls-files` lists two `.serena/logs/health-checks/*.log` files. `.serena/.gitignore:1–2` excludes cache/local configuration, not logs. | Decide whether these are retained evidence or incidental runtime output. Add a narrowly scoped ignore rule for future runtime logs; preserve existing evidence pending owner review. Log contents were not inspected. |
| **High** | `scripts/verify_handoff.py:28` defines `verify(root: Path, atlas_relative: str) -> dict`; it verifies atlas/rehearsal artifacts. Actual management handoff commands are documented at `scripts/manage.py:2–7`. | Clarify its atlas-specific purpose in the command index; consider a compatibility-preserving rename later. Do not merge/delete these distinct tools. |

### Active entrypoints—retain

- **Management/provenance:** `scripts/manage.py`, `scripts/workflow.py`, production-plan and catalog tooling—required by `AGENTS.md:20–21,35–38`.
- **Paid tooling:** `scripts/kling_batch.py` loads release/telemetry modules at `scripts/kling_batch.py:35–50`; Gemini remains explicitly producer-only at `CLAUDE.md:45`.
- **Rendering/import reconstruction:** atlas imports at `scripts/build_preproduction_atlas.py:17–24`; Instagram rebuild instructions at `inbox/instagram-andreathar/2026-10-09-chrome/README.md:24`.
- **Observability:** `scripts/respan_smoke.py:17,55–59` imports Gemini’s environment loader and performs a provider call. **Not an offline smoke test; not executed.**
- All **16 test files** match configured discovery. No redundant suite established.

### Checks actually performed

- Read contract, cleanup inventory, current state/configuration, callers/imports, documentation and test sources.
- Parsed **45 Python files** successfully without executing imports.
- Shell syntax checks passed for both shell scripts and session-start hook.
- `manage.py status` with bytecode disabled: **OK**, three skill-hash warnings.
- No files changed; no services, provider commands, installs or tests executed. `resume`/`lint` skipped because they read session-log/mistake records (`scripts/manage.py:640–641,675–677`).

**Parent-owned next step:** review the external-placeholder hook and approve a small cleanup proposal separating historical request specs, runtime artifacts and active entrypoints. No deletion authorization is implied.