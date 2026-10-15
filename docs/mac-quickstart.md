# Run the M0 diagnostic project on the Mac

Use the whole repository, keeping `unity/Everkio` and `unity/Packages` together. The project is pinned to **Unity 6000.6.6f1**, matching the confirmed Mac installation. These commands are prepared and locally tested as orchestration; actual Unity compilation and iPhone deployment are **NOT RUN**.

## Prepare and compile
Close any Unity window using this project. From the repository root in Mac Terminal:

```sh
python3 tools/unity_project.py check
python3 tools/unity_project.py prepare
python3 tools/unity_project.py validate
```

The runner locates `/Applications/Unity/Hub/Editor/6000.6.6f1/Unity.app/Contents/MacOS/Unity`; pass `--unity /path/to/Unity` if yours differs. Activate the editor license in Hub before running batch commands. Python 3.10+ is required. If Unity reports a license, module or compiler error, preserve the log under `artifacts/`; do not treat missing output as success.

`prepare` creates `Assets/Scenes/Diagnostics.unity` only when absent and preserves the scene on subsequent runs. It contains a camera and a local diagnostic panel, not an animal or AR scene. Unity generates remaining project defaults and package lock on first import; review and commit them after validation. AR Foundation, ARKit and render-pipeline choices are deliberately not yet claimed as tested or pinned.

To inspect interactively, add `unity/Everkio` to Hub, open the scene and press Play. The panel can start cat-labelled or dog-labelled instrumentation captures. It explicitly states that no animal is loaded. Warm-up is 30 seconds, capture is 10 minutes, and the requested diagnostic frame rate is 60. A target frame rate is not a measured result. During capture automatic sleep is suppressed and restored afterward; leaving the app stops capture as incomplete.

## Export the Xcode project
Choose a bundle identifier you control. Replace the example below with your identifier and use a new output directory for each export:

```sh
python3 tools/unity_project.py export-ios \
  --bundle-id com.yourcompany.everkio.diagnostics \
  --output artifacts/ios-diagnostics-001
```

The runner invokes Unity with iOS selected before compilation and exports a Development/IL2CPP build. It requires the method's completion marker and expected Xcode project; it refuses to overwrite an existing destination. It does not install on a device or configure signing credentials.

Open `artifacts/ios-diagnostics-001/Unity-iPhone.xcodeproj` in Xcode, choose your development team and connected iPhone 14 Pro, then build/run. Keep signing local. Record any build failures plus editor/Xcode versions before changing dependencies. Do not assume Xcode 27.0 compatibility until this succeeds.

## Capture and inspect
Start a diagnostic capture in the app. After it completes, export the app container using Xcode's device tools and locate `EverkioBenchmarks/<run-id>` under the app's persistent data directory. Preserve the complete raw run folder.

```sh
python3 tools/benchmark.py /path/to/exported/run
```

An instrumentation capture **must remain PARTIAL or FAIL**, never an animal-presence PASS. It has no animal, validated presentation timing, touch latency or native thermal evidence. Use it to test the collection/export/analysis path only. Even a successful device launch does not pass M0's remaining asset/protocol prerequisites or any G-P gate.

## Implementation references
The runner uses Unity's [command-line execution](https://docs.unity.com/en-us/engine/6000.3/manual/unity-editor/command-line-arguments/run-unity) and [editor argument contract](https://docs.unity.com/en-us/engine/6000.3/manual/unity-editor/command-line-arguments/editor). No shell interpolation, cloud build service or network inference is used by the runner. Unity may contact its licensing/package services when launched.
