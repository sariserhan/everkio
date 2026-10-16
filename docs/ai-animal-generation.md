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

## Rig cleanup, painted surfaces and sampled export 003

This continuation supersedes the native-shutdown blocker above **on the tested host**. It stays outside the Unity product project; M0 remains PARTIAL and no animal/AR milestone is passed.

### Actual shutdown fix

A subprocess isolation matrix reproduced SIGSEGV with Rigify generation alone; plain bpy import, Rigify addon enable, GLB import/export and FBX export each exited 0. The generated Rigify UI is registered by `exec(script.as_string(), {})` in the installed `rig_ui_template.py`, independently of addon registration. Disabling the addon alone leaves these generated classes registered. The preparation tool now identifies the generated panel namespace by the owned rig ID, calls its existing `unregister()` once and then disables Rigify, including cleanup after failures once a rig exists. It refuses missing/ambiguous cleanup namespaces. It uses neither forced exit nor a changed exit status to hide a crash.

The minimal reproduction with this cleanup exits 0, as do full cat, full dog and repeated full cat preparation commands. Reopen/deformation/GLB/FBX checks also exit 0. Two synthetic cleanup tests verify matching namespace selection/deduplication and refusal of missing/ambiguous registrations without unregistering other rigs. **63 Python tests pass.** The previous failures remain preserved in evidence 002; no claim of an upstream fix or universal Blender reliability is made. The successful local fix removes the need to install a different Blender binary just to continue this preparation.

### Painted surfaces, still drafts

Used the built-in imagegen skill/tool to paint six registered mesh-view targets for each animal from the original synthetic reference. Exact prompts, target/projection/fit hashes and output provenance are in [`assets/ai-reference/paint-manifest.json`](../assets/ai-reference/paint-manifest.json); selected PNGs are `cat-paint-sheet-v1.png` and `dog-paint-sheet-v1.png`. All references are generic synthetic animals, not customer pets. No gated weights, API credential, paid infrastructure or hosted 3D generator was configured. Built-in account/subscription usage cost was not independently measured.

Native Blender rendering created the target sheets. A local 3D material experiment projects the painted views onto the actual mesh using surface orientation and BVH visibility, blends weights and uses Blender's native baker to produce one 2048×2048 colour image on unique UVs. This is a colour map with a constant draft roughness, **not an accepted PBR/fur/eye solution**. The initial hard-view selection showed clear seams and was superseded by weighted blending. Paint may shift silhouettes/features or retain lighting; no exact registration guarantee is claimed.

Both painted GLBs have one skinned mesh, 46 joints, one material and one embedded PNG colour texture. Checksums of vertex coordinates and topology match the unpainted source exactly; painting did not repair anatomy. Blended paint used a fallback at 153 cat / 289 dog vertices where no visible positive-facing view met the experiment's tolerance. Those regions, texture projection seams, ear/paw interiors, eye registration and view-dependent shading need correction/review. Front/rear desktop renders were inspected. Both species remain below product acceptance: geometry ridges, projected facial detail, stiff proportions and imperfect paw placement are visible. There is no separate eye geometry, real fur, normal/roughness map validation, calibrated scale or LOD acceptance.

Private files: `artifacts/ai-animals-003/{cat,dog}-blended-v2/painted-draft.blend`, `painted-draft.glb`, `coat-basecolor.png`, projection report and front/rear PNGs. `material-integrity-v2.json` records raw geometry and GLB hashes. Experimental projection/render scripts remain with the evidence rather than becoming an unvalidated production asset pipeline.

### Deformed export comparison

Prepared a deliberately labelled diagnostic sweep: head and neck five-degree test rotations and one-foot-at-a-time 0.03-unit lifts, 145 frames at 24 FPS. This is **not natural motion, gait or contact acceptance**. Direct Rigify GLB export matched rest but failed the experiment's 0.001-normalized-unit pose-parity tolerance. Disabling bendy-bone segments greatly reduced the head/neck discrepancy, but foot discrepancy remained; retaining the full hierarchy did not resolve it. No exporter defect is asserted from these observations alone.

The successful comparison sets one segment per deform bone and samples the 46 deform transforms into a separate constraint-free export skeleton. This deliberately changes Blender bendy deformation to linear skinning and requires later deformation review. The source Rigify rig stays available for authoring. On both **textured** animals, GLB export/reimport at neutral, head, neck, all four foot peaks and final neutral retained the sampled surface to maximum nearest-rest-mapped vertex error **0.000008062 cat / 0.000003966 dog**, in normalized units. These eight sampled poses are a diagnostic comparison, not full animation/contact coverage, a physical error measurement or phone evidence. Full data, failed variants, sampled frames and scripts are preserved.

Final diagnostic exports: `artifacts/ai-animals-003/{cat,dog}-textured-animation-v2-smoke/animation-smoke.glb`, `.blend`, `animation-parity.json`. Later curated clips need their own sampled export and visual/foot-contact review. No walk, start/stop, turn, sit, lie, eat or approach sequence is represented as completed. No Unity animal import or AR implementation occurred.


### Lower-detail drafts and review videos

LOD preparation caught a stale Blender RNA-reference cleanup issue: removing a list of UV/attribute proxy objects skipped entries after indices shifted. Final V2 removes by saved names, verifies one `CoatUV` and removes all temporary projection-weight attributes. Source geometry and baked colour PNG hashes match V1; V1 outputs and failed assertions are retained. The corrected material/animation checks refer to `*-blended-v2/` and `*-textured-animation-v2-smoke/`.

Each species now has static skinned draft levels at **30,000 / 15,000 / 7,500 triangles**, with normalized weights capped at four influences. All six GLBs reimported with one UV map, one material and a skin; final LOD2 front renders were inspected. Private inventory: `artifacts/ai-animals-003/{cat,dog}-lod-drafts-v2/lod-inventory.json`; checks: `lod-integrity.json`. These are polygon-reduction trials, not accepted mobile LODs: no switching thresholds, motion/contact/silhouette acceptance or phone timing is established.

Actual rendered desktop orbit videos: [`cat draft`](../artifacts/ai-animals-003/cat-textured-animation-smoke/draft-motion-review.mp4) and [`dog draft`](../artifacts/ai-animals-003/dog-textured-animation-smoke/draft-motion-review.mp4). Each is 145 H.264 frames at 24 FPS, 640×576, duration 6.041667 seconds; full FFmpeg decode succeeded. Frames at 0/2/4 seconds were inspected. In-frame labels explicitly identify local 3D drafts and diagnostic control sweeps, not AR or natural gait. Videos use the initial blended colour variant; final V2 removes unused UV/attribute data, with identical source geometry and colour PNG hashes. Grainy preview sampling, coat/eye/seam/anatomy defects and lack of floor/contact remain visible; no realism gate is claimed.

**Next blocker remains asset acceptance and M0 physical calibration**, rather than gated-model access or the recovered rig shutdown failure. Do not turn these technical checks, attractive paint sheets or desktop videos into milestone passes.

## Walking/contact candidate and isolated Unity compatibility 004

This is continued local generic art and toolchain preparation from `f35a593`, not a passed M1/M2 implementation. No paid resource, gated model, customer data or reconstruction job. The product project and installed phone app remain unchanged.

Authored a four-beat constant-speed walking candidate for each existing painted rig: 121 frames at 30 FPS, four seconds of sampled movement, normalized stride 0.35, stance fraction 0.65 and swing height 0.065. Planted control targets are constant in world coordinates; swinging targets use a smooth endpoint trajectory. These are artist-selected trial parameters, not biological measurements or frozen acceptance limits. Source bones use the already-tested one-segment linear deformation path.

Selected bottom vertices from toe-weight regions to observe **skinned-paw proxies**. Initial V1 had small gaps/penetration; V2 applies small constant vertical IK placement corrections toward a 0.002 normalized-unit sole proxy height. Masks/method stay unchanged between variants. All 121 sampled V2 poses had finite vertices and no vertex below the zero-height plane. Worst within-stance XY proxy drift was **0.001945 cat / 0.003709 dog** normalized units. These are imperfect weight-selected regions, not independently validated anatomical contact landmarks. They do not establish believable contact, continuous-time clearance, natural gait or real-room grounding. Initial measurements and failures remain preserved.

Constraint-free sampled GLB export/reimport compared **all 121 frames** against the authoring surface: maximum mapped-vertex errors **0.000008271 cat / 0.000004556 dog**, normalized units. Import was configured at 30 FPS before importing keys, preserving time alignment. Source/export scripts, per-frame differences, raw paw observations and provenance are under `artifacts/ai-animals-004/{cat,dog}-walk-v2/`. Baked joint translation supplies body travel; Unity root-motion extraction and an in-place/controller path are not validated.

Actual floor/shadow desktop review videos: [`cat walk candidate`](../artifacts/ai-animals-004/cat-walk-v2/walk-review.mp4), [`dog walk candidate`](../artifacts/ai-animals-004/dog-walk-v2/walk-review.mp4). Each decodes fully: 121 H.264 frames, 30 FPS, 768×640, duration 4.033333 seconds including the last displayed frame. In-frame labels identify an unaccepted draft at normalized scale, not AR. Contact/front and side stills and extracted video frames were inspected. Bodies/head/tail remain stiff, motion lacks secondary weight shifts and toe roll, and anatomy/coat/eyes are unfinished. Cyclic walking starts/ends mid-gait; start/stop, turns, sit/lie, eat/approach/reaction clips are not supplied by this trial. No independent reviewers or cohort accepted it.

### Actual Unity asset-path check

Created a separate ignored project at `artifacts/asset-compatibility-004/`, pinned to the installed Unity **6000.6.6f1**, with built-in modules only. Exported sampled FBX files and copied the existing baked colour PNGs into that temporary project. No candidate asset or script was added to `unity/Everkio` and no phone build was made.

Editor smoke checks import one skinned mesh, 46 deform bones, 30,000 triangles, a 2048² colour texture and a four-second animation per species. They sample the legacy clip, bake finite surface geometry, check normalized height and body translation, and render actual textured Unity images. Result: **editor compatibility checks pass**, not presence/photorealism acceptance. Cat: 18,061 imported vertices, height 0.9978993, translation 1.3999999. Dog: 19,544 vertices, height 0.9980719, translation 1.3999991. UV/normal splits explain imported vertex counts; no physical metre/breed-size claim. Standard shader rendered both meshes, with visibly shiny/plastic coat and unfinished detail. Production shader/Animator, Play Mode behavior, animation/contact parity inside Unity and phone performance remain untested.

The initial smoke validator applied renderer scale twice to baked snapshots, reporting approximately 100× height/travel. It exited 1; those logs are preserved. Explicit `BakeMesh(mesh, true)` scale compensation fixed the **validator**, not a claimed asset-scale repair. Source FBX contains a 100× transform hierarchy; future import/rig/controller work must handle that intentionally. Final batch exited 0 with `EVERKIO_ISOLATED_ASSET_CHECK_OK` and both PNGs/report present. [Official BakeMesh documentation](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SkinnedMeshRenderer.BakeMesh.html) and [SampleAnimation documentation](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/AnimationClip.SampleAnimation.html) were reviewed because Context7 was unavailable. Metadata: `artifacts/ai-animals-004/unity-import-results.json`; renders: `unity-cat.png`, `unity-dog.png`; failed and successful logs plus the exact isolated C# check are retained privately.

The next asset work is genuine motion/anatomy/material correction and independent review, rather than more polygon extraction. None of these desktop checks or videos is animal/AR device evidence. M0 physical protocol/calibration gaps and every product gate remain open.

## Stationary start/walk/stop preparation 005

Continued from `953fbae` with the existing ungated generated shapes and painted rigs. New `tools/author_animal_motion.py` runs in the same isolated Blender 4.5.14 LTS environment. It checks the exact source hash, refuses existing output directories, disables saved scripts, rejects pre-existing actions/NLA and writes a failure/result manifest. Rigify's existing drivers are retained; an initial overly broad animation-data guard rejected both rigs because drivers also use animation data. Those failed attempts are preserved.

The normalized trial now has a one-second stationary beginning, three discrete 0.35-unit steps per foot with staggered swing onset, then a stationary ending. Quintic horizontal interpolation gives zero endpoint speed; sinusoidal squared lift has zero endpoint vertical speed. Body travel follows mean paw-target displacement, totaling 1.05 normalized units. This six-second/181-frame authoring experiment supplies controlled entry/exit, not biologically accepted acceleration, approach behavior or root-motion extraction. Body/head/tail secondary movement and toe roll remain unfinished.

Source binds: cat `45753671a79d4a4d5b07cbd7584fc1fceb4419a0f7482b71684419c714146b19`, dog `741955d5c362fe7eb73d1ecef9426fff780ac43eaf42d5a3df121d54513ab570` for `artifacts/ai-animals-003/{species}-blended-v2/painted-draft.blend`. Example, from repository root:

```sh
artifacts/ai-animals-002/blender-venv/bin/python tools/author_animal_motion.py \
  --source artifacts/ai-animals-003/cat-blended-v2/painted-draft.blend \
  --source-sha256 45753671a79d4a4d5b07cbd7584fc1fceb4419a0f7482b71684419c714146b19 \
  --species cat --output artifacts/new-cat-motion
```

Successful authoring exit means outputs were produced, **not** that floor/contact checks passed. Inspect `motion-review.json`. Final checks compare every deformed vertex during the first/last 30 frames: maximum hold displacement **0 for both species**. Controller stance targets remain fixed. Skinned paw-proxy stance drift is **0.002343 cat / 0.002875 dog** normalized units. Cat sampled floor check passes; **dog fails**, with maximum penetration **0.002464** at the right rear toe. Inspection identified vertex 11176, weighted approximately 88% `DEF-toe.R` and 12% `DEF-foot.R.001`. A planted controller alone does not guarantee a planted skinned paw. The floor is not lowered and the mesh is not lifted to hide this defect. Weight/rig/contact correction is still required.

Intermediate authoring output: `artifacts/ai-animals-005/{cat,dog}-start-stop-v3/`; earlier failed guard and intermediate versions retained. Five new synthetic trajectory/input tests check stationary bookends, bounded monotonic travel, fixed stance targets, endpoint continuity wrong-source rejection and existing-evidence preservation; these tests do not evaluate animals or natural motion. Product Unity project prepare/validate were rerun successfully, with no source or phone deployment change.


V4 makes one measured correction pass: for each sole proxy that dipped below zero, add a **constant** vertical offset to that foot control and regenerate the entire clip. This preserves the fixed stance target instead of changing the floor or hiding failures. Reports retain both passes' minima. Both V4 whole-surface sampled floor checks now pass, with zero stationary-hold displacement; cat drift is unchanged, dog worst stance XY drift is 0.002865. Dog proxy minima are 0.001770–0.002071, but stance heights reach **0.007158** normalized units. That variable clearance is still a contact-quality limitation, not accepted grounding. Full ranges: `stance-clearance-review.json`; final drafts: `*-start-stop-v4/`. Original V3 failures remain evidence. Continuous-time/subframe contact and independent natural-motion review remain untested.

V4 GLB export/reimport checks **all 181 frames**: maximum mapped surface error cat **0.000008285**, dog **0.000004199** normalized units. Sampled FBX then imports into a new isolated Unity 6000.6.6f1 project, `artifacts/asset-compatibility-005/`. Both editor checks pass with one 46-bone skin / 30,000 triangles, six-second clips and approximately 1.05 travel. Sampling all 181 frames in Unity gives minimum floor Y **0.001987696 cat / 0.001770854 dog** and **zero hold displacement**. Exact report: `unity-import-results.json`; batch exits 0 with `EVERKIO_ISOLATED_ASSET_CHECK_OK`. Actual Unity images were inspected and still show plastic/shiny unfinished coat and eyes. This is legacy editor sampling/CPU baking, not production Animator, GPU skinning, Unity-to-Blender per-vertex parity, AR or device acceptance.

Context7 was not available and the official Blender API web fetch returned HTTP 402; installed Blender RNA descriptions separately confirm that actions, drivers and NLA tracks are distinct. Local snapshot: `installed-blender-api.json`. No dependency was added to the product or test runtime.

Final review videos: [cat](../artifacts/ai-animals-005/cat-start-stop-v4/motion-review.mp4), [dog](../artifacts/ai-animals-005/dog-start-stop-v4/motion-review.mp4). Each is a **61-frame / 10 FPS / 6.1-second** H.264 preview at 640×576, sampling every third frame of the 181-frame / 30 FPS authoring clip. This reduced preview cadence is not a motion/performance measurement. Full FFmpeg decode succeeds, and extracted frames at 0.5/2.5/5.5 seconds were inspected. Labels state draft/not AR; stiffness, unfinished anatomy/coat/eyes and awkward leg spacing remain. Earlier V3 render was intentionally cancelled to render corrected V4 instead; its incomplete output/log and cancellation manifest are preserved, never treated as a completed review video. No human-review or presence gate is inferred.

## Idle motion and head/neck fit correction 006

Baseline `7a55f2b`; local generic asset preparation only. No spending, gated model, hosted generation, customer media or reconstruction research. The main Unity product project is unchanged and remains a diagnostic harness.

`tools/author_animal_motion.py --clip idle` now authors a six-second/181-frame candidate with two small chest-lift cycles and a smooth head look. The default `--clip walk` retains the prior start/walk/stop path. Idle checks require finite moving surface vertices, a closed endpoint pose, fixed foot-control targets and reported whole-surface floor clearance. Stationary-hold checks are explicitly not applicable to an animated idle. This is not validated breathing, gaze/eye tracking, blink or natural motion.

The first cat idle used nonuniform chest scale and had a larger GLB mapped-vertex error, **0.000322500** normalized units. It was within the existing 0.001 engineering smoke tolerance, but prompted investigation rather than a quality claim. Its render was cancelled and preserved. Removing nonuniform scaling reduced error to **0.000023728 cat / 0.000020817 dog** on the original rigs. Native reopened-pose checks confirm movement and exact endpoint closure. Actual original-rig walk CSVs remain **byte-identical** to continuation 005 after adding idle support.

### Fit defect and correction

Transparent front/side/top renders show the generated animals' heads turned relative to their torsos, while the original template head bones point along the torso. Weight inspection also finds shoulder influence in the selected upper-front region. This explains a weak/poorly placed head look; it does not establish a complete anatomical diagnosis.

Added optional `neck_chain_points` to the pinned rig fit: four explicit, normalized endpoints for `spine.008` through `spine.011`, anchored to the existing chest. Validation rejects malformed/nonfinite/out-of-bounds points and degenerate/excessive segments; connected endpoint assertions still run before Rigify generation. Original fit files remain unchanged. New draft candidates:

- `assets/rig-fits/triposg-006-cat-head.json`
- `assets/rig-fits/triposg-006-dog-head.json`

These points were manually selected from actual mesh overlays, not measured animal anatomy or independently accepted landmarks. Example preparation, using the same private source mesh/environment:

```sh
artifacts/ai-animals-002/blender-venv/bin/python tools/prepare_animal_rig.py \
  --mesh artifacts/ai-animals-002/cat-triposg/mesh.glb \
  --fit assets/rig-fits/triposg-006-cat-head.json --output artifacts/new-cat-head-rig
```

Both revised rigs prepare/export/shut down successfully, with 46 deform bones, four normalized influences and no unweighted vertices. The original cat fit also reruns successfully as a compatibility check. Native paint transfer verifies **identical vertex positions and polygon indices**, copies existing UVs/materials and retains new weights. Initial lazy image-buffer validation failed; explicitly loading the packed texture resolves that check. Failed script/log and final script remain in evidence 006. The region-weight sum assigned to `DEF-spine.011` rises from 229.59 to 1482.69 for cat and 763.86 to 2661.20 for dog. This is a fixed coordinate-selected region, not a validated head segmentation or realism score.

### Revised motion checks

| Candidate | Max source surface motion | Endpoint/hold result | Max GLB mapped-vertex error |
|---|---:|---|---:|
| Cat idle | 0.014959 | Loop error 0 | 0.000023042 |
| Dog idle | 0.032478 | Loop error 0 | 0.000020658 |
| Cat start/walk/stop | 1.054634 | Stationary surface holds 0 | 0.000006719 |
| Dog start/walk/stop | 1.057587 | Stationary surface holds 0 | 0.000004561 |

All values are normalized units. Each GLB checks all 181 frames; all four source sampled floor checks pass. Idle skinned sole-proxy drift: cat 0.000005209 / dog 0.000033087; walk drift: cat 0.002345 / dog 0.002864. Proxies and positive floor clearance are not accepted anatomical contact, continuous-time clearance or physical scale. Exact per-frame data and reports: `artifacts/ai-animals-006/{cat,dog}-refit-{idle,walk}/`.

The separate Unity project `artifacts/asset-compatibility-006/` imports both original-rig idles and all four refit clips. Actual editor CPU skin sampling checks all 181 frames, finite geometry and floor clearance. Refit idles have zero world travel and endpoint surface delta 0; refit walks travel approximately 1.05 with zero displacement during stationary holds. Batch exits 0 with `EVERKIO_REFIT_ASSET_CHECK_OK`. In `unity-refit-results.json`, `endPoseDelta` is endpoint movement (expected for walks), and `holdError` is only an acceptance check for walk bookends (idle intentionally moves). Neither is a product gate. Actual Unity PNGs were inspected and still show unfinished shiny/plastic coat and eyes. Production Animator/GPU/phone behavior and Unity-to-Blender full vertex parity remain untested.

Python regression suite: **81 passing tests** (three new tests across idle/fit guards), plus actual Blender and isolated Unity assertions. No dependency added. Context7 is unavailable; the existing pinned Blender APIs and installed native behavior were used. A current read-only device inventory/details query confirms the iPhone 14 Pro / iOS 26.6.2 (23G90), paired/connected via local network with Developer Mode enabled. No app launch, capture, deployment, battery-health measurement or presentation calibration followed from that metadata query.

Required motion coverage remains incomplete: idle/head look and start/walk/stop are unaccepted drafts; turn, sit, lie, eating/contact, approach and input-triggered reactions are not supplied by this continuation. Fur/eyes/anatomy, independent motion review, scored AR/device evidence and every product gate remain open.

Final refit videos: [cat idle](../artifacts/ai-animals-006/cat-refit-idle/motion-review.mp4), [dog idle](../artifacts/ai-animals-006/dog-refit-idle/motion-review.mp4), [cat walk](../artifacts/ai-animals-006/cat-refit-walk/motion-review.mp4), [dog walk](../artifacts/ai-animals-006/dog-refit-walk/motion-review.mp4). The two original-rig V2 idles are retained for comparison. All six completed previews fully decode: **61 H.264 frames / 10 FPS / 6.1 sec / 640×576**, sampling every third 30-FPS authored frame. Refit idle extremes at 2/4 seconds and walk poses were inspected; captions state draft/not AR. These are low-cadence engineering previews, not natural-motion or performance acceptance. Eyes remain painted, ears/tail static and body movement/coat unfinished. No independent reviewer accepted them.

Owner now reports **75% Battery Health Maximum Capacity** in response to the explicit health question. This is separate from historical 91% charge and does not become CSV battery charge or a measured run-start value. Room markings and measured temperature remain unknown; M0 calibration and protocol freeze are still incomplete. See [device matrix](device-matrix.md).


### Physical-player preflight 007

The separate [asset-check app](../tools/asset_check/README.md) now builds, signs, installs and runs the four 006 refit clips on the actual iPhone 14 Pro / iOS 26.6.2. A complete uninterrupted report and four inspected 2556×1179 PNGs confirm the narrow runtime animation/skin/texture/screenshot/export path; finite sampled surfaces remain above the normalized floor. Owner also confirms seeing the dog. Exact results, failures, build GUID and private evidence are in [M0 status, continuation 007](m0-status.md#separate-physical-iphone-asset-preflight-007--october-16). Main diagnostic project stays unchanged. These are draft scene images, not AR recordings, sustained performance, natural motion or realism acceptance; M1 and G-P remain NOT RUN. No paid generation or gated weights were used.


### Turning candidates 008 — October 16

Baseline `62b08ed`. Extended the existing source-hash-bound motion author with `--clip turn`: three sequential 30-degree stepping increments produce a six-second, 181-frame turn, with stationary bookends. Foot controllers follow fixed targets during stance and lifted arcs during swing; the root follows their mean angular progression. The existing walk/idle paths are retained. No dependency, generation service, gated weight or spending added.

The actual refit cat/dog rigs reach **−90.0000077 degrees** evaluated root rotation; zero body translation and zero deformed-surface movement in the stationary bookends. All 181 sampled surfaces are finite and above the floor after the existing constant per-foot correction. Cat worst stance proxy XY drift **0.002716674** normalized units; dog **0.006208875**. These are weight-selected mesh proxies, not anatomical contact evidence. Dog's initial pass penetrates the floor by **0.002921086**; the correction removes penetration, with final whole-surface minimum **0.000340781**. Cat minimum **0.002017540**. Clearance does not establish firm contact, acceptable sliding, body-weight transfer or natural turning.

A new evaluated-root guard initially ran before the dependency-graph update and rejected a stale matrix; failure preserved in `cat-author-v2.log` and `cat-refit-turn-v2/motion-review.json`. Moving validation after the existing update fixes the check. V1 remains exploratory; final candidates are `artifacts/ai-animals-008/{cat,dog}-refit-turn-v3/`. **82 Python tests pass**, including planted angular progression/endpoints; native Blender assertions separately check actual geometry, motion and root rotation. No gate passes from these checks.

Motion inventory: idle/head look, start/walk/stop and one turn direction now have drafts. Sit/lie, eating, approach/reactions, full gaze/blink and natural secondary movement remain incomplete; anatomy, coat/fur/eyes, true physical size, anatomical contact and independent art/motion review remain open. Reusing the walk path is not evidence of an accepted approach behavior. Existing physical-player evidence 007 covers only the earlier idle/walk clips; it does not cover these turns.


Final GLB sampled parity: cat maximum vertex error **0.0000067864**, dog **0.0000054309**, all 181 poses each. Isolated Unity import/sampling exits 0 with `EVERKIO_TURN_ASSET_CHECK_OK`; endpoint surface rotation errors **0.000001733 / 0.000002942**, stationary surface error 0, floor minima **0.002016574 / 0.000340849**. `unity-refit-results.json` retains historical field names: `travel` is the bounding-box-center displacement from rotating an asymmetric shape, not root translation; `endPoseDelta` is expected nonzero for a turn. Sampled endpoint validation accepts the FBX coordinate conversion's handedness by checking the smaller error for ±90° world Y rotation. This is a rigid endpoint check, not full deformed-pose cross-engine parity. Unity renders inspected; chest folding, unfinished eyes/material and stiff tail/body remain open defects.

Reproduce authoring with the pinned Blender Python, `tools/author_animal_motion.py --clip turn --species cat --source artifacts/ai-animals-006/cat-head-refit-painted-v2/painted-draft.blend --source-sha256 9a3dc322cfa6556ba0a375008eadea598fbd01f28bd17c0395fa0c5e08ae364e --output artifacts/NEW-cat-turn`; dog source hash is `a62cdccfa64092f2bb33b8da68481ee924a6c678c608b5d20375a370b5523ea7`. Use fresh outputs. Exact export/render/Unity check scripts are retained under evidence 008; no new product runtime controller was introduced.


Completed turn review videos both fully decode: **61 H.264 frames, 10 FPS, 6.1 seconds, 640×576**. Extracted frames at 2/4/5.5 seconds and actual Unity PNGs inspected. They show draft turns, unfinished coat/eyes, chest folding and stiff body/tail; lower preview cadence is not a performance measurement. Native authoring remains 30 FPS. No independent motion/contact or presence acceptance follows.

Review files: [cat turn](../artifacts/ai-animals-008/cat-refit-turn-v3/motion-review.mp4), [dog turn](../artifacts/ai-animals-008/dog-refit-turn-v3/motion-review.mp4).
