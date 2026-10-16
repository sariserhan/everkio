using System;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using Everkio.AssetChecks;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class AssetCheckBuild
{
    private static void Require(bool condition,string message) { if(!condition) throw new InvalidOperationException(message); }
    public static void ExportIOS()
    {
        Require(Application.unityVersion=="6000.6.6f1","Use pinned Unity 6000.6.6f1");
        Require(EditorUserBuildSettings.activeBuildTarget==BuildTarget.iOS,"Launch Unity with -buildTarget iOS");
        string output=Argument("-everkioOutput"), bundle=Argument("-everkioBundleId");
        Require(Regex.IsMatch(bundle,@"^[A-Za-z][A-Za-z0-9-]*(\.[A-Za-z][A-Za-z0-9-]*)+$"),"Invalid bundle identifier");
        Require(!Directory.Exists(output)&&!File.Exists(output),"Refuse existing export destination");
        const string scenePath="Assets/Scenes/AssetCheck.unity";
        Require(!File.Exists(scenePath),"Use a fresh isolated project; refuse scene overwrite");
        var scene=EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
        var player=new GameObject("Local Asset Check").AddComponent<AssetCheckPlayer>();
        player.models=new GameObject[AssetCheckPlayer.CandidateCount]; player.motions=new AnimationClip[AssetCheckPlayer.CandidateCount]; player.coats=new Material[AssetCheckPlayer.CandidateCount]; player.candidateNames=new string[AssetCheckPlayer.CandidateCount];
        Directory.CreateDirectory("Assets/CheckMaterials"); AssetDatabase.Refresh();
        int index=0;
        foreach(var species in new[]{"cat","dog"}) foreach(var kind in new[]{"idle","walk","turn","react","sniff"})
        {
            string path="Assets/Candidates/"+species+"-refit-"+kind+".fbx";
            var importer=AssetImporter.GetAtPath(path) as ModelImporter; Require(importer!=null,"Missing candidate FBX");
            importer.animationType=ModelImporterAnimationType.Legacy; importer.importAnimation=true; importer.isReadable=true;
            importer.animationCompression=ModelImporterAnimationCompression.Off; importer.SaveAndReimport();
            var model=AssetDatabase.LoadAssetAtPath<GameObject>(path); Require(model!=null,"Candidate prefab missing");
            var skins=model.GetComponentsInChildren<SkinnedMeshRenderer>(); Require(skins.Length==1&&skins[0].bones.Length==46&&skins[0].sharedMesh.triangles.Length/3==30000,"Unexpected candidate structure");
            var clip=AssetDatabase.LoadAllAssetsAtPath(path).OfType<AnimationClip>().FirstOrDefault(c=>!c.name.StartsWith("__preview__"));
            Require(clip!=null&&clip.legacy&&Mathf.Abs(clip.length-6)<.01f,"Expected six-second legacy clip");
            var texture=AssetDatabase.LoadAssetAtPath<Texture2D>("Assets/Candidates/"+species+".png"); Require(texture!=null&&texture.width==2048,"Expected coat texture");
            var shader=Shader.Find("Standard"); Require(shader!=null,"Standard shader missing");
            var material=new Material(shader); material.mainTexture=texture; material.SetFloat("_Glossiness",.05f);
            AssetDatabase.CreateAsset(material,"Assets/CheckMaterials/"+species+"-"+kind+".mat");
            player.models[index]=model; player.motions[index]=clip; player.coats[index]=material; player.candidateNames[index]=species+"-"+kind; index++;
        }
        var camera=new GameObject("Preview camera").AddComponent<Camera>(); camera.orthographic=true; camera.clearFlags=CameraClearFlags.SolidColor; camera.backgroundColor=new Color(.18f,.20f,.21f); player.previewCamera=camera;
        var floor=GameObject.CreatePrimitive(PrimitiveType.Plane); floor.transform.localScale=Vector3.one*2;
        var floorMaterial=new Material(Shader.Find("Standard")); floorMaterial.color=new Color(.22f,.24f,.25f); floorMaterial.SetFloat("_Glossiness",0); AssetDatabase.CreateAsset(floorMaterial,"Assets/CheckMaterials/Floor.mat"); floor.GetComponent<Renderer>().sharedMaterial=floorMaterial;
        RenderSettings.ambientLight=new Color(.45f,.45f,.45f);
        var light=new GameObject("Preview light").AddComponent<Light>(); light.type=LightType.Directional; light.intensity=1; light.shadows=LightShadows.Soft; light.transform.rotation=Quaternion.Euler(45,-35,0);
        Directory.CreateDirectory("Assets/Scenes"); Require(EditorSceneManager.SaveScene(scene,scenePath),"Scene save failed");
        PlayerSettings.companyName="Everkio"; PlayerSettings.productName="Everkio Asset Check";
        PlayerSettings.defaultInterfaceOrientation=UIOrientation.LandscapeLeft;
        PlayerSettings.SetApplicationIdentifier(NamedBuildTarget.iOS,bundle);
        PlayerSettings.SetScriptingBackend(NamedBuildTarget.iOS,ScriptingImplementation.IL2CPP);
        AssetDatabase.SaveAssets();
        var report=BuildPipeline.BuildPlayer(new BuildPlayerOptions { scenes=new[]{scenePath}, locationPathName=output, target=BuildTarget.iOS, options=BuildOptions.Development });
        Require(report.summary.result==BuildResult.Succeeded,"Asset check iOS export failed");
        Debug.Log("EVERKIO_ASSET_DEVICE_EXPORT_OK "+output);
    }
    private static string Argument(string name)
    {
        var args=Environment.GetCommandLineArgs(); for(int i=0;i<args.Length-1;i++) if(args[i]==name&&!string.IsNullOrWhiteSpace(args[i+1])) return args[i+1];
        throw new ArgumentException("Missing "+name);
    }
}
