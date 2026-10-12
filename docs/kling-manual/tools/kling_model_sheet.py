#!/usr/bin/env python3
"""Gera a ficha de modelos (markdown) a partir do snapshot sanitizado de `kling who_am_i`.

Offline, só stdlib, não chama o Kling e não gasta crédito.

Uso:
  python3 -I tools/kling_model_sheet.py snapshots/who_am_i.sanitized.json > 03-modelos-ao-vivo.md
"""
import hashlib
import json
import sys


def cell(v):
    if v is None:
        return ""
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return str(v).replace("|", "\\|").replace("\n", " ")


def main(path):
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    snap = json.loads(raw)
    meta = snap.get("_meta", {})
    body = snap["body"]
    models = body["availableModels"]

    out = []
    w = out.append
    w("# 03 · Modelos observados [SNAPSHOT]")
    w("")
    w("> Gerado por `tools/kling_model_sheet.py` — **não editar à mão**.")
    w(f"> Fonte: `snapshots/who_am_i.sanitized.json` (sha256 `{sha}`), capturado em {meta.get('captured', '?')} via `kling who_am_i`; `mcpVersion` {body.get('mcpVersion')}.")
    w("> Snapshot datado, não cotação nem promessa de acesso futuro. Antes de produzir, consulte `kling who_am_i`, remova identidade e segredos e gere nova ficha.")
    w("")
    w("## Índice rápido")
    w("")
    w("| Ferramenta | Modelo padrão | Modelos disponíveis |")
    w("|---|---|---|")
    for tool, v in models.items():
        names = ", ".join(f"`{m['model']}`" for m in v["models"])
        w(f"| `{tool}` | `{v.get('defaultModel') or '—'}` | {names} |")
    w("")

    for tool, v in models.items():
        w(f"## `{tool}`")
        w("")
        w(f"Padrão: `{v.get('defaultModel') or '(nenhum — escolha explícita)'}`. **Sempre passe `--model` explicitamente.**")
        w("")
        for m in v["models"]:
            w(f"### `{m['model']}`")
            w("")
            if m.get("alias"):
                w(f"- Alias: {cell(m['alias'])}")
            if m.get("description"):
                w(f"- Descrição (Kling): {cell(m['description'])}")
            for extra in ("combinedItemCap", "combinedItemCaps", "elementSupport"):
                if extra in m:
                    w(f"- `{extra}`: `{json.dumps(m[extra], ensure_ascii=False)}`")
            w("")
            args = m.get("arguments") or []
            if args:
                w("| Argumento | Obrig. | Padrão | Valores permitidos | Descrição |")
                w("|---|---|---|---|---|")
                for a in args:
                    w(f"| `{a['name']}` | {'sim' if a.get('required') else 'não'} | {cell(a.get('default'))} | {cell(a.get('allowedValues'))} | {cell(a.get('description'))} |")
                w("")
            ins = m.get("inputs") or []
            if ins:
                w("| Input (slot) | Obrig. | Descrição |")
                w("|---|---|---|")
                for i in ins:
                    w(f"| `{i['name']}` | {'sim' if i.get('required') else 'não'} | {cell(i.get('description'))} |")
                w("")
            else:
                w("_Sem slots de input declarados._")
                w("")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
