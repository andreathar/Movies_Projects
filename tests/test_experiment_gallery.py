"""Stable-ID joins protect historical gallery evidence from positional swaps."""
import copy
import importlib.util
from pathlib import Path
import unittest

SPEC=importlib.util.spec_from_file_location('experiment_gallery',Path(__file__).resolve().parents[1]/'scripts/experiment_gallery.py')
gallery=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(gallery)

class GalleryIdentityTests(unittest.TestCase):
    def setUp(self):
        self.resources=[{'asset_id':k,'path':k+'.mp4','sha256':k*64} for k in ['a','b']]
        self.observations=[{'asset_id':k,'frames':40,'observed':k,'limits':'inherited'} for k in ['a','b']]
        self.analyses=[{'asset_id':k,'sourcePath':k+'.mp4','sourceSHA256':k*64,'decodedFrames':40} for k in ['b','a']]

    def test_reordered_analyses_join_by_asset_id(self):
        records=gallery.join_records(self.resources,self.observations,self.analyses)
        self.assertEqual([(r['asset_id'],r['analysis']['sourcePath']) for r in records],[('a','a.mp4'),('b','b.mp4')])
        self.assertEqual(records[0]['observation']['observed'],'a')

    def test_duplicate_ids_refused_in_each_input(self):
        for index in range(3):
            inputs=copy.deepcopy([self.resources,self.observations,self.analyses]);inputs[index].append(inputs[index][0])
            with self.subTest(index=index),self.assertRaisesRegex(ValueError,'Duplicate'):
                gallery.join_records(*inputs)

    def test_missing_analysis_or_resource_refused(self):
        with self.assertRaisesRegex(ValueError,'asset IDs differ'):
            gallery.join_records(self.resources,self.observations,self.analyses[:1])
        with self.assertRaisesRegex(ValueError,'Missing resource'):
            gallery.join_records(self.resources[:1],self.observations,self.analyses)

    def test_matching_filename_does_not_override_hash_or_path_evidence(self):
        for field,value in [('sourceSHA256','wrong'),('sourcePath','other.mp4')]:
            analyses=copy.deepcopy(self.analyses);analyses[0][field]=value
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'identity mismatch'):
                gallery.join_records(self.resources,self.observations,analyses)

    def test_frame_evidence_mismatch_refused(self):
        self.analyses[0]['decodedFrames']=41
        with self.assertRaisesRegex(ValueError,'Frame count mismatch'):
            gallery.join_records(self.resources,self.observations,self.analyses)

    def test_html_uses_one_identity_for_video_audio_and_sheets(self):
        data={'costumeReferences':[],'videos':[{'asset_id':'a','video':{'path':'media/a.mp4','sha256':'a'*64},'observation':{'observed':'historical','limits':'no approval'},'audio':{'path':'review/a/audio.wav'},'asr':None,'sheets':[{'path':'review/a/frames.jpg','firstFrame':0,'lastFrame':39}]}]}
        rendered=gallery.render_index(data,'gallery/v3').decode()
        for path in ['../../media/a.mp4','../../review/a/audio.wav','../../review/a/frames.jpg']:
            self.assertIn(path,rendered)
        self.assertIn('data-asset-id="a"',rendered)
        self.assertIn('no approval',rendered)

if __name__=='__main__':unittest.main()
