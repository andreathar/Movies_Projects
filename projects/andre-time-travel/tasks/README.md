# Film tasks

| Path | Holds | Status authority |
|---|---|---|
| `board.json` | The live production board (T01–T21). | Yes, the only one. Producer applies changes. |
| `specs/` | Execution specifications: what each task must deliver and how it is checked. | No. |
| `plans/` | Planning documents: workflow map (W01–W68), cleanup plan. Dated views, never a second board. | No. |

New files are named `YYYY-MM-DD-topic-vN`. Board entries cite their spec as `specs/<file>` in the `specification` field. Glossary of board task, work package and Parley assignment: `../../../tasks/README.md`.

## Moved files (old path to current path)

Delivered documents, reviews and handoffs cite the pre-split paths and keep them as provenance. Resolve them here.

| Old path | Current path |
|---|---|
| `tasks/production-tasks.md` | `tasks/specs/production-tasks.md` |
| `tasks/scene-detail-assets-v1.md` | `tasks/specs/scene-detail-assets-v1.md` |
| `tasks/workflow-map-v1.md` | `tasks/plans/workflow-map-v1.md` |
| `tasks/project-cleanup-plan-v1.md` | `tasks/plans/project-cleanup-plan-v1.md` |
