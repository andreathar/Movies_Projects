#!/usr/bin/env bash
# Inventário local sem executar Kling, acessar sessão ou instalar pacote.
# --check-published acrescenta consultas públicas npm, sem consultar conta/generação.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../../../" && pwd)"
SKILL="$ROOT/.agents/skills/kling-cli/SKILL.md"
if command -v kling >/dev/null 2>&1; then
  KLING_EXECUTABLE="$(command -v kling)" node --input-type=module <<'JS'
import {readFileSync,realpathSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
const entry=realpathSync(process.env.KLING_EXECUTABLE);
const manifest=JSON.parse(readFileSync(resolve(dirname(entry),'../package.json'),'utf8'));
console.log(JSON.stringify({executable:entry,package:manifest.name,version:manifest.version,repository:manifest.repository},null,2));
JS
else
  echo 'kling: não instalado'
fi
if [[ -f "$SKILL" ]]; then
  echo 'Versão e revisão da skill (independentes do executável):'
  sed -n '1,7p' "$SKILL"
fi
if [[ "${1:-}" == '--check-published' ]]; then
  npm view @klingai/cli-global version --registry=https://registry.npmjs.org
fi
