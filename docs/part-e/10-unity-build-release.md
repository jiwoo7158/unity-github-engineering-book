# 10. Unity 자동 빌드와 CD

## 10.1 테스트와 빌드의 차이

테스트는 특정 동작이나 규칙의 정확성을 확인한다. **빌드(Build)**는 게임 프로젝트의 코드·에셋·설정을 실제 실행 파일 또는 대상 플랫폼 패키지로 변환한다. Unity Editor의 Play Mode에서 잘 동작하더라도 빌드에서는 다른 문제가 발생할 수 있다.

예: Editor 전용 API를 Runtime 코드에서 사용하거나, Addressables/StreamingAssets 설정이 누락되거나, 플랫폼별 그래픽·플러그인 호환성이 달라질 수 있다. 따라서 **클린 빌드의 성공과 Player 실행 확인**은 별도의 검증 항목이다.

- **CI**: 변경을 통합하면서 테스트·빌드 등 검사를 반복하는 실천.
- **Continuous Delivery**: 언제든 출시 가능한 산출물을 준비하는 접근.
- **Continuous Deployment**: 검증을 통과한 결과물을 사람 승인 없이 자동 배포하는 접근.
- **GitHub Actions**: 이를 구성하는 도구로, CD를 도입하려면 실제 배포 권한과 승인 절차까지 설계해야 한다.

게임 팀에서는 처음부터 자동 배포까지 가기보다 **자동 빌드 → 내부 테스터 배포 → Release Candidate 승인** 순서가 안전하다.

## 10.2 Unity의 빌드 요소

| 요소 | 내용 | 중요한 이유 |
|---|---|---|
| Build Target | Windows, Linux, Android 등 | 플랫폼별 실행 결과가 다름 |
| Build Profiles | Unity 버전에 따른 빌드 설정 관리 | 여러 설정의 재현성 |
| Build Configuration | Development/Release 등 | 디버그 기능·최적화 차이 |
| Scene List | 실제 빌드에 포함되는 씬 | 누락하면 시작·이동 오류 |
| Scripting Backend | Mono/IL2CPP 등 | 플랫폼 및 빌드 환경 영향 |
| Define Symbols | 조건부 컴파일 | 에디터/실빌드 결과 차이 |
| Player Settings | 회사명·제품명·버전·아이콘 등 | 배포되는 게임 정보 |
| Output Path | 빌드 파일의 저장 위치 | Artifact 수집에 필요 |

Unity 6 계열에서는 **Build Profiles** 관련 UI를 중심으로 빌드 설정을 관리할 수 있다. 이전 버전의 `Build Settings` 설명과 혼동하지 말고 사용 중인 에디터 버전의 공식 매뉴얼을 확인하자.

## 10.3 재현 가능한 로컬 명령줄 빌드

처음부터 Actions로 자동화하지 않는다. **개발자 컴퓨터에서 CLI 빌드를 성공**시키고, 그 명령을 Runner에서도 사용할 수 있는지 확인한다.

```csharp
// Assets/Editor/CI/BuildScript.cs
using System;
using System.IO;
using UnityEditor;
using UnityEditor.Build.Reporting;

public static class BuildScript
{
    public static void BuildWindows()
    {
        const string outputPath = "Builds/Windows/AsterArena.exe";
        string directory = Path.GetDirectoryName(outputPath);
        if (!string.IsNullOrEmpty(directory))
            Directory.CreateDirectory(directory);

        // 현재 프로젝트에서 활성화된 빌드 씬만 포함한다.
        string[] scenes = Array.ConvertAll(
            Array.FindAll(EditorBuildSettings.scenes, s => s.enabled),
            s => s.path);

        if (scenes.Length == 0)
            throw new InvalidOperationException("No enabled scenes for build.");

        var options = new BuildPlayerOptions
        {
            scenes = scenes,
            locationPathName = outputPath,
            target = BuildTarget.StandaloneWindows64,
            options = BuildOptions.None
        };

        BuildReport report = BuildPipeline.BuildPlayer(options);
        if (report.summary.result != BuildResult.Succeeded)
            throw new Exception($"Build failed: {report.summary.result}");
    }
}
```

- `Assets/Editor`에 있으므로 **에디터 코드**로 컴파일한다.
- `EditorBuildSettings.scenes`에서 활성 씬을 수집한다. 게임의 Bootstrap 씬이 빠지지 않았는지 확인한다.
- 출력 경로는 프로젝트 루트를 기준으로 해석되는 경우를 가정한 예시이며, 실제 빌드 스크립트 실행 환경에 맞춰 절대 경로 처리가 필요할 수 있다.
- `BuildTarget.StandaloneWindows64`를 명시했지만 실행하는 Editor에 해당 플랫폼 모듈이 설치되어 있어야 한다.
- 실제 배포에서는 게임 버전·빌드 번호·조건부 컴파일·주소 가능 에셋 빌드 절차 등을 추가로 고려한다.

### Windows PowerShell에서 실행

```powershell
& "C:\Program Files\Unity\Hub\Editor\YOUR_VERSION\Editor\Unity.exe" `
  -batchmode -quit `
  -projectPath "C:\Work\AsterArena" `
  -executeMethod BuildScript.BuildWindows `
  -logFile "C:\Work\build.log"
```

`YOUR_VERSION`, 프로젝트 경로와 Output 경로를 실제 값으로 바꾼다. 실행 후 빌드 디렉터리와 로그, 프로세스 종료 코드, 실행 파일의 실제 실행까지 확인한다. Unity 프로세스가 성공적으로 종료되어도 **게임이 정상 플레이된다는 보장은 없다**.

## 10.4 Unity 라이선스와 Runner 선택

GitHub Actions Runner에서 Unity Editor를 실행하려면 **설치·플랫폼 모듈·라이선스 활성화**가 필요하다. 여기서 많은 팀이 처음 실패한다.

- Unity Personal, Pro 등 라이선스 유형에 따라 허용되는 비대화형 인증 방식과 계정·시트 관리가 달라질 수 있다.
- Unity Hub 기반 로그인과 명령줄/빌드 서버 활성화는 서로 다른 제약이 있을 수 있다.
- CI용 비밀 값을 GitHub Secrets로 보관하더라도 서비스 약관과 라이선스 허용 범위에 적합해야 한다.
- Self-hosted Runner는 Unity Editor를 미리 설치한 머신을 재사용할 수 있지만 보안·운영 관리가 필요하다.
- GitHub-hosted Runner는 매번 실행 환경을 준비해야 할 수 있어 빌드 시간이 길어질 수 있다.

**이 책은 라이선스 키를 임의로 생성하거나 개인 라이선스 활성화를 우회하는 방법을 다루지 않는다.** 사용 중인 Unity 버전과 라이선스의 공식 빌드 자동화 가이드에 따라 설정해야 한다.

## 10.5 Actions 자동 빌드 설계 예시

다음은 **Runner에 Unity가 설치되어 있고, Windows에서 합법적으로 활성화된 라이선스를 사용한다는 전제**를 가진 워크플로 예시다. 이 파일을 그대로 제출하면 모든 저장소에서 동작하는 만능 구성은 아니다. Self-hosted Runner의 레이블, Editor 경로, 보안 범위를 먼저 맞춰야 한다.

```yaml
name: Unity Windows Build
on:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  build:
    runs-on: [self-hosted, windows, unity-builder]
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true
      - name: Build player
        shell: pwsh
        run: |
          & "${{ vars.UNITY_EDITOR_PATH }}" `
            -batchmode -quit `
            -projectPath "${{ github.workspace }}" `
            -executeMethod BuildScript.BuildWindows `
            -logFile "${{ github.workspace }}/unity-build.log"
      - name: Upload build
        uses: actions/upload-artifact@v4
        with:
          name: aster-arena-windows
          path: Builds/Windows/
          if-no-files-found: error
      - name: Upload log
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: unity-build-log
          path: unity-build.log
          if-no-files-found: warn
```

**운영 전 점검:**

1. Runner에 `unity-builder` 라벨이 설정되어 있는가?
2. `vars.UNITY_EDITOR_PATH`가 올바른 exe 경로인가?
3. 빌드 대상 플랫폼 모듈이 설치되어 있는가?
4. Unity 라이선스가 해당 Runner에서 합법적으로 활성화되어 있는가?
5. `BuildScript.BuildWindows` 메서드가 프로젝트에 있고 씬 목록이 준비되어 있는가?
6. 출력 폴더가 실제로 생성되는가?
7. 이 Runner에서 신뢰하지 않는 PR 코드를 실행하지 않도록 보호했는가?

## 10.6 Git LFS와 패키지 복원

Unity 자동 빌드는 단순 C# 컴파일이 아니다. 코드뿐 아니라 텍스처·모델·애니메이션·패키지 등이 있어야 한다.

- `actions/checkout` 단계에서 LFS 다운로드가 필요한지 확인한다.
- 에셋이 LFS 포인터 상태로 남지 않았는지 빌드 전에 검사한다.
- `manifest.json`과 lockfile이 올바르게 추적되는지 확인한다.
- 패키지 레지스트리 접근/사설 패키지 인증/사내 파일 서버 의존성을 파악한다.
- Library 캐시는 최적화 수단이지, 누락된 에셋을 보완하는 대체품이 아니다.

## 10.7 Cache와 빌드 시간

Unity의 `Library` 캐시는 임포트 시간을 줄일 수 있지만 용량이 크고, Unity 버전·대상 플랫폼·패키지 변화에 따라 유효성이 달라진다. 잘못된 캐시를 재사용해 원인 불명의 오류가 발생할 수 있다.

**캐시 키에 고려할 값:** OS, Unity 버전, 타깃 플랫폼, `manifest.json`, lockfile, 주요 빌드 옵션. 성능 향상을 확인하기 전에는 캐시 구조를 과하게 최적화하지 않는다. 캐시 내용에 기밀 데이터가 들어가지 않도록 한다.

## 10.8 빌드 Artifact와 GitHub Release

| 항목 | Actions Artifact | GitHub Release |
|---|---|---|
| 목적 | CI 실행의 일시적 결과 전달 | 버전별 공개/공유 배포 기록 |
| 일반적 수명 | 보관 정책에 따라 제한 | 릴리스 관리 정책에 따라 유지 |
| 사용 시점 | PR 검증·테스터 빌드 | 데모·정식 릴리스·핫픽스 |
| 연결 정보 | 실행 번호·커밋 SHA | Git Tag·버전·릴리스 노트 |

릴리스에는 예를 들어 `v0.2.0-beta.1`처럼 **정해진 버전 규칙**을 사용한다. Git Tag는 특정 커밋을 표시하는 이력 표식이며 Release는 그 버전을 사용자에게 설명하고 파일을 첨부하는 GitHub 기능이다.

## 10.9 릴리스 승인과 사고 복구

최종 게임 파일을 배포하기 전에 다음을 확인하자.

- 클린 환경에서 설치·실행 가능한가?
- 게임 시작·저장·로드·종료·재실행이 가능한가?
- 실제 타깃 하드웨어에서 프레임 및 메모리 사용량이 허용 범위인가?
- 컨트롤러와 해상도 옵션이 정상 동작하는가?
- 상용 에셋·오픈소스 패키지의 라이선스 요구사항을 충족하는가?
- 문제가 생기면 이전 버전으로 되돌리거나 핫픽스를 배포할 수 있는가?
- 세이브 데이터가 이전 버전과 호환되는가? 업데이트 후 되돌리기가 항상 안전한 것은 아니다.

## 10.10 실습과 확인 기준

로컬 명령줄로 Windows 게임을 한 번 빌드하고, 실습용 별도 폴더에서 실행한다. 기록할 값은 **Unity 버전, Commit SHA, 빌드 옵션, 실행 경로, 테스트 결과**다. 이후 조건이 갖춰졌다면 수동 Actions 워크플로를 실행해 Artifact를 생성한다.

**확인할 결과:** 에디터에서 실행되는 상태와 실제 사용자에게 배포되는 빌드가 다르다는 점을 이해하고, 특정 커밋을 기반으로 다시 게임을 빌드할 수 있다.

**공식 자료:** [Unity Build Profiles](https://docs.unity3d.com/Manual/BuildSettings.html), [빌드 스크립팅](https://docs.unity3d.com/ScriptReference/BuildPipeline.BuildPlayer.html), [Actions Artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts), [Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)

---

## 10.11 확장: Unity 빌드를 자동화하기 전에 하는 로컬 검증

CI 환경 구축이 실패하는 흔한 이유는 **로컬에서도 검증되지 않은 빌드 명령을 곧바로 Actions에 넣기 때문**이다. 먼저 로컬 PC에서 에디터 GUI를 열지 않고 동일한 결과를 낼 수 있는지 확인한다.

1. `ProjectSettings/ProjectVersion.txt`를 확인해 Unity 버전을 정확히 기록한다.
2. `Packages/manifest.json`과 `packages-lock.json`이 저장소에 포함되어 있는지 확인한다.
3. Build Profiles 또는 프로젝트 빌드 설정에서 대상 플랫폼을 확인한다.
4. 빈 폴더에 프로젝트를 Clone하여 정상적으로 로드되는지 테스트한다.
5. 준비된 빌드 스크립트를 Unity 명령줄에서 실행한다.
6. 로그와 실행 결과를 확인하고, 생성된 `.exe` 등 게임 파일을 실제로 실행한다.

```powershell
$Unity = 'C:\Program Files\Unity\Hub\Editor\YOUR_VERSION\Editor\Unity.exe'
$Project = 'C:\Work\AsterArena'
& $Unity -batchmode -quit -projectPath $Project `
  -buildTarget StandaloneWindows64 `
  -executeMethod BuildScripts.BuildWindows64 `
  -logFile "$Project\build.log"
```

`BuildScripts.BuildWindows64`은 프로젝트 안에 실제로 정의해야 하는 **사용자 작성 static 메서드**다. 이름만 지정한다고 Unity에 자동 생성되는 것이 아니다. Unity 6 계열의 명령줄 빌드에서는 빌드 타깃 또는 프로필을 명시하는 것이 특히 중요하다. [공식 명령줄 빌드 문서](https://docs.unity3d.com/kr/current/Manual/build-command-line.html)를 참고한다.

## 10.12 빌드 스크립트 예제의 경계와 안전 조건

책에 포함된 `examples/unity-ci/BuildScripts.cs`는 Windows Standalone Player를 위한 최소 학습 예제다. Unity Editor 전용 코드로 컴파일되도록 `Editor/` 디렉터리에 넣고 사용한다.

최소 빌드 예제는 게임의 제작용 빌드 정책 전체를 제공하지 않는다. 실제 프로젝트에서는 별도로 다음을 정한다.

- 어떤 씬을 빌드에 포함하는가?
- 버전 번호는 누가, 어떤 절차로 바꾸는가?
- Build Target과 플랫폼별 옵션은 무엇인가?
- 개발용 로그·디버깅 심벌을 포함하는가?
- 실패했을 때 작업 전체를 실패로 표시하는가?
- 결과물의 위치와 보존 기간은 어떻게 되는가?

### Runner 선택지

| Runner | 장점 | 주의할 점 |
|---|---|---|
| GitHub-hosted | 컴퓨터·OS 유지보수 부담 감소 | Unity 설치·활성화·비용 설정이 필요 |
| Self-hosted (팀 PC) | 현재 설치된 Unity 환경 재사용 가능 | 보안, 작업 중단, PC 절전, 장기 유지보수 |
| 전문 Unity 빌드 서비스 | 게임 엔진 중심 작업 흐름 | 요금·기능·제약을 따로 검토 |

Self-hosted Runner는 GitHub에서 관련 지침을 따라 **직접 설치해야 하는 프로그램**이다. 단순히 Actions를 켜는 것만으로 로컬 PC가 Runner가 되지 않는다. 신뢰할 수 없는 외부 코드가 팀원의 PC에서 실행되지 않도록 이벤트와 Runner 접근 범위를 제한해야 한다.

## 10.13 완전 자동화보다 검증 가능한 단계적 자동화

권장 도입 순서:

1. **로컬 수동 빌드**: 정확한 에디터 버전과 절차를 문서화한다.
2. **로컬 명령줄 빌드**: 사람의 클릭 없이 동일 빌드를 생성한다.
3. **수동 트리거 Action**: 안전하게 준비된 Runner에서만 빌드를 시작한다.
4. **PR 테스트**: 빌드 없이도 빠르게 검증 가능한 작은 검사를 추가한다.
5. **정기 통합 빌드**: 비용과 필요성이 충분할 때 도입한다.
6. **릴리스 자동화**: 산출물 검증·승인 조건을 먼저 확립한 뒤 도입한다.

팀의 Unity 버전, 라이선스, Runner OS, 패키지 의존성이 맞지 않는다면 3단계부터 즉시 실행하기 어렵다. 설명 편의를 위해 **Secrets에 인증 문자열을 임의로 만들어 넣거나** 검증되지 않은 활성화 명령을 복사해 실행하지 않는다.

## 10.14 빌드 검증 결과를 어디까지 남길까?

다음 정도의 메타데이터는 남기는 것을 추천한다.

```text
Build ID: 0.3.4-dev.8
Git commit: <actual-commit-sha>
Unity version: <exact-editor-version>
Target: Windows x64
Build method: BuildScripts.BuildWindows64
Automated tests: 12 passed / 0 failed
Playtest: 미수행 (별도 검증 필요)
Known issues: BUG-41, BUG-43
```

실제 Git SHA와 에디터 버전은 빌드 과정에서 수집하도록 자동화할 수 있다. 예시 문자열을 그대로 출시 기록으로 옮기지 말자.

**추가 실습:** Windows 빌드를 로컬에서 실행하고, `build.log`와 산출물 폴더를 확인한다. 스크립트를 일부러 잘못된 씬 경로로 변경했을 때 실패를 명확하게 감지할 수 있는지도 검증한다. 그다음 실제 프로젝트에서 어떤 Runner를 운영할지 결정한다.
