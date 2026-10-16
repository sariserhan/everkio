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
| Named owners | Roles only | Product owner names engineering/art/test owners |
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
| Physical-device install/launch | PASS — app installed, process launched, Metal/scene initialized | `device-install-002.json`, `device-launch-002.json`, `device-console-002.log` |
| App-container copy preflight | PASS — copied empty Documents directory; this does not validate a capture | `device-copy-preflight-003.json` / `.log` |
| Device capture → export → analysis | NOT RUN — awaiting operator start/completion | Device console attached; no saved run yet |

The 20261016 UTC log filenames are still October 15 in New York. The Python log contains an intentional mocked runner failure within a passing test; it is not a live Unity failure. Actual first-export failure is preserved separately.

### Gate and next blockers

**M0 remains PARTIAL; M1–M3 and G-P/G-I/G-F/G-M remain NOT RUN.** Compilation and Xcode export establish tooling progress only. The diagnostic scene contains no animal or AR; Update cadence, unknown thermal state and absent touch measurements cannot establish presence acceptance.

The [asset plan and shortlist](asset-plan.md) records candidates and required rights/motion/mobile checks. Product owner explicitly approved shortlist preparation only, with **no spending approved**. No animal asset is selected, licensed or imported. Resolve selection, procurement ceiling and rights before animal/AR implementation. Owners, two rooms/two lighting conditions, warm-up/protocol freeze, battery/ambient context and validated timing/thermal method remain open. Flagship hardware/60 FPS remain NOT RUN.

Research funding and hard spending controls remain unset. No paid services, purchases, cloud provisioning, reconstruction jobs or M4–M14 work performed.


Build notes: Xcode emitted Unity-generated deprecation warnings, an absent App Store icon warning and an always-run build-script warning. These did not block this local development build; App Store submission is outside scope. The player console reports A16/Metal initialization and a nominal thermal notification at launch, but this is not continuous native thermal evidence in the recorder. Development-player UDP discovery is visible in the console; no offline/no-network claim has been validated. No launch exception was observed in the inspected startup log. Phone panel appearance still needs operator confirmation.


Build evidence index: `artifacts/build-evidence-002.json` records SHA-256 hashes of editor/recorder/panel source, scene, package lock, export report, generated Xcode project and signed executable/framework. Installed diagnostic executable SHA-256: `a0f76ecbc18bf7d1d22b4710cf5e5a5a532bf97fff92d0dbca2319ea3a91367e`. Raw logs, device identifiers, generated Xcode project, signing output and captures remain ignored/private in this local checkout; they have not been published or placed in a durable external evidence store. Preserve this directory for reproducibility. No scored run has begun.

Copy preflight initially failed because `devicectl` requires the destination directory to exist (`device-copy-preflight-002.log`); creating a fresh destination fixed it. Quickstart now includes this step. The app's Documents directory was empty at inspection, so full recorder export and numerical analysis still await a real capture. This is a pending physical-device action, not a passed pipeline test.
