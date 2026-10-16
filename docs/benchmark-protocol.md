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

The spec permits 100 touches aggregated across three sessions. The single-run inspector conservatively returns PARTIAL for fewer samples; `tools/benchmark_series.py` now supports a numerical series for one animal/device. `tools/presence_ratings.py` now checks one frozen cat/dog clip pair and its anonymous ratings. Full gate automation remains unimplemented. Do not fabricate events to make either inspector pass.

## Unity recorder limitations
`PresenceRecorder` collects **Update cadence**, not display presentation. The package deliberately declares `unity_update_proxy` and does not create touch measurements. The original device captures wrote thermal state as `unknown`; the subsequent iOS bridge samples `NSProcessInfo.thermalState` for every recorded Update. Editor, simulator and unsupported native values remain `unknown`. The optional manifest field `thermal_method` records the provider (`ios_nsprocessinfo_thermalstate_per_update` or `unavailable`). Thermal state is an OS category, not a temperature measurement or an independent OS-warning/crash declaration. A recorder export cannot pass the inspector as acceptance evidence. Native nominal thermal sampling was verified in both a short physical-device smoke capture and a complete 600-second diagnostic (35,973 nominal samples; see status log). Thermal transitions, instrumentation overhead and timing against independent device presentation/high-speed video remain unvalidated before scored animal runs.

The recorder uses [Unity's monotonic realtime API](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Time-realtimeSinceStartupAsDouble.html), [battery level](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SystemInfo-batteryLevel.html), and [Unity allocated memory](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Profiling.Profiler.GetTotalAllocatedMemoryLong.html). Allocated Unity memory is not total process resident memory; battery may be unavailable. Sources reviewed 2026-10-15. C# compilation, iOS launch and completed and interrupted real-device capture/export/analysis were verified on that date; see [actual run results](m0-status.md). This does not validate presentation timing, touch latency, thermal transitions or instrumentation overhead; the native nominal-thermal export path is verified separately.

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

Room/lighting identifiers must accompany actual animal runs after the layouts are documented. Warm-up remains the existing 30-second draft pending animal load/measurement calibration and protocol freeze. Record battery health/date (owner reported 75% Maximum Capacity on October 16), actual run-start charge, ambient context, presentation/touch validation method and thermal/overhead calibration before scored runs. Health percentage must never populate the `battery_level` charge column. Wired diagnostic battery increases do not qualify as battery-drain measurements. These conditions do not waive usable animal quality, source/output rights or the remaining calibration requirements. AI generation is the selected asset direction; stock procurement is optional and spending is unapproved.


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


## Independent presentation trace preparation

A short Metal System Trace capture/export and process-attributed displayed-surface inspection now work on the baseline phone; see [the reproducible setup commands](mac-quickstart.md#presentation-measurement-setup-checks). `tools/metal_trace.py` deliberately outputs PARTIAL / G-P NOT RUN. Its reported swap p95/worst describe only the supplied attributed rows, without asserting full-session continuity, frozen conditions, recorder-clock correlation or calibrated overhead. A 15-second idle trace cannot replace three 600-second animal sessions. CPU-to-display latency is not input-to-visible latency, and HUD logging is a separate workload. Earlier raw captures keep their original timing declarations.


## Blinded rating analysis preparation

Use the [empty study template](../benchmarks/ratings-template/README.md) with actual consented, blinded data when approved clips and study conditions are ready. No cohort study has run. Freeze the anonymous enrolled cohort, method and clip hashes before collection. The analyzer includes every enrolled ID in each denominator, reports explicit abstentions separately, flags missing responses and requires at least 20 respondent IDs; participation and identity are independently reviewed. Each animal's realism, room presence and natural motion must separately have at least 80% ratings ≥4/5; exact integer comparisons avoid rounding at the boundary. Clip order is balanced cat-first/dog-first, and each evaluator sees the two positions once.

```sh
python3 tools/presence_ratings.py benchmarks/runs/private-study \
  --output benchmarks/runs/private-study-report.json
```

The output is new and immutable. Input hashes bind the manifest, CSV and referenced clip files; mismatches, duplicate responses, unknown cohort IDs, reused clips, invalid scores and escaping paths are rejected. `physical_device` / `animal_presence` and nonempty provenance references are declarations, not authenticity verification. Missing declarations or diagnostic/desktop inputs cannot receive a complete numerical result. The tool cannot validate participants, consent, blinding, free-text defects, clip contents or independent review, and **always leaves G-P NOT RUN**. Preserve qualitative notes and failed/abstained cases for manual review; synthetic fixtures are tests only.

## Input-marker setup fixture — uncalibrated

The diagnostic panel now has **Start input marker setup**, separate from timing captures and screenshots. It shows a blue/yellow field and numbered event. Each pointer-down within that field requests a colour/counter change and stores Unity's receipt time and frame index. Stop exports up to 250 receipts to `Documents/EverkioDiagnostics/InputMarkers/<run-id>/`; focus loss, pause or disabling exports an interrupted fixture. Abrupt OS termination can still lose the in-memory run. Starting this mode prevents a concurrent timing capture; its GUI/export work must not contaminate a scored run.

The immutable bundle is `manifest.json` plus `pointer-receipts.csv` (`event_id,unity_receipt_ms,requested_marker_state,unity_frame_index`). The manifest declares `input_marker_setup_only`, `unity_imgui_pointer_receipt_only`, `calibration_validated=false`, instrumentation-only scene and G-P NOT RUN. A completed fixture means the operator finished its export; even 250 receipts supply **no validated latency observations**. There is no `visible_ms`, no generated `touches.csv`, no hardware-contact timestamp and no inferred first visible frame. Synthetic editor checks validate sequence, clock guards and capacity only; they create no device measurements.

For a physical setup smoke check, start the mode, tap the coloured field five times, confirm the number/colour changes, then press **Stop and export marker setup**. Copy the folder and check counts, monotonically increasing receipt times, event IDs, requested states and interruption flags. This verifies local pointer/UI/export plumbing only. IMGUI touch-to-pointer delivery on the pinned iPhone build must be observed; the editor self-check cannot establish it.

Latency calibration still requires independently recording **both finger contact and screen response**, documenting source timestamps/frame rate, exposure/rolling-shutter effects, dropped frames and uncertainty. A screen recording excludes physical contact; the app's requested marker state does not establish presentation. An external camera may support method development, but an unvalidated camera/frame rate cannot silently become a precision timing instrument. Match numbered events, retain raw footage and bracket earliest/latest plausible contact/response before any timing claim. These receipt times are not aligned to benchmark capture clocks automatically. A marker test never replaces actual animal input-to-visible-response observations or the required scored session coverage.

Implementation sources checked October 16 (Context7 unavailable): Unity [pointer-down event](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/EventType.MouseDown.html), [IMGUI pointer coordinates](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Event-mousePosition.html) and [event consumption](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Event.Use.html). Exact 6000.6.6f1 compilation/device results belong in the status log; these references alone establish no physical timing behavior.
