# 02 · Ficha de modelos: conferir / regerar (preparado, sem crédito)

## Estado atual (verificado 2026-10-12)

`docs/kling-manual/03-modelos-ao-vivo.md` foi gerada do snapshot
`docs/kling-manual/snapshots/who_am_i.sanitized.json` (capturado 2026-10-09, `mcpVersion` 1.3.3).
Comparado ao `who_am_i` ao vivo de hoje (também `1.3.3`), a ficha **está correta** — inclusive os
defaults de resolução, que variam por ferramenta:

| Ferramenta | Default `resolution` (ao vivo) | A ficha diz |
|------------|-------------------------------|-------------|
| `motion_control` (todos os modelos) | **720p** | 720p ✔ |
| `image_to_video` / `text_to_video` (todos) | **1080p** | 1080p ✔ |
| `omni_ref_video` | **1080p** | 1080p ✔ |

**Conclusão:** a ficha não está errada. O que rebaixava a qualidade era a **escolha explícita** de
`720p` nos jobs (ver `03-politica-de-resolucao.md`), não uma ficha desatualizada.

## Regerar (higiene, opcional)

```bash
# 1) capturar ao vivo (não gasta crédito)
kling who_am_i -q --skill-name kling-cli --skill-version 0.2.1 > /tmp/who_am_i.raw.json

# 2) sanitizar: remover body.user (dado de identidade) e adicionar _meta.captured
#    (mesmo procedimento usado em 2026-10-09; não deixar body.user no snapshot)

# 3) regenerar a ficha a partir do snapshot
cd docs/kling-manual
python3 -I tools/kling_model_sheet.py snapshots/who_am_i.sanitized.json > 03-modelos-ao-vivo.md
```

## Quando regerar

- Sempre que o `mcpVersion` do `who_am_i` mudar em relação ao do snapshot.
- Sempre que aparecer/desaparecer um modelo ou um argumento (comparar `availableModels`).
- Após atualizar a skill (item `01`), para confirmar que a lista ao vivo confere com a do skill.

## Não fazer

- Não editar `03-modelos-ao-vivo.md` à mão (é derivado).
- Não deixar `body.user` no snapshot (dado de identidade; o snapshot é versionado).
