# Suggested Commands

All from repo root `/mnt/data/Projects_SSD/Movies_Projects` unless noted.

```bash
.venv/bin/python scripts/manage.py status     # read-only workspace+board state
.venv/bin/python scripts/manage.py validate   # workspace integrity, exit 2 on error
.venv/bin/python scripts/manage.py lint       # hard contradictions + advisories
.venv/bin/python scripts/manage.py resume     # session-start digest
.venv/bin/python scripts/manage.py handoff check <file>            # handoff schema+hashes
.venv/bin/python scripts/manage.py handoff ingest <file> --by ROLE # producer only, sole writer command
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m unittest tests.test_workflow.WorkflowTests.test_paths_cannot_escape_workspace  # single test

.venv/bin/python scripts/workflow.py index  --output reports/workflow-v1/file-index.json  # SHA-256 inventory
.venv/bin/python scripts/workflow.py verify --index  reports/workflow-v1/file-index.json
.venv/bin/python scripts/workflow.py new-draft --id <slug> --title "<title>" [--test-only]
.venv/bin/python scripts/workflow.py check-clean-draft --path drafts/<slug>
.venv/bin/python scripts/production_plan.py check --verify-media   # canonical plan check

python3 scripts/review_sweep.py --film andre-time-travel           # free local image review log
python3 scripts/review_sweep.py --record <path> --verdict keep|keep-tone-only|reject|variant-needed
serena memories check                                              # validate mem: references
```

Atlas rebuild (needs Pillow/ReportLab/pdftoppm/DejaVu; output must be a new revision folder):
```bash
python3 scripts/build_preproduction_atlas.py --source 05_storyboard/source/atlas.json --output 05_storyboard/preproduction-atlas-v3 --revision v3
python3 scripts/verify_handoff.py --output reports/<name>.json
```

Site (`sites/movies-demandas/`): `npm run dev|build|lint|test|check:data`, `npm run review:start|status|stop`.

Producer-only paid (never run without producer role + written scope + fresh balance): `scripts/kling_batch.py --submit-only|--resume JOB`, `scripts/gemini_generate.py`.
