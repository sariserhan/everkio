from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from tools.benchmark import EvidenceError
from tools.metal_trace import inspect_trace


class MetalTraceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'export.xml'
        self.root = ET.fromstring('''<trace-query-result><node>
          <schema name="displayed-surfaces-interval">
            <col><mnemonic>start</mnemonic><engineering-type>start-time</engineering-type></col>
            <col><mnemonic>event-label</mnemonic><engineering-type>narrative</engineering-type></col>
            <col><mnemonic>display-name</mnemonic><engineering-type>display-name</engineering-type></col>
          </schema>
          <row><start-time>1000000</start-time><narrative id="label"><process id="app"><pid>42</pid></process></narrative><display-name id="display">Built-In Display</display-name></row>
          <row><start-time>21000000</start-time><narrative><process ref="app"/></narrative><display-name ref="display"/></row>
          <row><start-time>61000000</start-time><narrative ref="label"/><display-name ref="display"/></row>
          <row><start-time>62000000</start-time><narrative><process><pid>99</pid></process></narrative><display-name ref="display"/></row>
          <row><start-time>63000000</start-time><narrative>Surface only</narrative><display-name ref="display"/></row>
        </node></trace-query-result>''')
        self.node = self.root.find('node')

    def inspect(self):
        ET.ElementTree(self.root).write(self.path)
        return inspect_trace(self.path, 42)

    def test_resolves_references_and_filters_application(self):
        report = self.inspect()
        self.assertEqual(report['attributed_swaps'], 3)
        self.assertEqual(report['other_or_unattributed_rows'], 2)
        self.assertEqual(report['swap_interval_p95_ms'], 40)
        self.assertEqual(report['swap_span_seconds'], .06)
        self.assertEqual(report['status'], 'PARTIAL')
        self.assertEqual(report['presence_gate'], 'NOT RUN')
        self.assertNotIn('touch_p95_ms', report)

    def test_unresolved_and_cyclic_references_rejected(self):
        field = self.node.findall('row')[1][1][0]
        for ref in ('missing', 'cycle'):
            with self.subTest(ref=ref):
                field.set('ref', ref)
                field.set('id', 'cycle')
                with self.assertRaises(EvidenceError): self.inspect()

    def test_duplicate_ids_rejected(self):
        self.node.findall('row')[1][0].set('id', 'display')
        with self.assertRaises(EvidenceError): self.inspect()

    def test_reordered_or_duplicate_swaps_rejected(self):
        for timestamp in ('1000000', '0', '-1', 'nan'):
            with self.subTest(timestamp=timestamp):
                self.node.findall('row')[1][0].text = timestamp
                with self.assertRaises(EvidenceError): self.inspect()

    def test_multiple_displays_or_processes_rejected(self):
        row = self.node.findall('row')[1]
        row[2].attrib.clear()
        row[2].text = 'Second Display'
        with self.assertRaises(EvidenceError): self.inspect()
        row[2].set('ref', 'display')
        process = ET.SubElement(row[1], 'process')
        ET.SubElement(process, 'pid').text = '99'
        with self.assertRaises(EvidenceError): self.inspect()

    def test_wrong_schema_row_shape_and_units_rejected(self):
        schema = self.node.find('schema')
        schema.set('name', 'ca-client-present-request')
        with self.assertRaises(EvidenceError): self.inspect()
        schema.set('name', 'displayed-surfaces-interval')
        schema.find('col/engineering-type').text = 'duration'
        with self.assertRaises(EvidenceError): self.inspect()
        schema.find('col/engineering-type').text = 'start-time'
        self.node.findall('row')[0].remove(self.node.findall('row')[0][0])
        with self.assertRaises(EvidenceError): self.inspect()

    def test_no_matching_application_cannot_produce_metrics(self):
        self.inspect()
        for pid in (99, 111, 0, True):
            with self.subTest(pid=pid):
                with self.assertRaises(EvidenceError): inspect_trace(self.path, pid)

    def test_cli_partial_and_overwrite_protection(self):
        self.inspect()
        output = Path(self.tmp.name) / 'report.json'
        command = [sys.executable, 'tools/metal_trace.py', str(self.path), '--pid', '42', '--output', str(output)]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
        original = output.read_bytes()
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(output.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
