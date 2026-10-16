#!/usr/bin/env python3
"""Derive metadata and inactive reviewer adapters. No client configuration writes."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REVIEWERS = ('historian', 'continuity', 'qc')

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def encoded(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()

def local(root, path):
    p = Path(path)
    if p.is_absolute() or '..' in p.parts or '\\' in path:
        raise ValueError(f'Unsafe path: {path}')
    target = root / p
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path outside workspace: {path}')
    return target

def unique(items, key):
    ids = [i[key] for i in items]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', i) for i in ids):
        raise ValueError(f'Duplicate or invalid {key}')
    return set(ids)

def mission(text):
    match = re.search(r'^## (?:Mission|Missão)\s*\n(.*?)(?=\n## |\Z)', text, re.M | re.S)
    if not match or not match[1].strip():
        raise ValueError('Role brief needs a Mission section')
    return ' '.join(match[1].split())

def skill_description(text):
    match = re.search(r'^description:\s*(.*)$', text, re.M)
    if match:
        value = match[1].strip().strip('\"\'')
        if value not in ('>', '|', '>-', '|-'):
            return value
        block = text[match.end():].split('\n---', 1)[0]
        return ' '.join(line.strip() for line in block.splitlines() if line.startswith('  '))
    return next((line.lstrip('# ').strip() for line in text.splitlines() if line.startswith('# ')), 'Procedimento registrado')

def render(root):
    root = Path(root).resolve()
    sources = []
    def read(path):
        raw = local(root, path).read_bytes()
        sources.append({'path': path, 'sha256': digest(raw)})
        return raw.decode()
    read('AGENTS.md')
    agents = json.loads(read('agents/registry.json'))
    registry = json.loads(read('skills/registry.json'))
    role_ids = unique(agents['roles'], 'id')
    skill_ids = unique(registry['skills'], 'name')
    if not set(REVIEWERS) <= role_ids:
        raise ValueError('Missing reviewer role')
    skills = []
    for s in registry['skills']:
        if not re.fullmatch(r'skills/[a-z0-9-]+', s['path']):
            raise ValueError('Invalid skill path')
        target = root / s['path'] / 'SKILL.md'
        # Only registry-declared shared roots may resolve outside the workspace.
        if s['type'] == 'machine_local_symlink':
            if not Path(s['source']).is_absolute() or target.resolve() != (Path(s['source'])/'SKILL.md').resolve():
                raise ValueError(f'Skill link differs from registered source: {s["name"]}')
        else:
            local(root, s['path']+'/SKILL.md')
            if s['type'] == 'project_vendored' and target.resolve() != local(root, s['source']+'/SKILL.md').resolve():
                raise ValueError('Vendored skill source mismatch')
        raw = target.read_bytes()  # Broken links and absent sources must fail.
        if b'placeholder' in raw[:250].lower():
            raise ValueError(f'Placeholder is not a skill: {s["name"]}')
        actual = digest(raw)
        sources.append({'path': s['path']+'/SKILL.md', 'sha256': actual})
        skills.append({'id': s['name'], 'title': s['name'], 'description': re.split(r'(?<=\.)\s+', skill_description(raw.decode()), maxsplit=1)[0],
            'path': s['path']+'/SKILL.md', 'kind': 'linked' if s['type']=='machine_local_symlink' else 'project',
            'sourceType': s['type'], 'effectiveSource': s['source'] if s['type']=='project_vendored' else s['path'], 'sha256': actual, 'registeredHashMatches': actual == s.get('sourceSha256', actual),
            'available': True, 'roles': [r['id'] for r in agents['roles'] if s['name'] in r['skills']]})
    roles, outputs = [], {}
    for r in agents['roles']:
        if len(r['skills']) != len(set(r['skills'])) or not set(r['skills']) <= skill_ids:
            raise ValueError(f'Unknown or duplicate skill reference: {r["id"]}')
        brief = read(r['brief'])
        summary = mission(brief)
        roles.append({**{k: r[k] for k in ('id','name','brief','skills')}, 'summary': summary,
            **{k: r.get(k,False) for k in ('dispatchAuthority','paidSubmissionAuthority','creativeDecisionAuthority')}})
        if r['id'] not in REVIEWERS:
            continue
        if r.get('paidSubmissionAuthority') or r.get('dispatchAuthority') or r.get('creativeDecisionAuthority'):
            raise ValueError('Reviewer adapter would grant authority')
        prompt = ('Generated from '+r['brief']+'; do not edit this adapter.\n'
            'Read workspace AGENTS.md and the exact assignment before work. This adapter is for findings-only review. '
            'Return evidence to the parent; do not edit files, dispatch, spend, submit jobs, or approve production. '
            'If the assignment needs unavailable tools, report the limitation. This text is an operating rule, not a security boundary.\n\n'+brief)
        name = 'movies-'+r['id']
        outputs[f'agents/generated/claude/{name}.md'] = ('---\nname: '+name+'\ndescription: '+json.dumps(summary)+'\ntools: Read, Glob, Grep\n---\n\n'+prompt).encode()
        outputs[f'agents/generated/codex/{name}.toml'] = ('# PREPARED ONLY: discovery and activation not verified.\nname = '+json.dumps(name)+'\ndescription = '+json.dumps(summary)+'\ndeveloper_instructions = '+json.dumps(prompt)+'\n').encode()
    catalog = {'schemaVersion':1, 'sources':sources, 'skills':skills, 'roles':roles,
        'automaticSkillDiscovery':registry.get('automaticProjectDiscoveryConfigured',False),
        'coordinateRegistered':'coordinate' in skill_ids,
        'adapters':{'status':'prepared_activation_pending', 'roles':list(REVIEWERS),
            'artifacts':[{'path':p,'sha256':digest(b)} for p,b in outputs.items()],
            'runtimeVerified':False}}
    outputs['agents/generated/catalog.json'] = encoded(catalog)
    return outputs

def sync(root, check=False):
    outputs = render(root)  # Fully validate before writing any output.
    differences = [p for p,b in outputs.items() if not local(root,p).is_file() or local(root,p).read_bytes()!=b]
    if check and differences:
        raise ValueError('Generated catalog/adapters drift: '+', '.join(differences))
    for p in differences:
        dest = local(root,p); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(outputs[p])
    return {'status':'ok','files':len(outputs),'changed':differences,'activation':'pending'}

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try:
        print(json.dumps(sync(args.root,args.check)))
    except (ValueError,KeyError,OSError) as error:
        print(str(error),file=sys.stderr); sys.exit(2)
