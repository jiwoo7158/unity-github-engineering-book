# 09. Unity 테스트 자동화와 CI

## 9.1 게임 QA와 자동 테스트의 역할

액션 게임에서 회피의 무적 판정이나 피해 계산이 규칙대로 동작하는지 검증하는 일과, 회피가 '기분 좋게 느껴지는지' 확인하는 일은 다르다. 전자는 자동 테스트에 적합할 수 있고 후자는 실제 플레이와 관찰이 필요하다.

| 영역 | 추천 검증 | 자동화 적합성 |
|---|---|---|
| 피해량·경험치 계산 | Unit Test | 높음 |
| 아이템 수량과 소비 규칙 | Unit Test | 높음 |
| 세이브 직렬화·역직렬화 | Integration Test | 높음 |
| 게임 상태 전환 | Edit/Play Mode Test | 중간~높음 |
| 물리 판정·애니메이션 타이밍 | Play Mode 또는 수동 | 중간 |
| 타격감·난이도·UI 직관성 | 실제 플레이테스트 | 낮음 |
| FPS·메모리·GC | 프로파일링·성능 측정 | 일부 자동화 가능 |

**CI(지속적 통합)**는 변경을 자주 통합하고 자동 검사를 수행해 회귀 문제를 조기에 발견하는 실천이다. GitHub Actions는 CI 실행 도구이지, 테스트 설계를 자동으로 완성해 주는 도구가 아니다.

## 9.2 Unity Test Framework와 Test Runner

Unity Package Manager에서 **Test Framework**의 설치·버전을 확인한다. `Window → General → Test Runner` 등 버전에 맞는 경로에서 Edit Mode 및 Play Mode 테스트를 선택·실행할 수 있다. 프로젝트마다 Package Manager의 정확한 패키지 버전을 기록한다.

- **Edit Mode Test**: Editor 환경의 테스트. 순수 규칙·유틸리티 로직에 적합.
- **Play Mode Test**: 게임 루프 및 프레임 기반 동작이 필요한 테스트에 사용. 실행 플랫폼/환경에 따라 결과가 달라질 수 있다.
- **NUnit**: Assert 등 테스트 작성에 사용하는 프레임워크.
- **Assembly Definition (`.asmdef`)**: 테스트 코드가 어느 어셈블리에 속하는지 분리·구성한다.

### 테스트 가능한 설계

데미지 로직이 `MonoBehaviour.Update`와 애니메이션·UI에 얽혀 있으면 단위 테스트가 어렵다. 계산 규칙을 별도의 C# 클래스로 추출하면 Editor에서 Unity 씬을 열지 않고도 검증할 수 있다.

```csharp
// Assets/Scripts/Combat/DamageCalculator.cs
public static class DamageCalculator
{
    public static int ApplyArmor(int damage, int armor)
    {
        if (damage < 0) damage = 0;
        if (armor < 0) armor = 0;
        return System.Math.Max(0, damage - armor);
    }
}
```

```csharp
// Assets/Tests/EditMode/DamageCalculatorTests.cs
using NUnit.Framework;

public class DamageCalculatorTests
{
    [Test]
    public void ArmorReducesDamage()
    {
        Assert.AreEqual(7, DamageCalculator.ApplyArmor(10, 3));
    }

    [Test]
    public void DamageNeverBecomesNegative()
    {
        Assert.AreEqual(0, DamageCalculator.ApplyArmor(1, 99));
    }
}
```

위 코드는 **프로젝트의 Assembly Definition 및 테스트 참조 설정을 마친 후** 사용할 수 있는 교육용 예시다. 이 테스트가 통과해도 Unity의 히트박스 판정·애니메이션 연동이 정상이라는 뜻은 아니다.

## 9.3 테스트 어셈블리 구성

Unity Test Runner에서 테스트 어셈블리 폴더를 생성하거나, `Assets/Tests/EditMode/`에 테스트용 `.asmdef`를 만든다. 일반적으로 테스트 전용 어셈블리는 Test Assemblies 관련 설정, NUnit 참조, 테스트할 코드 어셈블리에 대한 참조가 필요하다. Unity 버전과 `.asmdef` 설정 방식에 따라 GUI 경로·참조 옵션이 다를 수 있다.

**좋은 테스트 구조**

```text
Assets/
  Scripts/
    Combat/
      DamageCalculator.cs
      Combat.Runtime.asmdef      # 선택 사항
  Tests/
    EditMode/
      DamageCalculatorTests.cs
      Combat.EditModeTests.asmdef
    PlayMode/
      CombatPlayModeTests.cs
      Combat.PlayModeTests.asmdef
```

순수 C# 계산 로직부터 테스트하고, 나중에 게임오브젝트 생성·프레임 대기가 필요한 기능으로 확장하자. 모든 `MonoBehaviour`를 Mock으로 감싸려고 억지로 구조를 복잡하게 만들 필요는 없다.

## 9.4 경계값과 예외 테스트

일반적인 정상 입력만 검사하면 실제 게임 버그를 충분히 막을 수 없다.

- 체력 0, 최대치, 음수 피해량 등 경계값.
- 아이템 개수 0에서 소비, 최대 수량 초과.
- 씬 전환 직후 객체 참조 해제.
- 회피 중 연속 입력, 입력 해제, 사망 이벤트.
- 세이브 파일 누락·손상·구버전 데이터.
- 로딩 중 취소·게임 종료.

게임 로직의 수치 변경이 잦다면 고정 숫자 테스트만 많은 것보다 **불변 규칙**을 테스트하는 것이 좋다. 예를 들어 '피해 적용 후 체력이 0보다 작아지지 않는다' 같은 속성은 여러 값에 걸쳐 의미가 유지된다.

## 9.5 Play Mode 테스트의 특성

`[UnityTest]`를 사용하면 `IEnumerator`의 프레임 기반 테스트를 작성할 수 있다. 예를 들어 적이 공격 이벤트를 받은 뒤 다음 프레임에 HP가 감소하는지 검증한다.

```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine.TestTools;

public class ExamplePlayModeTests
{
    [UnityTest]
    public IEnumerator OneFramePasses()
    {
        yield return null;
        Assert.IsTrue(true);
    }
}
```

이 코드는 실행 형태를 보여주는 최소 예시다. **실제 기능을 검증하려면 공격 이벤트, 게임 오브젝트, 시간 제어 및 종료 정리**를 구현해야 한다. 물리·애니메이션 테스트는 타임스텝과 실행 환경 차이에 영향을 받을 수 있으므로 불안정한(Flaky) 테스트를 줄이는 설계가 중요하다.

## 9.6 로컬에서 명령줄로 Test Runner 실행

Unity Editor 설치 경로는 OS와 설치 버전에 따라 다르다. Windows PowerShell에서는 다음과 같은 패턴을 사용할 수 있다. `UNITY_EDITOR_PATH`와 `PROJECT_PATH`를 실제 경로로 교체한다.

```powershell
& "C:\Program Files\Unity\Hub\Editor\YOUR_VERSION\Editor\Unity.exe" `
  -batchmode -nographics -quit `
  -projectPath "C:\Work\AsterArena" `
  -runTests -testPlatform EditMode `
  -testResults "C:\Work\TestResults\editmode-results.xml" `
  -logFile "C:\Work\TestResults\editor.log"
```

- `-batchmode`: GUI 상호작용이 없는 배치 실행.
- `-nographics`: 그래픽 없는 실행에 사용 가능한 옵션이지만 **모든 테스트·렌더링 환경에서 적합하지는 않다**.
- `-quit`: 실행 종료.
- `-runTests`: 테스트 실행 지시.
- `-testPlatform EditMode`: 실행 테스트 종류 지정.
- `-testResults`: 테스트 결과 XML 저장.
- `-logFile`: 진단용 Editor 로그 경로.

**주의:** Unity Test Framework 버전에 따라 정확한 CLI 인수, 실행 플랫폼, 필요한 폴더, 라이선스 조건을 확인한다. Play Mode 테스트와 Player Build 테스트의 명령줄 옵션도 구분한다. 테스트 결과가 만들어졌는지, 실제로 **0개 테스트 실행**으로 통과한 것은 아닌지 확인해야 한다.

## 9.7 GitHub Actions와 연결하는 설계

CI를 설계할 때 가장 먼저 해야 하는 일은 'Unity 명령줄 테스트가 **로컬 컴퓨터에서** 재현되는지' 확인하는 것이다. 로컬에서 실패하는 테스트를 곧바로 CI에 올리면 라이선스·OS·캐시·코드 문제를 구별하기 어려워진다.

권장 연결 순서:

1. 테스트 어셈블리와 Edit Mode 테스트 작성.
2. 로컬 Test Runner에서 결과 확인.
3. 로컬 명령줄에서 동일 테스트 확인.
4. Runner에서 Unity Editor 설치·라이선스 활성화 설계.
5. GitHub Actions에 테스트 명령 연결.
6. XML·Editor 로그를 Artifact로 보관.
7. 실패 시 PR에 Check 결과가 표시되는지 확인.
8. 준비가 되면 Branch Ruleset에서 필수 Check로 지정.

### 개념을 보여주는 Job 예시

```yaml
# 단독 사용 불가: Workflow jobs 아래에 들어갈 작업 구조 예시
unity-tests:
  runs-on: self-hosted
  steps:
    - uses: actions/checkout@v4
      with:
        lfs: true
    - name: Run Unity tests
      shell: pwsh
      run: |
        & "${{ vars.UNITY_EDITOR_PATH }}" `
          -batchmode -quit `
          -projectPath "${{ github.workspace }}" `
          -runTests -testPlatform EditMode `
          -testResults "${{ github.workspace }}/TestResults/results.xml" `
          -logFile "${{ github.workspace }}/TestResults/editor.log"
    - name: Upload logs
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: unity-tests
        path: TestResults/
```

이것은 **Windows PowerShell이 설치되고 Unity가 활성화된, 신뢰할 수 있는 Self-hosted Runner**라는 전제의 예시다. `vars.UNITY_EDITOR_PATH`는 설정된 Repository Variable이어야 하며 경로·라이선스·폴더 존재 여부·테스트 실행 종료 코드를 검증해야 한다. 공개 PR에서 이 Runner를 실행하도록 허용하지 말자.

## 9.8 어떤 테스트를 언제 돌릴까?

| 실행 시점 | 검사 예시 | 이유 |
|---|---|---|
| 로컬 커밋 전 | 빠른 Edit Mode 테스트 | 피드백 속도 |
| PR 생성/수정 | Edit Mode + 중요 통합 테스트 | 회귀 문제 조기 발견 |
| 매일 또는 수동 | Play Mode + Unity 빌드 | 비용 큰 검사 분리 |
| 마일스톤 승인 | 실제 빌드·성능·플레이테스트 | 게임 품질 판단 |

## 9.9 실습과 확인 기준

피해 계산 클래스를 작성하고 NUnit 테스트를 세 개 이상 만든다. 하나는 의도적으로 실패시키고 Test Runner에서 오류를 확인한다. 이후 정상값으로 수정해 재실행한다. 가능하다면 로컬 명령줄로 Edit Mode 테스트를 재현하고 보고서 파일까지 확인한다.

**확인할 결과:** 자동 테스트의 범위와 게임플레이 테스트의 범위를 구분하고, CI가 실패할 때 테스트 코드·실행 환경·라이선스를 순서대로 조사할 수 있다.

**공식 자료:** [Unity Test Framework](https://docs.unity3d.com/Packages/com.unity.test-framework@latest), [Unity 명령줄 인수](https://docs.unity3d.com/Manual/EditorCommandLineArguments.html), [GitHub Actions](https://docs.github.com/en/actions)

---

## 9.10 확장: 최소 단위 테스트를 실제로 구성하기

이 책의 `examples/unity-ci/`에는 테스트 가능한 최소 C# 로직과 Unity Edit Mode 테스트 예시를 제공한다. 본문에서 설명하는 테스트 코드는 **Unity 프로젝트의 올바른 위치에 가져와야 실제로 실행**되며, 프로젝트의 Unity·Test Framework 버전에 따라 Assembly Definition과 패키지 설정을 조정해야 한다.

### 먼저 코드와 엔진 의존성을 분리한다

'체력이 0 미만으로 떨어지지 않아야 한다' 같은 순수 규칙은 Unity Scene이나 MonoBehaviour 없이 작성할 수 있다.

```csharp
public static class HealthMath
{
    public static int AfterDamage(int current, int damage)
    {
        if (damage < 0) throw new System.ArgumentOutOfRangeException(nameof(damage));
        return System.Math.Max(0, current - damage);
    }
}
```

```csharp
using NUnit.Framework;

public class HealthMathTests
{
    [Test]
    public void DamageNeverProducesNegativeHealth()
    {
        Assert.AreEqual(0, HealthMath.AfterDamage(3, 10));
    }

    [Test]
    public void NegativeDamageIsRejected()
    {
        Assert.Throws<System.ArgumentOutOfRangeException>(
            () => HealthMath.AfterDamage(5, -1));
    }
}
```

실제 Unity 프로젝트에서는 테스트 폴더를 별도 테스트 Assembly Definition으로 구성하고 NUnit을 테스트 참조로 사용할 수 있도록 설정해야 한다. [Unity Test Framework](https://docs.unity3d.com/Packages/com.unity.test-framework@latest) 문서를 확인하자.

### 프로젝트 통합 순서

1. Unity Package Manager에서 Test Framework가 설치되어 있는지 확인한다.
2. Edit Mode용 테스트 Assembly Definition을 만든다.
3. 실제 로직이 Assembly Definition으로 분리되어 있다면 테스트 어셈블리에서 참조한다.
4. Test Runner에서 테스트를 수동 실행한다.
5. 정상 테스트뿐 아니라 **일부러 실패시키는 테스트**로 실패가 표시되는지 확인한다.
6. 로컬 명령줄 테스트를 실행해 결과 XML 파일을 얻는다.
7. 동일한 명령을 CI Runner에서 실행하도록 구성한다.

## 9.11 명령줄 테스트와 실패 처리

### Windows PowerShell 예시

```powershell
$Unity = 'C:\Program Files\Unity\Hub\Editor\YOUR_VERSION\Editor\Unity.exe'
$Project = 'C:\Work\AsterArena'
& $Unity -batchmode -nographics -quit `
  -projectPath $Project -runTests -testPlatform editmode `
  -testResults "$Project\test-results\editmode.xml" `
  -logFile "$Project\test-results\editor.log"
```

`YOUR_VERSION`은 설치된 정확한 Unity Editor 버전으로 교체한다. `-nographics`는 테스트 환경에 따라 적합하지 않을 수 있으므로 Play Mode나 렌더링 의존 테스트에서는 사용 여부를 별도로 확인한다. 실행 전 결과 저장 폴더를 준비하고 종료 코드·로그·테스트 XML을 함께 확인해야 한다.

**중요:** Unity Editor 실행 명령이 실패하더라도 항상 보기 좋은 XML이 생성되는 것은 아니다. 로그에 라이선스 오류·패키지 컴파일 실패·테스트 어셈블리 인식 오류가 기록될 수 있다. CI에서는 XML 파일이 존재한다는 사실뿐 아니라 **Unity 프로세스 종료 코드와 테스트 결과**를 함께 확인한다.

## 9.12 자동 테스트와 게임 플레이 QA의 경계

| 자동화가 잘 맞는 것 | 실제 플레이 검증이 필요한 것 |
|---|---|
| 피해·체력·보상 등 규칙 계산 | 타격감, 카메라 멀미, 플레이 템포 |
| 저장 데이터 직렬화·역직렬화 | 튜토리얼의 이해도와 몰입도 |
| 일정한 입력 조건의 상태 전이 | 적 행동이 공정하게 느껴지는가 |
| 알려진 버그의 재현 테스트 | 난이도와 보상의 재미 |

인디 팀이라면 **반복해서 실패하는 규칙부터 테스트**를 추가하는 방식이 좋아. 모든 MonoBehaviour에 테스트를 붙이는 데 시간을 쓰다가 실제 게임 개발이 중단되면 목적이 뒤바뀐 거야.

### Unity 테스트의 CI 도입 게이트

- 로컬에서 반복 실행해도 같은 결과가 나오는가?
- 특정 개발자 PC의 절대 경로에 의존하지 않는가?
- 테스트용 씬과 에셋이 저장소에 포함되어 있는가?
- 실패한 원인을 로그와 결과 파일로 찾을 수 있는가?
- 자동 테스트가 통과해도 별도로 수동 검증해야 하는 부분을 알고 있는가?

**추가 실습:** 예시 HealthMath 코드를 프로젝트에 넣고 Edit Mode 테스트 2건을 통과시킨 후, 고의로 로직을 바꿔 실패를 재현한다. 이 과정을 PR 검사로 옮기기 전에 먼저 개발자 컴퓨터에서 명령줄 실행이 안정적으로 동작하는지 확인한다.
