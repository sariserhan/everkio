#!/usr/bin/env python3
"""Prepare, validate or export the M0 Unity project using a locally installed editor."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'unity' / 'Everkio'
VERSION = '6000.6.6f1'
DEFAULT_EDITOR = Path(f'/Applications/Unity/Hub/Editor/{VERSION}/Unity.app/Contents/MacOS/Unity')
METHODS = {'prepare': 'Prepare', 'validate': 'Validate', 'export-ios': 'ExportIOS'}
MARKERS = {'prepare': 'EVERKIO_PREPARE_OK', 'validate': 'EVERKIO_EDITOR_VALIDATION_OK',
           'export-ios': 'EVERKIO_IOS_EXPORT_OK'}


def validate_source(project=PROJECT):
    version = (project / 'ProjectSettings' / 'ProjectVersion.txt').read_text()
    if f'm_EditorVersion: {VERSION}' not in version.splitlines():
        raise ValueError(f'Project must be pinned to {VERSION}')
    manifest = json.loads((project / 'Packages' / 'manifest.json').read_text())
    package = manifest['dependencies']['com.everkio.benchmarks']
    if not package.startswith('file:'):
        raise ValueError('Benchmark package must resolve locally')
    package_root = (project / 'Packages' / package[5:]).resolve()
    if not (package_root / 'package.json').is_file():
        raise ValueError(f'Missing local benchmark package: {package_root}')
    return package_root


def command(action, editor, project, log, output=None, bundle_id=None):
    if action not in METHODS:
        raise ValueError('Unknown action')
    args = [str(editor), '-batchmode', '-quit', '-projectPath', str(project), '-logFile', str(log)]
    if action == 'export-ios':
        if output is None or not bundle_id:
            raise ValueError('export-ios requires --output and --bundle-id')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9-]*(\.[A-Za-z][A-Za-z0-9-]*)+', bundle_id):
            raise ValueError('Invalid bundle identifier')
        if output.exists():
            raise ValueError('Output already exists; select a new destination')
        # Build target must be selected before script compilation in batch mode.
        args += ['-buildTarget', 'iOS', '-everkioOutput', str(output), '-everkioBundleId', bundle_id]
    elif output is not None or bundle_id:
        raise ValueError('--output and --bundle-id are only valid for export-ios')
    args += ['-executeMethod', f'Everkio.Editor.EverkioBuild.{METHODS[action]}']
    return args


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', *METHODS])
    parser.add_argument('--unity', type=Path, default=DEFAULT_EDITOR)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--bundle-id')
    parser.add_argument('--dry-run', action='store_true', help='print argument array without launching Unity')
    args = parser.parse_args(argv)
    try:
        package = validate_source()
        if args.action == 'check':
            if args.output or args.bundle_id:
                raise ValueError('check does not accept export options')
            print(json.dumps({'source_structure': 'PASS', 'editor_version': VERSION,
                              'local_package': str(package), 'unity_compilation': 'NOT RUN',
                              'device_acceptance': 'NOT RUN'}, indent=2))
            return 0
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
        log = ROOT / 'artifacts' / f'{args.action}-{stamp}.log'
        output = args.output.resolve() if args.output else None
        editor = args.unity.expanduser().resolve()
        cmd = command(args.action, editor, PROJECT, log, output, args.bundle_id)
        if args.dry_run:
            print(json.dumps(cmd, indent=2))
            return 0
        if not editor.is_file() or not os.access(editor, os.X_OK):
            raise ValueError(f'Unity executable unavailable: {editor}. Run this command on the Mac or pass --unity.')
        if (PROJECT / 'Temp' / 'UnityLockfile').exists():
            raise ValueError('Project may be open in Unity. Close the editor first; lockfiles are not removed automatically.')
        if args.action == 'export-ios' and sys.platform != 'darwin':
            raise ValueError('This export workflow requires the configured Mac build host')
        log.parent.mkdir(parents=True, exist_ok=True)
        print(f'Running Unity {VERSION}. Log: {log}', flush=True)
        result = subprocess.run(cmd, check=False)  # argument list, never a shell
        report = {'action': args.action, 'editor_version': VERSION, 'exit_code': result.returncode,
                  'status': 'PASS' if result.returncode == 0 else 'FAIL',
                  'scope': 'Unity command only; no device or presence acceptance', 'log': str(log)}
        if result.returncode == 0 and (not log.is_file() or MARKERS[args.action] not in log.read_text(errors='replace')):
            report['status'] = 'FAIL'
            report['error'] = 'Expected completion marker missing; editor method execution is not established'
        if result.returncode == 0 and args.action == 'export-ios':
            if not (output / 'Unity-iPhone.xcodeproj').is_dir():
                report['status'] = 'FAIL'
                report['error'] = 'Unity exited successfully but expected Xcode project is absent'
        report_path = log.with_suffix('.json')
        report_path.write_text(json.dumps(report, indent=2) + '\n')
        print(f"{report['status']}: {report_path}")
        return 0 if report['status'] == 'PASS' else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Setup error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
