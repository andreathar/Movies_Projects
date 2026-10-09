# 12 · Custos e ledger

**Correção importante a uma suposição anterior minha:** eu tinha escrito que os custos observados eram ~2× a tabela. Ao cruzar o ledger com os horários e as janelas de saldo, **isso não se sustenta**. As anomalias vêm de jobs rodando ao mesmo tempo, não de preço fora da tabela (detalhe abaixo). Status: **[INFERÊNCIA forte]**, a ser confirmada pelo producer. O próprio ledger já suspeitava ("possibly a concurrent account charge", LNOTE-R3-anomaly); aqui se identifica qual era a cobrança concorrente: os jobs `gemini-3-pro-image` do mesmo projeto.

## 1. Tabela de preços (créditos por segundo de saída)

Fonte: tabela de API do Kling transcrita em 2026-08-04 por uma skill de terceiros, em "unidades por segundo" (1 unidade = US$ 0,14). A conversão **1 unidade = 10 créditos** é minha [INFERÊNCIA], e bate com os custos limpos do projeto (seção 2).

| Modelo · configuração | 720p | 1080p | 4K |
|---|---|---|---|
| VIDEO 3.0 · sem áudio | 6 | 8 | 30 |
| VIDEO 3.0 · áudio nativo (sem controle de voz) | 9 | 12 | 30 |
| VIDEO 3.0 Turbo · (só com áudio) | 8 | 10 | — |
| VIDEO 3.0 Omni · sem vídeo de entrada, sem áudio | 6 | 8 | 30 |
| VIDEO 3.0 Omni · sem vídeo de entrada, com áudio | 8 | 10 | 30 |
| VIDEO 3.0 Omni · com vídeo de entrada, sem áudio | 9 | 12 | 30 |
| Motion Control 3.0 | 9 | 12 | — |
| Avatar 2.0 (fora do CLI) | 4 | 8 | — |

Voice Control (app/API): +2 cr/s sobre o vídeo [OFICIAL via terceiros]; para assinantes aparece como grátis na página de planos [TERCEIROS]. `imageCount` N multiplica por N. Não há tabela pública para `o1`, `v2_5`, `v2_6` neste levantamento.

Imagens (observado no projeto, créditos por imagem a 2K) [PROJETO]:

| Modelo | Créditos/imagem |
|---|---|
| `kling-image-o1` | 1 |
| `kling-image-v3_0_omni` | 2 |
| `gemini-3.1-flash-image` | 15 |
| `gemini-3-pro-image` | 20 |

`element_create` do Element "Andre v2" aparece como 180 no ledger, mas a janela contém 3 jobs de 20 créditos (ver 3): o custo real do Element deve ser ~120 [INFERÊNCIA].

## 2. Custos de vídeo do projeto contra a tabela [PROJETO + tabela]

| Job | Config | Tabela | Ledger | Leitura |
|---|---|---|---|---|
| PILOT-01 | v3_0 · 5 s · 720p · mudo | 30 | 70 | janela contém R2-J03 (40) |
| PILOT-02 | idem | 30 | 70 | janela é a mesma de R2-J04 (70) |
| PILOT-03 | idem | 30 | **30** | janela limpa: bate |
| PILOT-04 | v3_0 · 8 s · 720p · áudio | 72 | **72** | bate |
| PILOT-05 | idem | 72 | 92 | +20 sem entrada correspondente |
| G-03, G-05 | turbo · 5 s · 720p | 40 | **40** | bate |
| G-01 v2 / UNCERTAIN | turbo · 10 s · 720p | 80 | **80** | bate |
| G-02 GL02 | v3_0 · 12 s · 720p · áudio | 108 | **108** | bate |

Todo vídeo "limpo" bate com a tabela. As exceções (PILOT-01, -02, -05) são exatamente múltiplos de 20, o custo de uma imagem `gemini-3-pro-image`.

## 3. O que está errado no ledger (para o producer)

O ledger reconcilia custo pela **diferença de saldo** (`X->Y`). Quando dois jobs correm ao mesmo tempo, a mesma queda de saldo é atribuída aos dois [INFERÊNCIA com evidência nos próprios dados]:

- Janela **6539→6498** (41): `R3-oppenheimer-speaking-o1-v2` (o1, 1 cr) e `R2-J02` (gemini, 2×20 = 40) recebem 41 cada. Real: 41 no total.
- Janela **6425→6355** (70): `R2-J04` (gemini) e `PILOT-02` (vídeo 30) recebem 70 cada. Real: 40 + 30.
- Janela **6495→6425** (70) de `PILOT-01` contém a janela 6465→6425 (40) de `R2-J03`. Real: 30 + 40.
- Janela do Element (6776→6596 = 180) contém três janelas de 20 (6776→6756→6736→6716).
- Quedas sem entrada: `PILOT-05` +20 e alguns saltos de 5 créditos.

Soma do ledger: **2.300**. Soma das janelas únicas: **2.049**. Variação real de saldo 7.741→5.813: **1.928** (se não houve crédito entrando). Ou seja, o ledger **superestima algo entre ~250 e ~370 créditos**. Não corrija sozinho; é do producer (ledger é dele). Sugestão: marcar essas linhas com `charge_status` = `window_overlap_do_not_sum`.

## 4. Como registrar sem erro daqui para frente

1. **Um job pago por vez**: espere o estado final (`query_tasks --poll`) antes de submeter o próximo.
2. Registre `creditsConsumed` da **resposta de submissão** quando existir. O ledger repete que o provedor "não retornou creditsConsumed" (L001, LNOTE-R3-anomaly): confira se o campo vem na resposta do CLI (`--quiet` dá JSON compacto) e, se vier, use-o em vez de inferir pelo saldo.
3. Se precisar de saldo: `kling account` antes e depois, **com nenhum outro job em andamento**.
4. Se dois jobs forem inevitáveis, registre a soma uma vez e divida pela tabela.
5. Sempre: `generationId`, `shot_id`, modelo, argumentos, `authorization_ref`, sha256 do download.

## 5. Planejamento de orçamento

Conta atual (2026-10-09 15:04) [LIVE]: plano **Ultra**, saldo **31.621** — um salto de 5.813 → 31.621 sem registro no ledger; o producer deve anotar a origem (renovação/plano). Para estimar: `segundos × cr/s × imageCount`, com tabela da seção 1, e some 25% de folga para refazer. A autorização por job continua obrigatória.
