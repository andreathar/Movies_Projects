# Plano de regeneração com custo — nova direção (personalidades de costas e desfocadas + legado)

Projeto: andre-time-travel · "The Table Between Centuries" · Papel: producer (delegado de envio pago e ledgers, bot Produção e Créditos 9bfe6c7d)
Data: 2026-10-09 ~12:45 (America/Sao_Paulo) · Status: **PROPOSTA — nenhum job enviado, nada gerado, ledgers inalterados.** Cada job precisa de OK explícito do Andre.

## 1. Saldo
- Consulta somente-leitura em 2026-10-09T12:37:08-03:00 no pop-os: `kling account -q --skill-name kling-cli --skill-version 0.2.0` (kling-cli 0.2.1, MCP `query_membership_and_credits`; mesmo comando que `scripts/kling_batch.py::account()` usa).
- Resultado: membershipType SSVIP (Premier), **availableRemainCredits = 5813**. Bate com a última linha do ledger (LG-02-andre-GL02, balance_after 5813). Snapshot histórico 7.741 (2026-10-08) não é saldo vivo.

## 2. Direção aplicada (STATE.md › NEW CREATIVE DIRECTION, 12:35)
Personalidades sentadas à mesa, vistas de COSTAS e DESFOCADAS (corpo/ombros/nuca/silhueta) enquanto o Andre fala; imagens intercaladas mostram o que elas se tornaram, como falam delas hoje e como os atos repercutiram, em tom íntimo. Zero rosto inteiro (AGENTS.md). Falas das figuras continuam off/de costas; nenhuma citação inventada.

Estrutura proposta por capítulo (8 eventos, fontes maiores que o slot de 42 s; a montagem corta):
REF bíblia de costas → KF keyframes OTS (o1+Element) → X01 estabelecimento de costas (L01) → X02 Andre fala L02 OTS → X03 LEGADO 1 → X04 figura de costas faz L03, Andre escuta ao fundo → X05 Andre fala L04 OTS → X06 LEGADO 2 → X07 LEGADO 3 → X08 fecho de costas.

## 3. Preços observados (base de cada estimativa)
| Código | Tipo de job | Preço usado | Base (credit-ledger.csv / 07_generations/responses) |
|---|---|---|---|
| O1 | kling-image-o1 2K + Element, 1 img | 1 cr | LR3-*-o1: 16 de 18 jobs = 1 (2 deltas de 41 em LNOTE-R3-anomaly, causa desconhecida) |
| PRO | gemini-3-pro-image i2i 2K, 1 img | 20 cr | creditsConsumed=20 em responses/R3-session-02..08; LR2-J10..J14 = 20 |
| TURBO | kling-video-v3_0_turbo i2v 720p, sem áudio/Element | 8 cr/s | LG-01-insert-galileo-v2 creditsConsumed=80 (10 s); LG-03/LG-05 = 40 (5 s) |
| V3A | kling-video-v3_0 i2v 720p + áudio nativo + Element | 9 cr/s | LG-02-andre-GL02 creditsConsumed=108 (12 s); LPILOT-04 = 72 (8 s) |
| V3S | kling-video-v3_0 i2v 720p sem áudio + Element | 6 cr/s (pior caso 14) | LPILOT-03 = 30 (5 s), igual à doc (6 cr/s, prompt-playbook-kling.md); LPILOT-01/02 = 70 vieram de deltas sobrepostos a jobs R2-J03/J04 concorrentes |

Durações de fala = segundos medidos no scratch (01_script/dialogue-lines.csv) + ≥2 s de cauda, arredondado para cima (regra do playbook). O-L04 recebe +2 s extras para o silêncio de ≥4 s.

## 4. Resumo por capítulo
| Capítulo | Takes/imagens novas | Subtotal (créditos) | Pior caso V3S a 14 cr/s | Só legado animado (TURBO) |
|---|---|---|---|---|
| ABERTURA | 4 | 178 | 178 | 0 |
| CESAR | 10 | 496 | 616 | 120 |
| GENGHIS | 10 | 505 | 625 | 120 |
| GALILEU | 10 | 523 | 643 | 120 |
| NAPOLEAO | 10 | 481 | 617 | 120 |
| OPPENHEIMER | 10 | 514 | 634 | 120 |
| FECHAMENTO | 5 | 264 | 304 | 40 |
| **TOTAL** | 59 | **2961** | **3617** | 640 |

## 5. Comparação com o saldo
- Saldo vivo: **5813**.
- Base (1 take por plano): **2961** → sobra 2852.
- Base + reserva de retake 30% (888): **3849** → sobra 1964.
- Pior caso (V3S a 14 cr/s) + reserva 30% (1085): **4702** → sobra 1111.
- Envelope v3 reservava 1.300 para correções/Edição H: cabe nos cenários base e base+reserva; no pior caso fica abaixo (sobra 1111).
- Opção B: animar os stills de legado localmente (Ken Burns/parallax, 0 cr) economiza 640 → base 2321.
- Teto do capítulo Galileu (900, stop 810) já tem 348 gastos; com o plano novo (523) passaria de 810 → precisa de nova autorização de escopo do Andre.

## 6. A descontar após triagem (Edição e Qualidade ainda não entregou)
Takes existentes que PODEM ser reaproveitados se a triagem quadro a quadro aceitar (nenhum mostra a figura de costas, que é o pedido central):
| Plano novo | Take existente | Desconto possível |
|---|---|---|
| G-X02 | G-02-andre-GL02_1 (G-L02 frontal, sem figura) | −108 |
| G-X05 | PILOT-04-galileo-speech-native_1 (G-L04, palavras duvidosas → ADR) | −99 |
| G-X04 | PILOT-01-galileo-listening-locked_1 (escuta) | −30 |
| G-X08 | PILOT-02-galileo-gentle-turn_1 (fecho) | −30 |
| G-X01 | G-01-insert-galileo-v2_1 (insert mão/papel, 10 s) | −30 |
| O-X05 | PILOT-05-oppenheimer-speech-OL04_1 (O-L04 + silêncio) | −72 |
| O-X08 | PILOT-03-oppenheimer-expression_1 | −30 |
| **Máximo** | | **−399** → base mínima 2562 |

Também reaproveitáveis como insumo (custo 0, não reduzem linhas): plates de era R1-J27..J32 e R2-plate-*; keyframes R3 KF-<era>-speaking/listening (como image_1, mas foram compostos com "ninguém mais no quadro" → o OTS exige keyframe novo); figurinos R1-J21..J25; inserts de mão R2-J10..J14; olhos G-03/G-05 e R1/R2 eyes (podem virar acento, a decidir pela Direção — a nova direção tira o foco dos olhos).

## 7. Lista de takes (detalhe em plano-regeneracao-takes.csv)
| Take | Descrição | Modelo | Dur. (s) | Créditos | Reaproveitável/insumo |
|---|---|---|---|---|---|
| IN-KF | Keyframes o1 com Element (3 quadros x 2 tentativas): mesa presente, Andre fala, match-cut | O1 |  | 6 |  |
| IN-01 | Mesa do presente, mao do Andre entra (insert sem rosto) | PRO + TURBO | 5 | 60 | R2-J10..J14 / R1-J32 plate como referencia (custo 0) |
| IN-02 | Andre fala IN-L01 (5.83s) a mesa; cadeiras opostas com 5 silhuetas de costas desfocadas (a confirmar com Direcao) | V3A | 8 | 72 |  |
| IN-03 | Match-cut pela mesa para Roma (sem rosto) | TURBO | 5 | 40 | keyframe = R1-J27 plate Roma (0 cr) |
| C-REF | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) | PRO |  | 40 | R1-J21..J25 figurino abaixo do pescoco como referencia |
| C-KF | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta | O1 |  | 6 | R3 KF-<era>-speaking/listening + plates R1-J27..J31 como image_1/3 (0 cr) |
| C-X01 | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | V3S | 5 | 30 |  |
| C-X02 | Andre fala C-L02 (8.81s) sobre o ombro desfocado da figura | V3A | 11 | 99 |  |
| C-X03 | LEGADO 1 - o que ele se tornou (imagem intima, sem rosto da figura) still + animacao curta | PRO + TURBO | 5 | 60 |  |
| C-X04 | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | V3S | 5 | 30 |  |
| C-X05 | Andre fala C-L04 (6.05s) OTS | V3A | 9 | 81 |  |
| C-X06 | LEGADO 2 - como falam dele hoje (sala de aula, livro, praca, debate; sem rosto) | PRO + TURBO | 5 | 60 |  |
| C-X07 | LEGADO 3 - repercussao dos atos (lugar/objeto/consequencia; sem rosto) | PRO + TURBO | 5 | 60 |  |
| C-X08 | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | V3S | 5 | 30 |  |
| K-REF | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) | PRO |  | 40 | R1-J21..J25 figurino abaixo do pescoco como referencia |
| K-KF | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta | O1 |  | 6 | R3 KF-<era>-speaking/listening + plates R1-J27..J31 como image_1/3 (0 cr) |
| K-X01 | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | V3S | 5 | 30 |  |
| K-X02 | Andre fala K-L02 (9.22s) sobre o ombro desfocado da figura | V3A | 12 | 108 |  |
| K-X03 | LEGADO 1 - o que ele se tornou (imagem intima, sem rosto da figura) still + animacao curta | PRO + TURBO | 5 | 60 |  |
| K-X04 | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | V3S | 5 | 30 |  |
| K-X05 | Andre fala K-L04 (6.67s) OTS | V3A | 9 | 81 |  |
| K-X06 | LEGADO 2 - como falam dele hoje (sala de aula, livro, praca, debate; sem rosto) | PRO + TURBO | 5 | 60 |  |
| K-X07 | LEGADO 3 - repercussao dos atos (lugar/objeto/consequencia; sem rosto) | PRO + TURBO | 5 | 60 |  |
| K-X08 | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | V3S | 5 | 30 |  |
| G-REF | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) | PRO |  | 40 | R1-J21..J25 figurino abaixo do pescoco como referencia |
| G-KF | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta | O1 |  | 6 | R3 KF-<era>-speaking/listening + plates R1-J27..J31 como image_1/3 (0 cr) |
| G-X01 | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | V3S | 5 | 30 | G-01-insert-galileo-v2_1 (insert mao/papel 10 s) como abertura alternativa |
| G-X02 | Andre fala G-L02 (9.38s) sobre o ombro desfocado da figura | V3A | 12 | 108 | G-02-andre-GL02_1 (108 cr, fala G-L02 frontal SEM a figura) - so se a triagem aceitar plano sem a figura |
| G-X03 | LEGADO 1 - o que ele se tornou (imagem intima, sem rosto da figura) still + animacao curta | PRO + TURBO | 5 | 60 |  |
| G-X04 | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | V3S | 5 | 30 | PILOT-01-galileo-listening-locked_1 como contraplano de escuta |
| G-X05 | Andre fala G-L04 (8.62s) OTS | V3A | 11 | 99 | PILOT-04-galileo-speech-native_1 (G-L04; palavras duvidosas p/ ADR) - idem |
| G-X06 | LEGADO 2 - como falam dele hoje (sala de aula, livro, praca, debate; sem rosto) | PRO + TURBO | 5 | 60 |  |
| G-X07 | LEGADO 3 - repercussao dos atos (lugar/objeto/consequencia; sem rosto) | PRO + TURBO | 5 | 60 |  |
| G-X08 | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | V3S | 5 | 30 | PILOT-02-galileo-gentle-turn_1 como fecho |
| N-REF | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) | PRO |  | 40 | R1-J21..J25 figurino abaixo do pescoco como referencia |
| N-KF | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta | O1 |  | 6 | R3 KF-<era>-speaking/listening + plates R1-J27..J31 como image_1/3 (0 cr) |
| N-X01 | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | V3S | 5 | 30 |  |
| N-X02 | Andre fala N-L02 (8.52s) sobre o ombro desfocado da figura | V3A | 11 | 99 |  |
| N-X03 | LEGADO 1 - o que ele se tornou (imagem intima, sem rosto da figura) still + animacao curta | PRO + TURBO | 5 | 60 |  |
| N-X04 | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | V3S | 7 | 42 |  |
| N-X05 | Andre fala N-L04 (3.1s) OTS | V3A | 6 | 54 |  |
| N-X06 | LEGADO 2 - como falam dele hoje (sala de aula, livro, praca, debate; sem rosto) | PRO + TURBO | 5 | 60 |  |
| N-X07 | LEGADO 3 - repercussao dos atos (lugar/objeto/consequencia; sem rosto) | PRO + TURBO | 5 | 60 |  |
| N-X08 | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | V3S | 5 | 30 |  |
| O-REF | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) | PRO |  | 40 | R1-J21..J25 figurino abaixo do pescoco como referencia |
| O-KF | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta | O1 |  | 6 | R3 KF-<era>-speaking/listening + plates R1-J27..J31 como image_1/3 (0 cr) |
| O-X01 | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | V3S | 5 | 30 |  |
| O-X02 | Andre fala O-L02 (11.86s) sobre o ombro desfocado da figura | V3A | 14 | 126 |  |
| O-X03 | LEGADO 1 - o que ele se tornou (imagem intima, sem rosto da figura) still + animacao curta | PRO + TURBO | 5 | 60 |  |
| O-X04 | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | V3S | 5 | 30 |  |
| O-X05 | Andre fala O-L04 (3.43s) OTS + >=4 s de silencio | V3A | 8 | 72 | PILOT-05-oppenheimer-speech-OL04_1 (O-L04 8 s com silencio) |
| O-X06 | LEGADO 2 - como falam dele hoje (sala de aula, livro, praca, debate; sem rosto) | PRO + TURBO | 5 | 60 |  |
| O-X07 | LEGADO 3 - repercussao dos atos (lugar/objeto/consequencia; sem rosto) | PRO + TURBO | 5 | 60 |  |
| O-X08 | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | V3S | 5 | 30 | PILOT-03-oppenheimer-expression_1 como fecho |
| OUT-KF | Keyframes o1 com Element (3 quadros x 2 tentativas) | O1 |  | 6 |  |
| OUT-01 | Andre fala OUT-L01 (9.72s) no presente | V3A | 12 | 108 |  |
| OUT-02 | As 5 figuras de costas desfocadas na mesa longa (payoff "estavam na mesa"); ref nova + video com Element | PRO + V3S | 5 | 50 |  |
| OUT-03 | LEGADO coletivo - eco das 5 historias hoje (sem rostos) | PRO + TURBO | 5 | 60 |  |
| OUT-04 | Mesa vazia, hold/fade sobre a madeira + creditos | TURBO | 5 | 40 | keyframe = R1-J32 plate presente (0 cr) |

## 8. Premissas
- 720p, como todos os vídeos já feitos; 1080p não tem preço observado.
- Um take por plano; retakes ficam na reserva de 30%. Keyframes o1 com 2 tentativas por quadro.
- Planos com o Andre em quadro usam kling-video-v3_0 + Element 323525046658711 (playbook). Legado e inserts sem rosto usam turbo sem Element.
- Legado = still PRO + 5 s de turbo; o conteúdo e as fontes vêm da História (Personagens Históricos).
- Preços são observados, não garantidos; antes de cada lote, reler o saldo e enviar com `--submit-only` (um ID por vez), como manda o envelope v3.
- Kling v3_0 aceita até 15 s (O-X02 = 14 s); se não aceitar, dividir o plano em 2 (custo/s igual).

## 9. Lacunas / riscos
- O pedido central (figura de costas em quadro com o Andre) não foi testado: o playbook só valida "ninguém mais no quadro". Antes de multiplicar por 5, sugiro um piloto (G-REF + G-KF + G-X02, ~154 cr) com OK do Andre.
- Bíblias de costas (Personagens) e triagem (Edição) ainda não saíram; a lista pode mudar.
- Legado: estátuas, retratos e fotos de época mostram rosto → precisa de regra explícita (de costas, fora de foco, objeto, lugar). Imagem sintética de Hiroshima/Nagasaki é sensível; a História/Direção pode preferir material de arquivo licenciado (fora dos créditos Kling).
- Anomalias sem explicação: 41 cr em 2 jobs o1; 70 cr em PILOT-01/02. Job G-01 de 80 cr com ID perdido continua aberto (não reenviar).
- Edição H (línguas históricas), dublagem ElevenLabs e sync ficam fora deste orçamento.
- Nada aqui aprova gasto; os portões de imagem final e filme final seguem false.
