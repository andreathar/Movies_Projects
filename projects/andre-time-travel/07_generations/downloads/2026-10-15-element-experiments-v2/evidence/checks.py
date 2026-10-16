import concurrent.futures, hashlib, html.parser, json, os, subprocess, urllib.parse
from pathlib import Path
R=Path('/mnt/data/Projects_SSD/Movies_Projects');P='projects/andre-time-travel/';C=P+'07_generations/downloads/2026-10-15-element-experiments-v2/';E=R/C/'evidence';T=Path('/tmp/kling-batch2-20261015')
H=P+'agents/handoffs/2026-10-15-kling-element-experiments-v2-reconciliation.json'
env=dict(os.environ,TMPDIR='/tmp',PYTHONDONTWRITEBYTECODE='1')
commands={
 'assets':['.venv/bin/python','scripts/manage.py','assets','validate'],
 'validate':['.venv/bin/python','scripts/manage.py','validate'],
 'handoff':['.venv/bin/python','scripts/manage.py','handoff','check',H],
 'lint':['.venv/bin/python','scripts/manage.py','lint'],
 'resume':['.venv/bin/python','scripts/manage.py','resume'],
 'plan-media':['.venv/bin/python','scripts/production_plan.py','check','--verify-media'],
 'management-tests':['.venv/bin/python','-m','unittest','discover','-s','tests','-p','test_manage.py'],
 'shared-media-tests':['.venv/bin/python','-m','unittest','discover','-s','tests','-p','test_shared_media.py'],
 'export-tests':['node','--test','sites/movies-demandas/tests/export.test.mjs'],
 'workspace-freshness':['node','sites/movies-demandas/scripts/export-workspace.mjs',str(R),'--check'],
 'data-check':['node','sites/movies-demandas/scripts/check-data.mjs'],
 'production-freshness':['node','sites/movies-demandas/scripts/export-production.mjs',str(R),'--check'],
}
def run(item):
 name,cmd=item
 cwd=R/'sites/movies-demandas' if name=='data-check' else R
 if name=='data-check':cmd=['node','scripts/check-data.mjs']
 p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=120)
 (E/(name+'.stdout')).write_text(p.stdout);(E/(name+'.stderr')).write_text(p.stderr)
 return name,dict(command=cmd,exitCode=p.returncode,stdoutFile=name+'.stdout',stderrFile=name+'.stderr')
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=dict(pool.map(run,commands.items()))
# Read-only file-link verification, no service/public exposure.
class Links(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  self.links.extend(v for k,v in attrs if k in ('src','href'))
parser=Links();parser.feed((R/C/'index.html').read_text());missing=[]
for link in parser.links:
 if not urllib.parse.urlsplit(link).scheme and not (R/C/link).exists():missing.append(link)
assert not missing,missing
resources=json.loads((R/C/'manifest.json').read_text())['resources']
for x in resources:assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
before=(E/'integration-before/asset-registry.csv').read_bytes();after=(R/P/'asset-registry.csv').read_bytes();assert after.startswith(before)
results['local-integrity']={'exitCode':0,'galleryLinksChecked':len(parser.links),'missingLinks':missing,'newMediaRehashed':len(resources),'oldRegistryBytesPreserved':len(before)}
(E/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({n:r['exitCode'] for n,r in results.items()},indent=2))
for n,r in results.items():
 if r['exitCode'] and n!='production-freshness':print(n,(E/(n+'.stderr')).read_text()[-2000:],(E/(n+'.stdout')).read_text()[-3000:])
