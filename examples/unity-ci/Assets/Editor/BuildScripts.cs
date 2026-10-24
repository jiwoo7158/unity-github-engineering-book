#if UNITY_EDITOR
using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;

namespace AsterArena.EditorTools
{
    public static class BuildScripts
    {
        // Called with: -executeMethod AsterArena.EditorTools.BuildScripts.BuildWindows64
        public static void BuildWindows64()
        {
            string[] scenes = EditorBuildSettings.scenes
                .Where(s => s.enabled)
                .Select(s => s.path)
                .ToArray();
            if (scenes.Length == 0)
                throw new BuildFailedException("No enabled scenes in Build Profiles/Settings.");

            string output = Path.GetFullPath("Builds/Windows/AsterArena.exe");
            Directory.CreateDirectory(Path.GetDirectoryName(output));

            BuildReport report = BuildPipeline.BuildPlayer(new BuildPlayerOptions
            {
                scenes = scenes,
                locationPathName = output,
                target = BuildTarget.StandaloneWindows64,
                options = BuildOptions.None
            });

            if (report.summary.result != BuildResult.Succeeded)
                throw new BuildFailedException("Windows build did not succeed.");

            UnityEngine.Debug.Log("Build success: " + output);
        }
    }
}
#endif
