import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

from tools.prepare_animal_rig import check_fit


class RigFitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.mesh = self.root / 'mesh.glb'
        self.mesh.write_bytes(b'synthetic guard fixture, not a GLB')
        self.output = self.root / 'new-rig'
        self.fit = {'schema_version': 1, 'species': 'cat', 'source_mesh_sha256': hashlib.sha256(self.mesh.read_bytes()).hexdigest(),
                    'metarig': 'basic_quadruped', 'blender_version': '4.5.14', 'yaw_degrees': 25, 'center_x': .144,
                    'target_triangles': 30000, 'template_fit': {'x_scale': 2.2, 'front_y_scale': .9, 'rear_y_scale': .55, 'z_scale': .82}}

    def test_valid_guard_creates_no_output(self):
        check_fit(self.mesh, self.fit, self.output)
        self.assertFalse(self.output.exists())

    def test_existing_output_or_missing_parent_rejected(self):
        self.output.mkdir()
        with self.assertRaises(ValueError): check_fit(self.mesh, self.fit, self.output)
        self.assertEqual(list(self.output.iterdir()), [])
        with self.assertRaises(ValueError): check_fit(self.mesh, self.fit, self.root / 'absent' / 'out')

    def test_different_source_mesh_rejected(self):
        self.mesh.write_bytes(b'different asset')
        with self.assertRaises(ValueError): check_fit(self.mesh, self.fit, self.output)

    def test_malformed_or_wrong_species_template_version_rejected(self):
        with self.assertRaises(ValueError): check_fit(self.mesh, [], self.output)
        for key, value in [('schema_version', True), ('species', 'wolf'), ('metarig', 'human'), ('blender_version', 'other'), ('template_fit', [])]:
            with self.subTest(key=key):
                fit = dict(self.fit, **{key: value})
                with self.assertRaises(ValueError): check_fit(self.mesh, fit, self.output)

    def test_invalid_scale_cannot_reach_blender(self):
        for value in (0, -1, 5, float('nan'), float('inf'), True, '1'):
            with self.subTest(value=value):
                fit = copy.deepcopy(self.fit)
                fit['template_fit']['z_scale'] = value
                with self.assertRaises(ValueError): check_fit(self.mesh, fit, self.output)

    def test_unsupported_orientation_or_budget_rejected(self):
        for key, value in [('yaw_degrees', False), ('yaw_degrees', 181), ('center_x', float('nan')), ('center_x', True), ('target_triangles', 30000.), ('target_triangles', 1000000)]:
            with self.subTest(key=key, value=value):
                fit = dict(self.fit, **{key: value})
                with self.assertRaises(ValueError): check_fit(self.mesh, fit, self.output)


if __name__ == '__main__':
    unittest.main()
