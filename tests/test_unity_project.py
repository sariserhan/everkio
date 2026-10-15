import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from tools import unity_project
from tools.unity_project import command, validate_source, PROJECT, VERSION


class UnityProjectTests(unittest.TestCase):
    def test_local_package_resolves(self):
        package = validate_source()
        self.assertEqual(json.loads((package / 'package.json').read_text())['name'], 'com.everkio.benchmarks')

    def test_pinned_version_is_required(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'ProjectSettings').mkdir()
            (p / 'ProjectSettings/ProjectVersion.txt').write_text('m_EditorVersion: 6000.0.1f1\n')
            with self.assertRaises(ValueError):
                validate_source(p)

    def test_paths_with_spaces_and_shell_characters_are_literal_arguments(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / 'build $not-a-command'
            args = command('export-ios', Path('/Applications/Unity Editor'), PROJECT,
                           Path(d) / 'log file', output, 'com.example.everkio')
            self.assertEqual(args[0], '/Applications/Unity Editor')
            self.assertEqual(args[args.index('-everkioOutput') + 1], str(output))
            self.assertIn('iOS', args)
            self.assertEqual(args[-1], 'Everkio.Editor.EverkioBuild.ExportIOS')

    def test_existing_export_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                command('export-ios', Path('Unity'), PROJECT, Path('log'), Path(d), 'com.example.app')

    def test_export_requires_valid_explicit_bundle_id(self):
        with tempfile.TemporaryDirectory() as d:
            for bundle in (None, '', 'single', 'com.bad id', '-com.invalid', 'com..invalid'):
                with self.subTest(bundle=bundle), self.assertRaises(ValueError):
                    command('export-ios', Path('Unity'), PROJECT, Path('log'), Path(d) / 'out', bundle)

    def test_prepare_does_not_request_ios_or_export(self):
        args = command('prepare', Path('Unity'), PROJECT, Path('log'))
        self.assertNotIn('-buildTarget', args)
        self.assertNotIn('-everkioOutput', args)
        self.assertEqual(args[-1], 'Everkio.Editor.EverkioBuild.Prepare')

    def test_check_runs_without_unity(self):
        result = subprocess.run([sys.executable, 'tools/unity_project.py', 'check'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['unity_compilation'], 'NOT RUN')

    def test_dry_run_does_not_launch_or_create_export(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'new build'
            result = subprocess.run([sys.executable, 'tools/unity_project.py', 'export-ios', '--dry-run',
                                     '--unity', '/no/editor', '--output', str(out),
                                     '--bundle-id', 'com.example.everkio'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(out.exists())
            self.assertEqual(json.loads(result.stdout)[0], '/no/editor')

    def test_zero_exit_without_completion_marker_fails(self):
        with tempfile.TemporaryDirectory() as d, patch.object(unity_project, 'ROOT', Path(d)), \
             patch.object(unity_project.subprocess, 'run') as run:
            run.return_value.returncode = 0
            result = unity_project.main(['prepare', '--unity', sys.executable])
            self.assertEqual(result, 1)
            reports = list((Path(d) / 'artifacts').glob('*.json'))
            self.assertEqual(json.loads(reports[0].read_text())['status'], 'FAIL')

    def test_success_requires_method_completion_evidence(self):
        with tempfile.TemporaryDirectory() as d, patch.object(unity_project, 'ROOT', Path(d)), \
             patch.object(unity_project.subprocess, 'run') as run:
            def completed(args, **kwargs):
                Path(args[args.index('-logFile') + 1]).write_text('EVERKIO_PREPARE_OK 6000.6.6f1')
                return subprocess.CompletedProcess(args, 0)
            run.side_effect = completed
            self.assertEqual(unity_project.main(['prepare', '--unity', sys.executable]), 0)

    def test_existing_editor_lock_is_preserved(self):
        with tempfile.TemporaryDirectory() as d, patch.object(unity_project, 'PROJECT', Path(d)), \
             patch.object(unity_project, 'validate_source'):
            lock = Path(d) / 'Temp' / 'UnityLockfile'
            lock.parent.mkdir()
            lock.write_text('existing editor')
            self.assertEqual(unity_project.main(['prepare', '--unity', sys.executable]), 2)
            self.assertEqual(lock.read_text(), 'existing editor')

    def test_missing_editor_fails_without_creating_export(self):
        result = subprocess.run([sys.executable, 'tools/unity_project.py', 'prepare', '--unity', '/no/editor'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('unavailable', result.stderr)


if __name__ == '__main__':
    unittest.main()
