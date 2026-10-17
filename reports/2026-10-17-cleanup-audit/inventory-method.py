import os, json, hashlib, collections, pathlib, subprocess
root=pathlib.Path('/mnt/data/Projects_SSD/Movies_Projects')
out=root/'reports/2026-10-17-cleanup-audit'
out.mkdir(exist_ok=True)
skip={'.git','.venv','node_modules','__pycache__','.mypy_cache','.ruff_cache','.serena','.sites-runtime','.wrangler','.vllm'}
rows=[]; links=[]
for base,dirs,files in os.walk(root,followlinks=False):
    dirs[:]=[d for d in dirs if d not in skip]
    for name in list(dirs)+files:
        p=pathlib.Path(base)/name; rel=p.relative_to(root).as_posix()
        if p.is_symlink():
            links.append({'path':rel,'target':os.readlink(p),'resolves':p.exists()}); continue
        if not p.is_file() or name.startswith('.env'): continue
        st=p.stat(); rows.append({'path':rel,'bytes':st.st_size,'suffix':p.suffix.lower()})
media={'.jpg','.jpeg','.png','.webp','.mp4','.mov','.wav','.mp3','.m4a','.flac','.pdf'}
sizes=collections.defaultdict(list)
for row in rows:
    if row['suffix'] in media and row['bytes']>0: sizes[row['bytes']].append(row)
groups=[]
for size, rr in sizes.items():
    if len(rr)<2: continue
    hashes=collections.defaultdict(list)
    for row in rr:
        h=hashlib.sha256()
        with (root/row['path']).open('rb') as f:
            for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
        hashes[h.hexdigest()].append(row['path'])
    for h, paths in hashes.items():
        if len(paths)>1: groups.append({'sha256':h,'bytesEach':size,'redundantBytesUpperBound':size*(len(paths)-1),'paths':paths})
groups.sort(key=lambda x:x['redundantBytesUpperBound'],reverse=True)
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0'); tracked=set(tracked)
summary={'scope':'Metadata inventory without symlink traversal. Content hashing restricted to same-size media/PDF candidates. No .env contents, runtime logs or databases read. Duplicate bytes do not authorize removal. Logical sizes, not allocated/hardlink-aware savings.','excludedDirectoryNames':sorted(skip),'inventoriedFiles':len(rows),'logicalBytes':sum(r['bytes'] for r in rows),'extensionCounts':dict(collections.Counter(r['suffix'] for r in rows)),'duplicateGroups':len(groups),'redundantBytesUpperBound':sum(g['redundantBytesUpperBound'] for g in groups),'brokenSymlinks':[l for l in links if not l['resolves']]}
for name,data in [('inventory.json',rows),('symlinks.json',links),('exact-duplicates.json',groups),('summary.json',summary)]:
    (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,indent=2)); print('TOP DUPLICATES'); print(json.dumps(groups[:12],indent=2))
