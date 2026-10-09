# Checkpoint — retomada Galileu (2026-10-09, ~13:20 -03)

Papel: diretor/produtor (sessão Hermes). Releitura completa de: AGENTS.md, START_HERE.md, workspace.json, manifest, board, approvals, D01–D16, STATE.md, `08_edit/reviews/holistic-staging-v1/*` (REPORT, findings, DIRECTOR_HANDOFF, DIRECTOR_RESPONSE_REVIEW), `08_edit/reviews/2026-10-09-revisao-nova-direcao/`, `docs/status-report-2026-10-09.md`, propostas v2/v3 em `03_bibles/`, planos em `07_generations/plans/`, pacote `07_generations/requests/2026-10-09-galileo-pilot-v2-phase-a/`. Nenhum job submetido, nenhum original/prévia/arquivo de outro agente alterado. Saldo vivo consultado às 12:28 -03: **5.813** (não reconsultado aqui).

## 1. Direção criativa vigente

- **Problema a resolver (Andre):** as personalidades "estão à mesa com ele, mas nunca aparecem à mesa com ele". Galileu é a prova: a conversa só fecha quando se percebe **duas pessoas próximas, sentadas à mesma mesa**.
- **Resposta adotada:** cada figura aparece **sentada, de costas e desfocada** enquanto Andre fala (plano sobre o ombro); os olhos viram **reação curta (1,5–2 s, máx. 2 por capítulo) sempre depois de um beat de costas**; imagens de legado/repercussão intercaladas em tom íntimo. Regra de zero rosto (AGENTS.md) continua absoluta: nenhum traço de rosto ou perfil, nem reflexo, em nenhum quadro.
- **Invariantes mantidos:** identidade = fotos 2024 + Element 323525046658711 (D01/D11); figurino cinza risca de giz/camisa branca listrada (D02); mesa de carvalho J26-2 que viaja com Andre, anel + lasca (D04); Andre à esquerda olhando para a direita da câmera (D09); roteiro v2 canônico (D07, APR-screenplay-v2); voz Kling = guia, dublagem depois (D14); `voiceTests/storyboard/paidBatch/finalPicture = false`.
- **Status de Galileu:** `galileo-en-preview-v1.mp4` é **candidata** (42 s, decodifica, −16,2 LUFS). Não é aceite de encenação. Os 9 takes e 7 slots mapeados permanecem como `accepted_pending_full_playback` (revisão por grades, sem reprodução integral).

## 2. Fontes canônicas (o que vale) e o que é derivado/proposta

| Tema | Canônico | Derivado / proposta (não edita o canônico) |
|---|---|---|
| Regras e papéis | `AGENTS.md`, `workspace.json`, `agents/registry.json`, `skills/andre-time-travel/SKILL.md` | `docs/REPEATABLE_WORKFLOW.md`, `docs/LOCAL_AGENT_HANDOFF.md` |
| Estado e tarefas | `manifest.json`, `tasks/board.json`, `00_brief/approvals.json`, `00_brief/decisions/D01–D16`, `memory/STATE.md` + `session-log.json` | `docs/status-report-2026-10-09.md` (foto de 12:20), `docs/budget-and-envelope-resume-v3.md` (previsão, não teto) |
| Diálogo | `01_script/script-en.md` + `01_script/dialogue-lines.csv` | bíblias de cena v1 §3 (falas antigas — F05), `*-v3-proposta.md` (dialogue-sound) |
| Continuidade/geometria | `03_bibles/table-and-continuity.md` (v1), `continuity-matrix.csv`, `character-andre.md` | `table-and-continuity-v2-proposta.md`, `continuity-matrix-v2-proposta.csv`, `scene-bibles/*-v2-proposta.md` (historiador), `legacy-images-v2-proposta.*` |
| Planos e custos | `credit-ledger.csv`, `asset-registry.csv`, escopos em `approvals.json` | `07_generations/plans/*` (v1→v3), `requests/2026-10-09-galileo-pilot-v2-phase-a/` |
| Montagem | `08_edit/timelines/galileo-en-v1.json`, `08_edit/picture-lock/galileo-en-preview-v1.mp4`, `08_edit/reviews/*` | `holistic-staging-v1/` (parecer + snapshots), `2026-10-09-revisao-nova-direcao/` (triagem) |

Pastas `08_edit/timelines`, `08_edit/normalized`, `04_audio/stems/dialogue` e o reaproveitamento dos pilotos fazem parte da estrutura e do escopo original (confirmado por Codex). Nada será movido, renomeado ou apagado.

## 3. Propostas que precisam ser integradas

| Proposta | Autor | Ação proposta | Para onde |
|---|---|---|---|
| Geometria mesa/assentos/câmera (§3A da v2) | continuity | **Adotar como geometria de trabalho** do piloto; vira canônica só após G-KF-M aceito | D17 (nova decisão) + `table-and-continuity.md` v2 |
| Gramática de costas BV-O/BV-R/BV-W e regra dos olhos | continuity + director | Adotar BV-O (cabeça fora) já; BV-W/nuca condicionados a D18 | D17/D18 |
| Bíblias de cena v2 (historiador) + v3 (dialogue) ×5 | historian, dialogue-sound | Integrar v3 de G/C/K/N na v1 (corrige F05: falas antigas); Oppenheimer sem v3 — pendente | `scene-bibles/*.md` (uma revisão, com hash) |
| Triagem SERVE/REAPROVEITAR/REFAZER (234 linhas) | editor+qc | Usar como fonte do plano de takes; pilotos de escuta PILOT-01/02 = REAPROVEITAR fora da geometria de Galileu | `plano-regeneracao-v3` já consome |
| Piloto Galileu v2 (A/B/C) e pacote Fase A | producer-bot | **Fase A autorizada (D16, 23 cr) mas com 1 incompatibilidade (ver §4.2)** | `request.json` r2 |
| Achados F01–F08 (holístico) | Codex | F01/F02 → fases A–C; F03 → timeline v2 (0 cr); F04 → D17; F05 → bíblias; F06 → matriz; F07 → esta sessão reancorada; F08 → entrega | listado em §6 |
| Campos `preview*` / status `accepted_pending_full_playback` (meus) | director | **Formalizar** vocabulário de takes e validação; não alimentar contagem de aprovação | `scripts/manage.py` + teste |

## 4. Decisões pendentes (só Andre, salvo indicação)

1. **Confirmar D16 diretamente neste chat.** O registro diz "relayed via Grok Bot". Não executo gasto com autorização retransmitida.
2. **D16-r2 — correção obrigatória antes de submeter o G-REF.** Evidência: `logs/kling-discovery-resume/who_am_i.json` declara para `gemini-3-pro-image` apenas `image_1` (obrigatória) e `image_2`; o `request.json` passa **5 imagens**. O `image_to_image --help` ao vivo (`logs/kling-discovery-checkpoint/`) exige "inputs as declared per model". Todos os 21 jobs anteriores desse modelo usaram ≤2 imagens. Opções: (a) manter `gemini-3-pro-image` com `image_1` = mesa J26-2 e `image_2` = J23 `_belowneck`, descrevendo punho/manga, luz de Arcetri e câmera no prompt — custo 20, teto 23 inalterado (**recomendo**); (b) trocar para `kling-image-o1` (10 inputs declarados, 1 cr observado, anomalia 41 já vista) — mudança de modelo, exige nova revisão. A regra da D16 diz que edição de conteúdo exige nova revisão: por isso é decisão, não ajuste silencioso.
3. **D18 — nuca desfocada.** Fase A fica com cabeça fora do quadro (texto aprovado). Liberar "nuca só por trás, desfocada, sem orelha/bochecha/barba/perfil/reflexo" para as fases B/C? O quadro `R3-oppenheimer-speaking-o1_1.jpg` já demonstra essa leitura (nuca e ombro desfocados, zero traço facial). Recomendo **sim**, com reprovação de take ao primeiro quadro com traço de perfil.
4. **D17 — geometria canônica** (mesa ~120×75×75 cm, lados longos, câmera atrás-direita da figura, 50 mm, altura dos olhos sentado). Recomendo canonizar quando o G-KF-M for aceito, não antes.
5. **Fases B (G-X01, 30 cr) e C (G-X02, 108 cr):** aprovação própria, após aceite da Fase A.
6. **Regra dos olhos** (1,5–2 s após beat de costas, máx. 2/capítulo): já aplicada nas propostas; precisa de registro de decisão (D19) para entrar nas bíblias.
7. **Dono único de manifest/board/approvals/ledger:** proponho esta sessão (produtor). Demais agentes entregam em caminhos próprios + handoff. Sem isso, F06 se repete.
8. **Legado (LI-05, LI-12, LI-15) e outro "cadeira dos séculos":** não bloqueiam Galileu; decidir depois do piloto.

## 5. Galileu — geometria, demonstração, fala/escuta, reação

**Geometria de trabalho (proposta v2 §3A, adotada para o piloto):** mesa J26-2, Galileu no lado longo próximo da câmera, Andre no lado longo oposto; conversa atravessa os ~75 cm; anel entre os dois, lasca no canto próximo à câmera; câmera atrás e à direita de Galileu, altura dos olhos sentado, 50 mm, travada; luz fria de Arcetri entrando da esquerda; Andre centro-esquerda em foco olhando para a direita da câmera (D09); ombro/manga de Galileu no terço direito, 25–35 % da largura, fortemente desfocados, parados salvo respiração.

**Demonstração do plano sobre o ombro:** (1) modelo já existente, 0 cr — `07_generations/originals/R3-oppenheimer-speaking-o1_1.jpg` (nuca e ombro em primeiro plano desfocados, Andre em foco; serve como guia de câmera/escala, não de pessoa); (2) prova paga — Fase A: G-REF (placa da disposição com cadeira vazia) → G-KF-M (Andre na cadeira, fala) → G-KF-L (escuta, edição mínima). Aceite: zero cabeça/perfil/sombra de rosto em zoom 100 %; mesmo tampo contínuo; semelhança igual aos KF R3.

**Compatibilidade fala/escuta dos clipes existentes (evidência: quadros do holístico):**

| Clipe | Geometria | Uso em Galileu |
|---|---|---|
| G-02 (G-L02, 12 s) e PILOT-04 (G-L04, 8 s) | Andre de frente, antebraços na mesa, janela/estante atrás — câmera no lugar de Galileu | **Compatíveis entre si**: contraplano frontal da fala (crop 1,08× remove marca) |
| PILOT-01 (escuta travada), PILOT-02 (virada) | Mesa ao lado/atrás de Andre, pedra escura, sem apoio dos braços | **Não é a mesma mesa/assento** (F01). Saem de G-04/G-07 quando G-X01 existir; continuam REAPROVEITAR em outro contexto |
| G-01-v2 insert, G-03/G-05 olhos | mão/manga e faixas de olhos | Mantidos; olhos só após beat de costas e ligados à palavra certa |

**Correção do momento da reação (F03), 0 cr, timeline v2 proposta (42 s):** 0–4 insert G-01 (G-L01 off em 0,5) · 4–16 fala G-L02 (G-X02 quando existir; até lá G-02 frontal) · 16–18 olhos A (G-03, 2 s, "harder and more interesting") · 18–22,8 beat de costas/escuta (G-X01; placeholder: insert) com G-L03 off em 20 · 22,8–30,8 PILOT-04 G-L04 · **30,8–33,5 olhos B (G-05) sobre "silencing a man does not settle a question"** · 33,5–38,5 costas/insert (silêncio) · 38,5–42 Andre em respeito (cauda de G-X01) → corte na mesa. Nada é acelerado; áudio-guia inalterado.

## 6. Próximo passo concreto

Andre responde os itens **1 e 2** de §4. Com "ok": executo a Fase A, um job por vez (`kling_batch.py --submit-only` → `--resume`), saldo antes/depois por job, parada em qualquer delta acima do estimado (>20 no G-REF, >1 em o1), teto 23. Entrego caminhos, sha256, deltas e grades de aceite; **sem** fases B/C.

## 7. Mudanças necessárias — arquivos e responsáveis

| # | Arquivo | Responsável | Mudança | Motivo |
|---|---|---|---|---|
| 1 | `07_generations/requests/2026-10-09-galileo-pilot-v2-phase-a/request.json` → `request-r2.json` (novo; r1 preservado) | producer (esta sessão) | 2 inputs declarados; prompt descreve manga/luz/câmera; `auth` = D16 | incompatível com `who_am_i` (§4.2) |
| 2 | `00_brief/decisions/D16-galileo-pilot-v2-phase-a.json` | producer, após Andre | anexar `confirmedBy: Andre (chat direto)` + hash de `request-r2.json` | autorização retransmitida |
| 3 | `00_brief/decisions/D17-geometria.json`, `D18-nuca.json`, `D19-regra-olhos.json` (novos) | producer, após Andre | registrar decisões de §4 | bíblias e prompts citam decisão, não proposta |
| 4 | `03_bibles/scene-bibles/galileo.md` (+ caesar, genghis, napoleon) | dialogue-sound | §3 só com IDs de fala + hash do CSV; incorporar v3 | F05 |
| 5 | `03_bibles/continuity-matrix.csv` | continuity | linhas de geometria/costas/olhos de Galileu a partir da v2-proposta | F06 |
| 6 | `08_edit/timelines/galileo-en-v2.json` (novo) + `picture-lock/galileo-en-preview-v2.mp4` | editor | ordem de §5; v1 preservada | F03; placeholders até fases B/C |
| 7 | `scripts/manage.py` + `tests/test_manage.py` | producer | validar `takes[].status ∈ {generated, accepted_pending_full_playback, accepted, rejected}` e `chapters[].preview*`; `accepted_pending_*` não conta como aceite | formalizar campos já usados |
| 8 | `memory/STATE.md` (3 linhas no topo) + `session-log.json` | producer | apontar para este checkpoint | F07 / retomada |
| 9 | `agents/handoffs/2026-10-09-director-checkpoint-galileo.json` (novo) | producer | hashes-base e escopo desta releitura | contrato de edição local |

Fora do escopo desta etapa: qualquer geração, fases B/C, capítulos C/K/N/O, dublagem, ElevenLabs, commit.
