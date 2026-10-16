# Isolated iPhone asset preflight

This is a separate development app for the four draft cat/dog idle/walk clips from evidence 006. It does not modify `unity/Everkio`, implement AR, or pass M1/G-P. It requests no camera, microphone or photo-library access. Screenshots show the rendered draft scene, not the room. Keep evidence private.

Use pinned Unity 6000.6.6f1 with iOS Build Support. Create a **fresh** scratch project under ignored `artifacts/` with `Assets/Candidates/` containing the four `cat-refit-idle.fbx`, `cat-refit-walk.fbx`, `dog-refit-idle.fbx`, `dog-refit-walk.fbx` and the two `cat.png`, `dog.png` coats. Exact inputs/hashes used in run 007 are in `artifacts/device-asset-check-007/source-inputs.json`; source assets/settings are retained in evidence 006. Copy `AssetCheckPlayer.cs` into `Assets/Runtime/` and `AssetCheckBuild.cs` into `Assets/Editor/`. Do not copy the older compatibility editor scripts. Use these built-in modules at version `1.0.0` in `Packages/manifest.json`: `com.unity.modules.animation`, `imageconversion`, `physics`, `jsonserialize`, `imgui`, `screencapture` (each with the same `com.unity.modules.` prefix). No external package is required.

From the repository root, substitute fresh absolute paths and your locally selected identifiers:

```sh
/Applications/Unity/Hub/Editor/6000.6.6f1/Unity.app/Contents/MacOS/Unity \
  -batchmode -quit -buildTarget iOS -projectPath /absolute/fresh/scratch-project \
  -executeMethod AssetCheckBuild.ExportIOS \
  -everkioOutput /absolute/fresh/ios-export \
  -everkioBundleId com.yourcompany.everkio.assetcheck \
  -logFile /absolute/fresh/unity-export.log

xcodebuild -project /absolute/fresh/ios-export/Unity-iPhone.xcodeproj \
  -scheme Unity-iPhone -configuration Debug \
  -destination 'platform=iOS,id=YOUR_DEVICE_UDID' \
  -derivedDataPath /absolute/fresh/DerivedData \
  -allowProvisioningUpdates -allowProvisioningDeviceRegistration -jobs 4 \
  DEVELOPMENT_TEAM=YOUR_APPROVED_TEAM CODE_SIGN_STYLE=Automatic build
```

Require Unity exit 0 and `EVERKIO_ASSET_DEVICE_EXPORT_OK`, then Xcode exit 0 and `BUILD SUCCEEDED`. Verify the built `.app` with `codesign --verify --deep --strict`; inspect its bundle identifier and minimum OS. Signing selections stay local; never commit credentials or provisioning profiles. Install the app from `DerivedData/Build/Products/Debug-iphoneos/` using `xcrun devicectl device install app`. Unlock the phone and launch its bundle identifier using `xcrun devicectl device process launch`. Use `--console` to retain runtime errors. The development-player local-network dialog may need dismissal; no inference service is used. Do not terminate the main diagnostic during a timing capture.

The preflight automatically plays four clips for about 25 seconds total, samples each animated surface once after two seconds and saves one PNG per clip plus `report.json` in `Documents/EverkioAssetChecks/<new-run-id>/`. Leave it foregrounded. Focus loss/pause makes the report incomplete. Every run gets a fresh directory and refuses file overwrite. Abrupt termination can leave no final report; missing evidence cannot pass.

Copy the data with the installed CLI, using a fresh **absolute** destination:

```sh
xcrun devicectl device copy from --device YOUR_DEVICE_UDID \
  --domain-type appDataContainer --domain-identifier com.yourcompany.everkio.assetcheck \
  --source Documents/EverkioAssetChecks \
  --destination /absolute/fresh/copied-asset-checks
```

Require `completed=true`, `interrupted=false`, no report/entry error, exactly four distinct candidates, four readable PNGs, 46 bones and nonzero motion in each entry. Runtime guards reject nonfinite vertices, floor penetration below -0.0001 normalized units, heights outside 0.8–1.2 and motion below 0.001. These are sampled compatibility checks, not anatomical/contact acceptance, real-world scale, complete-pose parity or natural motion. Inspect the actual PNGs, preserve failures, and bind evidence to source/asset hashes and the runtime build GUID.

The 60 FPS setting is a request, not a measurement. CPU mesh baking/PNG export disturbs timing. This app provides no sustained performance, touch latency, thermal/battery, offline-network review, AR, fur/eye quality or blinded presence evidence. Its report always leaves G-P `NOT RUN`. Do not feed it into the animal-presence benchmark as a scored session.
