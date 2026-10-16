# Local AI animal generation — first evaluation

Date: October 15, 2026. Scope: original generic cat/dog art preparation within M0–M3, following owner decision D13. This is not reconstruction of an actual pet, a funded R-track experiment or production M5 implementation. No stock asset purchase, paid API account, cloud GPU or remote inference endpoint was used.

**Actual result: local reference → AI shape/appearance → GLB/OBJ export works for both animals. Asset quality remains insufficient. No rig, animation, PBR/fur materials, physical scale or mobile LODs are delivered. No animal was imported into the diagnostic app.**

## Inputs and provenance

The built-in imagegen tool generated an original adult tabby cat and yellow Labrador reference. Saved PNGs, exact prompts, tool provenance and SHA-256 hashes are under [`assets/ai-reference`](../assets/ai-reference/manifest.json). The underlying image-model version was not exposed. No customer photo or third-party reference image was supplied. These are synthetic animal references, not proof of animal presence.

[OpenAI's published output terms](https://openai.com/policies/terms-of-use/#content) describe output ownership between the user and OpenAI, subject to applicable law, and explain that outputs may be similar to others. This records a source for the references; it does not assert exclusive copyright or a blanket clearance guarantee. No stock-pack license is needed for this path.

Selected first local model: [official TripoSR source](https://github.com/VAST-AI-Research/TripoSR) at `107cefdc244c39106fa830359024f6a2f1c78871`. Its README explicitly includes pretrained weights in its MIT release; copyright/permission notice is retained in [`third_party/TripoSR-LICENSE.txt`](../third_party/TripoSR-LICENSE.txt). [Official model repository](https://huggingface.co/stabilityai/TripoSR) revision `5b521936b01fbe1890f6f9baed0254ab6351c04a` was public/ungated when downloaded. Model is 1,677,246,742 bytes, SHA-256 `429e2c6b22a0923967459de24d67f05962b235f79cde6b032aa7ed2ffcd970ee`. Reviewed config SHA-256 `74ca708ce086bf68e97709ea6b3d91f14717921c04691e84043f0eb8fcc68e62`.

CPU surface extraction uses [torchmcubes](https://github.com/tatsy/torchmcubes) revision `879926d0ef58e6ce0ac2630fdecb5e53af7ed3ff`, whose current source declares MPL-2.0. It is a local build dependency, not code added to the iPhone app. Model/dependency licenses remain separate from reference/output provenance. Third-party software/source notices are retained in the private checkout/environment and evidence archive.

Alternatives reviewed: [Stable Fast 3D](https://github.com/Stability-AI/stable-fast-3d) has a gated model and recommends CPU below 32 GB unified memory; it was not downloaded or run. [Hunyuan3D-Swift](https://github.com/ZimengXiong/Hunyuan3D-Swift) reports a small local shape path but much higher full texture-pipeline memory than this 16 GB Mac; no model or code from it was executed. Their public claims are not local measurements. Context7 was unavailable; official repositories/model cards and installed dependency code were used.

## Reproduce the local evaluation

Observed host: Apple M5 MacBook Air, 16 GB unified memory; about 35 GiB free before setup. Python 3.11.15, PyTorch 2.14.1. CPU inference deliberately uses four threads; MPS availability was observed but not used or benchmarked. Use a fresh ignored directory; do not overwrite earlier runs.

```sh
mkdir -p artifacts/animal-evaluation-new/weights
uv venv --python python3.11 artifacts/animal-evaluation-new/venv
uv pip install --python artifacts/animal-evaluation-new/venv/bin/python \
  -r tools/animal-generation-requirements.txt

git clone https://github.com/VAST-AI-Research/TripoSR.git \
  artifacts/animal-evaluation-new/TripoSR
git -C artifacts/animal-evaluation-new/TripoSR checkout \
  107cefdc244c39106fa830359024f6a2f1c78871
uv pip install --python artifacts/animal-evaluation-new/venv/bin/python \
  --no-build-isolation \
  'git+https://github.com/tatsy/torchmcubes.git@879926d0ef58e6ce0ac2630fdecb5e53af7ed3ff'
```

Download the two model files into the fresh weights directory:

```sh
curl --fail --location --output artifacts/animal-evaluation-new/weights/model.ckpt \
  https://huggingface.co/stabilityai/TripoSR/resolve/5b521936b01fbe1890f6f9baed0254ab6351c04a/model.ckpt
curl --fail --location --output artifacts/animal-evaluation-new/weights/config.yaml \
  https://huggingface.co/stabilityai/TripoSR/resolve/5b521936b01fbe1890f6f9baed0254ab6351c04a/config.yaml
```

The generation script verifies both hashes before loading; never disable those checks to accept a different model. Prefetch only the public DINO configuration used by the upstream tokenizer:

```sh
artifacts/animal-evaluation-new/venv/bin/python - <<'PY'
from huggingface_hub import hf_hub_download
hf_hub_download('facebook/dino-vitb16', 'config.json',
                cache_dir='artifacts/animal-evaluation-new/hf-cache')
PY

HUGGINGFACE_HUB_CACHE="$PWD/artifacts/animal-evaluation-new/hf-cache" \
artifacts/animal-evaluation-new/venv/bin/python tools/generate_animal.py \
  --source artifacts/animal-evaluation-new/TripoSR \
  --weights artifacts/animal-evaluation-new/weights \
  --image assets/ai-reference/cat-tabby-v1.png --species cat \
  --output artifacts/animal-evaluation-new/cat
```

Repeat with the dog reference, species `dog` and a new `dog` output directory. The pinned Hugging Face client uses **HUGGINGFACE_HUB_CACHE**, not the newer `HF_HUB_CACHE` name: the first live attempt failed due to that mismatch and is preserved. The runner forces offline hub/transformer reads before imports, uses verified local weights, and has no hosted-inference path. Configuration prefetch/model download are separate network reads, not remote model execution. Full observed dependency versions and DINO cache/config hashes are preserved privately.

Current runner uses resolution 256, query chunks of 4096, seed 0 and CPU. It also verifies the cached DINO configuration hash before model loading; the recorded cache snapshot is `f205d5d8e640a89a2b8ef0369670dfc37cc07fc2`. It preserves the original reference and follows upstream alpha/foreground preprocessing; the processed `model-input.png` is recorded separately. Output includes `mesh.glb`, `mesh.obj` and `generation.json` with hashes/settings/limitations. Exit 0 means mesh generation completed, while the asset acceptance status stays PARTIAL / G-P NOT RUN. Invalid inputs or failed generation return 2; failed generations that reached model setup keep a failure manifest. Existing output directories and modified/unpinned source are rejected. Python dependency installation remains isolated from Unity and the standard-library benchmark tests.

## Actual artifacts and quality review

Private root: `artifacts/ai-animals-001/`. These are prepared assets outside the product project, not a scored M1/M3 run.

| Candidate | Vertices / triangles | Recorded generation-stage seconds | Local files |
|---|---|---|---|
| Cat, resolution 128 | 13,493 / 26,912 | 8.014 | `cat-v2/mesh.glb`, `.obj`, `generation.json` |
| Dog, resolution 128 | 9,927 / 19,784 | 7.236 | `dog-v1/mesh.glb`, `.obj`, `generation.json` |
| Cat, resolution 256 | 55,900 / 111,620 | 13.400 | `cat-res256/mesh.glb`, `.obj`, `generation.json` |
| Dog, resolution 256 | 40,491 / 80,848 | 13.359 | `dog-res256/mesh.glb`, `.obj`, `generation.json` |

Times cover model loading through export after dependency imports, excluding reference generation/download/setup/import time. No peak-memory, thermal or battery performance claim is made for this offline art tool. The built-in image tool was used for two references; no separate metered API credentials or paid infrastructure were configured. Account/subscription usage cost was not independently measured. Local 3D inference required no hosted calls.

All four GLBs reloaded with the expected vertex/triangle counts and matching hashes. Each has one connected component without topology repair, non-watertight topology, vertex colours, zero skins, zero animation channels and no PBR material definitions. `mesh-roundtrip-checks-v2.json` and `glb-structure-checks.json` contain checks. The first derived component report used trimesh's default hole repair, inflating component face counts; it is superseded by the explicitly unrepaired v2 analysis. Raw meshes were not changed.

Eight final previews (four yaw views per animal) are named `preview-visible-000/090/180/270.png` under the resolution-256 folders. They are desktop mesh renders, not phone/AR evidence. Trimesh/pyglet hidden-window rendering produced blank/clipped frames, and normal Cocoa teardown failed in the first attempt. Those attempts are preserved; valid previews used short-lived visible render processes with files saved before process exit. No blank preview is treated as visual verification. The preview helper and logs are in private evidence.

**Static quality precheck: FAIL for product use.** Both resolutions show blurred/inferred eye and muzzle detail, coarse coat appearance, faceted silhouettes and imperfect paws/limbs. Increasing extraction resolution adds roughly four times the triangles without recovering the missing facial/fur detail. Coat appearance is vertex colour, not a convincing PBR/fur solution. Open topology needs investigation before skinning; no deformation/contact review is possible yet. No external motion reviewers or blinded cohort have evaluated these assets.

Next bounded corrective work is a better shape/material generation or cleanup path, then retopology, separate eyes/fur, quadruped rig/skinning, required clips and mobile LODs. Do not spend further extraction iterations assuming more triangles alone will fix realism. No substitution of these draft assets for accepted photorealistic animals, no M0 protocol freeze inferred, no AR implementation or product gate passed.
