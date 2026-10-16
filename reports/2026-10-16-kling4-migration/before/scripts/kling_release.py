#!/usr/bin/env python3
"""Local release checks for the existing Kling runner. No network, upload or spend.

The producer records a real scoped decision in approvals.json; this module checks
its consistency, not the identity of a human approver. Provider prices are not
server-capped by these local checks.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import json
import math
from pathlib import Path

_media_spec = importlib.util.spec_from_file_location(
    "movies_shared_media", Path(__file__).with_name("shared_media.py")
)
if _media_spec is None or _media_spec.loader is None:
    raise ImportError("could not load shared_media.py")
shared_media = importlib.util.module_from_spec(_media_spec)
_media_spec.loader.exec_module(shared_media)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def local_path(film, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute() or '..' in Path(value).parts:
        raise ValueError('evidência deve usar caminho relativo ao filme')
    path = (film / value).resolve()
    if not path.is_relative_to(film.resolve()) or not path.is_file():
        raise ValueError('evidência ausente ou fora do filme: ' + value)
    return path


def normalized_args(args):
    result = {}
    for key, value in args.items():
        name = key.replace('_', '').replace('-', '').lower()
        if name in result:
            raise ValueError('ARG_DUPLICATE: alias duplicado: ' + key)
        if name == 'elements' and isinstance(value, str):
            value = json.loads(value)
        if isinstance(value, bool):
            value = 'true' if value else 'false'
        elif not isinstance(value, (dict, list)):
            value = str(value)
        if name == 'elements' and isinstance(value, list):
            value = sorted(value, key=lambda e: str(e.get('id', '')))
        result[name] = value
    return result


def fingerprint(film, job, *, media_root=None):
    """Exclude job name/auth/note; changing those must not conceal a retry."""
    args = dict(job.get('args', job.get('options', {})))
    if job.get('elements') is not None:
        args['elements'] = job['elements']
    def media(ref):
        if ref.startswith(('https://', 'http://')):
            return {'url': ref}  # Exact URL only; a URL is not content verification.
        try:
            path = shared_media.input_path(film, ref, media_root=media_root)
        except ValueError as error:
            raise ValueError('referência local ausente/fora do filme: ' + ref + '; ' + str(error)) from error
        return {'sha256': file_hash(path)}
    images = job.get('images', job.get('refs', []))
    named = job.get('inputs') or {}
    # Normalize the CLI's equivalent single-image mappings.
    if images and not named and job['tool'] in {'image_to_video', 'motion_control', 'omni_ref_video'}:
        if job['tool'] == 'motion_control':
            names = ['image']
        elif job['tool'] == 'image_to_video' and job['model'] not in {'kling-video-o1', 'kling-video-v3_0_omni'}:
            names = ['first_image']
        else:
            names = ['image_' + str(i + 1) for i in range(len(images))]
        if len(names) != len(images):
            raise ValueError('quantidade de imagens incompatível')
        named, images = dict(zip(names, images)), []
    payload = {'tool': job['tool'], 'model': job['model'], 'prompt': job['prompt'],
               'args': normalized_args(args), 'images': [media(x) for x in images],
               'inputs': {key: media(value) for key, value in named.items()},
               'referenceDurationSeconds': job.get('referenceDurationSeconds'),
               'inputFacts': job.get('inputFacts') or {}}
    return digest(payload)


def verified_evidence(film, evidence):
    if not isinstance(evidence, dict) or file_hash(local_path(film, evidence.get('path'))) != evidence.get('sha256'):
        raise ValueError('hash da evidência divergiu')


def moment(value):
    result = dt.datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError('data precisa de fuso horário')
    return result


def positive(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def authorize(film, job, *, now=None):
    """Check a per-job release before discovery/account/upload. Never create one."""
    try:
        approvals = json.loads((film / '00_brief/approvals.json').read_text())
        matches = [a for a in approvals.get('approvals', []) if a.get('id') == job.get('auth')]
        if len(matches) != 1:
            raise ValueError('autorização específica não encontrada')
        entry = matches[0]
        if entry.get('kind') != 'kling_job_release' or entry.get('status') != 'approved':
            raise ValueError('autorização não libera um job Kling; planejamento e teto histórico não liberam envio')
        scope = entry['scope']
        payload_hash = fingerprint(film, job)
        if scope.get('job') != job['job'] or scope.get('payloadSha256') != payload_hash or scope.get('maxJobs') != 1:
            raise ValueError('pedido difere do conteúdo e job liberados')
        now = now or dt.datetime.now(dt.UTC)
        if moment(scope['expiresAt']) <= now:
            raise ValueError('liberação expirada')
        verified_evidence(film, entry['decisionEvidence'])
        quote = scope['quote']
        if quote.get('basis') not in {'official_panel', 'provider_quote'} or quote.get('unit') != 'Kling credits':
            raise ValueError('estimativa não é cotação de créditos da conta')
        if quote.get('payloadSha256') != payload_hash or moment(quote['expiresAt']) <= now or moment(quote['verifiedAt']) > now:
            raise ValueError('cotação vencida, futura ou de outro pedido')
        if not positive(scope.get('maxCredits')) or not positive(quote.get('credits')) or quote['credits'] > scope['maxCredits']:
            raise ValueError('cotação inválida ou acima do teto')
        verified_evidence(film, quote['evidence'])
        schema_hash = scope.get('schemaSha256')
        if not isinstance(schema_hash, str) or len(schema_hash) != 64:
            raise ValueError('hash do schema revisado ausente')
        refs = job.get('images', []) + list((job.get('inputs') or {}).values())
        if any(not ref.startswith(('https://', 'http://')) for ref in refs) and scope.get('allowReferenceUploads') is not True:
            raise ValueError('pedido inclui upload local sem escopo explícito')
        return {'approvalId': entry['id'], 'payloadSha256': payload_hash,
                'approvalSha256': digest(entry), 'schemaSha256': schema_hash,
                'maxCredits': scope['maxCredits'], 'quote': quote,
                'providerEnforcesCeiling': False}
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise SystemExit('liberação bloqueou antes de qualquer chamada: ' + str(exc)) from exc


def reject_duplicate(film, job):
    """Fail closed for identical content, including an uncertain renamed job."""
    payload_hash = fingerprint(film, job)
    for path in sorted((film / '07_generations/responses').glob('*.intent.json')):
        try:
            prior = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            raise SystemExit('intenção ilegível; reconciliar antes de novo envio: ' + path.name) from exc
        previous = prior.get('payloadSha256')
        if previous is None:
            try:
                previous = fingerprint(film, prior)
            except (OSError, ValueError, TypeError, KeyError):
                # Historical incomplete intents are preserved; exact tool/model/prompt
                # matches still need producer reconciliation, not a renamed retry.
                if all(prior.get(k) == job.get(k) for k in ('tool', 'model', 'prompt')):
                    raise SystemExit('intenção anterior incompleta com o mesmo pedido: ' + path.name)
        if previous == payload_hash:
            raise SystemExit('conteúdo já submetido ou incerto; renomear não autoriza reenvio: ' + path.name)
    return payload_hash


def registry(film):
    """Read-only view of existing receipts. No second ledger or invented job ID."""
    result = []
    for path in sorted((film / '07_generations/responses').glob('*.intent.json')):
        job = path.name.removesuffix('.intent.json')
        def read(suffix):
            p = path.with_name(job + suffix)
            try:
                return json.loads(p.read_text()) if p.exists() else {}
            except (OSError, ValueError):
                return {'recordError': True}
        intent = read('.intent.json')
        submit = read('.submit.json').get('body') or {}
        response = read('.response.json').get('body') or {}
        balance = read('.balance.json')
        release = intent.get('release')
        quote = release.get('quote') if isinstance(release, dict) else None
        def generation(body):
            nested = body.get('generations') or []
            return nested[0] if nested and isinstance(nested[0], dict) else body
        sent, observed = generation(submit), generation(response)
        gen_id = (sent.get('generationId') or sent.get('generation_id')) if isinstance(sent, dict) else None
        result.append({'job': job, 'model': intent.get('model'), 'generationId': gen_id,
                       'status': observed.get('status', 'SUBMITTED' if gen_id else 'SUBMISSION_UNKNOWN')
                       if isinstance(observed, dict) else ('SUBMITTED' if gen_id else 'SUBMISSION_UNKNOWN'),
                       'payloadSha256': intent.get('payloadSha256'),
                       'estimate': None, 'quote': quote,
                       'providerReportedCredits': balance.get('creditsConsumed'),
                       'chargeBasis': balance.get('chargeBasis', 'unknown'),
                       'balanceDelta': balance.get('creditsDelta'), 'balanceDeltaIsCharge': False,
                       'creativeApproval': 'not_inferred', 'source': str(path.relative_to(film))})
    return result
