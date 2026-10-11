# Movies_Projects — Folder Structure

The tree below is the 2026-10-09 scaffold snapshot, excluding the virtual environment, Git/cache internals and symlink targets. It is not the full live tree.

`workspace.json` `requiredDirectories` is what `manage.py validate` guards. A producer patch on this branch proposes adding `00_brief/decisions/`, `03_bibles/detail-planning/`, `05_storyboard/source/` and `08_edit/reviews/` to that list. Those directories already exist. Derived atlas folders `preproduction-atlas-v1/` through `preproduction-atlas-v3/` also exist, with `approved: false`, and stay out of the required list because the next render is a new folder. `.agents/` holds the in-repo `kling-cli` checkout that `skills/kling-cli` links to. `drafts/` and `series/` are the continuation scaffold.

Names that share a word and are not the same set:

- Chapter key `galileo`. Plans and handoffs named `piloto-galileu*` are that chapter. Do not rename cited files.
- Era stills: `02_references/keyframes/andre/`. Empty per-chapter folders under `05_storyboard/keyframes/<chapter>/` are not those stills. Study sets are `detail-studies-v1/` and `chatgpt-in-out-v1/`.
- `08_edit/picture-lock/galileo-en-preview-v1.mp4` is a candidate preview. The manifest calls it assembled pending full playback and dubbing. It was not moved.
- `07_generations/accepted/` is empty. Chapter `acceptedTakeId` values are null. A candidate is not an accepted take.
- `inbox/Photos-Andre-Suit/` and `inbox/instagram-andreathar/` are extra intake. They were not reclassified. No inbox file is an approval.

```text
Movies_Projects/
  .hermes/
  .hermes/plans/
  .hermes/skills/
  agents/
  docs/
  docs/archive/
  inbox/
  inbox/andre-reference-photos/
  inbox/andre-voice/
  inbox/failed-clips/
  memory/
  projects/
  projects/andre-time-travel/
  projects/andre-time-travel/00_brief/
  projects/andre-time-travel/00_brief/research/
  projects/andre-time-travel/00_brief/research/snapshots/
  projects/andre-time-travel/01_script/
  projects/andre-time-travel/01_script/translations/
  projects/andre-time-travel/02_references/
  projects/andre-time-travel/02_references/andre/
  projects/andre-time-travel/02_references/andre/approved/
  projects/andre-time-travel/02_references/andre/raw/
  projects/andre-time-travel/02_references/andre/selected/
  projects/andre-time-travel/02_references/andre/synthetic/
  projects/andre-time-travel/02_references/history-eyes/
  projects/andre-time-travel/02_references/history-eyes/caesar/
  projects/andre-time-travel/02_references/history-eyes/galileo/
  projects/andre-time-travel/02_references/history-eyes/genghis/
  projects/andre-time-travel/02_references/history-eyes/napoleon/
  projects/andre-time-travel/02_references/history-eyes/oppenheimer/
  projects/andre-time-travel/02_references/legacy/
  projects/andre-time-travel/02_references/legacy/quarantined/
  projects/andre-time-travel/02_references/table/
  projects/andre-time-travel/02_references/wardrobe/
  projects/andre-time-travel/03_bibles/
  projects/andre-time-travel/03_bibles/scene-bibles/
  projects/andre-time-travel/04_audio/
  projects/andre-time-travel/04_audio/en/
  projects/andre-time-travel/04_audio/historical/
  projects/andre-time-travel/04_audio/historical/caesar/
  projects/andre-time-travel/04_audio/historical/galileo/
  projects/andre-time-travel/04_audio/historical/genghis/
  projects/andre-time-travel/04_audio/historical/napoleon/
  projects/andre-time-travel/04_audio/historical/oppenheimer/
  projects/andre-time-travel/04_audio/stems/
  projects/andre-time-travel/04_audio/stems/ambience/
  projects/andre-time-travel/04_audio/stems/dialogue/
  projects/andre-time-travel/04_audio/stems/foley/
  projects/andre-time-travel/04_audio/stems/music/
  projects/andre-time-travel/04_audio/voice-tests/
  projects/andre-time-travel/05_storyboard/
  projects/andre-time-travel/05_storyboard/animatics/
  projects/andre-time-travel/05_storyboard/contact-sheets/
  projects/andre-time-travel/05_storyboard/keyframes/
  projects/andre-time-travel/05_storyboard/keyframes/caesar/
  projects/andre-time-travel/05_storyboard/keyframes/galileo/
  projects/andre-time-travel/05_storyboard/keyframes/genghis/
  projects/andre-time-travel/05_storyboard/keyframes/napoleon/
  projects/andre-time-travel/05_storyboard/keyframes/oppenheimer/
  projects/andre-time-travel/06_pilot/
  projects/andre-time-travel/06_pilot/originals/
  projects/andre-time-travel/06_pilot/reviews/
  projects/andre-time-travel/06_pilot/speech-variants/
  projects/andre-time-travel/07_generations/
  projects/andre-time-travel/07_generations/accepted/
  projects/andre-time-travel/07_generations/originals/
  projects/andre-time-travel/07_generations/rejected/
  projects/andre-time-travel/07_generations/requests/
  projects/andre-time-travel/07_generations/responses/
  projects/andre-time-travel/08_edit/
  projects/andre-time-travel/08_edit/normalized/
  projects/andre-time-travel/08_edit/picture-lock/
  projects/andre-time-travel/08_edit/subtitles/
  projects/andre-time-travel/08_edit/timelines/
  projects/andre-time-travel/09_delivery/
  projects/andre-time-travel/09_delivery/captions/
  projects/andre-time-travel/09_delivery/qc/
  projects/andre-time-travel/09_delivery/stems/
  projects/andre-time-travel/agents/
  projects/andre-time-travel/docs/
  projects/andre-time-travel/logs/
  projects/andre-time-travel/memory/
  projects/andre-time-travel/tasks/
  reports/
  scripts/
  shared/
  shared/templates/
  skills/
  skills/andre-time-travel/
  tasks/
  tests/
```

## Entry points

- `README.md`: startup links and offline commands.
- `AGENTS.md`: rules for every agent working here.
- `workspace.json`: film registry and required layout.
- `projects/andre-time-travel/docs/production-plan.md`: canonical film plan.
- `projects/andre-time-travel/tasks/board.json`: authoritative production tasks.
- `projects/andre-time-travel/memory/STATE.md`: resume state and known gaps.
- `scripts/manage.py`: offline read-only status/validation.
- `reports/setup-verification.json`: real test, lint, source-mapping and layout verification output.

Shared/profile skills are linked, not duplicated. The project-specific procedure lives in `skills/andre-time-travel/`. Agent briefs are roles for explicit delegation, not running bots. Reference files and generation outputs are not approved by scaffold validation.
