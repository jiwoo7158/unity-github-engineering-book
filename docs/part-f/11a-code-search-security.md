# 11-A. Code Search·Blame·Dependabot·보안 검사

게임 개발자는 AI가 만든 기능이 이미 존재하는지 확인해야 할 때가 많다. 또 코드 한 줄을 누가 왜 바꾸었는지 알아야 중복이나 회귀 버그를 줄일 수 있다. GitHub의 코드 탐색과 보안 기능은 이런 상황을 돕지만, **자동 코드 중복 검출기나 Unity 전용 패키지 관리자와 동일하지는 않다.**

## C.1 코드 검색: 구현 전에 기존 시스템 찾기

GitHub 웹에서 저장소를 열고 검색 창 또는 코드 검색 화면을 이용한다. 코드 검색은 저장소 범위, 경로, 언어, 심벌 등의 조건으로 탐색할 수 있다.

```text
repo:OWNER/REPO Damage
repo:OWNER/REPO path:Assets/Game/Combat
repo:OWNER/REPO language:C# ApplyDamage
```

위 표현의 `OWNER/REPO`는 실제 저장소명으로 바꾸고, 쿼리 구문과 지원 범위는 [Code Search 문서](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax)에 따라 확인한다. 파일이 색인되지 않았거나 검색 대상이 아니면 결과가 없을 수 있다. 이름을 검색해서 결과가 없다고 곧바로 '해당 기능이 없다'고 확정해서는 안 된다.

**구현 전 검색 절차**

1. Issue에서 요청한 동작의 핵심 동사와 데이터(예: Damage, Health, Attack)를 고른다.
2. 저장소에서 유사한 클래스, 인터페이스, 이벤트, ScriptableObject를 찾는다.
3. 구현하려는 기능이 기존 시스템을 재사용할 수 있는지 확인한다.
4. 기존 클래스가 있다면 새 클래스를 만들기보다 확장 또는 연결이 적절한지 검토한다.
5. PR 설명에 어떤 코드를 재사용했고 왜 새 구현이 필요한지 기록한다.

검색은 설계 검토의 입력 자료야. 동일한 이름의 코드라도 의미와 책임이 다르면 통합하는 편이 오히려 나쁠 수 있다.

## C.2 Blame: 누가 언제 변경했는가?

1. GitHub에서 파일을 연다.
2. 파일 보기의 `Blame` 버튼을 선택한다.
3. 특정 줄에 표시된 커밋과 작성자·변경 시점을 확인한다.
4. 커밋 메시지와 연결된 Pull Request/Issue를 열어 **왜 변경했는지** 조사한다.
5. 원인 파악 후 재현 가능한 테스트를 작성하거나 수정한다.

`Blame`은 마지막으로 해당 줄을 바꾼 이력을 보여주므로 **책임 추궁 도구가 아니다**. AI가 만들고 사람이 병합한 코드라면 Blame의 작성자가 설계 의도를 혼자 알고 있다는 보장도 없다. [공식 Blame 설명](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files)을 참고한다.

로컬에서도 다음 명령을 쓸 수 있다.

```bash
git log --oneline -- Assets/Game/Combat/DamageCalculator.cs
git blame Assets/Game/Combat/DamageCalculator.cs
git show COMMIT_SHA -- Assets/Game/Combat/DamageCalculator.cs
```

대규모 코드 정리나 서식 변경으로 Blame이 읽기 어려워진다면 `.git-blame-ignore-revs`를 고려할 수 있다. 단, 팀에서 기록할 커밋을 합의해야 한다.

## C.3 Compare, History, PR 검색

GitHub의 파일 `History`, 커밋 비교(Compare), PR 검색을 함께 사용하면 코드의 변화를 더 잘 이해할 수 있다.

- **History**: 파일의 과거 변경을 순서대로 볼 때.
- **Compare**: 두 브랜치 또는 커밋 사이의 차이를 확인할 때.
- **PR 검색**: 기능이 만들어진 목적·검토 의견·테스트 결과를 확인할 때.
- **Blame**: 특정 줄의 마지막 변경을 추적할 때.

예를 들어 전투 피해량이 변경되었는데 게임 밸런스가 깨졌다면 `DamageCalculator`의 History를 확인하고 관련 PR을 찾아 '버그 수정인지 밸런스 변경인지' 파악한다.

## C.4 Dependabot의 역할과 Unity에서의 한계

GitHub Dependabot은 지원되는 패키지 생태계와 매니페스트를 대상으로 취약점 알림 또는 버전 업데이트 등을 제공할 수 있다. 그러나 Unity Package Manager의 `Packages/manifest.json`이나 Asset Store 에셋이 **모두 Dependabot에서 자동 지원된다고 가정하면 안 된다.**

GitHub가 공개한 [지원 생태계 목록](https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems)에서 **Unity Package Manager는 일반적인 지원 생태계로 명시되어 있지 않다**. 별도로 사용하는 .NET/NuGet 프로젝트나 GitHub Actions 워크플로처럼 지원 매니페스트가 있는 경우는 별개다.

| 대상 | 점검할 사항 |
|---|---|
| `Packages/manifest.json` | Unity Package Manager에서 직접 버전·호환성 관리 |
| Asset Store 패키지 | 배포자 공지, 라이선스, Unity 버전 호환성 수동 확인 |
| NuGet 매니페스트가 있는 별도 도구 | 해당 생태계가 지원되면 Dependabot 검토 |
| `.github/workflows/*.yml` | Actions 의존성·버전 고정 확인 |

### Dependabot Alerts 설정과 확인

1. 저장소 `Settings`로 이동한다.
2. 보안 설정 중 `Advanced Security`의 사용 가능한 기능을 확인한다.
3. `Dependabot alerts`를 활성화하고 필요하면 관련 알림 설정을 검토한다.
4. 저장소 `Security` 영역에서 탐지된 알림을 검토한다.
5. 실제 사용하는 의존성인지, 수정 가능한 버전인지, 업데이트 후 Unity 기능에 영향이 있는지 확인한다.
6. 업데이트 후 테스트 및 빌드 결과까지 검증한다.

지원 여부와 기능별 과금/권한은 공개·비공개 저장소와 요금제에 따라 달라질 수 있다. [공식 Dependabot 안내](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-dependabot-alerts)를 기준으로 판단한다.

## C.5 Code Scanning, Secret Scanning, Push Protection

이 세 가지를 혼동하지 말자.

| 기능 | 무엇을 찾으려는가? | 제한 사항 |
|---|---|---|
| Code scanning | 코드에서 알려진 문제 패턴과 취약점 | 언어·분석기·설정에 따라 탐지 범위 차이 |
| Secret scanning | 지원하는 비밀 키·토큰 패턴 | 모든 비밀 문자열이나 사용처를 완전 탐지하지 못함 |
| Push protection | 지원 패턴의 비밀값이 푸시되는 것을 사전 차단 | 지원 패턴, 설정·정책에 따라 차이 |

Unity 프로젝트에서 특히 위험한 정보에는 스토어 업로드 인증 토큰, Discord Webhook URL, 개인 API 키, 라이선스 파일, 서버 접근 정보 등이 있어. `Secrets`에 저장한다고 Git에 이미 커밋된 비밀이 저절로 사라지지는 않는다.

**비밀 유출 시 대응 순서**

1. 유출된 토큰을 즉시 폐기 또는 교체한다(회수 가능한 경우).
2. 관련 시스템에서 권한 사용 내역과 영향 범위를 조사한다.
3. 새 키는 GitHub Secrets 또는 적절한 외부 비밀 관리 수단에 보관한다.
4. 저장소의 코드와 이력에 포함된 비밀값의 제거 필요성을 판단한다. 단, 이력 재작성은 팀 전체에 영향을 주므로 신중하게 진행한다.
5. 재발 방지 규칙과 검증을 추가한다.

**주의:** GitHub의 보안 기능은 중요한 보조 도구이지만 모든 프로젝트에 동일한 수준으로 제공되는 것은 아니야. UI에서 기능이 보이지 않으면 저장소 권한·플랜·조직 정책을 확인한다. [공식 보안 설정](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository)

## C.6 실습: AI가 만든 중복 코드 찾기

1. 테스트 저장소에 `HealthComponent`가 있다고 가정한다.
2. AI가 작성한 별도 `EnemyHPManager`에 체력 감소·사망 로직이 들어 있다고 가정한다.
3. GitHub 검색으로 `Health`, `HP`, `Damage`, `ApplyDamage`를 조회한다.
4. 두 클래스의 책임과 참조 관계를 비교한다.
5. 새 로직이 기존 시스템을 재사용해야 하는지 결론을 작성한다.
6. 중복을 제거한 PR을 제출하고 Blame/History로 이전 구현을 확인한다.
7. 변경 이전과 이후의 Unity 동작을 비교한다.

**학습 완료 기준**: '비슷한 이름의 코드가 있다'는 이유만으로 지우지 않고, 각 코드의 책임·참조·기능을 설명한 뒤 안전하게 통합할 수 있다.

**공식 자료**: [Code Search](https://docs.github.com/en/search-github/github-code-search) · [파일 보기·Blame](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files) · [Dependabot](https://docs.github.com/en/code-security) · [보안 설정](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository)
