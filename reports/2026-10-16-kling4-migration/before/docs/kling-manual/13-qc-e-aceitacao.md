# 13 · QC e aceitação de um take

Princípio do projeto: arquivo gerado **não** é take aceito. Nada abaixo substitui o gate humano (reprodução em velocidade normal, aprovação de semelhança e de voz do Andre, revisão de idioma). Protocolo-base: `prompt-playbook-kling.md` §4 [PROJETO]. Os comandos são ffmpeg/ffprobe padrão; a máquina tem ambos (`/usr/bin`) [LIVE].

## 0. Baixar a tempo e fixar

URLs de resultado expiram em **24 h** [OFICIAL]. Baixe, calcule `sha256sum`, grave em `07_generations/originals/` com nome novo (nunca sobrescrever) e só então registre no ledger.
`query_tasks` devolve duas URLs de vídeo: `url` (com a marca do Kling no canto inferior direito) e `urlWithoutWatermark`. A marca "AI Generated" no canto superior esquerdo segue a configuração da conta na web; alterar, esperar 30 s e consultar de novo [OFICIAL, descrição de `query_tasks`]. Qual versão é a de entrega é decisão do producer; **guarde a sem marca como original se o plano permitir**.

## 1. Técnico (barato, automático)

```bash
f=take.mp4
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,duration \
        -show_entries format=duration,size -of json "$f"
ffmpeg -v error -i "$f" -f null - ; echo "decode exit=$?"   # saída vazia e exit 0 = decodifica inteiro
sha256sum "$f"
```

Compare com o pedido: duração, resolução, quadros (o piloto de olhos: 121 quadros, 1516×604, 5,041667 s). Falha: duração diferente do pedido, zero quadros, resolução errada, erro de decodificação.

## 2. Visual

```bash
ffmpeg -v error -i "$f" -vf "select='eq(n,0)+eq(n,60)+eq(n,120)',scale=640:-1,tile=3x1" -frames:v 1 triptych.png
ffmpeg -v error -i "$f" -vf "scale=160:-1,tile=11x11" -frames:v 1 grid_all_frames.png   # 5 s ≈ 121 quadros
```

- Triptych (primeiro/meio/último) = triagem. **Grade de todos os quadros com recorte do rosto = o gate** para qualquer take com rosto (playbook).
- Ajuste `tile` ao número de quadros (`nb_frames`). Para takes longos, divida em blocos.
- Cheque em todos os quadros: **nenhum rosto completo de figura histórica**, incluindo reflexos em superfícies; mão/objeto não invadem o rosto; mesa com a mancha de anel no lugar combinado (J26-2); figurino igual ao aprovado; sem objetos novos; sem texto deformado.
- Olhos: o piloto de olhos teve duas piscadas em vez de uma e foi aceito "pendente de reprodução em velocidade real" — registre desvios assim, não os esconda.

## 3. Áudio e fala

```bash
ffmpeg -v error -i "$f" -vn -af "ebur128=peak=true" -f null - 2>&1 | tail -n 12   # LUFS e true peak
```

STT (já existe no projeto, `.venv` com faster-whisper `base.en`) [PROJETO]:

```bash
.venv/bin/python -c "
from faster_whisper import WhisperModel
m=WhisperModel('base.en'); seg,_=m.transcribe('take.mp4'); print(' '.join(s.text.strip() for s in seg))"
```

Compare palavra a palavra com `dialogue-lines.csv`. Cheque: pausa onde o prompt pediu, silêncio depois da última palavra, ausência de música ou voz extra, volume constante. O projeto não fixa meta de loudness; registre o valor medido e deixe a meta para o editor.
`base.en` só transcreve inglês: para outros idiomas use modelo multilíngue e revisão humana (gate de idioma).

## 4. Critérios de aceitação (checklist)

| # | Critério | Quem decide |
|---|---|---|
| 1 | Decodifica inteiro; duração/resolução/fps conforme o pedido | automático |
| 2 | Grade de todos os quadros sem rosto completo de figura histórica nem reflexo | Claude/Codex + humano |
| 3 | Semelhança do Andre com a referência aprovada | **Andre** |
| 4 | Fala = texto canônico (STT) e voz aprovada | Andre |
| 5 | Continuidade: mesa, figurino, luz, direção do olhar | Codex |
| 6 | Sem artefato (morph, mão extra, texto deformado) | reprodução humana |
| 7 | Registro: `generationId`, sha256, custo, `authorization_ref`, decisão (aceito/rejeitado + motivo) | producer |

Takes rejeitados continuam no disco com o motivo; não se apaga.

## 5. Segunda opinião automatizada (opcional, exige escopo)

Indexar clipes finais num serviço de busca de vídeo (ex.: Jockey/TwelveLabs) para perguntar "algum quadro mostra um rosto de frente?" é **upload para terceiros** = escrita externa, só com autorização (ver `15`). Não substitui a grade local.
