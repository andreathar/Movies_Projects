# 09 · Motion Control (`motion_control`)

Pega o movimento de um vídeo (ou de um movimento salvo na biblioteca) e aplica a uma **imagem de sujeito**. Nunca usado no filme [NÃO TESTADO].

## Declaração viva [LIVE]

| Modelo | Slots | Argumentos |
|---|---|---|
| `kling-video-v3_0` (padrão) | `image`*, `video` | `prompt`*, `motionId`, `motionDirection`*, `resolution` (720p padrão; 1080p), `keepOriginalSound` (true), **`elements`** |
| `kling-video-v2_6` | `image`*, `video` | idem, sem `elements` |

\* obrigatório. A imagem deve ter "uma pessoa ou animal claro". **Exatamente uma** fonte de movimento: o slot `video` **ou** `motionId` (nunca os dois, nunca nenhum). Preflight: `MOTION_SOURCE`.

`motionDirection` (obrigatório):
- `image_direction`: a orientação segue a **imagem**; só aceita movimentos de **3 a 10 s**.
- `motion_direction`: a orientação segue o **vídeo** de movimento.

`prompt` é obrigatório mas pode ser string vazia.

## Comando-modelo [NÃO TESTADO]

```bash
kling motion_control --model kling-video-v3_0 \
  --image 07_generations/originals/<keyframe-aceito>.png \
  --video ./movimento-referencia.mp4 \
  --motionDirection image_direction --resolution 720p --keepOriginalSound false \
  --elements '[{"id":"323525046658711","bindName":"Andre"}]' \
  --rationale "Transfer a short hand-press motion onto the approved keyframe" \
  --skill-name kling-cli --skill-version 0.2.0 --poll 300 \
  "<<<323525046658711>>> keep appearance, locked camera"
```

Com movimento salvo: troque `--video` por `--motionId <id>` (liste com `kling motion_library_list`: cada item traz `id`, nome, URL, capa, duração em ms e se tem áudio).

## O que dizem as fontes [OFICIAL via notas de lançamento, lidas em skill de terceiros]

- VIDEO 3.0 Motion Control (lançado 2026-03-04): saída de até **30 s**, consistência facial alta mesmo com oclusões (mão ou objeto na frente do rosto) e vários ângulos.
- A ligação facial por Element melhora a consistência. A orientação do personagem precisa **bater com a do vídeo** de movimento.
- Dica de entrada: imagem do sujeito nítida e vídeo de movimento com o corpo/rosto inteiro visível e iluminação limpa [INFERÊNCIA].

## Valor para o filme [INFERÊNCIA, a testar com autorização]

1. **Mão que pressiona e para (inserto abaixo do pescoço)**: gravar a própria mão como movimento e aplicar ao inserto da figura. Controle de gesto que `image_to_video` não dá. Sem rosto, então compatível com a regra de zero rosto completo. Use gravação própria (direitos limpos).
2. **Dublagem com lip-sync real do Andre (Edição H e outras)**: se o Andre grava a fala dele no idioma alvo e esse vídeo é a fonte de movimento, a boca do keyframe pode seguir a fala gravada. Com `keepOriginalSound true` a **voz original dele** vem junto. Hipótese: contorna o limite de idiomas do áudio nativo (`10`). **Não verificado**: o quanto a boca é transferida, a qualidade do som e a identidade. Teste curto (3–5 s, 720p) antes de qualquer promessa. Voz real é decisão da Andre (D13/D14).
3. Ensaio de movimento reaproveitável (`motion_library_list`) para repetir o mesmo gesto em vários takes.

## Custos [OFICIAL transcrito, conversão ×10 é INFERÊNCIA]

3.0: 0,9 U/s (720p) e 1,2 U/s (1080p) ⇒ ~9 e ~12 cr/s. Uma fonte de movimento de 5 s a 720p ≈ 45 cr. Confirmar no `creditsConsumed` e no ledger (os custos observados no projeto já divergiram do papel, ver `12`).

## Armadilhas

- `image_direction` com movimento fora de 3–10 s falha.
- Fonte com áudio: decida `keepOriginalSound`. Padrão **true** traz o áudio do vídeo para o resultado.
- Vídeo de movimento de terceiros pode ter direitos de uso. Prefira gravação própria ou biblioteca da conta.
- Reflexos: se o resultado mostrar o rosto de uma figura histórica por reflexo, descarte (regra do projeto).
