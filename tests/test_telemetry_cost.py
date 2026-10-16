import csv
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stderr
import io
from tools import telemetry_cost
from tools.benchmark import EvidenceError
from tools.telemetry_cost import inspect_cost


class TelemetryCostTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.manifest = dict(schema='everkio-telemetry-cost-1', presence_gate='NOT RUN',
            calibration_validated=False, full_instrumentation_overhead_validated=False,
            evidence_kind='telemetry_cost_setup_only', scene_content='instrumentation_only',
            measured_work='shared_telemetry_reads_and_preallocated_buffer_append',
            completed=True, interrupted=False, high_resolution=True, expected_pairs=1024,
            recorded_rows=2048, stopwatch_frequency=1000000, run_id='synthetic-fixture',
            started_utc='2026-10-16T00:00:00Z', build_guid='synthetic', device_model='synthetic',
            os='synthetic', unity_version='6000.6.6f1', stop_reason='pairs_reached', thermal_method='unavailable')
        self.rows = []
        tick = 0
        for pair in range(1024):
            for phase in (('clock_only', 'telemetry') if pair % 2 == 0 else ('telemetry', 'clock_only')):
                end = tick + (2 if phase == 'clock_only' else 100)
                self.rows.append([pair, phase, tick, end, *(['', '', ''] if phase == 'clock_only' else [1024, '.5', 'unknown'])])
                tick = end

    def inspect(self):
        (self.folder / 'manifest.json').write_text(json.dumps(self.manifest))
        with (self.folder / 'costs.csv').open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['pair_index', 'phase', 'start_tick', 'end_tick', 'memory_bytes', 'battery_level', 'thermal_state'])
            writer.writerows(self.rows)
        return inspect_cost(self.folder)

    def test_alternating_pairs_report_raw_costs_and_never_pass(self):
        result = self.inspect()
        self.assertEqual(result['status'], 'PARTIAL')
        self.assertEqual(result['presence_gate'], 'NOT RUN')
        self.assertEqual(result['costs_us']['clock_only']['p95'], 2)
        self.assertEqual(result['costs_us']['telemetry']['p95'], 100)
        self.assertEqual(result['costs_us']['telemetry']['samples'], 1024)

    def test_rejects_wrong_pair_order_and_clock_overlap(self):
        original = [r[:] for r in self.rows]
        for column, value in [(0, 3), (1, 'clock_only'), (2, -1), (3, 0)]:
            with self.subTest(column=column):
                self.rows = [r[:] for r in original]
                self.rows[1][column] = value
                with self.assertRaises(EvidenceError): self.inspect()
        self.rows = original
        self.rows[2][2] = 0
        with self.assertRaises(EvidenceError): self.inspect()

    def test_rejects_false_completion_and_acceptance_claims(self):
        for key, value in [('recorded_rows', 1), ('calibration_validated', True),
                           ('full_instrumentation_overhead_validated', True), ('presence_gate', 'PASS'),
                           ('interrupted', True), ('stopwatch_frequency', True), ('expected_pairs', True)]:
            with self.subTest(key=key):
                old = self.manifest[key]; self.manifest[key] = value
                with self.assertRaises(EvidenceError): self.inspect()
                self.manifest[key] = old

    def test_preserves_interrupted_partial_pair_without_inventing_samples(self):
        self.rows = self.rows[:5]
        self.manifest.update(completed=False, interrupted=True, recorded_rows=5, stop_reason='focus_lost')
        result = self.inspect()
        self.assertEqual(sum(r['samples'] for r in result['costs_us'].values()), 5)
        self.assertFalse(result['completed'])

    def test_rejects_invalid_telemetry_and_control_contamination(self):
        for row, column, value in [(1, 4, '-1'), (1, 5, 'nan'), (1, 5, '1.1'), (1, 6, 'happy'), (0, 4, '1024')]:
            with self.subTest(row=row, column=column, value=value):
                old = self.rows[row][column]; self.rows[row][column] = value
                with self.assertRaises(EvidenceError): self.inspect()
                self.rows[row][column] = old

    def test_zero_length_clock_interval_and_low_resolution_do_not_pass_calibration(self):
        self.rows[0][3] = 0
        self.manifest['high_resolution'] = False
        result = self.inspect()
        self.assertFalse(result['high_resolution'])
        self.assertEqual(result['status'], 'PARTIAL')

    def test_cli_preserves_existing_report(self):
        self.inspect()
        output = self.folder / 'report.json'
        with patch('sys.argv', ['telemetry_cost.py', str(self.folder), '--output', str(output)]):
            self.assertEqual(telemetry_cost.main(), 1)
            original = output.read_bytes()
            with redirect_stderr(io.StringIO()):
                self.assertEqual(telemetry_cost.main(), 2)
            self.assertEqual(output.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
