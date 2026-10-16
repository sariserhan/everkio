# Everkio

**Feel their presence.** Photorealistic AI companions in augmented reality.

Roadmap: **Everkio Pets → Everkio Spatial → Everkio People**.

Implementation has started with M0 benchmark foundations and a Unity 6000.6.6f1 diagnostic project. This repository is **not yet a runnable AR application**. Unity compilation, iOS development build/signing and physical iPhone launch are verified. Licensed animals, AR and product acceptance remain pending. See [current handoff and blockers](docs/m0-status.md) and the [master specification](everkio_master_spec_v2.md).

## Run the local checks

Python 3.10+; standard library only, no installation or cloud credentials:

```sh
python3 -m unittest discover -s tests -v
python3 tools/benchmark.py /path/to/run --output /path/to/new-report.json
```

Exit codes: 0 = single-run numerical checks passed; 1 = incomplete or failing evidence; 2 = invalid input or IO error. No report grants G-P acceptance. The output file must not already exist, preventing accidental evidence overwrite.

## Contents

- `tools/benchmark.py`: validates local captures, computes p95 intervals, one-minute FPS, touch upper bounds, memory/battery summaries and evidence hashes.
- `benchmarks/templates/`: capture manifest and CSV contracts, with unknown values left unknown.
- `unity/Everkio/`: pinned diagnostic project with an editor-generated instrumentation scene.
- `unity/Packages/com.everkio.benchmarks/`: local recorder and diagnostic controls; compiled and exercised on iPhone with diagnostic evidence only.
- `tools/unity_project.py`: source check, prepare, validate and guarded iOS export commands.
- [Mac quickstart](docs/mac-quickstart.md): exact commands to compile and export for your iPhone.
- [Benchmark protocol](docs/benchmark-protocol.md): methods, limitations and interpretation.
- [Linux/Mac development workflow](docs/development-setup.md): shared source, Mac/iPhone build and validation path.

Active implementation is M0–M3 only. Production behavior, accounts, uploads, payments, persistent memory, headsets and humans remain deferred. Parallel reconstruction research requires the documented funded budget and enforcement prerequisites; no billable research has started.
