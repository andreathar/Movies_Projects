#!/usr/bin/env python3
"""Validate and export the visual plan selected by workspace.json, entirely offline.

The board owns task status; this source owns shot proposals and references. Provider
receipts and credit-ledger.csv remain the job/accounting sources. Derived views do
not grant creative acceptance, paid release or current account access.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = 'docs/kling-manual/snapshots/who_am_i.sanitized.json'
FAMILIES = 'shared/templates/kling-shot-families.json'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def safe(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or '\\' in relative or '..' in Path(relative).parts:
        raise ValueError('caminho relativo inseguro: ' + str(relative))
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('fonte fora do workspace: ' + relative)
    return path


def read(root, path):
    return json.loads(safe(root, path).read_text(encoding='utf-8'))


def project(root):
    workspace = read(root, 'workspace.json')
    return next(p for p in workspace['projects'] if p['id'] == workspace['activeFilm'])


def plan_source(root):
    p = project(root)
    path = p.get('productionPlan')
    return (p, path, read(root, path)) if path else (p, None, None)


def routes(root):
    snapshot = read(root, SNAPSHOT)
    result = []
    for tool, group in snapshot['body']['availableModels'].items():
        for model in group['models']:
            args = model.get('arguments', [])
            names = {a['name'] for a in args}
            result.append({'tool': tool, 'model': model['model'],
                           'inputs': [i['name'] for i in model.get('inputs', [])],
                           'requiredInputs': [i['name'] for i in model.get('inputs', []) if i.get('required')],
                           'parameters': [{'name': a['name'], 'required': bool(a.get('required')),
                                           'allowedValues': a.get('allowedValues', []), 'default': a.get('default')}
                                          for a in args if a['name'] not in {'prompt', 'elements'}],
                           'elements': 'elements' in names, 'audioControl': 'enable_audio' in names,
                           'externalAudio': any(i['name'].startswith('audio') for i in model.get('inputs', [])),
                           'multiShotControl': 'prefer_multi_shots' in names,
                           'combinedCaps': ([model['combinedItemCap']] if model.get('combinedItemCap') else []) + model.get('combinedItemCaps', []),
                           'elementSupport': model.get('elementSupport', {}),
                           'notes': route_notes(tool, model['model'])})
    return {'snapshotPath': SNAPSHOT, 'snapshotSha256': sha(safe(root, SNAPSHOT)),
            'status': 'dated_snapshot_not_live', 'routes': result}


def route_notes(tool, model):
    notes = ['Disponibilidade e preço atuais requerem consulta antes de execução.']
    if model == 'kling-video-v3_0_turbo':
        notes.append('Sem Elements, cauda ou controle explícito de áudio nesta rota; ausência do controle não garante silêncio.')
    if tool == 'omni_ref_video':
        notes.append('Com video_1: imagens + Elements ≤4; sem vídeo ≤7. Referência de vídeo: 3–10 s, 720–2160 px, 24–60 fps, até 200 MiB. Sem áudio independente.')
        if model == 'kling-video-v3_0_omni':
            notes.append('video_1 exige enable_audio=false. Element de vídeo não equivale a vídeo direto; com vídeo direto, só um Element de vídeo e nenhuma imagem/Element de imagem.')
    if tool == 'motion_control':
        notes.append('Uma fonte: video ou motionId. Medir referência; motion_direction acompanha sua duração. image_direction: 3–10 s. Vínculo facial v3 limitado a um Element e direção do vídeo.')
    if tool == 'image_to_video' and model == 'kling-video-v2_6':
        notes.append('Cauda exige 1080p. Áudio exige 1080p sem cauda.')
    if tool == 'image_to_video' and model == 'kling-video-v3_0_omni':
        notes.append('Somente imagens nesta rota. O rótulo first-tail não declara slot tail_image; não inventar cauda.')
    return notes


def acyclic(items, key='id', dependencies='dependsOn'):
    ids = {item[key]: item for item in items}
    if len(ids) != len(items):
        raise ValueError('IDs duplicados')
    done = set()
    def visit(identifier, trail):
        if identifier not in ids:
            raise ValueError('dependência ausente: ' + identifier)
        if identifier in trail:
            raise ValueError('dependência cíclica: ' + identifier)
        if identifier in done:
            return
        for dep in ids[identifier].get(dependencies, []):
            visit(dep, trail | {identifier})
        done.add(identifier)
    for identifier in ids:
        visit(identifier, set())
    return ids


def review_hash(item):
    if item.get('path') and item.get('sha256'):
        return item['sha256']
    content = {k: v for k, v in item.items() if k not in {'states', 'approvalEvidence'}}
    return hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def check_states(item, root, errors):
    states = item.get('states', {})
    enums = {'proposal': {'draft', 'proposed'}, 'technicalCheck': {'pending', 'static_checked', 'checked', 'failed'},
             'directorApproval': {'pending', 'approved', 'rejected'}, 'incorporation': {'not_incorporated', 'incorporated'}}
    for key, values in enums.items():
        if states.get(key) not in values:
            errors.append(f"{item['id']}: estado inválido {key}")
    if states.get('directorApproval') == 'approved':
        decision_ref = item.get('approvalEvidence')
        try:
            if not decision_ref or sha(safe(root, decision_ref['path'])) != decision_ref['sha256']:
                raise ValueError('aprovação sem evidência exata')
            decision = read(root, decision_ref['path'])
            if decision.get('decision') != 'approved' or decision.get('artifact', {}).get('sha256') != review_hash(item) or not decision.get('scope') or not decision.get('reviewer'):
                raise ValueError('aprovação não corresponde ao artefato/uso')
            if not item.get('path') and decision.get('artifact', {}).get('selector') != item['id']:
                raise ValueError('aprovação de ficha exige selector com o ID exato')
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"{item['id']}: {exc}")
    if states.get('incorporation') == 'incorporated' and states.get('directorApproval') != 'approved':
        errors.append(f"{item['id']}: incorporação artística requer aprovação específica")


def validate(root, *, verify_media=False):
    errors, pending = [], []
    p, path, plan = plan_source(root)
    if not plan:
        return {'status': 'not_configured', 'errors': [], 'pending': [], 'path': None}
    try:
        if plan['kind'] != 'film_visual_production_plan' or plan['production'] != p['id']:
            raise ValueError('plano incompatível')
        film = safe(root, p['root'])
        board = read(root, p['tasks'])
        task_ids = {t['id'] for t in board['tasks']}
        manifest = read(root, p['manifest'])
        if plan['encounters'] != [c['id'] for c in manifest['chapters']]:
            errors.append('cinco encontros diferem do manifesto preservado')
        if plan['constraints'].get('historicalFullFaceFrames') != 0 or plan['constraints'].get('finalVoicePolicy') != 'D14_guide_only_until_separate_approval':
            errors.append('restrições de rosto/voz divergiram')
        for source in plan['preservedSources']:
            if sha(safe(root, source['path'])) != source['sha256']:
                errors.append('fonte preservada mudou: ' + source['path'])
        approvals = read(root, p['root'] + '/00_brief/approvals.json')['approvals']
        if not any(a.get('id') == plan['implementationApprovalId'] and a.get('kind') == 'local_plan_implementation' for a in approvals):
            errors.append('implementação sem referência de escopo')
        stages = acyclic(plan['stages'])
        refs = acyclic(plan['references'])
        shots = acyclic(plan['shots'])
        families = {f['id']: f for f in read(root, FAMILIES)['families']}
        with (film / '01_script/dialogue-lines.csv').open(newline='', encoding='utf-8') as stream:
            lines = {row['line_id']: row for row in csv.DictReader(stream)}
        for stage in stages.values():
            if not set(stage['taskIds']) <= task_ids or not stage.get('owner'):
                errors.append(stage['id'] + ': tarefa/dono ausente')
        for ref in refs.values():
            check_states(ref, root, errors)
            if verify_media and sha(safe(root, ref['path'])) != ref['sha256']:
                errors.append('referência mudou: ' + ref['id'])
        for shot in shots.values():
            check_states(shot, root, errors)
            if shot['encounter'] not in plan['encounters'] or shot['family'] not in families or shot['taskId'] not in task_ids:
                errors.append(shot['id'] + ': vínculo de encontro/template/tarefa inválido')
            if not set(shot['referenceIds']) <= refs.keys():
                errors.append(shot['id'] + ': referência ausente')
            for line in shot['lineIds']:
                if line not in lines:
                    errors.append(shot['id'] + ': fala ausente ' + line)
            if not shot.get('submissionBlocked'):
                errors.append(shot['id'] + ': proposta não pode ser liberação de submissão')
            pending.extend({'shotId': shot['id'], **b} for b in shot.get('blockers', []))
        timeline = plan['pilot']['timeline']
        end = 0.0
        for segment in timeline:
            if segment['referenceId'] not in refs or segment['endSeconds'] <= segment['startSeconds'] or abs(segment['startSeconds'] - end) > .001:
                errors.append('timeline tem lacuna, sobreposição ou referência ausente')
            end = segment['endSeconds']
        for audio in plan['pilot']['audio']:
            line = lines[audio['lineId']]
            if audio['path'] != p['root'] + '/' + line['audio_path'] or audio['rate'] != 1:
                errors.append('áudio divergente ou acelerado: ' + audio['lineId'])
            if verify_media and sha(safe(root, audio['path'])) != audio['sha256']:
                errors.append('áudio mudou: ' + audio['lineId'])
            if audio['startSeconds'] + audio['durationSeconds'] > end:
                errors.append('áudio ultrapassa corte')
        cause = next(a for a in plan['pilot']['audio'] if a['lineId'] == 'G-L04')
        reaction = next(t for t in timeline if t.get('reactionTo') == 'G-L04')
        if reaction['startSeconds'] < cause['startSeconds'] + cause['durationSeconds']:
            errors.append('reação antecede o fim da fala motivadora; alinhamento por palavra ainda não revisado')
        # Validate actual template field names/enums against the same preflight used by the runner.
        pf = module('plan_preflight', ROOT / 'docs/kling-manual/tools/kling_preflight.py')
        models = read(root, SNAPSHOT)['body']['availableModels']
        for family in families.values():
            request = copy.deepcopy(family['request'])
            request.update(job='OFFLINE-' + family['id'], prompt='Offline fixture. No generation.', auth='fixture')
            request.pop('submissionBlocked', None)
            report = pf.check_job(request, models, str(film), str(film), True)
            # Unresolved local refs are intentional; schema mistakes are not.
            blocking = [x for x in report.items if x['level'] == 'ERROR' and x['code'] not in {'VIDEO_FACTS_REQUIRED'}]
            errors.extend(family['id'] + ': ' + x['code'] for x in blocking)
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as exc:
        errors.append(str(exc))
    return {'status': 'error' if errors else 'ok', 'errors': errors, 'pending': pending,
            'path': path, 'mediaHashesVerified': verify_media, 'creativeAcceptanceGranted': False}


def template(root, family_id, shot_id=None):
    family = next(f for f in read(root, FAMILIES)['families'] if f['id'] == family_id)
    request = copy.deepcopy(family['request'])
    request['job'] = 'PROPOSAL-' + (shot_id or family_id)
    request['auth'] = None
    request['submissionBlocked'] = 'Proposta local: referências, revisão criativa, cotação e liberação específica pendentes.'
    request['prompt'] = family['promptTemplate']
    if shot_id:
        p, _, plan = plan_source(root)
        shot = next(s for s in plan['shots'] if s['id'] == shot_id)
        if shot['family'] != family_id:
            raise ValueError('família não corresponde à ficha')
        with safe(root, p['root'] + '/01_script/dialogue-lines.csv').open(newline='', encoding='utf-8') as stream:
            lines = {row['line_id']: row['text_en'] for row in csv.DictReader(stream)}
        request['prompt'] = request['prompt'].replace('{canonical_dialogue}', ' '.join(lines[i] for i in shot['lineIds']))
        if 'duration' in request['args'] and shot.get('proposedGenerationSeconds'):
            request['args']['duration'] = str(shot['proposedGenerationSeconds'])
    return request


def export(root):
    report = validate(root)
    if report['errors']:
        raise ValueError('; '.join(report['errors']))
    p, path, plan = plan_source(root)
    if not plan:
        return None
    capability = routes(root)
    source_paths = [path, FAMILIES, SNAPSHOT, 'scripts/production_plan.py', 'scripts/kling_release.py', 'docs/kling-manual/tools/kling_preflight.py', 'docs/PRODUCTION_PLAN.md'] + [s['path'] for s in plan['preservedSources']]
    for evidence in plan.get('deliverables', []):
        source_paths.append(evidence)
    return {'path': path, 'revision': plan['revision'], 'implementationApprovalId': plan['implementationApprovalId'],
            'status': 'local_implementation_prepared_creative_review_pending',
            'boardIsTaskAuthority': True, 'encounters': plan['encounters'], 'stages': plan['stages'],
            'references': [{k: r[k] for k in ('id', 'label', 'path', 'sha256', 'role', 'provenance', 'selection', 'states', 'notes')} for r in plan['references']],
            'shots': plan['shots'], 'pilot': plan['pilot'], 'constraints': plan['constraints'],
            'capabilities': capability, 'costPolicy': plan['costPolicy'], 'blockers': plan['blockers'],
            'families': [{k: f[k] for k in ('id', 'title', 'purpose', 'requiredDecisions')} for f in read(root, FAMILIES)['families']],
            'sourceVersions': [{'path': name, 'sha256': sha(safe(root, name))} for name in dict.fromkeys(source_paths)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('command', choices=['check', 'export', 'routes', 'jobs', 'template', 'check-request', 'review-hashes'])
    parser.add_argument('--verify-media', action='store_true')
    parser.add_argument('--family')
    parser.add_argument('--shot')
    parser.add_argument('--spec', type=Path)
    args = parser.parse_args()
    if args.command == 'check':
        result = validate(args.root, verify_media=args.verify_media)
    elif args.command == 'export':
        result = export(args.root)
    elif args.command == 'routes':
        result = routes(args.root)
    elif args.command == 'jobs':
        release = module('plan_release', ROOT / 'scripts/kling_release.py')
        result = release.registry(safe(args.root, project(args.root)['root']))
    elif args.command == 'review-hashes':
        _, _, plan = plan_source(args.root)
        result = [{'id': item['id'], 'sha256': review_hash(item), 'hashScope': 'file' if item.get('path') else 'shot_content'} for item in plan['references'] + plan['shots']]
    elif args.command == 'check-request':
        if not args.spec:
            parser.error('check-request exige --spec')
        job = json.loads(args.spec.read_text())
        if isinstance(job, list):
            if len(job) != 1:
                parser.error('check-request aceita exatamente um pedido')
            job = job[0]
        pf = module('request_preflight', ROOT / 'docs/kling-manual/tools/kling_preflight.py')
        release = module('request_release', ROOT / 'scripts/kling_release.py')
        film = safe(args.root, project(args.root)['root'])
        models = read(args.root, SNAPSHOT)['body']['availableModels']
        check = pf.check_job(job, models, str(film), str(film), False)
        result = {'errors': [i for i in check.items if i['level'] == 'ERROR'], 'items': check.items, 'schemaSha256': hashlib.sha256(json.dumps(models, sort_keys=True).encode()).hexdigest(), 'payloadSha256': None, 'paidReleaseGranted': False}
        if not result['errors']:
            result['payloadSha256'] = release.fingerprint(film, job)
    else:
        if not args.family:
            parser.error('template exige --family')
        result = template(args.root, args.family, args.shot)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if isinstance(result, dict) and result.get('errors') else 0


if __name__ == '__main__':
    raise SystemExit(main())
