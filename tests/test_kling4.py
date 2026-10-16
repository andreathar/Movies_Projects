"""Synthetic production contracts only; no CLI, provider, uploads or paid requests."""
import copy
import hashlib
import importlib.util
import json
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('v4_runner', ROOT / 'scripts/kling_batch.py')
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)
MODELS = json.loads((ROOT/'docs/kling-manual/snapshots/2026-10-16-who_am_i.sanitized.json').read_text())['body']['availableModels']
TOOLS = json.loads((ROOT/'docs/kling-manual/snapshots/2026-10-16-tool_list.json').read_text())['body']['tools']


class Kling4Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir='/tmp')
        self.addCleanup(self.temp.cleanup)
        self.film = Path(self.temp.name)
        self.review = self.file('review.json', b'{"synthetic":true,"decision":"fixture only"}')
        # Header is sufficient for offline geometry probing; never represents real approved media.
        self.image = self.file('frame.png', b'\x89PNG\r\n\x1a\n' + struct.pack('>I',13) + b'IHDR' + struct.pack('>II',1280,720) + b'\x08\x02\0\0\0')
        self.job = {'job':'synthetic-v4','model':'kling-video-v4_0','tool':'image_to_video', 'prompt':'Stillness after the difficult line.', 'auth':'synthetic-scope', 'args':{'duration':'5','resolution':'720p','imageCount':'1'},'inputs':{'first_image':'frame.png'}, 'shotContract':{'version':1,'provider':'kling-global','interface':'cli','references':[self.reference('first_image','image','frame.png')],'beats':[{'start':0,'end':5,'action':'Listen after the line'}],'continuity':{'cast':'Andre; existing companion stays outside safe crop','wardrobe':'fixture suit v1','table':'fixture D04 selected hash','screenAxis':'Andre left, looking right','historicalFaceExclusion':'zero full historical faces and reflections','cameraMode':'locked_single_shot'},'audio':{'strategy':'uncontrolled_review_required'}}}

    def file(self, name, raw):
        path=self.film/name;path.write_bytes(raw)
        return {'path':name,'sha256':hashlib.sha256(raw).hexdigest()}

    def reference(self,target,kind,source,**extras):
        return {'target':target,'kind':kind,'source':source,'sha256':hashlib.sha256((self.film/source).read_bytes()).hexdigest(),'provenance':'synthetic local fixture; no human approval','use':'composition','review':{'status':'approved','scope':'composition'},'reviewEvidence':self.review,**extras}

    def report(self,job=None):
        return k.pf.check_job(job or self.job,MODELS,str(self.film),str(self.film),False)

    def errors(self,job=None):
        return {x['code'] for x in self.report(job).items if x['level']=='ERROR'}

    def omni(self):
        j=copy.deepcopy(self.job);j['tool']='omni_ref_video';j['inputs']={'image_1':'frame.png'}
        j['args'].update(aspect_ratio='16:9',prefer_multi_shots=True,enable_audio=False,keepOriginalSound=False)
        j['shotContract']['references'][0]['target']='image_1';j['shotContract']['audio']['strategy']='postproduction'
        j['shotContract']['continuity']['cameraMode']='reviewed_multishot'
        return j

    def video(self,j,target='video_1',seconds=20,element=False):
        facts={'durationSeconds':seconds,'bytes':1000,'width':1280,'height':720,'fps':24}
        name='clip-'+target.replace(':','-')+'.mp4';self.file(name,b'synthetic video bytes, no remote call')
        ref=self.reference(target,'video',name,facts=facts)
        if not element:
            j['inputs'][target]='https://example.invalid/'+name;ref['source']=j['inputs'][target];ref['localEvidence']=name
            j.setdefault('inputFacts',{})[target]=facts
        else:
            eid=target.split(':')[1]
            detail=self.file('element.json',json.dumps({'body':{'id':eid,'type':'video','resource':{'video':'https://example.invalid/video'}}}).encode())
            ref['elementEvidence']=detail;j['elements']=[{'id':eid,'bindName':'Fixture','type':'video'}];j['prompt']+=' <<<'+eid+'>>>'
        j['shotContract']['references'].append(ref)
        j['shotContract']['billing']={'inputVideoSeconds':seconds,'inputVideoDurationIncluded':True}
        return ref

    def test_valid_keyframe_and_omni_contracts(self):
        self.assertEqual(self.errors(),set())
        self.assertEqual(self.errors(self.omni()),set())

    def test_v4_image_ratio_is_exact_not_legacy_tolerance(self):
        path=self.film/'frame.png'
        path.write_bytes(b'\x89PNG\r\n\x1a\n'+struct.pack('>I',13)+b'IHDR'+struct.pack('>II',1000,395)+b'\x08\x02\0\0\0')
        self.job['shotContract']['references'][0]['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertIn('FILE_ASPECT',self.errors())
        path.write_bytes(b'\x89PNG\r\n\x1a\n'+struct.pack('>I',13)+b'IHDR'+struct.pack('>II',1000,400)+b'\x08\x02\0\0\0')
        self.job['shotContract']['references'][0]['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(self.errors(),set())

    def test_v4_image_size_is_decimal_mb_without_unadvertised_dimension_cap(self):
        with patch.object(k.pf.os.path,'getsize',return_value=30_000_001):
            self.assertIn('FILE_SIZE',self.errors())
        with patch.object(k.pf.os.path,'getsize',return_value=30_000_000):
            self.assertEqual(self.errors(),set())
        path=self.film/'frame.png'
        path.write_bytes(b'\x89PNG\r\n\x1a\n'+struct.pack('>I',13)+b'IHDR'+struct.pack('>II',4096,2304)+b'\x08\x02\0\0\0')
        self.job['shotContract']['references'][0]['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(self.errors(),set())

    def test_v4_not_invented_for_motion_control(self):
        j=copy.deepcopy(self.job);j['tool']='motion_control'
        self.assertIn('MODEL',self.errors(j))

    def test_public_4k_and_old_flags_do_not_expand_live_allowlist(self):
        for key,value,code in [('resolution','4k','ARG_VALUE'),('enable_audio',False,'ARG_UNKNOWN'),('prefer_multi_shots',False,'ARG_UNKNOWN')]:
            with self.subTest(key=key):
                j=copy.deepcopy(self.job);j['args'][key]=value;self.assertIn(code,self.errors(j))

    def test_no_implicit_audio_or_removed_identity_binding(self):
        j=copy.deepcopy(self.job);j['shotContract']['audio']['strategy']='postproduction'
        self.assertIn('V4_AUDIO_PLAN',self.errors(j))
        j=copy.deepcopy(self.job);j['elements']=[{'id':'123','bindName':'Andre'}];j['prompt']+=' <<<123>>>'
        self.assertIn('ARG_UNKNOWN',self.errors(j))
        j=self.omni();j['shotContract']['references'].append({'target':'element:123'})
        self.assertIn('V4_REFERENCES',self.errors(j))

    def test_manifest_covers_exact_sources_hash_and_use(self):
        for update,code in [({'source':'other.png'},'V4_REFERENCE_EVIDENCE'),({'sha256':'0'*64},'V4_REFERENCE_EVIDENCE'),({'use':'identity'},'V4_REFERENCE_SCOPE'),({'review':{'status':'pending','scope':'composition'}},'V4_REFERENCE_SCOPE')]:
            j=copy.deepcopy(self.job);j['shotContract']['references'][0].update(update);self.assertIn(code,self.errors(j))
        j=copy.deepcopy(self.job);j['shotContract']['references']=[];self.assertIn('V4_REFERENCES',self.errors(j))
        j=copy.deepcopy(self.job);j['shotContract']['references'][0]['reviewEvidence']={'path':'../elsewhere','sha256':'0'*64};self.assertIn('V4_REFERENCE_EVIDENCE',self.errors(j))

    def test_multishot_and_locked_camera_are_not_silently_changed(self):
        j=self.omni();j['args']['prefer_multi_shots']=False;self.assertIn('ARG_VALUE',self.errors(j))
        j=self.omni();j['shotContract']['continuity']['cameraMode']='locked_single_shot';self.assertIn('V4_CAMERA',self.errors(j))

    def test_v4_video_20_seconds_not_rejected_by_legacy_10_second_rule(self):
        j=self.omni();self.video(j)
        self.assertEqual(self.errors(j),set())
        j['shotContract']['billing']['inputVideoSeconds']=5;self.assertIn('V4_BILLING',self.errors(j))

    def test_combined_video_elements_and_direct_duration_cap(self):
        j=self.omni();self.video(j,seconds=20);self.video(j,'element:123',seconds=15,element=True)
        self.assertIn('V4_VIDEO_TOTAL',self.errors(j))
        self.assertNotIn('VIDEO_ELEMENT_MIX',self.errors(j))
        j['shotContract']['references'][-1]['elementEvidence']['sha256']='0'*64
        self.assertIn('V4_REFERENCE_EVIDENCE',self.errors(j))

    def test_audio_is_typed_as_audio_and_measured_before_upload(self):
        j=self.omni();audio=self.file('voice.wav',b'synthetic audio')
        ref=self.reference('audio_1','audio','voice.wav',localEvidence='voice.wav',facts={'durationSeconds':6,'bytes':15})
        ref['voiceContentReview']='reviewed_voice_only';ref['source']='https://example.invalid/voice.wav';ref['use']='voice';ref['review']['scope']='voice'
        j['inputs']['audio_1']=ref['source'];j['shotContract']['references'].append(ref)
        self.assertEqual(self.errors(j),set())
        ref['facts']['durationSeconds']=4;self.assertIn('V4_AUDIO_LIMIT',self.errors(j))

    def test_retaining_silent_source_is_blocked(self):
        j=self.omni();ref=self.video(j,seconds=10)
        j['args'].update(keepOriginalSound=True,enable_audio=False)
        j['shotContract']['audio']['strategy']='retain_source'
        self.assertIn('V4_SOURCE_AUDIO',self.errors(j))
        ref['facts']['hasAudio']=True
        self.assertEqual(self.errors(j),set())

    def test_changed_live_element_is_blocked_before_balance(self):
        j=self.omni();self.video(j,'element:123',seconds=5,element=True)
        with patch.object(k,'run',side_effect=[{'ok':True,'body':{'availableModels':MODELS}}, {'ok':True,'body':{'tools':TOOLS}}, {'ok':True,'body':{'id':'123','type':'video','resource':{'video':'https://example.invalid/changed'}}}]) as remote_call, patch.object(k,'account') as balance:
            with self.assertRaisesRegex(SystemExit,'Element mudou'):k.preflight(j,self.film)
            self.assertEqual(remote_call.call_args.args[0][1:3],['element_get','123'])
            balance.assert_not_called()

    def test_tool_schema_change_invalidates_release_digest(self):
        def run_for(tools):
            with patch.object(k,'run',side_effect=[{'ok':True,'body':{'availableModels':MODELS}},{'ok':True,'body':{'tools':tools}}]):
                return k.preflight(self.job,self.film)['schemaSha256']
        original=run_for(TOOLS)
        changed=copy.deepcopy(TOOLS)
        next(t for t in changed if t['name']=='image_to_video')['inputSchema']['description']='changed contract'
        self.assertNotEqual(original,run_for(changed))

    def test_combined_count_includes_audio_and_elements(self):
        j=self.omni()
        for n in range(2,11):
            target='image_'+str(n);j['inputs'][target]='frame.png';j['shotContract']['references'].append(self.reference(target,'image','frame.png'))
        for n in range(1,6):self.video(j,'video_'+str(n),seconds=3)
        j['inputs']['audio_1']='https://example.invalid/voice.wav'
        self.assertIn('COMBINED_CAP',self.errors(j))

    def test_keyframe_total_not_slot_number_enforces_ten(self):
        j=copy.deepcopy(self.job)
        for n in range(1,11):
            target='keyframe_'+str(n);j['inputs'][target]='frame.png';j['shotContract']['references'].append(self.reference(target,'image','frame.png'))
        self.assertIn('COMBINED_CAP',self.errors(j))

    def test_invalid_beats_and_native_dialogue_fail_closed(self):
        j=copy.deepcopy(self.job);j['shotContract']['beats'][0]['end']=6;self.assertIn('V4_BEATS',self.errors(j))
        j=self.omni();j['args']['enable_audio']=True;j['shotContract']['audio']={'strategy':'native_guide','dialogue':'fictional exact line','measuredSeconds':7,'languageReview':'reviewed'}
        self.assertIn('V4_DIALOGUE',self.errors(j))

    def test_contract_changes_invalidate_payload_release(self):
        first=k.release.fingerprint(self.film,self.job)
        self.job['shotContract']['continuity']['wardrobe']='different costume'
        self.assertNotEqual(first,k.release.fingerprint(self.film,self.job))

    def test_valid_v4_preflight_requires_both_live_discovery_tools(self):
        def remote(cmd):
            if cmd[1]=='who_am_i':return {'ok':True,'body':{'availableModels':MODELS}}
            if cmd[1]=='tool_list':return {'ok':True,'body':{'tools':TOOLS}}
            raise AssertionError('No other CLI call permitted')
        with patch.object(k,'run',side_effect=remote) as remote_call:
            result=k.preflight(self.job,self.film)
        self.assertEqual([c.args[0][1] for c in remote_call.call_args_list],['who_am_i','tool_list'])
        self.assertIsNotNone(result['toolSchemaSha256']);self.assertFalse(result['generationTested'])
        with patch.object(k,'run',side_effect=[{'ok':True,'body':{'availableModels':MODELS}},{'ok':False}]):
            with self.assertRaisesRegex(SystemExit,'tool_list'):k.preflight(self.job,self.film)

    def test_invalid_contract_stops_before_account_or_upload(self):
        j=copy.deepcopy(self.job);j.pop('shotContract')
        with patch.object(k.release,'authorize',return_value={}), patch.object(k,'run',return_value={'ok':True,'body':{'availableModels':MODELS}}) as remote_call,patch.object(k,'account') as balance:
            with self.assertRaisesRegex(SystemExit,'V4_CONTRACT'):
                k.submit(self.film,j['job'],j['tool'],j['model'],j['prompt'],j['args'],[],j['auth'],'fixture',inputs=j['inputs'],submit_only=True)
            balance.assert_not_called()
            self.assertEqual([c.args[0][1] for c in remote_call.call_args_list],['who_am_i'])


if __name__=='__main__':unittest.main()
