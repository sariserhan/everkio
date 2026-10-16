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

    def test_reviewed_neck_chain_guard(self):
        points = [[.035, -.35, .79], [.055, -.4, .82], [.08, -.45, .85], [.2, -.58, .85]]
        check_fit(self.mesh, dict(self.fit, neck_chain_points=points), self.output)
        for invalid in (None, [], points[:3], [[0, 0]] * 4,
                        [[True, 0, .8]] * 4, [[0, float('nan'), .8]] * 4,
                        [[2, 0, .8]] * 4, [[0, 0, -1]] * 4,
                        [[0, 0, .8]] * 4, [[0, -2, .8], [0, 1, .8], *points[:2]]):
            with self.subTest(points=invalid):
                with self.assertRaises(ValueError):
                    check_fit(self.mesh, dict(self.fit, neck_chain_points=invalid), self.output)
        self.assertFalse(self.output.exists())
    def test_tail_chain_rejects_degenerate_or_out_of_bounds_fits(self):
        points = [[.015, .51, .58], [.09, .59, .39], [.19, .64, .29], [.285, .66, .26]]
        check_fit(self.mesh, dict(self.fit, tail_chain_points=points), self.output)
        for invalid in (None, points[:3], [[0, 0, .5]] * 4,
                        [[0, float('inf'), .5], *points[1:]],
                        [[0, 0, 2], *points[1:]]):
            with self.subTest(points=invalid):
                with self.assertRaises(ValueError):
                    check_fit(self.mesh, dict(self.fit, tail_chain_points=invalid), self.output)
        self.assertFalse(self.output.exists())


class RigUICleanupTests(unittest.TestCase):
    def fake_bpy(self, namespaces):
        from types import FunctionType, SimpleNamespace
        panels = []
        for namespace in namespaces:
            draw = FunctionType((lambda: None).__code__, namespace)
            panels.append(type('GeneratedPanel', (), {'draw': draw}))
        return SimpleNamespace(types=SimpleNamespace(Panel=SimpleNamespace(__subclasses__=lambda: panels)))

    def test_unregisters_matching_generated_namespace_once(self):
        from types import SimpleNamespace
        from tools.prepare_animal_rig import unregister_rig_ui
        calls = []
        match = {'rig_id': 'owned-rig', 'unregister': lambda: calls.append('owned')}
        other = {'rig_id': 'other-rig', 'unregister': lambda: calls.append('other')}
        unregister_rig_ui(SimpleNamespace(data={'rig_id': 'owned-rig'}), self.fake_bpy([other, match, match]))
        self.assertEqual(calls, ['owned'])

    def test_ambiguous_or_missing_registration_rejected_before_cleanup(self):
        from types import SimpleNamespace
        from tools.prepare_animal_rig import unregister_rig_ui
        calls = []
        same_callback = lambda: calls.append('ambiguous')
        for namespaces in [[], [{'rig_id': 'owned-rig'}],
                           [{'rig_id': 'owned-rig', 'unregister': same_callback},
                            {'rig_id': 'owned-rig', 'unregister': same_callback}],
                           [{'rig_id': 'owned-rig', 'unregister': lambda: calls.append(1)},
                            {'rig_id': 'owned-rig', 'unregister': lambda: calls.append(2)}]]:
            with self.subTest(namespaces=namespaces):
                with self.assertRaises(ValueError):
                    unregister_rig_ui(SimpleNamespace(data={'rig_id': 'owned-rig'}), self.fake_bpy(namespaces))
                self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main()
