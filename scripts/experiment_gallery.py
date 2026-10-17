#!/usr/bin/env python3
"""Publish/check a metadata-only experiment gallery; never copy or generate media."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path

FILM = 'projects/andre-time-travel'
V1 = FILM + '/07_generations/downloads/2026-10-15-element-experiments-v1'
V2 = FILM + '/07_generations/downloads/2026-10-15-element-experiments-v2'
GUIDE = FILM + '/docs/kling-element-experiments-20261017-v3.md'


def unique(items, label):
    result = {}
    for item in items:
        key = item['asset_id']
        if not isinstance(key, str) or not key or key in result:
            raise ValueError(f'Duplicate/missing {label} asset ID: {key}')
        result[key] = item
    return result


def join_records(resources, observations, analyses):
    """Join by stable identity, refusing incomplete/contradictory source evidence."""
    media = unique(resources, 'resource')
    reviews = unique(observations, 'observation')
    metrics = unique(analyses, 'analysis')
    if set(reviews) != set(metrics):
        raise ValueError('Observation/analysis asset IDs differ')
    joined = []
    for key, review in reviews.items():
        if key not in media:
            raise ValueError(f'Missing resource: {key}')
        resource, analysis = media[key], metrics[key]
        if (resource['path'], resource['sha256']) != (
            analysis['sourcePath'], analysis['sourceSHA256']
        ):
            raise ValueError(f'Resource/analysis identity mismatch: {key}')
        if review['frames'] != analysis['decodedFrames']:
            raise ValueError(f'Frame count mismatch: {key}')
        joined.append({'asset_id': key, 'resource': resource,
                       'observation': review, 'analysis': analysis})
    return joined


def local(root, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError(f'Nonlocal path: {relative}')
    full = root / path
    if not full.resolve().is_relative_to(root):
        raise ValueError(f'Path escapes workspace: {relative}')
    return full


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_index(gallery, output):
    def url(relative):
        return html.escape(os.path.relpath(relative, output), quote=True)
    def esc(value):
        return html.escape(str(value), quote=True)
    lines = ['<!doctype html><html lang="pt-BR"><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Experimentos Kling · apresentação corrigida v3</title>',
             '<style>body{font:16px system-ui;max-width:1100px;margin:32px auto;padding:0 20px;background:#121821;color:#e9eef5}a{color:#9ac9ff}video,img{max-width:100%;max-height:540px}article{border:1px solid #475367;padding:20px;margin:24px 0;border-radius:12px}code{overflow-wrap:anywhere}</style>',
             '<h1>Experimentos Kling · apresentação corrigida v3</h1>',
             '<p>Correção técnica de associação por asset ID; nenhum novo arquivo de mídia, aceite ou gasto. Observações e limites herdados da revisão de 15/10, sem novo playback ou escuta.</p>',
             '<nav>' + ' · '.join('<a href="'+url(p)+'">'+esc(label)+'</a>' for label,p in [
                 ('Galeria v1 histórica', V1+'/index.html'),
                 ('Galeria v2 histórica (associações corrigidas aqui)', V2+'/index.html'),
                 ('Lições e correção', GUIDE), ('Mapa com hashes', output+'/gallery.json'),
                 ('Prompts históricos', V2+'/prompts.json'),
                 ('Observações originais', V2+'/review.json')]) + '</nav>',
             '<h2>Referências de figurino (candidatas)</h2>']
    for item in gallery['costumeReferences']:
        lines.append('<p><a href="'+url(item['path'])+'">'+esc(item['asset_id'])+'</a> · '+esc(item['resourceName'])+'</p>')
    for card in gallery['videos']:
        key = esc(card['asset_id'])
        lines.extend(['<article data-asset-id="'+key+'"><h2>'+key+'</h2>',
                      '<video controls preload="none" src="'+url(card['video']['path'])+'"></video>',
                      '<p>SHA-256: <code>'+card['video']['sha256']+'</code></p>',
                      '<p>'+esc(card['observation']['observed'])+'</p>',
                      '<p><strong>Limites da revisão herdada:</strong> '+esc(card['observation']['limits'])+'</p>'])
        if card['audio']:
            lines.append('<p>Áudio derivado do mesmo asset ID (escuta não validada): <audio controls preload="none" src="'+url(card['audio']['path'])+'"></audio></p>')
        if card['asr']:
            lines.append('<p><a href="'+url(card['asr']['path'])+'">Hipótese ASR histórica, não validada</a></p>')
        lines.append('<details><summary>Folhas estáticas históricas do mesmo asset ID</summary>')
        for sheet in card['sheets']:
            lines.append('<a href="'+url(sheet['path'])+'"><img loading="lazy" src="'+url(sheet['path'])+'" alt="Quadros '+str(sheet['firstFrame'])+'–'+str(sheet['lastFrame'])+'"></a>')
        lines.append('</details></article>')
    lines.append('</html>')
    return ('\n'.join(lines)+'\n').encode()


def build(root, output):
    root = Path(root).resolve()
    local(root, output)
    sources = []
    def read(relative):
        path = local(root, relative)
        sources.append({'path': relative, 'sha256': fingerprint(path)})
        return json.loads(path.read_text())
    def ref(relative):
        return {'path': relative, 'sha256': fingerprint(local(root, relative))}
    manifests = [read(V1+'/manifest.json'), read(V2+'/manifest.json')]
    review = read(V2+'/review.json')
    analyses = read(V2+'/evidence/analysis.json') + read(V2+'/evidence/local-analysis.json')
    resources = [r for manifest in manifests for r in manifest['resources']]
    joined = join_records(resources, review['observations'], analyses)
    for resource in resources:
        if fingerprint(local(root, resource['path'])) != resource['sha256']:
            raise ValueError('Resource hash mismatch: '+resource['asset_id'])
    cards = []
    for item in joined:
        key, analysis = item['asset_id'], item['analysis']
        sheets, next_frame = [], 0
        for sheet in analysis['sheets']:
            if not sheet['path'].startswith('temporal/'+key+'/') or sheet['firstFrame'] != next_frame:
                raise ValueError('Sheet identity/coverage mismatch: '+key)
            sheets.append({**ref(V2+'/review/'+sheet['path']),
                           'firstFrame': sheet['firstFrame'], 'lastFrame': sheet['lastFrame']})
            next_frame = sheet['lastFrame']+1
        if next_frame != analysis['decodedFrames']:
            raise ValueError('Incomplete sheet coverage: '+key)
        audio = V2+'/review/temporal/'+key+'/audio.wav'
        asr = V2+'/review/temporal/'+key+'/asr.json'
        cards.append({'asset_id': key, 'video': ref(item['resource']['path']),
                      'observation': item['observation'], 'sheets': sheets,
                      'audio': ref(audio) if local(root,audio).is_file() else None,
                      'asr': ref(asr) if local(root,asr).is_file() else None})
    gallery = {'schemaVersion': 1, 'kind': 'experiment_gallery_identity_correction',
               'sources': sources, 'supersedesPresentation': V2+'/index.html',
               'supersessionScope': 'presentation joins only; historical observations, reviews and ingestion remain unchanged',
               'approved': False, 'newMediaFiles': 0, 'normalSpeedPlaybackWatched': False,
               'actualAudioListening': False, 'inheritedReview': V2+'/review.json',
               'videos': cards, 'costumeReferences': [r for r in resources if r.get('elementId')=='324019350521447']}
    readme = ('# Apresentação de experimentos v3\n\nAbrir index.html localmente. Corrige somente associações de apresentação por asset ID. '
              'gallery.json registra fontes e hashes. Não é um novo lote de mídia nem aceite; v1/v2 permanecem como evidência histórica. '
              'Vídeo, folhas, áudio e ASR apontam aos arquivos existentes do mesmo ID; observações são herdadas sem nova revisão temporal/escuta. '
              'Fonte reproduzível: scripts/experiment_gallery.py --output '+output+' --check.\n')
    return {'gallery.json': (json.dumps(gallery,ensure_ascii=False,indent=2)+'\n').encode(),
            'index.html': render_index(gallery,output), 'README.md': readme.encode()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output',required=True)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    outputs = build(args.root,args.output)
    dest = local(args.root.resolve(),args.output)
    if args.check:
        if any(not (dest/n).is_file() or (dest/n).read_bytes()!=data for n,data in outputs.items()):
            raise ValueError('Gallery drift; publish a new revision rather than overwrite history')
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,data in outputs.items():
            with (dest/name).open('xb') as stream:
                stream.write(data)
    print(json.dumps({'status':'ok','check':args.check,'files':list(outputs),'newMediaFiles':0}))


if __name__ == '__main__':
    main()
