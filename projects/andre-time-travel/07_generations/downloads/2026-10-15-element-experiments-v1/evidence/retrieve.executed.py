import csv,datetime,hashlib,json,pathlib,shutil,urllib.request,urllib.error
ROOT=pathlib.Path('/mnt/data/Projects_SSD/Movies_Projects')
TMP=pathlib.Path('/tmp/kling-study-20261015')
STORE=ROOT/'projects/andre-time-travel/07_generations/originals/kling-experiments-20261015-v1'
CAT=ROOT/'projects/andre-time-travel/asset-registry.csv'
MAX=300*1024**2
assert shutil.disk_usage(ROOT).free>MAX+2*1024**3
entries=[]
for eid in ['324018220506771','323980733525179','323867570654831','323854711683871']:
 e=json.loads((TMP/f'element_get-{eid}.json').read_text())['body']; res=e['resource']
 for role,u in res.items():
  if role=='secondary':
   for i,s in enumerate(u):entries.append(dict(asset_id=f'KEXP-E{eid}-secondary-{i+1}',elementId=eid,referenceName=e['name'],resourceName=s['name'],url=s['url'],role='secondary',quality='provider_original_resource'))
  else:entries.append(dict(asset_id=f'KEXP-E{eid}-{role}',elementId=eid,referenceName=e['name'],resourceName=role,url=u,role=role,quality='provider_original_resource'))
for web_id,stem in [('323869015528491','6594ad9e-275a-49f7-bafb-86ff5c37f9a0-lOOnFi5GnZekGcPTPJvXbQ'),('323868230505094','5b73de17-dcb1-44b3-a5f9-6d0f0e84990e-OJgen8T99rGpK7yc5NUWaw')]:
 entries.append(dict(asset_id=f'KEXP-W{web_id}-result',webHistoryId=web_id,generationId=None,role='result',resourceName=stem+'-output.mp4',url=f'https://v15-kling.klingai.com/bs2/upload-ylab-stunt-sgp/{stem}-output.mp4?x-kcdn-pid=112372',quality='observed_web_result_originality_unverified'))
if (TMP/'extra.json').exists():entries.extend(json.loads((TMP/'extra.json').read_text()))
hashes={}
for row in csv.DictReader(CAT.open()):
 if row['path_base'] in ('workspace','film') and row['sha256']:
  path=ROOT/('projects/andre-time-travel/' if row['path_base']=='film' else '')/row['path_or_provider_id']
  hashes.setdefault(row['sha256'],path)
# Find local uploaded source files before any transfer (size-index candidates verified after response).
local_sizes={}
for base in [ROOT/'inbox',ROOT/'projects/andre-time-travel',ROOT/'outputs']:
 if base.exists():
  for f in base.rglob('*'):
   if f.is_file() and f.suffix.lower() in ('.png','.jpg','.jpeg','.webp','.mp4','.mp3'):
    local_sizes.setdefault(f.stat().st_size,[]).append(f)
STORE.mkdir(parents=True,exist_ok=True)
previous=json.loads((TMP/'retrieval.json').read_text()) if (TMP/'retrieval.json').exists() else dict(records=[],transferBytes=0)
used=previous['transferBytes'];byurl={r['url']:{k:r[k] for k in ['path','sha256','bytes','contentType','retrieval','retrievedAt']} for r in previous['records'] if 'path' in r};report=previous['records']
for rec in entries:
 if any(r['asset_id']==rec['asset_id'] for r in report):continue
 try:
  if rec['url'] in byurl:
   rec.update(byurl[rec['url']]);rec['retrieval']='duplicate_url_reused';report.append(rec);continue
  cap=150*1024**2 if rec['url'].split('?')[0].endswith('.mp4') else 40*1024**2
  req=urllib.request.Request(rec['url'])
  with urllib.request.urlopen(req,timeout=45) as response:
   content_type=response.headers.get('Content-Type','');length=int(response.headers.get('Content-Length','0'))
   assert length<=cap and used+length<=MAX,'storage transfer bound exceeded'
   payload=response.read(min(cap,MAX-used)+1)
  assert len(payload)<=cap and used+len(payload)<=MAX,'actual transfer bound exceeded'
  used+=len(payload);h=hashlib.sha256(payload).hexdigest();existing=hashes.get(h)
  if existing is None:
   for candidate in local_sizes.get(len(payload),[]):
    if hashlib.sha256(candidate.read_bytes()).hexdigest()==h:existing=candidate;break
  if existing is not None:
   assert hashlib.sha256(existing.read_bytes()).hexdigest()==h,'existing hash drift'
   target=existing;retrieval='already_local_hash_reused'
  else:
   ext='.png' if payload.startswith(b'\x89PNG') else '.jpg' if payload.startswith(b'\xff\xd8') else '.webp' if payload[:4]==b'RIFF' else '.mp4' if b'ftyp' in payload[:32] else '.mp3' if payload[:3]==b'ID3' or content_type.startswith('audio/') else '.bin'
   assert ext!='.bin','unknown media format'
   target=STORE/(rec['asset_id']+ext)
   with target.open('xb') as out:out.write(payload)
   retrieval='downloaded'
  hashes[h]=target
  fields=dict(path=str(target.relative_to(ROOT)),sha256=h,bytes=len(payload),contentType=content_type,retrieval=retrieval,retrievedAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
  byurl[rec['url']]=fields;rec.update(fields)
 except Exception as exc:
  rec['retrieval']='unavailable';rec['error']=f'HTTP {exc.code}' if isinstance(exc,urllib.error.HTTPError) else type(exc).__name__+': '+str(exc).split('http')[0][:160]
 report.append(rec)
 (TMP/'retrieval.json').write_text(json.dumps(dict(transferBytes=used,storageBudgetBytes=MAX,records=report),ensure_ascii=False,indent=2)+'\n')
 print(rec['asset_id'],rec['retrieval'],rec.get('bytes'),flush=True)
