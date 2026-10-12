"""Offline producer tests: never invoke Kling or download live assets."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import io


def mock_response(url):
    response = io.BytesIO(b'mock media')
    response.geturl = lambda: url
    return response


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('kling_batch', ROOT / 'scripts/kling_batch.py')
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)


class ProducerTests(unittest.TestCase):
    def setUp(self):
        scratch = Path(os.environ.get('TMPDIR', Path.home() / '.hermes/cache/scratch'))
        scratch.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.tmp.cleanup)
        self.film = Path(self.tmp.name)
        self.preflight_patch = patch.object(k, 'preflight', return_value={})
        self.preflight_patch.start()
        self.addCleanup(self.preflight_patch.stop)

    def submit(self, **kwargs):
        return k.submit(self.film, 'J1', 'text_to_video', 'mock-model', 'prompt',
                        {'duration': '5'}, [], 'approved-scope', 'note', **kwargs)

    def test_submit_marker_blocks_before_account_or_network(self):
        path = self.film / '07_generations/responses/J1.submit.json'
        path.parent.mkdir(parents=True)
        path.write_text('{}')
        with patch.object(k, 'account') as account, patch.object(k, 'run') as run:
            with self.assertRaises(SystemExit):
                self.submit()
            account.assert_not_called()
            run.assert_not_called()

    def test_pre_submit_account_snapshot_is_durable_before_network(self):
        import subprocess
        def cli(cmd, **kwargs):
            if cmd[1] == 'account':
                return subprocess.CompletedProcess(cmd, 0, json.dumps({'body': {'availableRemainCredits': 100}}), '')
            intent = json.loads((self.film / '07_generations/responses/J1.intent.json').read_text())
            self.assertEqual(intent['accountBefore']['body']['availableRemainCredits'], 100)
            return subprocess.CompletedProcess(cmd, 0, json.dumps({'body': {'generationId': 'mock-id'}}), '')
        with patch.object(k.subprocess, 'run', side_effect=cli):
            result = self.submit(submit_only=True)
        self.assertEqual(result['generationId'], 'mock-id', result)

    def test_post_submit_unavailable_balance_has_unknown_delta_and_zero_is_retained(self):
        for after in (None, 0):
            film = self.film / str(after)
            with patch.object(k, 'account', side_effect=[100, after]), patch.object(k, 'run', return_value={'body': {'generationId': 'mock-id'}}):
                result = k.submit(film, 'J1', 'text_to_video', 'mock', 'prompt', {}, [], 'auth', '', submit_only=True)
            self.assertEqual(result['balanceAfter'], after)
            self.assertEqual(result['creditsDelta'], None if after is None else 100)
            import csv
            row = next(csv.reader((film / 'credit-ledger.csv').read_text().splitlines()))
            self.assertEqual(row[8], '' if after is None else '0')

    def test_legacy_batch_interface_reconciles_before_poll(self):
        calls = []
        def network(cmd):
            calls.append(cmd[1])
            if cmd[1] != 'query_tasks':
                return {'body': {'generationId': 'mock-id'}}
            self.assertTrue((self.film / 'credit-ledger.csv').exists())
            return {'body': {'generations': [{'status': 'COMPLETED', 'result': {'works': [{'url': 'https://mock/test.mp4'}]}}]}}
        with patch.object(k, 'account', side_effect=[100, 80]), patch.object(k, 'run', side_effect=network), patch.object(k, 'download', return_value=['mock.mp4']):
            result = self.submit()
        self.assertEqual(result['status'], 'COMPLETED')
        self.assertEqual(calls, ['text_to_video', 'query_tasks'])

    def test_submit_only_archives_intent_then_reconciles_without_query(self):
        def network(cmd):
            intent = json.loads((self.film / '07_generations/responses/J1.intent.json').read_text())
            self.assertEqual(intent['balanceBefore'], 100)
            self.assertEqual(intent['prompt'], 'prompt')
            self.assertEqual(intent['auth'], 'approved-scope')
            self.assertEqual(cmd[cmd.index('--poll') + 1], '0')
            return {'body': {'generationId': 'mock-id'}}
        with patch.object(k, 'account', side_effect=[100, 80]), patch.object(k, 'run', side_effect=network) as run:
            result = self.submit(submit_only=True)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(result['creditsDelta'], 20)
        self.assertEqual(result['generationId'], 'mock-id')
        self.assertEqual(len((self.film / 'credit-ledger.csv').read_text().splitlines()), 1)
        with patch.object(k, 'account') as account, patch.object(k, 'run', return_value={'body': {'generations': [{'generationId': 'mock-id', 'status': 'RUNNING'}]}}) as run:
            result = k.resume(self.film, 'J1')
        account.assert_not_called()
        self.assertEqual(run.call_args.args[0][1:3], ['query_tasks', 'mock-id'])
        self.assertEqual(run.call_count, 1)
        self.assertEqual(result['status'], 'RUNNING')
        self.assertEqual(len((self.film / 'credit-ledger.csv').read_text().splitlines()), 1)

    def test_reconciliation_preserves_existing_ledger_bytes(self):
        ledger = self.film / 'credit-ledger.csv'
        previous = b'id,created,provider\r\nLold,time,Kling\r\n'
        ledger.write_bytes(previous)
        with patch.object(k, 'account', side_effect=[100, 80]), patch.object(k, 'run', return_value={'body': {'generationId': 'mock-id'}}):
            self.submit(submit_only=True)
        self.assertTrue(ledger.read_bytes().startswith(previous))

    def test_existing_prompt_is_not_overwritten(self):
        prompt = self.film / '07_generations/requests/J1.prompt.txt'
        prompt.parent.mkdir(parents=True)
        prompt.write_text('original prompt\n')
        with patch.object(k, 'account', return_value=100), patch.object(k, 'run') as run:
            with self.assertRaisesRegex(SystemExit, 'existing prompt differs'):
                self.submit(submit_only=True)
            run.assert_not_called()
        self.assertEqual(prompt.read_text(), 'original prompt\n')

    def test_all_evidence_markers_fail_closed(self):
        for kind in ('response', 'submit', 'intent'):
            with self.subTest(kind=kind):
                path = self.film / f'07_generations/responses/J1.{kind}.json'
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('incomplete')
                with patch.object(k, 'account') as account, patch.object(k, 'run') as run:
                    with self.assertRaises(SystemExit):
                        self.submit(submit_only=True)
                    account.assert_not_called()
                    run.assert_not_called()
                path.unlink()

    def test_unavailable_balance_never_submits(self):
        with patch.object(k, 'account', return_value=None), patch.object(k, 'run') as run:
            with self.assertRaisesRegex(SystemExit, 'balance unavailable'):
                self.submit(submit_only=True)
            run.assert_not_called()
        self.assertFalse((self.film / '07_generations/responses/J1.intent.json').exists())

    def test_unknown_id_failures_still_record_charge_once(self):
        for response in ({'ok': False, 'raw': 'bad'}, {'body': {'generations': [None]}}):
            with self.subTest(response=response):
                film = self.film / str(len(list(self.film.iterdir())))
                with patch.object(k, 'account', side_effect=[100, 80]), patch.object(k, 'run', return_value=response):
                    result = k.submit(film, 'J1', 'text_to_video', 'mock', 'prompt', {}, [], 'auth', '', submit_only=True)
                self.assertEqual(result['creditsDelta'], 20)
                self.assertEqual(result['status'], 'SUBMISSION_UNKNOWN')
                with patch.object(k, 'account') as account, patch.object(k, 'run') as run:
                    result = k.resume(film, 'J1')
                    account.assert_not_called()
                    run.assert_not_called()
                self.assertEqual(len((film / 'credit-ledger.csv').read_text().splitlines()), 1)

    def test_network_exception_records_unknown_charge(self):
        with patch.object(k, 'account', side_effect=[100, 80]), patch.object(k, 'run', side_effect=TimeoutError('uncertain')):
            result = self.submit(submit_only=True)
        self.assertEqual(result['creditsDelta'], 20)
        self.assertTrue(result['error']['submissionUncertain'])

    def test_crash_between_receipt_and_ledger_is_recoverable(self):
        original = k.durable
        def fail_ledger(path, text):
            if path.name == 'credit-ledger.csv':
                raise OSError('mock disk failure')
            return original(path, text)
        with patch.object(k, 'account', side_effect=[100, 80]), patch.object(k, 'run', return_value={'body': {'generationId': 'mock-id'}}), patch.object(k, 'durable', side_effect=fail_ledger):
            with self.assertRaises(OSError):
                self.submit(submit_only=True)
        for _ in range(2):
            with patch.object(k, 'account') as account, patch.object(k, 'run', return_value={'body': {'generations': [{'status': 'RUNNING'}]}}):
                k.resume(self.film, 'J1')
                account.assert_not_called()
        self.assertEqual(len((self.film / 'credit-ledger.csv').read_text().splitlines()), 1)

    def test_intent_only_recovery_does_not_claim_delayed_charge(self):
        path = self.film / '07_generations/responses/J1.intent.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({'balanceBefore': 100, 'created': 'mock-time', 'auth': 'scope', 'model': 'mock', 'tool': 'text_to_video', 'options': {}, 'note': ''}))
        with patch.object(k, 'account', return_value=70), patch.object(k, 'run') as run:
            result = k.resume(self.film, 'J1')
            run.assert_not_called()
        self.assertIsNone(result['creditsDelta'])
        self.assertEqual(result['status'], 'SUBMISSION_UNKNOWN')

    def test_run_preserves_raw_subprocess_response(self):
        import subprocess
        proc = subprocess.CompletedProcess(['mock'], 1, 'not json\n', 'mock error')
        with patch.object(k.subprocess, 'run', return_value=proc):
            result = k.run(['mock'])
        self.assertFalse(result['ok'])
        self.assertEqual(result['_cli']['stdout'], 'not json\n')
        self.assertEqual(result['_cli']['rc'], 1)

    def test_completed_resume_preserves_default_url_mp4_and_hash(self):
        import hashlib
        with patch.object(k, 'account', side_effect=[100, 80]), patch.object(k, 'run', return_value={'body': {'generationId': 'mock-id'}}):
            self.submit(submit_only=True)
        data = {'body': {'generations': [{'generationId': 'mock-id', 'status': 'COMPLETED', 'result': {'works': [{'url': 'https://mock/default', 'urlWithoutWatermark': 'https://mock/clean', 'contentType': 'video/mp4'}]}}]}}
        def retrieve(url, path):
            self.assertEqual(url, 'https://mock/default')
            Path(path).write_bytes(b'mock media')
        with patch.object(k, 'run', return_value=data), patch.object(k.urllib.request, 'urlopen', side_effect=lambda url, **kw: mock_response(url)) as download:
            result = k.resume(self.film, 'J1')
            target = self.film / result['works'][0]
            before = target.stat().st_mtime_ns
            k.resume(self.film, 'J1')
            self.assertEqual(download.call_count, 1)
            self.assertEqual(target.stat().st_mtime_ns, before)
        self.assertEqual(target.suffix, '.mp4')
        meta = json.loads(target.with_suffix('.json').read_text())
        self.assertEqual(meta['sha256'], hashlib.sha256(b'mock media').hexdigest())
        self.assertEqual(meta['url'], 'https://mock/default')

    def test_resume_live_flat_response_running_and_completed(self):
        with patch.object(k, 'account', side_effect=[100, 80]), patch.object(k, 'run', return_value={'body': {'generationId': 'mock-id'}}):
            self.submit(submit_only=True)
        running = {'ok': True, 'body': {'generationId': 'mock-id', 'status': 'RUNNING', 'works': [{'status': 'RUNNING'}]}}
        with patch.object(k, 'run', return_value=running):
            self.assertEqual(k.resume(self.film, 'J1')['status'], 'RUNNING')
        completed = {'ok': True, 'body': {'generationId': 'mock-id', 'status': 'COMPLETED', 'works': [{'url': 'https://mock/video.mp4', 'contentType': 'video'}]}}
        def retrieve(url, path):
            Path(path).write_bytes(b'mock video')
        with patch.object(k, 'run', return_value=completed), patch.object(k.urllib.request, 'urlopen', side_effect=lambda url, **kw: mock_response(url)):
            self.assertEqual(len(k.resume(self.film, 'J1')['works']), 1)
        wrong = {'ok': True, 'body': {'generationId': 'other-id', 'status': 'COMPLETED', 'works': []}}
        with patch.object(k, 'run', return_value=wrong):
            self.assertEqual(k.resume(self.film, 'J1')['status'], 'QUERY_UNKNOWN')

    def test_different_existing_original_is_never_overwritten(self):
        original = self.film / '07_generations/originals/J1_1.mp4'
        original.parent.mkdir(parents=True)
        original.write_bytes(b'original')
        def retrieve(url, path):
            Path(path).write_bytes(b'different')
        with patch.object(k.urllib.request, 'urlopen', side_effect=lambda url, **kw: mock_response(url)):
            with self.assertRaisesRegex(SystemExit, 'refusing overwrite'):
                k.download(self.film, 'J1', 'mock-id', {}, [{'url': 'https://mock/video.mp4'}])
        self.assertEqual(original.read_bytes(), b'original')

    def test_cli_submit_only_requires_single_job_and_resume_has_no_spec(self):
        from unittest.mock import patch
        fixture = self.film / 'spec.json'
        fixture.write_text(json.dumps([{'job': 'a'}, {'job': 'b'}]))
        with patch.object(k.sys, 'argv', ['runner', '--spec', str(fixture), '--submit-only']), patch.object(k, 'submit') as submit:
            with self.assertRaises(SystemExit) as error:
                k.main()
            self.assertEqual(error.exception.code, 2)
            submit.assert_not_called()
        with patch.object(k.sys, 'argv', ['runner', '--film', str(self.film), '--resume', 'J1']), patch.object(k, 'resume', return_value={'status': 'RUNNING'}) as resume:
            self.assertEqual(k.main(), 0)
            resume.assert_called_once_with(self.film, 'J1')


if __name__ == '__main__':
    unittest.main()
