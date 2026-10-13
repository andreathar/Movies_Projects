#!/usr/bin/env python3
"""Data contract: every generated media hash must map back to the asset registry.

Read-only. Never edits the canonical registry; unmapped media get proposal rows
(approved=false, hash recomputed from the file) for the producer to review and append.

  asset_contract.py check [--manifest REL] [--proposal OUT.csv]   exit 2 if any gap
"""
import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILM = ROOT / 'projects/andre-time-travel'
REGISTRY = FILM / 'asset-registry.csv'
DEFAULT_MANIFEST = FILM / '05_storyboard/keyframes/detail-studies-v1/manifest.json'
HEADER = ['asset_id', 'kind', 'path_or_provider_id', 'path_base', 'source', 'sha256', 'approved', 'notes']
PROPOSED_KIND = 'synthetic_detail_study_candidate'  # new kind: needs producer sign-off


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def registry_index(path=REGISTRY):
    with path.open(newline='', encoding='utf-8') as f:
        rows = [r for r in csv.DictReader(f) if r.get('sha256')]
    return {r['sha256']: r for r in rows}


def check(manifest_path=DEFAULT_MANIFEST, registry=REGISTRY, root=ROOT):
    manifest = json.loads(Path(manifest_path).read_text())
    index = registry_index(registry)
    report = {'manifest': str(Path(manifest_path).relative_to(root)), 'images': 0, 'mapped': 0,
              'unregistered': [], 'hash_mismatch': [], 'missing_file': [], 'reference_unregistered': []}
    seen_refs = set()
    for image in manifest['images']:
        report['images'] += 1
        file = root / image['path']
        if not file.is_file():
            report['missing_file'].append(image['path']); continue
        actual = sha256(file)
        if actual != image['sha256']:
            report['hash_mismatch'].append({'path': image['path'], 'manifest': image['sha256'], 'actual': actual}); continue
        if actual in index:
            report['mapped'] += 1
        else:
            report['unregistered'].append({'name': image['name'], 'path': image['path'], 'sha256': actual,
                                           'status': image.get('status'), 'productionAccepted': image.get('productionAccepted')})
        for ref in image.get('references', []):
            if ref['sha256'] not in index and ref['sha256'] not in seen_refs:
                seen_refs.add(ref['sha256'])
                report['reference_unregistered'].append(ref)
    report['ok'] = not (report['unregistered'] or report['hash_mismatch'] or report['missing_file'])
    return report


def proposal_rows(report, film=FILM, root=ROOT):
    rows = []
    for item in report['unregistered']:
        rel = str((root / item['path']).relative_to(film))
        rows.append({'asset_id': 'DS-' + item['name'], 'kind': PROPOSED_KIND, 'path_or_provider_id': rel,
                     'path_base': 'film', 'source': 'detail-studies-v1 manifest.json (decision D20); built-in image generation, billing not exposed',
                     'sha256': item['sha256'], 'approved': 'false',
                     'notes': 'Candidate only; productionAccepted=false. Proposed by asset_contract.py, not yet appended.'})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=['check'])
    ap.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument('--proposal', type=Path, help='write proposed registry rows here (never the canonical file)')
    args = ap.parse_args(argv)
    report = check(args.manifest if args.manifest.is_absolute() else ROOT / args.manifest)
    if args.proposal:
        if args.proposal.resolve() == REGISTRY.resolve():
            ap.error('proposal must not target the canonical registry')
        with args.proposal.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, HEADER); w.writeheader(); w.writerows(proposal_rows(report))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report['ok'] else 2


if __name__ == '__main__':
    sys.exit(main())
