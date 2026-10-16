import copy
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.benchmark import EvidenceError
from tools.presence_ratings import COLUMNS, DIMENSIONS, inspect_ratings


class RatingsTests(unittest.TestCase):
    # Fixture declarations are synthetic and never establish a real study or gate.
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = {'schema_version': 1, 'protocol_revision': 'fixture-v1', 'operator': 'fixture',
                         'blinding_reference': 'synthetic fixture', 'consent_reference': 'synthetic fixture',
                         'evidence_kind': 'physical_device', 'scene_content': 'animal_presence',
                         'evaluator_ids': [f'E{i:02}' for i in range(20)], 'clips': {}}
        self.rows = []
        for species in ('cat', 'dog'):
            path = self.root / (species + '.mp4')
            path.write_bytes(('synthetic parser fixture, not video: ' + species).encode())
            self.manifest['clips'][species] = dict(clip_id=species+'-fixture', file=path.name,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(), device='fixture', os='fixture', build='fixture', asset_digest='fixture')
        for i, evaluator in enumerate(self.manifest['evaluator_ids']):
            for species in ('cat', 'dog'):
                order = (1 if i % 2 == 0 else 2) if species == 'cat' else (2 if i % 2 == 0 else 1)
                for dimension in DIMENSIONS:
                    self.rows.append(dict(zip(COLUMNS, [evaluator, 'true', species, species+'-fixture', str(order), dimension, '4' if i<16 else '2'])))

    def write(self):
        (self.root / 'manifest.json').write_text(json.dumps(self.manifest))
        with (self.root / 'ratings.csv').open('w', newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=COLUMNS);writer.writeheader();writer.writerows(self.rows)

    def inspect(self):
        self.write()
        return inspect_ratings(self.root)

    def test_exact_80_percent_per_cell_without_granting_presence(self):
        r=self.inspect()
        self.assertEqual(r['status'],'PASS')
        self.assertEqual(r['presence_gate'],'NOT RUN')
        self.assertEqual((r['cat_first'],r['dog_first']),(10,10))
        self.assertTrue(all(c['favorable']==16 and c['denominator']==20 and c['scores']['2']==4 for c in r['cells']))

    def test_one_failed_dimension_cannot_be_pooled_away(self):
        row=next(r for r in self.rows if r['evaluator_id']=='E15' and r['species']=='dog' and r['dimension']=='natural_motion')
        row['score']='3'
        r=self.inspect()
        self.assertEqual(r['status'],'FAIL')
        self.assertEqual(len(r['failures']),1)
        self.assertIn('dog.natural_motion',r['failures'][0])

    def test_absent_unfavorable_evaluators_stay_in_denominator(self):
        self.rows=[r for r in self.rows if r['evaluator_id']!='E19']
        r=self.inspect()
        self.assertEqual((r['evaluators'],r['responding_evaluators']),(20,19))
        self.assertEqual(r['status'],'PARTIAL')
        self.assertTrue(all(c['denominator']==20 and c['missing_responses']==1 for c in r['cells']))

    def test_abstentions_are_not_removed_or_imputed(self):
        for row in self.rows:
            if row['evaluator_id']=='E15':row['score']=''
        r=self.inspect()
        self.assertEqual(r['status'],'FAIL')
        self.assertTrue(all(c['favorable']==15 and c['abstentions']==1 and c['denominator']==20 for c in r['cells']))

    def test_undersized_or_unbalanced_study_is_partial(self):
        original_manifest, original_rows = copy.deepcopy(self.manifest), copy.deepcopy(self.rows)
        self.manifest['evaluator_ids']=self.manifest['evaluator_ids'][:-1]
        self.rows=[r for r in self.rows if r['evaluator_id']!='E19']
        self.assertEqual(self.inspect()['status'],'PARTIAL')
        self.manifest, self.rows = original_manifest, original_rows
        for row in self.rows:row['presentation_order']='1' if row['species']=='cat' else '2'
        self.assertEqual(self.inspect()['status'],'PARTIAL')

    def test_diagnostic_or_missing_provenance_cannot_pass(self):
        self.manifest.update(evidence_kind='desktop',scene_content='instrumentation_only',blinding_reference='')
        self.assertEqual(self.inspect()['status'],'PARTIAL')
        self.manifest['evidence_kind']='physical_device';self.manifest['scene_content']='animal_presence'
        self.manifest['blinding_reference']='fixture'
        (self.root/'cat.mp4').unlink()
        self.assertEqual(self.inspect()['status'],'PARTIAL')

    def test_duplicates_and_invalid_rows_rejected(self):
        original=copy.deepcopy(self.rows)
        self.rows.append(dict(self.rows[0]))
        with self.assertRaises(EvidenceError):self.inspect()
        for field,value in [('consented_adult','false'),('score','4.0'),('score','6'),('score','True'),
                            ('species','wolf'),('dimension','pooled'),('clip_id','wrong'),('evaluator_id','unknown')]:
            self.rows=copy.deepcopy(original);self.rows[0][field]=value
            with self.subTest(field=field,value=value):
                with self.assertRaises(EvidenceError):self.inspect()
        self.rows=copy.deepcopy(original)
        for r in self.rows:
            if r['evaluator_id']=='E00':r['presentation_order']='1'
        with self.assertRaises(EvidenceError):self.inspect()

    def test_hash_path_and_reused_clip_guards(self):
        original=copy.deepcopy(self.manifest)
        for change in [{'file':'../escape.mp4'},{'file':str(self.root/'cat.mp4')},{'sha256':'0'*64},
                       {'file':'cat.mp4','sha256':self.manifest['clips']['cat']['sha256']}]:
            self.manifest=copy.deepcopy(original);self.manifest['clips']['dog'].update(change)
            with self.subTest(change=change):
                with self.assertRaises(EvidenceError):self.inspect()

    def test_malformed_cohort_schema_and_csv_rejected(self):
        original=copy.deepcopy(self.manifest)
        for change in [{'schema_version':True},{'evaluator_ids':['duplicate','duplicate']},{'clips':{}},{'evaluator_ids':['name@example.com']}]:
            self.manifest=copy.deepcopy(original);self.manifest.update(change)
            with self.subTest(change=change):
                with self.assertRaises(EvidenceError):self.inspect()
        self.manifest=original;self.write();(self.root/'ratings.csv').write_text('wrong,columns\n1,2\n')
        with self.assertRaises(EvidenceError):inspect_ratings(self.root)

    def test_cli_never_overwrites_report(self):
        self.write();output=self.root/'report.json';output.write_text('preserved')
        result=subprocess.run([sys.executable,'tools/presence_ratings.py',str(self.root),'--output',str(output)],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(output.read_text(),'preserved')


if __name__=='__main__':unittest.main()
