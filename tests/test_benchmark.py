import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.benchmark import EvidenceError, inspect_run, percentile


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.manifest = {
            'schema_version': 1, 'run_id': 'unit-fixture', 'protocol_revision': 'v2.1',
            'operator': 'test', 'species': 'cat', 'scene_content': 'animal_presence', 'device': 'fixture', 'os': 'fixture',
            'build': 'fixture', 'asset_digest': 'fixture', 'room': 'fixture', 'lighting': 'fixture',
            'warmup_policy': 'fixture', 'evidence_kind': 'physical_device',
            'timing_method': 'validated_present_intervals', 'timing_validation_reference': 'fixture',
            'touch_validation_reference': 'fixture', 'completed': True,
            'offline_verified': True, 'network_trace_reviewed': True,
            'chargeable_inference_calls': 0, 'crashes': 0, 'interruptions': 0, 'thermal_warnings': 0,
        }
        self.save_manifest()
        self.frames(range(0, 600001, 20))
        self.touches()

    def save_manifest(self):
        (self.path / 'manifest.json').write_text(json.dumps(self.manifest))

    def frames(self, times, thermal='nominal'):
        with (self.path / 'frames.csv').open('w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['frame_index', 'elapsed_ms', 'memory_mb', 'battery_level', 'thermal_state'])
            w.writerows((i, t, 100, 0.8, thermal) for i, t in enumerate(times))

    def touches(self, latency=50, uncertainty=1):
        with (self.path / 'touches.csv').open('w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['event_id', 'input_ms', 'visible_ms', 'uncertainty_ms'])
            w.writerows((i, i * 100, i * 100 + latency, uncertainty) for i in range(100))

    def test_numerical_pass_is_never_presence_gate_pass(self):
        report = inspect_run(self.path)
        self.assertEqual(report['status'], 'PASS')
        self.assertEqual(report['presence_gate'], 'NOT RUN')
        self.assertEqual(report['metrics']['frame_p95_ms'], 20)
        self.assertEqual(len(report['metrics']['windows']), 10)
        self.assertEqual(report['metrics']['windows'][-1]['fps'], 50)
        self.assertEqual(len(report['evidence_sha256']), 3)

    def test_synthetic_and_editor_cannot_pass(self):
        for kind in ('synthetic', 'editor', 'unverified_player'):
            self.manifest['evidence_kind'] = kind
            self.save_manifest()
            self.assertEqual(inspect_run(self.path)['status'], 'PARTIAL')

    def test_instrumentation_scene_cannot_pass(self):
        self.manifest['scene_content'] = 'instrumentation_only'
        self.save_manifest()
        self.assertEqual(inspect_run(self.path)['status'], 'PARTIAL')

    def test_update_proxy_cannot_pass(self):
        self.manifest['timing_method'] = 'unity_update_proxy'
        self.save_manifest()
        self.assertEqual(inspect_run(self.path)['status'], 'PARTIAL')

    def test_short_run_cannot_pass(self):
        self.frames(range(0, 60000, 20))
        self.assertEqual(inspect_run(self.path)['status'], 'PARTIAL')

    def test_long_stall_cannot_hide_behind_good_percentile(self):
        self.frames(list(range(0, 300001, 20)) + list(range(360000, 600001, 20)))
        report = inspect_run(self.path)
        self.assertEqual(report['metrics']['frame_p95_ms'], 20)
        self.assertEqual(report['status'], 'FAIL')
        self.assertTrue(any('minute 6' in f for f in report['failures']))

    def test_slow_frames_fail(self):
        self.frames(range(0, 600001, 40))
        self.assertEqual(inspect_run(self.path)['status'], 'FAIL')

    def test_latency_strict_boundary_and_uncertainty(self):
        self.touches(99, 1)
        self.assertEqual(inspect_run(self.path)['status'], 'FAIL')
        self.touches(98, 1)
        self.assertEqual(inspect_run(self.path)['status'], 'PASS')

    def test_unknown_and_dangerous_thermals(self):
        self.frames(range(0, 600001, 20), 'unknown')
        self.assertEqual(inspect_run(self.path)['status'], 'PARTIAL')
        self.frames(range(0, 600001, 20), 'critical')
        self.assertEqual(inspect_run(self.path)['status'], 'FAIL')

    def test_nonfinite_and_nonmonotonic_samples_rejected(self):
        for times in ([0, 20, float('nan')], [0, 20, float('inf')], [0, 20, 19], [0, 20, 20]):
            self.frames(times)
            with self.assertRaises(EvidenceError):
                inspect_run(self.path)

    def test_missing_frames_rejected(self):
        p = self.path / 'frames.csv'
        p.write_text(p.read_text().replace('1,20,', '2,20,', 1))
        with self.assertRaises(EvidenceError):
            inspect_run(self.path)

    def test_missing_touches_remains_partial(self):
        (self.path / 'touches.csv').unlink()
        self.assertEqual(inspect_run(self.path)['status'], 'PARTIAL')

    def test_missing_or_nonzero_inference_count(self):
        self.manifest['chargeable_inference_calls'] = None
        self.save_manifest()
        self.assertEqual(inspect_run(self.path)['status'], 'PARTIAL')
        self.manifest['chargeable_inference_calls'] = 1
        self.save_manifest()
        self.assertEqual(inspect_run(self.path)['status'], 'FAIL')

    def test_aborted_run_is_incomplete(self):
        self.manifest['completed'] = False
        self.save_manifest()
        self.assertEqual(inspect_run(self.path)['status'], 'PARTIAL')

    def test_duplicate_touch_and_out_of_range_touch_rejected(self):
        p = self.path / 'touches.csv'
        p.write_text(p.read_text() + '0,0,50,1\n')
        with self.assertRaises(EvidenceError):
            inspect_run(self.path)
        p.write_text('event_id,input_ms,visible_ms,uncertainty_ms\nx,600000,600050,1\n')
        with self.assertRaises(EvidenceError):
            inspect_run(self.path)

    def test_cli_refuses_to_overwrite_evidence(self):
        result = subprocess.run([sys.executable, 'tools/benchmark.py', str(self.path),
                                 '--output', str(self.path / 'manifest.json')], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads((self.path / 'manifest.json').read_text()), self.manifest)

    def test_nearest_rank(self):
        self.assertEqual(percentile(list(range(1, 101))), 95)
        self.assertIsNone(percentile([]))


if __name__ == '__main__':
    unittest.main()
