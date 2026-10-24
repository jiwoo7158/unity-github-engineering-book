# 07-B. Discussions와 Projects Status Updates: 논의와 보고의 분리

GitHub를 사용할 때 '모든 대화를 Issue로 만들면 되지 않을까?'라고 생각하기 쉽다. 그러나 아직 작업으로 확정되지 않은 논의, 이미 책임과 완료 조건이 정해진 작업, 프로젝트 전체의 현황 보고는 목적이 다르다.

## B.1 어떤 정보는 어디에 두는가?

| 목적 | 추천 위치 | 비고 |
|---|---|---|
| '전투 방식 A와 B 중 무엇을 택할까?' | Discord 회의 + 필요 시 Discussions | 선택지가 열려 있는 논의 |
| '회피 입력 시 무적 구간 구현' | Issue | 담당자와 검증 기준이 존재 |
| '이번 개발 주기의 전체 진척과 위험' | Projects Status Update | 일정, 위험, 중요한 성과 공유 |
| 'AI 코드에서 중복 로직 발견' | Issue 또는 PR 리뷰 | 구체적인 수정·검토 대상 |
| '게임 엔진 버전 선택 이유' | ADR(Repository 문서) | 시간이 지나도 남아야 할 결정 근거 |

여기서 **단일 원본(Source of Truth)**을 지켜야 한다. 같은 의사결정 결과를 Discord·Notion·Issues·Discussions 네 곳에서 각각 별도로 관리하면 서로 다른 버전이 생긴다.

## B.2 GitHub Discussions란?

Discussions는 저장소나 조직에서 질문·아이디어·토론 등을 다루는 기능이다. 저장소 설정에 따라 Discussions를 활성화할 수 있다. 카테고리의 성격을 `General`, `Ideas`, `Q&A`, `Announcements`, `Polls` 등으로 구분해서 운영할 수 있다.

**생성 절차 예시**

1. 저장소 `Settings → General → Features`에서 Discussions 사용 여부를 확인한다.
2. 저장소의 `Discussions` 탭에서 카테고리를 살펴본다.
3. 필요하면 `Ideas`와 `Questions` 정도로 최소한의 카테고리를 구성한다.
4. 논의에 배경, 대안, 결정해야 할 질문, 종료 조건을 명확히 작성한다.
5. 결론이 난 뒤 구현이 필요하면 **새 Issue를 만들고 Discussion에서 링크**한다.
6. 최종 결정이 중요한 설계 원칙에 관한 것이면 ADR에 이유를 남긴다.

!!! tip "Discussions를 반드시 도입할 필요는 없다"
    팀원들이 이미 Discord에 익숙하고 개발 기록은 Issues로 충분하다면 Discussions는 생략해도 좋다. 두 공간을 동시에 운영해서 오히려 논의가 분산된다면 이득이 없다.

### 토론 예시

**제목**: `기본 공격은 콤보형인가, 단발 집중형인가?`

- 결정할 질문: 첫 프로토타입에서 어떤 공격 조작을 사용할 것인가?
- 후보: 단발 공격 / 3연타 콤보
- 평가 기준: 구현량, 조작감 검증 가능성, 팀의 애니메이션 제작 능력
- 관련 자료: 짧은 플레이 영상, 현재 기획 요약
- 결정권자 및 기한: 전투 담당자와 게임 디렉터가 다음 리뷰 전에 결정
- 결정 후 행동: 구현 Issue로 전환, 진행할 수 없는 안건은 이유와 함께 종료

## B.3 Projects Status Updates는 작업 Status와 다르다

Projects의 **개별 작업 `Status` 필드**는 각 Issue가 `In Progress`, `Review`, `Done` 어디에 있는지를 표시한다. 반면 **Project Status Update**는 프로젝트 자체가 `On track`, `At risk` 등 어떤 상태인지를 설명하는 **고수준 보고**다.

GitHub 공식 문서에서 Projects의 상태 업데이트는 프로젝트의 시작 날짜·목표 날짜·현재 상태·Markdown 메시지 등을 포함할 수 있으며, 프로젝트 패널에서 과거 기록을 확인할 수 있다고 설명한다.

**상태 업데이트 작성 절차**

1. Projects를 연다.
2. 프로젝트의 오른쪽 상단에서 사이드 패널을 연다.
3. `Status updates` 옆의 `Add update`를 선택한다.
4. 전체 상태와 필요한 날짜 정보를 정한다.
5. 이번 주 완료된 실제 결과물, 가장 큰 위험, 다음 결정 내용을 짧게 작성한다.
6. 저장하고 팀원에게 프로젝트 링크를 공유한다.

프로젝트에 쓰기 권한이 있으면 업데이트할 수 있고, 읽기 권한으로도 보거나 구독할 수 있다. 프로젝트 템플릿 상태에서는 제한이 있을 수 있다. [공식 상태 업데이트 문서](https://docs.github.com/en/issues/planning-and-tracking-with-projects/sharing-project-updates)를 참조한다.

### 3분 안에 읽히는 보고 예시

```markdown
상태: At risk
기간: 이번 주

완료된 결과물:
- Windows 개발 빌드 0.3.4
- 이동 / 회피 / 피격 연결 검증

주요 위험:
- 적 AI 담당 작업이 플레이어 감지 규칙을 기다리는 중

필요한 결정:
- 이번 주 보스 추가를 보류하고 일반 적 1종 통합을 우선할지 결정

다음 확인 시점:
- 금요일 통합 플레이 리뷰
```

이 방식은 모든 팀원이 매번 길게 개발 보고서를 다시 쓰는 것보다 부담이 적다. 다만 상태 업데이트가 **Issue별 실제 검증**을 대체하지는 않는다.

## B.4 실제 회의에서 어떻게 연결하나?

회의 전에 팀장이 미완료 Issue·차단 항목·최근 빌드를 확인한다. 회의 중에는 **하나의 Project 화면을 공유**하고 새로 생긴 논의와 결정할 항목만 다룬다. 회의 이후에는 결정이 반영된 Issue를 생성/수정한다.

1. 회의 시작 5분: 이번 주 실제 빌드를 실행하고 공동 목표 재확인.
2. 10분: `Blocked`와 `Review` 작업부터 확인.
3. 10분: 필요한 설계·우선순위 결정.
4. 5분: 담당자, 다음 행동, 검증 기준 확인.
5. 회의 종료 후: 프로젝트 상태 업데이트를 남기고 관련 Issue 링크 첨부.

### 꼭 피해야 할 것

- 회의 전에 준비하지 않은 팀원에게 즉석에서 장시간 자료 조사를 요구하기.
- 토론이 끝났는데 담당자와 완료 조건이 없는 상태로 회의를 종료하기.
- 프로젝트 상태를 단순히 완료 Issue 개수로만 `On track` 판정하기.
- Discord 메시지를 공식 결론이라고 가정하면서 GitHub에는 전혀 남기지 않기.

## B.5 실습

토론 주제 하나를 정해서 Discussion 또는 Discord에서 후보를 비교하고, 결과가 정해지면 구현 Issue 두 개를 등록한다. 그다음 프로젝트 전체 상태 업데이트를 한 건 작성한다. 팀원에게 **'무엇을 결정했는지', '내 할 일은 어디에 있는지', '프로젝트는 왜 위험 상태인지'** 설명해 보라고 한다.

**공식 자료**: [Discussions 개요](https://docs.github.com/en/discussions) · [Discussions 카테고리](https://docs.github.com/en/discussions/managing-discussions-for-your-community/managing-categories-for-discussions) · [Projects 상태 보고](https://docs.github.com/en/issues/planning-and-tracking-with-projects/sharing-project-updates)
