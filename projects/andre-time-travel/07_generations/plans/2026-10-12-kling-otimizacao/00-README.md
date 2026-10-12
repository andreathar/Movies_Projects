# Otimização do uso do Kling — pacote preparado (2026-10-12)

**Estado: PREPARADO. Nenhum crédito gasto, nenhuma submissão feita.** Todos os comandos e
specs aqui estão prontos para execução, mas **bloqueados** até autorização explícita de Andre
(`00_brief/approvals.json` → `paidGenerationBatchApproved: false`).

Origem da investigação (2026-10-12): CLI instalada `0.2.1` **é a última** nas duas regiões; a
sensação de "não fica tão bom quanto a interface" tem causa identificável e corrigível.

## Diagnóstico em uma linha

Todos os vídeos do projeto foram gerados em **720p** (`std`), enquanto o default do servidor e
da interface é **1080p** (`pro`); e para imagem única o modelo recomendado (`turbo`) não está
sendo usado. O prompt em si é bom.

## O que este pacote entrega

| # | Item | Arquivo | Gasta? |
|---|------|---------|--------|
| 1 | Atualizar skill 0.2.0 → 0.2.1 (+ `omni_ref_video`) | `01-upgrade-skill.md` | não — **feito 2026-10-12** |
| 2 | Conferir/regerar ficha de modelos (higiene; snapshot atual já está correto) | `02-regerar-ficha-modelos.md` | não |
| 3 | Política de resolução (720p = rascunho; 1080p/4K = take) | `03-politica-de-resolucao.md` | não |
| 4 | Teste A/B resolução × modelo (galileu-ouvindo) | `ab-teste-resolucao-modelo.json` | sim (90–336 cr) |
| 5 | Guia de prompt para **motion control** (andar A→B) | `04-guia-prompts-motion-control.md` | não |
| 6 | Specs preparadas de motion control | `motion-control-specs.json` | sim (45–105 cr) |

## Custos estimados (tabela `12`, créditos)

| Caminho | Config | Custo |
|---------|--------|-------|
| AB-01 | `turbo` · 5 s · 1080p · mudo | 50 |
| AB-02 | `v3_0` · 5 s · 1080p · mudo · Element | 40 |
| AB-03 (opcional) | `v3_0` · 5 s · **4K** · mudo | 150 |
| AB-04 (opcional) | `v3_0` · 8 s · 1080p · áudio (fala GL04) | 96 |
| MC-01 | `motion_control` · ~5 s · 720p · mudo | 45 |
| MC-02 | `motion_control` · ~5 s · 1080p · mudo | 60 |

- Núcleo A/B (AB-01+AB-02): **90 cr**.
- Núcleo motion (MC-01): **45 cr**.
- Pacote completo (AB-01..04 + MC-01..02): **441 cr** ≈ 1,4 % do saldo 31.621 (Ultra).
- Rota motion com vídeo próprio (`--video`): + custo de motion por segundo, ver guia.

## Dependências e donos

- **Autorização de gasto**: Andre (gate `paidGenerationBatchApproved`). Sem isso, nada roda.
- **Runner pago**: apenas `scripts/kling_batch.py` (lane producer). Ver `AGENTS.md` e
  `.claude/hooks/kling-preflight.py`. Os specs usam `auth` placeholder — **trocar por um APR real**.
- **Itens 1 e 2** são de ambiente (sem crédito): dono = producer. Não interrompem geração.
- **Item 5 (prompts)**: usar antes de qualquer `motion_control`.

## Como rodar (somente após autorização)

```bash
# 1) validar specs sem gastar
.venv/bin/python docs/kling-manual/tools/kling_preflight.py <spec-ou-request>
# 2) saldo antes (nada mais rodando)
kling account -q --skill-name kling-cli --skill-version 0.2.1
# 3) submeter UM job por vez
.venv/bin/python scripts/kling_batch.py --spec projects/andre-time-travel/07_generations/plans/2026-10-12-kling-otimizacao/ab-teste-resolucao-modelo.json --only AB-01-turbo-1080p --submit-only
# 4) consultar depois (nunca reenviar)
.venv/bin/python scripts/kling_batch.py --resume AB-01-turbo-1080p
```

## Critérios de aceite do teste A/B

Comparar no mesmo keyframe e mesmo prompt: nitidez/pele, estabilidade de identidade ao longo do
take, artefatos de movimento, e custo real vs tabela. Registrar 1 take recomendado por variante
em `13-qc-e-aceitacao.md`. **Não** promover nenhum take a aprovado sem playback em velocidade real
e aceite de Andre.
