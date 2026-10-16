# M0 handoff — 2026-10-15

**M0: PARTIAL. M1–M3: NOT RUN. G-P/G-I/G-F/G-M: NOT RUN.**

## Delivered
- Initialized a local Git repository on `main`; no remote or public publication.
- Added dependency-free Python capture inspection, CSV/manifest contracts and a Unity diagnostic recorder package.
- Added repeatable local tests and Linux/Mac setup instructions.
- Added a Unity 6000.6.6f1 project skeleton, diagnostic scene generator and device-facing capture controls.
- Added guarded prepare/validate/iOS-export commands with unique logs, completion checks and overwrite protection. See [Mac quickstart](mac-quickstart.md).
- Preserved implementation limits and stricter evidence criteria; no synthetic results count toward device gates.

## Initial Linux verification (historical)
`python3 -m unittest discover -s tests -v`: **29 tests passed** on the current Linux host. Tests exercise percentile/window logic, stalled frames, invalid timestamps, missing evidence, thermal conditions, uncertainty at the latency boundary, inference violations, interrupted captures and evidence overwrite protection. All fixtures are synthetic and temporary. Build-runner tests mock Unity and verify argument boundaries, exact editor pinning, overwrite/lock protection and rejection of a zero exit without a completion marker; these are not Unity compile tests.

Unity compilation, editor tests, iOS build/install, asset rendering, actual FPS/latency/memory/battery/thermals and any owner identity evaluation: **NOT RUN**. No Unity editor or .NET compiler was found in the inspected environment. This is benchmark tooling, not an AR app demo.

## Blockers and next actions
| Blocker | Evidence so far | Next action / responsible role |
|---|---|---|
| Baseline iPhone and test environment | iPhone 14 Pro; iOS 26.6.2 explicitly reconfirmed by user; baseline candidate | Verify installed OS/build and freeze device/room/lighting matrix |
| Mac/Xcode build host | Apple silicon Mac, macOS 26.6.2, Xcode 27.0, Unity 6000.6.6f1 with iOS Build Support and developer account confirmed | Compile with confirmed editor and verify iPhone deployment/signing |
| Named owners | Serhan Sari confirmed engineering, art/licensing and testing ownership during live Mac execution | Owner coordinates procurement and protocol freeze |
| Licensed cat/dog assets | No assets in repository; rights unknown | Art owner selects assets with rig/motion/fur coverage and redistribution terms within approved procurement limit |
| Timing/thermal validation | Update proxy only; thermal unknown | Engineering validates device presentation/input method and native thermal telemetry |
| Protocol freeze | Thresholds documented; warm-up, rooms and battery context not frozen | Test owner records conditions and protocol revision before scoring |
| Research funding | Numerical caps/funding/vendors/cohort remain unset | Product/finance/research owners complete R0; no billable research starts |

No paid services were invoked, assets purchased, cloud resources provisioned, or reconstruction jobs dispatched. Current work adds no accounts, payments, production behavior, personal-media intake or future-phase implementation.

After missing M0 inputs are resolved, validate the Unity package in the chosen editor, freeze dependencies, and record M0's gate decision before M1/M2 work. Generic animal motion and AR still require licensed assets and real-device evidence. Do not bypass these prerequisites with a cartoon or browser mockup.


## Supplied installation inventory (before live verification)
User confirms Unity **6000.6.6f1** with **iOS Build Support**, Xcode **27.0** (27A266a), Apple silicon Mac on macOS **26.6.2** (25G83), and iPhone 14 Pro on iOS **26.6.2**. The source project is pinned to the confirmed editor; compile, signing and physical-device deployment remain NOT RUN.


## Live Mac execution — 2026-10-15 (America/New_York)

Source baseline: `533143a`; local `main` and fetched `origin/main` agree at that commit before this work. Remote exists at `github.com/sariserhan/everkio`; the original no-remote statement above describes repository initialization only. Pre-existing generated Unity settings/scene/lockfile were preserved and reviewed. No push or publication performed.

### Observed environment

- Apple silicon `arm64`; macOS 26.6.2 (25G83).
- Xcode 27.0 (27A266a), selected at `/Applications/Xcode.app/Contents/Developer`; iOS SDK 27.0.
- Python 3.14.6; Unity 6000.6.6f1 (d20c9ac777da).
- Connected **physical iPhone 14 Pro (iPhone15,2)**, iOS 26.6.2 (23G90), wired/paired, Developer Mode enabled. Identifiers remain in ignored local evidence.
- Product owner approved the local SERHAN SARI development team and `com.serhansari.everkio.diagnostics`. Signing identity, provisioning and private keys remain local; no credentials committed.

### Commands and actual results

| Check | Result | Local evidence (ignored `artifacts/`) |
|---|---|---|
| `python3 -m unittest discover -s tests -v` | PASS — 29 tests on this Mac; fixtures are synthetic | `python-tests.log` |
| `python3 tools/unity_project.py prepare` | PASS — completion marker, existing diagnostic scene preserved | `prepare-20261015T235814Z-dc3905ed.log` and `.json` |
| `python3 tools/unity_project.py validate` | PASS — editor method compiled and executed | `validate-20261015T235854Z-1bc82e26.log` and `.json` |
| First `export-ios` | FAIL — iOS target not activated; iOS Build Support absent on disk | `export-ios-20261015T235929Z-160721e2.log` and `.json` |
| Unity Hub module install | PASS — official Hub CLI installed matching iOS support; initial database-lock warnings recovered | `unity-ios-module-install.log` |
| Second export attempt | Blocked by stale lock from failed batch; no running editor or open file holder found; lock archived rather than deleted | `stale-lock-after-failed-ios-export` |
| Retry `export-ios` to `artifacts/ios-diagnostics-002` | PASS — Development/IL2CPP export and expected Xcode project; includes clearer missing-module error | `export-ios-20261016T000032Z-560bb141.log` and `.json` |
| Xcode build, development signing | PASS — exit 0, `BUILD SUCCEEDED` | `xcode-build-002.log` |
| Physical-device install/launch | PASS — app installed, process launched, Metal/scene initialized | `device-install-002.json`, `device-processes-during-capture.json`, `device-console-002.log` |
| App-container copy preflight | PASS — copied empty Documents directory; this does not validate a capture | `device-copy-preflight-003.json` / `.log` |
| Diagnostic capture → export → analysis | PASS for pipeline execution — one automatic 600-second run and two interrupted runs saved/copied/analyzed; presence inspection PARTIAL/FAIL as expected | `device-capture-copy-001/002/003.json`, `diagnostic-analysis-001/002/003.json` |

The 20261016 UTC log filenames are still October 15 in New York. The Python log contains an intentional mocked runner failure within a passing test; it is not a live Unity failure. Actual first-export failure is preserved separately.

### Gate and next blockers

**M0 remains PARTIAL; M1–M3 and G-P/G-I/G-F/G-M remain NOT RUN.** Compilation and Xcode export establish tooling progress only. The diagnostic scene contains no animal or AR; Update cadence, unknown thermal state and absent touch measurements cannot establish presence acceptance.

The [asset plan and shortlist](asset-plan.md) records candidates and required rights/motion/mobile checks. Product owner explicitly approved shortlist preparation only, with **no spending approved**. No animal asset is selected, licensed or imported. Resolve selection, procurement ceiling and rights before animal/AR implementation. Two rooms/two lighting conditions, warm-up/protocol freeze, battery/ambient context and validated timing/thermal method remain open. Flagship hardware/60 FPS remain NOT RUN.

Research funding and hard spending controls remain unset. No paid services, purchases, cloud provisioning, reconstruction jobs or M4–M14 work performed.


Build notes: Xcode emitted Unity-generated deprecation warnings, an absent App Store icon warning and an always-run build-script warning. These did not block this local development build; App Store submission is outside scope. The player console reports A16/Metal initialization and a nominal thermal notification at launch, but this is not continuous native thermal evidence in the recorder. Development-player UDP discovery is visible in the console; no offline/no-network claim has been validated. No launch exception was observed in the inspected startup log. Operator confirmed the phone panel is visible and started a cat-labelled diagnostic capture.


Build evidence index: `artifacts/build-evidence-002.json` records SHA-256 hashes of editor/recorder/panel source, scene, package lock, export report, generated Xcode project and signed executable/framework. Installed diagnostic executable SHA-256: `a0f76ecbc18bf7d1d22b4710cf5e5a5a532bf97fff92d0dbca2319ea3a91367e`. Raw logs, device identifiers, generated Xcode project, signing output and captures remain ignored/private in this local checkout; they have not been published or placed in a durable external evidence store. Preserve this directory for reproducibility. No animal-presence scored run has begun; the in-progress diagnostic run is separate.

Copy preflight initially failed because `devicectl` requires the destination directory to exist (`device-copy-preflight-002.log`); creating a fresh destination fixed it. Quickstart now includes this step. The app's Documents directory was empty at inspection, so full recorder export and numerical analysis still await a real capture. This is a pending physical-device action, not a passed pipeline test.


Operator confirmed iOS Build Support is installed and the phone's diagnostic panel is visible, then started a cat-labelled capture. The app was observed running as PID 4222. `device-processes-during-capture.json` is the launch/process evidence; the attached console's launch JSON is only finalized when that command exits and was not yet present. Do not terminate the console during capture. The current run is diagnostic instrumentation, not cat rendering or a scored presence session.


Owner decision: Serhan Sari confirmed responsibility for engineering, art/licensing and testing. The reply did not identify rooms or lighting conditions; those stay unresolved rather than inferred. Independent M3 reviewers and blinded evaluators still need recruitment; owner assignment does not replace those requirements.


### Actual diagnostic capture 001 — interrupted

- Run ID: `20261016T000346-20c1f818b095483796a98ffb1939d151`; local capture started at 20:03:46 New York, October 15. Device-produced raw files copied unchanged to `artifacts/device-captures-001/<run-id>/`.
- Manifest: iPhone15,2, iOS 26.6.2; Unity build GUID `c84c9111ec10425396ea57469f65bcf4`; `scene_content=instrumentation_only`, `timing_method=unity_update_proxy`, `evidence_kind=unverified_player`. External device inventory/operator confirmation establishes physical provenance for this diagnostic, but raw declarations were not rewritten to make it pass.
- Stop: `completed=false`, `interruptions=1`, `stop_reason=operator_stop`. The console stack shows `DiagnosticPanel.OnGUI → StopCapture → Finish`, rather than an inferred crash. Preserve this incomplete run.
- 3,768 samples / 3,767 intervals over **62.832661 seconds** after warm-up. Update-interval p95 **16.756167 ms**, worst **19.266458 ms**; first full-minute Update cadence **59.95 FPS**. These are short, empty-scene instrumentation measurements, not sustained animal rendering or display-presentation results.
- Peak Unity allocated memory **70.0992 MiB** (not total resident process memory); reported battery change **0.0** while wired. No battery-drain conclusion is supported. Every recorded thermal sample remains `unknown`; zero touch samples.
- `python3 tools/benchmark.py artifacts/device-captures-001/<run-id> --output artifacts/diagnostic-analysis-001.json` produced **FAIL** with `interruptions`, missing duration/completion and other required evidence; G-P remains **NOT RUN**. The inspector accepted the real CSV/manifest format and generated hashes. This verifies the interrupted capture → device storage → Mac copy → analysis path, not the automatic full-duration completion path.
- Raw SHA-256: manifest `14d9775ae062e76f0d4d3e21749e34c02ca217734114e18c9c737cbfea293d8c`; frames `7b9d8dad204b4540b412b8a0f0887c72ac7953cf26466a3d61d42310a62e6430`.

Operator confirmed another capture was running and intended to leave it foregrounded through automatic completion. The next saved manifest is dog-labelled (not cat-labelled); the raw label is retained below. No milestone/gate status changed.


### Actual diagnostic capture 002 — focus-loss interruption

- Run ID: `20261016T000533-42ee1bbec1154fd69c166f80bf301e67`, dog-labelled instrumentation. Raw copied unchanged to `artifacts/device-captures-002/<run-id>/`; this second copy also includes the earlier run.
- Manifest: same physical device/OS/build as run 001; `completed=false`, `interruptions=1`, `stop_reason=focus_loss`. Console shows `applicationWillResignActive`, `OnApplicationFocus → Finish`, then application backgrounding. What caused the focus loss is not established. No automatic resumption or evidence splicing performed.
- **32,845 samples / 32,844 intervals over 547.829823 seconds**, about 52.17 seconds short of the required capture duration. Update-interval p95 **16.913375 ms**, worst **24.0085 ms**. Nine complete one-minute windows are **59.95–59.9667 Update FPS**; the final partial window is unscored. These are empty-scene proxy measurements, not animal/AR/display performance acceptance.
- Peak Unity allocated memory **70.1330 MiB**; battery increased by **0.05** while wired. No battery-drain inference. Thermal samples remain `unknown`, with no touch observations.
- Inspector output `artifacts/diagnostic-analysis-002.json`: **FAIL** (`interruptions`, plus missing completion/duration and other evidence); expected CLI exit **1**, not malformed-input exit 2. G-P remains **NOT RUN**. Copy log/result: `device-capture-copy-002.log` / `.json`.
- Raw SHA-256: manifest `5d78059f82967d9f20299ddeaf7202e24528a6bd64bb0956038c6146963935be`; frames `bfdc9f4e77b7cdc231d6e3a0e34ad74a0f3aa5b51d9fe9932f406bafd02c39e8`.

The interrupted device capture/export/analysis pipeline is verified twice. **At this point, the automatic full-duration completion path was still unverified (resolved by run 003 below)**; next physical action is a fresh run kept foregrounded through “Capture complete.” Do not combine interrupted runs or shorten the acceptance duration. The app's interruption behavior worked as designed and has not been relaxed to produce a favorable result.

Private evidence archive: `artifacts/m0-device-evidence-interrupted-001.zip`, SHA-256 `964e862305958732076f3533f617254d123b493a7355256c71eb784f7e694526`. Includes both unchanged interrupted bundles, their analysis reports, device/build provenance and a snapshot of logs. Archive is ignored and contains device identifiers; no external sharing performed. It is a local preservation copy, not a backup on a separate host.


### Actual diagnostic capture 003 — automatic full-duration completion

- Run ID: `20261016T001612-04d2ba4c4d1740519cda5f32b33cea7f`; **cat-labelled instrumentation only**, started 20:16:12 New York, October 15, with 30-second draft warm-up. Same iPhone15,2 / iOS 26.6.2 / Unity build GUID as the previous runs.
- Device manifest records **`completed=true`, `interruptions=0`, `stop_reason=duration_reached`**. Console shows automatic completion through `PresenceRecorder.Update → Finish`. No export exception observed. Raw manifest remains unchanged as `instrumentation_only` / `unverified_player` / `unity_update_proxy`.
- **35,973 samples / 35,972 intervals over 600.004520 seconds**. Update-interval p95 **16.895667 ms**, worst **23.554625 ms**. All ten full one-minute windows are **59.95–59.9667 Update FPS**. The tiny trailing partial window is unscored; its apparent rate is not a sustained FPS result. These values describe an empty diagnostic scene and do not establish animal rendering performance, validated display timing or flagship support.
- Peak Unity allocated memory **70.136944 MiB**, not total process resident memory. Battery reported 0.90 → 0.95 while wired; no battery-drain conclusion. All thermal samples remain `unknown`; no touch timings, network/offline trace or animal/AR video was collected.
- Device copy **PASS**: `artifacts/device-capture-copy-003.json` / `.log`; raw evidence under `artifacts/device-captures-003/<run-id>/`. This copy also preserves both earlier runs; byte comparison confirmed their manifest/CSV contents unchanged.
- `python3 tools/benchmark.py artifacts/device-captures-003/<run-id> --output artifacts/diagnostic-analysis-003.json` parsed the physical recorder output and produced **PARTIAL**, exit **1**, **no measured failures**, **G-P NOT RUN**. Missing evidence includes animal content, validated timing, touches, thermal coverage, protocol/operator/asset context, offline/network review and undeclared crash/inference/warning counts. External provenance does not silently replace these missing raw declarations.
- Raw SHA-256: manifest `838674eaf88d3c8ec7d7df40c352522b83f48d9a81a3f9c7f591d789ee9a8086`; frames `1e43956f4d989ac25ae5b62ba4593f7920f96d878c2c418dfbe68649ac6e751f`.

**Diagnostic pipeline execution is verified end to end:** signed real-device launch → explicit operator start → warm-up → automatic 10-minute collection → device export → Mac copy → numerical inspection. The interruption paths are separately verified and retained. This is a tooling result only; it passes no milestone or product acceptance gate.

Private complete evidence archive: `artifacts/m0-device-evidence-003.zip`, SHA-256 `d1cdeb43f1b7fe5bbfe0aca913fab673109091fea39e815bad7ce5ef677127c9`. Contains all three unchanged raw runs, three analysis reports, device/build provenance and log snapshots. The earlier interrupted-only archive is retained. Archives stay ignored/local, contain device identifiers and have not been published.

**Next blocker:** select legitimate cat/dog assets, approve an all-in procurement ceiling and verify rights/motion/mobile suitability using [the asset plan](asset-plan.md). Also freeze two room configurations, two lighting conditions, warm-up/ambient/battery context and validated presentation/input/thermal methods. Serhan Sari owns engineering, art/licensing and testing. No animal/AR implementation, paid service or reconstruction work begins while these prerequisites remain unresolved. **M0 PARTIAL; M1–M3 and G-P/G-I/G-F/G-M NOT RUN.**


## M0 continuation — native thermal telemetry and capture progress

Baseline source: `0d91b0a`. Still **M0 PARTIAL**, with **M1–M3 and all product gates NOT RUN**. No animal/AR implementation or expenditure authorized by the continuation.

Owner confirmed “yes, livingroom” to the open-floor/furnished and daylight/artificial-evening proposal. Record R1/R2 as living-room configurations and L1/L2 as the selected lighting conditions in [the benchmark protocol](benchmark-protocol.md). Detailed layouts, ambient/battery context and measurement/protocol freeze still need evidence.

Changes:
- Native Objective-C++ iOS bridge explicitly maps NSProcessInfo thermal states into nominal/fair/serious/critical; simulator/unrecognized values remain unknown. Recorder samples the native category per Update, exports it in `frames.csv`, and declares optional `thermal_method` provenance. No temperature, OS-warning or crash counts are invented.
- Diagnostic panel shows warm-up/capture countdown and live thermal category, scrolls within the screen safe area, and reminds the operator that Stop creates an incomplete run. Capture start logs include run ID/species/durations. Completion and interruption rules remain unchanged.
- Editor validation checks thermal CSV names, invalid-state fallback and unavailable/editor sampling. No new runtime dependencies, cloud code, camera permission or animal content.

| Check | Actual result | Private local artifact |
|---|---|---|
| Python tooling | PASS — 29 tests, including existing unknown/serious/critical handling | `artifacts/python-tests-thermal-004.log` |
| Unity validation and thermal contract checks | PASS | `artifacts/validate-20261016T003333Z-5d88be69.log` / `.json` |
| Updated Unity iOS export | PASS; native source included in generated target | `artifacts/export-ios-20261016T003348Z-93b08842.log` / `.json`, `artifacts/ios-diagnostics-004/` |
| Xcode Debug/signing | PASS; native `.mm` compiled and linked, `BUILD SUCCEEDED` | `artifacts/xcode-build-004.log` |
| Updated iPhone install/launch | PASS after unlock; initial locked-device launch failure preserved. Operator confirms countdown works | `artifacts/device-install-004.json`, `artifacts/device-console-004.log`, `artifacts/device-console-004-retry.log` |
| New native thermal CSV export | PASS for short smoke path — 777 nominal samples saved/copied/analyzed; run intentionally incomplete | `artifacts/device-captures-004/20261016T003529-9dcd07dcd9824e0fb213a281fec14ae9/`, `artifacts/diagnostic-analysis-004.json` |
| New-build full-duration run / thermal transitions / instrumentation overhead | NOT RUN | Previous complete diagnostic belongs to the prior build |

Previous raw captures/reports/archives remain unchanged and private. This update does not promote earlier unknown thermal samples into evidence. Presentation and input-to-visible timing remain unvalidated. Procurement/rights, documented layouts and calibrated protocol remain the blockers to further animal/AR work. No purchases, paid services, cloud resources, reconstruction jobs or M4–M14 work performed.


### Native thermal smoke capture 004 — intentionally incomplete

- Run `20261016T003529-9dcd07dcd9824e0fb213a281fec14ae9`, cat-labelled instrumentation, new build GUID `445642daef0e47eab20d789b6ec26ea8`, same physical iPhone/OS. Manifest declares `thermal_method=ios_nsprocessinfo_thermalstate_per_update`.
- 777 rows over **12.975543 seconds** after warm-up; **777 nominal thermal samples**, zero unknown samples. Native bridge → managed sample → CSV → device copy → inspector is verified for nominal state. State transitions and simulator fallback are not device-tested; severe states were not induced. Editor contract/fallback checks passed during export.
- Operator pressed Stop as requested: `completed=false`, `interruptions=1`, `stop_reason=operator_stop`. Inspector correctly returned **FAIL**, exit 1, for interruption/incomplete evidence; `thermal-state coverage` is no longer missing. **G-P NOT RUN**. Update p95 17.105541 ms, worst 48.198667 ms, peak Unity allocated memory 70.106688 MiB. Short empty-scene measurements do not establish sustained performance or instrumentation overhead.
- Raw files copied unchanged under `artifacts/device-captures-004/<run-id>/`; report `artifacts/diagnostic-analysis-004.json`; copy provenance `artifacts/device-capture-copy-004.json`. Earlier run folders were retained across development-app update.
- Raw hashes: manifest `2c3fb1316de783e3ea5dc75243241b22904f33b1cbdb5578cbf2e7727a7d063e`; CSV `eaa21a3baa44654f35436c1edfdbe0f9512b1fd21eeb496adad62beb94133fe1`.
- First launch failed with locked-device denial; retry after unlock succeeded. Direct `idevicescreenshot` could not find the paired device through its transport, so no phone screenshot was obtained. Operator confirmed “countdown is working” but reported missing “display or capture”; clarification is pending on whether that means camera/animal view, media capture or locating diagnostic data. Do not mark this UI report resolved from a valid CSV alone.

Private native-thermal smoke evidence archive: `artifacts/m0-native-thermal-smoke-004.zip`; SHA-256 `3007ab50faec7d37a713af559a56319a62430562d8852bcfe6488a0abac11f04`. Integrity checked. Source/signed binary hashes are in `artifacts/build-evidence-004.json`. No new-build full-duration, thermal-transition, overhead or visual screenshot proof is claimed.
