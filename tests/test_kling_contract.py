"""Contract regression tests. All providers, uploads and asset transfers are mocked."""
import copy
import csv
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('contract_runner', ROOT / 'scripts/kling_batch.py')
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)
MODELS = json.loads((ROOT / 'docs/kling-manual/snapshots/who_am_i.sanitized.json').read_text())['body']['availableModels']


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir='/tmp')
        self.addCleanup(self.temp.cleanup)
        self.film = Path(self.temp.name)
        self.job = dict(job='T1', tool='image_to_video', model='kling-video-v3_0', auth='scope-test',
                        prompt='a quiet blink', images=['https://example.invalid/frame.jpg'],
                        args=dict(duration='5', resolution='720p', imageCount='1', enable_audio=False, prefer_multi_shots=False))

    def submit(self, **overrides):
        j = {**self.job, **overrides}
        return k.submit(self.film, j['job'], j['tool'], j['model'], j['prompt'], j['args'],
                        j['images'], j['auth'], '', submit_only=True, inputs=j.get('inputs'),
                        elements=j.get('elements'), reference_duration=j.get('referenceDurationSeconds'),
                        submission_blocked=j.get('submissionBlocked'))

    def responses(self, cmd):
        if cmd[1] == 'who_am_i':
            return {'ok': True, 'body': {'availableModels': MODELS}}
        if cmd[1] == 'query_tasks':
            return {'ok': True, 'body': {'generationId': 'fake-id', 'status': 'RUNNING'}}
        return {'ok': True, 'body': {'generationId': 'fake-id', 'creditsConsumed': 0}}

    def test_unbound_element_stops_before_balance_or_submission(self):
        with patch.object(k, 'run', side_effect=self.responses) as run, patch.object(k, 'account') as account:
            with self.assertRaisesRegex(SystemExit, 'ELEMENT_NOBIND'):
                self.submit(model='kling-video-v3_0_turbo', prompt='<<<123>>> blink',
                            args={'duration': '5', 'resolution': '720p', 'imageCount': '1'})
            self.assertEqual([x.args[0][1] for x in run.call_args_list], ['who_am_i'])
            account.assert_not_called()

    def test_missing_explicit_audio_or_multishot_fails_closed(self):
        with patch.object(k, 'run', side_effect=self.responses), patch.object(k, 'account') as account:
            with self.assertRaisesRegex(SystemExit, 'DEFAULT'):
                self.submit(args={'duration': '5', 'resolution': '720p', 'imageCount': '1'})
            account.assert_not_called()

    def test_placeholder_and_blocked_plan_make_no_calls(self):
        with patch.object(k, 'run') as run, patch.object(k, 'account') as account:
            for kw in ({'auth': 'REPLACE-WITH-AUTHORIZED-APR-ID'}, {'submissionBlocked': 'draft'}):
                with self.subTest(kw=kw), self.assertRaises(SystemExit):
                    self.submit(**kw)
            run.assert_not_called()
            account.assert_not_called()

    def test_named_inputs_and_native_elements_are_not_dropped(self):
        with patch.object(k, 'run', side_effect=self.responses) as run, patch.object(k, 'account', side_effect=[100, 50]):
            self.submit(images=[], inputs={'first_image': 'https://example.invalid/frame.jpg'},
                        elements=[{'id': '123', 'bindName': 'Andre'}], prompt='<<<123>>> blink')
        cmd = run.call_args_list[-1].args[0]
        self.assertEqual(cmd[cmd.index('--input') + 1], 'first_image=https://example.invalid/frame.jpg')
        self.assertEqual(json.loads(cmd[cmd.index('--elements') + 1]), [{'id': '123', 'bindName': 'Andre'}])
        self.assertEqual(cmd[cmd.index('--enable_audio') + 1], 'false')
        intent = json.loads((self.film / '07_generations/responses/T1.intent.json').read_text())
        self.assertIn('schemaSha256', intent['validation'])

    def test_aliases_are_canonicalized_before_cli(self):
        args = dict(self.job['args'])
        args['enableAudio'] = args.pop('enable_audio')
        args['image_count'] = args.pop('imageCount')
        with patch.object(k, 'run', side_effect=self.responses) as run, patch.object(k, 'account', side_effect=[100, 100]):
            self.submit(args=args)
        cmd = run.call_args_list[-1].args[0]
        self.assertIn('--enable_audio', cmd)
        self.assertIn('--imageCount', cmd)
        self.assertNotIn('--enableAudio', cmd)
        self.assertNotIn('--image_count', cmd)

    def test_duplicate_argument_alias_fails_before_submission(self):
        args = {**self.job['args'], 'enableAudio': True}
        with patch.object(k, 'run', side_effect=self.responses), patch.object(k, 'account') as account:
            with self.assertRaisesRegex(SystemExit, 'ARG_DUPLICATE'):
                self.submit(args=args)
            account.assert_not_called()

    def test_mixed_named_and_positional_inputs_are_rejected(self):
        with patch.object(k, 'run', side_effect=self.responses), patch.object(k, 'account') as account:
            with self.assertRaisesRegex(SystemExit, 'INPUT_MIX'):
                self.submit(inputs={'tail_image': 'https://example.invalid/tail.jpg'})
            account.assert_not_called()

    def test_provider_zero_charge_beats_concurrent_balance_delta(self):
        with patch.object(k, 'run', side_effect=self.responses), patch.object(k, 'account', side_effect=[100, 20]):
            result = self.submit()
        self.assertEqual(result['creditsDelta'], 80)
        self.assertEqual(result['creditsConsumed'], 0)
        self.assertFalse(result['balanceDeltaIsCharge'])
        row = next(csv.reader((self.film / 'credit-ledger.csv').read_text().splitlines()))
        self.assertEqual(float(row[6]), 0)

    def test_unknown_charge_stays_blank_not_balance_delta(self):
        def network(cmd):
            data = self.responses(cmd)
            data.get('body', {}).pop('creditsConsumed', None)
            return data
        with patch.object(k, 'run', side_effect=network), patch.object(k, 'account', side_effect=[100, 20]):
            result = self.submit()
        self.assertIsNone(result['creditsConsumed'])
        row = next(csv.reader((self.film / 'credit-ledger.csv').read_text().splitlines()))
        self.assertEqual(row[6], '')

    def test_timeout_uncertainty_is_durable_and_never_retried(self):
        def network(cmd):
            if cmd[1] == 'who_am_i':
                return self.responses(cmd)
            raise TimeoutError('synthetic timeout')
        with patch.object(k, 'run', side_effect=network), patch.object(k, 'account', side_effect=[100, 80]):
            self.assertEqual(self.submit()['status'], 'SUBMISSION_UNKNOWN')
        with patch.object(k, 'run') as run, patch.object(k, 'account') as account:
            with self.assertRaises(SystemExit):
                self.submit()
            self.assertEqual(k.resume(self.film, 'T1')['status'], 'SUBMISSION_UNKNOWN')
            run.assert_not_called()
            account.assert_not_called()

    def test_success_without_assets_is_not_reported_complete(self):
        with patch.object(k, 'run', side_effect=self.responses), patch.object(k, 'account', side_effect=[100, 100]):
            self.submit()
        for status in ('COMPLETED', 'succeeded', 'SUCCESS'):
            data = {'ok': True, 'body': {'generationId': 'fake-id', 'status': status, 'works': []}}
            with patch.object(k, 'run', return_value=data), patch.object(k, 'download') as download:
                self.assertEqual(k.resume(self.film, 'T1')['status'], 'RESULT_EMPTY')
                download.assert_not_called()

    def test_query_error_never_downloads_even_with_success_status(self):
        with patch.object(k, 'run', side_effect=self.responses), patch.object(k, 'account', side_effect=[100, 100]):
            self.submit()
        data = {'ok': False, 'body': {'generationId': 'fake-id', 'status': 'COMPLETED', 'works': [{'url': 'https://example.invalid/v.mp4'}]}}
        with patch.object(k, 'run', return_value=data), patch.object(k, 'download') as download:
            self.assertEqual(k.resume(self.film, 'T1')['status'], 'QUERY_ERROR')
            download.assert_not_called()

    def test_large_json_capture_does_not_use_pipe(self):
        data = k.run([sys.executable, '-c', 'import json; print(json.dumps({"ok":True,"body":{"payload":"x"*300000}}))'])
        self.assertEqual(len(data['body']['payload']), 300000)
        with patch.object(k.subprocess, 'run', return_value=subprocess.CompletedProcess(['fake'], 0, '{}', '')) as run:
            k.run(['fake'])
            self.assertNotIn('capture_output', run.call_args.kwargs)
            self.assertNotEqual(run.call_args.kwargs['stdout'], subprocess.PIPE)

    def test_secrets_and_signed_queries_redacted_in_diagnostics(self):
        raw = json.dumps({'ok': True, 'body': {'access_token': 'SYNTHETIC_SECRET', 'url': 'https://example.invalid/a?signature=fake'}})
        process = subprocess.CompletedProcess(['fake'], 0, raw, 'Authorization: Bearer SYNTHETIC_SECRET')
        with patch.object(k.subprocess, 'run', return_value=process):
            data = k.run(['fake'])
        self.assertEqual(data['body']['access_token'], '[REDACTED]')
        self.assertNotIn('SYNTHETIC_SECRET', json.dumps(data['_cli']))
        self.assertNotIn('signature=fake', data['_cli']['stdout'])
        self.assertEqual(data['body']['url'], 'https://example.invalid/a?signature=fake')

    def test_non_https_asset_is_rejected_without_fetch(self):
        with patch.object(k.urllib.request, 'urlopen') as fetch:
            with self.assertRaisesRegex(ValueError, 'HTTPS'):
                k.download(self.film, 'T1', 'fake-id', {}, [{'url': 'file:///tmp/fake.mp4'}])
            fetch.assert_not_called()

    def test_empty_download_creates_no_original(self):
        response = io.BytesIO(b'')
        response.geturl = lambda: 'https://example.invalid/v.mp4'
        with patch.object(k.urllib.request, 'urlopen', return_value=response):
            with self.assertRaisesRegex(ValueError, 'empty asset'):
                k.download(self.film, 'T1', 'fake-id', {}, [{'url': response.geturl()}])
        self.assertFalse((self.film / '07_generations/originals/T1_1.mp4').exists())


class PreflightRegressionTests(unittest.TestCase):
    def report(self, job, models=MODELS):
        return k.pf.check_job(job, models, '/tmp', '/tmp', False).items

    def test_model_declared_element_limit_is_enforced(self):
        job = {'tool': 'motion_control', 'model': 'kling-video-v3_0', 'images': ['https://example.invalid/x.jpg'],
               'args': {'motionId': '123', 'motionDirection': 'motion_direction', 'elements': [{'id':'1','bindName':'a'},{'id':'2','bindName':'b'}]},
               'prompt': '<<<1>>> <<<2>>>', 'referenceDurationSeconds': 30}
        self.assertIn('ELEMENTS_CAP', [i['code'] for i in self.report(job)])

    def test_motion_duration_and_source_are_not_inferred_as_five_seconds(self):
        job = {'tool':'motion_control','model':'kling-video-v3_0','images':['https://example.invalid/x.jpg'],
               'args':{'motionId':'123','motionDirection':'image_direction'},'prompt':'move','referenceDurationSeconds':30}
        self.assertIn('MOTION_DURATION', [i['code'] for i in self.report(job)])
        del job['referenceDurationSeconds']
        self.assertIn('MOTION_DURATION_UNKNOWN', [i['code'] for i in self.report(job)])

    def test_tail_is_never_filled_by_second_image(self):
        job={'tool':'image_to_video','model':'kling-video-v3_0','prompt':'x','images':['https://example.invalid/1','https://example.invalid/2']}
        self.assertIn('SLOT_COUNT',[i['code'] for i in self.report(job)])

    def test_combined_cap_and_omni_audio_exclusion(self):
        models=copy.deepcopy(MODELS)
        spec=models['omni_ref_video']['models'][0]
        spec['combinedItemCap']={'maxItems':1,'inputPrefixes':['image_'],'arguments':['elements']}
        spec['inputs']=[{'name':'image_1','required':False}]
        spec['arguments']=[{'name':n,'required':False} for n in ['prompt','elements','enable_audio','keepOriginalSound']]
        job={'tool':'omni_ref_video','model':spec['model'],'prompt':'<<<1>>> x','inputs':{'image_1':'https://example.invalid/x'},
             'args':{'elements':[{'id':'1','bindName':'a'}],'enable_audio':True,'keepOriginalSound':True}}
        codes=[i['code'] for i in self.report(job,models)]
        self.assertIn('COMBINED_CAP',codes)
        self.assertIn('OMNI_AUDIO',codes)


if __name__ == '__main__':
    unittest.main()
