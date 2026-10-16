using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;
using Stopwatch = System.Diagnostics.Stopwatch;

namespace Everkio.Benchmarks
{
    // Measures the shared reads and buffer append only, not full recorder/display overhead.
    [RequireComponent(typeof(PresenceRecorder))]
    public sealed class TelemetryCostProbe : MonoBehaviour
    {
        private const int Pairs = 1024;
        private struct Row { public int pair; public bool workload; public long start, end; }
        private readonly List<Row> rows = new List<Row>(Pairs * 2);
        private readonly List<PresenceRecorder.Sample> samples = new List<PresenceRecorder.Sample>(Pairs);
        private bool running;
        private int previousSleep;
        private double began;
        private string id, started;
        public bool IsRunning => running;
        public string Status { get; private set; } = "Telemetry call cost is unmeasured; full instrumentation overhead remains uncalibrated.";

        [Serializable] private sealed class Manifest
        {
            public string schema = "everkio-telemetry-cost-1", presence_gate = "NOT RUN";
            public string evidence_kind = "telemetry_cost_setup_only", scene_content = "instrumentation_only";
            public string measured_work = "shared_telemetry_reads_and_preallocated_buffer_append";
            public bool calibration_validated = false, full_instrumentation_overhead_validated = false;
            public bool completed, interrupted, high_resolution;
            public int expected_pairs = Pairs, recorded_rows;
            public long stopwatch_frequency;
            public string run_id, started_utc, build_guid, device_model, os, unity_version, stop_reason, thermal_method;
        }

        public void Begin()
        {
            if (running || GetComponent<PresenceRecorder>().IsRunning || GetComponent<InputMarkerPanel>()?.IsRunning == true ||
                GetComponent<DiagnosticPanel>()?.IsSavingScreenshot == true || !Application.isFocused)
                throw new InvalidOperationException("Keep the app foregrounded and finish other diagnostic operations first.");
            if (Stopwatch.Frequency <= 0) throw new InvalidOperationException("Clock frequency unavailable.");
            rows.Clear(); samples.Clear();
            id = Guid.NewGuid().ToString("N"); started = DateTime.UtcNow.ToString("O");
            previousSleep = Screen.sleepTimeout; Screen.sleepTimeout = SleepTimeout.NeverSleep;
            began = Time.realtimeSinceStartupAsDouble; running = true;
            Status = "Measuring telemetry calls; no capture/input or full-overhead result.";
        }

        private void Update()
        {
            if (!running) return;
            if (Time.realtimeSinceStartupAsDouble - began > 30) { Finish(true, "timeout"); return; }
            try
            {
                // Alternating pair order limits order bias; raw costs are never baseline-subtracted.
                for (int n = 0; n < 8 && samples.Count < Pairs; n++)
                {
                    int pair = samples.Count;
                    Measure(pair, pair % 2 != 0); Measure(pair, pair % 2 == 0);
                }
                if (samples.Count == Pairs) Finish(false, "pairs_reached");
            }
            catch (Exception error) { Debug.LogError(error); Finish(true, "measurement_error"); }
        }

        private void Measure(int pair, bool workload)
        {
            long start = Stopwatch.GetTimestamp();
            if (workload) samples.Add(PresenceRecorder.ReadSample(0));
            long end = Stopwatch.GetTimestamp();
            CheckInterval(start, end, rows.Count == 0 ? 0 : rows[rows.Count - 1].end);
            rows.Add(new Row { pair = pair, workload = workload, start = start, end = end });
        }

        private static void CheckInterval(long start, long end, long previous)
        {
            if (start < previous || end < start) throw new InvalidOperationException("Invalid cost-probe clock interval.");
        }

        private void Finish(bool interrupted, string reason)
        {
            if (!running) return;
            running = false; Screen.sleepTimeout = previousSleep;
            try
            {
                string folder = Path.Combine(Application.persistentDataPath, "EverkioDiagnostics", "TelemetryCost", id);
                Directory.CreateDirectory(folder);
                using (var writer = new StreamWriter(new FileStream(Path.Combine(folder, "costs.csv"), FileMode.CreateNew, FileAccess.Write)))
                {
                    writer.WriteLine("pair_index,phase,start_tick,end_tick,memory_bytes,battery_level,thermal_state");
                    foreach (var row in rows)
                    {
                        string telemetry = ",,";
                        if (row.workload)
                        {
                            var sample = samples[row.pair];
                            telemetry = sample.memory.ToString(CultureInfo.InvariantCulture) + "," +
                                (sample.battery < 0 ? "" : sample.battery.ToString("R", CultureInfo.InvariantCulture)) + "," + ThermalTelemetry.Name(sample.thermal);
                        }
                        writer.WriteLine(row.pair + "," + (row.workload ? "telemetry" : "clock_only") + "," + row.start + "," + row.end + "," + telemetry);
                    }
                }
                var manifest = new Manifest { completed = !interrupted && rows.Count == Pairs * 2,
                    interrupted = interrupted, recorded_rows = rows.Count, stopwatch_frequency = Stopwatch.Frequency,
                    high_resolution = Stopwatch.IsHighResolution, run_id = id, started_utc = started,
                    build_guid = Application.buildGUID, device_model = SystemInfo.deviceModel, os = SystemInfo.operatingSystem,
                    unity_version = Application.unityVersion, stop_reason = reason, thermal_method = ThermalTelemetry.Method };
                using (var writer = new StreamWriter(new FileStream(Path.Combine(folder, "manifest.json"), FileMode.CreateNew, FileAccess.Write)))
                    writer.Write(JsonUtility.ToJson(manifest, true));
                Status = "Telemetry cost setup exported: " + id + ". Full overhead calibration NOT RUN.";
                Debug.Log("EVERKIO_TELEMETRY_COST_SAVED " + folder + " completed=" + manifest.completed);
            }
            catch (Exception error) { Status = "Telemetry cost export failed: " + error.Message; Debug.LogError(error); }
        }

        private void OnApplicationFocus(bool focused) { if (!focused) Finish(true, "focus_lost"); }
        private void OnApplicationPause(bool paused) { if (paused) Finish(true, "application_paused"); }
        private void OnDisable() { Finish(true, "component_disabled"); }

        public static void ValidateContract()
        {
            CheckInterval(10, 12, 9); CheckInterval(12, 12, 12);
            foreach (var interval in new[] { new long[] { 8, 10, 9 }, new long[] { 10, 9, 9 } })
            {
                bool rejected = false;
                try { CheckInterval(interval[0], interval[1], interval[2]); } catch (InvalidOperationException) { rejected = true; }
                if (!rejected) throw new InvalidOperationException("Cost probe retained an invalid interval.");
            }
            Debug.Log("EVERKIO_TELEMETRY_COST_CONTRACT_OK synthetic clock checks only");
        }
    }
}
