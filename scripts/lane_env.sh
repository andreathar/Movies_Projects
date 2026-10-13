# scripts/lane_env.sh — export lane identity + Respan cost tags in one place.
# Usage (in the lane shell, BEFORE `agent-parley run <participant>`):
#     source scripts/lane_env.sh <lane-name> <film-role> <scene-id> [episode]
# Example:
#     source scripts/lane_env.sh codex-edit-qc editor S04-galileo
# Effects:
#   MOVIES_LANE_NAME / MOVIES_LANE_ROLE   -> film gate hooks (docs/PARLEY_PROTOCOL.md)
#   RESPAN_WORKFLOW_NAME=<scene-id>       -> Respan groups every turn of this lane under the scene
#   RESPAN_METADATA={lane,role,scene,episode} -> filterable span metadata
# Project-wide defaults (customer_id, project, episode) live in .codex/respan.json and .claude/respan.json.
# Producer shell: export MOVIES_PRODUCER_LANE=1 yourself; this script never does.
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "usage: source scripts/lane_env.sh <lane-name> <film-role> <scene-id> [episode]" >&2
  return 2 2>/dev/null || exit 2
fi
export MOVIES_LANE_NAME="$1"
export MOVIES_LANE_ROLE="$2"
export RESPAN_WORKFLOW_NAME="$3"
_ep="${4:-andre-time-travel}"
export RESPAN_METADATA="{\"lane\":\"$1\",\"role\":\"$2\",\"scene\":\"$3\",\"episode\":\"$_ep\"}"
unset _ep
echo "lane=$MOVIES_LANE_NAME role=$MOVIES_LANE_ROLE scene=$RESPAN_WORKFLOW_NAME (Respan workflow)"
