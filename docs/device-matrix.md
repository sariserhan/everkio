# M0 device matrix

Updated 2026-10-15 from live Mac/device commands and operator confirmation. This is an inventory, not a support or performance claim.

| Role | Hardware/software | Evidence | Status |
|---|---|---|---|
| Baseline candidate | Physical iPhone 14 Pro (iPhone15,2); iOS 26.6.2 (23G90) | Live `devicectl` inventory; operator confirmed diagnostic panel | Wired/paired, Developer Mode enabled; signed diagnostic installed/launched; animal/AR performance NOT RUN |
| iOS build host | Apple silicon (arm64), macOS 26.6.2 (25G83), Xcode 27.0 (27A266a), iOS SDK 27.0 | Live host commands and build logs | Unity 6000.6.6f1 (d20c9ac777da); iOS support installed through Hub; diagnostic compilation/export/Xcode build PASS |
| Signing | Local Apple development identity; owner-approved team and diagnostic bundle ID | Successful Xcode signing/install | PASS for local development; credentials remain local |
| Source/analysis host | Current Mac workspace; Python 3.14.6 and Git | 73 passing Python tests (synthetic fixtures) and real complete/interrupted-capture analysis | Local tooling works; initial Linux results retained as historical evidence |
| Separate flagship comparison | Not nominated | None | NOT RUN; no 60 FPS claim |

## Optional inventory refresh
Run in Terminal on the Mac:

```sh
sw_vers
uname -m
xcodebuild -version
xcode-select -p
df -h /System/Volumes/Data
ls /Applications/Unity/Hub/Editor
```

An absent Unity directory or Xcode command error is useful setup information; do not change the selected developer directory or install arbitrary versions solely to silence the error. Also record the Mac model from About This Mac (no serial number needed). Confirm the iPhone OS version/build in Settings → General → About; retain the reported version until verified rather than silently correcting it.

Unity 6000.6.6f1 is now pinned in the source project. Use the inventory to validate the toolchain and select AR Foundation/ARKit at the relevant gate. The diagnostic project has compiled and launched on the physical baseline candidate; [status](m0-status.md) retains actual evidence and remaining limitations. Before scored runs, also record battery health/charge, room/lighting, ambient conditions, warm-up policy and artifact/build identifiers as required by the execution plan.

## Toolchain setup decision
The user confirms Unity 6000.6.6f1 with iOS Build Support, superseding the earlier suggested Unity 6.3 LTS candidate. Use this exact editor version. The diagnostic package compiled, exported and built with Xcode 27.0, then installed/launched on the connected iPhone. This establishes compatibility for this diagnostic build only; AR packages, animal shaders and scored performance are not yet tested. The first export failed because the iOS module was missing on disk; installing the matching module fixed export. Do not downgrade Xcode speculatively.

References: [Unity release support](https://unity.com/releases/unity-6/support), [Hub installation](https://docs.unity.com/en-us/hub/add-editor). Reviewed 2026-10-15.


## Owner-reported battery context — asset continuation 003

Owner reported **91% current charge**, explicitly clarified as charge rather than Maximum Capacity. This is a conversational observation, not an independently measured or scored run-start endpoint. Battery health remains unknown. Marked repeatable layout positions and measured ambient temperature have not been supplied; the earlier living-room/open-floor/furnished/daylight/evening choices remain proposed conditions, not a frozen scored protocol.
