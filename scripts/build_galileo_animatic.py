#!/usr/bin/env python3
"""Render a local still animatic from the selected plan. Never generates remotely.

One lightweight encode, one thread; no overwrite of an existing preview. Source
hashes must match. Labels remain visible; no approval flags or source media change.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import subprocess
import textwrap
from pathlib import Path

import production_plan as production

GEOMETRY = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 640" role="img" aria-label="Geometria proposta de Galileo">
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3z" fill="#dea85c"/></marker></defs>
<rect width="800" height="640" fill="#142027"/><g font-family="sans-serif" fill="#f2ede3">
<text x="40" y="45" font-size="24">GALILEO · GEOMETRIA PROPOSTA</text>
<text x="40" y="76" font-size="15">Vista superior esquemática · D17 pendente · sem escala fotogramétrica</text>
<rect x="190" y="240" width="330" height="205" rx="8" fill="#a17a48"/><text x="215" y="335" font-size="22">Mesa 120 × 75 cm</text>
<text x="247" y="366" font-size="16">altura proposta 75 cm</text>
<circle cx="350" cy="165" r="35" fill="#538b94"/><text x="315" y="116" font-size="21">ANDRE</text>
<circle cx="350" cy="510" r="35" fill="#68707c"/><text x="285" y="568" font-size="21">GALILEO</text>
<path d="M350,202 L350,466" stroke="#f2ede3" stroke-dasharray="8 8"/><text x="535" y="340" font-size="15">eixo de conversa</text>
<path d="M605,509 L377,180" stroke="#dea85c" stroke-width="3" marker-end="url(#arrow)"/>
<rect x="585" y="508" width="52" height="34" rx="4" fill="#dea85c"/>
<text x="575" y="577" font-size="15">Câmera: 50 mm</text><text x="575" y="601" font-size="15">altura 117,5 cm</text>
<text x="40" y="610" font-size="15">No quadro: Andre à esquerda; só ombro histórico à direita. Cabeça fora.</text>
</g></svg>'''


def exclusive(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data.encode() if isinstance(data, str) else data)


def render(root, output):
    from PIL import Image, ImageOps, ImageDraw, ImageFont
    report = production.validate(root, verify_media=True)
    if report['errors']:
        raise ValueError('; '.join(report['errors']))
    _, plan_path, plan = production.plan_source(root)
    if any((output / n).exists() for n in ('animatic.mp4', 'index.html', 'render-evidence.json', 'card-1.png')):
        raise ValueError('preview já existe; criar nova revisão, sem sobrescrever')
    output.mkdir(parents=True, exist_ok=True)
    refs = {r['id']: r for r in plan['references']}
    import csv
    with production.safe(root, 'projects/andre-time-travel/01_script/dialogue-lines.csv').open(newline='') as stream:
        lines = {r['line_id']: r['text_en'] for r in csv.DictReader(stream)}
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    concat = ['ffconcat version 1.0']
    timeline = plan['pilot']['timeline']
    for i, segment in enumerate(timeline, 1):
        reference = refs[segment['referenceId']]
        source = ImageOps.exif_transpose(Image.open(production.safe(root, reference['path']))).convert('RGB')
        source.thumbnail((1280, 566))
        frame = Image.new('RGB', (1280, 720), '#101920')
        frame.paste(source, ((1280-source.width)//2, 58+(566-source.height)//2))
        draw = ImageDraw.Draw(frame)
        draw.text((24, 14), 'GALILEO · PRÉ-VISUALIZAÇÃO CANDIDATA · VOZ-GUIA', font=font, fill='#efc87c')
        draw.text((24, 633), segment['label'], font=small, fill='white')
        line_id = 'G-L03' if i == 1 else ('G-L04' if i == 2 else None)
        if line_id:
            for j, text in enumerate(textwrap.wrap(lines[line_id], width=112)):
                draw.text((24, 659+j*24), text, font=small, fill='#e5e7eb')
        filename = f'card-{i}.png'
        target = output / filename
        with target.open('xb') as stream:
            frame.save(stream, format='PNG')
        concat.extend([f"file '{filename}'", f"duration {segment['endSeconds']-segment['startSeconds']:.6f}"])
    concat.append(f"file 'card-{len(timeline)}.png'")
    exclusive(output/'frames.ffconcat', '\n'.join(concat)+'\n')
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-threads', '1', '-filter_complex_threads', '1',
               '-f', 'concat', '-safe', '0', '-i', str(output/'frames.ffconcat')]
    for audio in plan['pilot']['audio']:
        command.extend(['-i', str(production.safe(root, audio['path']))])
    filters = []
    for i, audio in enumerate(plan['pilot']['audio'], 1):
        delay = round(audio['startSeconds']*1000)
        filters.append(f'[{i}:a]aresample=48000,adelay={delay}:all=1[a{i}]')
    duration = plan['pilot']['durationSeconds']
    filters.append(f'[a1][a2]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,apad,atrim=duration={duration}[audio]')
    command += ['-filter_complex', ';'.join(filters), '-map', '0:v:0', '-map', '[audio]', '-t', str(duration),
                '-r', '24', '-c:v', 'libx264', '-threads', '1', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '160k', '-ac', '2', '-movflags', '+faststart', str(output/'animatic.mp4')]
    subprocess.run(command, check=True, timeout=180, stdin=subprocess.DEVNULL)
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(output/'animatic.mp4')], text=True))
    subprocess.run(['ffmpeg', '-v', 'error', '-threads', '1', '-i', str(output/'animatic.mp4'), '-f', 'null', '-'], check=True, timeout=120, stdin=subprocess.DEVNULL)
    if not (output/'geometry.svg').exists():
        exclusive(output/'geometry.svg', GEOMETRY)
    cards = []
    for s in plan['shots']:
        cards.append(f"<article><h3>{html.escape(s['id']+' · '+s['title'])}</h3><p>{html.escape(s['intention'])}</p><p>{html.escape(s['action'])}</p><p>{html.escape(s['camera'])}</p><p><b>Candidato · checagem/aceite pendentes</b></p></article>")
    page = '''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Galileo · proposta local</title><style>body{margin:auto;max-width:1060px;padding:32px;background:#142027;color:#f2ede3;font:18px/1.6 system-ui}h1,h2{line-height:1.15}small{color:#dec590}video,img{max-width:100%}article{border:1px solid #47525a;border-radius:10px;padding:18px;margin:16px 0}code{overflow-wrap:anywhere}a{color:#efc87c}</style><small>THE TABLE BETWEEN CENTURIES · PRÉ-VISUALIZAÇÃO</small><h1>Uma pergunta. Uma resposta.<br>Depois, a reação.</h1><p>Galileo · G-L03/G-L04 · 16 s · três imagens e dois áudios existentes. Zero geração paga.</p><video controls preload="metadata" src="animatic.mp4"></video><p><strong>Voz-guia e imagens candidatas.</strong> Não é atuação gerada nem prova de lip-sync. Revisão integral por ouvido e aceite de Andre pendentes. O texto inglês permanece intacto.</p><h2>Espaço proposto</h2><img src="geometry.svg" alt="Diagrama da mesa e do eixo, com medidas propostas"><p>Medidas, lente e posição são proposta D17. Cabeça histórica inteira fora do quadro; nenhum novo direito de revelar nuca. IN/OUT ainda precisam de aprovação de semelhança e continuidade.</p><h2>Fichas ligadas ao quadro oficial</h2>'''+''.join(cards)+'''<h2>Fontes e limites</h2><p><a href="visual-review.md">Triagem de 13 imagens</a> · <a href="guide-measurements.json">Medições dos 22 guias</a> · <a href="render-evidence.json">Hash e verificação técnica</a> · <a href="README.md">Decisões pendentes</a></p><p>Fonte canônica: <code>05_storyboard/source/production-plan.json</code>. Board, aprovações, recibos e ledger continuam com seus próprios escopos. O player não aprova mídia.</p></html>'''
    exclusive(output/'index.html', page)
    evidence = {'schemaVersion':'1.0', 'kind':'local_still_animatic', 'sourcePlan':plan_path,
                'sourcePlanSha256':production.sha(production.safe(root,plan_path)),
                'outputSha256':production.sha(output/'animatic.mp4'), 'bytes':(output/'animatic.mp4').stat().st_size,
                'durationSeconds':float(probe['format']['duration']), 'probe':probe,
                'decodePassed':True, 'visualKind':'static_images_with_persistent_labels', 'sourceMediaHashesChecked':True,
                'normalSpeedPlaybackReviewed':False, 'fullListeningReviewed':False, 'lipSyncTested':False,
                'creativeAccepted':False, 'newPaidJobs':0, 'uploads':0,
                'cutsQuantizedToFrameRate':24, 'audioRate':1,
                'limitations':plan['pilot']['limitations']}
    exclusive(output/'render-evidence.json', json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
    return {k:v for k,v in evidence.items() if k != 'probe'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=production.ROOT)
    parser.add_argument('--output',required=True,help='Nova pasta relativa ao workspace')
    args=parser.parse_args()
    output=production.safe(args.root,args.output)
    print(json.dumps(render(args.root,output),ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
