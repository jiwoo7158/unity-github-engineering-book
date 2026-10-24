# 07. GitHub Projects: 개발 현황과 진행 제어

## 7.1 Issues와 Projects의 차이

Issues는 저장소에 속하는 구체적인 작업/문제 기록이고, **Projects는 Issue와 PR 등을 모아 표·보드·로드맵 형태로 관리하는 계획 공간**이다. Project는 단일 저장소에만 묶이지 않을 수 있다. 따라서 게임 코드 저장소와 아트/문서 저장소가 별개여도 하나의 개발 계획에서 관련 작업을 볼 수 있다.

GitHub Projects는 일정 방식으로 고정된 도구가 아니다. 팀이 사용하는 프로세스에 맞춰 필드·보기·자동화를 **직접 설계**해야 한다. 'Projects를 켰다'는 사실이 곧 소프트웨어공학 계획이 만들어졌다는 뜻은 아니다.

## 7.2 팀장용과 팀원용 화면

개인 또는 조직 계정에서 Project를 생성해 적절한 저장소 Issue·PR을 추가한다. 팀원들은 같은 Project를 보되 **저장된 View**를 다르게 사용한다.

| View | 대상 | 구성 |
|---|---|---|
| `00 · 전체 현황` | 팀장 | Table, Status·Priority·Owner·Iteration |
| `01 · 내 작업` | 팀원 | `assignee:@me`로 필터, 중요순 정렬 |
| `02 · 이번 개발 주기` | 팀 전체 | `iteration:@current` 필터 |
| `03 · 리뷰 대기` | 개발자·리뷰어 | 검토 대상 PR/특정 상태 |
| `04 · 막힌 작업` | 팀장 | 차단 또는 명시된 Blocked 상태 |
| `05 · 마일스톤` | 팀장 | Roadmap 및 목표 날짜 |

**View 자체는 다른 데이터 사본이 아니다.** 동일한 Issue가 여러 View에 나타날 수 있으므로 중복 입력 부담을 줄일 수 있다.

## 7.3 Projects에서 알아야 할 구성 요소

1. **Items**: Issue, PR, Draft issue 등 Project에 포함된 항목.
2. **Fields**: Status, Priority, Estimate, Date, Iteration 등 메타데이터.
3. **Views**: Table(행), Board(칸반), Roadmap(시간축)으로 표시.
4. **Filters**: 필드·담당자·라벨·마일스톤 기준 조회.
5. **Workflows**: Issue 종료 시 Done 등 자동 상태 변경.
6. **Insights**: 사용자 지정 차트로 현재 업무의 상태와 추세 확인.

### 구체적인 필드 설계

| 필드 | 예 | 이유 |
|---|---|---|
| `Status` | Backlog / Ready / In Progress / Review / QA / Done | 진행 단계 구분 |
| `Priority` | P0 / P1 / P2 / P3 | 실제 처리 순서 |
| `Iteration` | 이번 주기 | 반복 개발 계획 |
| `Target date` | 2026-11-06 | 완료 목표 시점 |
| `Effort` | 1 / 2 / 3 / 5 | 상대적 규모 가늠 |
| `Workstream` | Code / Design / Art / QA | 직무별 보기 |
| `Stage` | Prototype / Slice / Alpha / Beta | 게임 생명주기 |

필드가 많으면 팀원이 데이터를 입력하지 않게 된다. 시작 시에는 `Status`, `Priority`, `Iteration`, `Workstream` 정도로 제한하고, 실제 도움이 되는 필드만 추가하자. `Assignee`, `Labels`, `Milestone`은 원본 Issue의 속성과 연계해서 쓰는 경우가 많다.

## 7.4 Table, Board, Roadmap의 차이

**Table**은 담당자·예상 작업량·상태를 한 번에 비교하기 좋다. 팀장에게 유리하다. **Board**는 상태별로 카드를 이동하면서 현재 해야 할 일을 파악하기 좋다. **Roadmap**은 날짜와 단계 간의 선후 관계를 개략적으로 보는 데 쓴다. 날짜가 기록되었다고 일정이 자동으로 정확해지는 것은 아니므로, 작업량·차단 관계를 함께 보자.

### Board 예시

```text
Backlog        Ready           In Progress       Review           QA              Done
보스 2페이즈   적 탐지 AI      회피 애니메이션    피해 계산 PR     회피 게임패드    기본 이동
업적 시스템    사운드 연결     전투 UI           적 공격 로직    보스 타격감     카메라 추적
```

팀원은 자신의 필터를 적용해 지금 무엇을 해야 할지만 보면 된다. 하지만 현재 작업이 막혔을 때는 **그 이유를 기록**해야 한다. 상태 필드만 추가해도 이유가 남지 않으면 팀장이 다시 메시지로 확인해야 한다.

## 7.5 필터 예시

GitHub Projects의 필터는 프로젝트 필드와 Issue/PR 메타데이터를 조합한다. 아래는 저장된 View에 쓸 수 있는 예시다.

```text
assignee:@me
assignee:@me status:"In progress"
iteration:@current
label:bug status:todo
no:assignee
no:priority
```

필터 값은 Project에 실제 등록된 **필드 이름과 옵션 이름**을 따라야 한다. 예를 들어 우리 프로젝트에 `In Progress` 옵션이 있다면 해당 표현을 사용해야 한다. 여러 필터 조합은 보통 AND로 작동하며 같은 필드의 여러 값은 특정 구문에서 OR로 해석될 수 있으므로 공식 문서와 화면 미리보기를 확인한다.

## 7.6 Milestone과 Iteration의 역할

- **Milestone**: `Prototype 완료`, `Vertical Slice 승인`, `Alpha` 등 검증 기준이 명확한 결과물 목표.
- **Iteration**: 1~2주 같은 반복 개발 주기. 이번 기간에 수행할 작업을 묶는다.
- **Target Date**: 특정 작업·단계의 예상 날짜. 불확실성에 따라 갱신한다.

게임 개발에서 **시간이 지났다는 사실만으로 다음 단계로 넘어가지는 않는다**. '회피 테스트를 통과했는가', '외부 플레이어가 기본 전투를 이해하는가' 등 마일스톤 통과 기준을 프로젝트 정의 문서에 따로 기록해야 한다.

## 7.7 자동화: 기본 제공 워크플로 먼저 사용

GitHub Projects에는 새 항목에 기본 Status를 부여하거나, Issue 종료·PR 병합 시 Done으로 변경하고, 특정 조건의 항목을 자동으로 추가/보관하는 **기본 자동화**가 있다.

1. Project를 열고 메뉴의 `Workflows` 항목을 찾는다.
2. 필요한 기본 워크플로를 선택한다.
3. 적용 이벤트·상태 값을 확인한다.
4. 작은 테스트 Issue로 실제 동작을 검증한다.
5. 자동 Done이 QA 완료의 의미와 충돌하는지 확인한다.

!!! warning "코드 병합과 게임 플레이 검증을 혼동하지 말자"
    PR이 병합되었다는 이유만으로 게임플레이 검증 단계까지 Done이 되면 팀에게 잘못된 신호를 준다. 코드 개발 Issue와 QA Issue를 분리하거나, 상태 워크플로를 프로젝트 의미에 맞게 조정하자.

## 7.8 팀장 1명이 운영할 때의 책임 분리

팀장이 **전체 작업을 계획하고 우선순위를 결정**하는 방향은 현실적이다. 하지만 모든 내용을 팀장이 작성하고 모든 결과를 승인하는 구조는 병목이 될 수 있다.

- 팀장: 마일스톤, 우선순위, 프로젝트 필드, 중요한 의존성, 위험 조정.
- 각 담당자: Issue의 구체적인 구현 방법·현재 상태·차단 사유 갱신.
- 기술 책임자: 아키텍처 영향이 큰 PR과 테스트 정책 검토.
- QA 담당(겸임 가능): 실제 빌드의 검증 결과 기록.

팀장 화면에는 `Unassigned`, `Blocked`, `Review`, `QA`를 우선 노출한다. 팀원 화면에는 `assignee:@me`와 현재 Iteration을 우선 노출한다. '업무가 안 된다'는 문제가 보이면 가장 먼저 **작업의 구체성/선행 작업/실제 가용 시간**을 확인한다.

## 7.9 Insights와 계획의 한계

Insights는 특정 필드별 개수·상태 분포 등을 시각화할 수 있다. 그러나 닫힌 Issue 수가 많다고 실제 게임 완성도가 높은 것은 아니다. '작업을 매우 작게 나누면 완료 개수가 늘어나는' 착시가 생긴다. 지표는 **마일스톤의 실제 빌드, 플레이테스트, 치명적 버그 수, 재작업 발생 이유**와 함께 봐야 한다.

## 7.10 Projects 템플릿과 재사용

Project 복사·템플릿은 보기·필드·일부 워크플로 구조를 재사용하는 데 유용하다. 다만 **게임 개발 단계별 모든 Issue와 자동화 파일이 프로젝트 복사만으로 완벽히 생성되는 것은 아니다**. 필요한 경우 Repository Template, Issue Templates, Actions, API를 조합해야 한다(12장).

## 7.11 실습과 확인 기준

Aster Arena Project를 만들고 상태·우선순위·Iteration 필드를 설정한다. 06장에서 작성한 Issue를 추가하고 `전체 현황`, `내 작업`, `이번 주기`, `QA` 보기로 저장한다. 테스트 Issue를 닫아 상태가 자동 변경되는지 확인한다. 자동 완료가 게임 검증 완료로 오해되지 않도록 운영 규칙을 문서화한다.

**확인할 결과:** 팀장이 모든 사람에게 반복해서 메시지를 보내지 않고도 중요한 문제를 찾고, 팀원은 Project에서 자신의 다음 행동을 파악한다.

**공식 자료:** [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects), [Projects 필터](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/filtering-projects), [기본 자동화](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations), [Best Practices](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)

---

## 7.12 확장 실습: 팀장과 팀원의 화면을 실제로 만들기

이 절은 개인 계정이나 Organization에서 새 Projects를 만든 뒤 하나의 게임 프로젝트를 구성하는 예시다. GitHub UI는 자주 바뀌므로 정확한 버튼 위치가 다르다면 [Projects Quickstart](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects)의 최신 순서를 확인한다.

1. GitHub의 `Projects`에서 `New project`를 선택한다.
2. 기본 Table 또는 Board 형태로 프로젝트를 만든다. 이름은 `Aster Arena · Development`로 한다.
3. 프로젝트에 게임 코드 저장소의 Issue 5건을 추가한다.
4. `Status`를 `Backlog / Ready / In Progress / Review / QA / Done`으로 맞춘다. 기본 Status 옵션은 편집 가능하다.
5. `Priority`라는 Single select 필드를 추가해 `P0 / P1 / P2 / P3`을 만든다.
6. `Iteration` 필드를 추가한다. 반복 개발 주기는 가용 시간에 맞게 1~2주로 설정한다.
7. `View`를 복제·편집해서 `00 전체`, `01 내 작업`, `02 이번 주기`, `03 리뷰·QA`를 구성한다.
8. 팀원의 `내 작업` View에는 `assignee:@me`를 적용한다. 새로 배정한 Issue가 실제로 나타나는지 확인한다.
9. 팀장은 미배정·차단 항목을 별도 필터로 확인한다. 차단 이유는 Issue의 댓글이나 Dependency 관계에 남긴다.

**주의:** Projects의 필드 `Status`와 저장소 Issue의 열린/닫힌 상태는 별도의 개념이다. Issue가 열려 있어도 Project에 `Done`으로 표시하는 등의 불일치가 가능하다. 자동화 규칙이 어떤 항목의 어느 상태를 바꾸는지 반드시 테스트한다.

## 7.13 Auto-add와 기본 워크플로 상세

GitHub Projects의 기본 워크플로는 별도의 Actions YAML을 작성하지 않아도 설정할 수 있다.

### 새로운 Issue 자동 추가

1. Project 오른쪽 상단 메뉴에서 `Workflows`를 연다.
2. `Auto-add to project`를 선택한다.
3. 저장소를 지정하고 Issue 필터(예: `is:issue label:game-task`)를 입력한다.
4. `Save and turn on workflow`로 활성화한다.
5. 조건에 맞는 **새로운 테스트 Issue**를 만든다.
6. Project에 자동 등록되었는지 확인한다.

Auto-add는 기본적으로 새로 생성하거나 업데이트되는 항목을 감지한다. **설정하기 이전부터 존재하던 모든 Issue가 소급해서 자동 추가되는 것은 아니다.** 기존 항목은 수동으로 추가하거나 별도 절차를 적용한다. 플랜에 따른 워크플로 개수 제한도 있다. [공식 자동 추가 문서](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically)

### 새 항목 상태 자동 지정

1. 같은 Workflows 메뉴에서 `Item added to project`를 선택한다.
2. 이벤트 유형과 초기 Status(`Ready` 또는 `Todo`)를 설정한다.
3. 활성화하고 새 Issue를 추가해 본다.
4. 테스트 결과가 예상과 다르면 필드 옵션 이름·사용 범위·기존 자동화를 확인한다.

### 병합과 완료 자동화의 함정

GitHub 기본 워크플로는 PR 병합 또는 Issue 종료를 감지해 상태를 Done으로 바꿀 수 있다. 이 기능을 켰을 때 **QA가 끝나지 않은 작업이 완료로 표시되는 문제**가 생긴다면 단계를 분리해야 한다.

- 구현 Issue를 병합 시 종료하고, QA는 별도 Issue로 관리.
- 하나의 Issue를 유지한다면 자동 완료 규칙을 조정하고 `QA` 상태에서 사람의 검증을 요구.

팀 규모가 작다면 첫 번째 방식이 이해하기 쉬울 수 있지만, 어떤 방식을 택하든 팀이 **Done의 의미**를 공통으로 알고 있어야 한다.

## 7.14 Insights와 진행 상황 해석

Projects의 Insights는 필드별 항목 분포나 추세를 살펴볼 때 유용하다. 하지만 게임 완성도는 '닫힌 Issue 수'와 같지 않다.

실습으로 `Insights → New chart`에서 Status별 작업 수를 살펴보고, 그 결과를 실제 Unity 통합 빌드와 비교해 보자. 예를 들어 Done이 80%라도 전투와 UI가 통합되지 않았다면 마일스톤은 아직 통과하지 못했을 수 있다.

차트 외에 반드시 확인할 정보:

- 이번 마일스톤의 **실제 실행 가능한 빌드**가 있는가?
- `Blocked` 항목이 누구의 결정을 기다리는가?
- 기능이 추가되는 속도보다 버그와 통합 문제가 빨리 늘고 있지 않은가?
- 팀원의 가용 시간 변화가 계획에 반영되었는가?

### 팀장을 위한 매주 5분 점검

1. `no:assignee` 또는 실제 프로젝트에 맞는 미배정 필터로 담당자가 없는 작업 확인.
2. 이번 Iteration에서 완료되지 않은 작업의 차단 사유 확인.
3. Review·QA 항목이 지나치게 쌓였는지 확인.
4. 프로젝트 상태 업데이트에 이번 주 빌드·위험·다음 결정을 기록(07-B장).
5. 다음 작업을 무조건 늘리기보다 지금 진행 중인 작업을 먼저 마무리하도록 우선순위 재조정.

**공식 자료:** [Projects 시작하기](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects) · [기본 자동화](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations) · [프로젝트 상태 업데이트](https://docs.github.com/en/issues/planning-and-tracking-with-projects/sharing-project-updates)
