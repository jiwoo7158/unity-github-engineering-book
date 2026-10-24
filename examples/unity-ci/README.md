# Unity 테스트/로컬 빌드 학습 예제

이 폴더는 **독립적으로 바로 열 수 있는 전체 Unity 프로젝트가 아니다.** 소스 코드 파일 3개를 본인의 테스트 Unity 프로젝트에 옮긴 뒤 설정하는 실습 자료다. Unity 에디터, Unity Test Framework 패키지와 적절한 빌드 모듈이 필요하다.

1. `Assets/Game/Core/HealthMath.cs`를 테스트 프로젝트에 복사한다.
2. Unity에서 `Assets/Game/Core`에 Runtime `.asmdef`를 생성해 이름을 `AsterArena.Runtime`으로 정하거나, 기존 Runtime 어셈블리 구성에 포함한다.
3. `Assets/Tests/EditMode/HealthMathTests.cs`를 복사한다.
4. Unity에서 Edit Mode Test Assembly를 생성한다. 테스트 어셈블리에서 `AsterArena.Runtime`을 참조하도록 한다. NUnit/Test Framework 참조도 테스트 어셈블리에서 활성화한다. 에디터 버전에 따라 UI가 다르므로 Test Framework 문서를 확인한다.
5. Test Runner의 Edit Mode에서 테스트 3건을 실행한다.
6. `Assets/Editor/BuildScripts.cs`를 복사한다. 프로젝트에 **사용 가능한 빌드 씬을 등록**해야 한다.
7. Windows 64비트 모듈이 설치된 Unity 에디터에서 정확한 에디터 경로와 함께 아래 명령을 실행한다.

```powershell
$Unity = 'C:\Program Files\Unity\Hub\Editor\YOUR_VERSION\Editor\Unity.exe'
$Project = 'C:\Path\To\YourUnityProject'
& $Unity -batchmode -quit -projectPath $Project -buildTarget StandaloneWindows64 `
  -executeMethod AsterArena.EditorTools.BuildScripts.BuildWindows64 `
  -logFile "$Project\build.log"
```

**주의:** 예제는 특정 Unity 프로젝트/패키지 버전에서 실제 실행되었다는 보증이 없다. 프로젝트가 사용하는 Unity Editor 버전, 테스트 패키지, 라이선스, Build Profiles에 맞춰 수정해야 한다. GitHub Actions Runner에 배포하기 전에 로컬에서 먼저 검증한다.
