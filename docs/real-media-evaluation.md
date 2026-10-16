# Real-photo/video animal evaluation — preparation

October 16, 2026. Owner: Serhan Sari. Status: **preparation complete; execution NOT RUN**. Spending remains unapproved. This packet answers the owner's request to improve the draft cat/dog using real media. It does not amend R0, accept a model license, acquire weights, ingest private media or start reconstruction/training.

## Proposed route

Use existing pretrained animal models to fit an individual animal's shape, appearance and pose from authorized multi-view photos/video. Broad training from scratch is not the first experiment. A reconstruction still needs editable geometry, convincing fur/eyes, stable skinning, complete motion and mobile optimization. A realistic source photograph cannot correct the current bad sit/lie deformation by itself.

Compare a photo/video-derived **rigged mesh** against the existing generic draft first. A Gaussian appearance layer is a separate optional comparison if its rights, deformability and phone rendering become feasible. Source-video playback or a model that only repeats the recorded motion cannot satisfy the interactive companion requirement. Reconstruction of a recognizable real animal belongs to the existing R-track, even if its intended later role is a generic companion; relabelling it does not bypass R0.

## Candidates checked from primary sources

These are documentation findings, not installed or benchmarked pipelines. Exact source snapshots/hashes are private in `artifacts/real-media-preparation-013/sources.json`.

| Candidate / reviewed revision | Useful direction | Published setup / observed terms | Decision now |
|---|---|---|---|
| [4D-Animal](https://github.com/zhongshsh/4D-Animal/tree/2b8a95968c1a17287697b6c1c1991bb1415a2097) | Video-based animal shape/pose fitting; first candidate for further dependency review | README installs CUDA 12.1 PyTorch and CUDA-specific PyTorch3D; external data is a separate download. [Top-level license](https://github.com/zhongshsh/4D-Animal/blob/2b8a95968c1a17287697b6c1c1991bb1415a2097/LICENSE) is Apache-2.0. | HOLD: external model/data terms, code provenance, cat coverage, editable export and hardware access remain unverified. Apache at the repository root is insufficient to clear the entire pipeline. |
| [AnimalAvatar](https://github.com/facebookresearch/AnimalAvatar/tree/a28e90567f263280473628f03c93aefa8a0c70b4) | Video-driven dog shape/appearance fitting; methodological comparison | README describes CUDA 11.8, external SMAL/DensePose assets and CoP3D data. [Code license](https://github.com/facebookresearch/AnimalAvatar/blob/a28e90567f263280473628f03c93aefa8a0c70b4/LICENSE.txt) is CC BY-NC 4.0. | HOLD: noncommercial restriction is unresolved for Everkio's intended use. No commercial clearance claimed; do not execute or embed under an assumed permission. Cat suitability is not established by the dog paper. |
| [GART](https://github.com/JiahuiLei/GART/tree/16c11f8a5bb3ae249a9d04dc9d98c316e10f1126) | Articulated Gaussian appearance comparison, including a dog example | README tests Ubuntu/CUDA; installer uses CUDA extensions. Root code is MIT, but the [bundled rasterizer license](https://github.com/JiahuiLei/GART/blob/16c11f8a5bb3ae249a9d04dc9d98c316e10f1126/lib_render/diff_gaussian_rasterization-alphadep/LICENSE.md) limits use to research/evaluation and requires consent for commercial use. | HOLD: dependency/model/data rights, cat support, relighting and Unity/iOS runtime unverified. Do not treat the root MIT license as covering every component. |

4D-Animal acknowledges AnimalAvatar as a code reference; notice/provenance review is still required. This observation is not a finding of license incompatibility. The attempted GART simple-knn `LICENSE.md` retrieval returned 404; its terms remain unresolved, not permissive by default. No authors/vendors were contacted.

The published CUDA paths are **not verified to work on this Apple silicon Mac**. A port, an already-owned compatible NVIDIA host, or a funded capped provider would need separate evaluation. No minimum VRAM, Mac training speed, provider price or per-pet cost is asserted. Do not rent a GPU or attempt an MPS port simply because a paper reports attractive images. No new gated weights or credentials are requested.

## Source-media plan — draft, before intake

Prefer original footage for one cat and one dog, with permission from the media rightsholder and animal owner where different. Internet visibility, a dataset download link or permission to view a clip does not establish reconstruction, training-reuse or output-delivery rights. Keep model-code, weights, template, source-media and derived-output terms separately recorded.

For a living animal when new capture is possible:

1. Use consistent diffuse light, a simple background and a visible floor. Keep the whole animal, paws and tail in view; avoid motion blur and changing zoom.
2. Capture front, back, both sides and intermediate angles, plus close face/eye/ear/nose and distinctive coat details. Record a known size reference separately to establish scale.
3. Record short separate clips of natural standing, walking, turning and settling/sitting/lying when available. Record the animal, not a screen playing another recording. Do not force an uncomfortable pose to fill the motion list.
4. Reserve a separate camera pass and separate motion clip as held-out evaluation. Do not split adjacent frames from the same clip between input and held-out sets and call them independent evidence.

These are proposed coverage targets, not a demonstrated sufficient capture recipe or a fixed required photo count. Existing archives may have missing angles/scale; record those unknowns and permit rejection rather than inventing identity details. Memorial material retains its separately governed path; no new capture is presumed possible.

Before any intake, complete this private case record for each animal:

| Field | Required record |
|---|---|
| Pseudonymous case ID / species / path | Cat or dog; living or memorial; no owner name in public evidence |
| Media and animal permissions | Rightsholder/owner confirmation, permitted fitting/evaluation/output use and withdrawal route |
| Training reuse | Separate explicit opt-in if proposed; default is no cross-pet/general-model training reuse |
| Files and coverage | Source paths, SHA-256, angles, motion, lighting, scale reference and missing regions |
| Evaluation split | Separate input and held-out files, locked before fitting |
| Storage lifecycle | Owner-approved private encrypted location/access, retention/deletion date, backup/export/deletion scope |

No actual case or consent is recorded by this template. Do not upload private recordings or commit them to Git. Source animals/media availability is awaiting the owner's answer; no filesystem search for personal pet media has occurred.

## Bounded experiment after prerequisites

An initial proposal is **one cat and one dog**, one initial attempt and at most one correction each. That is at most four reconstruction attempts if separately approved and funded, not an authorized job count. Two exploratory cases cannot pass the 20-pet-per-path G-I cohort requirement.

Before execution, the [R0 plan](../everkio_reconstruction_feasibility_plan.md#r0--freeze-numerical-budget-and-protocol) still requires numerical funding, case/attempt/runtime/storage/egress caps, contingency, concurrency and enforced dispatch/reservation limits. All remain UNSET. No cost estimate in this packet supplies approval or an enforceable ceiling. A free local experiment is not an automatic waiver of the owner's funded-research prerequisite. Rights and retention must also be frozen before intake.

When those prerequisites are documented:

1. Pin one cleared pipeline and every dependency/weight/template revision; inspect scripts before running and use an isolated environment. Do not run upstream destructive environment commands in the existing Everkio environments.
2. Lock case eligibility, source hashes and held-out comparisons. Report absent views and inferred appearance.
3. Fit within the actual approved limits, retaining failures, original output, cost/runtime and any correction separately. No automatic retries or broader-model training.
4. Inspect held-out views, both body sides, face, coat, eyes, fur and topology; then inspect deformation, planted feet and all required motion. Existing failed sit/lie drafts remain rejected.
5. Produce an editable mesh/rig/material/LOD inventory and a separate iPhone preflight, recording conversion losses and thermal/performance effects. The current main diagnostic scene remains animal/AR-free until its gates permit integration.
6. Report exploration as PARTIAL/FAIL as appropriate. Full G-P/G-I requires its own device matrix, calibrated timing, independent review and cohort; attractive stills or these two cases cannot pass it.

## What is actually established

Public code/README/license text was inspected and pinned; no environment was installed, model/data weights acquired, reference media ingested, inference/training/reconstruction run or GPU provisioned. Existing AI-generated meshes and device clip exports remain the only animal build evidence. Their realism remains unaccepted. M0 is PARTIAL; M1–M3 and all product gates remain NOT RUN.
