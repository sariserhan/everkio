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

## Ungated shape and rig evaluation 002

The owner authorized M4–M14 conditionally after prerequisite gates (D14), with **no spending**. Current work remains generic asset preparation outside Unity. After reporting website access to Stable Fast 3D, the owner chose **“Continue without gated weights.”** No gated weights were acquired, no account/token was configured, and no paid or customer-pet reconstruction job ran.

Selected second shape model: [official TripoSG source](https://github.com/VAST-AI-Research/TripoSG) revision `fc5c40990181e2a756c4e0b1c2f4d6b5202faf8c`, public [VAST-AI/TripoSG weights](https://huggingface.co/VAST-AI/TripoSG) revision `2c1c516d22d58db486a058d98d31bb6177344e06`. The model card declares MIT. Retained [source license](../third_party/TripoSG-LICENSE.txt) and [NOTICE](../third_party/TripoSG-NOTICE.txt) identify additional upstream code and terms; MIT is not a blanket claim about every dependency. This evaluation bypassed RMBG using the original alpha references and disabled the optional FlashVDM decoder. Review applicable inherited-code/output terms before distribution; no model/runtime is embedded in the app.

The upstream path targets CUDA. The isolated evaluation adapted the [unmerged MPS proposal](https://github.com/VAST-AI-Research/TripoSG/pull/44), not a claim of supported upstream Mac operation: optional DISO import, surface-grid allocation on the actual input device, and 4096-point VAE decode chunks. Exact patch SHA-256 `9e12c7563af9dc918002a7b73be51cf57dd8a3e2d7e8e73ab9e7acdf4c212446`. Python 3.11, torch 2.14.1, diffusers 0.32.2, transformers 4.49.0 and peft 0.14.0 were isolated in `artifacts/ai-animals-002/triposg-venv/`; full freeze and source/config/weight hashes are retained privately. Public weight downloads checked LFS SHA-256 and size. Local-only inference used MPS float16, CPU seed 42, 30 denoising steps and hierarchical extraction at 128→256. A 0.65 MPS allocation fraction, finite-latent checks, 600-second denoising guard and 900-second parent-process timeout bounded this evaluation. These controls do not authorize future paid research.

| Actual result | Cat | Dog |
|---|---|---|
| Raw shape vertices / triangles | 127,360 / 254,664 | 127,508 / 255,004 |
| Recorded generation-stage seconds | 95.453 | 97.309 |
| Whole subprocess seconds | 98.303 | 100.676 |
| Raw GLB SHA-256 | `0675b83c2819c46411e436b3cbe896cabc7312142a6b38a81a0cf1dda9a76108` | `41884f18a50392982d1e6713349087704ce4936a1a0844669dad04f1146cc97b` |
| Derived rig vertices / triangles | 15,002 / 30,000 | 15,000 / 30,000 |
| Unweighted vertices / maximum joint influences | 0 / 4 | 0 / 4 |
| Exported GLB deform bones | 46 | 46 |
| Maximum nearest rest-vertex error, GLB reimport | 0.00003151 | 0.00001659 |
| Maximum nearest rest-vertex error, FBX reimport | 0.00002037 | 0.00000960 |

Stage times exclude dependency imports, downloads and setup. MPS allocation snapshots around 3.7 GiB are allocator readings, **not total peak resident memory**. Both raw shapes were watertight on reload and contained tiny disconnected extraction fragments; raw files remain unchanged. Four yaw previews per species were saved and inspected. Shape/silhouette improved over TripoSR, but eyes/muzzles, surface ridges and proportions remain visibly imperfect. These uncoloured surfaces do not establish realism.

### Draft rig preparation and actual failures

Pinned PyPI `bpy` 4.5.14 LTS ARM64 wheel, SHA-256 `b846b91edacd8c77ef439bb02e8b7ee63ae8c49009a7575944507e27bb47acd9`. The initial streaming install stalled; a verified wheel download installed successfully. No ML or Blender dependency was added to the standard-library Python tooling or Unity app. `tools/prepare_animal_rig.py` requires this version and source-hash-matched [fit records](../assets/rig-fits/), refuses overwrite, works on a derived copy, rejects removal of more than 0.5% disconnected vertices, reduces polygons, generates a Rigify quadruped and clamps/normalizes skinning to four influences. Height 1.0 is an art normalization, **not physical scale**.

Three actual setup defects were corrected: connected metarig endpoints were initially scaled twice; imported quaternion rotation caused the intended yaw to be ignored; initial landmark placement left one front limb without effective weights. The final fit explicitly changes rotation mode, adjusts yaw/centering and places the draft metarig closer to the shape. No anatomical fitting accuracy is claimed. The revised V3 rigs have 283 control/mechanism/deform bones and 46 deform bones. All vertices have normalized weights with at most four joint influences.

V3 independent checks reopened the saved files with embedded UI scripts disabled, moved head and neck by five degrees and raised each foot control by 0.03 normalized units. Every control produced finite surface changes; resetting returned to the original pose within 0.00001. This catches a disconnected/unresponsive rig; it does not establish correct skinning, natural gait or planted-foot contact. Neutral and head-pose desktop renders were inspected. GLB/FBX reimport retained one skinned animal surface and rest coordinates within the errors above. FBX contains 78 bones including necessary hierarchy, GLB 46. Blender creates a separate bone-display helper during GLB import; binary JSON inspection confirmed only one actual mesh in each exported GLB. No animation was exported, and deformed export parity was not measured.

**Preparation-command blocker:** V3–V7 saved drafts and reports, then the PyPI Blender process exited 139 at native shutdown. A preserved macOS crash report shows `EXC_BAD_ACCESS` during allocator/static `VectorSet` destruction. Serial execution, normal Python fallthrough, addon cleanup/factory reset and Blender's quit operator did not resolve it; no force-exit workaround hides the error. Separate reopen/deformation/render/reimport processes exited 0, so readable artifacts exist, but the generation command remains unreliable for unattended use. Official Blender binary download listing returned HTTP 403 on this host; an installed supported Blender executable or an investigated upstream fix is still needed. Earlier V2 process exits were 0 but their fits are superseded. Six new standard-library fit guards bring the suite to **61 passing tests**, separate from these actual Blender checks.

Example **experimental command**, currently subject to the shutdown blocker:

```sh
artifacts/ai-animals-002/blender-venv/bin/python tools/prepare_animal_rig.py \
  --mesh artifacts/ai-animals-002/cat-triposg/mesh.glb \
  --fit assets/rig-fits/triposg-002-cat.json \
  --output artifacts/ai-animals-002/cat-rig-new
```

The pinned model checkout, patched experimental inference driver, per-file downloads/hashes, exact environment freezes, templates, raw shapes, desktop renders, fit failures, final deformation/reimport scripts/results and native crash report are retained under ignored `artifacts/ai-animals-002/`. No installed environments, signed binaries or weights are committed.

### Skipped model paths and remaining gate

Stable Fast 3D source/dependencies and local CPU texture-baker/UV native extensions were prepared; a 16×16 one-triangle raster/interpolation smoke check passed (136 covered texels, finite interpolation). Homebrew `libomp` was installed for compilation. The first dependency attempt failed on an incompatible setuptools pin; retry succeeded. **No SF3D weights were downloaded or inference executed**, and preparation is not an accepted textured animal. The owner's latest decision closes this gated-weight path. Hunyuan3D-Swift source/requirements were reviewed but no model ran; its published full material path exceeds this 16 GB host's memory. Source MIT and model-specific terms must not be conflated.

**Asset acceptance remains PARTIAL / product quality precheck FAIL.** No PBR coat, separate eyes/fur, anatomy/contact acceptance, required motion clips, calibrated physical scale, mobile LOD set, Unity animal rendering or phone AR evidence exists. Preparation provides movable drafts, not accepted animals. Next work is material/anatomy correction and reliable rig authoring, followed by reviewed motion and the unresolved M0 protocol freeze/calibration. G-P and every later product gate remain NOT RUN. Spending and reconstruction research remain unapproved/unfunded; D14 authorizes later implementation only after prerequisites pass.
