# Everkio

**Feel their presence.** Photorealistic AI companions in augmented reality.

Roadmap: **Everkio Pets → Everkio Spatial → Everkio People**.

Implementation has started with M0 benchmark foundations and a Unity 6000.6.6f1 diagnostic project. This repository is **not yet a runnable AR application**. Unity compilation, iOS development build/signing and physical iPhone launch are verified. The diagnostic capture/export/analysis path is verified on a complete 600-second run; accepted AI-generated animals, AR and product acceptance remain pending. See [current handoff and blockers](docs/m0-status.md) and the [master specification](everkio_master_spec_v2.md).

## Run the local checks

Python 3.10+; standard library only, no installation or cloud credentials:

```sh
python3 -m unittest discover -s tests -v
python3 tools/benchmark.py /path/to/run --output /path/to/new-report.json
```

Exit codes: 0 = single-run numerical checks passed; 1 = incomplete or failing evidence; 2 = invalid input or IO error. No report grants G-P acceptance. The output file must not already exist, preventing accidental evidence overwrite.

## Contents

- `tools/benchmark.py`: validates local captures, computes p95 intervals, one-minute FPS, touch upper bounds, memory/battery summaries and evidence hashes.
- `tools/benchmark_series.py`: inspects one animal/device across at least three sessions, pools touch observations and preserves individual failures; never grants G-P.
- `tools/metal_trace.py`: inspects process-attributed displayed-surface swap intervals from an Instruments XML export; always PARTIAL, with no recorder calibration or G-P claim.
- `tools/telemetry_cost.py`: checks clock-only/telemetry raw cost pairs from the opt-in device probe; always PARTIAL and never full instrumentation-overhead calibration.
- `benchmarks/templates/`: capture manifest and CSV contracts, with unknown values left unknown.
- `unity/Everkio/`: pinned diagnostic project with an editor-generated instrumentation scene.
- `unity/Packages/com.everkio.benchmarks/`: local recorder and diagnostic controls; compiled and exercised on iPhone with diagnostic evidence only.
- `InputMarkerPanel`: independent-recording setup with numbered colour changes and receipt-only exports; no latency validation is implied.
- `tools/unity_project.py`: source check, prepare, validate and guarded iOS export commands.
- `tools/presence_ratings.py`: frozen-cohort blinded rating checks with separate species/dimension thresholds; never grants G-P.
- `tools/generate_animal.py`: pinned local CPU AI-to-3D evaluation with model/config checksums and immutable outputs; no accepted animal rig is implied.
- `tools/prepare_animal_rig.py`: pinned Blender draft quadruped preparation with source/fit guards, optional per-animal head/neck/tail joints and orderly Rigify UI cleanup; tested on both generated animals, without claiming motion/realism acceptance.
- `tools/author_animal_motion.py`: idle/head-look, reaction/head-lowering, planted-turn and start/walk/stop draft authoring tied to source hashes with measured loops, surface holds and explicit floor failures; no natural-motion acceptance.
- [AI animal generation](docs/ai-animal-generation.md): original references, reproducible local workflow, generated mesh evidence and actual quality defects.
- [Real-media evaluation](docs/real-media-evaluation.md): pinned candidate/rights/hardware review and proposed photo/video workflow; reconstruction execution remains unfunded and NOT RUN.
- [Mac quickstart](docs/mac-quickstart.md): exact commands to compile and export for your iPhone.
- [Benchmark protocol](docs/benchmark-protocol.md): methods, limitations and interpretation.
- [Linux/Mac development workflow](docs/development-setup.md): shared source, Mac/iPhone build and validation path.

Current work remains at M0–M3 prerequisites. Decision D14 conditionally authorizes M4–M14 after their prerequisite gates pass, with spending still unapproved; it grants no public/commercial launch approval. Production behavior, accounts, uploads, payments, persistent memory, headsets and humans have not passed their prerequisites. Parallel reconstruction research still requires the documented funded budget and enforcement controls; no billable research has started.
