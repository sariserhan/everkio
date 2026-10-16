# Run the M0 diagnostic project on the Mac

Use the whole repository, keeping `unity/Everkio` and `unity/Packages` together. The project is pinned to **Unity 6000.6.6f1**. Unity compilation, Development/IL2CPP export, Xcode build/signing and physical iPhone installation/launch were verified on October 15, 2026. See [actual results and remaining gates](m0-status.md); these checks do not establish animal or AR presence.

## Prepare and compile
Close any Unity window using this project. From the repository root in Mac Terminal:

```sh
python3 tools/unity_project.py check
python3 tools/unity_project.py prepare
python3 tools/unity_project.py validate
```

The runner locates `/Applications/Unity/Hub/Editor/6000.6.6f1/Unity.app/Contents/MacOS/Unity`; pass `--unity /path/to/Unity` if yours differs. Activate the editor license in Hub before running batch commands. Python 3.10+ is required. If Unity reports a license, module or compiler error, preserve the log under `artifacts/`; do not treat missing output as success.

Verify that `/Applications/Unity/Hub/Editor/6000.6.6f1/PlaybackEngines/iOSSupport` exists. On the first live Mac run, the editor was installed but this module was absent. Install it through Hub's Add modules, or the official Hub command:

```sh
"/Applications/Unity Hub.app/Contents/MacOS/Unity Hub" -- --headless install-modules --version 6000.6.6f1 -m ios
```

Wait for installation to finish before exporting. If a failed batch leaves a project lock, first check running Unity processes and open file holders. Archive a confirmed stale lock under ignored `artifacts/`; never remove a lock held by an editor.

`prepare` creates `Assets/Scenes/Diagnostics.unity` only when absent and preserves the scene on subsequent runs. It contains a camera and a local diagnostic panel, not an animal or AR scene. Unity generates remaining project defaults and package lock on first import; review and commit them after validation. AR Foundation, ARKit and render-pipeline choices are deliberately not yet claimed as tested or pinned.

To inspect interactively, add `unity/Everkio` to Hub, open the scene and press Play. The panel can start cat-labelled or dog-labelled instrumentation captures. It explicitly states that no animal is loaded. Warm-up is 30 seconds, capture is 10 minutes, and the requested diagnostic frame rate is 60. A target frame rate is not a measured result. During capture automatic sleep is suppressed and restored afterward; leaving the app stops capture as incomplete. The updated panel shows warm-up/capture time remaining and current thermal state; wait for “Capture complete” without pressing Stop. The controls scroll within the screen safe area.

## Export the Xcode project
Choose a bundle identifier you control. Replace the example below with your identifier and use a new output directory for each export:

```sh
python3 tools/unity_project.py export-ios \
  --bundle-id com.yourcompany.everkio.diagnostics \
  --output artifacts/ios-diagnostics-001
```

The runner invokes Unity with iOS selected before compilation and exports a Development/IL2CPP build. It requires the method's completion marker and expected Xcode project; it refuses to overwrite an existing destination. It does not install on a device or configure signing credentials.

Open `artifacts/ios-diagnostics-001/Unity-iPhone.xcodeproj` in Xcode, choose your development team and connected iPhone 14 Pro, then build/run. Keep signing local. Record any build failures plus editor/Xcode versions before changing dependencies. Do not assume Xcode 27.0 compatibility until this succeeds.

Alternatively, after choosing your local team and device, use command-line signing overrides. This can register the development bundle/device with Apple; use your approved account. Keep identifiers and signing output in local logs, and select fresh export/DerivedData paths for a new evidence build:

```sh
xcrun devicectl list devices
xcodebuild -project artifacts/ios-diagnostics-001/Unity-iPhone.xcodeproj \
  -scheme Unity-iPhone -configuration Debug \
  -destination 'platform=iOS,id=YOUR_DEVICE_UDID' \
  -derivedDataPath artifacts/xcode-diagnostics-001 \
  -allowProvisioningUpdates -allowProvisioningDeviceRegistration \
  DEVELOPMENT_TEAM=YOUR_TEAM_ID CODE_SIGN_STYLE=Automatic build \
  > artifacts/xcode-build-001.log 2>&1
xcrun devicectl device install app --device YOUR_DEVICE_UDID \
  artifacts/xcode-diagnostics-001/Build/Products/Debug-iphoneos/EverkioDiagnostics.app
xcrun devicectl device process launch --device YOUR_DEVICE_UDID \
  --console com.yourcompany.everkio.diagnostics
```

The console command remains attached; use a separate terminal for evidence copying. Do not interrupt it during capture, since signals may be forwarded to the app. Unlock/trust the phone or handle account/Keychain prompts locally if requested. No passwords, certificates or provisioning profiles belong in Git.

## Capture and inspect
Start a diagnostic capture in the app. After it completes, export the app container using Xcode's device tools and locate `EverkioBenchmarks/<run-id>` under the app's persistent data directory. Preserve the complete raw run folder.

For a development installation, the tested device tooling also supports copying the app's Documents directory without exporting the whole container:

```sh
mkdir artifacts/device-captures-001
xcrun devicectl device copy from --device YOUR_DEVICE_UDID \
  --domain-type appDataContainer \
  --domain-identifier com.yourcompany.everkio.diagnostics \
  --source Documents/EverkioBenchmarks \
  --destination artifacts/device-captures-001
```

Use a new destination and retain all run directories, including incomplete captures. Read `manifest.json` before analysis; an incomplete run tests the failure path only.

```sh
python3 tools/benchmark.py /path/to/exported/run
```

An instrumentation capture **must remain PARTIAL or FAIL**, never an animal-presence PASS. It has no animal, validated presentation timing, touch latency or native thermal evidence. Use it to test the collection/export/analysis path only. Even a successful device launch does not pass M0's remaining asset/protocol prerequisites or any G-P gate.

## Implementation references
The runner uses Unity's [command-line execution](https://docs.unity.com/en-us/engine/6000.3/manual/unity-editor/command-line-arguments/run-unity) and [editor argument contract](https://docs.unity.com/en-us/engine/6000.3/manual/unity-editor/command-line-arguments/editor). No shell interpolation, cloud build service or network inference is used by the runner. Unity may contact its licensing/package services when launched.


## Save a visual diagnostic screenshot

When no data run is active, tap **Save diagnostic screenshot**. The app waits for the rendered frame, encodes a PNG and reports the saved filename or failure. Screenshot work is disabled during timing collection to keep its readback/encoding work out of those samples. Screenshots show the current diagnostic app view; they contain no animal/AR content and do not measure physical display timing.

Images are saved privately under `Documents/EverkioDiagnostics/Screenshots`, separately from the benchmark CSV bundles. This does not write to Photos, record video or upload anything. Copy the images to a fresh local directory:

```sh
mkdir artifacts/device-screenshots-001
xcrun devicectl device copy from --device YOUR_DEVICE_UDID   --domain-type appDataContainer   --domain-identifier com.yourcompany.everkio.diagnostics   --source Documents/EverkioDiagnostics/Screenshots   --destination artifacts/device-screenshots-001
```

Preserve PNG hashes and source/build/device provenance with the M0 evidence. These diagnostic images do not qualify as animal-presence clips or implement the deferred product media-sharing/recording flow.
