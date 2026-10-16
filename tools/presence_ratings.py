#!/usr/bin/env python3
"""Inspect anonymous blinded ratings; never grants the presence gate."""
import argparse
import json
from pathlib import Path
import re
import sys

try:
    from .benchmark import EvidenceError, read_csv
    from .generate_animal import digest
except ImportError:
    from benchmark import EvidenceError, read_csv
    from generate_animal import digest

DIMENSIONS = ('animal_realism', 'room_presence', 'natural_motion')
COLUMNS = ['evaluator_id', 'consented_adult', 'species', 'clip_id', 'presentation_order', 'dimension', 'score']


def inspect_ratings(folder):
    folder = Path(folder).resolve()
    manifest_path, ratings_path = folder / 'manifest.json', folder / 'ratings.csv'
    hashes = {p.name: digest(p) for p in (manifest_path, ratings_path)}
    manifest = json.loads(manifest_path.read_text())
    if not isinstance(manifest, dict) or type(manifest.get('schema_version')) is not int or manifest['schema_version'] != 1:
        raise EvidenceError('Unsupported ratings manifest')
    clips = manifest.get('clips')
    if not isinstance(clips, dict) or set(clips) != {'cat', 'dog'}:
        raise EvidenceError('One frozen cat/dog clip pair is required per study bundle')
    cohort = manifest.get('evaluator_ids')
    if not isinstance(cohort, list) or any(not isinstance(e, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', e) for e in cohort) or len(set(cohort)) != len(cohort):
        raise EvidenceError('A frozen list of distinct anonymous evaluator IDs is required')
    evaluators = set(cohort)
    clip_ids, clip_hashes, clip_paths, failures, missing = set(), set(), set(), [], []
    for key in ('protocol_revision', 'operator', 'blinding_reference', 'consent_reference'):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            missing.append(f'manifest.{key}')
    if manifest.get('evidence_kind') != 'physical_device' or manifest.get('scene_content') != 'animal_presence':
        missing.append('physical-device animal/AR clips; desktop/diagnostic/synthetic clips cannot qualify')
    for species, clip in clips.items():
        if not isinstance(clip, dict) or not isinstance(clip.get('clip_id'), str) or not clip['clip_id'].strip() or clip['clip_id'] in clip_ids:
            raise EvidenceError('Clips need distinct, nonempty IDs')
        clip_ids.add(clip['clip_id'])
        relative = clip.get('file')
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            raise EvidenceError('Clip paths must be relative to this bundle')
        path = (folder / relative).resolve()
        if not path.is_relative_to(folder) or path in (manifest_path, ratings_path):
            raise EvidenceError('Clip path escapes the bundle or refers to study inputs')
        if not re.fullmatch(r'[0-9a-f]{64}', str(clip.get('sha256', ''))):
            raise EvidenceError('Clips need a SHA-256 digest')
        if clip['sha256'] in clip_hashes or path in clip_paths:
            raise EvidenceError('Cat and dog need distinct source clips')
        clip_hashes.add(clip['sha256'])
        clip_paths.add(path)
        for key in ('device', 'os', 'build', 'asset_digest'):
            if not isinstance(clip.get(key), str) or not clip[key].strip():
                missing.append(f'clips.{species}.{key}')
        if not path.is_file():
            missing.append(f'clip file: {relative}')
        else:
            observed = digest(path)
            if observed != clip['sha256']:
                raise EvidenceError('Clip hash does not match the frozen study input')
            hashes[relative] = observed
    rows = read_csv(ratings_path, COLUMNS)
    responses, orders, respondents = {}, {}, set()
    for row in rows:
        evaluator, species, dimension = row['evaluator_id'], row['species'], row['dimension']
        if evaluator not in evaluators:
            raise EvidenceError('Evaluator is not in the frozen cohort')
        if row['consented_adult'] != 'true':
            raise EvidenceError('Only declared consenting adult evaluators may be analyzed')
        if species not in clips or dimension not in DIMENSIONS or row['clip_id'] != clips[species]['clip_id']:
            raise EvidenceError('Ratings do not match the frozen species/clip/dimension')
        if row['presentation_order'] not in ('1', '2') or row['score'] not in ('', '1', '2', '3', '4', '5'):
            raise EvidenceError('Order must be 1/2 and score 1–5 or blank for abstention')
        key, order_key = (evaluator, species, dimension), (evaluator, species)
        if key in responses:
            raise EvidenceError('Duplicate evaluator/species/dimension response')
        order = int(row['presentation_order'])
        if order_key in orders and orders[order_key] != order:
            raise EvidenceError('Presentation order changes within one evaluator/clip')
        orders[order_key] = order
        responses[key] = int(row['score']) if row['score'] else None
        respondents.add(evaluator)
    if len(evaluators) < 20 or len(respondents) < 20:
        missing.append('at least 20 consenting adult evaluators')
    complete_orders = []
    for evaluator in sorted(evaluators):
        if any((evaluator, s, d) not in responses for s in clips for d in DIMENSIONS):
            missing.append(f'incomplete six-dimension responses: {evaluator}')
        cat_order, dog_order = orders.get((evaluator, 'cat')), orders.get((evaluator, 'dog'))
        if cat_order is not None and dog_order is not None:
            if cat_order == dog_order:
                raise EvidenceError('Each evaluator must see distinct first/second clip positions')
            complete_orders.append(cat_order)
    if abs(complete_orders.count(1) - complete_orders.count(2)) > 1:
        missing.append('balanced cat-first/dog-first order')
    cells = []
    for species in ('cat', 'dog'):
        for dimension in DIMENSIONS:
            values = [responses.get((e, species, dimension)) for e in evaluators]
            favorable = sum(v is not None and v >= 4 for v in values)
            if evaluators and favorable * 5 < 4 * len(evaluators):
                failures.append(f'{species}.{dimension}: fewer than 80% rate at least 4/5')
            cells.append({'species': species, 'dimension': dimension, 'denominator': len(evaluators),
                          'favorable': favorable, 'favorable_fraction': favorable / len(evaluators) if evaluators else None,
                          'scores': {str(i): values.count(i) for i in range(1, 6)},
                          'abstentions': sum(responses.get((e, species, dimension), 'missing') is None for e in evaluators),
                          'missing_responses': sum((e, species, dimension) not in responses for e in evaluators)})
    for relative, expected in hashes.items():
        if digest(folder / relative) != expected:
            raise EvidenceError('Study inputs changed during inspection')
    return {'schema_version': 1, 'status': 'FAIL' if failures else ('PARTIAL' if missing else 'PASS'),
            'scope': 'One clip pair and ratings thresholds only; authenticity, blinding quality, independent motion review and full G-P are not established',
            'presence_gate': 'NOT RUN', 'evaluators': len(evaluators), 'responding_evaluators': len(respondents), 'cat_first': complete_orders.count(1),
            'dog_first': complete_orders.count(2), 'cells': cells, 'failures': failures,
            'missing_evidence': missing, 'evidence_sha256': hashes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        report = inspect_ratings(args.bundle)
        payload = json.dumps(report, indent=2, allow_nan=False) + '\n'
        if args.output:
            with args.output.open('x') as stream:
                stream.write(payload)
        else:
            print(payload, end='')
        return 0 if report['status'] == 'PASS' else 1
    except (OSError, ValueError, TypeError) as error:
        print(f'Evidence error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
