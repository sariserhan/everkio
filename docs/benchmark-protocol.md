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

The spec permits 100 touches aggregated across three sessions. The single-run inspector conservatively returns PARTIAL for fewer samples; `tools/benchmark_series.py` now supports a numerical series for one animal/device. Blinded rating aggregation and full gate automation remain unimplemented. Do not fabricate events to make either inspector pass.

## Unity recorder limitations
`PresenceRecorder` collects **Update cadence**, not display presentation. The package deliberately declares `unity_update_proxy` and does not create touch measurements. The original device captures wrote thermal state as `unknown`; the subsequent iOS bridge samples `NSProcessInfo.thermalState` for every recorded Update. Editor, simulator and unsupported native values remain `unknown`. The optional manifest field `thermal_method` records the provider (`ios_nsprocessinfo_thermalstate_per_update` or `unavailable`). Thermal state is an OS category, not a temperature measurement or an independent OS-warning/crash declaration. A recorder export cannot pass the inspector as acceptance evidence. Native nominal thermal sampling was verified in a short physical-device smoke capture (see status log); validate transitions and profile instrumentation overhead and validate timing against device presentation/high-speed video before scored animal runs.

The recorder uses [Unity's monotonic realtime API](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Time-realtimeSinceStartupAsDouble.html), [battery level](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SystemInfo-batteryLevel.html), and [Unity allocated memory](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Profiling.Profiler.GetTotalAllocatedMemoryLong.html). Allocated Unity memory is not total process resident memory; battery may be unavailable. Sources reviewed 2026-10-15. C# compilation, iOS launch and completed and interrupted real-device capture/export/analysis were verified on that date; see [actual run results](m0-status.md). This does not validate presentation timing, touch latency or thermal sampling.

The initial warm-up default is 30 seconds and is marked draft, not a frozen study decision. Captures are limited to 600–1800 seconds and 500,000 samples, stored in memory then written after capture to avoid per-frame disk IO. Instrumentation overhead and list memory must be profiled before scored runs. Pausing, focus loss, disabling or manual stopping records an incomplete capture. Abrupt OS termination can lose the in-memory capture; absent/incomplete evidence never counts as a pass. Add crash-resilient recording only after measuring its overhead.

No recorder code requests camera/microphone permissions, uploads data, calls inference, or starts automatically. A successful offline trace and explicit operator review are still required; absence of network code in this component does not prove the whole future app is offline.


## iOS thermal bridge and capture progress

The local package includes an Objective-C++ iOS plug-in and a C# bridge. State names map explicitly to the existing CSV contract; unknown and future values do not become nominal. The editor validation command checks known state names, an invalid value and the unsupported/editor fallback. Python's thermal tests still reject serious/critical samples and mark unknown coverage incomplete.

Implementation references: [Apple thermal state](https://developer.apple.com/documentation/foundation/processinfo/thermalstate-swift.enum) and [Unity native plug-in integration](https://docs.unity.com/en-us/engine/6000.3/manual/platform-specific/iphone/ios-developing/plugins-for-ios/ios-native-plugin-use/automated-integration). Official sources checked October 15, 2026; exact Unity 6000.6 behavior is established by export/build/device checks in the [status log](m0-status.md). Context7 MCP was unavailable in this session.

The panel shows separate warm-up and capture countdowns, sample count and current thermal state, inside a scrollable safe area. `Capture complete` remains the only completion indication; Stop, focus loss and backgrounding still preserve an incomplete run. Start logs include the run ID, species label and configured durations so monitoring need not infer start from a later export. Countdown rendering and native queries add instrumentation work; their overhead is not yet calibrated against an independent presentation clock.


## Selected study conditions — owner confirmation October 15, 2026

Serhan Sari confirmed the living room for the proposed open-floor/furnished configurations and daylight/artificial-evening lighting. These are two configurations of one room, not two independently tested rooms. This selects conditions; it does not claim they have been prepared or evaluated with animals.

| ID | Condition | Record before a scored run |
|---|---|---|
| R1 | Living room, open floor area | Mark placement, route, camera orbit and floor scale reference; preserve a private setup photo/diagram |
| R2 | Living room, furnished area | Mark furniture/occlusion boundaries and tracking-interruption route; preserve a private setup photo/diagram |
| L1 | Daylight | Date/time, window/blind positions, ambient conditions and starting device thermal state |
| L2 | Artificial evening light | Lights used and positions, ambient conditions and starting device thermal state |

Room/lighting identifiers must accompany actual animal runs after the layouts are documented. Warm-up remains the existing 30-second draft pending animal load/measurement calibration and protocol freeze. Battery health/start charge, ambient context, presentation/touch validation method and continuous native thermal validation still need recording before scored runs. Wired diagnostic battery increases do not qualify as battery-drain measurements. These conditions do not remove the licensed-asset or procurement blockers.


## Diagnostic visual evidence

The screenshot button exports the current Unity-rendered diagnostic app view to an immutable UUID-named PNG after end-of-frame rendering. It is available only outside active benchmark runs. The two added dependencies are built-in Unity ScreenCapture and ImageConversion modules, pinned to `1.0.0`; there is no external capture service or Photos permission. Editor validation checks that PNG encoding produces the expected signature, while physical screenshot/export/visual verification is recorded separately in [M0 status](m0-status.md).

[Unity's screenshot API](https://docs.unity3d.com/6000.6/Documentation/ScriptReference/ScreenCapture.CaptureScreenshotAsTexture.html) requires capture after rendering; an end-of-frame coroutine supplies that point. This is a rendered app image, not independent physical-presentation or touch-latency proof. An empty diagnostic screenshot cannot meet animal/AR motion or realism requirements. Video recording and future product capture/sharing remain unimplemented.


## Numerical three-session inspection

```sh
mkdir -p benchmarks/reports
python3 tools/benchmark_series.py /path/to/run-1 /path/to/run-2 /path/to/run-3   --output benchmarks/reports/new-series.json
```

The output directory must exist and the report must be new. Use separate series for cat and dog, and for each device/OS/build/asset/protocol/warm-up/timing/thermal method. Mixing these configurations is rejected rather than pooled. Room and lighting may vary; at least two named configurations and two named lighting conditions across at least three sessions are required. A publisher/asset change needs a new series.

The series inspector retains every supplied single-run report, failure, missing field and evidence hash. It replaces only the single-run 100-touch minimum with a pooled minimum of 100 validated observations. Each session must still contain touch observations and satisfy its own latency bound; a pooled percentile cannot hide a failing individual session. Existing conservative offline/network declarations are still required for each supplied run. It rejects repeated directories, run IDs and identical frame files, and detects input changes during inspection. These checks do not authenticate operator declarations or prove the source files are genuine.

All supplied failed/incomplete runs remain in the result; there is no best-three selection or splicing of interrupted sessions. Missing evidence remains PARTIAL, observed failures remain FAIL, and mixed/malformed/duplicate evidence is rejected with exit 2. A PASS is only a numerical-series result: **G-P always remains NOT RUN** until separate cat/dog device evidence, independent motion/AR review and blinded evaluation pass. Synthetic test fixtures are not experimental evidence.
