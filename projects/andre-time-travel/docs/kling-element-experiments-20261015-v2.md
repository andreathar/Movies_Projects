# Experimentos Kling — lote 2 e revisão temporal, 15/10/2026

Entrega de arquivo e método, pendente de revisão do produtor. Nenhuma amostra aceita para produção. Os documentos e a mídia do lote 1 permanecem intactos.

## Entrega e lacunas

O catálogo `07_generations/downloads/2026-10-15-element-experiments-v2/index.html` reúne o lote 1 por ligação e os seis arquivos novos, sem recopiar seus vídeos. Quatro recursos de `Costumes_Athar_2` (Element `324019350521447`) vieram da CLI existente: capa, `back`, `side`, `closeUp`, total 3.442.665 bytes. Seus prompts de origem/modelo/settings não são expostos pelo Element e não foram recuperados.

O quinto arquivo é cópia deduplicada do download local `kling_20261015_VIDEO_Element1fi_3780_0.mp4`, 11.053.435 bytes. Seu AIGC conserva `SGP_PROD_ai_web_324018500523155`. Esse ID difere de `324018500502140`, inventariado no histórico: a relação é candidata, não comprovada. O vídeo local tem 361 quadros, 1280×720, 24fps, 15,041667s e **nenhuma faixa de áudio**. Não sabemos se o original remoto tem áudio.

O prompt exibido anteriormente está preservado literalmente em `prompts.json`, inclusive `against .`, `diferent` e `thet`. Falta o oponente, sua referência técnica, a serialização do pedido e seus parâmetros. Não preencher por aparência ou pelo nome do arquivo. A conexão atual oferece apenas o frontend local; a navegação Kling mostrou login. A CLI consulta Elements, mas não fornece a correspondência desse histórico web. Não houve login, nova autorização, contorno de API ou busca massiva.

Total novo de mídia original: **6 arquivos / 14.641.524 bytes**, quatro downloads e duas cópias locais; zero duplicatas persistidas, zero mídia anterior recopiada. Registro: 318→324 linhas, todas as seis novas `approved=false`. O inventário antigo continua reservado para outro lote. Não houve URL expirada entre os quatro downloads; para o teste web falta a URL, não há evidência de expiração.

Também foi preservado `20261014_133324-IMG_STYLE.jpg` do diretório local de Andre (145.424 bytes), com hash distinto. Nome-base, dimensões 768×1376, conteúdo observado e diferença média de pixels 0,604/255 indicam correspondência forte com a capa de `Costumes_Athar_2`. É candidato a fonte local, sem prova do upload exato nem prompt de origem; a variante local e a capa do provedor são conservadas com papéis diferentes.

## O que a inspeção demonstra

Foram vistos 1.636 quadros em 45 folhas estáticas consecutivas, tiles 256×144, abrangendo os quatro vídeos anteriores e o candidato local. Isso amplia a revisão de cinco quadros para cobertura temporal por quadros; **não é reprodução em velocidade normal, escuta, análise facial em resolução integral nem aceite**. Blur e oclusão limitam mãos, contato e identidade. Métricas/ASR estão separadas de percepção em `review.json` e `review/temporal/`.

| Asset ID | Observação própria por sequência | Consequência para preparar o próximo teste |
|---|---|---|
| `KEXP-E324018220506771-video` | Corpo inteiro e retrato simultâneos durante os 192 quadros; corpo aproxima e gira, retrato articula. | Preferir futuramente referência limpa de uma pessoa/vista por vez; composto pode misturar enquadramentos. Não editar o original. |
| `KEXP-W323866270650569-result` | Elenco de três persiste; corte f170→171 (7,125s); gestos/bocas e olhares à câmera. | Especificar posição dos três, comportamento e plano/corte se forem critérios. Nome não fixa blocking. |
| `KEXP-W323868230505094-result` | Só o homem em todos os quadros; duas companheiras ausentes. Café/roupa/efeito mudaram juntos. Salto de pose/enquadramento em 7,125s. | Isolar alteração de roupa; exigir preservação de elenco, posições, mesa e câmera. Não basta contar nomes no pedido. |
| `KEXP-W323869015528491-result` | Três personagens em mesa baixa, posições diferentes; corte 7,625s; floco cobre rosto por volta de 10,83–11,25s. | Nova geração não herda assentos não especificados. FX deve ficar atrás dos rostos/mãos quando continuidade for requisito. |
| `KEXP2-W324018500523155-local` | Dois homens mantêm roupa/visual amplo durante luta, giros e sobreposições. Começa em retrato e abre. | Não inferir identidade do oponente, lente 200mm ou vínculo de histórico. Contato, mãos e rosto sob blur precisam revisão ampliada e playback humano. |

O figurino novo mostra camiseta verde mesclada em V, calça azul xadrez e tênis escuro com marca N branca; vistas frontal, traseira, perfil e detalhe de torso. Há um rosto próprio nas referências. Tratar como roupa, separando identidade; possíveis recortes futuros são derivados com hash novo e autorização própria. Ele não substitui D02.

## Áudio: medições e lacuna de escuta

Este modelo não recebeu áudio: o tool informou que entrada de áudio não é suportada. Extrações WAV ficam disponíveis para escuta humana. Nenhuma avaliação de inteligibilidade, idioma, voz, dublagem ou sincronia foi aceita.

| Vídeo | I (LUFS) | LRA (LU) | Pico reportado pelo ebur128 (dBFS) |
|---|---:|---:|---:|
| Referência de 8s | −21,6 | 2,9 | −5,2 |
| Base de três pessoas | −24,8 | 3,8 | −9,6 |
| Edição roupa/café/efeito | −24,8 | 3,8 | −9,6 |
| Café/neve | −24,0 | 4,2 | −7,9 |
| Candidato kung-fu local | sem faixa | — | — |

O PCM mono 16k da base e da edição tem 240.745 amostras em cada arquivo, correlação **0,9999734**, RMSE 8,285 em PCM16, mas não é idêntico. Há forte evidência numérica de áudio preservado/recomprimido, enquanto duas pessoas sumiram do vídeo. Preservar som não prova preservar elenco ou sincronizar falantes. Logs `ebur128`, `silencedetect` e comparação estão arquivados; limiares não são julgamento auditivo.

ASR offline usou o modelo inglês já em cache `faster-whisper-base.en`, CPU int8. As hipóteses das cenas contêm frases implausíveis: conservar como saída automática, sem tratá-las como transcrição ou concluir idioma. No vídeo de 8s, a última hipótese termina perto do fim: verificar possível truncamento pela escuta. O candidato de luta não permite avaliar sons de golpes porque não possui track local.

## Nomear sem destruir a proveniência

Guardar campos independentes: `asset_id`, `elementId`, `originalName`, nome de cada recurso, `sha256`, alias local e vínculo a prompt/inputs/result. Os aliases são propostas locais; nada foi renomeado na conta.

| ID | Nome original exato | Alias local proposto |
|---|---|---|
| 323980733525179 | `Andre_Athar_Element` | `AA-ID-20261014-v01` |
| 324018220506771 | `Andre Athar_vr` | `AA-VIDREF-v01` |
| 323867570654831 | `Costume 1` | `WD-GREYTIE-v01` |
| 323854711683871 | `table 1` | `TB-J26ALT4-v01` |
| 324019350521447 | `Costumes_Athar_2` | `WD-GREENCHK-v01` |

`EXP-KF-LOCAL-v01` descreve o candidato local sem alegar associação. Não reciclar alias de identidade para roupa ou nova versão, nem acrescentar “approved/canon”. `Andre Athar` dos testes antigos continua ID desconhecido, distinto dos dois Elements novos. Preservar `Video1`, `Blonde Lady`, `Sarah`, `Zen-style Café`, `Snowflake`, `Stellar Black Hole`, nomes/slots e marcadores técnicos literais nos registros históricos. `table 1` continua `_4_alt`, enquanto D04 escolheu `_2`.

## Semântica verificada e templates de preparação

O [guia oficial Element Library](https://kling.ai/quickstart/klingai-element-library-3-user-guide), revisto em 15/10, descreve referência principal e 1–3 suplementares, recomenda frontal principal e outros ângulos/detalhes. Distingue categorias de personagem, roupa, objeto, cenário e efeito; permite voz vinculada a personagens e chamada via `@` no app. Recomenda nomes únicos, relevantes e descrições com detalhes a preservar/ignorar. Essas capacidades ajudam a organizar o pedido; não comprovam fidelidade destes resultados.

A CLI global 0.2.1 foi preservada; o snapshot `tool_list.json` continua sendo a autoridade dos argumentos compatíveis. Binding real usa IDs/fields do schema e marcadores `<<<id>>>`. `[@nome]` abaixo é notação editorial do app, não um payload executável nem prova da serialização antiga. Não transformar webHistoryId num generationId da CLI. Limites e parâmetros dependem do modelo; consultar o schema antes de preparar submissão.

**Alterar uma variável, mantendo critérios verificáveis (rascunho):**

```text
In [@Video1], change only the costume worn by [@IDENTITY] to [@COSTUME].
Retain all three people, their identities and screen positions throughout.
Preserve table height/size, seating, room, shot timing, framing and motion.
Do not replace either companion. Do not introduce dialogue.
Audio plan: <explicitly choose preserve source / silent / exact authorized line>.
```

**Nova composição com ambiente/efeito (rascunho separado):**

```text
[@IDENTITY] sits <seat/height/screen position> at [@EXACT_TABLE_VERSION].
[@COMPANION_A] is <position>; [@COMPANION_B] is <position>.
Scene: [@SCENE]. Shot: <framing and movement>; cuts: <explicit plan>.
[@FX] stays behind the cast; faces, mouths and hands remain unobstructed.
Action: <one specific gaze/gesture beat>. Speech/audio: <explicit plan>.
```

**Ficha antes de qualquer envio futuro:**

```json
{
  "identity": {"asset_id":"<exact>","elementId":"<actual>","originalName":"<literal>","sha256":"<hash>"},
  "costume": {"elementId":"<actual>","originalName":"<literal>","ignore":"reference wearer face"},
  "editSource": {"asset_id":"<exact>","slot":"Video1","sha256":"<hash>"},
  "promptExact":"<unaltered text and actual tokens>",
  "bindingsOrdered":[], "model":"<live-compatible>", "settingsExplicit":{},
  "changeOnly":["costume"], "preserve":["cast","seating","table","camera","timing"],
  "audioPlan":"<specific>", "approved":false
}
```

Separar ensaios de roupa, cenário, FX e áudio torna causas comparáveis; a melhoria é proposta, não testada. Para luta, preencher oponente e binding reais antes de reutilizar o pedido truncado; “200mm” no texto não certifica óptica no arquivo.

O registro/galeria é descoberto pelo caminho existente **Organização → Pontos de entrada → Experimentos Kling / Lições de Elements**. O frontend expõe metadados e copiar caminho; não serve a galeria HTML (a rota natural retorna 404). Abrir o HTML local. Não houve redesign ou exposição de mídia.

Produtor desktop é o próximo responsável por revisar arquivo, confirmar vínculo do MP4, recuperar histórico autenticado e organizar escuta humana; nenhuma tarefa de outro agente foi disparada. G-IN/G-OUT, production-plan, D02/D04, identidade de produção `323525046658711` e todos os aceites permanecem intocados. Handoffs anteriores continuam históricos e pendentes; esta entrega só propõe reconciliação, sem ingestão. Andre não atribuiu aceite individual a estes exemplos; as observações acima são próprias.
