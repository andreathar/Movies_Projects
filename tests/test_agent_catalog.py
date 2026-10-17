import importlib.util
import json
import tempfile
import tomllib
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('agent_catalog',Path(__file__).parents[1]/'scripts/agent_catalog.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.write('AGENTS.md','contract')
        self.write('agents/CONTRACT.md','Shared mode/path/evidence contract.')
        self.write('shared/kling-capabilities.json',{'schemaVersion':1,'generationTested':False})
        self.roles=[{'id':r,'name':r,'brief':f'agents/{r}.md','skills':['sample']} for r in m.REVIEWERS]
        for r in self.roles:self.write(r['brief'],self.brief())
        self.write('agents/registry.json',{'roles':self.roles})
        self.skill={'name':'sample','path':'skills/sample','source':'project_canonical','type':'project_local'}
        self.write('skills/registry.json',{'skills':[self.skill]})
        self.write('skills/sample/SKILL.md','---\nname: sample\ndescription: Read evidence.\n---\n# Sample')
    def brief(self, mission='Inspect the source.'):
        return ('# Review\n\n## Mission\n'+mission+'\n\n## Authority\nRead only.\n'
                '\n## Reads\nAssigned source reports.\n\n## Review\nCheck evidence; mark missing checks not_run.\n'
                '\n## May not\nInvent evidence or approve production.\n')
    def write(self,path,data):
        p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data) if isinstance(data,dict) else data)
    def test_idempotent_and_prepared_only(self):
        m.sync(self.root);before=m.render(self.root);self.assertEqual(m.sync(self.root)['changed'],[]);m.sync(self.root,True)
        self.assertFalse((self.root/'.claude').exists());self.assertFalse((self.root/'.codex').exists())
        for path,raw in before.items():
            if path.endswith('.toml'):self.assertEqual(set(tomllib.loads(raw.decode())),{'name','description','developer_instructions'})
    def test_duplicate_roles_and_skills_rejected(self):
        self.write('agents/registry.json',{'roles':self.roles+[self.roles[0]]})
        with self.assertRaises(ValueError):m.render(self.root)
        self.write('agents/registry.json',{'roles':self.roles});self.write('skills/registry.json',{'skills':[self.skill,self.skill]})
        with self.assertRaises(ValueError):m.render(self.root)
    def test_unknown_skill_and_missing_brief_rejected(self):
        self.roles[0]['skills']=['missing'];self.write('agents/registry.json',{'roles':self.roles})
        with self.assertRaises(ValueError):m.render(self.root)
        self.roles[0]['skills']=['sample'];self.write('agents/registry.json',{'roles':self.roles});(self.root/self.roles[0]['brief']).unlink()
        with self.assertRaises(FileNotFoundError):m.render(self.root)
    def test_broken_link_and_escape_rejected(self):
        skill=self.root/'skills/sample/SKILL.md';skill.unlink();skill.symlink_to(self.root/'missing')
        with self.assertRaises(FileNotFoundError):m.render(self.root)
        self.roles[0]['brief']='../outside';self.write('agents/registry.json',{'roles':self.roles})
        self.write('skills/sample/SKILL.md','description: restored')
        with self.assertRaises(ValueError):m.render(self.root)
    def test_drift_check_never_writes(self):
        m.sync(self.root);dest=self.root/'agents/generated/claude/movies-qc.md';dest.write_text('manual edit')
        with self.assertRaisesRegex(ValueError,'drift'):m.sync(self.root,True)
        self.assertEqual(dest.read_text(),'manual edit')
    def test_authority_not_promoted(self):
        self.roles[0]['paidSubmissionAuthority']=True;self.write('agents/registry.json',{'roles':self.roles})
        with self.assertRaisesRegex(ValueError,'authority'):m.render(self.root)
    def test_brief_change_updates_metadata_and_adapters(self):
        old=m.render(self.root);self.write('agents/qc.md',self.brief('Inspect the exact export.'))
        new=m.render(self.root);self.assertNotEqual(old['agents/generated/catalog.json'],new['agents/generated/catalog.json']);self.assertNotEqual(old['agents/generated/codex/movies-qc.toml'],new['agents/generated/codex/movies-qc.toml'])

    def test_portuguese_mission_is_derived(self):
        self.write('agents/qc.md',self.brief('Verificar o arquivo.').replace('## Mission','## Missão'))
        catalog=json.loads(m.render(self.root)['agents/generated/catalog.json'])
        self.assertEqual(next(r for r in catalog['roles'] if r['id']=='qc')['summary'],'Verificar o arquivo.')

    def test_editing_and_full_media_completion_not_inherited(self):
        self.write('agents/qc.md',self.brief()+
                   '\n## Writes\nWRITE_SENTINEL reports and handoffs.\n'
                   '\n## Definition of done\nDECODE_SENTINEL play both masters.\n')
        outputs=m.render(self.root)
        for path,raw in outputs.items():
            if path.endswith(('.md','.toml')):
                prompt=raw.decode()
                self.assertNotIn('WRITE_SENTINEL',prompt)
                self.assertNotIn('DECODE_SENTINEL',prompt)
                self.assertNotIn('## Writes',prompt)
                self.assertIn('not_run',prompt)
                self.assertIn('The parent packages the handoff',prompt)
                self.assertIn('cannot complete full-media QC',prompt)

    def test_unavailable_startup_and_hash_checks_use_attributed_parent_evidence(self):
        for path, raw in m.render(self.root).items():
            if path.endswith(('.md', '.toml')):
                prompt = raw.decode()
                self.assertIn('parent-supplied startup/status evidence and input hashes', prompt)
                self.assertIn('do not claim to have independently run or computed them', prompt)
                self.assertIn('unavailable mandatory startup checks not_run', prompt)
                self.assertNotIn('Complete workspace AGENTS.md startup;', prompt)

    def test_missing_or_duplicate_review_section_rejected_before_writes(self):
        for text in (self.brief().replace('## Review','## Other'),
                     self.brief()+'\n## Review\nRepeated.\n'):
            with self.subTest(text=text):
                self.write('agents/qc.md',text)
                with self.assertRaisesRegex(ValueError,'section'):
                    m.sync(self.root)
                self.assertFalse((self.root/'agents/generated').exists())

    def test_shared_contract_hash_is_tracked(self):
        old=m.render(self.root)
        self.write('agents/CONTRACT.md','Changed shared contract.')
        new=m.render(self.root)
        self.assertNotEqual(old['agents/generated/catalog.json'],new['agents/generated/catalog.json'])
        self.assertIn('agents/CONTRACT.md',[s['path'] for s in json.loads(new['agents/generated/catalog.json'])['sources']])

    def test_short_names_preserve_adapter_identity(self):
        self.roles[0]['name']='History';self.write('agents/registry.json',{'roles':self.roles})
        outputs=m.render(self.root)
        self.assertIn('agents/generated/claude/movies-historian.md',outputs)
        self.assertIn('agents/generated/codex/movies-historian.toml',outputs)

    def test_mission_required_and_bounded(self):
        for text in ('## Purpose\nInspect.\n','## Mission\n\n## Reads\nSource.\n'):
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError,'Mission'):
                    m.mission(text)
        self.assertEqual(m.mission('## Mission\nInspect.\n## Writes\nDo not include.\n'),'Inspect.')

    def test_real_storyboard_and_modes_remain_unambiguous(self):
        root=Path(__file__).parents[1]
        forbidden=r'(?i)\bapprove\b'
        self.assertRegex('Approve keyframes and an audio-first animatic.',forbidden)
        self.assertNotRegex(m.mission((root/'agents/storyboard.md').read_text()),forbidden)
        for role in ('historian','continuity','qc'):
            text=(root/f'agents/{role}.md').read_text()
            self.assertNotIn('## Writes',m.review_sections(text))
        self.assertIn('not_run',(root/'agents/CONTRACT.md').read_text())
        registry=json.loads((root/'agents/registry.json').read_text())
        self.assertFalse(registry['autostart'])
        self.assertTrue(all(not r['running'] for r in registry['roles']))
