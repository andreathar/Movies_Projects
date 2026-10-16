import hashlib,json,subprocess,shutil
from pathlib import Path
R=Path('/mnt/data/Projects_SSD/Movies_Projects');P='projects/andre-time-travel/';C=P+'07_generations/downloads/2026-10-15-element-experiments-v2/';T=Path('/tmp/kling-batch2-20261015')
H=P+'agents/handoffs/2026-10-15-kling-element-experiments-v2-reconciliation.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,d):(R/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
assert not (R/H).exists()
cmd=['node','sites/movies-demandas/scripts/export-workspace.mjs',str(R)]
run=subprocess.run(cmd,cwd=R,capture_output=True,text=True);assert run.returncode==0,run.stderr
(R/C/'evidence/export-update.stdout').write_text(run.stdout)
guards=json.loads((T/'guards.json').read_text());allowed={P+'asset-registry.csv','sites/movies-demandas/scripts/export-workspace.mjs','sites/movies-demandas/data/workspace-reference.json'}
deltas=[{'path':p,'sha256Before':h,'sha256After':sha(R/p)} for p,h in guards.items() if sha(R/p)!=h]
assert {d['path'] for d in deltas}==allowed,deltas
priorNames=['2026-10-15-kling-element-experiments-v1.json','2026-10-15-qc-reference-review-controls-v3-kling-reconciliation.json']
prior=[json.loads((R/P/'agents/handoffs'/n).read_text()) for n in priorNames]
files={};claims=[]
for n,d in zip(priorNames,prior):
 for f in d['changedFiles']:
  path=f['path']; actual=sha(R/path)
  assert actual==f['sha256After'] or path in allowed,(n,path)
  files[path]={'path':path,'sha256After':actual,'reason':'Carried forward current-tree inventory from '+n+('; batch 2 metadata reconciliation' if path in allowed else '; unchanged bytes')}
 for claim in d['claims']:
  assert sha(R/claim['evidence'])==claim['sha256']
  claims.append(dict(claim,statement='Historical evidence only, before batch 2; not current execution or acceptance: '+claim['statement']))
put(C+'evidence/reconciliation.json',{'guardedFiles':len(guards),'unchangedProtected':len(guards)-len(deltas),'exactDeltas':deltas,'allowedMutable':sorted(allowed),'historicalHandoffsPreserved':[{'path':P+'agents/handoffs/'+n,'sha256':sha(R/P/'agents/handoffs'/n)} for n in priorNames],'ingestionPerformed':False,'scope':'Five new original media/sidecars, new archive/guide, append-only registry and two existing discoverability paths. Coalesced current hashes; no production acceptance.'})
for f in list((R/C).rglob('*'))+list((R/P/'07_generations/originals/kling-experiments-20261015-v2').iterdir())+[R/P/'docs/kling-element-experiments-20261015-v2.md']:
 if f.is_file():
  path=str(f.relative_to(R));files[path]={'path':path,'sha256After':sha(f),'reason':'New batch 2 archive/media/provenance/review artifact; unapproved'}
for name,statement in [('manifest.json','Five new canonical original media, exact resources/IDs, hashes and explicit missing source provenance; no production approval.'),('review.json','1636 frames viewed as static tiles; no normal-speed playback or actual listening. Audio similarity and offline ASR are supporting measurements only.'),('evidence/reconciliation.json','177 guards checked; exactly registry/exporter/workspace snapshot changed, protected sources and historical handoffs unchanged.')]:
 claims.append({'statement':statement,'evidence':C+name,'sha256':sha(R/C/name)})
d=json.loads((R/'shared/templates/agent-handoff-v2.json').read_text());d.update({'episode':'andre-time-travel','agentRole':'producer-delegated-kling-archivist','assignment':'Second bounded existing-assets batch and temporal/static-frame/audio-metric review; coalesced reconciliation pending producer review.','parentTask':'Andre proceed relayed by source thread 01a0ff67-e9e4-75a0-99db-8bf420559029; messageSentinel_9e7f601879308191bb67c6d98357b28c','workPackages':['W04','W07','W39','W66'],'readFirst':['AGENTS.md','docs/SHARED_MEDIA.md',C+'README.md',P+'docs/kling-element-experiments-20261015-v2.md'],'ownedPaths':sorted(files),'baseFiles':[{'path':x['path'],'sha256Before':x['sha256Before']} for x in deltas],'changedFiles':sorted(files.values(),key=lambda x:x['path']),'claims':claims,'verification':['All prior claimed file hashes rechecked. Only three authorized metadata paths differ. New catalog reuses prior media by path. Fresh checks saved separately at closeout.'],'nextActions':[{'role':'producer desktop','action':'Review this archive and reconciliation without automatic ingestion. Recover authenticated web record and confirm local kung-fu mapping; arrange human audio/playback review with Andre.','readiness':'pending_producer_review'}],'stageComplete':False,'stageCompleteReason':None,'blockers':[{'description':'No authenticated Kling browser history; web test serialized prompt/opponent/settings/URL missing. Local ProduceID differs, mapping unconfirmed.','owner':'Andre / producer desktop','unblockCondition':'Reconnect existing authenticated Kling tab or provide original request/export metadata proving association.'},{'description':'No actual audio perception or normal-speed playback in this session.','owner':'producer desktop','unblockCondition':'Human listening/playback and separate identity/costume/voice acceptance.'},{'description':'Production exporter snapshot retains earlier Git provenance; no production snapshot changed here.','owner':'producer','unblockCondition':'Review separately if a provenance-only refresh is desired.'}],'andreOnlyGates':['No creative acceptance. Existing production identity, D02/D04, G-IN/G-OUT exact approvals and production plan remain unchanged.'],'proposedDecisions':['Local descriptive aliases and future prompt templates only; no provider rename, new generation or financial authorization.'],'mistakes':[],'paidJobsSubmitted':0,'canonicalStateChanged':False,'reviewStatus':'pending_producer_review','ingest':{'status':'pending','by':None,'at':None},'supersedes':priorNames,'historicalHandoffsPreserved':[{'path':P+'agents/handoffs/'+n,'sha256':sha(R/P/'agents/handoffs'/n)} for n in priorNames],'knownLimitations':['Gallery remains local HTML; frontend exposes metadata/copy-path, no serving route.','Original source prompts of new costume resources not exposed. Older assets not fetched.','Raw ASR is unvalidated English model hypothesis, not heard language or dialogue judgment.']})
put(H,d)
print(json.dumps({'handoff':H,'changedFileClaims':len(files),'historicalClaims':len(claims)-3,'protectedUnchanged':len(guards)-3},indent=2))
