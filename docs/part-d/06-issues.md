# 06. GitHub Issues: 요구사항·작업·버그 관리

## 6.1 Issue가 소프트웨어공학에서 중요한 이유

Issue는 '할 일'을 적어두는 메모를 넘어 **요구사항과 결과물 사이의 연결 고리**다. 기획의 '회피가 재밌어야 한다'를 개발자가 실행할 수 있는 작업으로 나누고, 담당자·완료 기준·코드 변경·테스트 결과까지 추적하는 데 사용한다.

게임 개발에서는 보통 다음 유형이 반복된다.

| 분류 | 예 | 검증 결과 |
|---|---|---|
| 기능(Feature) | 공격 콤보 | 조건·시연·테스트 |
| 버그(Bug) | 회피 중 카메라 떨림 | 재현→수정→재현 방지 |
| 작업(Task) | 적 모델 임포트 | 규격 충족·참조 정상 |
| 조사(Research/Spike) | AI FSM/BT 비교 | 비교 결과·결정 기록 |
| 기획(Design) | 보스 공격 패턴 | 기획 문서·플레이테스트 |
| QA | 세이브 회귀 검사 | 빌드 번호·체크 결과 |

GitHub의 **Issue Types**는 Organization 수준에서 기능·버그·작업 유형 등을 분류하는 지원 기능이며, Labels는 저장소 단위로 다양하게 붙일 수 있다. 기능 지원 여부와 편집 권한을 구분한다.

## 6.2 Issue 작성의 최소 기준

아무리 좋은 Projects 보드를 만들어도 작업이 `전투 시스템 구현`이라는 제목 한 줄뿐이라면 팀원은 무엇을 해야 할지 모른다. 소규모 팀에 다음 항목을 권장한다.

1. **목적**: 왜 필요한가? 어떤 플레이 경험·문제를 다루는가?
2. **범위**: 이번 작업에 포함/제외하는 것은 무엇인가?
3. **입력·결과**: 어떤 조건에서 무엇이 일어나야 하는가?
4. **담당자**: 누가 작업을 이끌고 질문을 받을 수 있는가?
5. **선행 조건**: 어떤 코드·아트·기획 결정이 먼저 필요한가?
6. **완료 기준**: 무엇을 보여주면 완료로 판단하는가?
7. **검증**: 자동 테스트·수동 플레이 중 무엇을 확인하는가?

### 기능 Issue 예시

```markdown
# [Gameplay] 플레이어 회피 입력 및 상태 전환

## 목적
적의 공격 타이밍을 읽고 회피하는 전투 경험을 만든다.

## 범위
- 입력을 받으면 현재 이동 방향으로 회피
- 회피 동안 공격 불가
- 무적 구간은 설정 데이터로 조정
- 이번 작업에서는 카메라 이펙트 제외

## 선행 조건
#17 플레이어 상태 시스템 완성

## 완료 조건
- [ ] 기본 이동/대기에서 회피 가능
- [ ] 금지 상태에서는 회피 불가
- [ ] 연타 시 상태가 꼬이지 않음
- [ ] 실제 플레이 장면에서 동작 시연
- [ ] 관련 테스트와 변경 사항 PR 연결
```

기획 값은 확정된 수치가 아니라 **테스트를 통해 변경될 수 있는 가정**일 수 있다. 그렇다면 수치 조정의 책임자와 평가 방법을 명시하자.

## 6.3 Issue 생성 화면과 주요 항목

1. 해당 Repository의 `Issues` 탭을 연다.
2. `New issue` 또는 준비된 템플릿을 선택한다.
3. 제목과 본문을 작성한다.
4. `Assignees`에 담당자를 지정한다.
5. `Labels`, `Milestone`, `Projects`를 연결한다.
6. 관련 문서와 선행 Issue 링크를 추가한다.
7. 생성 후 댓글·상태·체크리스트를 갱신한다.

**Assignee**는 한 명 이상 지정할 수 있으나 한 작업의 주 책임을 명확히 하려면 팀 내부에서 대표 담당자를 정하는 것이 좋다. **Labels**는 복수의 분류로 필터링하기에 적합하고, **Milestone**은 특정 목표 시점에 완료할 Issue 묶음을 나타내는 데 쓸 수 있다.

## 6.4 상위 Issue와 Sub-issues

기능이 크면 부모 Issue와 하위 Issue를 활용한다.

```text
Epic: 전투 시스템
├─ 플레이어 공격 입력
├─ 피해 계산
├─ 회피 상태
├─ 적 공격 패턴
└─ 전투 피드백
```

GitHub의 Sub-issues는 단순 체크박스 텍스트와 달리 정식 Issue 관계로 구성되어 Project에서 계층 구조를 살펴볼 수 있다. 하위 Issue가 많아졌다고 해서 무조건 좋은 분해는 아니다. **한 작업을 누가 어떤 결과로 종료할지 판단 가능한 크기**까지 나누자.

## 6.5 의존성(Blocking/Blocked by)

회피 기능은 플레이어 상태 시스템이 먼저 필요하고, 전투 UI는 피해 이벤트 구조가 정해진 뒤 연결할 수 있다. 이런 관계를 `Relationships`의 의존성으로 명시하면 **막힌 작업**을 구분하는 데 도움이 된다.

- `A blocked by B`: B가 끝나기 전에는 A를 진행하기 어렵다.
- `A blocking C`: A가 C의 진행을 막고 있다.

모든 작은 의존성을 입력하면 오히려 관리 비용이 커지므로, 일정이나 담당자의 다음 행동에 실질적인 영향을 주는 관계만 기록하자.

## 6.6 Issue Forms로 기록 품질 일정하게 만들기

YAML 기반 Issue Forms는 새 Issue 작성 화면에서 필수 입력, 드롭다운, 입력창을 제공한다. 다음은 `.github/ISSUE_TEMPLATE/bug_report.yml`의 **동작 가능한 기본 예시**다.

```yaml
name: Bug report
description: 게임 기능 오류를 보고합니다.
title: "[Bug] "
labels: ["bug"]
body:
  - type: textarea
    id: summary
    attributes:
      label: 문제 요약
      description: 기대한 동작과 실제 결과를 적습니다.
    validations:
      required: true
  - type: textarea
    id: reproduction
    attributes:
      label: 재현 절차
      placeholder: "1. 게임을 실행한다.\n2. ..."
    validations:
      required: true
  - type: input
    id: build
    attributes:
      label: 빌드 버전
      placeholder: "0.2.1 (commit SHA 또는 태그)"
    validations:
      required: true
  - type: dropdown
    id: severity
    attributes:
      label: 심각도
      options:
        - Blocker
        - Critical
        - Major
        - Minor
    validations:
      required: true
```

**주의:** `labels: ["bug"]`가 지정되어 있다면 저장소에 해당 레이블을 미리 만들어 두는 편이 안전하다. 입력 폼은 정보를 강제할 수 있지만, 진단에 필요한 실제 로그·영상·파일이 제출되는지는 별도의 팀 규칙과 검토가 필요하다.

## 6.7 버그 보고의 품질

버그 Issue에는 적어도 **환경, 빌드, 기대 결과, 실제 결과, 재현 단계, 재현 빈도**를 기록한다. 가능하면 Console 로그, Player 로그, 영상, 세이브 파일을 첨부한다. 플레이어 개인정보나 비밀 정보가 섞이지 않았는지 확인해야 한다.

예시:

- **제목:** `[Bug][Critical] 보스 처치 직후 회피 시 결과 화면 미표시`
- **버전:** `v0.4.12`, Commit SHA 링크
- **환경:** Windows 11 / 게임패드 사용
- **재현:** 보스 처치 직후 회피 입력 → 결과 UI 누락
- **기대:** 보스 종료 연출 후 결과 화면 표시
- **검증:** 수정 후 같은 세이브와 새 게임 모두 검사

**심각도(Severity)**는 영향의 크기, **우선순위(Priority)**는 언제 고칠지에 대한 의사결정이다. 작은 시각 버그도 출시 영상에 직접 노출된다면 우선순위가 높을 수 있다.

## 6.8 GitHub Issue와 PR을 연결하는 방법

`Fixes #123`, `Closes #123` 같은 닫기 키워드는 기본 브랜치에 반영될 때 자동 종료 조건에 활용된다. 게임 QA가 코드 병합 뒤에 남아 있다면 미리 Issue를 닫아버리지 않도록 정책을 정하자.

**권장 분리 예시**

- 개발 Issue: 코드 수정·리뷰·자동 테스트·통합 완료 시 닫는다.
- QA Issue: 테스트 빌드와 플레이 시나리오 검증 후 닫는다.
- 또는 하나의 Issue에 명확한 상태 필드와 검증 완료 기준을 정의하고, PR은 `Refs #번호`로 연결한다.

어느 운영이든 **게임 플레이 검증 없이 GitHub 상태만 Done이 되는 착시**를 막는 것이 중요하다.

## 6.9 소규모 팀의 Issue 운영 규칙

- 생성 권한은 누구나 가질 수 있지만 우선순위와 마일스톤 변경 책임자는 정한다.
- 팀장이 모든 Issue 본문을 일일이 쓰지 않는다. 담당자가 초안을 작성하고 중요한 부분만 검토하도록 위임한다.
- 팀원에게 모호한 작업이 전달되면 Issue 댓글로 요구사항을 보완한다.
- 일주일 이상 멈춘 작업은 **무책임으로 단정하지 않고**, 차단 원인·의존성·작업 크기를 먼저 확인한다.
- 긴 논의의 결과만 Issue 본문 또는 결정 문서에 요약한다. Discord 메시지만 단독 근거로 남기지 않는다.

## 6.10 실습과 확인 기준

부모 Issue `전투 프로토타입`을 만들고, `이동`, `회피`, `공격`, `적 AI`, `전투 UI`, `테스트`의 하위 Issue를 작성한다. 회피 작업이 이동 상태 시스템에 의존하도록 연결하고, 담당자·완료 기준·마일스톤을 설정한다. 버그 템플릿을 통해 재현 가능한 오류 한 건을 보고한다.

**확인할 결과:** 어느 팀원도 구두 설명만 듣고 일을 시작하지 않아도 되며, Issue를 읽고 요구사항·검증 방법·관련 맥락을 찾을 수 있다.

**공식 자료:** [GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues), [Sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues), [의존성](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies), [Issue Forms](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/configuring-issue-templates-for-your-repository)

---

## 6.11 확장 실습: 실제로 작성 가능한 Issue Forms

Issue Forms는 GitHub 저장소의 `.github/ISSUE_TEMPLATE/` 디렉터리에 YAML 파일로 만든다. 이 책에는 **복사 가능한 예제**를 `examples/github-config/.github/ISSUE_TEMPLATE/`에 함께 넣었다. GitHub가 제공하는 기본 양식 화면에서 시작해도 되고, 예제 파일을 테스트 저장소로 복사해도 된다.

### 예제: 기능 개발 요청 양식

```yaml
name: "기능 개발"
description: "새로운 게임 기능의 목적과 완료 기준을 등록합니다."
title: "[Feature] "
labels: ["feature"]
body:
  - type: textarea
    id: goal
    attributes:
      label: "플레이어 관점의 목표"
      description: "어떤 플레이 경험을 만들기 위한 기능인가요?"
    validations:
      required: true
  - type: textarea
    id: scope
    attributes:
      label: "작업 범위와 제외 범위"
      description: "이번 Issue에서 포함할 것과 하지 않을 것을 명확히 적습니다."
    validations:
      required: true
  - type: textarea
    id: done
    attributes:
      label: "완료 조건"
      value: |
        - [ ] 기능 동작 확인
        - [ ] 주요 예외 조건 확인
        - [ ] Unity 실제 빌드에서 확인
    validations:
      required: true
```

위 예제는 `feature`라는 Label이 저장소에 존재한다는 전제에 맞춰 작성되었다. 아직 라벨을 만들지 않았다면 생성하거나 `labels` 설정을 제거한다. `id`는 필드별로 고유해야 하고, YAML 들여쓰기는 공백으로 처리해야 한다. [공식 문법](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms) 참조.

**적용 절차**

1. `.github/ISSUE_TEMPLATE/feature.yml` 파일을 만든다.
2. 변경을 `main`에 반영한다. 팀 규칙에 따라 PR을 이용해도 된다.
3. 저장소 `Issues → New issue`를 연다.
4. `기능 개발` 양식을 선택한다.
5. 실제 입력 가능한지 확인하고 테스트 Issue를 만든다.
6. 필요 없는 필드가 있는지 팀원의 의견을 받아 수정한다.

### 규모가 커진 작업을 분할하는 판단 기준

처음에는 '전투 시스템 구현'처럼 크고 추상적인 작업이 필요할 수 있다. 하지만 실행 단계에서는 **1~3회의 작업 세션 안에 결과를 검증할 수 있는 하위 작업**을 기준으로 나눠보자. 개발자가 하루에 실제로 몇 시간 작업할 수 있는지에 따라 세션의 길이는 달라진다.

분할 시 다음 질문을 사용한다.

1. 이 작업은 하나의 **검증 가능한 행동**을 만들어 내는가?
2. 다른 시스템 담당자와 합의할 입력·출력은 무엇인가?
3. 다른 작업이 미완성이라도 임시 테스트나 Stub을 이용해 검증 가능한가?
4. 막혔을 때 이유를 한 문장으로 표현할 수 있는가?
5. 담당자가 진행 상황을 보여줄 수 있는 최소 단위는 무엇인가?

예를 들어 `전투 시스템` → `피해 계산 로직` → `체력 감소 테스트` → `피격 UI 연결` 같은 식으로 분리한다. 단, 단순히 체크 박스 개수를 늘리기 위해 과도하게 잘게 나눌 필요는 없다.

## 6.12 Issue · PR · QA의 상태 전이

**권장 기본 원칙**: 구현 Issue를 닫는 기준과 QA Issue를 닫는 기준은 다를 수 있다. 특히 팀이 `검증 완료`를 `Done`의 의미로 사용한다면 PR 병합 즉시 자동으로 닫히는 Issue와 충돌할 수 있다.

| 상황 | 바람직한 기록 |
|---|---|
| 구현은 시작했지만 요구사항이 불명확 | Issue에 질문, `Blocked` 표시 |
| 구현이 끝나 PR 생성 | Issue에 PR 연결, Projects `Review` |
| 자동 테스트 통과 | PR 검사 통과, 수동 QA는 별도 |
| 코드 병합 완료 | 구현 Issue 종료 가능, QA 별도 진행 |
| Unity 플레이 검증 실패 | 버그 Issue 등록 및 관련 PR/Issue 연결 |
| 플레이 검증까지 통과 | QA Issue 종료, 마일스톤 통과 근거 기록 |

### 자동 종료 키워드 주의

`Fixes #123`, `Closes #123` 같은 키워드가 기본 브랜치 병합과 결합하면 연결된 Issue가 자동 종료될 수 있다. 팀이 해당 Issue를 'QA까지 완료되어야 닫는 작업'으로 정의했다면 의도치 않은 종료가 발생할 수 있으므로 `Refs #123` 같은 단순 참조로만 연결하는 방법을 고려한다.

## 6.13 작업을 방치하지 않게 하는 질문 방식

지연된 Issue에는 '언제 끝나요?'라고만 물어보는 것보다 원인을 구체화하는 질문이 효과적이다.

- **요구사항 부족**: '최종 결과물의 모습이 무엇인지 함께 확인해야 하나요?'
- **기술적 장애**: '재현 절차·오류 로그·시도한 해결책을 남길 수 있나요?'
- **의존성**: '선행 작업이 무엇이고 누가 언제 처리해야 하나요?'
- **예상 작업량 초과**: '어느 부분까지 쪼개면 이번 주 안에 검증할 수 있나요?'
- **참여 가능 시간 변화**: '이번 주 실제 가용 시간에 맞게 범위를 줄여야 하나요?'

작업 관리의 목적은 개발자를 감시하는 것이 아니라 **상황을 조기에 가시화하고 필요한 지원과 결정을 제공하는 것**이다.

**추가 확인 과제:** 3명의 팀원이 기능·버그·조사 유형으로 최소 한 건씩 Issue를 작성하고, 서로 읽었을 때 추가 구두 설명 없이 작업을 시작할 수 있는지 시험해 보자.
