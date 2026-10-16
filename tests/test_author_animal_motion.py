import hashlib
import math
from pathlib import Path
import tempfile
import unittest
from tools.author_animal_motion import author, trajectory, CONTROLS


class MotionTrajectoryTests(unittest.TestCase):
    def test_stationary_bookends_and_total_travel(self):
        for phase, _ in CONTROLS.values():
            for seconds in (0, .5, 1):
                self.assertEqual(trajectory(seconds, phase), (0, 0, True, 0))
            for seconds in (4.2, 5, 6):
                travel, lift, planted, stance = trajectory(seconds, phase)
                self.assertAlmostEqual(travel, 1.05)
                self.assertEqual((lift, planted, stance), (0, True, 3))

    def test_stance_positions_and_monotonic_bounded_swing(self):
        for phase, _ in CONTROLS.values():
            stances, previous = {}, 0
            for i in range(6001):
                travel, lift, planted, stance = trajectory(i / 1000, phase)
                self.assertGreaterEqual(travel + 1e-12, previous)
                self.assertTrue(0 <= lift <= .065)
                self.assertTrue(math.isfinite(travel))
                if planted:
                    self.assertEqual(stances.setdefault(stance, travel), travel)
                    self.assertEqual(lift, 0)
                previous = travel
            self.assertEqual(set(stances), {0, 1, 2, 3})

    def test_zero_speed_and_lift_at_swing_boundaries(self):
        epsilon = 1e-5
        for phase, _ in CONTROLS.values():
            for step in range(3):
                for boundary in (1 + phase + step, 1.35 + phase + step):
                    left, right = trajectory(boundary - epsilon, phase), trajectory(boundary + epsilon, phase)
                    self.assertLess(abs(right[0] - left[0]) / (2 * epsilon), 1e-6)
                    self.assertLess(abs(right[1] - left[1]) / (2 * epsilon), 1e-3)

    def test_rejects_wrong_hash_before_output_or_blender(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'source.blend'
            source.write_bytes(b'unreviewed')
            output = Path(folder) / 'output'
            with self.assertRaisesRegex(ValueError, 'source hash'):
                author(source, '0' * 64, 'cat', output)
            self.assertFalse(output.exists())


    def test_refuses_existing_output_without_altering_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'source.blend'
            source.write_bytes(b'reviewed-source')
            output = Path(folder) / 'output'
            output.mkdir()
            evidence = output / 'motion-review.json'
            evidence.write_text('preserve me')
            with self.assertRaisesRegex(ValueError, 'new output directory'):
                author(source, hashlib.sha256(source.read_bytes()).hexdigest(), 'dog', output)
            self.assertEqual(evidence.read_text(), 'preserve me')


if __name__ == '__main__':
    unittest.main()
