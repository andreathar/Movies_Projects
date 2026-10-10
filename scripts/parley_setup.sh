#!/usr/bin/env bash
# Phase 0 runbook for Agent Parley on Andre's machine (docs/PLAN-parley-integration-v1.md, P0.1-P0.4).
#
# Run from the base checkout as the operator (Andre). Default is a dry run that
# prints each step. `--apply` runs the read-only and setup steps (doctor, up,
# init set, pool set) and writes evidence under reports/parley-setup-v1/.
# Lanes are never launched by this script: one `agent-parley run` per terminal,
# by hand, as docs/PARLEY_PROTOCOL.md requires. Nothing here spends, commits,
# merges or changes approvals.

set -euo pipefail

REPO="${REPO:-$(cd "$(dirname "$0")/.." && pwd)}"
EVIDENCE="$REPO/reports/parley-setup-v1"
APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1

step() { printf '\n== %s\n' "$1"; }
show() { printf '   $ %s\n' "$*"; if [[ $APPLY -eq 1 ]]; then "$@"; fi; }

step "P0.1 doctor (read-only)"
show agent-parley doctor
if [[ $APPLY -eq 1 ]]; then
  mkdir -p "$EVIDENCE"
  agent-parley doctor --json > "$EVIDENCE/doctor.json"
  printf '   evidence: %s\n' "$EVIDENCE/doctor.json"
fi

step "P0.2 service, repository registration, lane init command, no spare worktrees"
show agent-parley up
show agent-parley status --repo "$REPO"
show agent-parley init set 'python3 -m venv .venv' --repo "$REPO"
show agent-parley pool set 0 --repo "$REPO"

step "P0.3 launch three lanes, one terminal each (NOT run by this script)"
cat <<EOF
   terminal 1:  agent-parley run claude-research --provider claude --repo "$REPO"
   terminal 2:  agent-parley run codex-edit-qc   --provider codex  --repo "$REPO"
   terminal 3:  agent-parley run claude-review   --provider claude --repo "$REPO"
                (add --credentials account-2 if the two Claude lanes must not share a login)
   In each lane shell before launch, export the film gate identity:
     export MOVIES_LANE_NAME=<lane name>  MOVIES_LANE_ROLE=<film role for this assignment>
   On the base checkout only (producer):  export MOVIES_PRODUCER_LANE=1
   Never pass a bypass or skip-permissions flag; resume lane approvals by hand.
EOF

step "P0.4 producer reservations (from the base checkout, in the producer's Parley session)"
cat <<EOF
   Reserve with no TTL: workspace.json AGENTS.md CLAUDE.md
     projects/andre-time-travel/{manifest.json,tasks/board.json,00_brief/approvals.json,
     00_brief/decisions/,credit-ledger.csv,asset-registry.csv,memory/STATE.md,
     memory/session-log.json,memory/mistakes.jsonl}
   Reserve the named resource: kling:submit
   Record the reservation IDs in $EVIDENCE/reservations.json
EOF

step "P0.5 smoke test and P0.6 hook proof"
printf '   follow docs/parley-smoke-test.md; evidence goes to %s\n' "$EVIDENCE"

step "P0.7 supervision for human gates"
cat <<EOF
   Lengthen stalled_after and claim_idle_after to one working day in the project
   settings (agent-parley docs/operations.md, supervision section) so Andre's
   review time never triggers wake, offer and release. Confirm with:
     agent-parley status --json --repo "$REPO"
EOF

step "verify gate (Andre only, when he decides to use participant merge)"
printf '   agent-parley verify set ".venv/bin/python scripts/manage.py validate && .venv/bin/python -m unittest discover -s tests" --repo "%s"\n' "$REPO"
printf '\nDry run complete. Re-run with --apply to execute the setup steps.\n'
