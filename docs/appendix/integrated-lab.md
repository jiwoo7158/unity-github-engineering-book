# 부록: Unity 게임 개발 GitHub 종합 실습

> **실습 목적**: 팀장 1명, 개발자 1~2명과 함께 **기획 → Issue → Projects → 브랜치 → PR → Actions → Unity QA → 릴리스** 전체 흐름을 작은 게임 기능 하나로 검증한다. 실제 게임 출시가 아니라 GitHub 기능과 소프트웨어공학 절차를 이해하기 위한 연습이다.

이 실습을 진행하기 전에 적어도 Git 기본 사용법, Unity 프로젝트 Clone, 저장소 권한 설정을 익혔다고 가정한다. Unity Actions 빌드는 라이선스·Runner가 준비되지 않아도 종합 실습의 나머지 부분을 완료할 수 있다.

## L.1 준비물과 역할

| 준비물 | 내용 |
|---|---|
| GitHub 계정 | 팀장과 개발자, 또는 개인 실습 계정 1개 |
| 저장소 | `aster-arena-practice` 같은 비공개 테스트 저장소 |
| Unity 프로젝트 | 이동 가능한 캐릭터 또는 빈 3D 씬으로 시작해도 됨 |
| 로컬 Git | CLI 또는 GitHub Desktop |
| GitHub Issues와 Projects | 저장소 기능과 접근 권한 |
| 자동화 | README 존재 검사 예제 (Unity 빌드가 아님) |
| 통합 검증 | Play Mode에서 특정 동작 확인 |

**역할 A(관리·검토)**: 요구사항 확정, Issue·Projects 생성, PR 검토, 검증 결과 확인.

**역할 B(개발)**: Issue 읽기, 브랜치 구현, PR 제출, 검증 근거 작성.

팀장 한 명만 있다고 해서 모든 코드를 직접 작성하는 것은 아니다. 담당자들이 자기 작업을 설명하고 상태를 갱신할 수 있어야 한다.

## L.2 새 Unity 프로젝트를 GitHub에 올리기

1. Unity에서 작은 3D 프로젝트를 생성한다.
2. 정확한 Unity 에디터 버전을 기록한다.
3. `Assets/`, `Packages/`, `ProjectSettings/`, `.meta`가 저장소에 포함되게 하고, 캐시인 `Library/` 등은 무시한다.
4. 적절한 `.gitignore`를 적용하고 처음 커밋한다.
5. GitHub에 원격 저장소를 만든 뒤 업로드한다.
6. 다른 폴더에 Clone해서 Unity 프로젝트를 열어본다.
7. 기본 씬을 실행한다. 이 단계에서 실패하면 다음 단계로 넘어가지 않는다.

**증거**: Clone한 프로젝트를 연 뒤 Unity Console에 심각한 에러가 없는 스크린샷 또는 짧은 기록.

## L.3 실제로 수행할 작업 만들기

**가상 기능**: 버튼을 누르면 플레이어의 체력이 10 감소하되 0 아래로 내려가지 않는다.

GitHub Issue에는 다음을 적는다.

- 목적: 체력 피해 처리 규칙을 간단히 검증한다.
- 범위: 체력 계산과 Play Mode에서의 결과 표시만 포함.
- 제외: 적 AI, 애니메이션, UI 미화, 저장 기능.
- 참고: 09장의 `HealthMath` 테스트 예시.
- 완료 기준: 정상 피해, 과도한 피해, 음수 입력 처리, 에디터 동작 확인.
- 담당자: B.

작업이 크다면 `체력 계산`, `입력/표시 연결`, `QA`로 하위 작업을 나눈다. 개별 Issue가 실제 플레이 가능한 결과를 도출하는지 확인한다.

## L.4 Projects 구성하기

1. Projects를 하나 만들고 앞 단계의 Issue를 추가한다.
2. `Status` 필드를 `Todo → In Progress → Review → QA → Done`처럼 구성한다.
3. 팀원 View는 `assignee:@me`로, 관리자 View는 전체 작업이 보이도록 만든다.
4. B가 시작한 Issue의 상태를 `In Progress`로 변경한다.
5. 선행 작업 때문에 진행할 수 없다면 Issue 댓글 또는 Dependencies를 이용해 구체적인 차단 이유를 공유한다.

팀장이 테스트 Issue가 자동 등록되는지 확인하고 싶다면 Projects Workflows의 Auto-add를 설정할 수 있다. 다만 이것은 **실습 필수는 아니며**, 계정 플랜에 따라 제한이 있을 수 있다.

## L.5 브랜치와 PR

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/health-damage
# Unity에서 코드를 변경한 뒤
git add Assets/
git commit -m "feat: add simple damage calculation"
git push -u origin feature/health-damage
```

1. B가 PR을 열고 Issue를 연결한다.
2. PR 설명에 변경 파일 목록과 Unity에서 확인한 결과를 남긴다.
3. A가 PR을 열고 Diff를 읽은 뒤 추가 확인이 필요한 부분을 댓글로 남긴다.
4. B가 수정 후 다시 Push한다.
5. 코드 내용과 기본 검사가 문제없으면 병합한다.
6. Unity 프로젝트에서 실제 동작을 확인하는 QA Issue는 팀이 합의한 기준에 따라 별도로 닫는다.

## L.6 처음 실행하는 Actions는 Unity 빌드가 아니어도 된다

이 책의 `examples/github-config/.github/workflows/check-readme.yml`을 테스트 저장소에 복사한다.

- PR을 만들면 GitHub Actions의 `Check repository basics`가 실행되는가?
- 해당 Job의 로그에서 README 검사 결과를 확인할 수 있는가?
- `README.md`를 잠시 이름 변경하거나 삭제한 브랜치에서는 검사가 실패하는가?
- 복구 후 다시 성공하는가?

**이 단계의 목적은 Actions의 트리거·Job·Step·로그를 이해하는 것**이다. Unity Test Framework나 빌드를 아직 자동 실행하지 않아도 된다.

## L.7 Unity 기능 검증

- [ ] 기본 입력에서 체력 감소가 발생한다.
- [ ] 체력이 0 미만으로 떨어지지 않는다.
- [ ] 비정상 입력 처리 정책에 어긋나지 않는다.
- [ ] Unity Editor 재시작 후 프로젝트가 정상 컴파일된다.
- [ ] 병합된 `main`에서도 같은 동작을 확인했다.

위 조건이 통과하지 못했다면 Bug Issue를 만들고 빌드 버전, 재현 절차, 실제·기대 결과, 로그를 남긴다.

**핵심 구분**: Actions의 README 검사가 통과했다는 것은 **게임 테스트가 성공했다는 뜻이 아니다**. 이후 09~10장의 Unity 테스트와 빌드 단계를 별도로 적용할 수 있다.

## L.8 마일스톤과 릴리스 후보

1. 테스트용 Git Tag를 생성한다(예: `v0.1.0-practice`).
2. 해당 태그가 어떤 커밋을 가리키는지 확인한다.
3. 필요하면 GitHub Releases에 테스트 메모와 작은 빌드 산출물을 올린다.
4. Projects Status Updates에는 실제 완료한 기능과 여전히 미검증인 부분을 함께 기록한다.
5. 팀장과 팀원은 결과를 토대로 다음 주의 작업량과 절차를 조정한다.

릴리스의 게임 실행 가능 여부는 별도로 확인해야 하며, Tag를 만드는 행위만으로 출시가 완성되지는 않는다.

## L.9 자가 검증표

| 질문 | 확인 방법 |
|---|---|
| 팀원은 어디에서 자기 일을 찾는가? | Projects 개인 View를 연다 |
| 무엇을 만들지는 어디에 있는가? | Issue의 목적·범위·완료 기준 |
| 변경된 코드의 이유를 추적할 수 있는가? | PR 및 연결된 Issue |
| 코드의 기본 검사는 어디에서 보나? | Actions 또는 PR Checks |
| 실제 Unity 게임을 확인했는가? | QA 항목과 실행한 빌드 |
| 팀장 없이도 다음 작업을 찾을 수 있는가? | 담당 작업과 우선순위·의존성 |
| 일이 멈췄을 때 왜 멈췄는가? | 명확히 기록된 Blocked 사유 |

이 항목 중 대부분을 확인할 수 없다면 도구를 더 추가하기보다 현재 작업 분해·문서의 구체성·팀원의 학습 부담부터 다시 점검하자.

## L.10 결과물을 보관하는 방법

- Issue와 PR은 실제 GitHub 저장소의 링크로 보관한다.
- Unity 화면·재현 영상 등은 팀의 저장소 크기와 보안 정책에 맞게 관리한다.
- 중요한 설계 결정만 ADR로 남긴다.
- 짧은 회의 결과는 프로젝트 상태 업데이트에 필요한 수준으로 기록한다.
- API 토큰·키·라이선스 파일·개인정보는 첨부하지 않는다.

**학습 완료 기준**: 팀원이 단순히 `GitHub에 코드를 올릴 수 있다`에서 벗어나, **어떤 요구사항을 구현했으며 그 결과를 어떤 근거로 검증했는지** 하나의 연결된 흐름으로 설명할 수 있다.
