# Preflight offline + auditoria do ledger — Claude, 2026-10-13

Somente leitura e crédito zero. Nenhum job enviado, nenhum arquivo existente alterado, exceto a correção de ferramenta descrita em 3.

## 1. Preflight de todos os pedidos existentes
Ferramenta: `docs/kling-manual/tools/kling_preflight.py` (snapshot who_am_i de 2026-10-09), `--allow-placeholders`.
Arquivos `07_generations/batches/*.json` (39 jobs), `request.json` e `request-gkf.template.json` da Fase A, e as duas specs `AB-MIN`. Saídas: `batches_*.txt` e `requests_*.txt` nesta pasta.

| Arquivo | Resultado |
|---|---|
| batches/GALILEO.json | 0 ERROR, 4 WARN (2 EXT_MISMATCH, 2 aspecto 5:2 em `first_image`) |
| batches/PILOT.json | 0 ERROR, 5 WARN (todos EXT_MISMATCH: `KF-*.jpg` é PNG) |
| batches/R2-references.json | 0 ERROR, 11 WARN (ver 3) |
| batches/R3-keyframes.json | 0 ERROR, 21 WARN (EXT_MISMATCH) |
| Fase A `request.json` | **1 ERROR**: 5 imagens para `gemini-3-pro-image`, que declara 2 slots (K1 do handoff de 2026-10-09 continua válido) |
| Fase A `request-gkf.template.json` | 0 ERROR, 7 WARN (placeholders permitidos) |
| AB-MIN v3_0 / Turbo | 0 ERROR, 0 WARN |

`requests/R3-session-01..08.json` não são pedidos: são registros `covered_by_real_photo`, `doNotGenerate: true`, custo 0.

Achados que valem correção na fonte:
- `02_references/table/R1-J26-table-anchor_2.png` é na verdade JPEG e alimenta cerca de 25 jobs. `02_references/keyframes/andre/KF-galileo-*.jpg`, `KF-oppenheimer-*.jpg`, `inserts/R2-J12-insert-galileo_1.jpg` e `originals/R3-present-speaking-o1-v2_1.jpg` são PNG. Todos já foram aceitos pela Kling no passado (as gerações existem), então o risco é baixo; ainda assim, renomear ou reexportar evita surpresa. Proposta, não executada: `file` para confirmar e copiar para o nome correto, sem apagar o original.
- GALILEO G-03/G-05: crop de olhos 2000x800 (0,40), no limite empírico de vídeo; aceito antes (R2 pad 5:2).

## 2. Ledger (`credit-ledger.csv`, 89 linhas)
Script: `ledger_overlap_audit.py`; proposta: `ledger-overlap-proposal.csv` (12 linhas sinalizadas). O ledger original não foi tocado.
- Soma das linhas: 2.351. Soma das 80 linhas `reconciled_from_balance_delta`: 2.180. Queda real de saldo coberta por essas janelas (7.741 → 5.813): **1.928**. Excesso: **252 créditos** contados em dobro por jobs concorrentes (janela de saldo compartilhada).
- Classes: 4 janelas idênticas (LR3-oppenheimer-speaking-o1-v2 = LR2-J02; LR2-J04 = LPILOT-02), 3 janelas "contidas" (os três polish de 20 em LELEMENT-andre-v2 de 180), 3 que contêm outras (LELEMENT 180, LR2-J01 41, LPILOT-01 70), 2 contidas (LR3-napoleon-listening 1; LR2-J03 40).
- Total real aproximado do projeto = 1.928 (janelas) + 51 (AB-MIN, `provider_reported`) = **1.979**, contra 2.351 no ledger.
- Continua sem registro o salto de saldo 5.813 → 31.621 entre 2026-10-09 e 2026-10-12 (recarga ou plano?). Decisão do produtor/Andre.
- Sugestão ao produtor: manter as linhas e adicionar coluna ou nota `shared_window` (ou dividir o custo entre os jobs concorrentes, marcando como estimativa); não somar `credits_consumed` de linhas reconciliadas sem essa correção. Jobs futuros devem sair um por vez (já é regra) e usar `creditsConsumed` do CLI.

## 3. Correção na ferramenta (único arquivo existente alterado)
`kling_preflight.py` tratava como ERROR toda imagem mais extrema que 2,5:1. Os jobs R2-J02..J06 (`image_to_image`, `gemini-3.1-flash-image`, entrada 4:1) geraram `4128x1024` com sucesso, então era falso positivo para ferramentas de imagem. Agora é WARN para `*_image`; segue ERROR para vídeo (4:1 foi rejeitado em vídeo). Novo teste adicionado; 16 testes passam. Hashes antes/depois no handoff.

## 4. O que ficou obsoleto
- Atualizar o skill kling-cli e o hash do registro: o Codex já fez (skill 0.2.1 com `omni_ref_video`).
- Teste A/B: executado em 2026-10-12 (27 + 24 créditos). Resta o MC-01 (45 créditos), bloqueado por Andre.
- Checklists por encontro: já existem em `tasks/plans/workflow-map-v1.md`; não dupliquei.
- Request-r2 da Fase A: o STATE diz "reassess need"; não preparei porque depende de Andre decidir se o teste D16 ainda é necessário.
