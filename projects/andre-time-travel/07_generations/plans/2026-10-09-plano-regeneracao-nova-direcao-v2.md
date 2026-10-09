# Plano de regeneração v2, pós-triagem: nova direção (personalidades de costas + legado)

Projeto: andre-time-travel. Papel: producer, delegado de envio pago e ledgers (bot Produção e Créditos 9bfe6c7d).
Data: 2026-10-09, cerca de 13:00 (America/Sao_Paulo).
Status: **PROPOSTA. Nenhum job enviado, nada gerado.**
Substitui para planejamento a v1 `2026-10-09-plano-regeneracao-nova-direcao.md` (preservada). Detalhe por take em `2026-10-09-plano-regeneracao-takes-v2.csv`; piloto em `2026-10-09-piloto-galileu-v2.md`.

## Base
- **Triagem da Edição**: `08_edit/reviews/2026-10-09-revisao-nova-direcao/review.csv` e `review.md` (sha256 15e0d84b… e a36b8611…).
  - Únicos: 45 SERVE, 100 REAPROVEITAR, 9 REFAZER (234 linhas com cópias).
  - Achados que importam aqui: nenhum vídeo serve como está; existem 0 planos de costas em vídeo e 0 imagens de legado.
  - O único quadro já na gramática nova é `07_generations/originals/R3-oppenheimer-speaking-o1_1.jpg` (4c26297a…).
  - Marca d'água KlingAI em G-01 e G-02, removível com crop de ~1,08x (local, 0 cr).
- **Decisões da Direção para o piloto**: G-X01 com 5 s; fala G-L02; ombro parado, só com respiração mínima; figurino J23 mais a manga R2-J12; mesa de 120×75×75 cm ainda como proposta.
- **Saldo vivo**: 5.813 (`kling account`, 12:37). Preços iguais aos da v1 §3: O1 1 cr; PRO 20 cr; TURBO 8 cr/s; v3_0 com áudio 9 cr/s; v3_0 sem áudio 6 cr/s (pior caso 14 cr/s).

## Total por capítulo
| Capítulo | v1 | v2 | Pior caso v2 | Takes pagos v2 | Takes descontados |
|---|---|---|---|---|---|
| ABERTURA | 178 | **175** | 215 | 4 | 0 |
| CESAR | 496 | **461** | 625 | 9 | 1 |
| GENGHIS | 505 | **470** | 634 | 9 | 1 |
| GALILEU | 523 | **341** | 441 | 7 | 3 |
| NAPOLEAO | 481 | **458** | 654 | 10 | 0 |
| OPPENHEIMER | 514 | **356** | 480 | 6 | 4 |
| FECHAMENTO | 264 | **258** | 298 | 4 | 1 |
| **TOTAL** | 2961 | **2519** | 3347 | 49 | 10 |

Pior caso: vídeo sem áudio a 14 cr/s; uma tentativa o1 a 41 por grupo de keyframes; a segunda variante de REF volta, onde foi cortada; G-REF volta a ter 2 imagens.

## Comparação com o saldo
- Plano v2: **2519**. Sobram 3294. Economia de 442 sobre a v1.
- v2 com reserva de 30% para refazer takes (756): **3275**. Sobram 2538.
- Pior caso com reserva (1004): **4351**. Sobram 1462, ainda acima dos 1.300 reservados para correções e Edição H.
- Opção B, com o legado animado localmente (0 cr), corta mais 640 e leva o plano a 1879.
- O escopo do Galileu (teto 900, parada em 810) tem 348 gastos. A v2 do capítulo (341) leva a 689, abaixo da parada.

## O que foi descontado e por quê
| Take | v1 | v2 | Status | Motivo (triagem) |
|---|---|---|---|---|
| IN-KF | 6 | 3 | REDUZIDO | R3-present-speaking-o1_1 (SERVE) como base; só a variação com as silhuetas |
| C-REF | 40 | 20 | REDUZIDO | Figurino abaixo do pescoço SERVE (J21/J24/J25; J22 REAPROVEITAR) + modelo de enquadramento R3-oppenheimer-speaking-o1_1 -> 1 variante |
| C-KF | 6 | 3 | REDUZIDO | Modelo de enquadramento R3-oppenheimer-speaking-o1_1 (SERVE): 3 tentativas em vez de 6 |
| C-X01 | 30 | 48 | AJUSTADO | Plano de costas estendido para 8 s para cobrir L01 e L03 (2 usos, dentro do limite de 1-2 usos da triagem) |
| C-X04 | 30 | 0 | DESCONTADO | Coberto pela 2a metade de C-X01 (mesma disposição; Andre escuta) |
| K-REF | 40 | 20 | REDUZIDO | Figurino abaixo do pescoço SERVE (J21/J24/J25; J22 REAPROVEITAR) + modelo de enquadramento R3-oppenheimer-speaking-o1_1 -> 1 variante |
| K-KF | 6 | 3 | REDUZIDO | Modelo de enquadramento R3-oppenheimer-speaking-o1_1 (SERVE): 3 tentativas em vez de 6 |
| K-X01 | 30 | 48 | AJUSTADO | Plano de costas estendido para 8 s para cobrir L01 e L03 (2 usos, dentro do limite de 1-2 usos da triagem) |
| K-X04 | 30 | 0 | DESCONTADO | Coberto pela 2a metade de K-X01 (mesma disposição; Andre escuta) |
| G-REF | 40 | 20 | REDUZIDO | Piloto: J23 _belowneck (SERVE) + manga R2-J12 + R3-oppenheimer-speaking-o1_1 (SERVE, modelo de enquadramento) -> 1 variante basta |
| G-KF | 6 | 3 | REDUZIDO | Enquadramento já resolvido por R3-oppenheimer-speaking-o1_1 (SERVE): mestre 2 tentativas + escuta 1 |
| G-X04 | 30 | 0 | DESCONTADO | PILOT-01 REAPROVEITAR (crop ~1,2x, escuta) + trecho de G-X01; L03 tem 2,83 s |
| G-X05 | 99 | 0 | DESCONTADO | PILOT-04 REAPROVEITAR: mantém a fala G-L04 frontal; trecho duvidoso coberto por G-X01/plano de costas |
| G-X08 | 30 | 0 | DESCONTADO | PILOT-02 REAPROVEITAR: corte no giro (~1,0 s) para o plano de costas; mesmo crop do PILOT-01 |
| N-REF | 40 | 20 | REDUZIDO | Figurino abaixo do pescoço SERVE (J21/J24/J25; J22 REAPROVEITAR) + modelo de enquadramento R3-oppenheimer-speaking-o1_1 -> 1 variante |
| N-KF | 6 | 3 | REDUZIDO | Modelo de enquadramento R3-oppenheimer-speaking-o1_1 (SERVE): 3 tentativas em vez de 6 |
| O-REF | 40 | 0 | DESCONTADO | R3-oppenheimer-speaking-o1_1 SERVE: já mostra nuca/ombro de Oppenheimer desfocado; vira frame inicial (confirmar silhueta e grade) |
| O-KF | 6 | 2 | REDUZIDO | Mestre de fala = R3-oppenheimer-speaking-o1_1 (SERVE); só a escuta derivada (2 tentativas) |
| O-X01 | 30 | 48 | AJUSTADO | Plano de costas estendido para 8 s para cobrir L01 e L03 (2 usos, dentro do limite de 1-2 usos da triagem) |
| O-X04 | 30 | 0 | DESCONTADO | Coberto pela 2a metade de O-X01 (mesma disposição; Andre escuta) |
| O-X05 | 72 | 0 | DESCONTADO | PILOT-05 REAPROVEITAR (O-L04 com silêncio): intercalar com OTS de O-X02 ou recompor ~1,2x |
| O-X08 | 30 | 0 | DESCONTADO | PILOT-03 REAPROVEITAR: reação do Andre, subir sombras/grade |
| OUT-KF | 6 | 0 | DESCONTADO | KF R3-present-speaking-o1_1 e R3-present-listening-o1_1 SERVE (presente, D02) |

**Pós-produção local, 0 créditos, a fazer na montagem:**
- crop de ~1,08x em G-01 e G-02 (marca d'água);
- crop de ~1,2x em PILOT-01, PILOT-02 e PILOT-05 (mesa vazia);
- grade em PILOT-03;
- G-05 usado até 2,8 s;
- olhos: 1 beat de 1,5 a 2 s por capítulo, só depois do plano de costas;
- G-01 com 1 ou 2 usos.

Nada disso entra no custo, mas tudo precisa da Edição.

**O que não teve desconto e por quê:**
- Planos de fala sobre o ombro (X02/X05) de César, Genghis e Napoleão: só existem keyframes estáticos (KF-*-speaking, REAPROVEITAR como base de contraplano), não vídeo de fala.
- Legado (X03/X06/X07 em todos os capítulos): 0 imagens existentes.
- Planos de costas (X01): 0 existentes.
- N-X04 (N-L03, a virada do roteiro): mantido separado.
- Fechos de C, K e N: só stills; ficam a descontar se a Direção aceitar still animado localmente.

**Marca d'água**: os vídeos novos também podem vir com marca. Por isso o critério de aceite exige o conteúdo essencial dentro dos 92% centrais do quadro, para o crop de 1,08x não cortar ombro nem rosto.

## Ainda a descontar ou decidir
- **REAPROVEITAR condicionado a gosto**: G-02 como contraplano frontal (já previsto na montagem); fechos de C, K e N a partir de KF-*-listening (stills); R3-galileo-speaking_1 como plano geral com espaço para o Galileu de costas (precisaria de geração para inserir a figura, então não gera desconto).
- O enquadramento modelo R3-oppenheimer-speaking-o1_1 mostra **nuca e ombro**. A especificação do piloto mantém a cabeça histórica fora do quadro, que é mais restritivo. Se a Direção liberar nuca desfocada, os prompts ficam mais simples. Não muda o custo.
- Inconsistências de olhos (dois tipos de César, Genghis R1-J14 mais velho, R1-J20 com pálpebra cortada) e referências de figurino com queixo (R2-wardrobe-*: cortar o topo antes de entrar em prompt): a Edição e Personagens tratam; 0 cr.

## Lista completa
| Take | Descrição | Modelo | Dur. (s) | v1 | v2 | Pior caso | Status |
|---|---|---|---|---|---|---|---|
| IN-KF | Keyframes o1 com Element (3 quadros x 2 tentativas): mesa presente, Andre fala, match-cut | O1 |  | 6 | 3 | 43 | REDUZIDO |
| IN-01 | Mesa do presente, mao do Andre entra (insert sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| IN-02 | Andre fala IN-L01 (5.83s) a mesa; cadeiras opostas com 5 silhuetas de costas desfocadas (a confirmar com Direcao) | V3A | 8 | 72 | 72 | 72 | MANTIDO |
| IN-03 | Match-cut pela mesa para Roma (sem rosto) | TURBO | 5 | 40 | 40 | 40 | MANTIDO |
| C-REF | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) | PRO |  | 40 | 20 | 40 | REDUZIDO |
| C-KF | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta | O1 |  | 6 | 3 | 43 | REDUZIDO |
| C-X01 | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | V3S | 8 | 30 | 48 | 112 | AJUSTADO |
| C-X02 | Andre fala C-L02 (8.81s) sobre o ombro desfocado da figura | V3A | 11 | 99 | 99 | 99 | MANTIDO |
| C-X03 | LEGADO 1 - o que ele se tornou (imagem intima, sem rosto da figura) still + animacao curta | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| C-X04 | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | V3S | 5 | 30 | 0 | 0 | DESCONTADO |
| C-X05 | Andre fala C-L04 (6.05s) OTS | V3A | 9 | 81 | 81 | 81 | MANTIDO |
| C-X06 | LEGADO 2 - como falam dele hoje (sala de aula, livro, praca, debate; sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| C-X07 | LEGADO 3 - repercussao dos atos (lugar/objeto/consequencia; sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| C-X08 | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | V3S | 5 | 30 | 30 | 70 | MANTIDO |
| K-REF | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) | PRO |  | 40 | 20 | 40 | REDUZIDO |
| K-KF | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta | O1 |  | 6 | 3 | 43 | REDUZIDO |
| K-X01 | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | V3S | 8 | 30 | 48 | 112 | AJUSTADO |
| K-X02 | Andre fala K-L02 (9.22s) sobre o ombro desfocado da figura | V3A | 12 | 108 | 108 | 108 | MANTIDO |
| K-X03 | LEGADO 1 - o que ele se tornou (imagem intima, sem rosto da figura) still + animacao curta | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| K-X04 | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | V3S | 5 | 30 | 0 | 0 | DESCONTADO |
| K-X05 | Andre fala K-L04 (6.67s) OTS | V3A | 9 | 81 | 81 | 81 | MANTIDO |
| K-X06 | LEGADO 2 - como falam dele hoje (sala de aula, livro, praca, debate; sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| K-X07 | LEGADO 3 - repercussao dos atos (lugar/objeto/consequencia; sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| K-X08 | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | V3S | 5 | 30 | 30 | 70 | MANTIDO |
| G-REF | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) | PRO |  | 40 | 20 | 40 | REDUZIDO |
| G-KF | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta | O1 |  | 6 | 3 | 43 | REDUZIDO |
| G-X01 | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | V3S | 5 | 30 | 30 | 70 | MANTIDO |
| G-X02 | Andre fala G-L02 (9.38s) sobre o ombro desfocado da figura | V3A | 12 | 108 | 108 | 108 | MANTIDO |
| G-X03 | LEGADO 1 - o que ele se tornou (imagem intima, sem rosto da figura) still + animacao curta | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| G-X04 | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | V3S | 5 | 30 | 0 | 0 | DESCONTADO |
| G-X05 | Andre fala G-L04 (8.62s) OTS | V3A | 11 | 99 | 0 | 0 | DESCONTADO |
| G-X06 | LEGADO 2 - como falam dele hoje (sala de aula, livro, praca, debate; sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| G-X07 | LEGADO 3 - repercussao dos atos (lugar/objeto/consequencia; sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| G-X08 | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | V3S | 5 | 30 | 0 | 0 | DESCONTADO |
| N-REF | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) | PRO |  | 40 | 20 | 40 | REDUZIDO |
| N-KF | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta | O1 |  | 6 | 3 | 43 | REDUZIDO |
| N-X01 | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | V3S | 5 | 30 | 30 | 70 | MANTIDO |
| N-X02 | Andre fala N-L02 (8.52s) sobre o ombro desfocado da figura | V3A | 11 | 99 | 99 | 99 | MANTIDO |
| N-X03 | LEGADO 1 - o que ele se tornou (imagem intima, sem rosto da figura) still + animacao curta | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| N-X04 | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | V3S | 7 | 42 | 42 | 98 | MANTIDO |
| N-X05 | Andre fala N-L04 (3.1s) OTS | V3A | 6 | 54 | 54 | 54 | MANTIDO |
| N-X06 | LEGADO 2 - como falam dele hoje (sala de aula, livro, praca, debate; sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| N-X07 | LEGADO 3 - repercussao dos atos (lugar/objeto/consequencia; sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| N-X08 | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | V3S | 5 | 30 | 30 | 70 | MANTIDO |
| O-REF | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) | PRO |  | 40 | 0 | 20 | DESCONTADO |
| O-KF | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta | O1 |  | 6 | 2 | 42 | REDUZIDO |
| O-X01 | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | V3S | 8 | 30 | 48 | 112 | AJUSTADO |
| O-X02 | Andre fala O-L02 (11.86s) sobre o ombro desfocado da figura | V3A | 14 | 126 | 126 | 126 | MANTIDO |
| O-X03 | LEGADO 1 - o que ele se tornou (imagem intima, sem rosto da figura) still + animacao curta | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| O-X04 | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | V3S | 5 | 30 | 0 | 0 | DESCONTADO |
| O-X05 | Andre fala O-L04 (3.43s) OTS + >=4 s de silencio | V3A | 8 | 72 | 0 | 0 | DESCONTADO |
| O-X06 | LEGADO 2 - como falam dele hoje (sala de aula, livro, praca, debate; sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| O-X07 | LEGADO 3 - repercussao dos atos (lugar/objeto/consequencia; sem rosto) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| O-X08 | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | V3S | 5 | 30 | 0 | 0 | DESCONTADO |
| OUT-KF | Keyframes o1 com Element (3 quadros x 2 tentativas) | O1 |  | 6 | 0 | 0 | DESCONTADO |
| OUT-01 | Andre fala OUT-L01 (9.72s) no presente | V3A | 12 | 108 | 108 | 108 | MANTIDO |
| OUT-02 | As 5 figuras de costas desfocadas na mesa longa (payoff "estavam na mesa"); ref nova + video com Element | PRO + V3S | 5 | 50 | 50 | 90 | MANTIDO |
| OUT-03 | LEGADO coletivo - eco das 5 historias hoje (sem rostos) | PRO + TURBO | 5 | 60 | 60 | 60 | MANTIDO |
| OUT-04 | Mesa vazia, hold/fade sobre a madeira + creditos | TURBO | 5 | 40 | 40 | 40 | MANTIDO |

Premissas e lacunas da v1 (§8 e §9) continuam valendo, salvo o que está acima. Nada aqui aprova gasto; cada job precisa do OK explícito do Andre.
