# M0 benchmark contract v1

This implementation supports preparation for [M0–M3](../everkio_m0_m3_execution_plan.md); it does not replace that plan's three runs, room/lighting coverage, blinded reviewers or G-P decision.

## Capture bundle
Each run is an immutable directory containing `manifest.json`, `frames.csv`, and optional `touches.csv`. Use the templates under `benchmarks/templates`. Generated raw exports belong in ignored `benchmarks/runs/` or another private evidence store. Preserve all runs, including failures. Record archive locations/digests in the milestone handoff.

- `scene_content` must be `animal_presence` for numerical acceptance; the M0 diagnostic scene writes `instrumentation_only` and cannot qualify.
- Manifest schema version 1 records protocol, operator, cat/dog, device/OS/build, asset digest, room/lighting, warm-up policy, evidence kind and measurement provenance. Unknown flags/counts remain null or absent; never substitute zero/true.
- `frames.csv`: sequential `frame_index` from zero, strictly increasing `elapsed_ms` starting at zero, `memory_mb`, `battery_level` in [0,1], and thermal state (`unknown`, `nominal`, `fair`, `serious`, `critical`). Blank memory/battery means missing. All elapsed samples use the same monotonic clock after warm-up.
- `touches.csv`: unique `event_id`, `input_ms`, `visible_ms`, `uncertainty_ms`. Times use the capture clock. These must be actual externally validated input-to-visible observations; animation dispatch timestamps do not suffice.

The inspector calculates nearest-rank p95 from adjacent timestamps. One-minute FPS counts completed intervals in `(start, end]`, so a long stall cannot disappear behind a favorable p95. The trailing partial minute is reported but not scored as a full minute. Touch p95 uses latency plus measurement uncertainty and must be strictly below 100 ms. Frame p95 must be ≤33.3 ms, each complete minute ≥30 FPS, and scored duration ≥600 seconds.

Numerical PASS requires physical-device metadata, validated presentation timing, completion, ≥100 touch events in this bundle, thermal coverage, memory and battery endpoints, zero reported chargeable inference/crashes/interruptions/warnings, and offline/network review. Missing inputs yield PARTIAL; measured violations yield FAIL; malformed evidence is rejected. These are evidence declarations, not authenticity verification. The inspector cannot independently validate an operator's claims or a referenced video. It **always leaves G-P NOT RUN** for human/cohort review.

The spec permits 100 touches aggregated across three sessions; this first inspector only supports a single bundle and conservatively returns PARTIAL for fewer samples. Cross-run aggregation, blinded rating aggregation and full gate automation are not implemented. Do not fabricate events to make the inspector pass.

## Unity recorder limitations
`PresenceRecorder` collects **Update cadence**, not display presentation. The package deliberately declares `unity_update_proxy`, writes thermal state as `unknown`, and does not create touch measurements. A recorder export cannot pass the inspector as acceptance evidence. Complete iOS native thermal capture and validate timing against device presentation/high-speed video during later authorized work.

The recorder uses [Unity's monotonic realtime API](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Time-realtimeSinceStartupAsDouble.html), [battery level](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SystemInfo-batteryLevel.html), and [Unity allocated memory](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Profiling.Profiler.GetTotalAllocatedMemoryLong.html). Allocated Unity memory is not total process resident memory; battery may be unavailable. Sources reviewed 2026-10-15. C# compilation, iOS launch and completed and interrupted real-device capture/export/analysis were verified on that date; see [actual run results](m0-status.md). This does not validate presentation timing, touch latency or thermal sampling.

The initial warm-up default is 30 seconds and is marked draft, not a frozen study decision. Captures are limited to 600–1800 seconds and 500,000 samples, stored in memory then written after capture to avoid per-frame disk IO. Instrumentation overhead and list memory must be profiled before scored runs. Pausing, focus loss, disabling or manual stopping records an incomplete capture. Abrupt OS termination can lose the in-memory capture; absent/incomplete evidence never counts as a pass. Add crash-resilient recording only after measuring its overhead.

No recorder code requests camera/microphone permissions, uploads data, calls inference, or starts automatically. A successful offline trace and explicit operator review are still required; absence of network code in this component does not prove the whole future app is offline.
