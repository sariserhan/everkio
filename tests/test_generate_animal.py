from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.generate_animal import CONFIG_SHA256, SOURCE_REVISION, WEIGHT_SHA256, check_inputs, digest


class GenerationGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source'
        self.weights = self.root / 'weights'
        self.image = self.root / 'reference.png'
        self.output = self.root / 'output'
        (self.source / 'tsr').mkdir(parents=True)
        self.weights.mkdir()
        for path in (self.source / 'tsr/system.py', self.weights / 'config.yaml',
                     self.weights / 'model.ckpt', self.image):
            path.write_text('synthetic test fixture, never a real model')

    def check(self):
        check_inputs(self.source, self.weights, self.image, self.output)

    def git_results(self, revision=SOURCE_REVISION, changes=''):
        return [subprocess.CompletedProcess([], 0, revision), subprocess.CompletedProcess([], 0, changes)]

    def test_existing_output_is_untouched(self):
        self.output.mkdir()
        marker = self.output / 'evidence'
        marker.write_text('preserve')
        with patch('tools.generate_animal.subprocess.run') as run:
            with self.assertRaises(ValueError): self.check()
            run.assert_not_called()
        self.assertEqual(marker.read_text(), 'preserve')

    def test_missing_input_and_output_parent_rejected(self):
        self.image.unlink()
        with self.assertRaises(ValueError): self.check()
        self.image.write_text('fixture')
        self.output = self.root / 'missing' / 'output'
        with self.assertRaises(ValueError): self.check()

    def test_wrong_or_modified_source_rejected(self):
        for revision, changes in (('other', ''), (SOURCE_REVISION, ' M tsr/system.py')):
            with self.subTest(revision=revision, changes=changes):
                with patch('tools.generate_animal.subprocess.run', side_effect=self.git_results(revision, changes)):
                    with self.assertRaises(ValueError): self.check()

    def test_unverified_model_or_config_rejected(self):
        for hashes in (['wrong'], [WEIGHT_SHA256, 'wrong']):
            with self.subTest(hashes=hashes):
                with patch('tools.generate_animal.subprocess.run', side_effect=self.git_results()), \
                     patch('tools.generate_animal.digest', side_effect=hashes):
                    with self.assertRaises(ValueError): self.check()

    def test_verified_preflight_does_not_create_output(self):
        with patch('tools.generate_animal.subprocess.run', side_effect=self.git_results()), \
             patch('tools.generate_animal.digest', side_effect=[WEIGHT_SHA256, CONFIG_SHA256]):
            self.check()
        self.assertFalse(self.output.exists())

    def test_digest_streams_exact_bytes(self):
        import hashlib
        self.assertEqual(digest(self.image), hashlib.sha256(self.image.read_bytes()).hexdigest())

    def test_cli_rejects_unapproved_species_without_ml_dependencies(self):
        command = [sys.executable, 'tools/generate_animal.py', '--source', str(self.source),
                   '--weights', str(self.weights), '--image', str(self.image),
                   '--species', 'wolf', '--output', str(self.output)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
