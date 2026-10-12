# 12 · Custos e ledger

## Estado da evidência (revisão 2026-10-12)

As tabelas abaixo são **histórico/estimativa**, não cotação. A relação 1 unidade da API
= 10 créditos desta conta não foi comprovada. Sobreposição de janelas de saldo torna
insegura a atribuição por job; as hipóteses anteriores foram preservadas para revisão,
não confirmadas como preço real. Não reescrever o ledger histórico com base nelas.

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

`element_create` do Element "Andre v2" aparece como 180 no ledger, mas a janela contém 3 jobs de 20 créditos (ver 3): a hipótese anterior de ~120 permanece não confirmada [INFERÊNCIA].

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

- Janela **6539→6498** (41): `R3-oppenheimer-speaking-o1-v2` (o1, 1 cr) e `R2-J02` (gemini, 2×20 = 40) recebem 41 cada. A janela caiu 41; atribuição individual não comprovada.
- Janela **6425→6355** (70): `R2-J04` (gemini) e `PILOT-02` (vídeo 30) recebem 70 cada. Hipótese: 40 + 30, sem prova individual.
- Janela **6495→6425** (70) de `PILOT-01` contém a janela 6465→6425 (40) de `R2-J03`. Hipótese: 30 + 40, sem prova individual.
- Janela do Element (6776→6596 = 180) contém três janelas de 20 (6776→6756→6736→6716).
- Quedas sem entrada: `PILOT-05` +20 e alguns saltos de 5 créditos.

Soma do ledger: **2.300**. Soma das janelas únicas: **2.049**. Variação real de saldo 7.741→5.813: **1.928** (se não houve crédito entrando). Ou seja, o ledger **superestima algo entre ~250 e ~370 créditos**. Não corrija sozinho; é do producer (ledger é dele). Sugestão: marcar essas linhas com `charge_status` = `window_overlap_do_not_sum`.

## 4. Registro a partir desta revisão

1. O produtor submete um job por vez com `--submit-only`; retoma o ID com `--resume`.
   Nunca repete submissão incerta, mesmo que haja autorização histórica de teto.
2. Registre `creditsConsumed` retornado pela submissão, inclusive zero, com origem
   `provider_reported`. Não invente o campo se ausente.
3. Saldo antes/depois e `creditsDelta` são observações da conta. O lock local não
   impede uso no site/outro processo, cobrança tardia, renovação ou crédito entrando.
   Ausência de concorrência aparente não transforma delta em custo comprovado.
4. O runner deixa a coluna de cobrança vazia se o provedor não informar valor. Não
   divide uma janela por tabela nem soma a mesma variação em mais de um job.
5. Preserve `generationId`, job, modelo, argumentos, referência de autorização,
   schema e SHA-256 do download. Recibos e ledger anteriores não são reescritos.

## 5. Planejamento, cotação e duração

Uma estimativa identifica fonte/data, hipóteses, duração de saída, duração de entrada
quando tarifada, número de resultados, resolução, áudio e Element. Cotação exige
valor explícito do provedor para o pedido/configuração. Esta auditoria não obteve
cotação, não consultou saldo para gastar e não testou geração.

O saldo 31.621 mencionado na versão anterior é observação de 2026-10-09, não saldo
atual. Os 90 créditos do A/B eram estimativa; o teste não isolava resolução. Motion 1
é descrito como 30 s no registro anterior, incompatível com a previsão de 45/60 para
5 s. O prompt não altera a duração do ativo. Sob a taxa histórica hipotética de 9/12
seriam 270/360 para 30 s, **sem confirmação de preço**. Reconfirmar recurso, duração,
compatibilidade e orçamento antes de propor execução; não gastar para descobrir isso.

Ver [17 · Integração CLI](17-integracao-cli.md). Nenhum preço, revisão de texto ou
saldo constitui autorização de produção.
