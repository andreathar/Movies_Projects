#!/bin/bash
# SessionStart hook for Claude Code cloud sessions (Movies_Projects).
# Intended path: .claude/hooks/session-start.sh (chmod +x), registered in
# .claude/settings.json under hooks.SessionStart.
# Runs only in a remote container. Makes the documented stdlib commands work:
#   .venv/bin/python scripts/manage.py validate
#   .venv/bin/python -m unittest discover -s tests
# It never edits tracked files, skills/registry.json, approvals or media.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$ROOT"

# 1. Project venv. The management tools and tests use only the standard
#    library, so no packages are installed; the venv exists so README commands
#    written as .venv/bin/python run unchanged.
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi

# 2. Machine-local skill links. skills/registry.json records symlinks into the
#    owner's Hermes profile (/home/athar/.hermes/...), which does not exist in a
#    cloud container, so manage.py validate exits 2 and two tests fail. Create a
#    clearly labelled placeholder SKILL.md at each missing target, outside the
#    repository. validate then passes and still reports the hash warning
#    "shared skill changed since linking", so the placeholder is never mistaken
#    for the real skill. Existing targets are left untouched.
python3 - <<'PY'
import json
from pathlib import Path

registry = json.loads(Path("skills/registry.json").read_text(encoding="utf-8"))
for skill in registry["skills"]:
    if skill.get("type") != "machine_local_symlink":
        continue
    if (Path(skill["path"]) / "SKILL.md").is_file():
        continue
    source = Path(skill["source"])
    skill_file = source / "SKILL.md"
    if skill_file.is_file():
        continue
    source.mkdir(parents=True, exist_ok=True)
    skill_file.write_text(
        f"---\nname: {skill['name']}\ndescription: Cloud-session placeholder. "
        "The real skill lives in the owner's local Hermes profile and is not "
        "available in this container.\n---\n\n"
        f"# {skill['name']} (placeholder)\n\n"
        "This file was created by .claude/hooks/session-start.sh so that "
        "manage.py validate and the unit tests can run in a Claude Code cloud "
        "session. It contains no procedure. Do not treat it as the skill, do "
        "not copy it into the repository, and do not update "
        "skills/registry.json hashes from it.\n",
        encoding="utf-8",
    )
    print(f"placeholder skill source created: {skill_file}")
PY

.venv/bin/python scripts/manage.py validate >/dev/null && echo "session-start: workspace validates"
