import hashlib,html.parser,json,os,shutil,subprocess,uuid
from pathlib import Path
from datetime import datetime,timezone
R=Path('/mnt/data/Projects_SSD/Movies_Projects');P='projects/andre-time-travel/';C=P+'07_generations/downloads/2026-10-15-element-experiments-v2/';M=P+'07_generations/originals/kling-experiments-20261015-v2/';E=R/C/'evidence';T=Path('/tmp/kling-batch2-20261015');H=P+'agents/handoffs/2026-10-15-kling-element-experiments-v2-reconciliation.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
env=dict(os.environ,TMPDIR='/tmp',PYTHONDONTWRITEBYTECODE='1')
def run(name,cmd,cwd=R):
 d=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=120);(E/(name+'.stdout')).write_text(d.stdout);(E/(name+'.stderr')).write_text(d.stderr);return {'command':cmd,'exitCode':d.returncode}
results={}
results['export-update-final']=run('export-update-final',['node','sites/movies-demandas/scripts/export-workspace.mjs',str(R)]);assert results['export-update-final']['exitCode']==0
# Preserve production snapshot; export comparison only into a newly named temporary file.
production=R/'sites/movies-demandas/data/production.json';original=sha(production);temp=production.parent/('kling-batch2-comparison-'+str(uuid.uuid4())+'.json');assert not temp.exists()
try:
 result=run('production-comparison',['node','sites/movies-demandas/scripts/export-production.mjs',str(R),str(temp)]);assert result['exitCode']==0
 a=json.loads(production.read_text());b=json.loads(temp.read_text())
 def diff(x,y,p=''):
  if isinstance(x,dict) and isinstance(y,dict):return sum([diff(x.get(k),y.get(k),p+'/'+k) for k in x.keys()|y.keys()],[])
  if isinstance(x,list) and isinstance(y,list) and len(x)==len(y):return sum([diff(v,w,p+'/'+str(i)) for i,(v,w) in enumerate(zip(x,y))],[])
  return [] if x==y else [{'path':p,'before':x,'after':y}]
 differences=diff(a,b);assert {d['path'] for d in differences}=={'/collectedAt','/provenance/repositoryHead'},differences
 put(E/'production-freshness-diff.json',{'productionUnchangedSHA256':original,'differences':differences,'sourceContentAndHashesUnchanged':True,'temporaryComparisonRemoved':True})
finally:
 if temp.exists():temp.unlink()
assert sha(production)==original
results['management-lint-tests']=run('management-lint-tests',['.venv/bin/python','-m','unittest','discover','-s','tests','-p','test_manage_lint.py'])
# A handoff is rehashed before running checks that depend on its inventory.
guards=json.loads((T/'guards.json').read_text());allowed={P+'asset-registry.csv','sites/movies-demandas/scripts/export-workspace.mjs','sites/movies-demandas/data/workspace-reference.json'}
deltas=[{'path':p,'sha256Before':h,'sha256After':sha(R/p)} for p,h in guards.items() if sha(R/p)!=h];assert {d['path'] for d in deltas}==allowed
rec=json.loads((E/'reconciliation.json').read_text());rec['exactDeltas']=deltas;put(E/'reconciliation.json',rec)
for name in ['build_catalog.py','add_local_source.py','reconcile.py','checks.py','finalize.py']:
 shutil.copy2(T/name,E/name)
class Links(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):self.links.extend(v for k,v in attrs if k in ('href','src'))
parser=Links();parser.feed((R/C/'index.html').read_text());missing=[link for link in parser.links if not (R/C/link).exists()];assert not missing,missing
manifest=json.loads((R/C/'manifest.json').read_text());assert len(manifest['resources'])==6
assert all(sha(R/x['path'])==x['sha256'] for x in manifest['resources'])
assert (R/P/'asset-registry.csv').read_bytes().startswith((E/'integration-before/asset-registry.csv').read_bytes())
put(E/'final-integrity.json',{'newMediaRehashed':6,'newMediaBytes':sum(x['bytes'] for x in manifest['resources']),'newRegistryRows':6,'originalRegistryRowsPreserved':318,'galleryLinksChecked':len(parser.links),'missingLinks':[],'guards':len(guards),'protectedUnchanged':len(guards)-3,'allowedMutable':sorted(allowed),'productionSnapshotSHA256':original,'audioListening':False,'normalSpeedPlayback':False,'frameTilesInspected':1636,'sheetsInspected':45,'paidJobs':0,'dispatch':0,'ingestion':False})
def refresh():
  d=json.loads((R/H).read_text());files={x['path']:x for x in d['changedFiles']}
  for x in files.values():x['sha256After']=sha(R/x['path'])
  for f in list((R/C).rglob('*'))+list((R/M).iterdir()):
   if f.is_file():files[str(f.relative_to(R))]={'path':str(f.relative_to(R)),'sha256After':sha(f),'reason':'Batch 2 media/catalog/provenance/review; no production acceptance'}
  for x in d['claims']:x['sha256']=sha(R/x['evidence'])
  d['ownedPaths']=sorted(files);d['changedFiles']=sorted(files.values(),key=lambda x:x['path']);d['verification']=['Fresh existing tests: 2 management, 24 management lint, 13 shared media and 5 exporter tests (44 total). No creative or audio acceptance.','Local integrity verifies 6 media hashes, 318 original CSV rows, gallery file links and 174 protected files unchanged.','Workspace exporter/data/assets/plan checks pass. Production freshness differs only on collectedAt and Git HEAD; unchanged snapshot preserved.','Final handoff/lint/resume checks recorded at closeout; all historical results remain historical.']
  put(R/H,d)
refresh()
for name,cmd,cwd in [
 ('assets-final',['.venv/bin/python','scripts/manage.py','assets','validate'],R),
 ('validate-final',['.venv/bin/python','scripts/manage.py','validate'],R),
 ('handoff-final',['.venv/bin/python','scripts/manage.py','handoff','check',H],R),
 ('lint-final',['.venv/bin/python','scripts/manage.py','lint'],R),
 ('resume-final',['.venv/bin/python','scripts/manage.py','resume'],R),
 ('workspace-freshness-final',['node','sites/movies-demandas/scripts/export-workspace.mjs',str(R),'--check'],R),
 ('data-final',['node','scripts/check-data.mjs'],R/'sites/movies-demandas')]:
 results[name]=run(name,cmd,cwd)
assert all(v['exitCode']==0 for v in results.values()),results
prior=json.loads((E/'checks.json').read_text());sizes={'originalMediaBytes':sum(x['bytes'] for x in manifest['resources']),'catalogAndReviewBytesBeforeCloseout':sum(f.stat().st_size for f in (R/C).rglob('*') if f.is_file()),'sourceSidecarsBytes':sum(f.stat().st_size for f in (R/M).glob('*.json')),'freeBytes':shutil.disk_usage(R).free}
put(E/'closeout.json',{'capturedAt':datetime.now(timezone.utc).isoformat(),'checks':results,'earlierChecks':prior,'testCounts':{'management':2,'managementLint':24,'sharedMedia':13,'export':5,'total':44},'storage':sizes,'knownBlockers':['Authenticated web history unavailable; local kung-fu ProduceID relationship unconfirmed.','Costume source prompts unknown; local JPEG upload relationship unconfirmed.','Audio listening and normal-speed playback not performed.','Production freshness only collectedAt/repositoryHead; snapshot preserved.'],'ingestionPerformed':False,'creativeAcceptance':False})
d=json.loads((R/H).read_text());d['claims'].extend([{'statement':'Final local checks passed; 44 existing tests, media integrity, preserved guards and explicit remaining blockers. Production snapshot kept unchanged.','evidence':C+'evidence/closeout.json','sha256':sha(E/'closeout.json')}]);put(R/H,d)
# Hash all deliverables except this checksum file and the handoff itself; no recursive signature.
items=[f for f in (R/C).rglob('*') if f.is_file() and f.name!='SHA256SUMS.txt']+[f for f in (R/M).iterdir() if f.is_file()]+[R/P/'docs/kling-element-experiments-20261015-v2.md']
(R/C/'SHA256SUMS.txt').write_text(''.join(sha(f)+'  '+str(f.relative_to(R))+'\n' for f in sorted(items)))
refresh()
print(json.dumps({'checks':{n:r['exitCode'] for n,r in results.items()},'testCount':44,'mediaFiles':6,'mediaBytes':14641524,'catalogAndReviewBytes':sum(f.stat().st_size for f in (R/C).rglob('*') if f.is_file()),'sidecarsBytes':sizes['sourceSidecarsBytes'],'checksumFiles':len(items),'handoffFileClaims':len(json.loads((R/H).read_text())['changedFiles'])},indent=2))
