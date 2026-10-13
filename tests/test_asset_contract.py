"""Asset data contract: manifest hashes must map to the registry. No media is generated."""
import csv, importlib.util, json, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('asset_contract', ROOT/'scripts/asset_contract.py')
ac = importlib.util.module_from_spec(spec); spec.loader.exec_module(ac)


class AssetContractTests(unittest.TestCase):
    def fixture(self, registered):
        tmp = Path(tempfile.mkdtemp())
        (tmp/'a.png').write_bytes(b'png-a'); (tmp/'b.png').write_bytes(b'png-b')
        images = [{'name': n, 'path': f'{n}.png', 'sha256': ac.sha256(tmp/f'{n}.png')} for n in 'ab']
        (tmp/'manifest.json').write_text(json.dumps({'images': images}))
        with (tmp/'reg.csv').open('w', newline='') as f:
            w = csv.DictWriter(f, ac.HEADER); w.writeheader()
            for n in registered:
                w.writerow({'asset_id': n, 'kind': 'k', 'path_or_provider_id': f'{n}.png', 'path_base': 'film',
                            'source': 's', 'sha256': ac.sha256(tmp/f'{n}.png'), 'approved': 'false', 'notes': ''})
        return tmp

    def test_all_registered_passes(self):
        t = self.fixture('ab')
        self.assertTrue(ac.check(t/'manifest.json', t/'reg.csv', t)['ok'])

    def test_unregistered_hash_fails_and_gets_unapproved_proposal(self):
        t = self.fixture('a')
        r = ac.check(t/'manifest.json', t/'reg.csv', t)
        self.assertFalse(r['ok']); self.assertEqual([u['name'] for u in r['unregistered']], ['b'])
        row = ac.proposal_rows(r, t, t)[0]
        self.assertEqual((row['approved'], row['sha256']), ('false', r['unregistered'][0]['sha256']))

    def test_tampered_file_is_hash_mismatch_not_registered(self):
        t = self.fixture('ab'); (t/'a.png').write_bytes(b'tampered')
        r = ac.check(t/'manifest.json', t/'reg.csv', t)
        self.assertFalse(r['ok']); self.assertEqual(len(r['hash_mismatch']), 1)

    def test_real_detail_studies_manifest_hashes_match_files(self):
        r = ac.check()
        self.assertEqual((r['hash_mismatch'], r['missing_file']), ([], []))


if __name__ == '__main__':
    unittest.main()
