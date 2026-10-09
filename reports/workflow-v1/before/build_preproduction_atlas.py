#!/usr/bin/env python3
"""Build review documents from existing film assets. No provider calls or approvals."""
from __future__ import annotations

import csv
import hashlib
import html
import io
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageOps
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
FILM = ROOT / 'projects/andre-time-travel'
OUT = FILM / '05_storyboard/preproduction-atlas-v1'
for folder in ('boards', 'shots', 'performance', 'evidence', 'documents'):
    (OUT / folder).mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('Body', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
W, H = 1600, 900
INK, PAPER, GOLD, MUTED = '#14252C', '#F0E9DD', '#D5AF70', '#AFC1C4'
ASSETS = {}
PAGES = []
OVERFLOWS = []
MANIFEST = json.loads((FILM / 'manifest.json').read_text())
LINES = list(csv.DictReader((FILM / '01_script/dialogue-lines.csv').open()))
LINE = {r['line_id']: r for r in LINES}

def rel(path):
    return Path(os.path.relpath(path, FILM)).as_posix()

def find(pattern):
    fs = sorted(FILM.glob(pattern))
    if not fs:
        raise ValueError('Missing reference: ' + pattern)
    return fs[0]

ANDRE = {
    'neutral': find('02_references/andre/synthetic/R1-J02*1.png'),
    'listening': find('02_references/andre/synthetic/R1-J04*1.png'),
    'concerned': find('02_references/andre/synthetic/R1-J05*1.png'),
    'thoughtful': find('02_references/andre/synthetic/R1-J06*1.png'),
    'seated': find('02_references/andre/synthetic/R1-J07*1.png'),
    'threequarter': find('02_references/andre/synthetic/R1-J08*1.png'),
    'present': find('02_references/andre/synthetic/R1-J09*1.png'),
}
TABLE = find('02_references/table/R1-J26*2.png')
PRESENT = find('02_references/table/*present-day*.png')
SCENES = [
    dict(code='C', key='caesar', name='Julius Caesar', place='ROME / EARLY 44 BCE', title='A name is not an answer', palette=['#A26436','#603C33','#CBB997'], plate='rome-44bce', eyeA='R1-J11*1_eyescrop.png', eyeB='R1-J12*1_eyescrop.png',
         question='Does victory leave a republic, or personal power?', arc='Command → calculation → uncertainty',
         action='The fingers press into the table, then stop. Andre lets the question land before answering.',
         light='Warm, diffuse oil-lamp direction; steady exposure on skin. Ochre plaster and muted red.',
         sound='Small flame, distant room tone, a dry sleeve against the grain. No cheering crowd.',
         costume='Muted wool and linen; an understated drape. Fabric weight and fold direction carry status.',
         warning='Fictional room and casting. Review the costume as a concept; no portrait, bust or polished vessel may reveal a face.',
         emphasis=['survive','one man','tyrant','leaves behind'], intentions=['Ask for permanence, with the confidence of someone used to yes.','Offer recognition first; let the consequence complicate it.','Test whether admiration has turned into condemnation.','Refuse a simple label. End by opening a question.'],
         timings=[(.4,2.6),(4,20.8),(21.7,24.5),(26,37.2)], sources=[1], cueA='Your name survives.',cueB='what happens to a republic'),
    dict(code='K', key='genghis', name='Genghis Khan', place='CAMPAIGN TENT / 1227', title='What an empire carries', palette=['#90704B','#514235','#B5A081'], plate='tent-1227', eyeA='R1-J13*1_eyescrop.png', eyeB='R1-J14*1_eyescrop.png',
         question='Can connection and destruction belong to the same legacy?', arc='Pride → resistance → guarded recognition',
         action='One grip loosens. Andre stays upright and keeps a level, humane gaze.',
         light='Felt-filtered amber and soft fire bounce. No moving flame shadow across eyes.',
         sound='Wind in felt, restrained leather creak, low fire. Avoid battle spectacle.',
         costume='Current candidate: blue patterned fabric, leather belt and ring. Proposed direction: restrained campaign clothing; confirm material and period details.',
         warning='The eye pair differs in brow colour and texture. The blue costume is a candidate, not a locked campaign outfit. No later imperial palace.',
         emphasis=['sons','families','call me','dead speak'], intentions=['Ask about what is left to the sons, not a list of victories.','Let the first sentence offer pride; slow at the human loss.','Seek a name that can contain both outcomes.','Hold the last clause quietly; do not perform a verdict.'],
         timings=[(.3,4.5),(5.3,19.5),(21,24.3),(25.3,39)], sources=[2,15],cueA='They will enlarge it.',cueB='families who never return'),
    dict(code='G', key='galileo', name='Galileo Galilei', place='ARCETRI / 1634', title='A question survives', palette=['#647F83','#AAA58F','#D3D3C3'], plate='arcetri-1634', eyeA='R1-J15*1_eyescrop.png', eyeB='R1-J16*1_eyescrop.png',
         question='Does silencing a person settle a question?', arc='Weariness → attention → quiet resolve',
         action='A hand rests beside a blank page. Andre leans forward only a fraction, then becomes still.',
         light='Soft cool window light, warm wood retained; page readable, face never overexposed.',
         sound='Quiet air, a single paper movement, a faint chair creak. Let stillness carry the final beat.',
         costume='Dark, plain scholar layers; soft aged cloth. No theatrical wizard robe.',
         warning='The costume reference contains generated writing; replace it with a reviewed prop before a readable close-up. Do not depict later blindness or insert a legendary quotation.',
         emphasis=['believed','simple story','question','settle'], intentions=['Ask with fatigue and a remaining thread of hope.','Warm recognition; resist turning him into a simplified hero.','Return from reputation to the work itself.','Offer respect in a plain voice. Leave silence after the final word.'],
         timings=[(.5,2.8),(4,17.8),(20,23.2),(25,35)], sources=[3,12],cueA='People learn from you.',cueB='does not settle a question'),
    dict(code='N', key='napoleon', name='Napoleon Bonaparte', place='SAINT HELENA / 1816', title='The price of greatness', palette=['#647265','#B7B9A6','#D4C8AD'], plate='sthelena-1816', eyeA='R1-J17*1_eyescrop.png', eyeB='R1-J18*1_eyescrop.png',
         question='Can greatness be separated from its price?', arc='Self-possession → wounded pride → reflection',
         action='A hand stops above a closed book. Andre does not lean away from the second question.',
         light='Muted sea-grey window light and damp plaster. Preserve skin warmth without a sepia wash.',
         sound='Distant wind, restrained room creak, cloth. Sea stays outside the scene.',
         costume='Dark green wool concept, pale waistcoat and shirt, restrained brass. Verify tailoring and remove unmotivated rings in future design.',
         warning='The current costume candidate has several rings; do not copy them into continuity without review. No claim of exact Longwood reconstruction.',
         emphasis=['laws','someone','great','price'], intentions=['Look for an institution that survives exile.','Make equality and its exclusions part of the same thought.','Let vulnerability appear inside the demand for praise.','Keep some people and others distinct; end without a final verdict.'],
         timings=[(.3,3.2),(4.2,17.5),(20.5,23.7),(25,38.5)], sources=[4,17],cueA='outlives your throne',cueB='still deny it to someone'),
    dict(code='O', key='oppenheimer', name='J. Robert Oppenheimer', place='FICTIONAL ROOM NEAR TRINITY / 15 JULY 1945', title='What comes next', palette=['#6D858C','#454D50','#D4BD93'], plate='trinity-1945', eyeA='R1-J19*1_eyescrop.png', eyeB='R1-J20*1_eyescrop.png',
         question='Can technical success answer a moral question?', arc='Anticipation → fear → stillness',
         action='A resting hand loses its tension. Andre stops speaking and stays present for the silence.',
         light='Dusty pre-dawn blue and one muted practical lamp. No flash, mushroom cloud or reflected face.',
         sound='Sparse desert wind and room tone. No dramatic detonation under the city names.',
         costume='Plain pale shirt, muted civilian jacket and fabric creases. Avoid borrowing a movie actor’s styling.',
         warning='The eye pair changes brow darkness and gaze. The meeting is fictional. No weapons diagrams, unsupported casualty totals or claimed quotation from the test.',
         emphasis=['works','Hiroshima and Nagasaki','right','question'], intentions=['Ask the narrow technical question first.','State the events clearly. Give the city names room; do not swell emotionally.','Drop the scientific certainty. Ask a human question.','Admit the limit of knowing the future; do not supply a moral answer.'],
         timings=[(.4,2.5),(4.5,20),(21.2,25.2),(27,36.5)], sources=[5,18,19,9],cueA='Hiroshima and Nagasaki',cueB='not the same as answering'),
]
for s in SCENES:
    s['platePath'] = find('02_references/table/*' + s['plate'] + '*.png')
    s['aPath'] = find('02_references/history-eyes/' + s['key'] + '/' + s['eyeA'])
    s['bPath'] = find('02_references/history-eyes/' + s['key'] + '/' + s['eyeB'])
    s['costumePath'] = find('02_references/wardrobe/*costume-' + s['key'] + '*belowneck.png')
BYKEY = {s['key']: s for s in SCENES}

def txt(c, text, x, y, width, size=22, color=PAPER, bold=False, leading=None, maxh=None):
    leading = leading or size * 1.4
    c.setFillColor(HexColor(color)); c.setFont('Bold' if bold else 'Body', size)
    font = 'Bold' if bold else 'Body'
    top = y
    for para in str(text).split('\n'):
        words = para.split(); row = ''
        for word in words:
            candidate = (row + ' ' + word).strip()
            if pdfmetrics.stringWidth(candidate, font, size) > width and row:
                c.drawString(x, y, row); y -= leading; row = word
            else:
                row = candidate
        c.drawString(x, y, row); y -= leading
    if maxh is not None and top-y > maxh:
        OVERFLOWS.append({'text':text,'height':top-y,'max':maxh})
    return y

def photo(c, path, x, y, w, h, label=None):
    key = str(path)
    if key not in ASSETS:
        im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
        im.thumbnail((1600,1100))
        buf=io.BytesIO(); im.save(buf,format='JPEG',quality=88)
        ASSETS[key] = ImageReader(buf)
    c.setFillColor(HexColor('#0A171D')); c.rect(x,y,w,h,fill=1,stroke=0)
    c.drawImage(ASSETS[key],x,y,w,h,preserveAspectRatio=True,anchor='c')
    if label:
        txt(c,label,x,y-23,w,14,MUTED,maxh=50)

def base(c, kicker, title, subtitle=None):
    c.setFillColor(HexColor(INK));c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(HexColor(GOLD));c.rect(48,H-52,56,4,fill=1,stroke=0)
    txt(c,kicker.upper(),122,H-59,1420,16,GOLD,bold=True)
    txt(c,title,48,H-118,1510,40,bold=True,maxh=108)
    if subtitle:txt(c,subtitle,48,H-162,1510,19,MUTED,maxh=60)
    c.setStrokeColor(HexColor('#38505A'));c.line(48,46,1552,46)
    txt(c,'THE TABLE BETWEEN CENTURIES  /  ANDRE ATHAR',48,24,850,12,GOLD)
    txt(c,'PREPRODUCTION V1 • PROPOSED / NOT APPROVED',1060,24,490,12,MUTED)

def finish(c, kind, ident, title, chapter, refs):
    PAGES.append({'kind':kind,'id':ident,'title':title,'chapter':chapter,'page':len(PAGES)+1,'image':f'{kind}/{ident}.png','references':[rel(p) for p in refs],'approved':False})
    c.showPage()

def tc(seconds):
    return f'{int(seconds)//60:02}:{seconds%60:04.1f}'

CUES = []
for s in SCENES:
    for i,(start,end) in enumerate(s['timings'],1):
        row = LINE[f"{s['code']}-L{i:02}"]
        CUES.append({**row,'chapter':s['key'],'startSecondsProposed':start,'endSecondsProposed':end,'timingBasis':'editorial allocation, not measured speech','intention':s['intentions'][i-1],'emphasis':s['emphasis'][i-1],'pause':'A brief breath at a sentence boundary; allow the listener to respond.','mouthRule':'Offscreen throughout' if i in (1,3) else 'Visible mouth requires approved speech route; dialogue may bridge reviewed inserts.','measuredSeconds':None})
CUES.insert(0,{**LINE['IN-L01'],'chapter':'opening','startSecondsProposed':.6,'endSecondsProposed':10.3,'timingBasis':'editorial allocation; four opening references measured separately','intention':'An intimate recollection. Curiosity becomes a need to understand consequence.','emphasis':'what came next','pause':'Separate the short middle sentence. Keep the final clause connected.','mouthRule':'Begin over the hand/table; any mouth-visible section remains a speech-test dependency.','measuredSeconds':None})
CUES.append({**LINE['OUT-L01'],'chapter':'ending','startSecondsProposed':.5,'endSecondsProposed':14.2,'timingBasis':'editorial allocation, not measured speech','intention':'Return responsibility to the present. Address one person rather than announce a lesson.','emphasis':'us / now','pause':'A small breath after past; another before the final question.','mouthRule':'Carry the final clause over the empty chair/table; end speech before the credit tail.','measuredSeconds':None})

def scene_for(key):
    return BYKEY.get(key)

def shot_details(shot):
    key=shot['chapter']; n=int(shot['id'].split('-')[1]);s=scene_for(key)
    if s:
        refs={1:s['costumePath'],2:ANDRE['threequarter'],3:s['aPath'],4:ANDRE['listening'],5:s['bPath'],6:s['costumePath'],7:ANDRE['thoughtful']}
        kind={1:'BELOW-NECK / TABLE',2:'ANDRE / MEDIUM CLOSE-UP',3:'EYES / STATE A',4:'ANDRE / LISTENING',5:'EYES / STATE B',6:'HAND / TABLE INSERT',7:'ANDRE / CLOSING HOLD'}[n]
        action={1:'A sleeve and one hand enter the established table edge.',2:'One quiet answer, seated; eyes just camera-right.',3:'A slight eye response to “'+s['cueA']+'”.',4:'Listen without moving the head out of the supplied angle.',5:'Let “'+s['cueB']+'” change the gaze; at most one blink.',6:s['action'],7:'Hold the consequence, then cut to wood before changing era.'}[n]
        gap={1:'Exact seated sleeve/hand composition still needed.',2:'Andre has not yet been composed into this era at the locked table.',3:'Eye strip is a reference; final full-frame composition and gaze need approval.',4:'Era-matched lighting and mouth visibility still need a keyframe.',5:'Two eye states were generated separately: compare iris, brow and crease continuity.',6:'The costume fragment is a material reference, not the required tabletop hand keyframe.',7:'Needs the same era lighting, seating and table geometry as the opening Andre shot.'}[n]
        return refs[n],kind,action,gap,[refs[n],s['platePath']]
    if key=='opening':
        return ([TABLE,ANDRE['present'],PRESENT][n-1],['TABLE / ARRIVAL','ANDRE / OPENING','TABLE / TRANSITION'][n-1],['Andre’s hand comes to rest on the edge.','A calm first question; head held within the approved angle.','Cut on the same grain and edge mark into Rome.'][n-1],'Reference assembly only; exact hand position and matched transition require a keyframe.',[PRESENT,TABLE])
    return ([ANDRE['present'],PRESENT,TABLE][n-1],['ANDRE / RETURN','EMPTY CHAIR / QUESTION','TABLE / CREDITS'][n-1],['Andre begins the question for us.','The empty chair receives the final clause.','Hold the wood; then fade after the last spoken word.'][n-1],'Leave the proposed 3.8-second credit tail after dialogue; check with measured final audio.',[PRESENT,TABLE])

def draw_cover(c):
    base(c,'Production reference atlas / 09 October 2026','The Table Between Centuries','A four-minute fictional conversation across five eras — starring Andre Athar')
    photo(c,ANDRE['threequarter'],48,150,550,510,'Synthetic Andre candidate. Human likeness approval remains pending.')
    txt(c,'One table. Five encounters.\nA question returned to us.',646,650,850,44,bold=True,maxh=200)
    txt(c,'This atlas assembles existing Kling references into review boards, shot cards and performance cards. It does not create or approve new film footage.',646,435,840,26,maxh=155)
    txt(c,'41 shot cards • 22 dialogue cards • 7 scene boards\n6 character boards • 1 wardrobe board • 4 voice tests',646,287,840,24,GOLD,maxh=120)
    finish(c,'boards','00-cover','The Table Between Centuries','all',[ANDRE['threequarter']])

def draw_workflow(c):
    base(c,'Production map','From reference to a finished performance','Keep visual design, personal likeness, language validation and finished-footage approval as separate decisions.')
    stages=[('01','SCRIPT + SOURCES','22 stable line IDs. Five fictional exchanges. Preserve factual anchors and mark language adaptations for review.'),('02','REFERENCE + BIBLES','Real photos, synthetic Andre, historical eyes, fabric and scene plates each keep their own role.'),('03','VOICE + PILOT','Approve likeness, test speech and listening in a restrained four-shot pilot, then measure final dialogue.'),('04','KEYFRAMES + PICTURE','Build era-specific Andre and hand shots only for measured coverage gaps. Review every generated take.'),('05','EDIT + TWO EDITIONS','Reuse approved eyes, hands and listening. Inspect exact masters, captions, sound and every risky frame.')]
    for i,(num,title,body) in enumerate(stages):
        y=646-i*112
        txt(c,num,52,y,90,38,GOLD,bold=True)
        txt(c,title,155,y+7,380,22,bold=True)
        txt(c,body,550,y+7,980,21,maxh=88)
    finish(c,'boards','01-workflow','Production workflow','all',[])

def draw_scene(c,s=None,ending=False):
    if s:
        key=s['key'];name=s['name'];place=s['place'];plate=s['platePath'];title=s['title'];question=s['question'];light=s['light'];sound=s['sound'];warn=s['warning']
    else:
        key='ending' if ending else 'opening';name='Return to the present' if ending else 'Arrival';place='PRESENT DAY / FICTIONAL ROOM';plate=PRESENT;title='The question is ours' if ending else 'Before the first question';question='What are we leaving for the people who come next?' if ending else 'What would it feel like to hear what comes next?';light='Quiet window light; retain the same wood and contemporary clothes.';sound='Room tone returns gradually. The transition is heard before it is seen.';warn='Present-day reference only. A hand insert and exact Andre/table composite are still missing.'
    base(c,'Scene board / '+place,name+' — '+title,'Fictional design proposal. Existing images are references, not a newly generated scene composite.')
    photo(c,plate,48,280,900,390,'Environment candidate / '+plate.name)
    txt(c,question,990,654,560,29,bold=True,maxh=140)
    txt(c,light,990,500,560,23,maxh=145)
    txt(c,'SOUND  '+sound,990,338,560,21,MUTED,maxh=140)
    txt(c,'CONTINUITY  '+warn,48,184,1500,22,GOLD,maxh=110)
    if s:
        for i,color in enumerate(s['palette']):
            c.setFillColor(HexColor(color));c.rect(48+i*94,700,80,18,fill=1,stroke=0)
    finish(c,'boards','scene-'+key,name+' scene board',key,[plate])

def draw_character(c,s=None):
    if not s:
        base(c,'Character bible / observed and proposed','Andre Athar','The real-photo wardrobe and the dark synthetic wardrobe are distinct candidates. Neither is approved here.')
        real=ROOT/'inbox/andre-reference-photos/20240202_015214.jpg'
        photo(c,real,48,235,410,450,'Real supplied photograph / 20240202_015214')
        photo(c,ANDRE['neutral'],490,235,410,450,'Synthetic neutral / R1-J02 / candidate')
        txt(c,'OBSERVED PHOTO DETAILS',945,656,605,22,GOLD,bold=True)
        txt(c,'Short dark textured hair, light facial stubble, grey blazer and a pale striped open-collar shirt. These observations do not certify likeness.',945,605,605,24,maxh=175)
        txt(c,'PROPOSED SCREEN LOOK',945,416,605,22,GOLD,bold=True)
        txt(c,'Dark jacket and charcoal shirt. Hold the same grooming, lapel, collar, sleeves and accessories through all five eras. Approve this change before locking it.',945,367,605,23,maxh=190)
        txt(c,'GEOMETRY  Neutral and gentle three-quarter only until the supplied views and pilot support more. Synthetic profiles do not establish unseen facial geometry.',48,143,1500,22,GOLD,maxh=95)
        finish(c,'boards','character-andre','Andre: photo and synthetic wardrobe','andre',[real,ANDRE['neutral']]);return
    base(c,'Historical casting / '+s['place'],s['name'],'Fictional casting and costume concept. No full historical face is used on this board.')
    photo(c,s['aPath'],48,494,1000,175,'STATE A / '+s['cueA'])
    photo(c,s['bPath'],48,249,1000,175,'STATE B / '+s['cueB'])
    photo(c,s['costumePath'],1120,239,430,430,'Below-neck costume concept')
    txt(c,s['arc'],48,183,1500,29,GOLD,bold=True,maxh=50)
    txt(c,s['costume']+' Compare both eye states for continuity before reuse; expression is not permission for a new identity.',48,125,1500,21,maxh=65)
    finish(c,'boards','character-'+s['key'],s['name']+' character board',s['key'],[s['aPath'],s['bPath'],s['costumePath']])

def draw_wardrobe(c):
    base(c,'Costume reference','Clothing tells the era','Below-neck fragments only. Period accuracy, accessories and continuity are still review gates.')
    for i,s in enumerate(SCENES):
        x=48+i*303
        photo(c,s['costumePath'],x,285,280,385)
        txt(c,s['name'],x,253,280,21,GOLD,bold=True,maxh=65)
        txt(c,s['costume'],x,185,280,16,maxh=120)
    finish(c,'boards','wardrobe-five-eras','Five costume references','all',[s['costumePath'] for s in SCENES])

def draw_shot(c,shot,start):
    ref,kind,action,gap,refs=shot_details(shot);s=scene_for(shot['chapter'])
    end=start+shot['targetSeconds']
    base(c,'Shot '+shot['id']+' / '+tc(start)+'–'+tc(end),kind,shot['description']+' • '+str(shot['targetSeconds'])+' seconds proposed')
    photo(c,ref,48,250,860,420,'Reference only / '+ref.name)
    txt(c,'ACTION',956,650,596,18,GOLD,bold=True)
    txt(c,action,956,612,596,24,maxh=155)
    txt(c,'FRAME + CAMERA',956,439,596,18,GOLD,bold=True)
    txt(c,shot['framingRestriction']+'. Locked camera. No widening, orbit or facial transition.',956,400,596,23,maxh=145)
    txt(c,'KEYFRAME GAP',48,172,1460,18,GOLD,bold=True)
    txt(c,gap,48,132,1490,22,maxh=73)
    finish(c,'shots',shot['id'],kind,shot['chapter'],list(dict.fromkeys(refs+[ref])))
    return {'id':shot['id'],'chapter':shot['chapter'],'startSeconds':start,'endSeconds':end,'durationSeconds':shot['targetSeconds'],'action':action,'camera':'locked','restriction':shot['framingRestriction'],'reference':rel(ref),'referenceRole':'composition or material candidate, not an approved final keyframe','missingComposition':gap,'approved':False,'generationId':None}

def draw_performance(c,r):
    s=scene_for(r['chapter']);ref=(s['aPath'] if 'offscreen' in r['speaker'] else ANDRE['listening']) if s else ANDRE['present']
    base(c,'Dialogue / '+r['line_id'],r['speaker'],f"Proposed chapter-local window {r['startSecondsProposed']:.1f}–{r['endSecondsProposed']:.1f}s • fictional dialogue • not a historical quotation")
    photo(c,ref,48,275,540,395,'Performance reference only / no final voice or likeness acceptance')
    y=txt(c,'“'+r['text_en']+'”',640,652,910,32,bold=True,maxh=240)
    txt(c,'INTENTION  '+r['intention'],640,min(y-40,385),910,23,maxh=145)
    txt(c,'EMPHASIS  '+r['emphasis'],640,213,910,20,GOLD,maxh=60)
    txt(c,r['mouthRule']+' '+r['pause'],48,123,1500,20,MUTED,maxh=73)
    finish(c,'performance',r['line_id'],r['speaker']+' / '+r['line_id'],r['chapter'],[ref])

def documents(specs):
    # Keep all new writing separate from the canonical screenplay and task approvals.
    p=OUT/'documents'
    with (p/'dialogue-performance.csv').open('w',newline='') as f:
        keys=['line_id','speaker','chapter','text_en','startSecondsProposed','endSecondsProposed','timingBasis','intention','emphasis','pause','mouthRule','measuredSeconds']
        w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(CUES)
    (p/'shot-specifications.json').write_text(json.dumps({'scope':'draft preproduction only','approved':False,'shots':specs},indent=2,ensure_ascii=False)+'\n')
    with (p/'shot-coverage.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(specs[0]));w.writeheader();w.writerows(specs)
    md=['# Director’s annotated script — reference edition v1','','Draft companion to `01_script/script-en.md`. All spoken text below is unchanged from `dialogue-lines.csv`. All dialogue is fictional. Times are proposed allocations, not measured performances. This document does not approve the canonical screenplay.','',
        '## Dramatic spine','','Andre begins by asking what it feels like to hear the future. Caesar asks about a name; the Khan about inheritance; Galileo about belief; Napoleon about laws and greatness; Oppenheimer about success and rightness. Each answer leaves a question that the next encounter cannot settle. The return to the present gives that responsibility to the audience.','',
        '## Timing and coverage','','The picture remains 12 + (5 × 42) + 18 = 240 seconds across 41 planned slots. A speech is allowed to bridge cuts. The 10-second opening Andre shot is not a 10-second limit on the whole answer. Eye cues follow the approved recorded words; the current slot order is a planning grid. Move a reaction cut inside its scene when measured audio requires it. Do not speed up a performance to preserve this draft.','',
        'Opening voice references are separate test files. Their completed duration does not approve English pronunciation, naturalness, likeness or synchronization. Ending proposal: speech 0.5–14.2 seconds within the 18-second ending, leaving 3.8 seconds for the credit tail. The actual recording may require a shorter approved final sentence or revised credits timing.','']
    for key in ['opening']+[s['key'] for s in SCENES]+['ending']:
        s=scene_for(key);md+=['## '+(s['name']+' — '+s['title'] if s else key.title()),'']
        if s:md += [s['question'], '', '**Action:** '+s['action'],'','**Light:** '+s['light'],'','**Sound:** '+s['sound'],'']
        for r in [v for v in CUES if v['chapter']==key]:
            md += [f"**{r['line_id']} — {r['speaker']}** ({r['startSecondsProposed']:.1f}–{r['endSecondsProposed']:.1f}s proposed)",'> '+r['text_en'],'','Direction: '+r['intention'],'','Coverage: '+r['mouthRule'],'']
        if s:md+=['**Design review:** '+s['warning'],'','**Factual anchors:** existing source IDs '+', '.join(map(str,s['sources']))+' in `00_brief/research/source-registry.json` and the canonical script. No fresh historical validation is claimed by this atlas.','']
    md += ['## Two editions','','English remains the first recording target. The historical-language edition needs line-by-line translation, back-translation, a declared period/pronunciation convention, and a named qualified reviewer. Caesar: Latin convention; Genghis: reviewed historical Mongolian approximation; Galileo: reviewed period/region Italian; Napoleon: resolve the Corsican/Tuscan-rooted target explicitly; Oppenheimer: English. An available modern TTS language does not establish period accuracy. Keep every line ID across versions.','',
           '## Suggested end card copy','','“A fictional encounter. All dialogue and reactions were written for this film.”','','“Starring Andre Athar. Synthetic imagery and voice production. Historical source notes accompany the film.”','','These are draft credit lines. Final provider, music, voice and production credits must match actual approved uses.']
    (p/'director-script-en.md').write_text('\n'.join(md)+'\n')
    md=['# The next useful image batch — specifications only','','Not submitted, not charged, not approved. The reference phase currently has 14 Kling credits left after the recorded 760-credit R1 batch. No guaranteed price for these requests is asserted. Review the existing boards before allocating another image batch.','',
        'Fifteen proposed missing compositions: two Andre frames and one hand/table insert for each era. These fill actual coverage gaps rather than multiply unrelated portraits. Approve the real-photo identity set, dark wardrobe candidate and table first. Refresh live model parameters and balance before any submission. These prose briefs are not executable provider payloads.','']
    for s in SCENES:
        for role in ['Andre speaking','Andre listening / closing hold','Historical hand and table']:
            md+=['## '+s['code']+' — '+role,'']
            if role.startswith('Andre'):
                md+=['Identity input: individually approved Andre photograph(s); do not use a montage. Wardrobe input: approved dark look only if Andre selects it. Geometry input: '+rel(TABLE)+'. Environment input: '+rel(s['platePath'])+'.','',
                    'Proposed composition: seated medium close-up, Andre in the left half with room toward camera-right. Head at a supplied gentle three-quarter angle, gaze toward the unseen interlocutor. Same table edge, collar, lapels and sleeve length. '+('Relaxed closed mouth and attentive gaze.' if 'listening' in role else 'Neutral pre-speech mouth; do not bake a phoneme into the image.')+' '+s['light']+' No other person, reflection, portrait, text or face in the background.','']
            else:
                md+=['Material input: '+rel(s['costumePath'])+'. Table geometry input: '+rel(TABLE)+'. Environment palette: '+rel(s['platePath'])+'.','',
                    'Proposed composition: one anatomically plausible hand and sleeve resting at the far edge of the same table; camera below the shoulder. The entire head and neck stay outside the frame. Cloth and hand belong to the historical interlocutor, not Andre. Preserve grain direction and edge damage. No extra jewellery, readable invented manuscript, mirrored face or extra fingers. '+s['action'],'']
    (p/'next-image-batch.md').write_text('\n'.join(md)+'\n')

def write_html():
    def esc(x):return html.escape(str(x),quote=True)
    cards=''.join(f'<article data-kind="{p["kind"]}" data-chapter="{p["chapter"]}"><a href="{p["image"]}" target="_blank"><img loading="lazy" src="{p["image"]}" alt="{esc(p["title"])}"></a><h3>{esc(p["id"])} · {esc(p["title"])}</h3><p>{esc(p["chapter"])} / draft, not approved</p></article>' for p in PAGES)
    audio=''.join(f'<div><strong>Opening reference {i}</strong><audio controls preload="metadata" src="../../04_audio/voice-tests/codex-opening-v1/IN-L01-athar-v2-ref-{i}.mp3"></audio></div>' for i in range(1,5))
    template='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Table Between Centuries — Reference Atlas</title>
<style>:root{color-scheme:dark;--bg:#14252c;--fg:#f0e9dd;--gold:#d5af70}*{box-sizing:border-box}body{background:var(--bg);color:var(--fg);font:16px/1.6 system-ui;margin:0}main{max-width:1500px;margin:auto;padding:42px 24px}h1{font:600 clamp(32px,5vw,68px)/1.08 Georgia;margin:15px 0}h2{font-size:28px}a{color:var(--gold)}.eyebrow{color:var(--gold);letter-spacing:.14em;text-transform:uppercase}header>p{max-width:940px;font-size:19px}.links{display:flex;gap:22px;flex-wrap:wrap;margin:24px 0}.filters{position:sticky;top:0;z-index:1;background:#14252cf5;border-block:1px solid #44606b;padding:15px 0;display:flex;gap:18px;flex-wrap:wrap}select,button{background:#213940;color:var(--fg);padding:10px;border:1px solid #789498;border-radius:5px}label{display:flex;align-items:center;gap:8px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,410px),1fr));gap:24px;margin-top:24px}article{background:#21353d;border:1px solid #38505a;border-radius:8px;overflow:hidden}article img{width:100%;display:block;aspect-ratio:16/9;object-fit:contain}article h3,article p{margin:12px 18px}article h3{font-size:17px}article p{color:#b1c4c8;font-size:14px}.audio{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}.audio audio{display:block;width:100%;margin-top:10px}.note{border-left:3px solid var(--gold);padding-left:18px;color:#cfdbdb}footer{margin-top:45px}[hidden]{display:none!important}@media print{.filters,.audio{display:none}.grid{grid-template-columns:1fr 1fr}article{break-inside:avoid}}</style>
<main><header><span class="eyebrow">Andre Athar · preproduction v1 · 09 October 2026</span><h1>The Table Between Centuries</h1><p>Five conversations, one recurring table, and a question for the present. A visual production atlas connecting existing references to the complete 41-shot plan and 22 fictional lines.</p><p class="note">These are designed reference boards and cards assembled from existing images. They are not 79 newly generated scenes. Original photographs, synthetic candidates and final approval remain separate. Click any card to inspect it at full size.</p><div class="links"><a href="reference-atlas.pdf">Download reference atlas PDF</a><a href="storyboard-cards.pdf">41 shot cards PDF</a><a href="performance-cards.pdf">22 dialogue cards PDF</a><a href="documents/director-script-en.md">Annotated script</a><a href="documents/next-image-batch.md">15 missing image briefs</a><a href="documents/shot-coverage.csv">Shot coverage CSV</a></div></header>
<section><h2>Opening · Athar voice references</h2><p>Four completed English tests. Likeness, pronunciation, naturalness and the final speech route still need review. Other characters do not use Andre’s voice.</p><div class="audio">AUDIO</div></section>
<h2>Explore the production cards</h2><div class="filters"><label>Type <select id="kind"><option value="all">All cards</option value="boards">Scene, character and wardrobe boards</option value="shots">Shot cards</option value="performance">Dialogue and performance</option></select></label><label>Chapter <select id="chapter"><option value="all">All chapters</option><option>andre</option><option>opening</option><option>caesar</option><option>genghis</option><option>galileo</option><option>napoleon</option><option>oppenheimer</option><option>ending</option></select></label><output id="count" aria-live="polite"></output></div><div class="grid">CARDS</div>
<footer><p>Photographs and source images remain in their original locations. The source map and checksums are in <a href="catalog.json">catalog.json</a>. Canonical approvals were not advanced by this atlas.</p><p>Google Drive discovery found the existing Biblioteca Cinematográfica; the inspected reference and storyboard folders were empty at the time of discovery. This local package is the complete handoff for this pass.</p></footer></main><script>const cards=[...document.querySelectorAll('article')];const kind=document.getElementById('kind'),chapter=document.getElementById('chapter');function filter(){let n=0;for(const c of cards){c.hidden=!((kind.value==='all'||c.dataset.kind===kind.value)&&(chapter.value==='all'||c.dataset.chapter===chapter.value||c.dataset.chapter==='all'));if(!c.hidden)n++;}document.getElementById('count').textContent=n+' cards';}kind.addEventListener('change',filter);chapter.addEventListener('change',filter);filter();</script></html>'''
    (OUT/'index.html').write_text(template.replace('CARDS',cards).replace('AUDIO',audio))

def main():
    c=canvas.Canvas(str(OUT/'reference-atlas.pdf'),pagesize=(W,H))
    draw_cover(c);draw_workflow(c);draw_character(c)
    draw_scene(c)
    for s in SCENES:draw_scene(c,s);draw_character(c,s)
    draw_scene(c,ending=True);draw_wardrobe(c);c.save()
    board_count=len(PAGES)
    c=canvas.Canvas(str(OUT/'storyboard-cards.pdf'),pagesize=(W,H))
    start=0;specs=[]
    for shot in MANIFEST['shots']:
        specs.append(draw_shot(c,shot,start));start+=shot['targetSeconds']
    c.save()
    c=canvas.Canvas(str(OUT/'performance-cards.pdf'),pagesize=(W,H))
    for row in CUES:draw_performance(c,row)
    c.save();documents(specs)
    # Rasterize the designed documents; source photographs are never changed.
    for pdf,folder in [('reference-atlas.pdf','boards'),('storyboard-cards.pdf','shots'),('performance-cards.pdf','performance')]:
        selected=[p for p in PAGES if p['kind']==folder]
        prefix=OUT/folder/'render'
        subprocess.run(['pdftoppm','-r','72','-png',str(OUT/pdf),str(prefix)],check=True)
        files=sorted((OUT/folder).glob('render-*.png'))
        if len(files)!=len(selected):raise ValueError('Rendered page count mismatch')
        for f,p in zip(files,selected):f.rename(OUT/p['image'])
    refs=sorted({r for p in PAGES for r in p['references']})
    source_refs=[]
    for r in refs:
        p=FILM/r
        source_refs.append({'path':r,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':'real_photograph' if '/inbox/' in str(p.resolve()) else 'existing_synthetic_reference','approved':False})
    catalog={'createdAt':datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(),'kind':'reference_document_layouts','newKlingImageGenerations':0,'counts':{'boards':board_count,'shots':len(specs),'performanceCards':len(CUES),'totalCardImages':len(PAGES)},'sourceReferences':source_refs,'pages':PAGES,'overflowChecks':OVERFLOWS,'approved':False}
    (OUT/'catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n');write_html()
    print(json.dumps({'counts':catalog['counts'],'overflowCount':len(OVERFLOWS),'path':str(OUT)}))
    if OVERFLOWS:print(json.dumps(OVERFLOWS,ensure_ascii=False))

if __name__=='__main__':main()
