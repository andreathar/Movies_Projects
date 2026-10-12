"""Synthetic documentary invariants. No generation, uploads, audio or image inspection."""
import copy
import importlib.util
from pathlib import Path
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('coherence_test', ROOT/'scripts/production_plan.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class CinematicCoherenceTests(unittest.TestCase):
    def setUp(self):
        self.refs = {'R': {'id': 'R', 'path': 'film/reference.png', 'sha256': 'a'*64,
                           'role': 'composition', 'provenance': 'synthetic_variant'}}
        self.shot = {'id': 'S', 'proposedGenerationSeconds': 5, 'referenceIds': ['R'],
                     'camera': 'Locked camera.', 'coherence': {}}
        self.job = {'job': 'S', 'args': {'duration': '5', 'enable_audio': False},
                    'prompt': 'One continuous five-second take. No speaking.'}
        self.mapping = {'first_image': 'film/reference.png'}

    def lint(self):
        return p.cinematic_lint(self.shot, self.refs, self.job, self.mapping)

    def codes(self, level=None):
        return {i['code'] for i in self.lint() if level is None or i['level'] == level}

    def segments(self):
        return [{'startSeconds': 0, 'endSeconds': 2, 'camera': 'locked'},
                {'startSeconds': 2, 'endSeconds': 5, 'camera': 'moving'}]

    def binding(self):
        self.shot['coherence']['referenceBindings'] = [
            {'slot': 'first_image', 'referenceId': 'R', 'role': 'composition'}]

    def override(self, code):
        self.shot['coherence']['overrides'] = [{'code': code, 'reason': 'Synthetic temporal exception.',
            'reviewer': 'Fixture reviewer, not a director approval',
            'subjectSha256': p.coherence_hash(self.shot, self.refs, self.job)}]

    def test_locked_vs_moving_is_warning_never_error(self):
        self.job['prompt'] += ' The camera orbits around the subject.'
        self.assertIn('CAMERA_MIXED', self.codes('WARN'))
        self.assertEqual(self.codes('ERROR'), set())

    def test_explicit_temporal_camera_segments_are_allowed(self):
        self.job['prompt'] = 'Locked camera for two seconds, then camera moves slowly.'
        self.shot['coherence']['segments'] = self.segments()
        self.assertIn('CAMERA_SEGMENTED', self.codes('INFO'))
        self.assertNotIn('CAMERA_MIXED', self.codes())
        self.assertEqual(self.codes('ERROR'), set())

    def test_negation_false_positive_remains_acknowledgeable_warning(self):
        self.job['prompt'] = 'Locked camera. Do not use a push-in.'
        self.override('CAMERA_MIXED')
        item = next(i for i in self.lint() if i['code'] == 'CAMERA_MIXED')
        self.assertEqual(item['level'], 'WARN')
        self.assertTrue(item['acknowledged'])
        self.assertEqual(self.codes('ERROR'), set())

    def test_subject_movement_does_not_become_camera_motion(self):
        self.job['prompt'] += ' The man leans forward after two seconds.'
        self.assertNotIn('CAMERA_MIXED', self.codes())
        self.assertNotIn('PROMPT_DURATION', self.codes())

    def test_invalid_partitions_are_errors_not_suppressed_camera_warnings(self):
        self.job['prompt'] += ' The camera tilts up.'
        for start, end in [(1, 5), (3, 5), (2, 6), (2, 4), (True, 5), (2, float('nan'))]:
            with self.subTest(start=start, end=end):
                segments = self.segments(); segments[1].update(startSeconds=start, endSeconds=end)
                self.shot['coherence']['segments'] = segments
                self.assertTrue(self.codes('ERROR') & {'SEGMENT_INTERVAL', 'SEGMENTS_TOTAL'})
                self.assertIn('CAMERA_MIXED', self.codes('WARN'))

    def test_nonfinite_negative_and_bool_durations_rejected(self):
        for value in [True, 0, -1, float('nan'), 'Infinity', 'five']:
            with self.subTest(value=value):
                self.job['args']['duration'] = value
                self.assertIn('DURATION_INVALID', self.codes('ERROR'))

    def test_structured_duration_mismatch_is_error_text_is_warning(self):
        self.job['prompt'] = 'During this three-second shot, listen.'
        self.assertIn('PROMPT_DURATION', self.codes('WARN'))
        self.assertNotIn('DURATION_REQUEST', self.codes())
        self.job['args']['duration'] = '10'
        self.assertIn('DURATION_REQUEST', self.codes('ERROR'))

    def test_duration_of_opening_segment_is_not_treated_as_total_fact(self):
        self.job['prompt'] = 'A three-second shot within the sequence, then two seconds of black.'
        self.assertIn('PROMPT_DURATION', self.codes('WARN'))
        self.assertEqual(self.codes('ERROR'), set())

    def test_silent_intent_checks_native_audio_original_sound_and_external_input(self):
        self.shot['coherence']['audioIntent'] = 'silent'
        for argument in ('enable_audio', 'enable-audio', 'keepOriginalSound'):
            with self.subTest(argument=argument):
                self.job['args'] = {'duration': 5, argument: 'true'}
                self.assertIn('AUDIO_CONTRADICTION', self.codes('ERROR'))
        self.job['args'] = {'duration': 5, 'enable_audio': False}
        self.mapping['audio'] = 'film/guide.wav'
        self.assertIn('AUDIO_CONTRADICTION', self.codes('ERROR'))

    def test_unavailable_audio_control_is_unknown_not_silent(self):
        self.shot['coherence']['audioIntent'] = 'silent'
        self.job['args'].pop('enable_audio')
        self.assertIn('AUDIO_CONTROL_UNKNOWN', self.codes('WARN'))
        self.assertEqual(self.codes('ERROR'), set())

    def test_no_speech_is_not_a_silent_soundtrack_contract(self):
        self.job['args']['enable_audio'] = True
        self.assertNotIn('AUDIO_TEXT_ONLY', self.codes())
        self.assertNotIn('AUDIO_CONTRADICTION', self.codes())

    def test_native_external_and_post_dubbing_are_separate(self):
        self.shot['coherence']['audioIntent'] = 'native_guide'
        self.assertIn('AUDIO_CONTRADICTION', self.codes('ERROR'))
        self.shot['coherence']['audioIntent'] = 'external_audio'
        self.assertIn('AUDIO_INPUT_MISSING', self.codes('ERROR'))
        self.shot['coherence']['audioIntent'] = 'post_dub'
        self.assertEqual(self.codes('ERROR'), set())

    def test_binding_requires_reference_selected_and_slot_present(self):
        self.binding()
        binding = self.shot['coherence']['referenceBindings'][0]
        binding['referenceId'] = 'MISSING'
        self.assertIn('BINDING_REFERENCE', self.codes('ERROR'))
        binding['referenceId'] = 'R'; binding['slot'] = 'tail_image'
        self.assertIn('BINDING_SLOT', self.codes('ERROR'))

    def test_duplicate_binding_is_error_unknown_content_or_role_only_warns(self):
        self.binding()
        binding = self.shot['coherence']['referenceBindings'][0]
        binding['role'] = 'identity'
        self.mapping['first_image'] = 'https://example.invalid/reference.png'
        self.assertTrue({'REFERENCE_ROLE', 'IDENTITY_PROVENANCE', 'BINDING_CONTENT_UNVERIFIED'} <= self.codes('WARN'))
        self.assertEqual(self.codes('ERROR'), set())
        self.shot['coherence']['referenceBindings'].append(copy.deepcopy(binding))
        self.assertIn('BINDING_REFERENCE', self.codes('ERROR'))

    def test_missing_provenance_warns_invalid_hash_errors(self):
        self.refs['R'].pop('provenance')
        self.assertIn('PROVENANCE_UNKNOWN', self.codes('WARN'))
        self.refs['R']['sha256'] = 'rendered and completed'
        self.assertIn('REFERENCE_HASH', self.codes('ERROR'))

    def test_sampled_frames_do_not_prove_full_playback(self):
        self.shot['coherence']['inspection'] = {'method': 'sampled_frames', 'fullPlaybackCompleted': True}
        self.assertIn('INSPECTION_CONTRADICTION', self.codes('ERROR'))

    def test_visual_inspection_and_audio_audition_are_independent(self):
        self.shot['coherence']['inspection'] = {'method': 'all_frames', 'fullPlaybackCompleted': False,
            'fullFrameInspectionCompleted': True, 'audioAuditionCompleted': False, 'evidence': 'synthetic-review'}
        self.assertEqual(self.codes('ERROR'), set())
        self.shot['coherence']['inspection'].update(method='sampled_frames', fullFrameInspectionCompleted=False,
                                                    audioAuditionCompleted=True)
        self.assertEqual(self.codes('ERROR'), set())
        self.shot['coherence']['inspection']['audioAuditionCompleted'] = 'true'
        self.assertIn('INSPECTION_FLAG', self.codes('ERROR'))

    def test_overrides_keep_evidence_and_expire_after_input_or_reference_changes(self):
        self.job['prompt'] += ' The camera rotates around the subject.'
        self.override('CAMERA_MIXED')
        self.assertEqual(self.codes('ERROR'), set())
        original = copy.deepcopy((self.shot, self.refs, self.job))
        self.lint()
        self.assertEqual((self.shot, self.refs, self.job), original)
        self.refs['R']['sha256'] = 'b'*64
        self.assertIn('OVERRIDE_INVALID', self.codes('ERROR'))
        self.refs['R']['sha256'] = 'a'*64
        self.job['prompt'] += ' Changed.'
        self.assertIn('OVERRIDE_INVALID', self.codes('ERROR'))

    def test_override_cannot_discard_deterministic_error_or_use_empty_justification(self):
        self.job['args']['duration'] = 10
        self.override('DURATION_REQUEST')
        self.assertTrue({'DURATION_REQUEST', 'OVERRIDE_INVALID'} <= self.codes('ERROR'))
        self.override('CAMERA_MIXED')
        self.shot['coherence']['overrides'][0]['reason'] = ' '
        self.assertIn('OVERRIDE_INVALID', self.codes('ERROR'))

    def test_empty_malformed_optional_metadata_reports_errors(self):
        for meta in [None, {'segments': []}, {'audioIntent': []}, {'referenceBindings': 'bad'},
                     {'inspection': {'method': 'invented'}}, {'inspection': {'method': []}},
                     {'overrides': 'bad'}]:
            with self.subTest(meta=meta):
                self.shot['coherence'] = meta
                self.assertTrue(self.codes('ERROR'))

    def test_existing_plan_reports_without_network_media_or_promotion(self):
        _, _, plan = p.plan_source(ROOT)
        before = copy.deepcopy(plan)
        with mock.patch('subprocess.run', side_effect=AssertionError('No external commands')):
            result = p.coherence_report(ROOT)
        self.assertEqual(result['errors'], [])
        self.assertFalse(result['mediaInspected'])
        self.assertFalse(result['creativeAcceptanceGranted'])
        self.assertFalse(result['paidReleaseGranted'])
        self.assertEqual(p.plan_source(ROOT)[2], before)
        self.assertIn('INPUT_ROLE_UNDOCUMENTED', {i['code'] for i in result['items']})

    def test_unknown_shot_does_not_silently_check_another(self):
        with self.assertRaises(ValueError):
            p.coherence_report(ROOT, 'NOT-A-SHOT')

    def test_completed_receipt_cannot_replace_approval_evidence(self):
        project, path, plan = p.plan_source(ROOT)
        plan = copy.deepcopy(plan)
        shot = next(s for s in plan['shots'] if s['id'] == 'G-P03')
        shot['providerStatus'] = 'COMPLETED'
        shot['states']['directorApproval'] = 'approved'
        with mock.patch.object(p, 'plan_source', return_value=(project, path, plan)):
            result = p.coherence_report(ROOT, 'G-P03')
        self.assertIn('STATE', {i['code'] for i in result['errors']})
        self.assertFalse(result['creativeAcceptanceGranted'])
        self.assertFalse(result['paidReleaseGranted'])


if __name__ == '__main__':
    unittest.main()
