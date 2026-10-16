using System;
using System.Collections;
using System.IO;
using UnityEngine;

namespace Everkio.Benchmarks
{
    [RequireComponent(typeof(PresenceRecorder))]
    public sealed class DiagnosticPanel : MonoBehaviour
    {
        private PresenceRecorder recorder;
        private InputMarkerPanel inputMarker;
        private TelemetryCostProbe costProbe;
        private GUIStyle label;
        private GUIStyle button;
        private Vector2 scroll;
        private int previousFrameRate;
        private bool savingScreenshot;
        public bool IsSavingScreenshot => savingScreenshot;
        private string screenshotStatus = "Screenshots save to private app files, not Photos. Video recording is not included.";
        private void Awake()
        {
            previousFrameRate = Application.targetFrameRate;
            Application.targetFrameRate = 60;
            recorder = GetComponent<PresenceRecorder>();
            inputMarker = GetComponent<InputMarkerPanel>();
            if (inputMarker == null) inputMarker = gameObject.AddComponent<InputMarkerPanel>();
            costProbe = GetComponent<TelemetryCostProbe>();
            if (costProbe == null) costProbe = gameObject.AddComponent<TelemetryCostProbe>();
            recorder.sceneContent = "instrumentation_only";
        }

        private void OnDestroy() { Application.targetFrameRate = previousFrameRate; }

        private void OnGUI()
        {
            if (inputMarker != null && inputMarker.IsRunning) return;
            if (label == null)
            {
                label = new GUIStyle(GUI.skin.label) { fontSize = 24, wordWrap = true };
                button = new GUIStyle(GUI.skin.button) { fontSize = 24 };
            }
            // Diagnostic controls only; no product UI or latency measurement.
            Rect safe = Screen.safeArea;
            float scale = Mathf.Max(0.1f, Mathf.Min(safe.width / 720f, safe.height / 1000f));
            Matrix4x4 previous = GUI.matrix;
            GUI.matrix = Matrix4x4.Scale(new Vector3(scale, scale, 1));
            GUILayout.BeginArea(new Rect(safe.x / scale + 30, (Screen.height - safe.yMax) / scale + 30,
                safe.width / scale - 60, safe.height / scale - 60));
            scroll = GUILayout.BeginScrollView(scroll);
            GUILayout.Label("Everkio — M0 Diagnostics", label);
            GUILayout.Label("Instrumentation only. No animal or AR scene is loaded. Results cannot establish presence quality.", label);
            GUILayout.Space(20);
            GUILayout.Label(recorder.Status, label);
            if (recorder.IsRunning)
            {
                double remaining = recorder.SampleCount == 0 ? recorder.WarmupRemainingSeconds :
                    System.Math.Max(0, recorder.captureSeconds - recorder.ElapsedSeconds);
                int seconds = (int)System.Math.Ceiling(remaining);
                GUILayout.Label((recorder.SampleCount == 0 ? "Warm-up remaining: " : "Capture remaining: ") +
                    (seconds / 60) + ":" + (seconds % 60).ToString("D2"), label);
                GUILayout.Label("Wait for Capture complete. Stop saves an incomplete run.", label);
            }
            GUILayout.Label("Frames: " + recorder.SampleCount, label);
            GUILayout.Label("Device thermal state: " + recorder.ThermalState, label);
            GUI.enabled = !recorder.IsRunning && !savingScreenshot && !costProbe.IsRunning;
            if (GUILayout.Button("Start cat-labelled diagnostic", button, GUILayout.Height(70))) StartCapture("cat");
            if (GUILayout.Button("Start dog-labelled diagnostic", button, GUILayout.Height(70))) StartCapture("dog");
            GUI.enabled = recorder.IsRunning;
            if (GUILayout.Button("Stop and save incomplete capture", button, GUILayout.Height(70))) recorder.StopCapture();
            GUI.enabled = true;
            GUILayout.Space(20);
            GUI.enabled = !recorder.IsRunning && !savingScreenshot && !costProbe.IsRunning;
            if (GUILayout.Button("Save diagnostic screenshot", button, GUILayout.Height(70)))
                StartCoroutine(SaveDiagnosticScreenshot());
            GUI.enabled = true;
            GUILayout.Label(screenshotStatus, label);
            GUI.enabled = !recorder.IsRunning && !savingScreenshot && !costProbe.IsRunning;
            if (GUILayout.Button("Start input marker setup", button, GUILayout.Height(70))) inputMarker.Begin();
            GUI.enabled = true;
            GUILayout.Label(inputMarker.Status, label);
            GUI.enabled = !recorder.IsRunning && !savingScreenshot && !costProbe.IsRunning;
            if (GUILayout.Button("Measure telemetry call cost (setup only)", button, GUILayout.Height(70))) costProbe.Begin();
            GUI.enabled = true;
            GUILayout.Label(costProbe.Status, label);
            if (recorder.IsRunning) GUILayout.Label("Screenshots are available after the data capture stops, to avoid disturbing timing samples.", label);
            GUILayout.Label("30-second draft warm-up; 10-minute capture. Keep this app foregrounded. Update cadence is not display or touch latency.", label);
            if (!string.IsNullOrEmpty(recorder.LastExportPath)) GUILayout.Label("Saved: " + recorder.LastExportPath, label);
            GUILayout.EndScrollView();
            GUILayout.EndArea();
            GUI.matrix = previous;
        }

        private void StartCapture(string species)
        {
            recorder.species = species;
            recorder.BeginCapture();
        }

        private IEnumerator SaveDiagnosticScreenshot()
        {
            savingScreenshot = true;
            screenshotStatus = "Saving diagnostic screenshot...";
            yield return new WaitForEndOfFrame();
            Texture2D screenshot = null;
            try
            {
                if (!Application.isFocused || recorder.IsRunning || costProbe.IsRunning || inputMarker.IsRunning)
                    throw new InvalidOperationException("Keep the app foregrounded and stop data capture before saving a screenshot.");
                screenshot = ScreenCapture.CaptureScreenshotAsTexture();
                if (screenshot == null) throw new IOException("Screen capture returned no image.");
                byte[] png = screenshot.EncodeToPNG();
                if (png == null || png.Length == 0) throw new IOException("Screenshot encoding returned no PNG.");
                string folder = Path.Combine(Application.persistentDataPath, "EverkioDiagnostics", "Screenshots");
                Directory.CreateDirectory(folder);
                string path = Path.Combine(folder, DateTime.UtcNow.ToString("yyyyMMddTHHmmss") + "-" + Guid.NewGuid().ToString("N") + ".png");
                using (var file = new FileStream(path, FileMode.CreateNew, FileAccess.Write)) file.Write(png, 0, png.Length);
                screenshotStatus = "Screenshot saved: " + Path.GetFileName(path);
                Debug.Log("Everkio diagnostic screenshot saved: " + path);
            }
            catch (Exception error)
            {
                screenshotStatus = "Screenshot failed: " + error.Message;
                Debug.LogError("Everkio diagnostic screenshot failed: " + error);
            }
            finally
            {
                if (screenshot != null) Destroy(screenshot);
                savingScreenshot = false;
            }
        }

        private void OnDisable()
        {
            StopAllCoroutines();
            if (savingScreenshot) screenshotStatus = "Screenshot canceled before export completed.";
            savingScreenshot = false;
        }
    }
}
