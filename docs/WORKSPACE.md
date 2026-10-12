# Workspace Map

The desktop project is **Movies_Projects**, anchored to this folder. `workspace.json` selects `projects/andre-time-travel/`; its production plan and local memory are canonical.

## Film stages

- `00_brief/`: scope, approvals, research ledger and cached source snapshots.
- `01_script/`: English draft, stable dialogue IDs, language strategy and translations.
- `02_references/`: raw/selected/approved/synthetic Andre references, historical eye references, wardrobe, table and quarantined legacy resources.
- `03_bibles/`: character, table, camera/lighting continuity and five scene bibles.
- `04_audio/`: English/historical speech, voice tests and dialogue/ambience/Foley/music stems.
- `05_storyboard/`: editable `source/atlas.json`, keyframes, contact sheets, shot list and animatics. Derived atlases `preproduction-atlas-v1/` through `v3/` are review documents with `approved: false`. The next render uses a new folder name.
- `06_pilot/`: original test clips, speech variants and reviews.
- `07_generations/`: approved requests, actual provider responses, originals, accepted and rejected takes.
- `08_edit/`: normalized media, timelines, subtitles, `reviews/`, and `picture-lock/`. The Galileo file in `picture-lock/` is a candidate preview, not an accepted lock.
- `09_delivery/`: masters, captions, stems and final QC.
- Film `tasks/`, `agents/`, `memory/`, `logs/`: canonical board, role bindings, resume state and operational records.

Workspace `agents/` and `skills/` hold role definitions and canonical workflow links. `inbox/` holds unapproved incoming material; files there are never automatically uploaded or approved. `scripts/manage.py` provides offline status/validation. No production media or rendering schedule is fabricated.
