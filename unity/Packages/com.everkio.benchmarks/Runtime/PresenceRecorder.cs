using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;
using UnityEngine.Profiling;

namespace Everkio.Benchmarks
{
    /// <summary>
    /// M0 diagnostic Update cadence. Does NOT measure display presentation or
    /// input-to-visible latency. No networking, permissions, or automatic start.
    /// </summary>
    public sealed class PresenceRecorder : MonoBehaviour
    {
        [Min(0)] public float warmupSeconds = 30;
        [Min(600)] public float captureSeconds = 600;
        [Tooltip("Operator supplied: cat or dog. No animal assets are included.")]
        public string species = "";
        public string sceneContent = "instrumentation_only";
        public bool IsRunning => running;
        public int SampleCount => samples.Count;
        public string Status { get; private set; } = "Ready";
        public string LastExportPath { get; private set; } = "";
        private string capturedSpecies;
        private string capturedContent;
        private int previousSleepTimeout;

        private const int MaxSamples = 500000;
        private readonly List<Sample> samples = new List<Sample>(150000);
        private double startAt;
        private double origin;
        private bool running;
        private string runId;
        private static readonly CultureInfo Invariant = CultureInfo.InvariantCulture;

        private struct Sample
        {
            public double elapsed;
            public long memory;
            public float battery;
        }

        [Serializable]
        private sealed class Manifest
        {
            public int schema_version = 1;
            public string run_id, species, scene_content, device, os, build;
            public string protocol_revision = "everkio-presence-v2.1";
            public string evidence_kind, warmup_policy;
            public string timing_method = "unity_update_proxy";
            public bool completed;
            public int interruptions;
            public string stop_reason;
        }

        [ContextMenu("Begin diagnostic capture")]
        public void BeginCapture()
        {
            if (running) throw new InvalidOperationException("Capture already running.");
            if (species != "cat" && species != "dog")
                throw new InvalidOperationException("Set species to cat or dog first.");
            if (float.IsNaN(warmupSeconds) || float.IsInfinity(warmupSeconds) || warmupSeconds < 0 ||
                float.IsNaN(captureSeconds) || float.IsInfinity(captureSeconds) || captureSeconds < 600 || captureSeconds > 1800)
                throw new InvalidOperationException("Use a finite warmup and 600–1800 second capture.");
            samples.Clear();
            capturedSpecies = species;
            capturedContent = sceneContent;
            LastExportPath = "";
            Status = "Warming up";
            runId = DateTime.UtcNow.ToString("yyyyMMddTHHmmss", Invariant) + "-" + Guid.NewGuid().ToString("N");
            startAt = Time.realtimeSinceStartupAsDouble + warmupSeconds;
            previousSleepTimeout = Screen.sleepTimeout;
            Screen.sleepTimeout = SleepTimeout.NeverSleep;
            running = true;
        }

        private void Update()
        {
            if (!running) return;
            double now = Time.realtimeSinceStartupAsDouble;
            if (now < startAt) return;
            if (samples.Count == 0) origin = now;
            Status = "Capturing";
            if (samples.Count >= MaxSamples) { Finish(false, "sample_limit"); return; }
            samples.Add(new Sample {
                elapsed = (now - origin) * 1000,
                memory = Profiler.GetTotalAllocatedMemoryLong(),
                battery = SystemInfo.batteryLevel
            });
            if (now - origin >= captureSeconds) Finish(true, "duration_reached");
        }

        [ContextMenu("Stop diagnostic capture")]
        public void StopCapture() { Finish(false, "operator_stop"); }
        private void OnApplicationPause(bool paused) { if (paused) Finish(false, "application_pause"); }
        private void OnApplicationFocus(bool focused) { if (!focused) Finish(false, "focus_loss"); }
        private void OnDisable() { Finish(false, "component_disabled"); }
        private void OnApplicationQuit() { Finish(false, "application_quit"); }

        private void Finish(bool completed, string reason)
        {
            if (!running) return;
            running = false;
            Screen.sleepTimeout = previousSleepTimeout;
            Status = "Saving";
            // No per-frame disk IO. Export only after scoring ends. An OS kill
            // can lose buffered frames; absence of a complete bundle never passes.
            string folder = Path.Combine(Application.persistentDataPath, "EverkioBenchmarks", runId);
            try
            {
                Directory.CreateDirectory(folder);
                using (var file = new StreamWriter(Path.Combine(folder, "frames.csv"), false))
                {
                    file.WriteLine("frame_index,elapsed_ms,memory_mb,battery_level,thermal_state");
                    for (int i = 0; i < samples.Count; i++)
                    {
                        Sample s = samples[i];
                        string battery = s.battery < 0 ? "" : s.battery.ToString("R", Invariant);
                        file.WriteLine(i.ToString(Invariant) + "," + s.elapsed.ToString("R", Invariant) + "," +
                            (s.memory / 1048576.0).ToString("R", Invariant) + "," + battery + ",unknown");
                    }
                }
                var manifest = new Manifest {
                    run_id = runId, species = capturedSpecies, scene_content = capturedContent, device = SystemInfo.deviceModel,
                    os = SystemInfo.operatingSystem, build = Application.buildGUID,
                    evidence_kind = Application.isEditor ? "editor" : "unverified_player",
                    warmup_policy = warmupSeconds.ToString("R", Invariant) + " seconds; draft, not frozen",
                    completed = completed, interruptions = completed ? 0 : 1, stop_reason = reason
                };
                File.WriteAllText(Path.Combine(folder, "manifest.json"), JsonUtility.ToJson(manifest, true));
                LastExportPath = folder;
                Status = completed ? "Capture complete (diagnostic only)" : "Incomplete: " + reason;
                Debug.Log("Everkio diagnostic evidence saved: " + folder);
            }
            catch (Exception error)
            {
                Status = "Export failed; no valid evidence";
                Debug.LogError("Everkio capture export failed; no valid evidence: " + error);
            }
        }
    }
}
