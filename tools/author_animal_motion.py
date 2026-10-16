#!/usr/bin/env python3
"""Author a bounded start/walk/stop draft on the reviewed quadruped rigs."""
import argparse
import csv
import json
import math
from pathlib import Path
import sys

try:
    from .generate_animal import digest
except ImportError:
    from generate_animal import digest


# shortcut: fixed normalized draft gait; replace with anatomy-reviewed clips before product use.
CONTROLS = {'foot_ik.L': (0, 'DEF-toe.L'),
            'front_foot_ik.L': (.25, 'DEF-front_toe.L'),
            'foot_ik.R': (.5, 'DEF-toe.R'),
            'front_foot_ik.R': (.75, 'DEF-front_toe.R')}
FPS = 30
LAST_FRAME = 181


def trajectory(seconds, offset):
    """Three discrete steps, with all feet stationary at both ends of the clip."""
    travel, lift, planted, stance = 0., 0., True, 0
    for step in range(3):
        u = (seconds - (1 + offset + step)) / .35
        if u >= 1:
            travel += .35
            stance += 1
        elif u > 0:
            travel += .35 * u ** 3 * (10 - 15 * u + 6 * u ** 2)
            lift = .065 * math.sin(math.pi * u) ** 2
            planted = False
    return travel, lift, planted, stance


def author(source, source_sha256, species, output):
    source, output = Path(source).resolve(), Path(output).absolute()
    if species not in ('cat', 'dog') or digest(source) != source_sha256:
        raise ValueError('Species or source hash does not match the reviewed draft')
    if output.exists() or not output.parent.is_dir():
        raise ValueError('Choose a new output directory with an existing parent')
    import bpy
    from mathutils import Vector
    if bpy.app.version_string != '4.5.14 LTS':
        raise ValueError('Use the pinned Blender 4.5.14 LTS module')
    output.mkdir()
    report = {'status': 'FAIL', 'presence_gate': 'NOT RUN', 'species': species,
              'source_sha256': source_sha256, 'fps': FPS, 'frames': LAST_FRAME,
              'limitations': ['Normalized scale, not physical animal size',
                              'Weight-selected paw proxies, not anatomical contact validation',
                              'Authored start/walk/stop candidate, not accepted natural motion',
                              'No AR, fur/eye repair or device evidence']}
    try:
        bpy.ops.wm.open_mainfile(filepath=str(source), use_scripts=False)
        scene = bpy.context.scene
        matches = [o for o in scene.objects if o.type == 'MESH' and o.name == species + '_surface_draft']
        if len(matches) != 1 or matches[0].parent is None or matches[0].parent.type != 'ARMATURE':
            raise ValueError('Expected the reviewed single surface and authoring armature')
        mesh, rig = matches[0], matches[0].parent
        for bone in rig.data.bones:
            bone.bbone_segments = 1
        if any(name not in rig.pose.bones for name in ('root', *CONTROLS)):
            raise ValueError('Missing reviewed rig controls')
        if rig.animation_data and (rig.animation_data.action or rig.animation_data.nla_tracks):
            raise ValueError('Source must be an unanimated painted draft')
        rest = {name: rig.pose.bones[name].matrix.copy() for name in ('root', *CONTROLS)}
        ids = {g.name: g.index for g in mesh.vertex_groups}
        points, correction = {}, {}
        for name, (_, group) in CONTROLS.items():
            vertices = [v for v in mesh.data.vertices if any(g.group == ids[group] and g.weight > .35 for g in v.groups)]
            if len(vertices) < 8:
                raise ValueError('Insufficient sole proxy vertices')
            cutoff = sorted(v.co.z for v in vertices)[len(vertices) // 8]
            points[name] = [v.index for v in vertices if v.co.z <= cutoff]
            correction[name] = .002 - min(mesh.data.vertices[i].co.z for i in points[name])
        scene.render.fps = FPS
        scene.frame_start, scene.frame_end = 1, LAST_FRAME
        rig.animation_data_create()
        rig.animation_data.action = bpy.data.actions.new('DRAFT_start_walk_stop_NOT_ACCEPTED')
        contact_passes = []
        for contact_pass in range(2):
            rows, targets, root_positions, hold_positions = [], {}, [], {}
            hold_errors = []
            for frame in range(1, LAST_FRAME + 1):
                seconds = (frame - 1) / FPS
                scene.frame_set(frame)
                paths = {name: trajectory(seconds, phase) for name, (phase, _) in CONTROLS.items()}
                distance = sum(p[0] for p in paths.values()) / len(paths)
                matrix = rest['root'].copy()
                matrix.translation += Vector((0, -distance, 0))
                rig.pose.bones['root'].matrix = matrix
                rig.pose.bones['root'].keyframe_insert('location', frame=frame)
                root_positions.append(tuple(matrix.translation))
                rig.update_tag(refresh={'OBJECT'})
                bpy.context.view_layer.update()
                for name, (travel, height, planted, stance) in paths.items():
                    matrix = rest[name].copy()
                    matrix.translation += Vector((0, -travel, height + correction[name]))
                    bone = rig.pose.bones[name]
                    bone.matrix = matrix
                    for key in ('location', 'rotation_quaternion'):
                        bone.keyframe_insert(key, frame=frame)
                    if planted:
                        previous = targets.setdefault((name, stance), matrix.translation.copy())
                        if (previous - matrix.translation).length > 1e-8:
                            raise ValueError('Planted controller moved')
                rig.update_tag(refresh={'OBJECT'})
                bpy.context.view_layer.update()
                evaluated = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
                positions = [evaluated.matrix_world @ v.co for v in evaluated.data.vertices]
                if frame <= FPS or frame > LAST_FRAME - FPS:
                    hold = 'start' if frame <= FPS else 'end'
                    reference = hold_positions.setdefault(hold, [v.copy() for v in positions])
                    hold_errors.append(max((v - initial).length for v, initial in zip(positions, reference)))
                if not all(math.isfinite(c) for v in positions for c in v):
                    raise ValueError('Nonfinite deformed geometry')
                for name, (_, _, planted, stance) in paths.items():
                    sole = [positions[i] for i in points[name]]
                    center = sum(sole, Vector()) / len(sole)
                    rows.append(dict(frame=frame, seconds=seconds, foot=name, planted=planted,
                                     stance=stance, x=center.x, y=center.y,
                                     min_z=min(v.z for v in sole), mesh_min_z=min(v.z for v in positions)))
            minima = {name: min(r['min_z'] for r in rows if r['foot'] == name) for name in CONTROLS}
            contact_passes.append({'pass': contact_pass + 1, 'sole_proxy_minima': minima,
                                   'mesh_min_z': min(r['mesh_min_z'] for r in rows)})
            if contact_pass == 0:
                # Constant per-foot correction preserves fixed stance controller targets.
                for name, minimum in minima.items():
                    if minimum < 0:
                        correction[name] += .002 - minimum
        stances = {}
        for row in rows:
            if row['planted']:
                stances.setdefault((row['foot'], row['stance']), []).append(row)
        drift = max(math.hypot(row['x'] - samples[0]['x'], row['y'] - samples[0]['y'])
                    for samples in stances.values() for row in samples)
        if root_positions[:FPS] != [root_positions[0]] * FPS or root_positions[-FPS:] != [root_positions[-1]] * FPS:
            raise ValueError('Start/end stationary hold failed')
        if max(hold_errors) > 1e-6:
            raise ValueError('Deformed surface moved during a stationary hold')
        penetration = max(0, -min(r['mesh_min_z'] for r in rows))
        scene.frame_set(1)
        bpy.ops.wm.save_as_mainfile(filepath=str(output / 'motion-candidate.blend'))
        with (output / 'paw-observations.csv').open('x') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        report.update(status='PARTIAL', controller_stance_check='PASS', stationary_holds_check='PASS',
                      motion_sha256=digest(output / 'motion-candidate.blend'),
                      body_travel_normalized=root_positions[0][1] - root_positions[-1][1],
                      constant_floor_corrections=correction, contact_passes=contact_passes,
                      worst_stance_xy_drift=drift,
                      stationary_surface_max_error=max(hold_errors),
                      sampled_floor_check='PASS' if penetration <= 1e-5 else 'FAIL',
                      worst_floor_penetration=penetration)
        return report
    except Exception as error:
        report['error'] = str(error)
        raise
    finally:
        with (output / 'motion-review.json').open('x') as stream:
            json.dump(report, stream, indent=2, allow_nan=False)
            stream.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--source-sha256', required=True)
    parser.add_argument('--species', choices=('cat', 'dog'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        author(args.source, args.source_sha256, args.species, args.output)
        return 0
    except Exception as error:
        print(f'Motion preparation failed: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
