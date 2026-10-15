# M0 device matrix

Updated 2026-10-15 from user-provided information. This is an inventory, not a support or performance claim.

| Role | Hardware/software | Evidence | Status |
|---|---|---|---|
| Baseline candidate | iPhone 14 Pro; iOS 26.6.2 (explicitly reconfirmed by user) | User confirmation | Available; device build number and deployment/performance tests pending |
| iOS build host | Apple silicon (arm64), macOS 26.6.2 (25G83), Xcode 27.0 (27A266a) | User-supplied terminal output | Unity 6000.6.6f1 and iOS Build Support confirmed by user; compilation/deployment compatibility untested |
| Signing | Apple developer account | User confirmation | Available; local Xcode signing/device deployment not tested |
| Source/analysis host | Current Linux workspace; Python 3 and Git available | Local command execution and 29 passing tooling tests | Available for source/tooling work; Unity absent |
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

Unity 6000.6.6f1 is now pinned in the source project. Use the inventory to validate the toolchain and select AR Foundation/ARKit at the relevant gate. The project has not been compiled. Before scored runs, also record battery health/charge, room/lighting, ambient conditions, warm-up policy and artifact/build identifiers as required by the execution plan.

## Toolchain setup decision
The user confirms Unity 6000.6.6f1 with iOS Build Support, superseding the earlier suggested Unity 6.3 LTS candidate. Use this exact editor version for the initial project; validate compilation and deployment before declaring toolchain compatibility. This is a candidate, not a claim of validated compatibility with Xcode 27.0. Confirm by compiling the diagnostic package and performing an iPhone build. Do not downgrade Xcode speculatively.

References: [Unity release support](https://unity.com/releases/unity-6/support), [Hub installation](https://docs.unity.com/en-us/hub/add-editor). Reviewed 2026-10-15.
