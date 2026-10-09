# Operations

1. Read project state and run `.venv/bin/python scripts/manage.py status`.
2. Put user media in the correctly named inbox; preserve it unchanged.
3. Use the active film board/specification, roles and skill links to perform only the next approved work.
4. Register source, checksum, approval and version for every real asset; never seed fake media paths.
5. Keep paid jobs producer-owned, with actual ID/charge persistence and separate retry decisions.
6. Store reviews and update the canonical board, approvals and manifest only after verification.
7. Record verified session progress locally.
8. Run `.venv/bin/python scripts/manage.py validate` and `.venv/bin/python -m unittest discover -s tests -v` after metadata/tool changes.

Status and validation are read-only, offline operations. Reference-generation charges and voice-test evidence now exist; consult the current film ledger, manifest and local response files. No accepted production takes are implied by those charges. Never treat a historical balance as live.

Read `START_HERE.md`, `docs/REPEATABLE_WORKFLOW.md` and `docs/LOCAL_AGENT_HANDOFF.md` before local editing. Reference atlas V1 remains the original delivery. Editable directions live in `05_storyboard/source/atlas.json`; rebuild into a new revision. `scripts/workflow.py` inventories files and creates clean, unregistered continuation drafts without network calls or inherited approvals.
