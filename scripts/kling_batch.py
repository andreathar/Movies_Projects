#!/usr/bin/env python3
"""Producer-only CLI runner. Submit once; interactive resume queries once.

Intent is durable before submission. Uncertain submissions are never retried.
Balance snapshots and ledger updates precede polling/downloads. Batch polling is
retained only for the original interface (without --submit-only/--resume).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import fcntl
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TELEMETRY = ["--skill-name", "kling-cli", "--skill-version", "0.2.1"]
TERMINAL = {"COMPLETED", "PARTIAL_COMPLETED", "SUCCEED", "FAILED", "CANCELLED"}


def run(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(proc.stdout)
        if not isinstance(data, dict):
            data = {"ok": False, "parsed": data}
    except json.JSONDecodeError:
        data = {"ok": False}
    # Keep the exact CLI response, including parse failures and nonzero exits.
    data['_cli'] = {"stdout": proc.stdout, "stderr": proc.stderr, "rc": proc.returncode}
    if proc.returncode:
        data['ok'] = False
    return data


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
            balance['creditsDelta'] if balance['creditsDelta'] is not None else '',
            f"reconciled_from_balance_delta ({balance['balanceBefore']}->{balance['balanceAfter']}); {balance['reconciliation']}; submission {'known_id' if gen_id else 'unknown_id'}",
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
           *, submit_only: bool = False) -> dict:
    req, res, _ = paths(film, job)
    with locked(film):
        if any((res / f'{job}.{kind}.json').exists() for kind in ('response', 'submit', 'intent')):
            raise SystemExit(f'{job}: submission evidence already exists; never resubmit')
        if not auth:
            raise SystemExit('explicit authorization reference is required')
        cmd = ['kling', tool, '--model', model, '--poll', '0', '-q', *TELEMETRY,
               '--rationale', f'Film reference batch {auth}: {note}']
        for img in images:
            p = None if img.startswith(('http://', 'https://')) else film / img
            if p is not None and not p.is_file():
                raise SystemExit(f'missing reference: {img}')
            cmd += ['--image', str(p) if p else img]
        for key, value in args.items():
            if key in {'poll', 'model', 'rationale'}:
                raise SystemExit(f'reserved option: {key}')
            cmd += [f'--{key}', str(value)]
        cmd.append(prompt)
        snapshot = {}
        before = account(snapshot)
        if before is None:
            raise SystemExit('balance unavailable; no submission made')
        intent = {'job': job, 'tool': tool, 'model': model, 'prompt': prompt,
                  'options': args, 'refs': images, 'auth': auth, 'note': note,
                  'balanceBefore': before, 'accountBefore': snapshot, 'command': cmd,
                  'created': dt.datetime.now().astimezone().isoformat(timespec='seconds')}
        prompt_path = req / f'{job}.prompt.txt'
        if prompt_path.exists() and prompt_path.read_text() != prompt + '\n':
            raise SystemExit('existing prompt differs; refusing overwrite')
        if not prompt_path.exists():
            durable(prompt_path, prompt + '\n')
        save(res / f'{job}.intent.json', intent)
        try:
            data = run(cmd)
        except Exception as exc:
            data = {'ok': False, 'error': str(exc), 'submissionUncertain': True}
        save(res / f'{job}.submit.json', data)
        gen_id = generation_id(data)
        balance = reconcile(film, job, intent, gen_id, immediate=True)
        result = summary(job, gen_id, 'SUBMITTED' if gen_id else 'SUBMIT_FAILED', balance,
                         error=None if gen_id else data)
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
            urllib.request.urlretrieve(url, temporary)
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
                        'provenance': 'synthetic_fictional_casting', 'approved': False,
                        'sha256': digest, 'url': url}
            metadata.pop('command', None)
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
        works = []
        if status.upper() in {'COMPLETED', 'PARTIAL_COMPLETED', 'SUCCEED'}:
            provider_works = generation.get('works') or (generation.get('result') or {}).get('works') or []
            works = download(film, job, gen_id, intent, provider_works)
        return summary(job, gen_id, status, balance, works,
                       None if data.get('ok', True) else data)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--film', default='projects/andre-time-travel')
    ap.add_argument('--spec', help='JSON file with job list (submission only)')
    ap.add_argument('--only', help='comma-separated job ids to run')
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--submit-only', action='store_true', help='submit exactly one job, reconcile, never query')
    mode.add_argument('--resume', metavar='JOB', help='query one stored job exactly once; never submit')
    a = ap.parse_args()
    film = (ROOT / a.film).resolve()
    if a.resume:
        if a.spec or a.only:
            ap.error('--resume cannot be combined with --spec/--only')
        result = resume(film, a.resume)
        print(json.dumps(result))
        return 2 if result['status'].upper() in {'FAILED', 'CANCELLED', 'SUBMISSION_UNKNOWN', 'QUERY_UNKNOWN'} else 0
    if not a.spec:
        ap.error('--spec is required for submission')
    jobs = json.loads(Path(a.spec).read_text(encoding='utf-8'))
    only = set(a.only.split(',')) if a.only else None
    selected = [j for j in jobs if not only or j['job'] in only]
    if only and only != {j['job'] for j in selected}:
        ap.error('--only contains unknown jobs')
    if a.submit_only and len(selected) != 1:
        ap.error('--submit-only requires exactly one selected job')
    for j in selected:
        result = submit(film, j['job'], j['tool'], j['model'], j['prompt'], j.get('args', {}),
                        j.get('images', []), j['auth'], j.get('note', ''), submit_only=a.submit_only)
        print(json.dumps(result))
        if result['status'].upper() not in ({'SUBMITTED'} if a.submit_only else {'COMPLETED'}):
            print('STOP: non-completed status; no automatic retry', file=sys.stderr)
            return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
