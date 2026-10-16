import pathlib,json,csv,hashlib,urllib.request,urllib.error,shutil,datetime
R=pathlib.Path('/mnt/data/Projects_SSD/Movies_Projects');T=pathlib.Path('/tmp/kling-batch2-20261015');S=R/'projects/andre-time-travel/07_generations/originals/kling-experiments-20261015-v2'
e=json.loads((T/'element_get-324019350521447.json').read_text())['body'];assert e['id']=='324019350521447';assert shutil.disk_usage(R).free>1024**3
entries=[dict(asset_id='KEXP2-E324019350521447-cover',resourceName='cover',url=e['resource']['cover'])]+[dict(asset_id='KEXP2-E324019350521447-secondary-'+str(i+1),resourceName=x['name'],url=x['url']) for i,x in enumerate(e['resource']['secondary'])]
existing={}
for x in csv.DictReader((R/'projects/andre-time-travel/asset-registry.csv').open()):
 if x['path_base'] in ('workspace','film') and x['sha256']:existing[x['sha256']]=R/('projects/andre-time-travel/' if x['path_base']=='film' else '')/x['path_or_provider_id']
S.mkdir(exist_ok=False);report=[];total=0
for x in entries:
 x.update(elementId=e['id'],originalName=e['name'],quality='provider_original_resource',sourcePrompt=None,sourcePromptGap='element_get exposes reference resources and description, not their source generation prompts',approved=False)
 try:
  assert x['url'].startswith('https://')
  with urllib.request.urlopen(x['url'],timeout=45) as resp:
   assert int(resp.headers.get('Content-Length','0'))<40*1024**2
   data=resp.read(40*1024**2+1);ct=resp.headers.get('Content-Type','')
  total+=len(data);assert len(data)<=40*1024**2 and total<=100*1024**2
  h=hashlib.sha256(data).hexdigest();f=existing.get(h)
  if f:assert hashlib.sha256(f.read_bytes()).hexdigest()==h;x['retrieval']='already_local_hash_reused'
  else:
   ext='.png' if data.startswith(b'\x89PNG') else '.jpg' if data.startswith(b'\xff\xd8') else None;assert ext
   f=S/(x['asset_id']+ext)
   with f.open('xb') as out:out.write(data)
   x['retrieval']='downloaded'
  x.update(path=str(f.relative_to(R)),sha256=h,bytes=len(data),contentType=ct,retrievedAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as err:x.update(retrieval='unavailable',error='HTTP '+str(err.code) if isinstance(err,urllib.error.HTTPError) else type(err).__name__)
 report.append(x);print(x['asset_id'],x['retrieval'],x.get('bytes'),flush=True)
 (T/'retrieval.json').write_text(json.dumps(dict(records=report,transferBytes=total,budgetBytes=100*1024**2),ensure_ascii=False,indent=2)+'\n')
