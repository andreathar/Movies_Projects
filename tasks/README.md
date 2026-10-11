# Tasks

The active production board is `../projects/andre-time-travel/tasks/board.json`; detailed task specifications are beside it. Setup did not complete any production task. Status values: pending, ready, blocked, in_progress, completed, cancelled. A completed task requires verified deliverable paths and a verification timestamp. The parent applies transitions after review.

## What "task" means in this workspace

| Term | Example | Where it lives | Source of truth |
|---|---|---|---|
| Board task | `T13` | `projects/<film>/tasks/board.json` | The board. Status is production status. |
| Work package | `W43` | `projects/<film>/tasks/workflow-map-v1.md` | A finer breakdown of board tasks. Not a second board, never a status of its own. |
| Parley assignment | a dispatch message plus path reservations | Agent Parley mail and reservations, outside the repository | Coordination only. A lane report of `ready` means ready for review, never done. Issue claims are not used here because there is no forge remote workflow (`docs/PARLEY_PROTOCOL.md`). |

Rules of thumb. A board task changes status only through the producer after verified evidence. A work package is a unit of assignment inside a board task. A Parley assignment records who was asked to do what, and which paths they reserved.

This root folder holds no board and no specification. It exists because `workspace.json` lists it as a required directory. Everything live is in each film's own `tasks/` folder: the board, the execution specification `production-tasks.md`, and planning documents such as the workflow map. New files there are named `YYYY-MM-DD-topic-vN`.
