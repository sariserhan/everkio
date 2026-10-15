# Everkio Benchmark Capture 0.1.0

Local diagnostic package for M0 preparation. Import via Unity Package Manager **Add package from disk** using this folder's `package.json`.

Add `PresenceRecorder` to a GameObject and set `species` to `cat` or `dog`. Call `BeginCapture()` explicitly; stop with `StopCapture()`. A completed capture exports under `Application.persistentDataPath/EverkioBenchmarks/<unique-run-id>`.

Requires a Unity 6 API-compatible editor; exact app version not yet selected. **Compilation and device behavior have not been tested.** No animal, AR dependency or production behavior is included. The sibling `unity/Everkio` project can generate an instrumentation-only scene using this package.

The recorded intervals measure Update cadence only. Thermals are unknown, memory covers Unity allocations, and input-to-visible latency requires separate validated measurement. Raw exports deliberately cannot pass the acceptance inspector. See the repository's `docs/benchmark-protocol.md` and `docs/development-setup.md` for setup, required evidence and limitations.
