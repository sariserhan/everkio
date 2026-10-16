import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.benchmark import EvidenceError, inspect_run
from tools.benchmark_series import inspect_series


class SeriesTests(unittest.TestCase):
    # All fixtures are synthetic; their declarations are parser test inputs only.
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.runs = []
        for i in range(3):
            folder = Path(self.tmp.name) / str(i)
            folder.mkdir()
            self.runs.append(folder)
            manifest = {
                'schema_version': 1, 'run_id': f'fixture-{i}', 'species': 'cat',
                'protocol_revision': 'fixture-v1', 'operator': 'fixture',
                'device': 'fixture-device', 'os': 'fixture-os', 'build': 'fixture-build',
                'asset_digest': 'fixture-asset', 'room': 'R2' if i == 2 else 'R1',
                'lighting': 'L2' if i == 1 else 'L1', 'scene_content': 'animal_presence',
                'warmup_policy': 'fixture-warmup', 'completed': True,
                'evidence_kind': 'physical_device', 'timing_method': 'validated_present_intervals',
                'timing_validation_reference': 'fixture-only', 'touch_validation_reference': 'fixture-only',
                'offline_verified': True, 'network_trace_reviewed': True,
                'chargeable_inference_calls': 0, 'crashes': 0, 'interruptions': 0, 'thermal_warnings': 0,
            }
            (folder / 'manifest.json').write_text(json.dumps(manifest))
            with (folder / 'frames.csv').open('w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['frame_index', 'elapsed_ms', 'memory_mb', 'battery_level', 'thermal_state'])
                w.writerows((j, t, 100 + i, 0.8, 'nominal') for j, t in enumerate(range(0, 600001, 20)))
            self.touches(folder, 34 if i == 0 else 33)

    def touches(self, folder, count, bad=0):
        with (folder / 'touches.csv').open('w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['event_id', 'input_ms', 'visible_ms', 'uncertainty_ms'])
            w.writerows((j, j * 1000, j * 1000 + (120 if j < bad else 50), 1) for j in range(count))

    def change(self, i, **values):
        p = self.runs[i] / 'manifest.json'
        m = json.loads(p.read_text())
        m.update(values)
        p.write_text(json.dumps(m))

    def test_three_sessions_pool_touches_without_granting_presence_gate(self):
        report = inspect_series(self.runs)
        self.assertEqual(report['status'], 'PASS')
        self.assertEqual(report['presence_gate'], 'NOT RUN')
        self.assertEqual(report['touch_samples'], 100)
        self.assertEqual(report['touch_upper_bound_p95_ms'], 51)
        self.assertTrue(all(r['report']['status'] == 'PARTIAL' for r in report['runs']))

    def test_incomplete_diagnostic_cannot_pass_with_enough_pooled_touches(self):
        self.change(0, scene_content='instrumentation_only', completed=False, interruptions=1)
        report = inspect_series(self.runs)
        self.assertEqual(report['status'], 'FAIL')
        self.assertTrue(any('animal presence scene' in m for m in report['missing_evidence']))
        self.assertEqual(report['presence_gate'], 'NOT RUN')

    def test_pooled_p95_cannot_hide_bad_individual_session(self):
        self.touches(self.runs[0], 34, bad=3)
        report = inspect_series(self.runs)
        self.assertEqual(report['touch_upper_bound_p95_ms'], 51)
        self.assertEqual(report['status'], 'FAIL')
        self.assertTrue(any('fixture-0: touch' in f for f in report['failures']))

    def test_missing_count_and_room_lighting_coverage_remain_partial(self):
        for i, folder in enumerate(self.runs):
            self.touches(folder, 10)
            self.change(i, room='R1', lighting='L1')
        report = inspect_series(self.runs)
        self.assertEqual(report['status'], 'PARTIAL')
        self.assertEqual(len(report['missing_evidence']), 3)

    def test_fewer_than_three_sessions_remain_partial(self):
        self.assertEqual(inspect_series(self.runs[:2])['status'], 'PARTIAL')

    def test_zero_touch_session_stays_partial_even_with_100_pooled(self):
        self.touches(self.runs[0], 50)
        self.touches(self.runs[1], 50)
        self.touches(self.runs[2], 0)
        report = inspect_series(self.runs)
        self.assertEqual(report['touch_samples'], 100)
        self.assertEqual(report['status'], 'PARTIAL')
        self.assertIn('fixture-2: touch observations for this session', report['missing_evidence'])

    def test_mixed_identity_build_or_protocol_rejected(self):
        for key in ('species', 'device', 'os', 'build', 'asset_digest', 'protocol_revision', 'warmup_policy', 'timing_method'):
            original = json.loads((self.runs[1] / 'manifest.json').read_text())[key]
            self.change(1, **{key: 'different'})
            with self.subTest(key=key), self.assertRaises(EvidenceError):
                inspect_series(self.runs)
            self.change(1, **{key: original})

    def test_duplicate_path_id_or_frame_evidence_rejected(self):
        with self.assertRaises(EvidenceError):
            inspect_series([self.runs[0]] * 3)
        self.change(1, run_id='fixture-0')
        with self.assertRaises(EvidenceError):
            inspect_series(self.runs)
        self.change(1, run_id='fixture-1')
        (self.runs[1] / 'frames.csv').write_bytes((self.runs[0] / 'frames.csv').read_bytes())
        with self.assertRaises(EvidenceError):
            inspect_series(self.runs)

    def test_thermal_missing_and_failure_not_cleared_by_aggregation(self):
        self.change(0, thermal_warnings=1)
        self.assertEqual(inspect_series(self.runs)['status'], 'FAIL')
        self.change(0, thermal_warnings=None)
        self.assertEqual(inspect_series(self.runs)['status'], 'PARTIAL')

    def test_evidence_changed_during_inspection_rejected(self):
        def changed(folder):
            report = inspect_run(folder)
            with (folder / 'frames.csv').open('a') as f:
                f.write('changed')
            return report
        with patch('tools.benchmark_series.inspect_run', side_effect=changed), self.assertRaises(EvidenceError):
            inspect_series(self.runs)

    def test_cli_refuses_to_overwrite_raw_evidence(self):
        output = self.runs[0] / 'manifest.json'
        original = output.read_bytes()
        result = subprocess.run([sys.executable, 'tools/benchmark_series.py', *map(str, self.runs),
                                 '--output', str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(output.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
