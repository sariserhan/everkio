using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

namespace Everkio.AssetChecks
{
    // Separate preflight app; never an animal/AR performance or presence study.
    public sealed class AssetCheckPlayer : MonoBehaviour
    {
        public GameObject[] models;
        public AnimationClip[] motions;
        public Material[] coats;
        public string[] candidateNames;
        public Camera previewCamera;
        [Serializable] public sealed class Entry { public string candidate, screenshot, error; public int vertices, bones, pngBytes; public float minimumY, height, motionExtent, animationTime; public double elapsedSeconds; }
        [Serializable] public sealed class Report
        {
            public string schema = "everkio-asset-device-check-1", presence_gate = "NOT RUN";
            public string scope = "Draft local mesh/clip check; no AR, realism, display timing or touch acceptance";
            public string device, os, unity, graphics, build, runId, startedUtc, error;
            public bool completed, interrupted;
            public Entry[] entries;
        }
        private readonly List<Entry> entries = new List<Entry>();
        private Report report;
        private GameObject actor;
        private SkinnedMeshRenderer skin;
        private Animation clipPlayer;
        private Vector3[] initialSurface;
        private string folder, status = "Starting local asset check";
        private int previousSleep, previousRate;
        private bool running;

        private IEnumerator Start()
        {
            previousSleep = Screen.sleepTimeout; previousRate = Application.targetFrameRate;
            Screen.sleepTimeout = SleepTimeout.NeverSleep; Application.targetFrameRate = 60;
            report = new Report { device=SystemInfo.deviceModel, os=SystemInfo.operatingSystem,
                unity=Application.unityVersion, graphics=SystemInfo.graphicsDeviceType.ToString(), build=Application.buildGUID,
                runId=Guid.NewGuid().ToString("N"), startedUtc=DateTime.UtcNow.ToString("O") };
            folder=Path.Combine(Application.persistentDataPath,"EverkioAssetChecks",report.runId);
            running=true;
            for (int index=0; index<candidateNames.Length; index++)
            {
                if (!SelectCandidate(index)) break;
                double began=Time.realtimeSinceStartupAsDouble;
                status=(index+1)+"/"+candidateNames.Length+" — "+candidateNames[index];
                while (Time.realtimeSinceStartupAsDouble-began<2 && !report.interrupted) yield return null;
                if (report.interrupted) break;
                yield return new WaitForEndOfFrame();
                var entry=Capture(candidateNames[index],Time.realtimeSinceStartupAsDouble-began);
                entries.Add(entry);
                if (!string.IsNullOrEmpty(entry.error)) break;
                while (Time.realtimeSinceStartupAsDouble-began<6.2 && !report.interrupted) yield return null;
                if (report.interrupted) break;
            }
            report.entries=entries.ToArray();
            report.completed=entries.Count==4 && !report.interrupted && string.IsNullOrEmpty(report.error) && entries.TrueForAll(e=>string.IsNullOrEmpty(e.error));
            running=false;
            Screen.sleepTimeout=previousSleep;
            try
            {
                Directory.CreateDirectory(folder);
                using(var file=new StreamWriter(new FileStream(Path.Combine(folder,"report.json"),FileMode.CreateNew,FileAccess.Write)))
                    file.Write(JsonUtility.ToJson(report,true));
                status=report.completed ? "Local asset check complete — G-P NOT RUN" : "Incomplete asset check — inspect report";
                Debug.Log("EVERKIO_ASSET_CHECK_SAVED "+folder+" completed="+report.completed);
            }
            catch(Exception error) { status="Report export failed: "+error.Message; Debug.LogError(status); }
        }
        private bool SelectCandidate(int index)
        {
            try
            {
                if(actor!=null) Destroy(actor);
                actor=Instantiate(models[index]);
                var renderers=actor.GetComponentsInChildren<SkinnedMeshRenderer>();
                if(renderers.Length!=1 || renderers[0].bones.Length!=46) throw new InvalidOperationException("Unexpected skin/bone structure");
                skin=renderers[0]; skin.sharedMaterial=coats[index]; skin.updateWhenOffscreen=true;
                var animation=actor.GetComponent<Animation>(); if(animation==null) animation=actor.AddComponent<Animation>();
                animation.Stop(); animation.AddClip(motions[index],"asset-check");
                animation["asset-check"].wrapMode=candidateNames[index].EndsWith("idle") ? WrapMode.Loop : WrapMode.ClampForever;
                if(!animation.Play("asset-check")) throw new InvalidOperationException("Animation did not start");
                clipPlayer=animation; animation["asset-check"].time=0; animation.Sample();
                var initial=new Mesh();
                try
                {
                    skin.BakeMesh(initial,true); var vertices=initial.vertices; initialSurface=new Vector3[vertices.Length];
                    for(int i=0;i<vertices.Length;i++) initialSurface[i]=skin.transform.TransformPoint(vertices[i]);
                }
                finally { Destroy(initial); }
                return true;
            }
            catch(Exception error) { report.error=error.ToString(); Debug.LogError(report.error); return false; }
        }
        private Entry Capture(string candidate,double elapsed)
        {
            var entry=new Entry { candidate=candidate, elapsedSeconds=elapsed };
            Mesh baked=null; Texture2D screenshot=null;
            try
            {
                if(!Application.isFocused || report.interrupted) throw new InvalidOperationException("App must remain foregrounded");
                baked=new Mesh(); skin.BakeMesh(baked,true);
                float minimum=float.PositiveInfinity, maximum=float.NegativeInfinity;
                var vertices=baked.vertices;
                if(initialSurface.Length!=vertices.Length) throw new InvalidOperationException("Skin topology changed");
                for(int i=0;i<vertices.Length;i++)
                {
                    var p=skin.transform.TransformPoint(vertices[i]);
                    entry.motionExtent=Mathf.Max(entry.motionExtent,Vector3.Distance(p,initialSurface[i]));
                    if(!float.IsFinite(p.x)||!float.IsFinite(p.y)||!float.IsFinite(p.z)) throw new InvalidOperationException("Nonfinite skinned surface");
                    minimum=Mathf.Min(minimum,p.y); maximum=Mathf.Max(maximum,p.y);
                }
                entry.vertices=baked.vertexCount; entry.bones=skin.bones.Length; entry.minimumY=minimum; entry.height=maximum-minimum;
                if(entry.vertices==0 || minimum<-.0001f || entry.height<.8f || entry.height>1.2f) throw new InvalidOperationException("Sampled surface bounds/floor check failed");
                entry.animationTime=clipPlayer["asset-check"].time;
                if(!clipPlayer.isPlaying || entry.animationTime<.1f || entry.motionExtent<.001f) throw new InvalidOperationException("Animated surface did not advance");
                screenshot=ScreenCapture.CaptureScreenshotAsTexture();
                if(screenshot==null) throw new IOException("Screenshot unavailable");
                var png=screenshot.EncodeToPNG(); if(png==null || png.Length<8) throw new IOException("PNG encoding failed");
                Directory.CreateDirectory(folder); entry.screenshot=candidate+".png";
                using(var file=new FileStream(Path.Combine(folder,entry.screenshot),FileMode.CreateNew,FileAccess.Write)) file.Write(png,0,png.Length);
                entry.pngBytes=png.Length;
            }
            catch(Exception error) { entry.error=error.ToString(); Debug.LogError(entry.error); }
            finally { if(baked!=null) Destroy(baked); if(screenshot!=null) Destroy(screenshot); }
            return entry;
        }
        private void LateUpdate()
        {
            if(skin==null) return;
            var target=skin.bounds.center;
            previewCamera.orthographicSize=Mathf.Max(.82f,.95f/previewCamera.aspect);
            previewCamera.transform.position=target+new Vector3(2.5f,.9f,3);
            previewCamera.transform.LookAt(target);
        }
        private void OnGUI()
        {
            var safe=Screen.safeArea; float scale=Mathf.Max(.1f,Mathf.Min(safe.width/1100f,safe.height/650f)); var previous=GUI.matrix;
            GUI.matrix=Matrix4x4.Scale(new Vector3(scale,scale,1));
            var style=new GUIStyle(GUI.skin.label) { fontSize=26, wordWrap=true };
            float x=safe.x/scale+20, y=(Screen.height-safe.yMax)/scale+15;
            GUI.Label(new Rect(x,y,safe.width/scale-40,70),"Everkio — DRAFT ASSET CHECK\n"+status,style);
            GUI.Label(new Rect(x,(Screen.height-safe.yMin)/scale-75,safe.width/scale-40,70),"Automatic local clip/PNG test. Keep foregrounded.\nAR, realism, performance and touch acceptance: NOT RUN.",style);
            GUI.matrix=previous;
        }
        private void OnApplicationFocus(bool focused) { if(running&&!focused) report.interrupted=true; }
        private void OnApplicationPause(bool paused) { if(running&&paused) report.interrupted=true; }
        private void OnDestroy() { Screen.sleepTimeout=previousSleep; Application.targetFrameRate=previousRate; }
    }
}
