#!/usr/bin/env python3
"""Producer-only CLI runner. Submit once; interactive resume queries once.

Intent is durable before submission. Uncertain submissions are never retried.
Balance observations and provider-reported charges are kept separate. The command
line requires --submit-only for one job; legacy callers may still poll explicitly.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import fcntl
import hashlib
import io
import importlib.util
import re
import math
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.parse
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TELEMETRY = ["--skill-name", "kling-cli", "--skill-version", "0.2.1"]
SUCCESS = {"COMPLETED", "PARTIAL_COMPLETED", "SUCCEED", "SUCCEEDED", "SUCCESS"}
TERMINAL = SUCCESS | {"FAILED", "CANCELLED", "CANCELED", "QUERY_UNKNOWN", "QUERY_ERROR", "RESULT_EMPTY"}
GENERATORS = {"text_to_image", "image_to_image", "text_to_video", "image_to_video", "omni_ref_video", "motion_control"}
_spec = importlib.util.spec_from_file_location("kling_preflight", ROOT / "docs/kling-manual/tools/kling_preflight.py")
pf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pf)
_release = importlib.util.spec_from_file_location("kling_release", ROOT / "scripts/kling_release.py")
release = importlib.util.module_from_spec(_release)
_release.loader.exec_module(release)

_trace = importlib.util.spec_from_file_location("kling_respan", ROOT / "scripts/kling_respan.py")
tracing = importlib.util.module_from_spec(_trace)
_trace.loader.exec_module(tracing)


def resolve_media_input(film: Path, ref: str, *, media_root: Path | None = None) -> str:
    """Resolve an explicit canonical input without copying or changing it."""
    if ref.startswith(('http://', 'https://')):
        return ref
    return str(release.shared_media.input_path(film, ref, media_root=media_root))


def redact(value, *, urls=True):
    """Reduz dados sensíveis no registro do subprocesso; não altera o payload enviado."""
    if isinstance(value, dict):
        return {k: "[REDACTED]" if re.search(r"token|authorization|cookie|secret|password|ticket", str(k), re.I)
                else redact(v, urls=urls) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v, urls=urls) for v in value]
    if isinstance(value, str):
        value = re.sub(r"(?i)\b(Bearer|Basic)\s+[A-Za-z0-9._~+/=-]+", r"\1 [REDACTED]", value)
        value = re.sub(r'(?i)((?:access_token|refresh_token|authorization|cookie|secret|password|ticket)["\s]*[:=]["\s]*)([^"\s,;}]+)', r'\1[REDACTED]', value)
        if urls:
            value = re.sub(r'https?://[^\s"<>]+', lambda m: m.group(0).split('?')[0] + ('?[REDACTED]' if '?' in m.group(0) else ''), value)
    return value


def preflight(job, film):
    """Consulta somente capacidades; falha antes de saldo/upload/submissão."""
    discovery = run(['kling', 'who_am_i', '-q', *TELEMETRY])
    if discovery.get('ok') is False:
        raise SystemExit('schema ao vivo indisponível; nenhum envio feito')
    try:
        models = discovery['body']['availableModels']
        report = pf.check_job(job, models, str(film), str(film), False)
        spec = next(m for m in models[job['tool']]['models'] if m['model'] == job['model'])
    except (KeyError, TypeError, ValueError, StopIteration):
        raise SystemExit('schema/modelo inválido; nenhum envio feito')
    blocking = [x for x in report.items if x['level'] == 'ERROR' or x['code'] in {'DEFAULT', 'MOTION_DURATION_UNKNOWN'}]
    if blocking:
        raise SystemExit('preflight bloqueou: ' + '; '.join(x['code'] + ': ' + x['msg'] for x in blocking))
    canonical = {pf.norm(a['name']): a['name'] for a in spec.get('arguments', [])}
    arguments = {canonical[pf.norm(name)]: pf.cli_value(value) for name, value in job['args'].items()}
    return {'modelSpec': spec, 'arguments': arguments, 'schemaSha256': hashlib.sha256(json.dumps(models, sort_keys=True).encode()).hexdigest(),
            'checkedAt': dt.datetime.now(dt.timezone.utc).isoformat(), 'items': report.items}



def run(cmd: list[str], *, timeout: int = 180) -> dict:
    # A CLI usa process.exit(): pipes podem truncar JSON grande no Node.
    # Arquivos temporários privados evitam perda de IDs e schemas sem alterar a CLI.
    with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as out, tempfile.TemporaryFile(mode='w+', encoding='utf-8') as err:
        timed_out = False
        try:
            proc = subprocess.run(cmd, stdout=out, stderr=err, text=True, timeout=timeout,
                                  stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            timed_out = True
            proc = subprocess.CompletedProcess(cmd, 124)
        out.seek(0)
        err.seek(0)
        stdout = proc.stdout if isinstance(proc.stdout, str) else out.read()
        stderr = proc.stderr if isinstance(proc.stderr, str) else err.read()
    try:
        data = json.loads(stdout)
        if not isinstance(data, dict):
            data = {"ok": False, "parsed": data}
    except json.JSONDecodeError:
        data = {"ok": False}
    # Preserve diagnostics with secret and signed-query redaction.
    data['_cli'] = {"stdout": redact(stdout), "stderr": redact(stderr), "rc": proc.returncode}
    if proc.returncode:
        data['ok'] = False
    if timed_out:
        data['submissionUncertain'] = True
    return redact(data, urls=False)


def account(snapshot: dict | None = None) -> int | None:
    data = run(["kling", "account", "-q", *TELEMETRY])
    if snapshot is not None:
        snapshot.update(data)
    try:
        value = data["body"]["availableRemainCredits"]
        if data.get('ok') is False or isinstance(value, bool):
            return None
        value = int(str(value))
        return value if value >= 0 else None
    except (KeyError, TypeError, ValueError):
        return None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def durable(path: Path, text: str) -> None:
    """Atomic replacement plus fsync; interrupted writes leave prior data intact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f'.{path.name}.', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        sync_dir(path.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def sync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def save(path: Path, data: dict) -> None:
    durable(path, json.dumps(data, indent=2) + '\n')


def paths(film: Path, job: str) -> tuple[Path, Path, Path]:
    if not job or job in {'.', '..'} or Path(job).name != job or '\\' in job:
        raise SystemExit('job must be a single filename identifier')
    return tuple(film / '07_generations' / folder for folder in ('requests', 'responses', 'originals'))


@contextmanager
def locked(film: Path):
    """Serialize this runner's balance snapshots and atomic ledger replacements."""
    film.mkdir(parents=True, exist_ok=True)
    with (film / '.kling-producer.lock').open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def generation_id(data: dict):
    body = data.get('body') or {}
    if not isinstance(body, dict):
        return None
    gens = body.get('generations') or []
    first = gens[0] if isinstance(gens, list) and gens and isinstance(gens[0], dict) else {}
    value = (body.get('generationId') or body.get('generation_id') or
             first.get('generationId') or first.get('generation_id'))
    return value if isinstance(value, str) and value.strip() else None


def reconcile(film: Path, job: str, intent: dict, gen_id, *, immediate=False) -> dict:
    """Persist accounting before an idempotent, atomic ledger update."""
    _, res, _ = paths(film, job)
    receipt = res / f'{job}.balance.json'
    if receipt.exists():
        balance = json.loads(receipt.read_text())
    else:
        try:
            after = account()
        except Exception:
            after = None
        before = intent['balanceBefore']
        # After a crash, later balance cannot safely be attributed to this job.
        balance = {'balanceBefore': before, 'balanceAfter': after,
                   'creditsDelta': before - after if immediate and after is not None else None,
                   'reconciliation': 'immediate' if immediate else 'delayed_unattributed'}
        submit_path = res / f'{job}.submit.json'
        submitted = json.loads(submit_path.read_text()) if submit_path.exists() else {}
        body = submitted.get('body') or {}
        charge = body.get('creditsConsumed', body.get('credits_consumed')) if isinstance(body, dict) else None
        try:
            charge = float(charge) if charge is not None and not isinstance(charge, bool) else None
            if charge is not None and (not math.isfinite(charge) or charge < 0):
                charge = None
        except (TypeError, ValueError):
            charge = None
        balance.update(creditsConsumed=charge, chargeBasis='provider_reported' if charge is not None else 'unknown',
                       balanceDeltaIsCharge=False)
        save(receipt, balance)
    ledger = film / 'credit-ledger.csv'
    previous = ''
    if ledger.exists():
        with ledger.open(encoding='utf-8', newline='') as stream:
            previous = stream.read()
    rows = list(csv.reader(io.StringIO(previous)))
    key = f'L{job}'
    if not any(row and row[0] == key for row in rows):
        out = io.StringIO(newline='')
        csv.writer(out, lineterminator='\r\n').writerow([
            key, intent['created'], 'Kling', gen_id or '', job, '',
            balance.get('creditsConsumed') if balance.get('creditsConsumed') is not None else '',
            f"{balance.get('chargeBasis', 'legacy_balance_receipt')}; balance_observation ({balance['balanceBefore']}->{balance['balanceAfter']}) is not a per-job charge; {balance['reconciliation']}; submission {'known_id' if gen_id else 'unknown_id'}",
            balance['balanceAfter'] if balance['balanceAfter'] is not None else '',
            intent['auth'], f"{intent['model']} {intent['tool']} {json.dumps(intent['options'])}; {intent['note']}"
        ])
        durable(ledger, previous + ('' if not previous or previous.endswith('\n') else '\n') + out.getvalue())
    return balance


def summary(job: str, gen_id, status: str, balance: dict, works=None, error=None) -> dict:
    return {'job': job, 'generationId': gen_id, 'status': status,
            'works': works or [], **balance, 'error': error}


def submit(film: Path, job: str, tool: str, model: str, prompt: str, args: dict[str, str],
           images: list[str], auth: str, note: str, poll: int = 300,
           *, submit_only: bool = False, inputs: dict | None = None, elements=None,
           reference_duration=None, submission_blocked=None, input_facts=None) -> dict:
    req, res, _ = paths(film, job)
    with locked(film):
        if any((res / f'{job}.{kind}.json').exists() for kind in ('response', 'submit', 'intent')):
            raise SystemExit(f'{job}: submission evidence already exists; never resubmit')
        if tool not in GENERATORS:
            raise SystemExit('unsupported generation tool')
        if not isinstance(auth, str) or not auth.strip() or re.search(r'REPLACE|PLACEHOLDER|<.*>|PENDING', auth, re.I):
            raise SystemExit('explicit authorization reference is required; placeholder rejected')
        args = dict(args)
        if elements is not None:
            if 'elements' in args and pf.cli_value(args['elements']) != pf.cli_value(elements):
                raise SystemExit('conflicting elements')
            args['elements'] = elements
        if 'prompt' in args:
            raise SystemExit('prompt must be top-level, not duplicated in args')
        job_spec = {'job': job, 'tool': tool, 'model': model, 'prompt': prompt, 'args': args,
                    'images': images, 'inputs': inputs or {}, 'auth': auth,
                    'referenceDurationSeconds': reference_duration, 'submissionBlocked': submission_blocked,
                    'inputFacts': input_facts or {}}
        if submission_blocked:
            raise SystemExit('draft plan is blocked: ' + str(submission_blocked))
        try:
            payload_hash = release.reject_duplicate(film, job_spec)
        except (ValueError, OSError, TypeError) as exc:
            raise SystemExit(str(exc)) from exc
        envelope = release.authorize(film, job_spec)
        validation = preflight(job_spec, film)
        if envelope and validation.get("schemaSha256") != envelope["schemaSha256"]:
            raise SystemExit("schema mudou desde a liberação; revisar antes de envio")
        args = validation.get('arguments', args)
        cmd = ['kling', tool, '--model', model, '--poll', '0', '-q', *TELEMETRY,
               '--rationale', f'Film reference batch {auth}: {note}']
        def media_path(img):
            return resolve_media_input(film, img)
        for slot, ref in (inputs or {}).items():
            if tool == 'motion_control':
                if slot not in {'image', 'video'}:
                    raise SystemExit('unsupported motion input')
                cmd += [f'--{slot}', media_path(ref)]
            elif tool in {'image_to_video', 'omni_ref_video'}:
                cmd += ['--input', f'{slot}={media_path(ref)}']
            else:
                raise SystemExit('named inputs not supported by this CLI command')
        for img in images:
            cmd += ['--image', resolve_media_input(film, img)]
        for key, value in args.items():
            if pf.norm(key) in {'poll', 'model', 'rationale', 'skillname', 'skillversion', 'tasktraceid', 'quiet', 'q', 'help', 'h', 'image', 'input', 'video', 'audio', 'tailimage'}:
                raise SystemExit(f'reserved option: {key}')
            cmd += [f'--{key}', pf.cli_value(value)]
        cmd.append(prompt)
        snapshot = {}
        before = account(snapshot)
        if before is None:
            raise SystemExit('balance unavailable; no submission made')
        if envelope and before < envelope['quote']['credits']:
            raise SystemExit('saldo inferior à cotação; nenhum envio feito')
        intent = {'payloadSha256': payload_hash, 'release': envelope, 'inputFacts': input_facts or {},
                  'job': job, 'tool': tool, 'model': model, 'prompt': prompt,
                  'options': args, 'refs': images, 'inputs': inputs or {}, 'validation': validation,
                  'referenceDurationSeconds': reference_duration, 'auth': auth, 'note': note,
                  'balanceBefore': before, 'accountBefore': snapshot, 'command': cmd,
                  'created': dt.datetime.now().astimezone().isoformat(timespec='seconds'),
                  'costTrace': tracing.context(film, job, payload_hash)}
        prompt_path = req / f'{job}.prompt.txt'
        if prompt_path.exists() and prompt_path.read_text() != prompt + '\n':
            raise SystemExit('existing prompt differs; refusing overwrite')
        if not prompt_path.exists():
            durable(prompt_path, prompt + '\n')
        save(res / f'{job}.intent.json', intent)
        def submit_and_record():
            try:
                data = run(cmd)
            except Exception as exc:
                data = {'ok': False, 'error': redact(str(exc)), 'submissionUncertain': True}
            save(res / f'{job}.submit.json', data)
            gen_id = generation_id(data)
            balance = reconcile(film, job, intent, gen_id, immediate=True)
            result = summary(job, gen_id, 'SUBMITTED' if gen_id else 'SUBMISSION_UNKNOWN', balance,
                             error=None if gen_id else data)
            if envelope:
                result['budgetExceeded'] = balance.get('creditsConsumed') is not None and balance['creditsConsumed'] > envelope['maxCredits']
                result['providerEnforcesCeiling'] = False
            return result

        result = tracing.execute(intent["costTrace"], envelope, submit_and_record)
        gen_id = result["generationId"]
    if submit_only or not gen_id:
        return result
    deadline = time.monotonic() + max(poll, 60)
    while True:
        result = resume(film, job)
        if result['status'].upper() in TERMINAL or time.monotonic() >= deadline:
            return result
        time.sleep(8)


def download(film: Path, job: str, gen_id, intent: dict, works: list) -> list[str]:
    _, _, orig = paths(film, job)
    orig.mkdir(parents=True, exist_ok=True)
    outputs = []
    for i, work in enumerate(works, 1):
        url = work.get('url')  # Watermark-free versions require separate approval.
        if not url:
            continue
        ctype = (work.get('contentType') or work.get('content_type') or '').lower()
        ext = '.mp4' if 'video' in ctype or 'mp4' in ctype or '.mp4' in url.lower() else ('.png' if 'png' in url.lower() else '.jpg')
        target = orig / f'{job}_{i}{ext}'
        meta_path = orig / f'{job}_{i}.json'
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else None
        if target.exists() and meta and meta.get('url') == url and meta.get('sha256') == sha256(target):
            outputs.append(str(target.relative_to(film)))
            continue
        fd, temporary = tempfile.mkstemp(prefix=f'.{job}_{i}.', dir=orig)
        os.close(fd)
        temporary = Path(temporary)
        try:
            if urllib.parse.urlsplit(url).scheme != 'https':
                raise ValueError('asset URL must use HTTPS')
            # No auth headers. Bound transfer; never turn a partial download into an original.
            with urllib.request.urlopen(url, timeout=60) as response, temporary.open('wb') as stream:
                if urllib.parse.urlsplit(response.geturl()).scheme != 'https':
                    raise ValueError('asset redirect must use HTTPS')
                total = 0
                while chunk := response.read(1024 * 1024):
                    total += len(chunk)
                    if total > 1024 * 1024 * 1024:
                        raise ValueError('asset exceeds 1 GiB transfer limit')
                    stream.write(chunk)
                if total == 0:
                    raise ValueError('empty asset response')
            digest = sha256(temporary)
            if target.exists():
                if sha256(target) != digest:
                    raise SystemExit(f'{target}: different original exists; refusing overwrite')
            else:
                with temporary.open('rb') as stream:
                    os.fsync(stream.fileno())
                os.link(temporary, target)  # Exclusive: never replace originals.
                sync_dir(orig)
            metadata = {**intent, 'generationId': gen_id,
                        'provenance': 'synthetic', 'approved': False,
                        'sha256': digest, 'url': url}
            metadata.pop('command', None)
            metadata.pop('accountBefore', None)
            if meta is None:
                save(meta_path, metadata)
            elif meta.get('sha256') != digest or meta.get('url') != url:
                raise SystemExit(f'{meta_path}: conflicting metadata; refusing overwrite')
        finally:
            temporary.unlink(missing_ok=True)
        outputs.append(str(target.relative_to(film)))
    return outputs


def resume(film: Path, job: str) -> dict:
    """One query for one stored ID. Never submits; unknown IDs only reconcile."""
    _, res, _ = paths(film, job)
    with locked(film):
        intent_path = res / f'{job}.intent.json'
        if not intent_path.exists():
            raise SystemExit(f'{job}: no stored intent; legacy jobs require manual recovery')
        intent = json.loads(intent_path.read_text())
        submit_path = res / f'{job}.submit.json'
        data = json.loads(submit_path.read_text()) if submit_path.exists() else {}
        gen_id = generation_id(data)
        balance = reconcile(film, job, intent, gen_id)
        if not gen_id:
            return summary(job, None, 'SUBMISSION_UNKNOWN', balance, error=data)
        data = run(['kling', 'query_tasks', gen_id, '-q', *TELEMETRY])
        save(res / f'{job}.response.json', data)
        if data.get('ok') is False:
            return summary(job, gen_id, 'QUERY_ERROR', balance, error=redact(data))
        body = data.get('body') or {}
        if not isinstance(body, dict):
            body = {}
        gens = body.get('generations') or []
        if not isinstance(gens, list):
            gens = []
        generation = next((g for g in gens if isinstance(g, dict) and (g.get('generationId') or g.get('generation_id')) == gen_id), None)
        # Live CLI 0.2.1 returns the queried generation directly in body.
        if generation is None and (body.get('generationId') or body.get('generation_id')) == gen_id:
            generation = body
        # Some CLI responses omit ID when querying exactly one job.
        if generation is None and len(gens) == 1 and isinstance(gens[0], dict) and not (gens[0].get('generationId') or gens[0].get('generation_id')):
            generation = gens[0]
        status = (generation or {}).get('status') or 'QUERY_UNKNOWN'
        if not isinstance(status, str):
            status = 'QUERY_UNKNOWN'
        works = []
        if status.upper() in SUCCESS:
            provider_works = generation.get('works') or (generation.get('result') or {}).get('works') or []
            if not isinstance(provider_works, list) or not any(isinstance(w, dict) and w.get('url') for w in provider_works):
                return summary(job, gen_id, 'RESULT_EMPTY', balance, error='terminal success without artifact URLs')
            works = download(film, job, gen_id, intent, provider_works)
        return summary(job, gen_id, status, balance, works,
                       None if data.get('ok', True) else data)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--film', default='projects/andre-time-travel')
    ap.add_argument('--media-root', type=Path, help='Canonical workspace for read-only reference resolution; no submission grant')
    ap.add_argument('--resolve-reference', help='Resolve one film-relative input and exit without provider calls')
    ap.add_argument('--spec', help='JSON file with job list (submission only)')
    ap.add_argument('--only', help='comma-separated job ids to run')
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--submit-only', action='store_true', help='submit exactly one job, reconcile, never query')
    mode.add_argument('--resume', metavar='JOB', help='query one stored job exactly once; never submit')
    a = ap.parse_args()
    film = (ROOT / a.film).resolve()
    if a.resolve_reference:
        if not a.media_root:
            ap.error('--resolve-reference requires --media-root')
        try:
            media_film = release.shared_media.scoped(a.media_root, a.film, file=False)
            path = resolve_media_input(film, a.resolve_reference, media_root=media_film)
            print(json.dumps({'readOnly': True, 'path': path, 'nativeAccessVerified': None}))
            return 0
        except (OSError, ValueError) as error:
            print(json.dumps({'error': str(error), 'readOnly': True}))
            return 2
    if a.media_root:
        ap.error('shared media submission is not enabled; use the existing canonical producer workflow. No grant, copy or provider call performed')
    if a.resume:
        if a.spec or a.only:
            ap.error('--resume cannot be combined with --spec/--only')
        result = resume(film, a.resume)
        print(json.dumps(result))
        return 2 if result['status'].upper() in {'FAILED', 'CANCELLED', 'CANCELED', 'SUBMISSION_UNKNOWN', 'QUERY_UNKNOWN', 'QUERY_ERROR', 'RESULT_EMPTY'} else 0
    if not a.spec:
        ap.error('--spec is required for submission')
    if not a.submit_only:
        ap.error('submission requires --submit-only; select one job, then use --resume')
    jobs = json.loads(Path(a.spec).read_text(encoding='utf-8'))
    only = set(a.only.split(',')) if a.only else None
    selected = [j for j in jobs if not only or j['job'] in only]
    if only and only != {j['job'] for j in selected}:
        ap.error('--only contains unknown jobs')
    if a.submit_only and len(selected) != 1:
        ap.error('--submit-only requires exactly one selected job')
    for j in selected:
        unknown = set(j) - {'job', 'tool', 'model', 'prompt', 'args', 'images', 'inputs', 'elements',
                            'auth', 'note', 'referenceDurationSeconds', 'submissionBlocked', 'inputFacts'}
        if unknown:
            ap.error('unknown job fields (not forwarded): ' + ', '.join(sorted(unknown)))
        result = submit(film, j['job'], j['tool'], j['model'], j['prompt'], j.get('args', {}),
                        j.get('images', []), j.get('auth'), j.get('note', ''), submit_only=a.submit_only,
                        inputs=j.get('inputs'), elements=j.get('elements'),
                        reference_duration=j.get('referenceDurationSeconds'), submission_blocked=j.get('submissionBlocked'),
                        input_facts=j.get('inputFacts'))
        print(json.dumps(result))
        if result.get('budgetExceeded'):
            print('STOP: cobrança do provedor excedeu o teto local; reconciliar, sem novo envio', file=sys.stderr)
            return 3
        if result['status'].upper() not in ({'SUBMITTED'} if a.submit_only else {'COMPLETED'}):
            print('STOP: non-completed status; no automatic retry', file=sys.stderr)
            return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
