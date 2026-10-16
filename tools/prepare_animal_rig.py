#!/usr/bin/env python3
"""Prepare an inspectable draft quadruped rig in an isolated Blender process."""
import argparse
import json
import math
from pathlib import Path
import sys

try:
    from .generate_animal import digest
except ImportError:
    from generate_animal import digest


def check_fit(mesh, fit, output):
    if Path(output).exists() or not Path(output).parent.is_dir():
        raise ValueError('Choose a new output directory with an existing parent')
    if not isinstance(fit, dict) or type(fit.get('schema_version')) is not int or fit.get('schema_version') != 1 or fit.get('species') not in ('cat', 'dog'):
        raise ValueError('Unsupported quadruped fit')
    if digest(mesh) != fit.get('source_mesh_sha256'):
        raise ValueError('Fit belongs to a different source mesh; review landmarks first')
    if fit.get('metarig') != 'basic_quadruped' or fit.get('blender_version') != '4.5.14':
        raise ValueError('Use the reviewed Blender/metarig configuration')
    if not isinstance(fit.get('template_fit'), dict):
        raise ValueError('Template fit must be an object')
    for key in ('x_scale', 'front_y_scale', 'rear_y_scale', 'z_scale'):
        value = fit.get('template_fit', {}).get(key)
        if type(value) not in (int, float) or not math.isfinite(value) or not 0 < value <= 4:
            raise ValueError(f'Invalid template fit: {key}')
    for key in ('yaw_degrees', 'center_x'):
        value = fit.get(key)
        if type(value) not in (int, float) or not math.isfinite(value) or abs(value) > (180 if key == 'yaw_degrees' else 1):
            raise ValueError(f'Invalid orientation or centering: {key}')
    if type(fit.get('target_triangles')) is not int or fit.get('target_triangles') != 30000:
        raise ValueError('Unsupported draft orientation or polygon budget')

    for key, label in (('neck_chain_points', 'Neck'), ('tail_chain_points', 'Tail')):
        if key not in fit:
            continue
        points = fit[key]
        if not isinstance(points, list) or len(points) != 4:
            raise ValueError(f'{label} fit requires four normalized joint points')
        for point in points:
            if not isinstance(point, list) or len(point) != 3 or any(type(v) not in (int, float) or not math.isfinite(v) for v in point):
                raise ValueError(f'Invalid {label.lower()} joint point')
            if abs(point[0]) > 1 or abs(point[1]) > 2 or not 0 <= point[2] <= 1.25:
                raise ValueError(f'{label} joint outside normalized draft bounds')
        if any(not .01 <= math.dist(a, b) <= .6 for a, b in zip(points, points[1:])):
            raise ValueError(f'Degenerate or excessive {label.lower()} segment')


def unregister_rig_ui(rig, bpy):
    # Rigify executes UI registration outside the addon; addon_disable cannot undo it.
    namespaces = []
    for panel in bpy.types.Panel.__subclasses__():
        namespace = getattr(getattr(panel, 'draw', None), '__globals__', {})
        if namespace.get('rig_id') == rig.data['rig_id'] and all(namespace is not item for item in namespaces):
            namespaces.append(namespace)
    if len(namespaces) != 1 or not callable(namespaces[0].get('unregister')):
        raise ValueError('Cannot identify the generated rig UI for orderly cleanup')
    namespaces[0]['unregister']()


def prepare(mesh_path, fit_path, output):
    fit = json.loads(Path(fit_path).read_text())
    check_fit(mesh_path, fit, output)
    import bpy
    import bmesh
    from mathutils import Vector

    if bpy.app.version_string != '4.5.14 LTS':
        raise ValueError('Run with the pinned Blender 4.5.14 LTS Python module')
    output = Path(output).resolve()
    output.mkdir()
    report = {'status': 'FAIL', 'presence_gate': 'NOT RUN', 'species': fit['species'],
              'source_mesh_sha256': digest(mesh_path), 'fit_sha256': digest(fit_path),
              'limitations': ['Initial template fit, not validated anatomy or motion',
                              'Height normalized to 1.0; physical scale is not established',
                              'No fur, eye materials, gait or contact acceptance']}
    rig = None
    rigify_enabled = False
    try:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(Path(mesh_path).resolve()))
        meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        if len(meshes) != 1:
            raise ValueError('Expected one source mesh')
        mesh = meshes[0]
        bpy.context.view_layer.objects.active = mesh
        mesh.select_set(True)
        mesh.rotation_mode = 'XYZ'
        mesh.rotation_euler.z = math.radians(fit['yaw_degrees'])
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        vertices = [v.co for v in mesh.data.vertices]
        height = max(v.z for v in vertices) - min(v.z for v in vertices)
        if not math.isfinite(height) or height <= 0:
            raise ValueError('Invalid source height')
        bottom = min(v.z for v in vertices)
        for v in mesh.data.vertices:
            v.co = (v.co - Vector((0, 0, bottom))) / height + Vector((fit['center_x'], 0, 0))

        # Remove disconnected extraction debris only in this derived copy.
        bm = bmesh.new()
        bm.from_mesh(mesh.data)
        unseen = set(bm.verts)
        parts = []
        while unseen:
            pending = [unseen.pop()]
            component = set(pending)
            while pending:
                for edge in pending.pop().link_edges:
                    for vertex in edge.verts:
                        if vertex in unseen:
                            unseen.remove(vertex)
                            component.add(vertex)
                            pending.append(vertex)
            parts.append(component)
        keep = max(parts, key=len)
        discarded = set(bm.verts) - keep
        if len(discarded) > len(bm.verts) * .005:
            raise ValueError('Disconnected geometry is too large to treat as extraction debris')
        report['removed_debris_vertices'] = len(discarded)
        bmesh.ops.delete(bm, geom=list(discarded), context='VERTS')
        bm.to_mesh(mesh.data)
        bm.free()
        mesh.name = fit['species'] + '_surface_draft'
        modifier = mesh.modifiers.new('Draft polygon reduction', 'DECIMATE')
        modifier.ratio = min(1, fit['target_triangles'] / len(mesh.data.polygons))
        bpy.ops.object.modifier_apply(modifier=modifier.name)
        for polygon in mesh.data.polygons:
            polygon.use_smooth = True

        bpy.ops.preferences.addon_enable(module='rigify')
        rigify_enabled = True
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.armature_basic_quadruped_metarig_add()
        meta = bpy.context.object
        meta.name = fit['species'] + '_metarig_draft'
        bpy.ops.object.mode_set(mode='EDIT')
        scales = fit['template_fit']
        # Snapshot shared joints before editing; connected endpoints otherwise scale twice.
        rest = {bone.name: (bone.head.copy(), bone.tail.copy()) for bone in meta.data.edit_bones}
        fitted = {}
        for name, points in rest.items():
            transformed = []
            for point in points:
                point.x *= scales['x_scale']
                point.y *= scales['front_y_scale'] if point.y < 0 else scales['rear_y_scale']
                point.z *= scales['z_scale']
                transformed.append(point)
            fitted[name] = transformed
        for key, names in (('neck_chain_points', ('spine.008', 'spine.009', 'spine.010', 'spine.011')),
                           ('tail_chain_points', ('spine.003', 'spine.002', 'spine.001', 'spine'))):
            if key not in fit:
                continue
            anchor = fitted[names[0]][0]
            for name, point in zip(names, fit[key]):
                target = Vector(point)
                if not .01 <= (target - anchor).length <= .6:
                    raise ValueError('Joint segment does not fit its chain anchor')
                fitted[name] = [anchor, target]
                anchor = target
        for name, (head, tail) in fitted.items():
            meta.data.edit_bones[name].head, meta.data.edit_bones[name].tail = head, tail
        for name, (head, tail) in fitted.items():
            bone = meta.data.edit_bones[name]
            if (bone.head - head).length > 1e-6 or (bone.tail - tail).length > 1e-6:
                raise ValueError('Connected metarig joints changed during fitting')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.pose.rigify_generate()
        rig = meta.data.rigify_target_rig
        if rig is None:
            raise ValueError('Rigify produced no target armature')
        bpy.ops.object.select_all(action='DESELECT')
        rig.select_set(True)
        mesh.select_set(True)
        bpy.context.view_layer.objects.active = rig
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        bpy.context.view_layer.objects.active = mesh
        bpy.ops.object.vertex_group_limit_total(group_select_mode='BONE_DEFORM', limit=4)
        bpy.ops.object.vertex_group_normalize_all(group_select_mode='BONE_DEFORM', lock_active=False)
        deform = {b.name for b in rig.data.bones if b.use_deform}
        group_ids = {g.index for g in mesh.vertex_groups if g.name in deform}
        unweighted = sum(not any(g.group in group_ids and g.weight > 0 for g in v.groups)
                         for v in mesh.data.vertices)
        report.update(vertices=len(mesh.data.vertices), polygons=len(mesh.data.polygons),
                      rig_bones=len(rig.data.bones), deform_bones=len(deform),
                      unweighted_vertices=unweighted)
        if unweighted:
            raise ValueError(f'Automatic skinning left {unweighted} vertices unweighted')
        if any(sum(g.group in group_ids and g.weight > 0 for g in v.groups) > 4 or
               abs(sum(g.weight for g in v.groups if g.group in group_ids) - 1) > 1e-5
               for v in mesh.data.vertices):
            raise ValueError('Skin weights must be normalized with at most four joint influences')
        report['max_joint_influences'] = max(sum(g.group in group_ids and g.weight > 0 for g in v.groups)
                                             for v in mesh.data.vertices)
        report['controls'] = [b.name for b in rig.pose.bones if not b.name.startswith(('ORG-', 'MCH-', 'DEF-'))]
        bpy.ops.object.select_all(action='DESELECT')
        mesh.select_set(True)
        rig.select_set(True)
        bpy.ops.wm.save_as_mainfile(filepath=str(output / 'rig-draft.blend'))
        bpy.ops.export_scene.gltf(filepath=str(output / 'rig-draft.glb'), export_format='GLB',
                                  use_selection=True, export_animations=False, export_def_bones=True)
        bpy.ops.export_scene.fbx(filepath=str(output / 'rig-draft.fbx'), use_selection=True,
                                use_armature_deform_only=True, add_leaf_bones=False, bake_anim=False)
        report.update(status='PARTIAL', rig_glb_sha256=digest(output / 'rig-draft.glb'))
        return report
    except Exception as error:
        report['error'] = str(error)
        raise
    finally:
        try:
            if rig is not None:
                unregister_rig_ui(rig, bpy)
            if rigify_enabled:
                bpy.ops.preferences.addon_disable(module='rigify')
            report['rigify_cleanup'] = 'complete'
        except Exception as error:
            report.update(status='FAIL', cleanup_error=str(error))
            raise
        finally:
            with (output / 'rig-preparation.json').open('x') as stream:
                json.dump(report, stream, indent=2, allow_nan=False)
                stream.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh', type=Path, required=True)
    parser.add_argument('--fit', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        prepare(args.mesh, args.fit, args.output)
        return 0
    except Exception as error:
        print(f'Rig preparation failed: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
