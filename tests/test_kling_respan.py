"""Kling/Respan accounting and failure boundaries; synthetic providers only."""
import csv
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('traced_runner', ROOT / 'scripts/kling_batch.py')
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)
t = k.tracing


class FakeSDK:
    def __init__(self, fault=None):
        self.fault = fault
        self.spans = []
        self.stack = []
        self.flushes = 0

    def decorator(self, kind):
        def decorate(name):
            def wrap(fn):
                def call(*args, **kwargs):
                    if self.fault == kind + '_before':
                        raise RuntimeError('PRIVATE SDK MESSAGE')
                    span = {'kind': kind, 'name': name, 'attrs': {}, 'args': args, 'kwargs': kwargs}
                    self.spans.append(span)
                    self.stack.append(span)
                    try:
                        span['return'] = fn(*args, **kwargs)
                        if self.fault == kind + '_after':
                            raise RuntimeError('PRIVATE SDK MESSAGE')
                        return span['return']
                    finally:
                        self.stack.pop()
                return call
            return wrap
        return decorate

    def set_attribute(self, key, value):
        if self.fault == 'attribute':
            raise RuntimeError('PRIVATE SDK MESSAGE')
        self.stack[-1]['attrs'][key] = value

    def flush(self):
        self.flushes += 1
        if self.fault == 'flush':
            raise RuntimeError('PRIVATE SDK MESSAGE')

    def load(self):
        if self.fault == 'init':
            raise ImportError('PRIVATE SDK MESSAGE')
        return self, self.decorator('workflow'), self.decorator('task'), lambda: self


class TracingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir='/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.film = Path(self.tmp.name) / 'episode'
        self.film.mkdir()
        self.env = patch.dict(os.environ, {'RESPAN_API_KEY': 'fake-key', 'MOVIES_KLING_RESPAN': '1',
            'RESPAN_WORKFLOW_NAME': 'S04-galileo',
            'RESPAN_METADATA': json.dumps({'lane':'producer','role':'producer','scene':'S04-galileo','task':'T13',
                                           'prompt':'PRIVATE PROMPT', 'image':'PRIVATE IMAGE','api_key':'PRIVATE KEY'})})
        self.env.start(); self.addCleanup(self.env.stop)
        self.sdk = FakeSDK()
        self.loader = patch.object(t, 'load_sdk', side_effect=lambda: self.sdk.load()).start()
        self.addCleanup(patch.stopall)
        self.envelope = {'quote':{'credits':30, 'unit':'Kling credits','basis':'provider_quote',
                                  'evidence':{'path':'PRIVATE EVIDENCE'}},
                         'schemaSha256':'a'*64, 'maxCredits':40}
        patch.object(k.release,'authorize',return_value=self.envelope).start()
        patch.object(k,'preflight',return_value={'schemaSha256':'a'*64}).start()
        patch.object(k,'account',side_effect=[100,20]).start()
        self.provider = patch.object(k,'run',return_value={'ok':True,'body':{'generationId':'provider-id',
                     'creditsConsumed':24},'private':'PRIVATE RESPONSE'}).start()

    def submit(self, **kw):
        return k.submit(self.film,'J1','text_to_video','mock-model','PRIVATE PROMPT',{},[],
                        'AUTH-ID','PRIVATE NOTE',submit_only=True,**kw)

    def attrs(self):
        return next(s['attrs'] for s in self.sdk.spans if s['kind']=='task')

    def test_one_workflow_one_task_quotes_and_charge_separate(self):
        result=self.submit()
        self.assertEqual(result['creditsConsumed'],24)
        self.assertEqual(result['creditsDelta'],80)
        self.assertEqual([s['kind'] for s in self.sdk.spans],['workflow','task'])
        attrs=self.attrs()
        for name,value in {'credit_quote':30,'credit_charge':24,'cost_unit':'Kling credits',
            'cost_provider':'Kling','generation_id':'provider-id','scene':'S04-galileo','task':'T13'}.items():
            self.assertEqual(attrs['respan.metadata.'+name],value)
        self.assertNotIn('respan.metadata.credit_charge',self.sdk.spans[0]['attrs'])
        self.assertFalse(any('token' in key or 'cost_usd' in key for key in attrs))
        intent=json.loads((self.film/'07_generations/responses/J1.intent.json').read_text())
        self.assertEqual(intent['costTrace']['cost_event_id'],attrs['respan.metadata.cost_event_id'])
        self.provider.assert_called_once()

    def test_raw_data_never_crosses_decorators(self):
        self.submit()
        self.assertNotIn('PRIVATE',json.dumps(self.sdk.spans))
        self.assertNotIn('fake-key',json.dumps(self.sdk.spans))
        for s in self.sdk.spans:
            self.assertEqual(s['args'],()); self.assertEqual(s['kwargs'],{}); self.assertIsNone(s['return'])

    def test_instrumentation_failures_before_after_or_flush_never_resubmit(self):
        for fault in ('init','workflow_before','task_before','task_after','workflow_after','attribute','flush'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory(dir='/tmp') as d:
                self.film=Path(d); self.sdk=FakeSDK(fault)
                with patch.object(k,'account',side_effect=[100,20]), patch('sys.stderr',new_callable=io.StringIO) as err:
                    result=self.submit()
                self.assertEqual(result['generationId'],'provider-id')
                self.assertNotIn('PRIVATE',err.getvalue())
                self.assertEqual(len(list(csv.reader((self.film/'credit-ledger.csv').read_text().splitlines()))),1)
        self.assertEqual(self.provider.call_count,7)

    def test_disabled_and_missing_credentials_do_not_import_sdk(self):
        for env in ({'MOVIES_KLING_RESPAN':'0'}, {'RESPAN_API_KEY':''}):
            with self.subTest(env=env), patch.dict(os.environ,env):
                op=Mock(return_value={'status':'SUBMISSION_UNKNOWN'})
                self.assertEqual(t.execute({'workflow':'test'},{},op),op.return_value)
                op.assert_called_once()
        self.loader.assert_not_called()

    def test_unknown_submission_and_retries_never_count_quote_as_charge(self):
        self.provider.side_effect=TimeoutError('PRIVATE URL https://example.invalid?token=secret')
        result=self.submit()
        self.assertEqual(result['status'],'SUBMISSION_UNKNOWN')
        self.assertNotIn('respan.metadata.credit_charge',self.attrs())
        self.assertEqual(self.attrs()['respan.metadata.credit_charge_basis'],'unknown')
        self.assertNotIn('PRIVATE',json.dumps(self.sdk.spans))
        for _ in range(2):
            with self.assertRaises(SystemExit):self.submit()
            self.assertEqual(k.resume(self.film,'J1')['status'],'SUBMISSION_UNKNOWN')
        self.provider.assert_called_once(); self.assertEqual(len(self.sdk.spans),2)

    def test_reported_failed_submission_charge_is_still_a_charge(self):
        self.provider.return_value={'ok':False,'body':{'creditsConsumed':4}}
        self.assertEqual(self.submit()['status'],'SUBMISSION_UNKNOWN')
        self.assertEqual(self.attrs()['respan.metadata.credit_charge'],4)

    def test_zero_is_known_and_invalid_charges_are_unknown(self):
        for charge in (0, None, True, -2, float('nan'),float('inf'),'bad'):
            with self.subTest(charge=charge),tempfile.TemporaryDirectory(dir='/tmp') as d:
                self.film=Path(d);self.sdk=FakeSDK()
                self.provider.return_value={'body':{'generationId':'provider-id','creditsConsumed':charge}}
                with patch.object(k,'account',side_effect=[100,20]):self.submit()
                if charge == 0 and not isinstance(charge,bool):self.assertEqual(self.attrs()['respan.metadata.credit_charge'],0)
                else:self.assertNotIn('respan.metadata.credit_charge',self.attrs())

    def test_polling_and_resume_do_not_emit_charge_spans(self):
        self.submit()
        self.provider.return_value={'ok':True,'body':{'generationId':'provider-id','status':'FAILED','creditsConsumed':999}}
        for _ in range(3):self.assertEqual(k.resume(self.film,'J1')['status'],'FAILED')
        self.assertEqual(len(self.sdk.spans),2); self.assertEqual(self.sdk.flushes,1)
        self.assertEqual(self.attrs()['respan.metadata.credit_charge'],24)
        self.assertEqual(len((self.film/'credit-ledger.csv').read_text().splitlines()),1)

    def test_local_persistence_error_is_not_masked_or_exported(self):
        original=k.durable
        def fail(path,text):
            if path.name=='credit-ledger.csv':raise OSError('PRIVATE LOCAL ERROR')
            original(path,text)
        with patch.object(k,'durable',side_effect=fail), self.assertRaisesRegex(OSError,'PRIVATE LOCAL ERROR'):
            self.submit()
        self.provider.assert_called_once()
        self.assertNotIn('PRIVATE',json.dumps(self.sdk.spans))
        self.assertEqual(self.attrs()['respan.metadata.submission_state'],'local_error')
        with self.assertRaises(SystemExit):self.submit()
        self.provider.assert_called_once()

    def test_preflight_and_balance_blocks_create_no_traces(self):
        with patch.object(k,'preflight',side_effect=SystemExit('blocked')):
            with self.assertRaises(SystemExit):self.submit()
        self.loader.assert_not_called(); self.provider.assert_not_called()

    def test_provider_cancellation_is_reraised_without_sensitive_capture(self):
        exc=KeyboardInterrupt('PRIVATE INTERRUPT')
        self.provider.side_effect=exc
        with self.assertRaises(KeyboardInterrupt) as caught:self.submit()
        self.assertIs(caught.exception,exc)
        self.assertNotIn('PRIVATE',json.dumps(self.sdk.spans));self.provider.assert_called_once()

    def test_cancellation_during_tracing_setup_does_not_start_submission(self):
        with patch.object(t,'load_sdk',side_effect=KeyboardInterrupt), self.assertRaises(KeyboardInterrupt):
            self.submit()
        self.provider.assert_not_called()

    def test_metadata_rejects_arbitrary_values_and_scene_disagreement(self):
        with patch.dict(os.environ,{'RESPAN_METADATA':json.dumps({'scene':'different','task':'https://secret', 'role':{},'lane':'two words'}), 'RESPAN_WORKFLOW_NAME':'S04-galileo'}):
            data=t.context(self.film,'J1','a'*64)
        self.assertEqual(data['scene'],'S04-galileo')
        for key in ('task','role','lane'):self.assertNotIn(key,data)
        for raw in ('[]','null','broken'):
            with patch.dict(os.environ,{'RESPAN_METADATA':raw,'RESPAN_WORKFLOW_NAME':''}):
                self.assertNotIn('scene',t.context(self.film,'J1','a'*64))

    def test_estimate_and_foreign_unit_not_exported_as_quote(self):
        for quote in ({'basis':'estimate','unit':'Kling credits','credits':30}, {'basis':'provider_quote','unit':'USD','credits':3}):
            attrs=t.cost_attributes({'quote':quote},{'status':'SUBMITTED','creditsConsumed':0,'chargeBasis':'provider_reported'})
            self.assertNotIn('credit_quote',attrs);self.assertEqual(attrs['credit_charge'],0)

    def test_duplicate_callback_guard(self):
        original=self.sdk.decorator
        def faulty(kind):
            if kind!='task':return original(kind)
            def dec(name):
                def wrap(fn):
                    def call():fn();fn()
                    return call
                return wrap
            return dec
        self.sdk.decorator=faulty
        self.submit();self.provider.assert_called_once()


class InstalledSDKTests(unittest.TestCase):
    def test_installed_sdk_with_memory_exporter_only(self):
        # Fresh process avoids Respan/OTel singleton interference with other tests.
        code = r'''
import importlib.util,json,socket,sys
from pathlib import Path
from unittest.mock import patch
def no_network(*a,**k):raise AssertionError('Network forbidden in SDK fixture')
with patch.object(socket.socket,'connect',no_network),patch.object(socket,'getaddrinfo',no_network):
 from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
 import respan_tracing.exporters
 memory=InMemorySpanExporter()
 with patch.object(respan_tracing.exporters,'RespanSpanExporter',return_value=memory):
  spec=importlib.util.spec_from_file_location('adapter',sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  tags=m.context(Path('episode'),'J1','a'*64)
  result={'status':'SUBMITTED','generationId':'job-123','creditsConsumed':24,'chargeBasis':'provider_reported','error':'PRIVATE OUTPUT'}
  assert m.execute(tags,{'quote':{'credits':30,'basis':'provider_quote','unit':'Kling credits'}},lambda:result) is result
  spans=memory.get_finished_spans();assert len(spans)==2,len(spans)
  task,workflow=spans
  assert task.parent.span_id==workflow.context.span_id
  assert task.attributes['respan.metadata.credit_charge']==24
  assert 'respan.metadata.credit_charge' not in workflow.attributes
  assert task.attributes['traceloop.workflow.name']=='S04-galileo'
  assert 'PRIVATE' not in json.dumps([dict(s.attributes) for s in spans])
  assert task.attributes.get('traceloop.entity.output') in (None,'null')
  print('Installed SDK: workflow + child task; in-memory exporter; no socket access')
'''
        env={'PATH':os.environ.get('PATH',''),'PYTHONDONTWRITEBYTECODE':'1','RESPAN_API_KEY':'synthetic',
             'MOVIES_KLING_RESPAN':'1','RESPAN_WORKFLOW_NAME':'S04-galileo'}
        proc=subprocess.run([os.sys.executable,'-B','-c',code,str(ROOT/'scripts/kling_respan.py')],env=env,
                            text=True,capture_output=True,timeout=30)
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)


if __name__=='__main__':unittest.main()
