#!/usr/bin/env python3
"""Local M0 evidence inspector. Never grants G-P or launch approval."""
import argparse
import bisect
import csv
import hashlib
import json
import math
from pathlib import Path
import sys


class EvidenceError(ValueError):
    pass


TOUCH_COUNT_MISSING = '100 touch samples in this run (use benchmark_series.py for cross-run aggregation)'


def number(value, label, minimum=0):
    if isinstance(value, bool):
        raise EvidenceError(f'{label}: boolean is not a measurement')
    try:
        n = float(value)
    except (ValueError, TypeError) as exc:
        raise EvidenceError(f'{label}: expected a finite number') from exc
    if not math.isfinite(n) or n < minimum:
        raise EvidenceError(f'{label}: invalid measurement {value!r}')
    return n


def percentile(values, p=0.95):
    """Nearest rank, deliberately no interpolation at the acceptance boundary."""
    if not values:
        return None
    return sorted(values)[math.ceil(p * len(values)) - 1]


def read_csv(path, columns):
    with path.open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != columns:
            raise EvidenceError(f'{path.name}: expected columns {columns}')
        rows = list(reader)
    if any(None in row or None in row.values() for row in rows):
        raise EvidenceError(f'{path.name}: malformed row')
    return rows


def inspect_run(folder):
    folder = Path(folder)
    manifest_path = folder / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    if not isinstance(manifest, dict) or manifest.get('schema_version') != 1:
        raise EvidenceError('unsupported manifest schema')
    missing, failures = [], []
    for key in ('run_id', 'protocol_revision', 'operator', 'device', 'os', 'build',
                'asset_digest', 'room', 'lighting', 'timing_method', 'warmup_policy'):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            missing.append(f'manifest.{key}')
    if manifest.get('scene_content') != 'animal_presence':
        missing.append('animal presence scene (instrumentation-only captures do not qualify)')
    if manifest.get('species') not in ('cat', 'dog'):
        missing.append('manifest.species (cat or dog)')
    if manifest.get('evidence_kind') != 'physical_device':
        missing.append('physical-device evidence (synthetic/editor captures are diagnostic only)')
    if manifest.get('timing_method') != 'validated_present_intervals':
        missing.append('validated presentation timing (Unity Update is only a proxy)')
    if not manifest.get('timing_validation_reference'):
        missing.append('timing validation reference')
    if manifest.get('completed') is not True:
        missing.append('completed capture; aborted runs remain in evidence')
    for flag in ('offline_verified', 'network_trace_reviewed'):
        if manifest.get(flag) is not True:
            missing.append(flag)
    calls = manifest.get('chargeable_inference_calls')
    if calls is None:
        missing.append('chargeable inference count')
    elif number(calls, 'chargeable_inference_calls') != 0:
        failures.append('interaction used chargeable cloud inference')
    for key in ('crashes', 'interruptions', 'thermal_warnings'):
        value = manifest.get(key)
        if value is None:
            missing.append(key)
        elif number(value, key) != 0:
            failures.append(key)

    frames_path = folder / 'frames.csv'
    rows = read_csv(frames_path, ['frame_index', 'elapsed_ms', 'memory_mb', 'battery_level', 'thermal_state'])
    times, memory, battery, thermals = [], [], [], []
    for i, row in enumerate(rows):
        if row['frame_index'] != str(i):
            raise EvidenceError('frame indices must be contiguous from zero')
        t = number(row['elapsed_ms'], 'elapsed_ms')
        if (i == 0 and t != 0) or (i > 0 and t <= times[-1]):
            raise EvidenceError('timestamps must start at zero and strictly increase')
        times.append(t)
        if row['memory_mb']:
            memory.append(number(row['memory_mb'], 'memory_mb'))
        if row['battery_level']:
            b = number(row['battery_level'], 'battery_level')
            if b > 1:
                raise EvidenceError('battery_level must be between zero and one')
            battery.append((i, b))
        if row['thermal_state'] not in ('unknown', 'nominal', 'fair', 'serious', 'critical'):
            raise EvidenceError('unrecognized thermal_state')
        thermals.append(row['thermal_state'])
    intervals = [b - a for a, b in zip(times, times[1:])]
    duration = times[-1] if times else 0
    if duration < 600000:
        missing.append('at least 600 seconds of continuous scored capture')
    p95 = percentile(intervals)
    if p95 is not None and p95 > 33.3:
        failures.append('frame interval p95 exceeds 33.3 ms')
    # Count completed intervals in (start, end]; intervals spanning a stall do
    # not create imaginary frames. Include the trailing partial window in output.
    windows = []
    for start in range(0, math.ceil(duration), 60000):
        end = min(start + 60000, duration)
        count = bisect.bisect_right(times, end) - bisect.bisect_right(times, start)
        fps = count / ((end - start) / 1000)
        complete = end - start == 60000
        windows.append({'start_ms': start, 'end_ms': end, 'fps': fps, 'complete': complete})
        if complete and fps < 30:
            failures.append(f'sustained FPS below 30 at minute {start // 60000 + 1}')
    if len(memory) != len(rows) or not rows:
        missing.append('complete memory samples')
    if not battery or battery[0][0] != 0 or battery[-1][0] != len(rows) - 1:
        missing.append('battery start/end measurements')
    if not thermals or 'unknown' in thermals:
        missing.append('thermal-state coverage')
    if any(t in ('serious', 'critical') for t in thermals):
        failures.append('serious/critical thermal state')

    touches_path = folder / 'touches.csv'
    latencies = []
    if touches_path.exists():
        touches = read_csv(touches_path, ['event_id', 'input_ms', 'visible_ms', 'uncertainty_ms'])
        ids = set()
        for row in touches:
            if not row['event_id'] or row['event_id'] in ids:
                raise EvidenceError('touch event IDs must be nonempty and unique')
            ids.add(row['event_id'])
            start = number(row['input_ms'], 'input_ms')
            end = number(row['visible_ms'], 'visible_ms')
            error = number(row['uncertainty_ms'], 'uncertainty_ms')
            if end < start or end > duration:
                raise EvidenceError('touch timestamps must be ordered and within capture')
            latencies.append(end - start + error)
    if len(latencies) < 100:
        missing.append(TOUCH_COUNT_MISSING)
    touch_p95 = percentile(latencies)
    if touch_p95 is not None and touch_p95 >= 100:
        failures.append('touch upper-bound p95 is not below 100 ms')
    if not manifest.get('touch_validation_reference'):
        missing.append('validated input-to-visible touch method')

    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (manifest_path, frames_path, touches_path) if p.exists()}
    return {
        'schema_version': 1, 'run_id': manifest.get('run_id'),
        'scope': 'Single-run numerical inspection only; not G-P acceptance',
        'status': 'FAIL' if failures else ('PARTIAL' if missing else 'PASS'),
        'presence_gate': 'NOT RUN', 'failures': failures, 'missing_evidence': missing,
        'metrics': {'duration_seconds': duration / 1000, 'frame_intervals': len(intervals),
                    'frame_p95_ms': p95, 'worst_frame_ms': max(intervals, default=None),
                    'windows': windows, 'touch_samples': len(latencies),
                    'touch_upper_bound_p95_ms': touch_p95,
                    'memory_peak_mb': max(memory, default=None),
                    'battery_change': battery[-1][1] - battery[0][1] if battery else None},
        'evidence_sha256': hashes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path, help='directory containing manifest.json and frames.csv')
    parser.add_argument('--output', type=Path, help='new JSON report file; never overwrites evidence')
    args = parser.parse_args()
    try:
        report = inspect_run(args.run)
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
