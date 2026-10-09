# Galileo EN v2 — entrega para revisão, sem aceite

Data: 2026-10-09. Escopo: montagem local solicitada na mensagem 3 do Parley, com a resolução de timing dada diretamente por Andre nesta sessão: “Seguir a ordem da v2, reposicionar G-L04 sem alterar a gravação e limitar olhos B a 2 s, completando com insert.”

Foram criados somente arquivos novos. Não houve commit, merge, geração externa, chamada paga ou alteração de manifest, board, approvals, ledger, STATE ou decisões. O produtor continua responsável pelo ledger. Esta entrega não registra aprovação de takes, de identidade, de voz ou de picture lock.

## Entregáveis

- [Prévia MP4](../../picture-lock/galileo-en-preview-v2.mp4): 42,000 s, 1.008 quadros, 1920 × 1080, 24 fps constantes, H.264, áudio AAC estéreo a 48 kHz e legenda inglesa selecionável.
- [Timeline v2](../../timelines/galileo-en-v2.json): cortes, fontes, hashes, timing de áudio, placeholders e limites desta revisão.
- [QC final](technical-qc.json), [ffprobe completo](ffprobe.json), [preservação após render](preservation.json), [preservação final](final-preservation.json) e [inventário com hashes](artifact-index.json).
- [Índice dos quadros](frames/index.json), [junções](frames/joins.png), [comandos executados](build-log.json), [receita de montagem](build.py) e [receita de extração dos quadros](frame_sheets.py).

SHA-256 do MP4: `bd687d42ea6692b4c81efa2a78a8acdcea48f2f98308e1f9b40ee55d5b7e850b`.

SHA-256 da timeline: `55dcaf3b90513c669615c7d72019162bf9a1f02127e440e855a6e8f3c0a84534`.

## Alterações da montagem

A ordem da seção 5 do checkpoint foi mantida usando as takes existentes. Todas as imagens rodam a 1×. Os olhos A ocupam exatamente 48 quadros (16–18 s); os olhos B, outros 48 quadros (30,791667–32,791667 s). O intervalo restante até 33,5 s usa um insert de 17 quadros, contínuo com o insert seguinte.

A gravação G-L04 permanece integral e com o mesmo hash; seu início no mix passou de 25,5 s para 22,8 s. Os quatro WAVs de fala, o room-tail e o mix original da v1 foram preservados. Foi criado um novo mix para acomodar o deslocamento autorizado, usando a receita de níveis da v1; portanto, o mix final da v2 não é idêntico em bytes ao mix da v1. Não houve aceleração, nova fala ou correção de pronúncia. G-L01, G-L02 e G-L03 mantêm seus inícios de 0,5, 4 e 20 s.

Em 24 fps, os cortes de imagem nominalmente previstos em 22,8 e 30,8 s são quantizados para 22,791667 e 30,791667 s, respectivamente. A diferença é de 8,333 ms em relação ao início/fim nominal do áudio G-L04. A duração total continua exatamente 42 s. O final nominal do arquivo G-L03 em 22,83 s sobrepõe o início de G-L04 por 30 ms; nenhum WAV foi cortado para esconder isso. A percepção dessa junção exige escuta.

As legendas mantêm as palavras da v1. Os tempos de G-L04 foram antecipados em 2,7 s e o fim da legenda G-L03 passou de 22,83 para 22,8 s para evitar sobreposição de legendas. O texto da legenda não constitui validação da fala efetivamente pronunciada.

## Verificação realizada

- Render concluído e `ffprobe -count_frames` confirmou 1.008 quadros de vídeo e duração de 42,000 s. A decodificação completa terminou com código 0, sem mensagens em `decode.log`.
- Medição do áudio codificado: −16,3 LUFS integrados, faixa de loudness de 6,5 LU e pico verdadeiro de −1,0 dBFS. Evidência: `loudness.log`.
- Inspeção visual de todas as 26 folhas sequenciais, cobrindo os quadros 0–1007, e da folha adicional de junções. Cada quadro foi visto como uma miniatura de 400 × 225 pixels. Foram incluídos os 456 quadros dos eventos sinalizados com risco de enquadramento histórico.
- Nessa resolução de inspeção, nenhum rosto histórico completo ou refletido foi observado. Os dois planos de olhos permaneceram recortados na faixa dos olhos; os inserts mantiveram mãos, mesa e torso, sem entrada de cabeça. Os planos de Andre não mostraram outra pessoa ou rosto refletido. Não se observaram quadros pretos acidentais ou imagem esticada nas junções.
- `.venv/bin/python -m unittest discover -s tests -v`: 29 testes passaram. `.venv/bin/python scripts/manage.py validate`: válido, sem erros, com os quatro avisos já existentes sobre hashes de skills compartilhadas. Esses resultados foram observados nos retornos dos comandos nesta sessão; não são prova de aceite do filme.
- Os 38 arquivos do baseline foram verificados por SHA-256 após o render e novamente na entrega. Isso inclui fontes, v1 e registros canônicos. O diff de arquivos já rastreados permaneceu vazio; o inventário de novos arquivos está em `artifact-index.json`.

Comandos principais de reprodução da receita (a receita recusa sobrescrever saídas já existentes):

```sh
python3 projects/andre-time-travel/08_edit/reviews/galileo-en-v2/build.py --ffmpeg /home/athar/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg --ffprobe /home/athar/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffprobe
python3 projects/andre-time-travel/08_edit/reviews/galileo-en-v2/frame_sheets.py --ffmpeg /home/athar/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/manage.py validate
```

`build-result.json` e o estado da timeline retratam o momento imediatamente posterior ao render, anterior à inspeção visual. `technical-qc.json` e este documento registram a inspeção posterior. Nenhum desses registros indica reprodução com áudio em velocidade normal ou aceite por Andre.

## Pendências para o produtor e Andre

1. Reproduzir o MP4 inteiro em velocidade normal, com áudio, e avaliar ritmo, sincronismo labial, junção G-L03/G-L04 e intenção das reações. Essa reprodução não foi realizada nesta revisão por folhas de quadros.
2. Avaliar a pronúncia já questionada de G-L04 e a voz-guia. A gravação foi preservada, não corrigida nem validada linguisticamente.
3. Resolver as substituições temporárias: G-X01 (escuta/back-view) e G-X02 (ângulo alternativo de Andre) não estão disponíveis. O insert ocupa a lacuna de G-X01; a tomada frontal existente ocupa G-X02. Não se afirma que um back-view novo foi produzido.
4. O trecho final de escuta, 38,5–41,5 s, usa PILOT-02, com a diferença conhecida de mesa/assento (F01). É um placeholder explícito e ainda exige decisão de continuidade.
5. Fazer a revisão de identidade de Andre e de pequenos artefatos em resolução integral. A inspeção de 400 × 225 por quadro verifica enquadramento amplo; não substitui esse aceite.

A entrega está pronta para revisão editorial, com essas limitações abertas. Nenhum gasto foi autorizado por esta montagem e nenhuma atualização de estado canônico foi feita.
