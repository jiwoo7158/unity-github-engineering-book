# 11. 문서, 릴리스 기록, 보안 및 저장소 운영

## 11.1 문서가 필요한 이유

소규모 게임팀은 프로그래밍보다 팀원의 기억과 채팅 메시지에 지식이 의존하는 경우가 많다. 문서는 글을 많이 쓰기 위한 산출물이 아니라 **지금 참여하지 않은 사람이 스스로 작업할 수 있도록 맥락을 보존하는 수단**이다.

모든 사항을 길게 설명할 필요는 없다. 다만 '게임 방향', '빌드 방법', '작업 완료 기준', '아키텍처와 변경 금지 규칙'이 Discord 대화에만 남으면 팀원이 교체되거나 시간이 지나면서 잊힌다.

## 11.2 문서의 원본(Source of Truth)을 정하기

Notion, Google Docs, GitHub Repository를 모두 사용할 수 있다. 문제는 도구의 개수가 아니라 **동일한 결정이 서로 다른 버전으로 여러 곳에 저장되는 것**이다.

| 문서·정보 | 권장 주 위치 | 이유 |
|---|---|---|
| 장기 기획·레퍼런스·회의 노트 | Notion 또는 Docs | 협업 편집과 시각적 표현 |
| 기술 설계와 코딩 규칙 | Repository `docs/` | 코드 변경과 함께 리뷰 가능 |
| 개발 작업·버그·완료 기준 | GitHub Issues | 담당·상태·PR 연결 |
| 일정·우선순위·전체 현황 | GitHub Projects | 보기·필드·필터 제공 |
| 테스트·빌드 결과 | GitHub Actions | 실행 로그·Check·Artifact 연결 |
| 공식적인 결정 | ADR/결정 기록 문서 | 이유와 대안 보존 |
| 개발 대화·회의 | Discord | 즉시 소통, 확정 사항은 기록으로 이동 |

이 배치는 예시이며 팀에 따라 조정 가능하다. **한 정보를 두 곳에서 수동 수정해야 하는 설계는 피한다.** 필요한 곳에는 원본 링크를 걸자.

## 11.3 Repository 문서의 추천 구조

```text
AsterArena/
├─ Assets/
├─ Packages/
├─ ProjectSettings/
├─ docs/
│  ├─ game-pillars.md
│  ├─ architecture.md
│  ├─ save-system.md
│  ├─ testing.md
│  ├─ asset-pipeline.md
│  ├─ build-and-release.md
│  └─ decisions/
│     └─ 0001-use-git-lfs.md
├─ README.md
├─ CONTRIBUTING.md
└─ .github/
   ├─ CODEOWNERS
   ├─ pull_request_template.md
   ├─ ISSUE_TEMPLATE/
   └─ workflows/
```

이 폴더는 모두 필수가 아니다. 처음에는 `README`, `CONTRIBUTING`, `architecture`, `testing` 정도만 존재해도 괜찮다. 문서가 코드와 연결되어 있어야 하는 이유는 **구현이 바뀌었을 때 같은 PR에서 문서를 함께 수정하도록 유도**할 수 있기 때문이다.

## 11.4 README에 반드시 담을 것

- 게임 소개와 현재 개발 상태.
- 정확한 Unity Editor 버전 및 설치할 플랫폼 모듈.
- Clone 방법 및 Git LFS 요구 여부.
- 프로젝트를 열고 실행하는 순서.
- 사용 중인 주요 패키지·외부 서비스.
- 문제 발생 시 연락할 위치와 Issue 템플릿.
- 개발 규칙·기획 원본 링크.
- 빌드 및 테스트 명령의 위치.

README의 품질을 검사하는 좋은 방법은 **프로젝트를 한 번도 열어보지 않은 팀원에게 복제와 실행을 맡겨보는 것**이다. 막히는 지점이 있으면 문서를 보완한다.

## 11.5 CONTRIBUTING와 Pull Request Template

`CONTRIBUTING.md`에는 브랜치 명명, PR 작성, 코드 포맷팅, 테스트, 리뷰 요청, 씬 충돌 예방 규칙 등을 정리한다. `pull_request_template.md`에는 변경 목적·검증 여부·관련 Issue·Unity 버전 변경 여부 등의 질문을 넣어 리뷰의 누락을 줄인다.

```markdown
## 관련 Issue
Refs #

## 변경 목적

## 영향 범위
- [ ] 게임플레이
- [ ] 씬 / 프리팹
- [ ] 저장 데이터
- [ ] 패키지 / Unity 설정

## 확인 결과
- [ ] Unity 에디터 컴파일
- [ ] 자동 테스트
- [ ] 실제 게임 플레이
- [ ] 문서 갱신
```

템플릿 체크박스가 체크되었다고 자동으로 검증된 것은 아니다. **검증된 빌드/Commit과 검사 방법**을 함께 적는 규칙이 더 효과적이다.

## 11.6 ADR: 기술적 의사결정 기록

**Architecture Decision Record**는 왜 그런 선택을 했는지 기록하는 짧은 문서다. 예를 들어 'ScriptableObject 기반 아이템 데이터'를 선택했다면 결정 배경과 대안을 적어두면 나중에 AI나 새 팀원이 같은 논쟁을 반복하지 않는다.

```markdown
# ADR-0001 Git LFS 도입
- 상태: Accepted
- 날짜: YYYY-MM-DD
- 맥락: FBX와 PSD로 Git 저장소 크기가 빠르게 증가한다.
- 결정: 지정 확장자를 Git LFS로 관리한다.
- 대안: Git 일반 추적, 별도 파일 서버, UVCS 유지.
- 영향: LFS 비용 모니터링과 팀원 설치가 필요하다.
- 재검토 조건: 용량·전송량이 허용 예산을 넘을 때.
```

중요한 선택만 남기면 된다. 변수 이름을 바꿀 때마다 ADR을 작성할 필요는 없다.

## 11.7 버전과 Release Notes

게임 버전은 플레이어가 실행 파일을 구분하기 위한 정보이며 Git Tag는 특정 소스 커밋을 가리킨다. **배포 파일 → 빌드 실행 → 소스 커밋**으로 되돌아갈 수 있어야 문제를 해결하기 쉽다.

예시:

```text
v0.1.0-alpha.1  핵심 이동과 공격
v0.2.0-beta.1   테스트용 전투 구역
v1.0.0          첫 정식 출시
v1.0.1          저장 오류 수정
```

SemVer 표기 자체를 그대로 게임에 적용할 의무는 없다. 팀에서 버전 변경 의미와 호환성 기준을 정의하는 것이 우선이다. Release Notes는 새 기능·수정·알려진 문제·세이브 호환 여부를 요약한다.

## 11.8 라이선스와 게임 에셋 권리

게임 저장소에는 코드 라이선스 외에도 개별 모델·텍스처·음원·폰트·플러그인 등 서로 다른 이용 조건이 존재한다.

- 외부 에셋의 사용 권한이 팀 내 공유와 재배포를 허용하는가?
- 유료 에셋을 Public Repository에 포함할 수 있는가?
- 오픈소스 라이선스의 저작권·고지·배포 의무가 있는가?
- 게임 최종 빌드에 포함된 라이브러리의 이용 조건은 무엇인가?
- 퇴사/졸업/팀원 교체 후에도 해당 에셋을 사용할 권한이 유지되는가?

GitHub Repository에 `LICENSE` 파일을 둔다고 **서드파티 에셋의 라이선스가 자동으로 변경되지는 않는다**. 의심스럽다면 사용 조건을 확인하고 배포 전 전문가 검토를 받는다.

## 11.9 보안 운영과 Secret 유출 대응

게임 저장소에서도 API 토큰, 배포 인증키, Discord Webhook, 빌드 서버 계정 정보가 유출될 수 있다.

**예방**: GitHub Secrets 사용, 최소 권한, 토큰 만료·갱신, 접근 가능한 팀원 제한, PR의 외부 코드 실행 주의, GitHub의 Secret Scanning/보안 기능 지원 범위 확인.

**유출 후 대응**: 비밀을 즉시 폐기·회전하고 영향 범위를 확인한다. 파일을 단순히 새 커밋에서 지우더라도 이전 Git 이력·캐시·로그·포크에 남아 있을 수 있다. 필요할 경우 이력 정리와 플랫폼 지원 절차를 검토하고 재발 방지 규칙을 추가한다.

## 11.10 백업과 접근 권한

GitHub 원격 저장소는 협업과 이력 보관에 유용하지만 **모든 데이터의 영구 백업 계약은 아니다**. Private 저장소 삭제, 인증 상실, LFS 누락, 프로젝트 설정 문제 등을 대비한다.

- 중요 마일스톤에 Git Tag·Release 생성.
- Repository의 백업/미러링 계획 수립.
- LFS 파일 포함 여부와 복구 가능성 확인.
- Actions Secret 값은 Git Clone으로 복제되지 않는다는 점 주의.
- Projects/Issues와 외부 Notion 데이터의 보관·내보내기 정책 확인.
- 조직 관리자/소유자 계정의 인수인계 절차 준비.

## 11.11 실습과 확인 기준

새 팀원용 README를 작성하고 다른 컴퓨터·폴더에서 읽으며 Clone과 Unity 실행을 시도한다. 기획 변경이 아닌 기술적 의사결정 하나를 ADR로 기록한다. PR 템플릿을 적용해 검증 항목이 누락되었을 때 무엇이 표시되는지 확인한다. 릴리스 초안을 작성하되 비밀·유료 에셋이 노출되는지 점검한다.

**확인할 결과:** 주요 지식의 원본 위치가 분명하며 팀원이 바뀌어도 프로젝트를 이해·설치·기여·검증할 수 있다.

**공식 자료:** [Repository 문서](https://docs.github.com/en/repositories), [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), [Releases](https://docs.github.com/en/repositories/releasing-projects-on-github), [보안](https://docs.github.com/en/code-security)

---

## 11.12 확장: Repository 안의 문서는 무엇을 원본으로 할까?

Notion과 GitHub 문서를 모두 사용하는 경우 **같은 내용을 두 곳에서 독립적으로 수정하지 않는 원칙**을 정하자.

| 자료 | 권장 원본 | 왜 여기에 두는가? |
|---|---|---|
| 게임 세계관·레벨 콘셉트·아이디어 | Notion 또는 기존 기획 도구 | 비개발 직군도 읽기 쉬움 |
| Issue별 요구사항과 완료 조건 | GitHub Issues | 담당·진행·PR 연결이 쉬움 |
| 핵심 코드 구조·기술 의사결정 | `docs/` 및 ADR | 코드 버전과 같이 검토 가능 |
| AI 개발 지침 | Repository의 `AGENTS.md` 등 | 팀원의 AI에 가능한 공통 맥락 제공 |
| 회의 중 빠른 대화 | Discord | 비동기·실시간 질문에 적합 |
| 최종 기획/기술 결정 | 지정된 원본에 기록 + Issue 링크 | 중복 기록 방지 |

이 기준은 팀의 실제 작성 습관에 따라 바뀔 수 있다. Notion을 이미 잘 쓰고 있다면 무조건 모든 문서를 Markdown으로 옮길 필요는 없다.

## 11.13 CODEOWNERS를 사용할 때의 주의

저장소의 `.github/CODEOWNERS` 등 지원 위치에 담당 경로를 작성해 관련 PR 리뷰어를 자동 요청할 수 있다. 하지만 **CODEOWNERS에 등록되었다고 그 사람이 모든 변경에 대해 자동으로 법적·실무적 책임을 지는 것은 아니다**.

```text
# 예시: 실제 GitHub 사용자명 또는 조직 팀명으로 변경
/Assets/Game/Gameplay/Combat/  @YOUR_ORG/combat-team
/Assets/Game/UI/               @YOUR_ORG/ui-team
/Packages/                     @YOUR_ORG/tech-leads
```

패턴은 저장소 루트 기준이며 코드 소유자에게 필요한 접근 권한이 있어야 한다. Organization 팀 명칭과 저장소 권한이 맞는지 테스트 PR로 확인한다.

## 11.14 배포 정보와 백업 정보는 다르다

GitHub Releases는 버전별 배포 파일과 변경 내역을 관리하는 데 유용하다. 그러나 GitHub에 배포 파일이 있다고 해서 개인 PC에 남아 있는 원본 PSD·Blender 데이터, Unity 외부 저장 데이터, 스토어 대시보드 설정까지 안전하게 백업된 것은 아니다.

팀 운영에는 최소한 다음 확인이 필요하다.

- 저장소와 Git LFS 파일을 다른 PC에서 Clone할 수 있다.
- 빌드 파일과 원본 프로젝트의 보존 위치를 구분한다.
- GitHub Actions Secrets처럼 웹에서 복원하기 어려운 운영 정보의 담당자를 정한다.
- 최종 게임의 라이선스와 외부 에셋 사용권을 확인한다.
- 장기 부재 또는 졸업 시 누가 Organization·스토어 계정을 관리하는지 정한다.

**확인할 결과:** 새 팀원이 README의 복원 절차만 보고 개발용 Unity 프로젝트를 열 수 있고, 팀장이 자리를 비워도 저장소·빌드·기본 운영 설정의 인수인계가 가능하다.
