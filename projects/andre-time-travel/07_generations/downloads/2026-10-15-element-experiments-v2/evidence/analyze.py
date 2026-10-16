import pathlib,json,subprocess,math,datetime,re,sys
from PIL import Image,ImageDraw,ImageStat,ImageChops,ImageOps
from fractions import Fraction
R=pathlib.Path('/mnt/data/Projects_SSD/Movies_Projects');T=pathlib.Path('/tmp/kling-batch2-20261015');V=T/'temporal';V.mkdir(exist_ok=True)
old=json.loads((R/'projects/andre-time-travel/07_generations/downloads/2026-10-15-element-experiments-v1/manifest.json').read_text());videos=[x for x in old['resources'] if x['path'].endswith('.mp4') and x['role']!='voice'];report=[]
if '--local-only' in sys.argv:videos=[json.loads((T/'local-kungfu.json').read_text())]
for x in videos:
 aid=x['asset_id'];f=R/x['path'];D=V/aid;D.mkdir(exist_ok=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(f)]));s=next(s for s in probe['streams'] if s['codec_type']=='video');rate=float(Fraction(s['avg_frame_rate']));expected=int(s['nb_read_frames']);w=256;hh=144;tileh=165
 p=subprocess.Popen(['ffmpeg','-v','error','-i',str(f),'-map','0:v:0','-vf',f'scale={w}:{hh}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 sheet=None;sheets=[];index=0;prev=None;scores=[]
 while True:
  data=p.stdout.read(w*hh*3)
  if not data:break
  assert len(data)==w*hh*3
  im=Image.frombytes('RGB',(w,hh),data)
  if index%40==0:sheet=Image.new('RGB',(w*5,tileh*8),'#191919');draw=ImageDraw.Draw(sheet)
  xx=(index%40%5)*w;yy=(index%40//5)*tileh;sheet.paste(im,(xx,yy));draw.text((xx+3,yy+hh+2),f'f{index:03d} {index/rate:05.2f}s',fill='white')
  grey=im.convert('L')
  if prev is not None:scores.append(dict(frame=index,seconds=index/rate,meanAbsoluteDifference=sum(ImageStat.Stat(ImageChops.difference(prev,grey)).mean)/255))
  prev=grey
  if index%40==39 or index==expected-1:
   start=index-index%40;path=D/f'frames-{start:03d}-{index:03d}.jpg';sheet.save(path,quality=94);sheets.append(dict(path=str(path.relative_to(T)),firstFrame=start,lastFrame=index,tileResolution=[w,hh],populatedTiles=index-start+1))
  index+=1
 stderr=p.stderr.read().decode();assert p.wait()==0 and index==expected,(aid,index,expected,stderr)
 has_audio=any(s['codec_type']=='audio' for s in probe['streams'])
 raw=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-filter_complex','ebur128=peak=true','-f','null','-'],capture_output=True,text=True) if has_audio else None
 (D/'ebur128.txt').write_text(raw.stderr if raw else 'No embedded audio stream; loudness/ASR not applicable.\n')
 silence=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-af','silencedetect=noise=-45dB:d=0.15','-f','null','-'],capture_output=True,text=True);(D/'silencedetect.txt').write_text(silence.stderr)
 scene=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vf',"select='gt(scene,0.20)',showinfo",'-an','-f','null','-'],capture_output=True,text=True);(D/'scene-candidates.txt').write_text(scene.stderr)
 if has_audio:subprocess.run(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','16000',str(D/'audio.wav')],check=True)
 stats=dict(asset_id=aid,sourcePath=x['path'],sourceSHA256=x['sha256'],probe=probe,decodedFrames=index,allFramesRepresented=True,sheets=sheets,frameDifferenceScores=scores,highDifferenceCandidates=sorted(scores,key=lambda z:z['meanAbsoluteDifference'],reverse=True)[:8],hasEmbeddedAudio=has_audio,audioSummary=raw.stderr[raw.stderr.rfind('Summary:'):] if raw else 'No embedded audio stream',audioSilenceLog='silencedetect.txt',sceneCandidateLog='scene-candidates.txt',audioPerception=dict(actualListening=False,reason='Audio input unsupported: tool returned audio content omitted because you do not support audio input.'),normalSpeedPlaybackWatched=False,reviewMethod='Every decoded frame represented in consecutive static sheets; computational differences and scene candidates; separate local ASR/metrics. Visual inspection coverage recorded separately.')
 (D/'analysis.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n');report.append(stats);print(aid,index,'sheets',len(sheets),'topchange',stats['highDifferenceCandidates'][:2],flush=True)
(T/('local-analysis.json' if '--local-only' in sys.argv else 'analysis.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
# New costume references, contact sheet only (original bytes unchanged).
if (T/'retrieval.json').exists():
 refs=json.loads((T/'retrieval.json').read_text())['records'];page=Image.new('RGB',(1000,1200),'#ededed');draw=ImageDraw.Draw(page)
 for i,x in enumerate(refs):
  if not x.get('path'):continue
  with Image.open(R/x['path']) as im:im.load();x['dimensions']=[im.width,im.height];thumb=ImageOps.contain(im.convert('RGB'),(490,550))
  xx=(i%2)*500;yy=(i//2)*600;page.paste(thumb,(xx+(500-thumb.width)//2,yy));draw.text((xx+4,yy+554),x['resourceName']+'\n'+x['asset_id'],fill='black')
 page.save(T/'costume2-reference-sheet.jpg',quality=94)
