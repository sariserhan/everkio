#!/usr/bin/env python3
"""Inspect one animal/device's session series; never grants G-P acceptance."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

try:
    from .benchmark import EvidenceError, TOUCH_COUNT_MISSING, inspect_run, number, percentile, read_csv
except ImportError:
    from benchmark import EvidenceError, TOUCH_COUNT_MISSING, inspect_run, number, percentile, read_csv


def inspect_series(folders):
    folders = [Path(p).resolve() for p in folders]
    if not folders or len(set(folders)) != len(folders):
        raise EvidenceError('Supply nonempty, distinct run directories')
    runs, manifests, latencies = [], [], []
    run_ids, frame_hashes = set(), set()
    failures, missing = [], []
    common = ('species', 'device', 'os', 'build', 'asset_digest', 'protocol_revision',
              'warmup_policy', 'timing_method', 'thermal_method')
    for folder in folders:
        report = inspect_run(folder)
        manifest = json.loads((folder / 'manifest.json').read_text())
        run_id = manifest.get('run_id')
        if not isinstance(run_id, str) or not run_id.strip() or run_id in run_ids:
            raise EvidenceError('Each session needs a nonempty, unique run_id')
        run_ids.add(run_id)
        frame_hash = report['evidence_sha256']['frames.csv']
        if frame_hash in frame_hashes:
            raise EvidenceError('Identical frame files cannot count as independent sessions')
        frame_hashes.add(frame_hash)
        if manifests and any(manifest.get(k) != manifests[0].get(k) for k in common):
            raise EvidenceError('Sessions must use the same animal, device, OS, build, asset and protocol/methods')
        manifests.append(manifest)
        failures.extend(f'{run_id}: {f}' for f in report['failures'])
        missing.extend(f'{run_id}: {m}' for m in report['missing_evidence'] if m != TOUCH_COUNT_MISSING)
        if report['metrics']['touch_samples'] == 0:
            missing.append(f'{run_id}: touch observations for this session')
        touch_path = folder / 'touches.csv'
        if 'touches.csv' in report['evidence_sha256']:
            touches = read_csv(touch_path, ['event_id', 'input_ms', 'visible_ms', 'uncertainty_ms'])
            latencies.extend(number(t['visible_ms'], 'visible_ms') - number(t['input_ms'], 'input_ms') +
                             number(t['uncertainty_ms'], 'uncertainty_ms') for t in touches)
        # Refuse a report assembled from evidence that changed during inspection.
        for name, digest in report['evidence_sha256'].items():
            if hashlib.sha256((folder / name).read_bytes()).hexdigest() != digest:
                raise EvidenceError('Evidence changed during inspection')
        runs.append({'path': str(folder), 'report': report})
    if len(runs) < 3:
        missing.append('at least three sessions for this animal/device')
    rooms = sorted({m['room'] for m in manifests if isinstance(m.get('room'), str) and m['room'].strip()})
    lighting = sorted({m['lighting'] for m in manifests if isinstance(m.get('lighting'), str) and m['lighting'].strip()})
    if len(rooms) < 2:
        missing.append('two room configurations across sessions')
    if len(lighting) < 2:
        missing.append('two lighting conditions across sessions')
    if len(latencies) < 100:
        missing.append('100 validated touch samples across sessions')
    touch_p95 = percentile(latencies)
    if touch_p95 is not None and touch_p95 >= 100:
        failures.append('pooled touch upper-bound p95 is not below 100 ms')
    return {
        'schema_version': 1, 'scope': 'One animal/device numerical session series only; not G-P acceptance',
        'status': 'FAIL' if failures else ('PARTIAL' if missing else 'PASS'),
        'presence_gate': 'NOT RUN', 'failures': failures, 'missing_evidence': missing,
        'configuration': {k: manifests[0].get(k) for k in common},
        'session_count': len(runs), 'rooms': rooms, 'lighting': lighting,
        'touch_samples': len(latencies), 'touch_upper_bound_p95_ms': touch_p95, 'runs': runs,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runs', type=Path, nargs='+')
    parser.add_argument('--output', type=Path, help='new JSON report; never overwrites evidence')
    args = parser.parse_args()
    try:
        report = inspect_series(args.runs)
        payload = json.dumps(report, indent=2, allow_nan=False) + '\n'
        if args.output:
            with args.output.open('x') as stream:
                stream.write(payload)
        else:
            print(payload, end='')
        return 0 if report['status'] == 'PASS' else 1
    except (OSError, ValueError, TypeError) as exc:
        print(f'Evidence error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
