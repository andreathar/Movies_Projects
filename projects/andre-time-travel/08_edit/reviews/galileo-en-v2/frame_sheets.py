#!/usr/bin/env python3
"""Extract every final frame to numbered bounded sheets, without altering media."""
import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
REVIEW = Path('08_edit/reviews/galileo-en-v2')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ffmpeg', default='ffmpeg')
    args = parser.parse_args()
    timeline = json.loads((ROOT / '08_edit/timelines/galileo-en-v2.json').read_text())
    destination = ROOT / REVIEW / 'frames'
    destination.mkdir()
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    tile_width, tile_height = 400, 225
    cell_height = tile_height + 24
    frame_bytes = tile_width * tile_height * 3
    manifest = []
    command = [args.ffmpeg, '-v', 'error', '-i', timeline['output'], '-map', '0:v:0', '-an', '-vf', f'scale={tile_width}:{tile_height}', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    with (destination / 'decode.log').open('x') as errors:
        process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=errors)
        index = 0
        sheet = None
        frames = []
        joins = []
        boundaries = {0, timeline['frameCount'] - 1}
        for event in timeline['pictureEvents']:
            boundaries.update([event['timelineStartFrame'], event['timelineEndFrameExclusive'] - 1])
        while True:
            raw = process.stdout.read(frame_bytes)
            if not raw:
                break
            if len(raw) != frame_bytes:
                raise RuntimeError('Incomplete decoded frame')
            tile = Image.frombytes('RGB', (tile_width, tile_height), raw)
            event = next(e for e in timeline['pictureEvents'] if e['timelineStartFrame'] <= index < e['timelineEndFrameExclusive'])
            if index % 40 == 0:
                sheet = Image.new('RGB', (tile_width * 5, cell_height * 8), '#151515')
                frames = []
            x = index % 5 * tile_width
            y = (index % 40 // 5) * cell_height
            sheet.paste(tile, (x, y))
            ImageDraw.Draw(sheet).text((x + 5, y + tile_height + 2), f"f{index:04d} {index/24:.3f}s {event['id']} {'RISK' if event['historicalFramingRisk'] else 'ANDRE'}", font=font, fill='white')
            frames.append(index)
            if index in boundaries:
                joins.append((index, event['id'], tile.copy()))
            if index % 40 == 39 or index == timeline['frameCount'] - 1:
                name = f'frames-{frames[0]:04d}-{frames[-1]:04d}.png'
                sheet.save(destination / name)
                manifest.append({'path': str(REVIEW / 'frames' / name), 'frames': frames, 'tileWidth': tile_width, 'tileHeight': tile_height, 'columns': 5})
            index += 1
        assert process.wait() == 0
        assert index == timeline['frameCount'] == 1008
    sheet = Image.new('RGB', (tile_width * 5, cell_height * ((len(joins) + 4) // 5)), '#151515')
    for pos, (index, event, tile) in enumerate(joins):
        x, y = pos % 5 * tile_width, pos // 5 * cell_height
        sheet.paste(tile, (x, y))
        ImageDraw.Draw(sheet).text((x + 5, y + tile_height + 2), f'f{index:04d} {index/24:.3f}s {event}', font=font, fill='white')
    sheet.save(destination / 'joins.png')
    with (destination / 'index.json').open('x') as stream:
        json.dump({'decodedFrames': index + 1, 'sheets': manifest, 'method': 'Every decoded final frame, sequentially numbered; frame inspection is not normal-speed playback'}, stream, indent=2)
    print(json.dumps({'sheets': len(manifest), 'frames': 1008, 'path': str(REVIEW / 'frames')}))


if __name__ == '__main__':
    main()
