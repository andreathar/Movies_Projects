"""Synthetic release/price/idempotency checks. No real credentials or provider calls."""
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('release_runner',ROOT/'scripts/kling_batch.py')
k=importlib.util.module_from_spec(spec);spec.loader.exec_module(k)
r=k.release


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir='/tmp');self.addCleanup(self.temp.cleanup)
        self.film=Path(self.temp.name);(self.film/'00_brief').mkdir()
        self.job=dict(job='SYNTHETIC-1',tool='image_to_video',model='kling-video-v3_0',prompt='Synthetic test.',args={'duration':'5','imageCount':'1','resolution':'720p','enable_audio':False,'prefer_multi_shots':False},images=['https://example.invalid/input.png'],auth='APR-SYNTHETIC')
        self.now=dt.datetime(2026,10,12,tzinfo=dt.timezone.utc)
        (self.film/'00_brief/evidence.txt').write_text('Synthetic decision and price fixture. No real authorization.')
        evidence={'path':'00_brief/evidence.txt','sha256':r.file_hash(self.film/'00_brief/evidence.txt')}
        fingerprint=r.fingerprint(self.film,self.job)
        self.entry={'id':self.job['auth'],'kind':'kling_job_release','status':'approved','decisionEvidence':evidence,'scope':{'job':self.job['job'],'payloadSha256':fingerprint,'schemaSha256':'a'*64,'maxJobs':1,'maxCredits':30,'expiresAt':'2099-01-01T00:00:00Z','allowReferenceUploads':False,'quote':{'basis':'official_panel','unit':'Kling credits','payloadSha256':fingerprint,'credits':27,'verifiedAt':'2026-10-11T00:00:00Z','expiresAt':'2099-01-01T00:00:00Z','evidence':evidence}}}
        self.save()

    def save(self):
        (self.film/'00_brief/approvals.json').write_text(json.dumps({'approvals':[self.entry]}))

    def authorize(self): return r.authorize(self.film,self.job,now=self.now)

    def test_exact_scoped_quote_is_separate_from_provider_ceiling(self):
        result=self.authorize();self.assertEqual(result['quote']['credits'],27)
        self.assertFalse(result['providerEnforcesCeiling'])

    def test_missing_scope_stops_runner_before_any_provider_call(self):
        self.entry['kind']='local_plan_implementation';self.save()
        with patch.object(k,'run') as run,patch.object(k,'account') as account:
            with self.assertRaisesRegex(SystemExit,'não libera'):
                k.submit(self.film,self.job['job'],self.job['tool'],self.job['model'],self.job['prompt'],self.job['args'],self.job['images'],self.job['auth'],'',submit_only=True)
            run.assert_not_called();account.assert_not_called()

    def test_changed_content_no_longer_authorized(self):
        self.job['prompt']='different'
        with self.assertRaisesRegex(SystemExit,'difere'): self.authorize()

    def test_declared_reference_facts_cannot_change_under_same_release(self):
        self.job['inputFacts']={'video_1':{'durationSeconds':5}}
        fingerprint=r.fingerprint(self.film,self.job)
        self.entry['scope']['payloadSha256']=fingerprint
        self.entry['scope']['quote']['payloadSha256']=fingerprint
        self.save();self.authorize()
        self.job['inputFacts']['video_1']['durationSeconds']=30
        with self.assertRaisesRegex(SystemExit,'difere'): self.authorize()

    def test_quote_cannot_be_estimate_wrong_currency_or_above_cap(self):
        for change in [{'basis':'estimate'},{'unit':'API units'},{'credits':31},{'credits':True},{'credits':float('nan')}]:
            with self.subTest(change=change):
                original=copy.deepcopy(self.entry);self.entry['scope']['quote'].update(change);self.save()
                with self.assertRaises(SystemExit): self.authorize()
                self.entry=original

    def test_expired_or_wrong_payload_quote_is_blocked(self):
        for change in [{'expiresAt':'2020-01-01T00:00:00Z'},{'payloadSha256':'b'*64},{'verifiedAt':'2099-01-01T00:00:00Z'}]:
            original=copy.deepcopy(self.entry);self.entry['scope']['quote'].update(change);self.save()
            with self.assertRaises(SystemExit): self.authorize()
            self.entry=original

    def test_changed_price_evidence_blocks(self):
        (self.film/'00_brief/evidence.txt').write_text('changed')
        with self.assertRaisesRegex(SystemExit,'hash'): self.authorize()

    def test_local_upload_must_be_in_scope(self):
        (self.film/'frame.png').write_bytes(b'synthetic')
        self.job['images']=['frame.png'];fp=r.fingerprint(self.film,self.job)
        self.entry['scope']['payloadSha256']=fp;self.entry['scope']['quote']['payloadSha256']=fp;self.save()
        with self.assertRaisesRegex(SystemExit,'upload'): self.authorize()
        self.entry['scope']['allowReferenceUploads']=True;self.save();self.authorize()

    def test_outside_evidence_and_symlinks_rejected(self):
        self.entry['decisionEvidence']['path']='../outside';self.save()
        with self.assertRaises(SystemExit): self.authorize()

    def test_renaming_same_unknown_payload_is_blocked(self):
        folder=self.film/'07_generations/responses';folder.mkdir(parents=True)
        (folder/'old.intent.json').write_text(json.dumps({**self.job,'job':'old','payloadSha256':r.fingerprint(self.film,self.job)}))
        with self.assertRaisesRegex(SystemExit,'renomear'): r.reject_duplicate(self.film,self.job)

    def test_legacy_intent_and_equivalent_input_alias_detected(self):
        folder=self.film/'07_generations/responses';folder.mkdir(parents=True)
        prior={'job':'old','tool':self.job['tool'],'model':self.job['model'],'prompt':self.job['prompt'],'options':self.job['args'],'refs':self.job['images']}
        (folder/'old.intent.json').write_text(json.dumps(prior))
        self.job['inputs']={'first_image':self.job['images'][0]};self.job['images']=[]
        with self.assertRaisesRegex(SystemExit,'renomear'): r.reject_duplicate(self.film,self.job)

    def test_schema_drift_stops_before_balance_and_submit(self):
        with patch.object(k,'preflight',return_value={'schemaSha256':'b'*64}),patch.object(k,'account') as account,patch.object(k,'run') as run:
            with self.assertRaisesRegex(SystemExit,'schema mudou'):
                k.submit(self.film,self.job['job'],self.job['tool'],self.job['model'],self.job['prompt'],self.job['args'],self.job['images'],self.job['auth'],'',submit_only=True)
            account.assert_not_called();run.assert_not_called()

    def test_insufficient_balance_never_uploads_or_generates(self):
        with patch.object(k,'preflight',return_value={'schemaSha256':'a'*64}),patch.object(k,'account',return_value=26),patch.object(k,'run') as run:
            with self.assertRaisesRegex(SystemExit,'saldo inferior'):
                k.submit(self.film,self.job['job'],self.job['tool'],self.job['model'],self.job['prompt'],self.job['args'],self.job['images'],self.job['auth'],'',submit_only=True)
            run.assert_not_called()

    def run_actual_gates(self):
        j=self.job
        return k.submit(self.film,j['job'],j['tool'],j['model'],j['prompt'],
                        j['args'],j['images'],j['auth'],'',submit_only=True,
                        inputs=j.get('inputs'),input_facts=j.get('inputFacts'))

    def bind_current_payload(self):
        fp=r.fingerprint(self.film,self.job)
        self.entry['scope']['payloadSha256']=fp
        self.entry['scope']['quote']['payloadSha256']=fp
        self.save()

    def assert_blocked_before_discovery(self,pattern):
        with patch.object(k,'preflight') as discovery,patch.object(k,'account') as account,patch.object(k,'run') as run:
            with self.assertRaisesRegex(SystemExit,pattern):self.run_actual_gates()
            discovery.assert_not_called();account.assert_not_called();run.assert_not_called()

    def test_absent_reference_blocks_runner_before_discovery(self):
        self.job['images']=['missing-reference.png']
        self.assert_blocked_before_discovery('referência local ausente')

    def test_changed_local_reference_blocks_runner_before_discovery(self):
        ref=self.film/'synthetic-reference.png';ref.write_bytes(b'synthetic version one')
        self.job['images']=[ref.name];self.entry['scope']['allowReferenceUploads']=True
        self.bind_current_payload();ref.write_bytes(b'synthetic version two')
        self.assert_blocked_before_discovery('difere')

    def test_pending_release_blocks_runner_before_discovery(self):
        self.entry['status']='pending';self.save()
        self.assert_blocked_before_discovery('não libera')

    def test_expired_quote_blocks_runner_before_discovery(self):
        self.entry['scope']['quote']['expiresAt']='2020-01-01T00:00:00Z';self.save()
        self.assert_blocked_before_discovery('cotação vencida')

    def test_renamed_intent_only_blocks_runner_before_discovery(self):
        folder=self.film/'07_generations/responses';folder.mkdir(parents=True)
        (folder/'previous.intent.json').write_text(json.dumps({**self.job,'job':'previous','payloadSha256':r.fingerprint(self.film,self.job)}))
        self.assert_blocked_before_discovery('renomear')

    def test_incompatible_model_blocks_after_only_readonly_discovery(self):
        self.job['model']='kling-video-v3_0_turbo';self.bind_current_payload()
        models=json.loads((ROOT/'docs/kling-manual/snapshots/who_am_i.sanitized.json').read_text())['body']['availableModels']
        with patch.object(k,'run',return_value={'ok':True,'body':{'availableModels':models}}) as run,patch.object(k,'account') as account:
            with self.assertRaisesRegex(SystemExit,'ARG_UNKNOWN'):self.run_actual_gates()
            self.assertEqual([call.args[0][1] for call in run.call_args_list],['who_am_i'])
            account.assert_not_called()
            self.assertFalse(list((self.film/'07_generations/responses').glob('*.intent.json')))

    def test_uncertain_transport_is_durable_with_actual_release_gate(self):
        models=json.loads((ROOT/'docs/kling-manual/snapshots/who_am_i.sanitized.json').read_text())['body']['availableModels']
        import hashlib
        self.entry['scope']['schemaSha256']=hashlib.sha256(json.dumps(models,sort_keys=True).encode()).hexdigest();self.save()
        def simulated_transport(cmd):
            if cmd[1]=='who_am_i':return {'ok':True,'body':{'availableModels':models}}
            if cmd[1]=='image_to_video':raise TimeoutError('synthetic timeout, no real network')
            raise AssertionError('unexpected transport: '+cmd[1])
        with patch.object(k,'run',side_effect=simulated_transport) as run,patch.object(k,'account',side_effect=[100,80]):
            result=self.run_actual_gates()
            self.assertEqual(result['status'],'SUBMISSION_UNKNOWN')
            self.assertEqual([call.args[0][1] for call in run.call_args_list],['who_am_i','image_to_video'])
        folder=self.film/'07_generations/responses'
        self.assertTrue((folder/(self.job['job']+'.intent.json')).is_file())
        self.assertTrue(json.loads((folder/(self.job['job']+'.submit.json')).read_text())['submissionUncertain'])
        with patch.object(k,'run') as run,patch.object(k,'account') as account:
            with self.assertRaisesRegex(SystemExit,'never resubmit'):self.run_actual_gates()
            self.assertEqual(k.resume(self.film,self.job['job'])['status'],'SUBMISSION_UNKNOWN')
            self.job['job']='RENAMED-UNCERTAIN'
            with self.assertRaisesRegex(SystemExit,'renomear'):self.run_actual_gates()
            run.assert_not_called();account.assert_not_called()

    def test_readonly_registry_keeps_unknown_charge_and_no_acceptance(self):
        folder=self.film/'07_generations/responses';folder.mkdir(parents=True)
        (folder/'S.intent.json').write_text(json.dumps(self.job))
        (folder/'S.balance.json').write_text(json.dumps({'creditsDelta':20,'creditsConsumed':None,'chargeBasis':'unknown'}))
        result=r.registry(self.film)[0]
        self.assertEqual(result['status'],'SUBMISSION_UNKNOWN');self.assertIsNone(result['providerReportedCredits'])
        self.assertFalse(result['balanceDeltaIsCharge']);self.assertEqual(result['creativeApproval'],'not_inferred')


class ConditionalContractTests(unittest.TestCase):
    def setUp(self):
        self.models=json.loads((ROOT/'docs/kling-manual/snapshots/who_am_i.sanitized.json').read_text())['body']['availableModels']
        self.job=dict(job='MOCK',tool='omni_ref_video',model='kling-video-v3_0_omni',prompt='test',auth='test',args={'duration':'5','resolution':'720p','imageCount':'1','enable_audio':False,'keepOriginalSound':False,'prefer_multi_shots':False,'aspect_ratio':'16:9'},inputs={'video_1':'https://example.invalid/video.mp4'},inputFacts={'video_1':{'durationSeconds':5,'width':1280,'height':720,'fps':24,'bytes':1000}})

    def codes(self,job=None): return {i['code'] for i in k.pf.check_job(job or self.job,self.models,'/tmp','/tmp',False).items if i['level']=='ERROR'}

    def test_video_plus_five_images_breaks_conditional_cap(self):
        self.job['inputs'].update({f'image_{i}':f'https://example.invalid/{i}.png' for i in range(1,6)})
        self.assertIn('COMBINED_CAP',self.codes())

    def test_sparse_image_slots_count_items_not_last_index(self):
        self.job['inputs']['image_7']='https://example.invalid/frame.png'
        self.assertEqual(self.codes(),set())

    def test_direct_video_disables_native_audio(self):
        self.job['args']['enable_audio']=True
        self.assertIn('OMNI_VIDEO_AUDIO',self.codes())

    def test_video_requires_measured_facts_and_local_decode(self):
        self.job.pop('inputFacts');self.assertIn('VIDEO_FACTS_REQUIRED',self.codes())

    def test_thirty_second_video_not_accepted_as_five_second_budget(self):
        self.job['inputFacts']['video_1']['durationSeconds']=30
        self.assertIn('VIDEO_LIMIT',self.codes())

    def test_video_element_cannot_mix_with_image_when_video_present(self):
        self.job['elements']=[{'id':'123','bindName':'actor','type':'video'}];self.job['prompt']='<<<123>>>'
        self.job['inputs']['image_7']='https://example.invalid/frame.png'
        self.assertIn('VIDEO_ELEMENT_MIX',self.codes())

    def test_element_type_required_for_conditional_routes(self):
        self.job['elements']=[{'id':'123','bindName':'actor'}];self.job['prompt']='<<<123>>>'
        self.assertIn('ELEMENT_TYPE_REQUIRED',self.codes())

    def test_v26_audio_tail_resolution(self):
        job={'job':'MOCK','tool':'image_to_video','model':'kling-video-v2_6','prompt':'test','args':{'enable_audio':True,'resolution':'720p'},'inputs':{'first_image':'https://example.invalid/a.png','tail_image':'https://example.invalid/b.png'}}
        self.assertTrue({'V26_AUDIO','V26_TAIL_RESOLUTION'}<=self.codes(job))


if __name__=='__main__': unittest.main()
