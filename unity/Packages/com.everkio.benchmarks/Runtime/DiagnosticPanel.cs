using UnityEngine;

namespace Everkio.Benchmarks
{
    [RequireComponent(typeof(PresenceRecorder))]
    public sealed class DiagnosticPanel : MonoBehaviour
    {
        private PresenceRecorder recorder;
        private GUIStyle label;
        private GUIStyle button;
        private int previousFrameRate;
        private void Awake()
        {
            previousFrameRate = Application.targetFrameRate;
            Application.targetFrameRate = 60;
            recorder = GetComponent<PresenceRecorder>();
            recorder.sceneContent = "instrumentation_only";
        }

        private void OnDestroy() { Application.targetFrameRate = previousFrameRate; }

        private void OnGUI()
        {
            if (label == null)
            {
                label = new GUIStyle(GUI.skin.label) { fontSize = 24, wordWrap = true };
                button = new GUIStyle(GUI.skin.button) { fontSize = 24 };
            }
            // Diagnostic controls only; no product UI or latency measurement.
            float scale = Mathf.Max(0.1f, Mathf.Min(Screen.width / 720f, Screen.height / 1000f));
            Matrix4x4 previous = GUI.matrix;
            GUI.matrix = Matrix4x4.Scale(new Vector3(scale, scale, 1));
            GUILayout.BeginArea(new Rect(30, 90, 660, 820));
            GUILayout.Label("Everkio — M0 Diagnostics", label);
            GUILayout.Label("Instrumentation only. No animal or AR scene is loaded. Results cannot establish presence quality.", label);
            GUILayout.Space(20);
            GUILayout.Label(recorder.Status, label);
            GUILayout.Label("Frames: " + recorder.SampleCount, label);
            GUI.enabled = !recorder.IsRunning;
            if (GUILayout.Button("Start cat-labelled diagnostic", button, GUILayout.Height(70))) StartCapture("cat");
            if (GUILayout.Button("Start dog-labelled diagnostic", button, GUILayout.Height(70))) StartCapture("dog");
            GUI.enabled = recorder.IsRunning;
            if (GUILayout.Button("Stop and save incomplete capture", button, GUILayout.Height(70))) recorder.StopCapture();
            GUI.enabled = true;
            GUILayout.Space(20);
            GUILayout.Label("30-second draft warm-up; 10-minute capture. Keep this app foregrounded. Update cadence is not display or touch latency.", label);
            if (!string.IsNullOrEmpty(recorder.LastExportPath)) GUILayout.Label("Saved: " + recorder.LastExportPath, label);
            GUILayout.EndArea();
            GUI.matrix = previous;
        }

        private void StartCapture(string species)
        {
            recorder.species = species;
            recorder.BeginCapture();
        }
    }
}
