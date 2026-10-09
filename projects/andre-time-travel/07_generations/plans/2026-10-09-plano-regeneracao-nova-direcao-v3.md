# Plano de regeneração v3: legado mapeado (pós-triagem e decisões da Direção)

Projeto: andre-time-travel. Papel: producer, delegado de envio pago e ledgers (bot Produção e Créditos 9bfe6c7d).
Data: 2026-10-09, cerca de 13:10 (America/Sao_Paulo).
Status: **PROPOSTA. Nenhum job enviado, nada gerado.**
Base: v2 `2026-10-09-plano-regeneracao-nova-direcao-v2.md` e `2026-10-09-plano-regeneracao-takes-v2.csv` (preservadas). Detalhe por take: `2026-10-09-plano-regeneracao-takes-v3.csv`.
Imagens de legado: `03_bibles/legacy-images-v2-proposta.csv` (historiador; sha256 1bd497ff…). Os preços são os mesmos da v1 §3; saldo vivo 5.813 (12:37).

## Decisões da Direção aplicadas
1. **Nuca desfocada liberada**, desde que nenhuma parte do rosto ou do perfil apareça: sem orelha em perfil, bochecha, borda da barba, nariz, cílios ou reflexo. Muda prompts e critérios, não custo (ver §Piloto).
2. **Reaproveitamento dos pilotos com crop e X01 de 8 s**: aceitos. Os descontos da v2 viram definitivos.
3. **Fechos de César, Genghis e Napoleão** (C-X08, K-X08, N-X08) viram stills animados localmente a partir de KF-*-listening: **0 cr**.
4. **Legado**: 16 imagens LI-01 a LI-16 mapeadas para X03, X06 e X07 de cada capítulo e para OUT-03. São 11 geradas, 3 de arquivo a 0 cr (LI-07, LI-10, LI-14), LI-05 gerada ou de arquivo, e LI-15 pendente do Andre.

## Total por capítulo
| Capítulo | v2 | v3 normal | v3 pior caso | Faixa LI-05/LI-15 |
|---|---|---|---|---|
| ABERTURA | 175 | **175** | 215 | n/a |
| CESAR | 461 | **431** | 555 | n/a |
| GENGHIS | 470 | **380–440** | 564–624 | 380–440 |
| GALILEU | 341 | **281** | 441 | n/a |
| NAPOLEAO | 458 | **368** | 524 | n/a |
| OPPENHEIMER | 356 | **236–296** | 360–420 | 236–296 |
| FECHAMENTO | 258 | **258** | 298 | n/a |
| **TOTAL** | 2519 | **2129–2249** | **2957–3077** | |

Como ler a faixa:
- **Limite inferior**: LI-05 vem de arquivo licenciado e LI-15 segue a opção (b), (c) de arquivo ou (d), todas a 0 cr.
- **Limite superior**: as duas são geradas (60 cr cada).
- **Pior caso**: vídeo sem áudio a 14 cr/s; uma tentativa o1 a 41 por grupo de keyframes; segunda variante de REF; e um 2º clipe para LI-04 e LI-09, cujas descrições têm duas tomadas (+60 cada).

## Comparação com o saldo
- v3 normal: **2129–2249**. Sobram 3564–3684. Economia de 270–390 sobre a v2.
- Com reserva de 30% para refazer takes: 2768–2924. Sobram 2889–3045.
- Pior caso com reserva: 3844–4000. Sobram 1813–1969, acima dos 1.300 reservados para correções e Edição H.
- Galileu: 348 já gastos + 281 da v3 = 629, abaixo da parada de 810. O teto de 900 por capítulo é do envelope v3, então cada capítulo ainda precisa do seu escopo aprovado.

## O que mudou da v2 para a v3
| Take | Legado | v2 | v3 | Status | Motivo |
|---|---|---|---|---|---|
| C-X03 | LI-01 | 60 | 60 | MANTIDO | Gerado (historiador: fonte verificada no CSV do legado) |
| C-X06 | LI-02 | 60 | 60 | MANTIDO | Gerado (historiador: fonte verificada no CSV do legado) |
| C-X07 | LI-03 | 60 | 60 | MANTIDO | Gerado (historiador: fonte verificada no CSV do legado) |
| C-X08 |  | 30 | 0 | DESCONTADO | Direção 2026-10-09: fecho vira still animado localmente (0 cr), a partir de KF-*-listening (REAPROVEITAR) |
| K-X03 | LI-04 | 60 | 60 | MANTIDO | Gerado. A descrição tem 2 tomadas; o pior caso prevê um 2º clipe (+60) |
| K-X06 | LI-05 | 60 | 0–60 | FAIXA | 0 cr se arquivo licenciado (licença ainda não verificada: escultura de 2006) ou 60 cr se gerado (recomendado: silhueta genérica, não réplica; ou opção B, a crônica) |
| K-X07 | LI-06 | 60 | 60 | MANTIDO | Gerado (historiador: fonte verificada no CSV do legado) |
| K-X08 |  | 30 | 0 | DESCONTADO | Direção 2026-10-09: fecho vira still animado localmente (0 cr), a partir de KF-*-listening (REAPROVEITAR) |
| G-X03 | LI-07 | 60 | 0 | ARQUIVO | Imagem de arquivo (historiador); animação local (push/rack), 0 cr. Licença: Domínio público (Wikimedia Commons, File:Medicean_Stars.png, 1334x1964; verificado na página do arquivo). Crédito de cortesia: History of Science Collections, University of Oklahoma Li |
| G-X06 | LI-08 | 60 | 60 | MANTIDO | Gerado (historiador: fonte verificada no CSV do legado) |
| G-X07 | LI-09 | 60 | 60 | MANTIDO | Gerado. A descrição tem 2 tomadas; o pior caso prevê um 2º clipe (+60) |
| N-X03 | LI-10 | 60 | 0 | ARQUIVO | Imagem de arquivo (historiador); animação local (push/rack), 0 cr. Licença: Opção 1: CC BY 2.0. Atribuição obrigatória a Yale Law Library (via Flickr/Wikimedia Commons, File:Code_civil_des_Français_(1804).jpg, 2751x3714), com crédito, link da licença e indicaç |
| N-X06 | LI-11 | 60 | 60 | MANTIDO | Gerado (historiador: fonte verificada no CSV do legado) |
| N-X07 | LI-12 | 60 | 60 | MANTIDO | Gerado (historiador: fonte verificada no CSV do legado) |
| N-X08 |  | 30 | 0 | DESCONTADO | Direção 2026-10-09: fecho vira still animado localmente (0 cr), a partir de KF-*-listening (REAPROVEITAR) |
| O-X03 | LI-13 | 60 | 60 | MANTIDO | Gerado (historiador: fonte verificada no CSV do legado) |
| O-X06 | LI-14 | 60 | 0 | ARQUIVO | Imagem de arquivo (historiador); animação local (push/rack), 0 cr. Licença: Obra do governo federal dos EUA, sem copyright nos EUA (17 U.S.C. §105). Proteção fora dos EUA não é regida pelo §105 (House Report 94-1476): o producer precisa confirmar para as ediçõ |
| O-X07 | LI-15 | 60 | 0–60 | FAIXA | Decisão do Andre: (a) gerado 60 cr; (b) arquivo de 1945 0 cr (licença por imagem; risco alto de rosto); (c) memorial, 0 ou 60 cr (revisão cultural e de direitos); (d) só as datas, ou o beat vai para a audiência de 1954: 0 cr local |
| OUT-03 | LI-16 | 60 | 60 | MANTIDO | Gerado (historiador: fonte verificada no CSV do legado) |

## Imagens de arquivo: registro de atribuição
Ainda **não** vão para o `asset-registry.csv`: só entram quando o arquivo existir localmente, com sha256. Animação local, 0 cr. Conteúdo e verificação feitos pelo historiador (`legacy-images-v2-proposta.csv`).
- **LI-07 (G-X03)**: Domínio público (Wikimedia Commons, File:Medicean_Stars.png, 1334x1964; verificado na página do arquivo). Crédito de cortesia: History of Science Collections, University of Oklahoma Libraries.
- **LI-10 (N-X03)**: Opção 1: CC BY 2.0. Atribuição obrigatória a Yale Law Library (via Flickr/Wikimedia Commons, File:Code_civil_des_Français_(1804).jpg, 2751x3714), com crédito, link da licença e indicação de alterações (crop/animação). Opção 2: domínio público (scan Gallica, 636x762, baixa resolução).
- **LI-14 (O-X06)**: Obra do governo federal dos EUA, sem copyright nos EUA (17 U.S.C. §105). Proteção fora dos EUA não é regida pelo §105 (House Report 94-1476): o producer precisa confirmar para as edições internacionais. Fonte: energy.gov, PDF da ordem de 16/12/2022.
- **Ao baixar**: salvar a página da licença (snapshot) junto com o arquivo e registrar no asset-registry a URL, a licença, o autor, o crédito, o sha256 do arquivo e o do snapshot, mais as alterações (crop/animação).
  - LI-10 em CC BY 2.0 exige crédito visível nos créditos finais.
  - LI-14: confirmar o status fora dos EUA antes das edições internacionais.
  - LI-10: manter fora de foco ou fora do quadro a vinheta alegórica com rosto desenhado.
- LI-07 traz uma "cauda gerada opcional" (telescópio no quintal) que **não está no custo**: seriam +60 se aprovada.

## Pendências que movem a faixa
- **LI-05 (K-X06)**: Direção e producer decidem entre arquivo, gerado sem réplica ou opção B (crônica). O arquivo não tem licença verificada (escultura de 2006; liberdade de panorama na Mongólia não checada). A recomendação do historiador e minha é **gerar** (60 cr), com silhueta genérica vista por trás.
- **LI-15 (O-X07)**: decisão do Andre entre (a), (b), (c) e (d). Risco alto de rosto em (b) e (c). LI-16 (OUT-03) não depende dela, como foi proposto.
- **Tom de LI-12** (canavial): checagem da Direção (dignidade, sem correntes simbólicas).

## Piloto do Galileu: custo inalterado (161 normal / 261 pior caso)
Os itens, durações e preços são os da `2026-10-09-piloto-galileu-v2.md`. Com a decisão 1, os prompts **podem** trocar a frase "entire head, neck … OUTSIDE the frame" por:
> The back of his head may appear only from directly behind and strongly out of focus — hair and nape only; no ear in profile, no cheek, jaw, beard edge, nose, eyelashes or any part of the face, no profile, no reflection.

O critério de aceite fica assim: nuca permitida apenas desfocada e por trás. Qualquer quadro com traço de rosto ou de perfil reprova o take, na grade de todos os quadros. O modelo R3-oppenheimer-speaking-o1_1 passa a valer também para a nuca. Isso não muda o custo. O G-X01 do piloto continua com 5 s (o de 8 s vale para C, K e O).

## Lista completa
| Take | Legado | Descrição | Dur. (s) | v2 | v3 | Faixa | Pior caso | Status |
|---|---|---|---|---|---|---|---|---|
| IN-KF |  | Keyframes o1 com Element (3 quadros x 2 tentativas): mesa presente, Andre fala, match-cut |  | 3 | 3 |  | 43 | REDUZIDO |
| IN-01 |  | Mesa do presente, mao do Andre entra (insert sem rosto) | 5 | 60 | 60 |  | 60 | MANTIDO |
| IN-02 |  | Andre fala IN-L01 (5.83s) a mesa; cadeiras opostas com 5 silhuetas de costas desfocadas (a confirmar com Direcao) | 8 | 72 | 72 |  | 72 | MANTIDO |
| IN-03 |  | Match-cut pela mesa para Roma (sem rosto) | 5 | 40 | 40 |  | 40 | MANTIDO |
| C-REF |  | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) |  | 20 | 20 |  | 40 | REDUZIDO |
| C-KF |  | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta |  | 3 | 3 |  | 43 | REDUZIDO |
| C-X01 |  | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | 8 | 48 | 48 |  | 112 | AJUSTADO |
| C-X02 |  | Andre fala C-L02 (8.81s) sobre o ombro desfocado da figura | 11 | 99 | 99 |  | 99 | MANTIDO |
| C-X03 | LI-01 | LI-01: Calendário: a página de junho cai e revela JULY | 5 | 60 | 60 |  | 60 | MANTIDO |
| C-X04 |  | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | 5 | 0 | 0 |  | 0 | DESCONTADO |
| C-X05 |  | Andre fala C-L04 (6.05s) OTS | 9 | 81 | 81 |  | 81 | MANTIDO |
| C-X06 | LI-02 | LI-02: Dicionário de estudante: verbete 'Kaiser' em foco | 5 | 60 | 60 |  | 60 | MANTIDO |
| C-X07 | LI-03 | LI-03: Salão de pedra vazio; dobra de lã branca com borda púrpura | 5 | 60 | 60 |  | 60 | MANTIDO |
| C-X08 |  | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | 5 | 30 | 0 |  | 0 | DESCONTADO |
| K-REF |  | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) |  | 20 | 20 |  | 40 | REDUZIDO |
| K-KF |  | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta |  | 3 | 3 |  | 43 | REDUZIDO |
| K-X01 |  | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | 8 | 48 | 48 |  | 112 | AJUSTADO |
| K-X02 |  | Andre fala K-L02 (9.22s) sobre o ombro desfocado da figura | 12 | 108 | 108 |  | 108 | MANTIDO |
| K-X03 | LI-04 | LI-04: Vento na estepe, depois linha de tinta avançando num mapa antigo (2 tomadas) | 5 | 60 | 60 |  | 120 | MANTIDO |
| K-X04 |  | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | 5 | 0 | 0 |  | 0 | DESCONTADO |
| K-X05 |  | Andre fala K-L04 (6.67s) OTS | 9 | 81 | 81 |  | 81 | MANTIDO |
| K-X06 | LI-05 | LI-05: Monumento de bronze visto de longe por trás, desfocado (ou opção B: crônica fechada) | 5 | 60 | 60 | 0–60 | 60 | FAIXA |
| K-X07 | LI-06 | LI-06: Muros de adobe em ruínas, poeira num portão vazio | 5 | 60 | 60 |  | 60 | MANTIDO |
| K-X08 |  | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | 5 | 30 | 0 |  | 0 | DESCONTADO |
| G-REF |  | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) |  | 20 | 20 |  | 40 | REDUZIDO |
| G-KF |  | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta |  | 3 | 3 |  | 43 | REDUZIDO |
| G-X01 |  | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | 5 | 30 | 30 |  | 70 | MANTIDO |
| G-X02 |  | Andre fala G-L02 (9.38s) sobre o ombro desfocado da figura | 12 | 108 | 108 |  | 108 | MANTIDO |
| G-X03 | LI-07 | LI-07: ARQUIVO: página do Sidereus Nuncius (1610), luas de Júpiter | 5 | 60 | 0 |  | 0 | ARQUIVO |
| G-X04 |  | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | 5 | 0 | 0 |  | 0 | DESCONTADO |
| G-X05 |  | Andre fala G-L04 (8.62s) OTS | 11 | 0 | 0 |  | 0 | DESCONTADO |
| G-X06 | LI-08 | LI-08: Discurso impresso sobre um púlpito (João Paulo II, 1992), uma linha legível | 5 | 60 | 60 |  | 60 | MANTIDO |
| G-X07 | LI-09 | LI-09: Pêndulo em silêncio, depois bola de bronze no plano inclinado (2 tomadas) | 5 | 60 | 60 |  | 120 | MANTIDO |
| G-X08 |  | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | 5 | 0 | 0 |  | 0 | DESCONTADO |
| N-REF |  | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) |  | 20 | 20 |  | 40 | REDUZIDO |
| N-KF |  | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta |  | 3 | 3 |  | 43 | REDUZIDO |
| N-X01 |  | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | 5 | 30 | 30 |  | 70 | MANTIDO |
| N-X02 |  | Andre fala N-L02 (8.52s) sobre o ombro desfocado da figura | 11 | 99 | 99 |  | 99 | MANTIDO |
| N-X03 | LI-10 | LI-10: ARQUIVO: folha de rosto do Code civil des Français (1804) | 5 | 60 | 0 |  | 0 | ARQUIVO |
| N-X04 |  | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | 7 | 42 | 42 |  | 98 | MANTIDO |
| N-X05 |  | Andre fala N-L04 (3.1s) OTS | 6 | 54 | 54 |  | 54 | MANTIDO |
| N-X06 | LI-11 | LI-11: Salão com cúpula, cadeiras vazias, púlpito com microfone | 5 | 60 | 60 |  | 60 | MANTIDO |
| N-X07 | LI-12 | LI-12: Canavial ao entardecer, trilha de terra, sem pessoas | 5 | 60 | 60 |  | 60 | MANTIDO |
| N-X08 |  | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | 5 | 30 | 0 |  | 0 | DESCONTADO |
| O-REF |  | Biblia: figura de COSTAS, corpo/ombros/nuca, figurino R1-J2x (2 variantes p/ escolha) |  | 0 | 0 |  | 20 | DESCONTADO |
| O-KF |  | Keyframes OTS o1 + Element (3 quadros x 2 tentativas): estabelecimento, fala, escuta |  | 2 | 2 |  | 42 | REDUZIDO |
| O-X01 |  | Estabelecimento: figura de costas desfocada em 1o plano, Andre do outro lado ouve a pergunta L01 (off) | 8 | 48 | 48 |  | 112 | AJUSTADO |
| O-X02 |  | Andre fala O-L02 (11.86s) sobre o ombro desfocado da figura | 14 | 126 | 126 |  | 126 | MANTIDO |
| O-X03 | LI-13 | LI-13: Chapéu porkpie numa bancada de laboratório | 5 | 60 | 60 |  | 60 | MANTIDO |
| O-X04 |  | Figura de costas faz a pergunta L03 (leve movimento de ombro/cabeca, desfocada); Andre escuta ao fundo | 5 | 0 | 0 |  | 0 | DESCONTADO |
| O-X05 |  | Andre fala O-L04 (3.43s) OTS + >=4 s de silencio | 8 | 0 | 0 |  | 0 | DESCONTADO |
| O-X06 | LI-14 | LI-14: ARQUIVO: ordem do DOE de 16/12/2022 (1954 "be vacated") | 5 | 60 | 0 |  | 0 | ARQUIVO |
| O-X07 | LI-15 | LI-15: PENDENTE DO ANDRE: opções a/b/c/d | 5 | 60 | 60 | 0–60 | 60 | FAIXA |
| O-X08 |  | Fecho: figura imovel de costas, Andre em silencio; corte pela mesa | 5 | 0 | 0 |  | 0 | DESCONTADO |
| OUT-KF |  | Keyframes o1 com Element (3 quadros x 2 tentativas) |  | 0 | 0 |  | 0 | DESCONTADO |
| OUT-01 |  | Andre fala OUT-L01 (9.72s) no presente | 12 | 108 | 108 |  | 108 | MANTIDO |
| OUT-02 |  | As 5 figuras de costas desfocadas na mesa longa (payoff "estavam na mesa"); ref nova + video com Element | 5 | 50 | 50 |  | 90 | MANTIDO |
| OUT-03 | LI-16 | LI-16: Mesa D04 no presente com os 5 objetos-eco | 5 | 60 | 60 |  | 60 | MANTIDO |
| OUT-04 |  | Mesa vazia, hold/fade sobre a madeira + creditos | 5 | 40 | 40 |  | 40 | MANTIDO |

Premissas e lacunas das versões anteriores continuam valendo. Nada aqui aprova gasto: cada job precisa do OK explícito do Andre.
