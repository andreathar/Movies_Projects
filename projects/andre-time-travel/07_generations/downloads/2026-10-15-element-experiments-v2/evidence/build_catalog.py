import csv, hashlib, html, io, json, os, shutil
from pathlib import Path
from datetime import datetime, timezone

R=Path('/mnt/data/Projects_SSD/Movies_Projects')
T=Path('/tmp/kling-batch2-20261015')
P='projects/andre-time-travel/'
C=P+'07_generations/downloads/2026-10-15-element-experiments-v2/'
OLD=P+'07_generations/downloads/2026-10-15-element-experiments-v1/'
GUIDE=P+'docs/kling-element-experiments-20261015-v2.md'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(path,obj):
 p=R/path; p.parent.mkdir(parents=True,exist_ok=True)
 assert not p.exists(),str(p)
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
guards=json.loads((T/'guards.json').read_text())
assert all(sha(R/p)==h for p,h in guards.items()),'Concurrent protected change: stop before integration'
base=R/C; assert not base.exists(); base.mkdir(parents=True)
(base/'evidence/integration-before').mkdir(parents=True)
mutable=[P+'asset-registry.csv','sites/movies-demandas/scripts/export-workspace.mjs','sites/movies-demandas/data/workspace-reference.json']
for p in mutable: shutil.copy2(R/p,base/'evidence/integration-before'/Path(p).name)
for name in ['guards.json','base-hashes.json','who_am_i.sanitized.json','tool_list.json','element_get-324019350521447.json','retrieval.json','local-kungfu.json','analysis.json','local-analysis.json','audio-base-edit-comparison.json','analyze.py','download_costume.py']:
 shutil.copy2(T/name,base/'evidence'/name)
shutil.copytree(T/'temporal',base/'review/temporal')
shutil.copy2(T/'costume2-reference-sheet.jpg',base/'review/costume2-reference-sheet.jpg')
retrieval=json.loads((T/'retrieval.json').read_text())
records=retrieval['records']+[json.loads((T/'local-kungfu.json').read_text())]
for rec in records:
 assert sha(R/rec['path'])==rec['sha256']
 rec['approved']=False
 rec['catalog']=C+'manifest.json'
 rec['proposedLocalAlias']='WD-GREENCHK-v01' if rec.get('elementId') else 'EXP-KF-LOCAL-v01'
 rec['role']='costume_reference' if rec.get('elementId') else 'local_result_candidate'
 put(rec['path']+'.json',rec)
with (base/'resources.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['asset_id','path','sha256','bytes','role','elementId','originalName','resourceName','retrieval','approved'],extrasaction='ignore');w.writeheader();w.writerows(records)
inventory=json.loads((R/OLD/'next-batch-inventory.json').read_text())
target=inventory['newlyAppearedDuringSession'][1]
target.update({'promptSource':OLD+'next-batch-inventory.json','promptCapture':'Historical displayed DOM text only; not serialized request; no fresh authenticated history visibility in batch 2','model':None,'settings':None,'generationId':None,'opponentElementId':None,'opponentOriginalName':None,'downloaded':False,'associatedCandidateAssetId':records[-1]['asset_id'],'candidateMappingConfirmed':False,'status':'blocked_authenticated_history_unavailable'})
put(C+'prompts.json',{'newExperiment':target,'newCostumeSourcePrompt':None,'newCostumePromptGap':'Element metadata exposes resources/description, not originating prompts/model/settings. No matching local source sidecar was established.','priorExactPrompts':OLD+'prompts.json','machineTokensPreserved':True})
put(C+'next-batch-inventory.json',{'olderObserved':inventory['olderObserved'],'olderDownloadedThisBatch':0,'pendingHistoryItem':target,'missingReferenceOriginals':OLD+'manifest.json','scope':'Bounded to two inventoried recent items; no whole-account history claim'})
observations=[
 {'asset_id':'KEXP-E324018220506771-video','frames':192,'observed':'Split screen throughout. Left body approaches then turns profile/back near 5.5–7.1s; right portrait articulates/blinks. Broad longer hair/beard, pinstripe jacket and black shirt persist in these thumbnails. Two simultaneous views remain, so this is a composite reference, not a clean single-subject shot.','limits':'No normal-speed playback or heard speech; no full-resolution facial/voice acceptance.'},
 {'asset_id':'KEXP-W323866270650569-result','frames':361,'observed':'Three cast members persist: realistic woman left, short-haired man center, cartoon Sarah right. Hard cut f170→171 at 7.125s changes height/framing. Mouth and hand activity exceeds a simple silent gaze; gaze also goes toward camera.','limits':'Table perspective changes; no metric proof of table geometry or exact facial likeness.'},
 {'asset_id':'KEXP-W323868230505094-result','frames':361,'observed':'Both companions are absent throughout all 361 static thumbnails. Solo short-haired man wears grey jacket/white shirt/tie in café; purple black-hole effect appears around 1.5s. Pose/framing/effect jumps f170→171 near 7.125s; automated scene threshold misses it.','limits':'Compared to the archived base sequence, visual cast is not retained. Audio similarity is measured separately, not heard.'},
 {'asset_id':'KEXP-W323869015528491-result','frames':361,'observed':'Three people persist, kneeling around a low table in café. Sarah is on screen left, realistic woman right. Hard cut f182→183 at 7.625s goes wide→close. Snow increases; a large foreground flake occludes the man’s face around 10.83–11.25s.','limits':'This is a separate generation; an unspecified previous seating arrangement cannot be assumed. Face continuity cannot be assessed while occluded.'},
 {'asset_id':records[-1]['asset_id'],'frames':361,'observed':'Opening portrait widens into two-person kung-fu choreography on white background. Longer-haired man in grey pinstripe jacket/black shirt and second dark-haired man in black remain broadly distinguishable. Camera framing and screen positions change as bodies move; limbs/faces overlap during blocks and kicks.','limits':'Every frame inspected as a 256×144 static tile; blur/occlusion prevents certifying hands, contact physics or exact identity. No inferred opponent identity, 200mm focal-length verification or binding to the inventoried web item. Local artifact has zero audio streams.'}
]
analyses=json.loads((T/'analysis.json').read_text())+json.loads((T/'local-analysis.json').read_text())
review={'method':'All decoded frames viewed as consecutive 256×144 static tiles, 40/tile sheet (last padded). 45 sheets / 1636 populated tiles. Computational scene/difference metrics and offline ASR are supporting data, not perception.','framesInspected':sum(o['frames'] for o in observations),'sheetsInspected':sum(len(d['sheets']) for d in analyses),'normalSpeedPlaybackWatched':False,'actualAudioListening':False,'audioInputLimitation':'Tool explicitly omitted audio because this model does not support audio input.','observations':observations,'audio':{'baseEditPearsonMono16k':0.9999733962252226,'baseEditInterpretation':'Strong numerical similarity after decoding; sample arrays are not identical. Does not establish perceived intelligibility, speaker match or lip sync.','rawComparison':'evidence/audio-base-edit-comparison.json','ASR':'Local cached faster-whisper-base.en, CPU int8, no downloads. Raw English hypotheses contain implausible text and are not trusted transcripts or language judgments.','needsHumanListening':['intelligibility and language','voice identity','lip sync and off-screen speech','hit sounds and original kung-fu audio','end truncation in 8-second reference']},'andreJudgments':'Andre described naming references as a successful strategy. No individual sample approval/judgment supplied. All observations here are the archivist’s.'}
put(C+'review.json',review)
aliases=[('323980733525179','Andre_Athar_Element','AA-ID-20261014-v01'),('324018220506771','Andre Athar_vr','AA-VIDREF-v01'),('323867570654831','Costume 1','WD-GREYTIE-v01'),('323854711683871','table 1','TB-J26ALT4-v01'),('324019350521447','Costumes_Athar_2','WD-GREENCHK-v01')]
put(C+'aliases.json',{'scope':'Local proposals only. No provider name, description or binding changed.','elements':[dict(elementId=a,originalName=b,proposedLocalAlias=c) for a,b,c in aliases],'results':[{'asset_id':o['asset_id'],'alias':a} for o,a in zip(observations,['AA-VIDREF-v01','EXP-3CAST-TABLE-01','EXP-GREYTIE-ZEN-01','EXP-ZEN-SNOW-01','EXP-KF-LOCAL-v01'])]})
store=shutil.disk_usage(R)
put(C+'manifest.json',{'schemaVersion':1,'capturedAt':datetime.now(timezone.utc).isoformat(),'scope':'Second bounded existing-assets batch; no generation, uploads, Element mutation, spend, installs, account changes or dispatch.','priorCatalog':OLD+'manifest.json','resources':records,'counts':{'newUniqueMediaFiles':len(records),'newMediaBytes':sum(x['bytes'] for x in records),'cdnDownloadFiles':4,'cdnDownloadBytes':retrieval['transferBytes'],'localCopiedFiles':1,'localCopiedBytes':records[-1]['bytes'],'duplicateHitsThisBatch':0,'priorMediaRecopied':0,'registryRowsBefore':318,'registryRowsAfter':323,'framesInspectedAsStaticTiles':1636,'sheets':45},'storage':{'budgetBytes':retrieval['budgetBytes'],'freeBytesAfter':store.free,'budgetAppliesTo':'New canonical original media; derived review files counted separately at closeout'},'newElementEvidence':'evidence/element_get-324019350521447.json','pendingHistoryItem':target,'provenanceGaps':['Costumes_Athar_2 source prompts/model/settings unknown; resources retrieved from current Element record.','Kung-fu serialized prompt, opponent token/ID, request model/settings and remote original URL unavailable: current browser exposes login only.','Local ProduceID SGP_PROD_ai_web_324018500523155 differs from inventoried webHistoryId 324018500502140; relationship unconfirmed.','Local kung-fu export has no embedded audio; remote original’s audio unknown.','Prior library previews retain unresolved IDs/originals from v1.','No attempted resource URL was expired in this batch; no URL available for web kung-fu result.'],'review':'review.json','aliases':'aliases.json','approved':False})
reg=R/P/'asset-registry.csv'; before=reg.read_bytes(); out=io.StringIO(newline=''); w=csv.writer(out,lineterminator='\n')
assert len(list(csv.DictReader(io.StringIO(before.decode()))))==318
for x in records:
 w.writerow([x['asset_id'],'kling_element_resource' if x.get('elementId') else 'kling_local_result_candidate',x['path'],'workspace','Kling existing assets archive 2026-10-15; Element '+x['elementId'] if x.get('elementId') else 'Kling existing local export; embedded ProduceID SGP_PROD_ai_web_324018500523155',x['sha256'],'false','experimental_unapproved; catalog='+C+'manifest.json; role='+x['role']+'; no production acceptance'+('; web mapping unconfirmed' if not x.get('elementId') else '; original_name='+x['originalName']+'; resource_name='+x['resourceName'])])
assert reg.read_bytes()==before
with reg.open('ab') as f:f.write(out.getvalue().encode())
assert reg.read_bytes().startswith(before)

guide='''# Experimentos Kling — lote 2 e revisão temporal, 15/10/2026

Entrega de arquivo e método, pendente de revisão do produtor. Nenhuma amostra aceita para produção. Os documentos e a mídia do lote 1 permanecem intactos.

## Entrega e lacunas

O catálogo `07_generations/downloads/2026-10-15-element-experiments-v2/index.html` reúne o lote 1 por ligação e os cinco arquivos novos, sem recopiar seus vídeos. Quatro recursos de `Costumes_Athar_2` (Element `324019350521447`) vieram da CLI existente: capa, `back`, `side`, `closeUp`, total 3.442.665 bytes. Seus prompts de origem/modelo/settings não são expostos pelo Element e não foram recuperados.

O quinto arquivo é cópia deduplicada do download local `kling_20261015_VIDEO_Element1fi_3780_0.mp4`, 11.053.435 bytes. Seu AIGC conserva `SGP_PROD_ai_web_324018500523155`. Esse ID difere de `324018500502140`, inventariado no histórico: a relação é candidata, não comprovada. O vídeo local tem 361 quadros, 1280×720, 24fps, 15,041667s e **nenhuma faixa de áudio**. Não sabemos se o original remoto tem áudio.

O prompt exibido anteriormente está preservado literalmente em `prompts.json`, inclusive `against .`, `diferent` e `thet`. Falta o oponente, sua referência técnica, a serialização do pedido e seus parâmetros. Não preencher por aparência ou pelo nome do arquivo. A conexão atual oferece apenas o frontend local; a navegação Kling mostrou login. A CLI consulta Elements, mas não fornece a correspondência desse histórico web. Não houve login, nova autorização, contorno de API ou busca massiva.

Total novo de mídia original: **5 arquivos / 14.496.100 bytes**, quatro downloads e uma cópia local; zero duplicatas persistidas, zero mídia anterior recopiada. Registro: 318→323 linhas, todas as cinco novas `approved=false`. O inventário antigo continua reservado para outro lote. Não houve URL expirada entre os quatro downloads; para o teste web falta a URL, não há evidência de expiração.

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
'''
(R/GUIDE).write_text(guide)
def link(p):return html.escape(os.path.relpath(R/p,base),quote=True)
sections=['<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Kling · arquivo de experimentos v2</title><style>body{font:16px system-ui;background:#121821;color:#e9eef5;max-width:1100px;margin:32px auto;padding:0 20px}a{color:#9ac9ff}video,img{max-width:100%;max-height:540px}article{padding:20px;border:1px solid #475367;border-radius:12px;margin:24px 0}code{overflow-wrap:anywhere}summary{cursor:pointer}small{color:#b8c7dc}</style><h1>Experimentos Kling · lote 2</h1><p>Arquivo para revisão. Cinco novos arquivos; sem aceite de produção, geração ou alterações na conta.</p><p><a href="'+link(OLD+'index.html')+'">Catálogo anterior</a> · <a href="'+link(GUIDE)+'">Lições/templates</a> · <a href="manifest.json">Manifesto</a> · <a href="prompts.json">Prompts e lacunas</a> · <a href="review.json">Método/observações</a> · <a href="aliases.json">Aliases locais</a></p><p>1.636 quadros vistos em folhas estáticas de 256×144. Sem reprodução em velocidade normal nem escuta. WAVs e ASR abaixo são derivados; ASR não validado. Galeria local, não servida pelo frontend.</p><article><h2>Costumes_Athar_2 · 324019350521447</h2><p>Alias proposto: WD-GREENCHK-v01. Capa, back, side, closeUp; prompts de origem desconhecidos.</p><img src="review/costume2-reference-sheet.jpg" alt="Quatro vistas do figurino verde e xadrez azul">']
for x in records[:4]: sections.append('<p><a href="'+link(x['path'])+'">'+html.escape(x['asset_id']+' · '+x['resourceName'])+'</a> <small>'+x['sha256']+'</small></p>')
sections.append('</article>')
for o,d in zip(observations,analyses):
 sections.append('<article><h2>'+html.escape(o['asset_id'])+'</h2><video controls preload="none" src="'+link(d['sourcePath'])+'"></video><p>'+html.escape(o['observed'])+'</p><p><strong>Limite:</strong> '+html.escape(o['limits'])+'</p>')
 if o['asset_id'].startswith('KEXP2'):sections.append('<p>ProduceID 324018500523155; relação com webHistoryId 324018500502140 não confirmada. Sem faixa de áudio local.</p>')
 a='review/temporal/'+o['asset_id']+'/'
 if (base/a/'audio.wav').exists():sections.append('<p>Derivado mono 16k para revisão humana: <audio controls preload="none" src="'+a+'audio.wav"></audio></p><a href="'+a+'asr.json">Hipótese ASR não validada</a>')
 sections.append('<details><summary>Todos os quadros — folhas estáticas</summary>')
 for s in d['sheets']: sections.append('<a href="review/'+s['path']+'"><img loading="lazy" src="review/'+s['path']+'" alt="Quadros '+str(s['firstFrame'])+'–'+str(s['lastFrame'])+'"></a>')
 sections.append('</details></article>')
sections.append('</html>');(base/'index.html').write_text('\n'.join(sections))
(base/'README.md').write_text('# Kling experiments v2\n\nOpen index.html locally. manifest.json links five originals, exact Element resources and historical prompt evidence; review.json states visual/audio limits. Prior catalog is linked, not copied. All candidates unapproved.\n\n5 new originals / 14,496,100 bytes; 3,442,665 downloaded and 11,053,435 copied once locally. 45 static sheets / 1,636 frames, no normal-speed playback or actual listening. Kung-fu local ProduceID differs from web history: mapping unresolved. Source costume prompts absent. Older inventory not fetched.\n\nNext owner: producer desktop; recover authenticated history, verify candidate mapping and arrange human audio review. No dispatch or ingestion.\n')
export=R/'sites/movies-demandas/scripts/export-workspace.mjs';text=export.read_text();assert text.count('element-experiments-v1/index.html')==1;assert text.count('kling-element-experiments-20261015-v1.md')==1
assert sha(export)==guards[str(export.relative_to(R))]
export.write_text(text.replace('element-experiments-v1/index.html','element-experiments-v2/index.html').replace('kling-element-experiments-20261015-v1.md','kling-element-experiments-20261015-v2.md'))
print(json.dumps({'newMediaFiles':5,'newMediaBytes':sum(x['bytes'] for x in records),'registryRows':323,'catalog':C,'guide':GUIDE,'protectedBefore':len(guards)},indent=2))
