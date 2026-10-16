#!/usr/bin/env python3
"""Inspect telemetry-call setup costs; never validates total instrumentation overhead."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

try:
    from .benchmark import EvidenceError, number, percentile
except ImportError:
    from benchmark import EvidenceError, number, percentile


def inspect_cost(folder):
    folder = Path(folder)
    with (folder / 'manifest.json').open('rb') as stream:
        manifest = stream.read(65537)
    with (folder / 'costs.csv').open('rb') as stream:
        payload = stream.read(2_000_001)
    if len(manifest) > 65536 or len(payload) > 2_000_000:
        raise EvidenceError('Cost setup bundle exceeds schema limits')
    m = json.loads(manifest)
    if not isinstance(m, dict) or m.get('schema') != 'everkio-telemetry-cost-1':
        raise EvidenceError('Unsupported cost setup schema')
    for key, expected in {'presence_gate': 'NOT RUN', 'calibration_validated': False,
                          'full_instrumentation_overhead_validated': False,
                          'evidence_kind': 'telemetry_cost_setup_only', 'scene_content': 'instrumentation_only',
                          'measured_work': 'shared_telemetry_reads_and_preallocated_buffer_append'}.items():
        if type(m.get(key)) is not type(expected) or m[key] != expected:
            raise EvidenceError(f'Unexpected setup declaration: {key}')
    for key in ('completed', 'interrupted', 'high_resolution'):
        if type(m.get(key)) is not bool:
            raise EvidenceError(f'Expected boolean: {key}')
    if m['completed'] == m['interrupted']:
        raise EvidenceError('Setup must be complete or explicitly interrupted')
    for key in ('run_id', 'started_utc', 'build_guid', 'device_model', 'os', 'unity_version', 'stop_reason', 'thermal_method'):
        if not isinstance(m.get(key), str) or not m[key].strip():
            raise EvidenceError(f'Missing provenance declaration: {key}')
    if type(m.get('expected_pairs')) is not int or m['expected_pairs'] != 1024:
        raise EvidenceError('Expected the fixed 1024-pair setup')
    frequency = m.get('stopwatch_frequency')
    if type(frequency) is not int or not 0 < frequency <= 10**12:
        raise EvidenceError('Invalid stopwatch frequency')
    reader = csv.DictReader(io.StringIO(payload.decode('utf-8-sig')))
    if reader.fieldnames != ['pair_index', 'phase', 'start_tick', 'end_tick', 'memory_bytes', 'battery_level', 'thermal_state']:
        raise EvidenceError('Unexpected cost CSV columns')
    rows = list(reader)
    if type(m.get('recorded_rows')) is not int or len(rows) != m['recorded_rows'] or len(rows) > 2048:
        raise EvidenceError('Recorded row count differs from manifest or exceeds capacity')
    if m['completed'] and (m['interrupted'] or len(rows) != 2048 or m['stop_reason'] != 'pairs_reached'):
        raise EvidenceError('Contradictory completion declaration')
    costs = {'clock_only': [], 'telemetry': []}
    previous = 0
    thermal_states = set()
    for i, row in enumerate(rows):
        if None in row or None in row.values():
            raise EvidenceError('Malformed cost row')
        phases = ('clock_only', 'telemetry') if i // 2 % 2 == 0 else ('telemetry', 'clock_only')
        phase = phases[i % 2]
        if row['pair_index'] != str(i // 2) or row['phase'] != phase:
            raise EvidenceError('Cost pairs must be contiguous with alternating order')
        ticks = [row[k] for k in ('start_tick', 'end_tick')]
        if not all(v.isascii() and v.isdecimal() for v in ticks):
            raise EvidenceError('Clock ticks must be nonnegative decimal integers')
        start, end = map(int, ticks)
        if start < previous or end < start or end > 2**63 - 1:
            raise EvidenceError('Clock intervals must be ordered and bounded')
        previous = end
        if phase == 'clock_only':
            if any(row[k] for k in ('memory_bytes', 'battery_level', 'thermal_state')):
                raise EvidenceError('Clock-only control contains telemetry')
        else:
            memory = row['memory_bytes']
            if not memory.isascii() or not memory.isdecimal() or int(memory) > 2**63 - 1:
                raise EvidenceError('Invalid memory measurement')
            if row['battery_level'] and number(row['battery_level'], 'battery_level') > 1:
                raise EvidenceError('Battery level must be between zero and one')
            if row['thermal_state'] not in ('unknown', 'nominal', 'fair', 'serious', 'critical'):
                raise EvidenceError('Invalid thermal category')
            thermal_states.add(row['thermal_state'])
        costs[phase].append((end - start) * 1_000_000 / frequency)
    return {
        'schema_version': 1, 'status': 'PARTIAL', 'presence_gate': 'NOT RUN',
        'scope': 'Telemetry reads/buffer append setup only; no full-overhead, presentation or latency validation',
        'run_id': m['run_id'], 'build_guid': m['build_guid'], 'device': m['device_model'],
        'completed': m['completed'], 'interrupted': m['interrupted'], 'high_resolution': m['high_resolution'],
        'stopwatch_frequency': frequency, 'thermal_states': sorted(thermal_states),
        'costs_us': {phase: {'samples': len(values), 'p50': percentile(values, .5),
                            'p95': percentile(values), 'worst': max(values) if values else None}
                     for phase, values in costs.items()},
        'evidence_sha256': {'manifest.json': hashlib.sha256(manifest).hexdigest(),
                            'costs.csv': hashlib.sha256(payload).hexdigest()},
        'limitations': ['Clock-only costs are reported separately, never subtracted or used as a correction',
                       'Repeated calls in an empty diagnostic workload do not establish per-frame animal workload cost',
                       'No full recorder control flow, GUI, disk export, GPU or observer-overhead calibration',
                       'Clock frequency/provenance are declarations; no independent clock or device authenticity validation'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        payload = json.dumps(inspect_cost(args.folder), indent=2, allow_nan=False) + '\n'
        if args.output:
            with args.output.open('x') as stream:
                stream.write(payload)
        else:
            print(payload, end='')
        return 1  # A cost probe can never pass calibration or a product gate.
    except (OSError, ValueError, TypeError) as error:
        print(f'Evidence error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
