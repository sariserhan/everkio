using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;

namespace Everkio.Benchmarks
{
    // Pointer receipt is not physical contact or display presentation; film both independently.
    [RequireComponent(typeof(PresenceRecorder))]
    public sealed class InputMarkerPanel : MonoBehaviour
    {
        private const int MaximumInputs = 250;
        private sealed class MarkerRun
        {
            public readonly double origin;
            public readonly List<Receipt> inputs = new List<Receipt>(MaximumInputs);
            public MarkerRun(double time) { origin = time; }
            public void Add(double time, int frame)
            {
                double elapsed = (time - origin) * 1000;
                if (!double.IsFinite(elapsed) || elapsed < 0 || frame < 0 || inputs.Count >= MaximumInputs ||
                    (inputs.Count > 0 && elapsed <= inputs[inputs.Count - 1].unityReceiptMs))
                    throw new InvalidOperationException("Invalid or excess pointer receipt.");
                inputs.Add(new Receipt { eventId = inputs.Count + 1, unityReceiptMs = elapsed, frame = frame });
            }
        }
        private struct Receipt { public int eventId, frame; public double unityReceiptMs; }
        [Serializable] private sealed class Manifest
        {
            public string schema = "everkio-input-marker-setup-1", presence_gate = "NOT RUN";
            public string scene_content = "instrumentation_only", evidence_kind = "input_marker_setup_only";
            public string timing_method = "unity_imgui_pointer_receipt_only";
            public bool calibration_validated = false, completed, interrupted;
            public string run_id, started_utc, build_guid, device_model, os, unity_version, stop_reason;
            public int input_count, maximum_inputs = MaximumInputs;
        }
        private MarkerRun run;
        private Manifest manifest;
        private int previousSleep;
        public bool IsRunning => run != null;
        public string Status { get; private set; } = "Input marker needs an independent recording of finger contact and screen response.";

        public void Begin()
        {
            if (IsRunning || GetComponent<PresenceRecorder>().IsRunning || GetComponent<TelemetryCostProbe>()?.IsRunning == true ||
                GetComponent<DiagnosticPanel>()?.IsSavingScreenshot == true)
                throw new InvalidOperationException("Finish the active diagnostic before starting the input marker.");
            manifest = new Manifest { run_id = Guid.NewGuid().ToString("N"), started_utc = DateTime.UtcNow.ToString("O"),
                build_guid = Application.buildGUID, device_model = SystemInfo.deviceModel,
                os = SystemInfo.operatingSystem, unity_version = Application.unityVersion };
            run = new MarkerRun(Time.realtimeSinceStartupAsDouble);
            previousSleep = Screen.sleepTimeout; Screen.sleepTimeout = SleepTimeout.NeverSleep;
        }

        private void OnGUI()
        {
            if (!IsRunning) return;
            Rect safe = Screen.safeArea;
            float scale = Mathf.Max(.1f, Mathf.Min(safe.width / 720f, safe.height / 1000f));
            float pad = 24 * scale, x = safe.x + pad, y = Screen.height - safe.yMax + pad;
            float width = safe.width - pad * 2, height = safe.height - pad * 2;
            var label = new GUIStyle(GUI.skin.label) { fontSize = Mathf.RoundToInt(25 * scale), wordWrap = true };
            GUI.Label(new Rect(x, y, width, 170 * scale),
                "Everkio — input marker setup\nFilm finger contact and this screen independently. Tap the coloured field.\nReceipt timestamps alone cannot establish latency. G-P NOT RUN.", label);
            var target = new Rect(x, y + 180 * scale, width, height - 290 * scale);
            var current = Event.current;
            if (current.type == EventType.MouseDown && current.button == 0 && target.Contains(current.mousePosition))
            {
                try { run.Add(Time.realtimeSinceStartupAsDouble, Time.frameCount); }
                catch (Exception error) { Debug.LogError(error); Finish(true, "invalid_receipt"); return; }
                current.Use();
            }
            int count = run.inputs.Count;
            Color previous = GUI.color;
            GUI.color = count % 2 == 0 ? new Color(.15f, .75f, 1) : new Color(1, .85f, .15f);
            GUI.DrawTexture(target, Texture2D.whiteTexture); GUI.color = previous;
            var markerLabel = new GUIStyle(label) { alignment = TextAnchor.MiddleCenter, fontSize = Mathf.RoundToInt(42 * scale) };
            markerLabel.normal.textColor = Color.black;
            GUI.Label(target, "Tap here\nEvent " + count + "\n" + (count % 2 == 0 ? "BLUE" : "YELLOW"), markerLabel);
            var button = new GUIStyle(GUI.skin.button) { fontSize = Mathf.RoundToInt(25 * scale) };
            if (GUI.Button(new Rect(x, y + height - 90 * scale, width, 80 * scale), "Stop and export marker setup", button))
                Finish(false, "operator_stop");
            else if (count == MaximumInputs) Finish(false, "input_limit");
        }

        private void Finish(bool interrupted, string reason)
        {
            if (!IsRunning) return;
            var saved = run; run = null;
            Screen.sleepTimeout = previousSleep;
            manifest.completed = !interrupted; manifest.interrupted = interrupted;
            manifest.stop_reason = reason; manifest.input_count = saved.inputs.Count;
            try
            {
                string folder = Path.Combine(Application.persistentDataPath, "EverkioDiagnostics", "InputMarkers", manifest.run_id);
                Directory.CreateDirectory(folder);
                using (var writer = new StreamWriter(new FileStream(Path.Combine(folder, "pointer-receipts.csv"), FileMode.CreateNew, FileAccess.Write)))
                {
                    writer.WriteLine("event_id,unity_receipt_ms,requested_marker_state,unity_frame_index");
                    foreach (var input in saved.inputs)
                        writer.WriteLine(input.eventId + "," + input.unityReceiptMs.ToString("R", CultureInfo.InvariantCulture) + "," +
                            (input.eventId % 2 == 0 ? "blue" : "yellow") + "," + input.frame);
                }
                using (var writer = new StreamWriter(new FileStream(Path.Combine(folder, "manifest.json"), FileMode.CreateNew, FileAccess.Write)))
                    writer.Write(JsonUtility.ToJson(manifest, true));
                Status = "Marker setup exported: " + manifest.run_id + "; " + saved.inputs.Count + " receipts. Independent latency calibration NOT RUN.";
                Debug.Log("EVERKIO_INPUT_MARKER_SAVED " + folder + " interrupted=" + interrupted);
            }
            catch (Exception error) { Status = "Marker export failed: " + error.Message; Debug.LogError(error); }
        }

        private void OnApplicationFocus(bool focused) { if (!focused) Finish(true, "focus_lost"); }
        private void OnApplicationPause(bool paused) { if (paused) Finish(true, "application_paused"); }
        private void OnDisable() { Finish(true, "component_disabled"); }

        public static void ValidateContract()
        {
            var probe = new MarkerRun(10); probe.Add(10.125, 5); probe.Add(10.25, 6);
            if (probe.inputs[0].unityReceiptMs != 125 || probe.inputs[1].eventId != 2)
                throw new InvalidOperationException("Input marker sequence/clock contract failed.");
            foreach (double invalid in new[] { double.NaN, double.PositiveInfinity, 9, 10.25 })
            {
                bool rejected = false;
                try { probe.Add(invalid, 7); } catch (InvalidOperationException) { rejected = true; }
                if (!rejected || probe.inputs.Count != 2) throw new InvalidOperationException("Invalid receipt was retained.");
            }
            for (int i = 2; i < MaximumInputs; i++) probe.Add(11 + i, i + 5);
            bool capped = false;
            try { probe.Add(1000, 1000); } catch (InvalidOperationException) { capped = true; }
            if (!capped || probe.inputs.Count != MaximumInputs) throw new InvalidOperationException("Input marker capacity failed.");
            Debug.Log("EVERKIO_INPUT_MARKER_CONTRACT_OK synthetic state only; no latency evidence");
        }
    }
}
