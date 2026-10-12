# 03 · Política de resolução (o ajuste de maior impacto)

## O problema

**Todos** os vídeos do projeto foram gerados com `resolution: 720p` explícito
(PILOT-01..05, G-01..G-05, G-02 — ver `07_generations/responses/*.intent.json`).

- `720p` = tier **`std`** (rótulo do próprio Kling); `1080p` = `pro`; `4k` = membro.
- O **default do servidor é 1080p** em toda ferramenta de vídeo (`who_am_i` ao vivo).
- A **interface web** usa esse default — 1080p (4K para membros).

Ou seja: o projeto produziu deliberadamente no tier barato e comparou com o tier `pro` da
interface. **Este é o principal motivo da diferença percebida.**

## Política proposta

| Uso | `resolution` | Observação |
|-----|--------------|------------|
| Teste de composição / movimento / prompt (descartável) | `720p` | mantém o custo baixo para iterar |
| **Take de produção (o que entra no corte)** | **`1080p`** | default do provedor e da interface |
| Plano herói, se exigir detalhe (rosto grande, inserto de mesa) | `4k` | 30 cr/s; usar com parcimônia |
| `motion_control` (produção) | `1080p` | default é 720p; subir explicitamente |

Regra curta: **rascunho em 720p, take em 1080p, herói em 4K.**

## Custo (tabela `12`, créditos por segundo de saída)

| Modelo · config | 720p | 1080p | 4K |
|---|---|---|---|
| VIDEO 3.0 · sem áudio | 6 | 8 | 30 |
| VIDEO 3.0 · áudio nativo | 9 | 12 | 30 |
| VIDEO 3.0 Turbo | 8 | 10 | — |
| Motion Control 3.0 | 9 | 12 | — |

Exemplos: 5 s mudo sobe de 30 (720p) para 40 (1080p); fala de 8 s sobe de 72 para 96; 4K a 30/s
faz um plano de 5 s custar 150. Saldo atual 31.621 (Ultra): um take de 1080p de 5 s ≈ 0,13 %.

## Impacto esperado

- 1080p entrega pele, olhos e grão visivelmente mais definidos — é exatamente onde o filme
  compara com a interface.
- 4K ajuda em close-ups de rosto e no detalhe da mancha da mesa, mas quadruplica o custo; reservar.
- Não confundir com prompt: subir a resolução **não** conserta enquadramento, identidade ou
  movimento. A ordem é: composição/prompt → 1080p → (4K só no herói).

## Como aplicar

- Nos specs/jobs: trocar `"resolution": "720p"` por `"1080p"` (ou `"4k"`).
- Nos documentos do manual (`06`, `07`, `09`) e nos comandos-modelo: atualizar o default para 1080p.
- Registrar no ledger o `creditsConsumed` real por job e comparar com a tabela `12`.
- O A/B (`ab-teste-resolucao-modelo.json`) mede isso no mesmo keyframe antes de mudar a produção.
