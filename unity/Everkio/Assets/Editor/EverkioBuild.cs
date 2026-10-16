using System;
using System.IO;
using System.Text.RegularExpressions;
using Everkio.Benchmarks;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;

namespace Everkio.Editor
{
    // Only the M0 instrumentation scene is generated. No AR/animal demo implied.
    public static class EverkioBuild
    {
        public const string EditorVersion = "6000.6.6f1";
        private const string ScenePath = "Assets/Scenes/Diagnostics.unity";

        private static void CheckVersion()
        {
            if (Application.unityVersion != EditorVersion)
                throw new InvalidOperationException("Expected Unity " + EditorVersion + "; got " + Application.unityVersion);
        }

        [MenuItem("Everkio/Prepare M0 diagnostics")]
        public static void Prepare()
        {
            CheckVersion();
            if (!File.Exists(ScenePath))
            {
                if (!Application.isBatchMode && !EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
                    throw new InvalidOperationException("Preparation canceled; existing scene was not changed.");
                Directory.CreateDirectory("Assets/Scenes");
                AssetDatabase.Refresh();
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
                var camera = new GameObject("Diagnostic Camera").AddComponent<Camera>();
                camera.clearFlags = CameraClearFlags.SolidColor;
                camera.backgroundColor = new Color(0.04f, 0.06f, 0.07f);
                var host = new GameObject("Everkio M0 Instruments");
                host.AddComponent<PresenceRecorder>();
                host.AddComponent<DiagnosticPanel>();
                if (!EditorSceneManager.SaveScene(scene, ScenePath))
                    throw new IOException("Could not save diagnostic scene.");
            }
            // Preserve an existing scene and its edits on repeat runs.
            PlayerSettings.companyName = "Everkio";
            PlayerSettings.productName = "Everkio Diagnostics";
            AssetDatabase.SaveAssets();
            Debug.Log("EVERKIO_PREPARE_OK " + Application.unityVersion);
        }

        public static void Validate()
        {
            CheckVersion();
            if (AssetDatabase.LoadAssetAtPath<SceneAsset>(ScenePath) == null)
                throw new InvalidOperationException("Diagnostic scene missing. Run prepare first.");
            string[] thermalNames = { "unknown", "nominal", "fair", "serious", "critical" };
            for (int value = -1; value <= 3; value++)
                if (ThermalTelemetry.Name((ThermalTelemetry.State)value) != thermalNames[value + 1])
                    throw new InvalidOperationException("Thermal CSV state contract failed.");
            if (ThermalTelemetry.Name((ThermalTelemetry.State)999) != "unknown" ||
                ThermalTelemetry.Read() != ThermalTelemetry.State.Unknown)
                throw new InvalidOperationException("Unavailable/editor thermal state must remain unknown.");
            // Reaching this method establishes that editor scripts compiled.
            Debug.Log("EVERKIO_EDITOR_VALIDATION_OK " + Application.unityVersion);
        }

        public static void ExportIOS()
        {
            Validate();
            if (!BuildPipeline.IsBuildTargetSupported(BuildTargetGroup.iOS, BuildTarget.iOS))
                throw new InvalidOperationException("iOS Build Support is unavailable. Install it for Unity " + EditorVersion + " in Unity Hub, then retry.");
            if (EditorUserBuildSettings.activeBuildTarget != BuildTarget.iOS)
                throw new InvalidOperationException("Launch Unity with -buildTarget iOS before exporting.");
            string output = RequiredArgument("-everkioOutput");
            string bundleId = RequiredArgument("-everkioBundleId");
            if (!Regex.IsMatch(bundleId, @"^[A-Za-z][A-Za-z0-9-]*(\.[A-Za-z][A-Za-z0-9-]*)+$"))
                throw new ArgumentException("Invalid bundle identifier.");
            if (Directory.Exists(output) || File.Exists(output))
                throw new IOException("Export destination already exists; choose a new path to preserve prior builds.");
            PlayerSettings.SetApplicationIdentifier(NamedBuildTarget.iOS, bundleId);
            PlayerSettings.SetScriptingBackend(NamedBuildTarget.iOS, ScriptingImplementation.IL2CPP);
            // Team/signing credentials stay local in Xcode. No automatic device install.
            var report = BuildPipeline.BuildPlayer(new BuildPlayerOptions {
                scenes = new[] { ScenePath }, locationPathName = output,
                target = BuildTarget.iOS, options = BuildOptions.Development
            });
            if (report.summary.result != BuildResult.Succeeded)
                throw new InvalidOperationException("iOS export failed: " + report.summary.result);
            Debug.Log("EVERKIO_IOS_EXPORT_OK " + output);
        }

        private static string RequiredArgument(string name)
        {
            string[] args = Environment.GetCommandLineArgs();
            for (int i = 0; i < args.Length - 1; i++)
                if (args[i] == name && !String.IsNullOrWhiteSpace(args[i + 1])) return args[i + 1];
            throw new ArgumentException("Missing " + name);
        }
    }
}
