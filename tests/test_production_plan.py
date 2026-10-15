"""Offline plan invariants; metadata-only fixtures, no media cloning or generation."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('production_plan_test',ROOT/'scripts/production_plan.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)


class ProductionPlanTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir='/tmp');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        project,path,plan=p.plan_source(ROOT)
        self.path=path;self.plan=copy.deepcopy(plan)
        names=['workspace.json',path,project['manifest'],project['tasks'],project['root']+'/00_brief/approvals.json',p.SNAPSHOT,p.FAMILIES,'scripts/production_plan.py','scripts/kling_release.py','docs/kling-manual/tools/kling_preflight.py','docs/PRODUCTION_PLAN.md']+[s['path'] for s in plan['preservedSources']]+plan['deliverables']
        names += [item['approvalEvidence']['path'] for item in plan['references'] + plan['shots'] if item.get('approvalEvidence')]
        for name in dict.fromkeys(names):
            dest=self.root/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((ROOT/name).read_bytes())

    def save(self): (self.root/self.path).write_text(json.dumps(self.plan))

    def errors(self): self.save();return p.validate(self.root)['errors']

    def test_valid_metadata_and_templates_do_not_mutate_approvals(self):
        approval=self.root/'projects/andre-time-travel/00_brief/approvals.json';before=approval.read_bytes()
        self.assertEqual(self.errors(),[])
        self.assertEqual(approval.read_bytes(),before)
        for family in p.read(self.root,p.FAMILIES)['families']:
            request=p.template(self.root,family['id'])
            self.assertTrue(request['submissionBlocked']);self.assertIsNone(request['auth'])

    def test_english_line_is_read_from_canonical_csv(self):
        request=p.template(self.root,'F3','G-P04')
        self.assertIn('silencing a man does not settle a question.',request['prompt'])
        self.assertNotIn('{canonical_dialogue}',request['prompt'])
        self.assertEqual(request['args']['duration'],'11')

    def test_preserved_source_drift_is_error(self):
        script=self.root/'projects/andre-time-travel/01_script/script-en.md';script.write_text('changed')
        self.assertTrue(any('fonte preservada' in e for e in self.errors()))

    def test_dependency_cycles_and_missing_refs_fail(self):
        self.plan['shots'][0]['dependsOn']=['G-P04']
        self.assertTrue(any('cíclica' in e for e in self.errors()))

    def test_reaction_cannot_precede_cause(self):
        self.plan['pilot']['audio'][1]['startSeconds']=5
        self.assertTrue(any('reação antecede' in e for e in self.errors()))

    def test_speed_change_is_not_accepted_as_timing_fix(self):
        self.plan['pilot']['audio'][0]['rate']=1.3
        self.assertTrue(any('acelerado' in e for e in self.errors()))

    def test_incorporation_is_not_technical_check(self):
        self.plan['references'][0]['states']['incorporation']='incorporated'
        self.assertTrue(any('aprovação específica' in e for e in self.errors()))

    def test_approval_without_hash_evidence_fails(self):
        self.plan['shots'][0]['states']['directorApproval']='approved'
        self.assertTrue(any('aprovação sem evidência' in e for e in self.errors()))

    def test_shot_approval_is_bound_to_content_and_exact_selector(self):
        shot=self.plan['shots'][0]
        decision={'decision':'approved','reviewer':'Synthetic director fixture',
                  'scope':'Synthetic shot review; not real acceptance',
                  'artifact':{'selector':shot['id'],'sha256':p.review_hash(shot)}}
        evidence=self.root/'synthetic-decision.json'
        evidence.write_text(json.dumps(decision))
        shot['approvalEvidence']={'path':'synthetic-decision.json','sha256':p.sha(evidence)}
        shot['states']['directorApproval']='approved'
        self.assertEqual(self.errors(),[])
        shot['camera']='Changed camera after review'
        self.assertTrue(any('não corresponde' in e for e in self.errors()))
        decision['artifact']['sha256']=p.review_hash(shot)
        decision['artifact']['selector']='ANOTHER-SHOT'
        evidence.write_text(json.dumps(decision));shot['approvalEvidence']['sha256']=p.sha(evidence)
        self.assertTrue(any('selector' in e for e in self.errors()))

    def test_reference_review_evidence_tracks_approved_rejected_and_pending_exact_hash(self):
        ref = self.plan['references'][0]
        evidence = self.root / 'synthetic-image-decision.json'
        for state in ['approved', 'rejected', 'pending']:
            decision = {'decision': state, 'reviewer': 'Synthetic fixture only',
                        'scope': 'Disposable test, no real creative approval',
                        'artifact': {'path': ref['path'], 'sha256': ref['sha256']}}
            evidence.write_text(json.dumps(decision))
            ref['states']['directorApproval'] = state
            ref['approvalEvidence'] = {'path': evidence.name, 'sha256': p.sha(evidence)}
            self.assertEqual(self.errors(), [])
            decision['artifact']['sha256'] = '0' * 64
            evidence.write_text(json.dumps(decision))
            ref['approvalEvidence']['sha256'] = p.sha(evidence)
            self.assertTrue(any('não corresponde' in e for e in self.errors()))

    def test_wrong_encounters_or_voice_policy_fail(self):
        self.plan['encounters'].pop();self.plan['constraints']['finalVoicePolicy']='approved'
        self.assertEqual(len(self.errors()),2)

    def test_templates_cannot_invent_unsupported_turbo_audio(self):
        path=self.root/p.FAMILIES;families=json.loads(path.read_text());families['families'][2]['request']['model']='kling-video-v3_0_turbo';path.write_text(json.dumps(families))
        self.assertTrue(any('ARG_UNKNOWN' in e for e in self.errors()))

    def test_routes_come_from_snapshot_and_export_pins_sources(self):
        route=p.routes(self.root)
        snap=p.read(self.root,p.SNAPSHOT)
        self.assertEqual(len(route['routes']),sum(len(g['models']) for g in snap['body']['availableModels'].values()))
        exported=p.export(self.root)
        self.assertTrue(any(s['path']==self.path for s in exported['sourceVersions']))
        self.assertFalse(exported['costPolicy']['newPaidAuthorization'])

    def test_baseline_exports_without_approving_old_or_new_media(self):
        before=copy.deepcopy(self.plan)
        self.save()
        exported=p.export(self.root)
        self.assertEqual(exported['activeBaseline'],self.plan['activeBaseline'])
        self.assertEqual(self.plan,before)
        self.assertEqual([r['states'] for r in exported['references']], [r['states'] for r in before['references']])
        self.assertFalse(exported['activeBaseline']['paidGenerationAuthorized'])
        self.assertTrue(all(s['state'] in {'ready_local','blocked'} for s in exported['activeBaseline']['steps']))

    def test_baseline_rejects_cycles_missing_links_and_paid_claim(self):
        original=copy.deepcopy(self.plan['activeBaseline'])
        mutations=[lambda b:b['steps'][0].update(dependsOn=[b['steps'][0]['id']]),
                   lambda b:b.update(referenceIds=['MISSING']),
                   lambda b:b.update(referenceIds=['G-OLD-LISTEN']),
                   lambda b:b.update(paidGenerationAuthorized=True),
                   lambda b:b['steps'][0].update(taskIds=['MISSING'])]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                self.plan['activeBaseline']=copy.deepcopy(original);mutate(self.plan['activeBaseline'])
                self.assertTrue(self.errors())

    def test_legacy_plan_without_baseline_stays_readable(self):
        self.plan.pop('activeBaseline',None)
        self.assertEqual(self.errors(),[])
        self.assertNotIn('activeBaseline',p.export(self.root))


if __name__=='__main__': unittest.main()
