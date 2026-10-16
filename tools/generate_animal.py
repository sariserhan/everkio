#!/usr/bin/env python3
"""Local CPU generation of generic evaluation meshes. No animal/AR gate granted."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

SOURCE_REVISION = '107cefdc244c39106fa830359024f6a2f1c78871'
WEIGHT_SHA256 = '429e2c6b22a0923967459de24d67f05962b235f79cde6b032aa7ed2ffcd970ee'
CONFIG_SHA256 = '74ca708ce086bf68e97709ea6b3d91f14717921c04691e84043f0eb8fcc68e62'
DINO_CONFIG_SHA256 = 'b87c0270b97db085fd82cf114a761fd0f62ae7914fbd407c752a2260646b689c'


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def check_inputs(source, weights, image, output):
    source, weights, image, output = map(Path, (source, weights, image, output))
    if output.exists():
        raise ValueError('Choose a new output directory; evidence is never overwritten')
    if not output.parent.is_dir():
        raise ValueError('Output parent must exist')
    for path in (source / 'tsr/system.py', weights / 'config.yaml', weights / 'model.ckpt', image):
        if not path.is_file():
            raise ValueError(f'Missing input: {path}')
    revision = subprocess.run(['git', '-C', str(source), 'rev-parse', 'HEAD'],
                              check=True, capture_output=True, text=True).stdout.strip()
    changes = subprocess.run(['git', '-C', str(source), 'status', '--porcelain'],
                             check=True, capture_output=True, text=True).stdout.strip()
    if revision != SOURCE_REVISION or changes:
        raise ValueError('Use the pinned, unmodified TripoSR source revision')
    if digest(weights / 'model.ckpt') != WEIGHT_SHA256:
        raise ValueError('Model checksum differs from the verified official weights')
    if digest(weights / 'config.yaml') != CONFIG_SHA256:
        raise ValueError('Model configuration differs from the reviewed official configuration')


def generate(source, weights, image, output, species):
    check_inputs(source, weights, image, output)
    # Force cached configuration reads; never dispatch to hosted inference.
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TRANSFORMERS_OFFLINE'] = '1'
    sys.path.insert(0, str(Path(source).resolve()))
    import numpy as np
    import torch
    from huggingface_hub import hf_hub_download
    from PIL import Image
    from tsr.system import TSR
    from tsr.utils import resize_foreground

    cached_config = hf_hub_download('facebook/dino-vitb16', 'config.json', local_files_only=True)
    if digest(cached_config) != DINO_CONFIG_SHA256:
        raise ValueError('Cached DINO configuration differs from the verified configuration')
    original = Image.open(image)
    if original.mode != 'RGBA' or original.getchannel('A').getextrema() != (0, 255):
        raise ValueError('Use a nonempty RGBA reference with a transparent background')
    torch.set_num_threads(4)
    torch.manual_seed(0)
    output = Path(output)
    output.mkdir()
    report = {
        'schema_version': 1, 'species': species, 'scene_content': 'generic_ai_asset_evaluation',
        'status': 'FAIL', 'presence_gate': 'NOT RUN', 'source_revision': SOURCE_REVISION,
        'model_sha256': WEIGHT_SHA256, 'config_sha256': digest(Path(weights) / 'config.yaml'),
        'dino_config_sha256': DINO_CONFIG_SHA256,
        'reference_sha256': digest(image), 'device': 'cpu', 'threads': 4, 'seed': 0,
        'marching_cubes_resolution': 256, 'query_chunk_size': 4096,
        'remote_inference_calls': 0,
        'limitations': ['Static vertex-coloured mesh; no rig, animation, fur shader or mobile LODs',
                        'Unseen anatomy and coat are inferred; no specific-pet identity claim',
                        'Not a realism, motion, AR or performance acceptance result'],
    }
    start = time.monotonic()
    try:
        print('Loading verified local TripoSR model on CPU', flush=True)
        model = TSR.from_pretrained(str(weights), config_name='config.yaml', weight_name='model.ckpt')
        model.eval()
        model.renderer.set_chunk_size(4096)
        rgba = np.asarray(resize_foreground(original, .85), dtype=np.float32) / 255
        rgb = rgba[:, :, :3] * rgba[:, :, 3:4] + .5 * (1 - rgba[:, :, 3:4])
        prepared = Image.fromarray((rgb * 255).astype(np.uint8))
        prepared.save(output / 'model-input.png')
        print('Inferring generic animal shape and appearance', flush=True)
        with torch.inference_mode():
            codes = model([prepared], device='cpu')
            print('Extracting mesh at resolution 256', flush=True)
            mesh = model.extract_mesh(codes, True, resolution=256)[0]
        if not len(mesh.vertices) or not len(mesh.faces) or not np.isfinite(mesh.vertices).all():
            raise ValueError('Model produced an empty or invalid mesh')
        mesh.export(output / 'mesh.glb')
        mesh.export(output / 'mesh.obj')
        report.update(status='PARTIAL', vertices=len(mesh.vertices), triangles=len(mesh.faces),
                      bounds=mesh.bounds.tolist(), watertight=bool(mesh.is_watertight),
                      mesh_sha256=digest(output / 'mesh.glb'))
        print('Static evaluation mesh saved; rig/motion/realism NOT RUN', flush=True)
        return report
    except Exception as error:
        report['error'] = str(error)
        raise
    finally:
        report['elapsed_seconds'] = time.monotonic() - start
        with (output / 'generation.json').open('x') as stream:
            json.dump(report, stream, indent=2, allow_nan=False)
            stream.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--weights', type=Path, required=True)
    parser.add_argument('--image', type=Path, required=True)
    parser.add_argument('--species', choices=('cat', 'dog'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        generate(args.source, args.weights, args.image, args.output, args.species)
        return 0  # Generation completed; generation.json still leaves acceptance PARTIAL.
    except Exception as error:
        print(f'Generation failed: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
