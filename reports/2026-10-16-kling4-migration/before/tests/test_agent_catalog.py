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
        self.roles=[{'id':r,'name':r,'brief':f'agents/{r}.md','skills':['sample']} for r in m.REVIEWERS]
        for r in self.roles:self.write(r['brief'],'# Review\n\n## Mission\nInspect the source.\n\n## Authority\nRead only.\n')
        self.write('agents/registry.json',{'roles':self.roles})
        self.skill={'name':'sample','path':'skills/sample','source':'project_canonical','type':'project_local'}
        self.write('skills/registry.json',{'skills':[self.skill]})
        self.write('skills/sample/SKILL.md','---\nname: sample\ndescription: Read evidence.\n---\n# Sample')
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
        old=m.render(self.root);self.write('agents/qc.md','# QC\n## Mission\nInspect the exact export.\n')
        new=m.render(self.root);self.assertNotEqual(old['agents/generated/catalog.json'],new['agents/generated/catalog.json']);self.assertNotEqual(old['agents/generated/codex/movies-qc.toml'],new['agents/generated/codex/movies-qc.toml'])

    def test_portuguese_mission_is_derived(self):
        self.write('agents/qc.md','# QC\n## Missão\nVerificar o arquivo.\n')
        catalog=json.loads(m.render(self.root)['agents/generated/catalog.json'])
        self.assertEqual(next(r for r in catalog['roles'] if r['id']=='qc')['summary'],'Verificar o arquivo.')
