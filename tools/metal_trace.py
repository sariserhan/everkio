#!/usr/bin/env python3
"""Inspect exported Instruments displayed-surface swaps; never grants G-P."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

try:
    from .benchmark import EvidenceError, percentile
except ImportError:
    from benchmark import EvidenceError, percentile


def inspect_trace(path, pid):
    if type(pid) is not int or pid <= 0:
        raise EvidenceError('Supply a positive application PID from this trace')
    payload = Path(path).read_bytes()
    root = ET.fromstring(payload)
    nodes = root.findall('./node')
    if len(nodes) != 1:
        raise EvidenceError('Export exactly one displayed-surfaces-interval table')
    node = nodes[0]
    schema = node.find('schema')
    if schema is None or schema.get('name') != 'displayed-surfaces-interval':
        raise EvidenceError('Expected displayed-surfaces-interval schema')
    columns = [c.findtext('mnemonic') for c in schema.findall('col')]
    required = {'start': 'start-time', 'display-name': 'display-name', 'event-label': 'narrative'}
    for name, kind in required.items():
        if columns.count(name) != 1:
            raise EvidenceError(f'Missing or ambiguous column: {name}')
        if schema.findall('col')[columns.index(name)].findtext('engineering-type') != kind:
            raise EvidenceError(f'Unexpected column type: {name}')
    ids = {}
    for element in node.iter():
        key = element.get('id')
        if key is not None:
            if key in ids:
                raise EvidenceError('Duplicate XML reference identifier')
            ids[key] = element

    def resolve(element):
        seen = set()
        while element.get('ref') is not None:
            ref = element.get('ref')
            if ref in seen or ref not in ids or ids[ref].tag != element.tag:
                raise EvidenceError('Invalid XML reference')
            seen.add(ref)
            element = ids[ref]
        return element

    times, displays = [], set()
    skipped = 0
    for row in node.findall('row'):
        if len(row) != len(columns):
            raise EvidenceError('Row does not match schema')
        label = resolve(row[columns.index('event-label')])
        processes = [resolve(p) for p in label.iter('process')]
        pids = set()
        for process in processes:
            value = process.find('pid')
            if value is None:
                raise EvidenceError('Process attribution lacks PID')
            pids.add(resolve(value).text)
        if str(pid) not in pids:
            skipped += 1
            continue
        if pids != {str(pid)}:
            raise EvidenceError('Ambiguous process attribution')
        start = resolve(row[columns.index('start')])
        display = resolve(row[columns.index('display-name')])
        if start.tag != 'start-time' or not (start.text or '').isdigit():
            raise EvidenceError('Expected nonnegative integer swap time in nanoseconds')
        timestamp = int(start.text)
        if times and timestamp <= times[-1]:
            raise EvidenceError('Application swap times must strictly increase')
        if not display.text or not display.text.strip():
            raise EvidenceError('Missing display identity')
        times.append(timestamp)
        displays.add(display.text)
    if len(times) < 2 or len(displays) != 1:
        raise EvidenceError('Need at least two application swaps on exactly one display')
    intervals = [(b - a) / 1_000_000 for a, b in zip(times, times[1:])]
    return {
        'schema_version': 1,
        'scope': 'Displayed-surface setup inspection only; not validated recorder timing or G-P acceptance',
        'status': 'PARTIAL', 'presence_gate': 'NOT RUN', 'pid': pid,
        'display': next(iter(displays)), 'attributed_swaps': len(times),
        'other_or_unattributed_rows': skipped,
        'swap_span_seconds': (times[-1] - times[0]) / 1_000_000_000,
        'swap_interval_p95_ms': percentile(intervals), 'worst_swap_interval_ms': max(intervals),
        'evidence_sha256': hashlib.sha256(payload).hexdigest(),
        'limitations': [
            'No animal, device/build or study-protocol acceptance is inferred from XML alone',
            'No common-clock correlation with Unity Update samples or overhead calibration',
            'CPU-to-display latency is not touch-to-visible latency; no touch result calculated',
            'Trace boundaries and skipped/unattributed rows require review; no continuity claim',
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export', type=Path)
    parser.add_argument('--pid', type=int, required=True)
    parser.add_argument('--output', type=Path, help='new JSON report; never overwrites evidence')
    args = parser.parse_args()
    try:
        report = inspect_trace(args.export, args.pid)
        payload = json.dumps(report, indent=2, allow_nan=False) + '\n'
        if args.output:
            with args.output.open('x') as stream:
                stream.write(payload)
        else:
            print(payload, end='')
        return 1  # Setup evidence is always PARTIAL, regardless of interval values.
    except (OSError, ValueError, TypeError, ET.ParseError) as exc:
        print(f'Evidence error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
