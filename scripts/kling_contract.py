"""Local production prerequisites for discovered Kling 4 routes. No provider I/O.

This policy supplements the live allowlist. Announced full-model limits never
expand the current account schema; unknown media facts fail before any upload.
"""
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

V4 = 'kling-video-v4_0'  # observed in who_am_i, 2026-10-16; no inferred aliases


def positive(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def evidence(root, entry):
    """Verify local evidence without accepting an approval merely from a label."""
    if not isinstance(entry, dict):
        raise ValueError('evidência ausente')
    ref = entry.get('path')
    if not isinstance(ref, str) or Path(ref).is_absolute() or '..' in Path(ref).parts:
        raise ValueError('evidência exige caminho relativo canônico')
    path = (Path(root) / ref).resolve()
    if not path.is_relative_to(Path(root).resolve()) or not path.is_file() or file_hash(path) != entry.get('sha256'):
        raise ValueError('evidência ausente/hash divergente: ' + str(ref))
    return path


def audio_facts(path):
    raw = subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], text=True, timeout=30)
    data = json.loads(raw)
    if not any(s.get('codec_type') == 'audio' for s in data['streams']):
        raise ValueError('sem stream de áudio')
    return {'durationSeconds': float(data['format']['duration']), 'bytes': Path(path).stat().st_size}


def check(job, spec, mapping, args, elements, root, rep, video_probe, allow_placeholders=False):
    if job.get('model') != V4:
        return
    contract = job.get('shotContract')
    if not isinstance(contract, dict) or type(contract.get('version')) is not int or contract.get('version') != 1:
        rep.err('V4_CONTRACT', 'V4 exige shotContract v1: referências por uso, beats, áudio e continuidade.')
        return
    if contract.get('provider') != 'kling-global' or contract.get('interface') != 'cli':
        rep.err('V4_INTERFACE', 'Este contrato é da CLI Global; Higgsfield/web/API são interfaces distintas.')
    try:
        duration = float(args.get('duration', 0))
    except (TypeError, ValueError):
        duration = 0
    if not positive(duration):
        rep.err('V4_DURATION', 'Duração explícita medida/revisada obrigatória.')
    if 'resolution' not in args or str(args.get('imageCount')) != '1':
        rep.err('V4_OUTPUT', 'Defina resolution explicitamente e imageCount=1 por liberação.')
    beats = contract.get('beats')
    if not isinstance(beats, list) or not beats:
        rep.err('V4_BEATS', 'Informe beats temporais com ação e limites em segundos.')
    else:
        end = 0
        for beat in beats:
            if not isinstance(beat, dict) or not isinstance(beat.get('action'), str) or not beat['action'].strip():
                rep.err('V4_BEATS', 'Beat sem ação.'); continue
            start, finish = beat.get('start'), beat.get('end')
            if not isinstance(start, (int, float)) or isinstance(start, bool) or not math.isfinite(start) or not positive(finish) or not end <= start < finish <= duration:
                rep.err('V4_BEATS', 'Beats devem ser ordenados, não sobrepostos e contidos na duração.')
            else:
                end = finish
    continuity = contract.get('continuity') or {}
    if not isinstance(continuity, dict) or not all(isinstance(continuity.get(k), str) and continuity[k].strip() for k in ('cast', 'wardrobe', 'table', 'screenAxis', 'historicalFaceExclusion')):
        rep.err('V4_CONTINUITY', 'Declare elenco/companheiros, figurino, mesa/marcas, eixo e exclusão facial histórica.'); continuity = {}
    audio = contract.get('audio') or {}
    if not isinstance(audio, dict) or audio.get('strategy') not in {'native_guide', 'retain_source', 'postproduction', 'uncontrolled_review_required'}:
        rep.err('V4_AUDIO_PLAN', 'Estratégia de áudio explícita obrigatória.'); audio = {}
    truth = lambda value: str(value).lower() == 'true'
    if audio.get('strategy') == 'native_guide' and not truth(args.get('enable_audio')):
        rep.err('V4_AUDIO_PLAN', 'Voz nativa exige controle enable_audio=true nesta rota.')
    if audio.get('strategy') == 'retain_source' and (not truth(args.get('keepOriginalSound')) or not any(k.startswith('video_') for k in mapping)):
        rep.err('V4_AUDIO_PLAN', 'Reter som exige vídeo de origem e keepOriginalSound=true.')
    if audio.get('strategy') == 'postproduction' and ('enable_audio' not in args or truth(args.get('enable_audio')) or truth(args.get('keepOriginalSound'))):
        rep.err('V4_AUDIO_PLAN', 'Pós exige ambos controles de som desligados; ausência de flag não garante silêncio.')
    if audio.get('strategy') == 'native_guide':
        if not isinstance(audio.get('dialogue'), str) or not audio['dialogue'].strip() or not positive(audio.get('measuredSeconds')) or audio['measuredSeconds'] > duration or audio.get('languageReview') != 'reviewed':
            rep.err('V4_DIALOGUE', 'Fala exata, duração medida e revisão de idioma requeridas; voz final é aceite separado.')
    if job['tool'] == 'image_to_video' and not mapping:
        rep.err('V4_KEYFRAME', 'Rota de keyframes exige pelo menos uma imagem explicitamente selecionada.')
    if job['tool'] == 'omni_ref_video':
        if str(args.get('prefer_multi_shots')).lower() != 'true':
            rep.err('V4_MULTISHOT', 'Omni V4 requer multi-shot=true; câmera fixa exige outra rota revisada.')
        if continuity.get('cameraMode') == 'locked_single_shot':
            rep.err('V4_CAMERA', 'Câmera fixa não foi qualificada em Omni com multi-shot obrigatório.')
        if args.get('aspect_ratio', 'auto') == 'auto' and not any(k.startswith(('image_', 'video_')) for k in mapping):
            rep.err('V4_AUTO_RATIO', 'auto exige imagem/vídeo direto; Elements/áudio não bastam.')
    if job['tool'] == 'text_to_video' and 'aspect_ratio' not in args:
        rep.err('V4_RATIO', 'Default contraditório no catálogo; definir proporção explicitamente.')
    refs = contract.get('references')
    if not isinstance(refs, list):
        rep.err('V4_REFERENCES', 'Manifesto tipado de referências obrigatório.'); refs = []
    expected = {target for target, value in mapping.items() if not (allow_placeholders and isinstance(value, str) and value.startswith('<'))} | {'element:' + str(e['id']) for e in elements}
    indexed = {}
    for ref in refs:
        if not isinstance(ref, dict) or not isinstance(ref.get('target'), str):
            rep.err('V4_REFERENCES', 'Referência sem target.'); continue
        target = ref['target']
        if target in indexed:
            rep.err('V4_REFERENCES', 'Target duplicado: ' + target)
        indexed[target] = ref
        if ref.get('kind') not in {'image', 'video', 'audio'} or not ref.get('provenance') or not ref.get('use'):
            rep.err('V4_REFERENCES', 'Tipo, proveniência e função da referência obrigatórios.')
        review = ref.get('review') or {}
        if not isinstance(review, dict) or review.get('status') != 'approved' or review.get('scope') != ref.get('use'):
            rep.err('V4_REFERENCE_SCOPE', 'Aprovação por uso pendente/divergente: ' + target)
        try:
            evidence(root, ref.get('reviewEvidence'))
            if target.startswith('element:'):
                path = evidence(root, ref.get('elementEvidence'))
                detail = json.loads(path.read_text())
                detail = detail.get('body', detail)
                detail = detail.get('element', detail)
                element_id = target.split(':', 1)[1]
                if str(detail.get('id')) != element_id or detail.get('type') != ref.get('kind') or not detail.get('resource'):
                    raise ValueError('element_get precisa confirmar ID, type e resources')
                actual = next(e for e in elements if str(e['id']) == element_id)
                if actual.get('type') != ref.get('kind'):
                    raise ValueError('tipo de Element difere do manifesto')
            else:
                value = mapping.get(target)
                if ref.get('source') != value or not re.fullmatch('[0-9a-f]{64}', str(ref.get('sha256', ''))):
                    raise ValueError('source/hash não corresponde ao slot')
                if isinstance(value, str) and not value.startswith(('https://', 'http://')):
                    evidence(root, {'path': value, 'sha256': ref['sha256']})
                elif value:
                    # A URL is mutable; a claimed digest without local bytes cannot establish identity.
                    evidence(root, {'path': ref.get('localEvidence'), 'sha256': ref['sha256']})
        except (OSError, ValueError, KeyError, TypeError, StopIteration) as err:
            rep.err('V4_REFERENCE_EVIDENCE', str(err))
    if set(indexed) != expected:
        rep.err('V4_REFERENCES', 'Manifesto deve cobrir exatamente todos os inputs e Elements, sem omitir identidade.')
    total_video = 0
    source_audio_confirmed = False
    for target, ref in indexed.items():
        kind = ref.get('kind')
        if target in mapping:
            expected_kind = 'video' if target.startswith('video') else 'audio' if target.startswith('audio') else 'image'
            if kind != expected_kind:
                rep.err('V4_REFERENCE_KIND', 'Tipo incompatível com slot ' + target)
        if kind not in {'audio', 'video'}:
            continue
        facts = ref.get('facts') or {}
        value = mapping.get(target)
        try:
            if value and not value.startswith(('https://', 'http://')):
                facts = video_probe(str(Path(root) / value)) if kind == 'video' else audio_facts(Path(root) / value)
        except (OSError, ValueError, KeyError, IndexError, subprocess.SubprocessError):
            rep.err('V4_MEDIA_PROBE', 'Mídia inválida: ' + target); continue
        if not isinstance(facts, dict) or not positive(facts.get('durationSeconds')) or not positive(facts.get('bytes')):
            rep.err('V4_MEDIA_FACTS', 'Medir duração/tamanho: ' + target); continue
        seconds = facts['durationSeconds']
        if target == 'video_1' and facts.get('hasAudio') is True:
            source_audio_confirmed = True
        if kind == 'video':
            total_video += seconds
            if not all(positive(facts.get(k)) for k in ('width', 'height')) or not 0.4 <= facts.get('width', 0) / facts.get('height', 1) <= 2.5 or not 3 <= seconds <= 30 or facts['bytes'] > 300 * 1000 * 1000:
                rep.err('V4_VIDEO_LIMIT', 'Vídeo exige 3–30 s, ≤300 MB e proporção 2:5–5:2.')
        elif not 5 <= seconds <= 30 or facts['bytes'] > 50 * 1000 * 1000 or ref.get('use') != 'voice' or ref.get('voiceContentReview') != 'reviewed_voice_only':
            rep.err('V4_AUDIO_LIMIT', 'Áudio exige voz, 5–30 s e ≤50 MB; não substitui trilha musical.')
    if audio.get('strategy') == 'retain_source' and not source_audio_confirmed:
        rep.err('V4_SOURCE_AUDIO', 'Som de video_1 não confirmado; arquivo mudo não pode fornecer áudio.')
    if total_video > 30:
        rep.err('V4_VIDEO_TOTAL', 'Vídeos diretos + video Elements excedem 30 segundos.')
    if total_video and contract.get('billing') != {'inputVideoSeconds': total_video, 'inputVideoDurationIncluded': True}:
        rep.err('V4_BILLING', 'Declarar duração de vídeos de entrada incluída na cobrança; preço atual permanece desconhecido.')
    rep.info('V4_EVIDENCE', 'Catálogo listado não é geração testada; QC temporal, voz, idioma, identidade e liberação financeira são gates separados.')

