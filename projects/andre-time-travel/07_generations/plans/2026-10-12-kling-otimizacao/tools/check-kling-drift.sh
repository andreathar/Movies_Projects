#!/usr/bin/env bash
# Read-only drift check between the installed Kling CLI, the published npm versions,
# and the packaged skill version. Never logs in, never generates, never reads .credentials.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../../../" && pwd)"
SKILL="$ROOT/.agents/skills/kling-cli/SKILL.md"

echo "== CLI =="
if command -v kling >/dev/null 2>&1; then
  kling --version
else
  echo "kling: NOT INSTALLED"
fi

echo "== npm latest (global / cn) =="
npm view @klingai/cli-global version 2>/dev/null || echo "global: lookup failed"
npm view @klingai/cli-cn version 2>/dev/null || echo "cn: lookup failed"

echo "== installed package =="
npm ls -g --depth=0 2>/dev/null | grep -i kling || echo "(none)"

echo "== skill frontmatter =="
if [[ -f "$SKILL" ]]; then
  sed -n '1,4p' "$SKILL"
  if grep -q 'omni_ref_video' "$SKILL"; then
    echo "omni_ref_video: present"
  else
    echo "omni_ref_video: MISSING (skill behind CLI)"
  fi
else
  echo "skill file not found: $SKILL"
fi

echo "== telemetry version in runner =="
grep -n 'skill-version' "$ROOT/scripts/kling_batch.py" 2>/dev/null || true
