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
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = 'docs/kling-manual/snapshots/who_am_i.sanitized.json'
FAMILIES = 'shared/templates/kling-shot-families.json'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError('não foi possível carregar o módulo: ' + str(path))
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


def coherence_hash(shot, references, request=None):
    """Bind warning acknowledgements to this proposal, references and exact request."""
    content = copy.deepcopy(shot)
    if isinstance(content.get('coherence'), dict):
        content['coherence'].pop('overrides', None)
    evidence = {'shot': content, 'references': references, 'request': request}
    return hashlib.sha256(json.dumps(evidence, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


def cinematic_lint(shot, references, request=None, mapping=None):
    """Offline documentary checks, not a media inspector or a spending gate.

    Optional annotations live on the existing shot.coherence, never in a new registry.
    Free-text matches only warn: negation, language and intent are not reliably parsed.
    mapping, when supplied, comes from the existing preflight's media_mapping.
    """
    items = []
    def add(level, code, msg, evidence=None):
        items.append({'shotId': shot.get('id'), 'level': level, 'code': code,
                      'msg': msg, 'evidence': evidence, 'acknowledged': False})
    def seconds(value):
        try:
            return float(value) if not isinstance(value, bool) and math.isfinite(float(value)) else None
        except (TypeError, ValueError, OverflowError):
            return None
    def flag(value):
        return value if isinstance(value, bool) else {'true': True, 'false': False}.get(str(value).lower())

    meta = shot.get('coherence', {})
    if not isinstance(meta, dict):
        add('ERROR', 'COHERENCE_SHAPE', 'coherence deve ser objeto.'); return items
    total = seconds(shot.get('proposedGenerationSeconds'))
    if shot.get('proposedGenerationSeconds') is not None and (total is None or total <= 0):
        add('ERROR', 'DURATION_INVALID', 'Duração proposta deve ser finita e positiva.')
    args = (request or {}).get('args', {})
    args = args if isinstance(args, dict) else {}
    args = {re.sub(r'[_\-\s]', '', str(k)).lower(): v for k, v in args.items()}
    requested = seconds(args.get('duration'))
    if 'duration' in args and (requested is None or requested <= 0):
        add('ERROR', 'DURATION_INVALID', 'Duração do pedido deve ser finita e positiva.')
    if total is not None and requested is not None and abs(total - requested) > .001:
        add('ERROR', 'DURATION_REQUEST', 'Duração estruturada do pedido difere da ficha.',
            {'shot': total, 'request': requested})
    total = requested if requested is not None else total
    segments = meta.get('segments')
    modes, end, segments_ok = set(), 0.0, True
    if segments is not None:
        if not isinstance(segments, list) or not segments or total is None or total <= 0:
            add('ERROR', 'SEGMENTS_SHAPE', 'Segmentos exigem lista não vazia e duração total positiva.')
            segments_ok = False
        else:
            for index, segment in enumerate(segments):
                start = seconds(segment.get('startSeconds')) if isinstance(segment, dict) else None
                stop = seconds(segment.get('endSeconds')) if isinstance(segment, dict) else None
                mode = segment.get('camera') if isinstance(segment, dict) else None
                if start is None or stop is None or start < 0 or stop <= start or abs(start-end) > .001 or stop > total+.001 or not isinstance(mode, str) or mode not in {'locked', 'moving'}:
                    add('ERROR', 'SEGMENT_INTERVAL', 'Segmento inválido: ordem, lacuna, sobreposição, limite ou câmera.', index)
                    segments_ok = False
                if stop is not None:
                    end = stop
                if isinstance(mode, str):
                    modes.add(mode)
            if abs(end-total) > .001:
                add('ERROR', 'SEGMENTS_TOTAL', 'Segmentos devem cobrir a duração total.', {'end': end, 'total': total})
                segments_ok = False

    prompt = (request or {}).get('prompt', args.get('prompt', shot.get('prompt', '')))
    text = '\n'.join(str(x or '') for x in (shot.get('camera'), prompt))
    fixed = re.search(r'locked (?:camera|framing)|fixed camera|c[âa]mera fixa', text, re.I)
    movement = re.search(r'(?:the )?camera (?:tilts?|orbits?|rotates?|pans?|moves?|dollies)|c[âa]mera (?:gira|orbita|move)|(?:dolly|push)[ -]in', text, re.I)
    if fixed and movement:
        # A schedule permits a fixed opening followed by movement. This is not NLP proof.
        explicit = segments is not None and segments_ok and modes == {'locked', 'moving'}
        add('INFO' if explicit else 'WARN', 'CAMERA_SEGMENTED' if explicit else 'CAMERA_MIXED',
            'Câmera fixa/móvel têm segmentos explícitos; conferir texto e resultado.' if explicit else
            'Texto menciona câmera fixa e movimento; conferir negação e sequência temporal.',
            [fixed.group(), movement.group()])
    number_words = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
                    'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11,
                    'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15}
    for match in re.finditer(r'\b(\d+(?:\.\d+)?|'+'|'.join(number_words)+r')[ -]second (?:shot|take)\b', str(prompt), re.I):
        value = number_words.get(match[1].lower()) or seconds(match[1])
        if total is not None and value != total:
            add('WARN', 'PROMPT_DURATION', 'Duração textual pode divergir do total; conferir se descreve um segmento.', match.group())

    audio = meta.get('audioIntent')
    if audio is not None and (not isinstance(audio, str) or audio not in {'silent', 'native_guide', 'external_audio', 'post_dub', 'unspecified'}):
        add('ERROR', 'AUDIO_INTENT', 'Intenção sonora fora do vocabulário documentado.')
        audio = None
    native, original = flag(args.get('enableaudio')), flag(args.get('keeporiginalsound'))
    audio_inputs = [slot for slot in (mapping or {}) if slot.startswith('audio')]
    if request is not None:
        if audio == 'silent' and (native is True or original is True or audio_inputs):
            add('ERROR', 'AUDIO_CONTRADICTION', 'Intenção silent conflita com áudio explicitamente ativado/fornecido.')
        elif audio == 'native_guide' and native is False:
            add('ERROR', 'AUDIO_CONTRADICTION', 'Voz nativa solicitada com enable_audio=false.')
        elif audio in {'silent', 'native_guide'} and native is None:
            add('WARN', 'AUDIO_CONTROL_UNKNOWN', 'Sem controle explícito não se comprova a intenção sonora.')
        if audio == 'external_audio' and mapping is not None and not audio_inputs:
            add('ERROR', 'AUDIO_INPUT_MISSING', 'Intenção external_audio sem slot de áudio no pedido.')
        if re.search(r'no audio|silent video|sem [áa]udio', str(prompt), re.I) and native is not False:
            add('WARN', 'AUDIO_TEXT_ONLY', 'Texto de silêncio não desativa áudio; conferir intenção e controle.', prompt)

    selected = shot.get('referenceIds', [])
    for ref_id in selected:
        ref = references.get(ref_id)
        if not ref:
            add('ERROR', 'REFERENCE_MISSING', 'Referência selecionada não existe.', ref_id); continue
        if not isinstance(ref.get('sha256'), str) or not re.fullmatch(r'[0-9a-fA-F]{64}', ref['sha256']):
            add('ERROR', 'REFERENCE_HASH', 'Referência sem SHA-256 válido.', ref_id)
        if not ref.get('provenance') or ref.get('provenance') == 'unknown':
            add('WARN', 'PROVENANCE_UNKNOWN', 'Origem não comprovada; não inferir fotografia/autoria/aprovação.', ref_id)
    bindings = meta.get('referenceBindings', [])
    if not isinstance(bindings, list):
        add('ERROR', 'BINDINGS_SHAPE', 'referenceBindings deve ser lista.'); bindings = []
    slots = set()
    for binding in bindings:
        if not isinstance(binding, dict) or any(not isinstance(binding.get(k), str) or not binding[k].strip() for k in ('slot', 'referenceId', 'role')):
            add('ERROR', 'BINDING_SHAPE', 'Binding exige slot, referenceId e role não vazios.'); continue
        slot, ref_id = binding['slot'], binding['referenceId']
        ref = references.get(ref_id, {})
        if slot in slots or ref_id not in selected or ref_id not in references:
            add('ERROR', 'BINDING_REFERENCE', 'Slot duplicado ou referência não selecionada/existente.', binding)
        slots.add(slot)
        if ref.get('role') and binding['role'] != ref['role']:
            add('WARN', 'REFERENCE_ROLE', 'Função de uso difere do catálogo; justificar a seleção, sem reclassificar o original.', binding)
        if binding['role'] == 'identity' and ref.get('provenance') in {'ui_screenshot', 'synthetic', 'synthetic_variant'}:
            add('WARN', 'IDENTITY_PROVENANCE', 'Origem declarada não é foto real; não promover identidade automaticamente.', ref_id)
        if mapping is not None:
            if slot not in mapping:
                add('ERROR', 'BINDING_SLOT', 'Binding não tem entrada correspondente no pedido.', slot)
            elif mapping[slot] != ref.get('path'):
                add('WARN', 'BINDING_CONTENT_UNVERIFIED', 'Caminho/URL/placeholder não comprova o arquivo do catálogo; conferir hash.', slot)
    if mapping is not None and set(mapping)-slots:
        add('WARN', 'INPUT_ROLE_UNDOCUMENTED', 'Entradas sem binding de função/referência.', sorted(set(mapping)-slots))

    inspection = meta.get('inspection')
    if inspection is not None:
        methods = {'not_reviewed', 'metadata_only', 'sampled_frames', 'all_frames', 'full_playback', 'full_playback_and_frames'}
        if not isinstance(inspection, dict) or not isinstance(inspection.get('method'), str) or inspection['method'] not in methods:
            add('ERROR', 'INSPECTION_SHAPE', 'Método de inspeção inválido.')
        else:
            method = inspection['method']
            for field in ('fullPlaybackCompleted', 'fullFrameInspectionCompleted', 'audioAuditionCompleted'):
                value = inspection.get(field, False)
                if not isinstance(value, bool):
                    add('ERROR', 'INSPECTION_FLAG', 'Flags de inspeção exigem booleanos.', field)
                if value is True and field != 'audioAuditionCompleted' and (method in {'not_reviewed', 'metadata_only', 'sampled_frames'} or
                        field == 'fullPlaybackCompleted' and method == 'all_frames' or
                        field == 'fullFrameInspectionCompleted' and method == 'full_playback'):
                    add('ERROR', 'INSPECTION_CONTRADICTION', 'Método declarado não sustenta a inspeção integral alegada.', field)
            if any(inspection.get(k) is True for k in ('fullPlaybackCompleted', 'fullFrameInspectionCompleted', 'audioAuditionCompleted')) and not inspection.get('evidence'):
                add('WARN', 'INSPECTION_EVIDENCE', 'Inspeção declarada sem referência de evidência; não comprova revisão.')
            if method in {'not_reviewed', 'metadata_only', 'sampled_frames', 'all_frames'}:
                add('INFO', 'INSPECTION_LIMIT', 'Inspeção visual parcial/estática não comprova reprodução integral, voz ou aceite artístico.', method)

    overrides = meta.get('overrides', [])
    if not isinstance(overrides, list):
        add('ERROR', 'OVERRIDE_INVALID', 'overrides deve ser lista.'); overrides = []
    digest = coherence_hash(shot, references, request)
    for override in overrides:
        if not isinstance(override, dict) or any(not isinstance(override.get(k), str) or not override[k].strip() for k in ('code', 'reason', 'reviewer', 'subjectSha256')):
            add('ERROR', 'OVERRIDE_INVALID', 'Override exige código, motivo, revisor e hash.'); continue
        matches = [i for i in items if i['code'] == override['code']]
        if override['subjectSha256'] != digest or not matches or any(i['level'] not in {'WARN', 'INFO'} for i in matches):
            add('ERROR', 'OVERRIDE_INVALID', 'Override obsoleto, sem aviso correspondente ou tentando dispensar erro.', override['code'])
        else:
            for item in matches:
                item.update(acknowledged=True, override=copy.deepcopy(override))
    return items


# Strict mode ("intolerante a ambiguidade"): um aviso só deixa de bloquear se foi
# reconhecido por override (código, motivo, revisor, hash). INFO listado abaixo é
# o recibo de uma declaração explícita que já resolveu a ambiguidade.
RESOLVED_BY_DECLARATION = {'CAMERA_SEGMENTED'}


def unresolved_ambiguity(items):
    """WARN/INFO sem reconhecimento válido. Em modo estrito, cada um bloqueia como ERROR."""
    return [i for i in items if i['level'] in {'WARN', 'INFO'} and not i.get('acknowledged')
            and i['code'] not in RESOLVED_BY_DECLARATION]


def coherence_report(root, shot_id=None, request=None):
    """Reuse canonical plan/templates and provider slot mapping; never submit."""
    p, path, plan = plan_source(root)
    if plan is None:
        raise ValueError('plano de produção ausente para o projeto ativo')
    refs = {r['id']: r for r in plan['references']}
    shots = [s for s in plan['shots'] if shot_id is None or s['id'] == shot_id]
    if not shots or request is not None and len(shots) != 1:
        raise ValueError('selecionar uma ficha existente para o pedido exato')
    pf = module('coherence_preflight', ROOT / 'docs/kling-manual/tools/kling_preflight.py')
    models = read(root, SNAPSHOT)['body']['availableModels']
    items, subjects = [], []
    for shot in shots:
        job = request if request is not None else template(root, shot['family'], shot['id'])
        spec = next((m for m in models.get(job.get('tool'), {}).get('models', []) if m['model'] == job.get('model')), None)
        mapping = None
        if spec:
            mapping_report = pf.Report(job.get('job'))
            mapping = pf.media_mapping(job, spec, mapping_report)
            items.extend(mapping_report.items)
            # Normalize only film-relative local names. No media is read or downloaded.
            mapping = {k: (p['root']+'/'+v if isinstance(v, str) and not v.startswith(('<', 'http:', 'https:', '/')) and not v.startswith(p['root']+'/') else v) for k, v in mapping.items()}
        else:
            items.append({'level': 'ERROR', 'code': 'MODEL', 'msg': 'Ferramenta/modelo ausente no snapshot.'})
        state_errors = []
        for item in [shot] + [refs[i] for i in shot.get('referenceIds', []) if i in refs]:
            check_states(item, root, state_errors)
        items.extend({'level': 'ERROR', 'code': 'STATE', 'msg': error} for error in state_errors)
        items.extend(cinematic_lint(shot, refs, job, mapping))
        subjects.append({'shotId': shot['id'], 'sha256': coherence_hash(shot, refs, job)})
    return {'path': path, 'items': items, 'errors': [i for i in items if i['level'] == 'ERROR'],
            'unresolved': unresolved_ambiguity(items),
            'subjects': subjects, 'mediaInspected': False, 'creativeAcceptanceGranted': False,
            'paidReleaseGranted': False}


def validate_baseline(baseline, refs, shots, task_ids, lines, root, verify_media):
    """Planning only: valid links never release paid work or approve media."""
    errors = []
    if baseline.get('status') != 'prepared_not_artistically_approved' or baseline.get('paidGenerationAuthorized') is not False:
        errors.append('base ativa não concede aceite artístico ou liberação paga')
    steps = acyclic(baseline['steps'])
    selected = set(baseline['referenceIds'])
    if not selected <= refs.keys() or any(refs[r]['selection'] == 'excluded_from_current_cut' for r in selected if r in refs):
        errors.append('base ativa contém referência ausente ou histórica excluída')
    if not set(baseline['lineIds']) <= lines.keys() or baseline['firstSpeakingShotId'] not in shots:
        errors.append('base ativa tem fala/ficha ausente')
    if baseline['nextStepId'] not in steps:
        errors.append('base ativa sem próximo responsável')
    for step in steps.values():
        if not set(step['taskIds']) <= task_ids or not set(step['referenceIds']) <= refs.keys():
            errors.append('etapa da base com vínculo ausente: ' + step['id'])
        if step['state'] not in {'ready_local', 'blocked'} or not all(step.get(k) for k in ('owner', 'inputs', 'output', 'acceptance')):
            errors.append('etapa da base sem dono, entradas ou aceite: ' + step['id'])
    for item in baseline['findings']:
        if not set(item['referenceIds']) <= refs.keys():
            errors.append('achado da base com referência ausente')
    if verify_media:
        for item in baseline['historyEvidence']:
            if sha(safe(root, item['path'])) != item['sha256']:
                errors.append('evidência histórica da base mudou: ' + item['path'])
    return errors


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
        if plan.get('activeBaseline'):
            errors.extend(validate_baseline(plan['activeBaseline'], refs, shots, task_ids, lines, root, verify_media))
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
        if plan is None:
            raise ValueError('plano de produção não encontrado')
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
    source_paths.extend(list(plan.get('deliverables', [])))
    return {'path': path, 'revision': plan['revision'], 'implementationApprovalId': plan['implementationApprovalId'],
            'status': 'local_implementation_prepared_creative_review_pending',
            'boardIsTaskAuthority': True, 'encounters': plan['encounters'], 'stages': plan['stages'],
            'references': [{k: r[k] for k in ('id', 'label', 'path', 'sha256', 'role', 'provenance', 'selection', 'states', 'notes')} for r in plan['references']],
            'shots': plan['shots'], 'pilot': plan['pilot'], 'constraints': plan['constraints'],
            **({'activeBaseline': plan['activeBaseline']} if plan.get('activeBaseline') else {}),
            'capabilities': capability, 'costPolicy': plan['costPolicy'], 'blockers': plan['blockers'],
            'families': [{k: f[k] for k in ('id', 'title', 'purpose', 'requiredDecisions')} for f in read(root, FAMILIES)['families']],
            'sourceVersions': [{'path': name, 'sha256': sha(safe(root, name))} for name in dict.fromkeys(source_paths)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('command', choices=['check', 'export', 'routes', 'jobs', 'template', 'check-request', 'review-hashes', 'check-coherence'])
    parser.add_argument('--verify-media', action='store_true')
    parser.add_argument('--family')
    parser.add_argument('--shot')
    parser.add_argument('--spec', type=Path)
    parser.add_argument('--strict', action='store_true', help='check-coherence: WARN/INFO sem reconhecimento viram bloqueio')
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
    elif args.command == 'check-coherence':
        if args.spec and not args.shot:
            parser.error('check-coherence --spec exige --shot')
        job = json.loads(args.spec.read_text()) if args.spec else None
        if args.spec and not isinstance(job, dict):
            parser.error('check-coherence aceita um pedido objeto')
        result = coherence_report(args.root, args.shot, job)
        if getattr(args, 'strict', False):
            result['strict'] = True
            result['errors'] = result['errors'] + result['unresolved']
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
