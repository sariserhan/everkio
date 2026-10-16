# Development setup — Linux source, Mac/iPhone validation

The user has confirmed an Apple silicon Mac on macOS 26.6.2 (25G83), Xcode 27.0 (27A266a), Unity 6000.6.6f1 with iOS Build Support, an Apple developer account and iPhone 14 Pro on iOS 26.6.2. The current agent workspace is now this Mac; tool versions were verified live and the signed diagnostic was installed/launched on the phone. The original Linux tooling tests remain historical evidence in the handoff.

Use Linux for source work and Python checks. Use the Mac for Unity compilation, Xcode export/signing and physical iPhone tests. Follow the [Mac quickstart](mac-quickstart.md) for executable commands; the project now exists at `unity/Everkio` and uses the local recorder package under `unity/Packages`.

## Shared repository
Transfer the entire repository or the prepared handoff archive, preserving relative paths. The checkout has `origin` at `github.com/sariserhan/everkio`; live build verification began from `533143a`. This execution has not pushed or published changes. Keep signing credentials and private media out of Git. Generated caches, builds, logs and raw captures are ignored. Do not copy the project folder alone because its local package dependency lives next to it.

The editor version is pinned. Unity-generated default project settings, the diagnostic scene and package lock were reviewed and committed after the Mac compile/export check. The current skeleton uses built-in IMGUI/JSON modules for instrumentation only. AR Foundation/ARKit and the render pipeline will be selected and verified at the relevant gate rather than represented as already working.

## Acceptance boundary
Compilation, signing and real-device installation/launch have passed for this diagnostic build; a complete 600-second diagnostic and two interrupted captures were saved, copied to the Mac and analyzed. Detailed run status is recorded in [the handoff](m0-status.md). The diagnostic scene contains no animal or AR content and cannot pass presence gates. M0 still needs room/lighting and protocol freeze, asset procurement/rights decisions and validated measurement methods; Serhan Sari owns engineering/art/testing. M1/M2 require licensed photorealistic animal assets before animal/AR work advances. No paid service was provisioned, asset purchased or reconstruction job launched; the existing local editor license and development signing account were used.

Unity supports Linux editing on specified configurations, but local graphics/editor support here has not been established. Unity's iOS process produces an Xcode project, and Xcode builds the application. References: [Unity system requirements](https://docs.unity3d.com/6000.0/Documentation/Manual/system-requirements.html), [iOS setup](https://docs.unity.com/en-us/engine/6000.3/manual/platform-specific/iphone/getting-started/ios-environment-setup). Cloud build is not configured; the available Mac is the selected validation path.
