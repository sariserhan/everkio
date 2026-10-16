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
| Device capture → export → analysis | PARTIAL — two interrupted physical-device runs saved/copied/analyzed; full-duration completion unverified | `device-capture-copy-001.json`, `diagnostic-analysis-001.json` |

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

The interrupted device capture/export/analysis pipeline is verified twice. **The automatic full-duration completion path is still NOT RUN to completion**; next physical action is a fresh run kept foregrounded through “Capture complete.” Do not combine interrupted runs or shorten the acceptance duration. The app's interruption behavior worked as designed and has not been relaxed to produce a favorable result.

Private evidence archive: `artifacts/m0-device-evidence-interrupted-001.zip`, SHA-256 `964e862305958732076f3533f617254d123b493a7355256c71eb784f7e694526`. Includes both unchanged interrupted bundles, their analysis reports, device/build provenance and a snapshot of logs. Archive is ignored and contains device identifiers; no external sharing performed. It is a local preservation copy, not a backup on a separate host.
