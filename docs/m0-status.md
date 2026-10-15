# M0 handoff — 2026-10-15

**M0: PARTIAL. M1–M3: NOT RUN. G-P/G-I/G-F/G-M: NOT RUN.**

## Delivered
- Initialized a local Git repository on `main`; no remote or public publication.
- Added dependency-free Python capture inspection, CSV/manifest contracts and a Unity diagnostic recorder package.
- Added repeatable local tests and Linux/Mac setup instructions.
- Added a Unity 6000.6.6f1 project skeleton, diagnostic scene generator and device-facing capture controls.
- Added guarded prepare/validate/iOS-export commands with unique logs, completion checks and overwrite protection. See [Mac quickstart](mac-quickstart.md).
- Preserved implementation limits and stricter evidence criteria; no synthetic results count toward device gates.

## Verification
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


## Current installation inventory
User confirms Unity **6000.6.6f1** with **iOS Build Support**, Xcode **27.0** (27A266a), Apple silicon Mac on macOS **26.6.2** (25G83), and iPhone 14 Pro on iOS **26.6.2**. The source project is pinned to the confirmed editor; compile, signing and physical-device deployment remain NOT RUN.
