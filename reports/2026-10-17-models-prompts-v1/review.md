# Independent text review — disposition

**2026-10-17 · independent reviewer `del_mvbx70wm_qkv0` · no provider calls or writes by reviewer.**

The reviewer consulted historian, lighting and dialogue/sound role perspectives. This is not three separate role approvals, media review, historical certification or director acceptance.

## Findings resolved in this revision

1. **Cinema4 preset/user lighting — P2.** Captured `light_id` enum allows only `custom`, while preset/user rules require a non-custom ID. The practical guide, prompt adaptation note and README now explicitly mark preset/user lighting **unresolved and not executable until the producer obtains a reconciled official schema**. Raw schema was preserved unchanged; actual server behaviour was not tested.
2. **Version/checksum evidence — P3.** Added sanitized npm latest dist-tags and versioned release metadata, plus the expected binary checksum from the official npm package's bundled `checksums.json`. The npm tarball's SHA-512 SRI matches the published `dist.integrity`; the actual GitHub Linux archive SHA-256 matches the saved expected value. See `snapshots/higgsfield-release-verification.json` and its linked evidence. No global installation was changed.

## Reviewer checks

- Mocked-write catalog render matched the generated inventory exactly.
- Counts agreed: 6 Kling routes, 15 exact model-ID spellings, 18 server tools; 107 Higgsfield operations, 22 workflows, 124 non-root registered command paths.
- Source/project hashes in `sources.json` matched at review time.
- No CSV dialogue quote mismatch or accidental Galileo baseline expansion found.
- Draft/approval boundaries, reaction causality, historical face restrictions, material uncertainty, lighting continuity and intentional silence were appropriately distinguished from acceptance.

**Scope limits:** no image inspection, playback, listening, language/performance/likeness/voice certification, provider calls or independent fresh external verification by the reviewer. Researcher independently rechecked npm metadata/integrity and corrected the two findings above. No review grants production, spending, upload or artistic approval. Producer owns any subsequent evaluation assignment; research is delivered as a closed documentation stage.
