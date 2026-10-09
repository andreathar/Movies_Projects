#!/usr/bin/env python3
"""Reproduce the v2 review candidate; refuses to overwrite any output."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REVIEW = Path('08_edit/reviews/galileo-en-v2')
FPS = 24
OUT = Path('08_edit/picture-lock/galileo-en-preview-v2.mp4')
TIMELINE = Path('08_edit/timelines/galileo-en-v2.json')
INSERT = '07_generations/originals/G-01-insert-galileo-v2_1.mp4'
SPEECH = '07_generations/originals/G-02-andre-GL02_1.mp4'
EYES_A = '07_generations/originals/G-03-eyes-galileo-A_1.mp4'
EYES_B = '07_generations/originals/G-05-eyes-galileo-B_1.mp4'
PILOT4 = '06_pilot/originals/PILOT-04-galileo-speech-native_1.mp4'
PILOT2 = '06_pilot/originals/PILOT-02-galileo-gentle-turn_1.mp4'
STEMS = Path('04_audio/stems/dialogue/galileo-guide-v1')


def digest(path):
    with (ROOT / path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path, data):
    with (ROOT / path).open('x') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ffmpeg', default='ffmpeg')
    parser.add_argument('--ffprobe', default='ffprobe')
    args = parser.parse_args()
    for output in [OUT, TIMELINE, REVIEW / 'baseline.json', REVIEW / 'guide-mix.wav']:
        if (ROOT / output).exists():
            raise SystemExit(f'Refusing existing output: {output}')
    log = []

    def run(argv, name):
        result = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True)
        with (ROOT / REVIEW / f'{name}.log').open('x') as stream:
            stream.write(result.stderr)
        log.append({'name': name, 'command': argv, 'exitCode': result.returncode})
        if result.returncode:
            write_json(REVIEW / 'failed-build.json', log)
            raise RuntimeError(f'{name} failed: {result.stderr[-1500:]}')
        return result.stdout

    media = [INSERT, SPEECH, EYES_A, EYES_B, PILOT4, PILOT2]
    stems = [str(STEMS / f'G-L0{i}.wav') for i in range(1, 5)]
    protected = [
        'manifest.json', 'tasks/board.json', '00_brief/approvals.json',
        'credit-ledger.csv', 'memory/STATE.md',
        '08_edit/timelines/galileo-en-v1.json',
        '08_edit/picture-lock/galileo-en-preview-v1.mp4',
        '08_edit/subtitles/galileo-en-v1.srt',
        'docs/checkpoint-2026-10-09-galileo-retomada.md',
        'docs/2026-10-09-direcao-encontros-fala-dificil.md',
        str(STEMS / 'room-tail.wav'), str(STEMS / 'galileo-guide-mix.wav'),
    ] + sorted(str(p.relative_to(ROOT)) for p in (ROOT / '00_brief/decisions').glob('*') if p.is_file())
    before = {p: digest(p) for p in dict.fromkeys(media + stems + protected)}
    write_json(REVIEW / 'baseline.json', {'pathBase': 'film-root', 'sha256': before})

    # The 22.8 / 30.8-second picture boundaries round to the nearest 24-fps frame.
    # Audio G-L04 remains at exactly 22.800 s: only 8.333 ms after its picture cut.
    specs = [
        ('E01', 'G-01', INSERT, 0, 96, 'Opening tabletop insert'),
        ('E02', 'G-02', SPEECH, 0, 288, 'Complete G-L02 at original speed; frontal substitute for G-X02'),
        ('E03', 'G-03', EYES_A, 0, 48, '2 s reaction after the G-L02 motivating statement'),
        ('E04', 'G-04', INSERT, 96, 115, 'Tabletop placeholder for unavailable G-X01; G-L03 offscreen at 20 s'),
        ('E05', 'G-04', PILOT4, 0, 192, 'Complete G-L04, same recording repositioned to 22.8 s'),
        ('E06', 'G-05', EYES_B, 0, 48, '2 s reaction after the final G-L04 statement'),
        ('E07', 'G-06', INSERT, 48, 17, 'Approved insert fill completing the original 30.8-33.5 window'),
        ('E08', 'G-06', INSERT, 65, 120, 'Contiguous tabletop silence; no false back-view claim'),
        ('E09', 'G-07', PILOT2, 36, 72, 'Provisional respect/listening shot; known different table/seat, not G-X01'),
        ('E10', 'G-06', INSERT, 216, 12, 'Final half-second cut back to the table'),
    ]
    events = []
    cursor = 0
    for ident, slot, path, source_frame, count, purpose in specs:
        events.append({
            'id': ident, 'slot': slot, 'path': path,
            'sourceSha256': before[path], 'sourceInFrame': source_frame,
            'sourceIn': source_frame / FPS, 'frameCount': count,
            'timelineStartFrame': cursor, 'timelineEndFrameExclusive': cursor + count,
            'timelineStart': cursor / FPS, 'duration': count / FPS,
            'playbackRate': 1.0, 'purpose': purpose,
            'historicalFramingRisk': path in [INSERT, EYES_A, EYES_B],
        })
        cursor += count
    assert cursor == 1008
    starts = [0.5, 4.0, 20.0, 22.8]
    durations = [2.47, 12.0, 2.83, 8.0]
    dialogue = [
        {'lineId': f'G-L0{i+1}', 'path': path, 'sourceSha256': before[path],
         'timelineStart': start, 'sourceIn': 0, 'duration': duration, 'playbackRate': 1.0}
        for i, (path, start, duration) in enumerate(zip(stems, starts, durations))
    ]
    timeline = {
        'revision': 'galileo-en-v2', 'pathBase': 'film-root',
        'purpose': 'Review candidate with guide voices and explicit existing-take placeholders; NOT accepted picture',
        'sourceCheckpoint': 'docs/checkpoint-2026-10-09-galileo-retomada.md#5',
        'assignment': 'Parley operator message 3',
        'timingClarification': {
            'source': 'Andre direct answer in this session, 2026-10-09',
            'quote': 'Seguir a ordem da v2, reposicionar G-L04 sem alterar a gravação e limitar olhos B a 2 s, completando com insert.',
            'scope': 'This derived edit only; no canonical decision record or production approval created',
        },
        'fps': FPS, 'targetSeconds': 42, 'frameCount': cursor,
        'outputWidth': 1920, 'outputHeight': 1080,
        'pictureEvents': events, 'dialogue': dialogue,
        'audio': {
            'recordings': 'Existing v1 normalized guide WAVs, byte-identical inputs; no new speech, word edits or speed changes',
            'mix': str(REVIEW / 'guide-mix.wav'),
            'mixMethod': 'Same v1 amix/room-tail/loudnorm recipe; only G-L04 delay changed from 25500 to 22800 ms',
            'mixIsBitIdenticalToV1': False, 'mixTargetLufs': -16, 'targetTruePeakDb': -1,
            'guideRecordingChanged': False, 'music': False,
            'pictureAudioOffsetMsForGL04': 1000 * (22.8 - 547 / 24),
            'nominalGL03GL04TrackOverlapSeconds': 0.03,
        },
        'subtitles': str(REVIEW / 'galileo-en-v2.srt'), 'output': str(OUT),
        'normalization': '24 fps source speed unchanged, aspect preserved and padded to 1920x1080, no zoom/crop, H.264 yuv420p',
        'fullPlaybackCompleted': False, 'voiceApproved': False, 'finalPictureApproved': False,
        'status': 'review_candidate_pending_frame_qc_and_normal_speed_playback',
        'limitations': [
            'G-X01/G-X02 absent: shared-space/back-view coverage remains unproven. Tabletop inserts are placeholders, not back-view footage.',
            'PILOT-02 final listening placeholder has the known table/seat mismatch F01.',
            'G-L04 doubtful guide pronunciation is preserved; canonical subtitles are not transcript certification.',
            'Eyes B now follows the final statement; relocating G-L04 means it no longer overlays the words as written in the old checkpoint.',
            '22.8 and 30.8 picture boundaries are quantized to 22.791667 and 30.791667 at 24 fps; no temporal acceleration.',
            'Final 38.5-42 window uses 3 s of PILOT-02 followed by a 0.5 s cut to the table.',
            'Upscaled review export from 720p-class sources; original provider watermarks retained.',
            'Normal-speed playback and acceptance by Andre remain outstanding.',
        ],
    }
    write_json(TIMELINE, timeline)

    # Preserve caption text; move only G-L04 entries with its existing recording.
    def seconds(value):
        h, m, s, ms = map(int, re.split('[:,]', value))
        return h * 3600 + m * 60 + s + ms / 1000

    def stamp(value):
        total = round(value * 1000)
        return f'{total//3600000:02}:{total//60000%60:02}:{total//1000%60:02},{total%1000:03}'

    blocks = (ROOT / '08_edit/subtitles/galileo-en-v1.srt').read_text().strip().split('\n\n')
    for index, block in enumerate(blocks):
        lines = block.splitlines()
        begin, end = [seconds(s) for s in lines[1].split(' --> ')]
        if begin >= 25.5:
            begin -= 2.7
            end -= 2.7
        if index == 4:
            end = min(end, 22.8)  # Avoid a 30 ms caption overlap, without trimming the recording.
        lines[1] = f'{stamp(begin)} --> {stamp(end)}'
        blocks[index] = '\n'.join(lines)
    with (ROOT / REVIEW / 'galileo-en-v2.srt').open('x') as stream:
        stream.write('\n\n'.join(blocks) + '\n')

    audio_cmd = [args.ffmpeg, '-n', '-hide_banner', '-nostdin']
    for stem in stems:
        audio_cmd += ['-i', stem]
    audio_cmd += ['-stream_loop', '-1', '-i', str(STEMS / 'room-tail.wav')]
    audio_filters = [f'[{i}:a]adelay={round(start*1000)}:all=1,apad,atrim=duration=42[a{i}]' for i, start in enumerate(starts)]
    audio_filters += ['[4:a]volume=0.25,atrim=duration=42[bed]', '[a0][a1][a2][a3][bed]amix=inputs=5:normalize=0,loudnorm=I=-16:TP=-1:LRA=7,atrim=duration=42[mix]']
    audio_cmd += ['-filter_complex', ';'.join(audio_filters), '-map', '[mix]', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', str(REVIEW / 'guide-mix.wav')]
    run(audio_cmd, 'audio-build')
    print('Guide mix rendered from unchanged source recordings.', flush=True)

    # Normalize each event into a new review-only intermediate; no original is rewritten.
    segments = ROOT / REVIEW / 'segments'
    segments.mkdir()
    segment_paths = []
    for event in events:
        rel = REVIEW / 'segments' / f"{event['id']}.mp4"
        start = event['sourceInFrame']
        count = event['frameCount']
        filters = f'trim=start_frame={start}:end_frame={start+count},setpts=PTS-STARTPTS,scale=1920:1080:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p'
        run([args.ffmpeg, '-n', '-hide_banner', '-nostdin', '-threads', '4', '-i', event['path'], '-map', '0:v:0', '-an', '-vf', filters, '-frames:v', str(count), '-c:v', 'libx264', '-threads', '4', '-preset', 'fast', '-crf', '18', str(rel)], f"segment-{event['id']}")
        segment_paths.append(rel)
        print(f"Rendered {event['id']}: {count} frames", flush=True)

    picture_cmd = [args.ffmpeg, '-n', '-hide_banner', '-nostdin', '-filter_complex_threads', '2']
    for segment in segment_paths:
        picture_cmd += ['-threads', '2', '-i', str(segment)]
    picture_cmd += ['-i', str(REVIEW / 'guide-mix.wav'), '-i', str(REVIEW / 'galileo-en-v2.srt')]
    filters = [f'[{i}:v]setpts=PTS-STARTPTS[v{i}]' for i in range(len(events))]
    filters.append(''.join(f'[v{i}]' for i in range(len(events))) + f'concat=n={len(events)}:v=1:a=0[picture]')
    picture_cmd += ['-filter_complex', ';'.join(filters), '-map', '[picture]', '-map', f'{len(events)}:a:0', '-map', f'{len(events)+1}:s:0', '-c:v', 'libx264', '-threads', '6', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '24', '-c:a', 'aac', '-b:a', '192k', '-c:s', 'mov_text', '-metadata:s:s:0', 'language=eng', '-metadata', 'title=Galileo v2 - review candidate - guide voices and placeholders', '-movflags', '+faststart', '-t', '42', str(OUT)]
    run(picture_cmd, 'picture-build')
    print('Preview rendered; checking exact output.', flush=True)
    probe = json.loads(run([args.ffprobe, '-v', 'error', '-count_frames', '-show_format', '-show_streams', '-of', 'json', str(OUT)], 'ffprobe'))
    write_json(REVIEW / 'ffprobe.json', probe)
    video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    assert int(video['nb_read_frames']) == 1008
    assert video['r_frame_rate'] == '24/1'
    assert (video['width'], video['height']) == (1920, 1080)
    assert float(probe['format']['duration']) == 42.0
    run([args.ffmpeg, '-v', 'error', '-i', str(OUT), '-f', 'null', '-'], 'decode')
    run([args.ffmpeg, '-hide_banner', '-i', str(OUT), '-filter_complex', 'ebur128=peak=true', '-f', 'null', '-'], 'loudness')
    after = {p: digest(p) for p in before}
    assert before == after, 'An input or protected file changed during the build'
    write_json(REVIEW / 'preservation.json', {'allBaselineHashesUnchanged': True, 'filesChecked': len(before), 'sha256': after})
    write_json(REVIEW / 'build-log.json', log)
    write_json(REVIEW / 'build-result.json', {
        'output': str(OUT), 'sha256': digest(OUT), 'timeline': str(TIMELINE),
        'timelineSha256': digest(TIMELINE), 'durationSeconds': 42, 'decodedFrames': 1008,
        'decodeExitCode': 0, 'inputsUnchanged': True, 'visualReviewCompleted': False,
        'normalSpeedPlaybackCompleted': False, 'accepted': False,
    })
    print(json.dumps({'output': str(OUT), 'sha256': digest(OUT), 'decodedFrames': 1008}), flush=True)


if __name__ == '__main__':
    main()
