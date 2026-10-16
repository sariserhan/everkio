# M0 handoff — 2026-10-15

**M0: PARTIAL. M1–M3: NOT RUN. G-P/G-I/G-F/G-M: NOT RUN.**

Latest live result: signed iPhone diagnostic build, PNG export and automatic 600-second native-thermal capture work; 73 Python tests pass. A short Instruments Metal trace/export/inspection now works after unlock/relaunch, while timing calibration remains incomplete. Ungated AI-generated cat/dog shapes, painted rig drafts and authored walk candidates now exist; isolated Unity FBX/skin/texture/clip compatibility is checked; Rigify shutdown is fixed on this host, but product quality remains unaccepted; spending remains unapproved. AI generation is the selected asset direction; a stock-pack purchase is not required. See the final continuation below; earlier sections retain historical results.

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
| Mac/Xcode build host | Diagnostic Unity export, signed Xcode build and iPhone deployment verified; details below | Revalidate when animal/AR dependencies are introduced |
| Named owners | Serhan Sari confirmed engineering, art/licensing and testing ownership during live Mac execution | Owner coordinates procurement and protocol freeze |
| Usable cat/dog assets | Local generic AI-to-3D meshes and movable rig drafts produced; quality precheck FAIL; no animation/PBR/LOD acceptance | Improve generation/materials and establish a usable quadruped rig; stock procurement is optional, spending remains unapproved |
| Timing/thermal validation | Update proxy only; native nominal thermals verified through full run; short independent Metal trace now exported/inspected | Correlate recorder/presentation clocks and calibrate input timing and overhead; thermal transitions untested |
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


## M0 visual diagnostic screenshot continuation

Baseline source `540b19e`. Owner clarified that the missing output meant an expected screenshot/video, rather than a broken countdown. The previous diagnostic only wrote CSV/manifest data. This continuation adds an explicit **Save diagnostic screenshot** button for private M0 evidence. It does not implement M7 product media sharing/recording or animal/AR content; video remains unimplemented.

Implementation: wait until end-of-frame, capture the Unity-rendered app view, encode PNG, and write a UTC/UUID filename with `FileMode.CreateNew` under `Documents/EverkioDiagnostics/Screenshots`. Report success only after write completion; errors remain visible/logged. Destroy the temporary texture after export and cancel pending work when the panel is disabled. Disable screenshot export while a timing run is active and disable starting a run while saving. No Photos/camera permission, upload or cloud service is involved.

Built-in ScreenCapture and ImageConversion modules are pinned at `1.0.0` in the app/package manifests and lockfile. Editor validation checks PNG encoding/signature. The screenshot is a rendered app image, not independent display-presentation or touch-latency evidence.

| Check | Actual result | Private local evidence |
|---|---|---|
| Unity iOS export/PNG self-check | PASS; initial export 005 superseded by 006 including coroutine cancellation guard | `artifacts/export-ios-20261016T004128Z-50645132.log` / `.json`; final `artifacts/export-ios-20261016T004146Z-cae73349.log` / `.json` |
| Xcode Debug/signing | PASS | `artifacts/xcode-build-006.log`; export `artifacts/ios-diagnostics-006/` |
| Python tooling | PASS — 29 tests | `artifacts/python-tests-screenshot-006.log` |
| iPhone installation | PASS | `artifacts/device-install-006.json` / `.log` |
| First launch | Blocked by locked phone; operator asked to unlock/open | `artifacts/device-console-006.log` |
| Physical PNG save/copy/visual inspection | PASS — operator saved image; retry copied valid 1179 × 2556 PNG; visually inspected | `artifacts/device-screenshots-006-retry/20261016T004309-1a11f45c683743e4a5937d72dff85979.png`, `artifacts/device-screenshot-copy-006-retry.json` |

**M0 remains PARTIAL; M1–M3 and all product gates NOT RUN.** No asset purchase, paid service, reconstruction job, animal/AR work or other future milestone implementation performed. New-build full-duration/native thermal transitions/overhead remain untested. Procurement and calibrated measurement/protocol evidence remain open.


### Screenshot 006 — actual visual result

Owner confirmed **Screenshot saved** on the updated phone app. Copy attempt 1 failed with CoreDevice connection reset (`device-screenshot-copy-006.log`); retry succeeded without changing the image. PNG `20261016T004309-1a11f45c683743e4a5937d72dff85979.png` copied to `artifacts/device-screenshots-006-retry/`. Decoder inspection reported **1179 × 2556** pixels. Visual inspection shows the M0 panel, instrumentation-only disclosure, nominal thermal state, controls and readable text without blank/clipped content. Buttons are disabled and the status says Saving in the image because the screenshot captures the frame before encoding/writing completes; the owner separately confirmed the later success message. No camera or animal is rendered.

PNG SHA-256: `45afe349f61e672e7afd925e98ea7f38071d3d86fef8c6116820ceb5191bb73a`. Source/signed executable and framework hashes are in `artifacts/build-evidence-006.json`. Phone update preserved previous raw data. The missing visual-output report is resolved for a diagnostic screenshot; video recording remains unimplemented. This demonstrates a Unity-rendered app screenshot/export path only, with no independent physical-presentation timing evidence or animal-presence acceptance.

Private evidence archive `artifacts/m0-diagnostic-screenshot-006.zip`; SHA-256 `d5dfc67c99ea334778d8e648814c9af2f77b69be5f1475fcf004c27951c7ef0d`; ZIP integrity verified. Includes PNG, provenance, final export/build/test logs and failed/successful copy logs. Evidence stays local/ignored; no publication or external upload.


## Autonomous continuation from `3c03af8`

Scope remains authorized M0–M3 only. Owner asked to continue until blocked, then explicitly selected **Keep spending unapproved** after reviewing [the concrete asset procurement proposal](asset-procurement-decision.md). No purchase, paid service or research budget is authorized. No licensed cat/dog source package is present in the repo or inspected local Unity Asset Store cache. Paid procurement and unverified/free reuploads cannot bypass this blocker.

### Asset findings and decision

- Official free Grey Cat demo found (Rip Vertices Studio, package 412724, version 1.2). Store declares Standard EULA and a standalone evaluation demo; published clip-count labels disagree, and the listed motions do not establish lie/eat/contact/turn coverage. Mobile variant omits fur; HD fur requires actual phone evaluation. No asset obtained, accepted or imported.
- Cheap same-publisher German Shepherd lists only five clips; it is not a documented motion-complete route. Domestic Animal Pack is the best documented single-pack evaluation option among reviewed candidates, but its proposed USD 200 all-in ceiling was **not approved**. Store claims cannot pass M1/realism/device gates.
- Evil_Katz “An Animated Cat” rejected as a legitimate source without original-rights clearance: uploader disclaims authorship and identifies a commercial-game source. Free cartoon/stylized assets and wolf substitution remain excluded.
- Public first-party HTML/description evidence is preserved in ignored `artifacts/asset-research/`; this is preliminary provenance research, not legal clearance. No publisher messages were sent and no new account was created.

### Session-series benchmark support

Added `tools/benchmark_series.py` to inspect one animal/device/configuration across at least three sessions and pool validated touch observations. It retains individual numerical failures/missing evidence, requires room/lighting coverage and consistent build/asset/protocol/methods, rejects duplicate/reused evidence, and refuses to overwrite output. It does not splice interrupted captures, auto-select favorable sessions or grant G-P. Single-run reports keep their conservative per-run 100-touch rule; only the series inspector can satisfy that count across sessions, with observations still required in each session.

Verification: **40 Python tests PASS** in `artifacts/python-tests-series-final.log` (29 existing + 11 new synthetic series tests). Cases cover pooled observations, invalid configuration/duplicates, empty session touches, hidden per-session latency failure, interrupted/diagnostic evidence, missing coverage, changed input and overwrite protection. A replay of actual prior complete diagnostic run 003 produced **PARTIAL / G-P NOT RUN** in `artifacts/actual-diagnostic-series-003.json`; diagnostic evidence still cannot pass as an animal session series. No real animal series is available.

### Current phone test and blockers

Owner started one full-duration diagnostic on the current native-thermal/screenshot build and agreed to keep it foregrounded. It subsequently completed and was exported; actual results are recorded below. No app rebuild or reinstall was performed during this capture.

Remaining independent evidence requires owner/hardware/art actions: legitimate cat/dog packages and procurement/rights resolution; actual marked room layouts and ambient/battery-health context; calibrated presentation/input timing with an independent reference; motion reviewers and blinded evaluators at M3. Additional flagship hardware remains untested. **M0 PARTIAL; M1–M3 and all product gates NOT RUN.** No M4–M14 implementation, paid research, reconstruction job or cloud provisioning is performed.


## Full native-thermal capture 007 and USB trace blocker

Source on the phone: screenshot/native-thermal build 006 from `3c03af8`, build GUID `252cc88c97e84661be47da3e43e453b8`. Analysis tools source: `f359ab7`. The owner kept the app foregrounded for the complete run. Capture was finished and safely copied before profiling attempts; no trace ran concurrently with this capture.

| Check | Actual result | Private local evidence |
|---|---|---|
| Full capture → save → device copy → analysis | PASS for diagnostic pipeline; automatic `duration_reached`, `completed=true`, zero recorded interruptions | `artifacts/device-captures-007/20261016T005107-fcc5d76491a54819857913ef4e059539/`, `device-capture-copy-007.json` / `.log` |
| Duration and native thermals | 600.008373 seconds, 35,973 rows; every thermal sample nominal, zero unknown | Raw manifest / `frames.csv` |
| Update cadence | p95 16.945958 ms; worst 23.362667 ms; ten complete minute windows 59.95–59.966667 Update FPS | `artifacts/diagnostic-analysis-007.json` |
| Memory / battery | Peak Unity allocated memory 70.230794 MiB; reported battery 0.95 → 0.95 | Same raw/report files; not resident-memory or battery-drain proof |
| Single-run and series inspectors | Correctly **PARTIAL / G-P NOT RUN**, with no measured numerical failures; missing animal, validated timing/touches and protocol evidence retained | `artifacts/diagnostic-analysis-007.json`, `diagnostic-series-007.json` |
| Prior raw evidence preservation | All eight files from four earlier runs byte-identical to capture export 004 | `artifacts/capture-preservation-007.json` |
| Instruments over local network | Attach by app name failed (exit 19); confirmed PID attach failed (exit 21) | `artifacts/metal-trace-007.log` / `.json`, `metal-trace-007-pid.log` / `.json` |
| Instruments retry after owner connected USB and unlocked phone | CoreDevice reports wired/paired/connected, `xcdevice` reports available over USB, current app PID confirmed; Instruments still lists phone offline and times out waiting for boot (exit 13, 30.83 seconds). **No usable trace** | `artifacts/device-inventory-usb-trace.json`, `xcdevice-usb-007.json`, `xctrace-devices-usb.log`, `metal-trace-007-usb.log` / `.json` |

Raw manifest SHA-256 `3dd247919cee4d69d72838dddca8cf26e2de4adfed7f4ac7145194a06af5e7f2`; raw frame CSV SHA-256 `1a1398af9f7bce357006da40155f58736bac2f7d5b716f0a334ea457833142d4`. Original provenance remains `instrumentation_only`, `unverified_player`, `unity_update_proxy`; no raw declarations were rewritten to claim acceptance. External CoreDevice inventory establishes the physical phone used, but does not validate the recorder's timing method. Partial trailing window is excluded from full-minute cadence scoring.

Private archive `artifacts/m0-native-full-capture-007.zip`, SHA-256 `01a5eb4b938c1f1037768979669e396482f027ba7797c4fcfd7d739d2b9f1a2a`; 42 files, ZIP integrity verified. Includes five raw captures, analyses, preservation hashes, trace failures/device inventories, asset research and test log. Per-file hashes are in `artifacts/evidence-index-007.json`. Evidence remains ignored/local; credentials and signed application binaries are not added to Git.

The full-duration native nominal-thermal path is now verified, superseding earlier pending full-run notes. Thermal transitions, instrumentation overhead, independent on-glass presentation, touch-to-visible latency, offline/network behavior, animal realism/motion/AR and owner-identity acceptance remain untested. Connection inventory during capture used local-network transport, so unchanged battery readings do not establish charge state or power efficiency. App-rendered screenshot export works; video recording remains unimplemented.

**Next blockers:** suitable licensed cat/dog packages with the required motion/rights evidence (owner explicitly leaves spending unapproved), and Instruments device visibility/calibrated timing. Resolving timing may require an interactive Instruments/Xcode device-support investigation; USB alone did not resolve it. No unpairing, security reset or speculative toolchain downgrade was performed. Marked living-room layouts, ambient/battery-health context, protocol freeze, reviewers and blinded evaluation remain outstanding. **M0 PARTIAL; M1–M3 and all product gates NOT RUN.** No further animal/AR implementation can proceed under the asset prerequisite. No paid services, purchases, reconstruction jobs or M4–M14 implementation performed.


## Presentation setup continuation 008 — Instruments attach recovered

Continued from `429f25b` with spending still unapproved. No animal/AR implementation, asset acquisition, app rebuild or installation occurred. Existing phone build remains `3c03af8` / GUID `252cc88c97e84661be47da3e43e453b8`. Earlier diagnostic captures and failed trace attempts remain preserved.

Initial refreshed inventory again showed the paired/wired phone available to CoreDevice but offline in Instruments. A short HUD-enabled relaunch was denied because iOS reported the phone locked (`artifacts/metal-hud-launch-008.json` / `metal-hud-console-008.log`). The owner then explicitly unlocked it. Relaunch succeeded, temporary Metal HUD logging appeared, and Instruments subsequently listed the phone online. Unlock/relaunch restored attachment in this attempt; this does not prove one definitive cause for every earlier offline failure.

| Check | Actual result | Private local evidence |
|---|---|---|
| Python regression tests | PASS — **48 tests**, including eight new synthetic Metal-export tests | `artifacts/python-tests-final-008.log`, `metal-trace-tests-008.log` |
| Unity editor validation | PASS, existing source still compiles and PNG/thermal contract checks execute | `artifacts/validate-20261016T011311Z-e07d87ef.log` / `.json` |
| HUD logging smoke | PASS for log availability only; 20 raw batches between 21:13:59.801 and 21:14:09.491 America/New_York | `artifacts/metal-hud-console-008-unlocked.log`, `metal-hud-smoke-008.json` |
| Restore normal launch | PASS, new process 4317; no HUD variables supplied; app still alive after trace | `artifacts/normal-launch-after-hud-008.json`, `normal-console-after-hud-008.log`, `device-processes-after-trace-008.log` |
| Metal System Trace attachment/recording | PASS, exit 0; requested 15-second limit, trace summary duration 16.903717 seconds; saved successfully | `artifacts/metal-diagnostics-008.trace/`, `metal-trace-008.log` / `.json` |
| TOC and displayed-surface XML export | PASS; target is physical iPhone 14 Pro, iOS 26.6.2, Everkio PID 4317 | `artifacts/metal-trace-008-toc.xml`, `metal-displayed-surfaces-008.xml`, export logs |
| Process-attributed swap inspection | **PARTIAL / G-P NOT RUN**; 977 swaps across 16.446209041 seconds, one unattributed row excluded; p95 adjacent swap interval 16.679792 ms, worst 66.718875 ms | `artifacts/metal-swap-analysis-008.json` |

Added standard-library-only `tools/metal_trace.py` and documented commands in the Mac quickstart. The inspector follows typed XML references, checks observed Instruments schema/row structure, attributes swaps by the selected PID, requires a single named display and strictly increasing swap times, hashes the raw export and refuses report overwrite. Tests cover referenced records, foreign/unattributed rows, missing/cyclic references, duplicate IDs, ordering, mixed displays/processes, wrong schema/types/row shape, missing target and CLI overwrite behavior. No changes to animal acceptance thresholds or raw recorder provenance.

This is a short idle diagnostic trace, with no simultaneous recorder capture, frozen warm-up or common-clock correlation. No ten-minute sustained performance or touch result is claimed from it. The worst swap interval is retained rather than hidden by p95. CPU-to-display latency is not touch-to-visible latency. HUD logging is a separate startup workload; raw batches and duplicate-metric warnings are retained, but batching/overlap/units are not sufficiently validated to pool HUD metrics. Normal launch was restored before the Metal trace, so HUD values are not substituted for trace results. The trace attachment blocker is recovered for this attempt; full presentation/input calibration, independent physical timing and instrumentation overhead remain open.

XML export SHA-256 `4ea858cda57832b1f3f497f7e3c2f31d4e5fefd47db41d2206b08c3f64041859`. Private evidence archive `artifacts/m0-presentation-setup-008.zip`, SHA-256 `5660be17a2b60265a0ed6c1ffe85db26081641609cbd919b4936054e147b8d1f`; 626 files including the trace package, exports, analysis, device/launch logs, tests and inspector source; ZIP integrity verified. Per-file hashes: `artifacts/evidence-index-008.json`. The system trace contains device/other-process metadata and remains local/ignored. No credentials are committed.

**Next blocker remains licensed cat/dog assets and rights/motion coverage.** Spending remains explicitly unapproved; the existing shortlist does not grant procurement or redistribution rights. Owner-supplied suitable already-licensed assets or a later approved procurement decision is needed before animal/AR implementation. Room layouts, ambient/battery-health context, calibrated protocol, independent reviews and cohort evidence remain missing. **M0 PARTIAL; M1–M3 and G-P/G-I/G-F/G-M NOT RUN.** No paid services, research/reconstruction jobs or M4–M14 implementation performed.


## Asset-direction correction — AI generation

Owner clarified that the animals should be AI-generated. The prior continuation treated a stock-pack license as the practical next dependency; that was too narrow. Updated the asset plan and decision D13: select a suitable AI-to-3D workflow, establish output/model/source rights and resource requirements, then evaluate the generated mesh/rig/motion on the actual phone. No stock purchase is mandatory. No generator is selected, no generation job has run, and spending remains unapproved. Personalized reconstruction research retains its separate funding/consent controls. M0 remains PARTIAL; M1–M3 and all product gates remain NOT RUN.


## AI animal generation 001 — actual local meshes produced

Owner selected AI-generated animals and then instructed execution. Source baseline `63e93e1`. Work is original generic animal art preparation within M0–M3; no customer-pet reconstruction or R-track experiment. Original synthetic cat/dog PNGs were created using the built-in imagegen tool and saved with exact prompts/hashes in `assets/ai-reference/`. No third-party input photo, stock asset pack or paid generation API was used. Subscription/account cost for the built-in image calls was not independently measured; no new paid service or account was provisioned.

Selected a local CPU TripoSR evaluation after checking official source/model documentation, license, current host resources and relevant code. Host is Apple M5 MacBook Air with 16 GB unified memory and approximately 35 GiB free before setup. Isolated Python 3.11 environment, weights and all generated raw evidence are under ignored `artifacts/ai-animals-001/`; no ML runtime dependency was added to the iPhone app. MIT notice retained in `third_party/TripoSR-LICENSE.txt`. Full provenance and reproducible commands: [AI animal generation](ai-animal-generation.md).

| Check | Actual result | Private evidence |
|---|---|---|
| Model acquisition | Public official weights downloaded, 1,677,246,742 bytes; published SHA-256 matched | `ai-animals-001/weights-download.json`, `sources/triposr-model.json` |
| Local extraction setup | CPU torchmcubes compiled successfully after correcting isolated-build dependency setup; initial failed install retained | `torchmcubes-install.log`, `torchmcubes-install-retry.log` |
| First cat generation | FAIL: offline config cache not found because old hub client expects `HUGGINGFACE_HUB_CACHE`; failed output preserved | `cat-generation.log`, `cat-v1/generation.json` |
| Resolution-128 cat / dog generation | PASS for static geometry/export only; 26,912 / 19,784 triangles, 8.014 / 7.236 recorded generation-stage seconds | `cat-v2/`, `dog-v1/` |
| Resolution-256 cat / dog generation | PASS for static geometry/export only; 111,620 / 80,848 triangles, 13.400 / 13.359 recorded generation-stage seconds | `cat-res256/`, `dog-res256/` |
| GLB round-trip and structure | PASS for count/hash/integrity checks; all four meshes have one connected component without repair; zero skins/animations/PBR material definitions, non-watertight topology | `mesh-roundtrip-checks-v2.json`, `glb-structure-checks.json` |
| Desktop four-view previews | Valid visible-window renders obtained and visually inspected; earlier hidden-window blank/clipped images and Cocoa teardown failure preserved as invalid previews | `cat-res256/preview-visible-*.png`, `dog-res256/preview-visible-*.png`, preview helper/logs |
| Final runner provenance guard | PASS on actual pinned source/model/config and cached DINO checksum; preflight creates no output | `final-preflight-check.log` |
| Python checks | PASS — **55 tests**, including seven new generation guard tests; real local inference and GLB checks above are separate from synthetic tests | `python-tests-final-guarded.log` |

Recorded stage times exclude dependency imports, reference generation, installation and downloads. No offline-tool peak-memory/thermal/battery claim. The runner forces offline hub/transformer reads, CPU inference and fixed extraction settings; there is no hosted-inference dispatch path. Public model/config downloads were separate network reads. It rejects an existing output directory, missing inputs, modified/unpinned source and wrong model/config checksums. No self-retry loop, automatic paid fallback or external compute resource was created.

**Static asset quality precheck: FAIL for product use.** Both resolutions have blurry/inferred eyes and muzzles, coarse coat detail and imperfect limb/paw silhouettes. Higher resolution adds triangles without resolving those appearance defects. No rig/skinning, breathing/locomotion/contact clips, PBR eyes/fur, verified physical scale or mobile LODs exist. No mesh was imported into the Unity diagnostic project or installed on the phone. These desktop renders are not animal/AR device evidence and pass no milestone.

Final cat GLB SHA-256 `c9795ad038f58054dd6a0edf3db1cf81751a568c8cccac722a6f4d126d929cd9`; dog `c2ef045b05e73075d708e6570a271ebfa067a16c3d3e0daaa530f8cc6a1c7a6e`. Private archive `artifacts/m0-ai-animals-001.zip`, SHA-256 `eba67315be3d2155971b03fceb441ddf55916a420627b1c1a1959620ac19c3f4`; 116 files, ZIP integrity verified. Contains references, generated meshes/inputs/previews, failures, provenance/config/license records, runner/tests and logs; excludes the large model weights and installed environment, which remain local. File hashes are recorded in `artifacts/ai-animals-001/evidence-index.json`. The first component-analysis report is superseded by v2 because trimesh's default split repaired holes; no source mesh was changed.

The prior “no generation run” and mandatory-stock-procurement blocker are superseded. Next blocker is **usable generated asset quality plus quadruped rig/motion**, followed by the remaining M0 protocol/calibration requirements. A higher-quality generation/material cleanup route must be evaluated within the unchanged no-spending boundary; do not lower the realism bar or disguise missing animation. **M0 PARTIAL; M1–M3 and G-P/G-I/G-F/G-M NOT RUN.** No paid infrastructure, customer media intake, reconstruction research or M4–M14 implementation performed.


## Ungated AI shape and rig continuation 002

Owner approved **M4–M14 after prerequisite gates, no spending** (D14), then chose **continue without gated weights**. This continuation remains M0 generic asset preparation. No milestone, launch, purchase, customer-upload or reconstruction-research gate is waived. No new Unity features, animal/AR import, iPhone build or deployment occurred; the installed diagnostic's earlier results remain historical evidence, not new animal evidence.

| Check | Actual result | Private evidence under `artifacts/ai-animals-002/` |
|---|---|---|
| Ungated TripoSG weights | Published sizes/LFS hashes checked; pinned public revision; no credentials | `triposg-downloads.json`, `sources/`, environment freeze |
| Local Metal shape generation | Cat/dog succeed; 254,664 / 255,004 raw triangles; generation stages 95.453 / 97.309 seconds | `cat-triposg/`, `dog-triposg/`, process JSON/logs |
| Shape inspection | Both reload finite/watertight with tiny extraction debris; smoother silhouettes than TripoSR, still defective faces/surfaces and no coat | `triposg-mesh-checks.json`, four yaw previews per species |
| Draft rig preparation | Corrected shared-joint scaling, ignored quaternion yaw and ineffective limb fit; derived 30,000-triangle rigs, zero unweighted vertices, max four normalized influences | `cat-rig-v3/`, `dog-rig-v3/`, tracked fit records/tool |
| Independent saved-rig smoke checks | Exit 0 for both; head, neck and four foot controls produce finite movement and reset; GLB/FBX retain skins/rest geometry | `*-rig-v3/deformation-roundtrip-final.json`, `*-rig-v3-review-final2.log`, neutral/head-pose renders |
| Preparation process reliability | **FAIL**: corrected V3–V7 drafts saved before native shutdown SIGSEGV / exit 139. Reopen processes succeed; this does not make preparation reliable | `process-results.json`, `blender-prepare-shutdown-crash.ips`, failed-run logs |
| Gated SF3D | Native dependencies/CPU bake smoke prepared; no weights downloaded or inference run. Owner then chose to skip gated weights | `sf3d-*.log`, `sf3d-baker-smoke.json` |
| Regression suite | **PASS — 61 tests**, including six rig-fit guard tests; synthetic checks separate from real Blender runs | `python-tests-final.log` |

Full provenance, timings, hashes, source notices, experimental reproduction command and defects are in [AI animal generation](ai-animal-generation.md). Model/source/Blender dependencies remain isolated from Unity and the standard-library test runtime. No hosted inference dispatch, paid resource or pet reconstruction study was started. Source/model/dependency terms remain distinct; no stock license is required for this selected AI route. Stable Fast 3D account access is not treated as local authentication, a downloaded model or generation evidence.

The native crash occurs during allocator/static destruction in the preserved report. Serial execution and several orderly shutdown attempts failed; no forced process exit masks it. The official Blender binary download listing returned HTTP 403 on this host. This is a local rig-tool reliability blocker, not evidence of an iPhone app crash. Current tracked tool is explicitly experimental. An apparent extra mesh during reimport was identified as Blender's bone-display helper; binary GLB inspection confirmed one exported animal mesh. No deformed-pose export parity or natural-motion acceptance is claimed.

**Next blockers:** reliable rig authoring; usable anatomy, PBR coat/eyes/fur and required reviewed motion clips; physical scale/LOD preparation; and remaining M0 room markings, ambient/battery context, timing calibration and protocol freeze. Reviewers/cohort/device evidence still have to follow. The gray desktop mesh renders are not AR or animal-presence evidence. **M0 PARTIAL; M1–M3 and G-P/G-I/G-F/G-M NOT RUN.** Conditional M4–M14 authority is recorded, but their gates have not been reached. No additional spending or reconstruction research is authorized.

Private evidence archive `artifacts/m0-ai-animals-002.zip`: **142 files**, 38,270,517 bytes, SHA-256 `91f0958e6403c4aaccccf1def818dee33bc9f3f36a02157a09a63330e2712f40`; ZIP integrity verified. Per-file hashes: `artifacts/ai-animals-002/evidence-index.json`. Includes model driver/patch, patched source, environment freezes, original output/rig drafts, failures, independent checks, previews, crash report and final test log; excludes large weights, installed environments and wheel. Evidence stays local/ignored; no credentials committed.

## Asset preparation continuation 003 — shutdown fixed, actual painted 3D drafts

Source baseline `3c570d6`. Continued within generic asset preparation; no spending, gated weights, hosted 3D inference or reconstruction-research job. No Unity product changes, animal/AR import, app rebuild or deployment. Previous phone diagnostic results do not become animal evidence.

| Check | Actual result | Private evidence under `artifacts/ai-animals-003/` |
|---|---|---|
| Native shutdown isolation | Plain bpy, addon enable, GLB import/export and FBX export exit 0; Rigify generation alone exits SIGSEGV | `shutdown-isolation.json`, minimal scripts/logs |
| Rigify cleanup fix | Generated UI registration is independent of addon registration. Unregister the owned UI namespace before addon disable. Full cat, dog and repeat-cat preparations now exit 0 | `rigify-cleanup-ui.py` / `.log`, `*-rig-clean.log`, `cat-rig-clean-repeat.log` |
| Saved-rig verification | Both independently reopen, respond to head/neck/four feet, reset and retain skin/rest shape through GLB/FBX | `*-rig-review.log`, `*-rig-clean/deformation-roundtrip-final.json` |
| Painted coat experiment | Built-in imagegen painted original synthetic mesh-view targets; native Blender projected/blended/baked one 2048² colour image per species. Geometry/topology hashes unchanged | tracked `assets/ai-reference/paint-manifest.json` and PNGs; private targets, projection scripts/logs and `material-integrity-v2.json` |
| Painted GLB integrity | One skinned surface / 46 joints / one material / one embedded PNG per species | `material-integrity-v2.json`, `*-blended-v2/painted-draft.glb` |
| Direct motion export | **FAIL** diagnostic pose-parity check. One-segment bones improve head/neck, but direct foot pose mismatch remains; full hierarchy did not resolve it | `*-animation-smoke/`, `*-animation-linear-smoke/`, `cat-animation-full-smoke/` |
| Sampled textured export | **PASS for eight diagnostic poses only** after sampling 46 transforms to a constraint-free, one-segment export skeleton. Max errors cat 0.000008062 / dog 0.000003966 normalized units | `*-textured-animation-v2-smoke/animation-parity.json`, GLBs, `.blend`, scripts/logs |
| Python regression tests | **PASS — 63 tests**, including two new UI cleanup tests; synthetic tests separate from actual Blender checks | `python-tests-final.log` |

The old shutdown blocker is resolved for the tested host/workloads. Cleanup uses the generated UI's own unregister function, fails rather than guessing when registration is ambiguous, and preserves output/failure manifests. No forced exit or remapped crash status. Source notices and the actual prior native crash evidence remain preserved. Context7 was unavailable; official Blender source and installed API/addon code were used.

The initial hard-view colour projection had conspicuous seams. Weighted blending/native baking improved them; fallback was needed at 153 cat / 289 dog vertices where no visible projection met tolerance. Actual front/rear mesh renders were inspected, not just the attractive generated paint sheets. Paint did not fix geometry: ridge/proportion defects, flat projected eyes, registration/seam flaws, imperfect paws and missing true fur remain. The diagnostic sweep is five-degree head/neck rotations and separate small foot lifts; it is **not** walking, sitting, lying, eating, approaching or natural/contact-reviewed motion. The sampled export deliberately uses linear skinning and needs deformation review. Colour-map constant roughness is not a completed PBR material.

See [full asset evidence and limitations](ai-animal-generation.md). No stock asset license is mandatory for this AI route; reference/output/model/dependency rights remain recorded separately. Built-in image tool account/subscription cost was not independently measured; no separate paid API or infrastructure was configured.

**Remaining blockers:** accepted anatomy/coat/eyes/fur, required natural motion/contact and physical scale/LOD acceptance, plus M0 environment records, warm-up/overhead/input/presentation calibration and protocol freeze. Battery Maximum Capacity, marked repeatable living-room positions and measured ambient temperature were requested from the owner; none is inferred. Independent reviewers, cohort and scored device runs remain outstanding. **M0 PARTIAL; M1–M3 and G-P/G-I/G-F/G-M NOT RUN.** No public launch, purchase or later-phase implementation occurred.

Owner clarified the reported **91% is current charge**, not battery Maximum Capacity. It is not substituted for battery health or a scored run-start measurement. Marked layout and measured ambient conditions remain unconfirmed; no additional physical action or gate approval is inferred.

Final material variant V2 also fixes a Blender RNA cleanup error: removing UV/attribute objects by retained references skipped entries as indices shifted. Removing by recorded names leaves one `CoatUV` and no projection-weight attributes. The six-view source and baked colour PNG hashes are unchanged; earlier variants and failed LOD assertions are preserved. Sampled pose checks pass again on both corrected textured exports.

Prepared draft LOD0/1/2 at **30,000 / 15,000 / 7,500 triangles per species**. All six GLBs reimport with a skin, one material and one UV map; vertices are finite and pre-export weights normalized to at most four influences. LOD2 front renders were inspected. These are decimation drafts; silhouette/UV/deformation acceptance, runtime switching/distances and device performance remain NOT RUN. See `*-lod-drafts-v2/lod-inventory.json`, `lod-integrity.json` and render/log evidence.

Rendered two actual 3D desktop diagnostic orbit videos, one per species: `*-textured-animation-smoke/draft-motion-review.mp4`. Each is H.264, 640×576, 145 frames at 24 FPS, 6.041667 seconds; FFmpeg full decode exits 0. Extracted frames at 0/2/4 seconds were inspected. Both carry “DRAFT - LOCAL 3D, NOT AR” and “Diagnostic control sweep, not natural gait.” They show the sampled one-segment mesh/colour variants, not a phone camera, AR placement or product performance. Final V2 removes unused UV data without changing source geometry or baked colour PNGs. No video is scored as animal-presence evidence.

Private evidence archive `artifacts/m0-ai-animals-003.zip`: **190 files**, 131,946,762 bytes, SHA-256 `5524c7a9d4504f5294e34aad230f62f6b94b03f9fa1d10862e0919c303050600`; ZIP integrity verified. Includes successful and failed isolation/preparation/material/animation/LOD attempts, exact local experimental scripts, meshes/rigs, texture sources and bakes, videos/decoded review frames, check reports, tracked tool/test/fit snapshot and final test log. Per-file hashes: `artifacts/ai-animals-003/evidence-index.json`. No model weights, installed environments, credentials or signed binaries are included. Runtime/dependency pins remain documented with evidence 002.

## Local walk, Unity compatibility and rating-analysis preparation 004

Baseline `f35a593`. Continued within authorized generic asset/toolchain/benchmark preparation. No spending, gated weights, hosted 3D service, pet-reconstruction research, product-project animal import, iPhone deployment or later-phase implementation. The installed diagnostic still contains no animals or AR.

| Check | Actual result | Private evidence under `artifacts/ai-animals-004/` |
|---|---|---|
| Authored walking candidate | Both generate 121-frame four-beat cycles at 30 FPS. Fixed world-space stance targets are checked; V2 adds small constant sole-height corrections | `walk-candidate*.py`, `*-walk-v1/`, `*-walk-v2/`, logs |
| Skinned-paw proxy observations | V2 worst stance XY drift cat 0.001945 / dog 0.003709 normalized units; all sampled mesh vertices above floor. Weight-selected proxies are not validated anatomical contacts | `paw-observations.csv`, `motion-review.json`; V1 retained |
| Sampled export/reimport | PASS for **121 frame comparisons**, maximum vertex errors cat 0.000008271 / dog 0.000004556 normalized units | `*-walk-v2/walk-export-parity.json`, GLBs, scripts/logs |
| Actual 3D floor/shadow videos | Both render and fully decode; 121 frames, 30 FPS, 768×640, 4.033333 sec. Stills/decoded frames inspected; labelled unaccepted draft, not AR | `*-walk-v2/walk-review.mp4`, video probe data, review frames |
| Isolated Unity FBX compatibility | PASS for editor import/sample/render only: one skinned surface, 46 bones, 30,000 triangles, 2048² colour map and four-second clip per species. Batch exit 0 and completion marker | `unity-import-04.log`, `unity-import-results.json`, `unity-cat.png`, `unity-dog.png`; separate project `artifacts/asset-compatibility-004/` |
| Initial Unity smoke validator | FAIL/exit 1 on double-applied scale. Explicit BakeMesh scale compensation corrects validator; no source asset repair claimed | `unity-import.log`, `unity-import-02.log`, `unity-import-03.log`; initial/final C# |
| Blinded-rating analyzer | Implemented one frozen clip-pair/cohort analysis with input hashes, separate six-cell thresholds and G-P always NOT RUN. No study conducted | tracked `tools/presence_ratings.py`, tests and empty template |
| Python regression suite | **PASS — 73 tests**, including ten new synthetic ratings tests | `python-tests-final.log`, `ratings-tests.log` |

The standalone Unity project is a compatibility experiment, not the product animal/AR harness. It uses legacy clip sampling and the Standard shader; Play Mode/production Animator, Unity deformed-pose parity, root-motion extraction, shader/fur quality and device performance are NOT RUN. FBX carries a 100× hierarchy; the editor checker compensates snapshot scale explicitly. Actual imported heights/body travel match normalized source expectations; physical size is not established. Unity renders show shiny/plastic surfaces and unfinished eyes/coat, not accepted realism.

Walk proxies and finite geometry do not establish natural movement or true grounded contact. The draft still has stiff torso/head/tail motion, no convincing toe roll/body-weight transfer and incomplete required clips. Cyclic clips start/stop mid-gait; turns, sit/lie, eating, approach and reactions remain unfinished. No independent motion review, blinded cohort or real-device animal run has occurred. Full settings, values, caveats and evidence links are in [AI animal generation](ai-animal-generation.md).

The rating analyzer retains every enrolled evaluator in each denominator, counts explicit abstention as not favorable, flags incomplete responses and unbalanced clip order, requires at least 20 respondent IDs and ≥80% ratings ≥4/5 separately per species/dimension. It binds raw inputs/clips by hash, rejects duplicate/mismatched/malformed evidence and refuses report overwrite. Consent/adulthood, authentic device footage, blinding quality, free-text defects and independent reviews still require human evidence; synthetic fixture declarations establish none of them. **G-P always stays NOT RUN.** Empty template: `benchmarks/ratings-template/`; no participant records were collected or committed.

**Next blockers:** accepted animal anatomy/materials and the full natural/contact-reviewed motion set; M0 measured environment/battery-health records and input/presentation/overhead calibration before protocol freeze; then actual animal/AR implementation/device evidence and independent reviewers/cohort. Owner-reported 91% remains current charge only. Reconstruction spending/funding controls are still absent. **M0 PARTIAL; M1–M3 and G-P/G-I/G-F/G-M NOT RUN.** Conditional M4–M14 authorization does not waive these prerequisites or fund paid work.

Private archive `artifacts/m0-ai-animals-004.zip`: **107 files**, 47,160,764 bytes, SHA-256 `c0d54dbce9163189bb1e57da045043845399b780a0ab0ab0e5df4f85e9949c85`; ZIP integrity verified. Includes both walk attempts, raw per-frame paw measurements, sampled exports/parity checks, floor/contact renders/videos, failed/successful Unity logs, exact isolated Unity source/assets/settings and ratings tool/tests/template snapshots. File hashes: `artifacts/ai-animals-004/evidence-index.json`. Excludes Unity Library/cache, installed environments, weights, signing credentials and participant records. Evidence remains local/ignored.
