# 부록 A. 자주 발생하는 문제와 해결 순서

이 장은 증상에서 바로 원인을 추정하지 않고, **확인할 사실 → 조사 명령·위치 → 안전한 대응** 순서로 구성했다.

## Git과 GitHub

| 증상 | 먼저 확인할 것 | 대응 원칙 |
|---|---|---|
| Commit은 했는데 GitHub에 없음 | `git status -sb`, `git remote -v`, `git log` | Push했는지 확인 |
| `remote origin already exists` | `git remote -v` | 중복 추가 대신 `set-url` 검토 |
| `non-fast-forward` Push 거절 | 원격 커밋 존재 여부 | Fetch 후 이력 비교, 무작정 force 금지 |
| Pull 시 충돌 | `git status`, 충돌 파일 | 양쪽 의도 확인 후 병합 |
| 잘못된 파일을 스테이징 | `git diff --staged` | `git restore --staged 파일` |
| 커밋한 파일을 되돌리고 싶음 | Push 여부, 협업 여부 | 공유 이력이면 `git revert` 우선 |
| GitHub 권한 없음 | 계정, 저장소 권한, 토큰 | 최소 권한으로 인증 재확인 |
| 큰 파일 Push 거절 | 파일 용량과 기존 이력 | LFS 정책 검토, 필요 시 별도 마이그레이션 |

## Unity 프로젝트

### Clone 후 Unity가 프로젝트를 열지 못함

1. 저장소 루트에 `Assets`, `Packages`, `ProjectSettings`가 있는지 확인한다.
2. `ProjectSettings/ProjectVersion.txt`의 Editor 버전이 실제 설치 버전과 일치하는지 확인한다.
3. Git LFS 사용 프로젝트인지 확인하고 `git lfs ls-files`와 원본 파일 다운로드 상태를 점검한다.
4. Package Manager 오류 및 사설 레지스트리 인증을 확인한다.
5. Unity Editor 로그를 읽고, **테스트 사본**에서만 캐시 초기화 등을 수행한다.

### Missing Script / Missing Material

- `.meta`가 삭제되거나 GUID가 변경되었는지 `git diff`로 확인한다.
- 에셋이 `Assets` 밖으로 옮겨졌는지 확인한다.
- 스크립트의 컴파일 에러·네임스페이스·어셈블리 참조를 검사한다.
- Package Manager에 필요한 패키지가 복원되었는지 확인한다.
- 씬/프리팹 병합 시 의도치 않게 참조가 제거되었는지 살펴본다.

### 씬 Merge 후 게임 오브젝트가 사라짐

1. 해당 파일의 양쪽 커밋과 병합 전 상태를 확인한다.
2. 가능하다면 UnityYAMLMerge를 활용한다.
3. Unity Editor에서 씬을 다시 열고 문제 오브젝트와 컴포넌트를 점검한다.
4. 복구 가능한 커밋 또는 저장된 작업 사본을 이용해 손상된 참조를 재구성한다.
5. 단일 씬 동시 수정을 줄이는 구조 개선 작업을 기록한다.

## Git LFS

### Pointer 내용이 실제 파일처럼 열림

`git lfs version`, `git lfs ls-files`, `git lfs fetch`, `git lfs checkout`을 확인한다. 호스팅 스토리지 권한·요금·전송 한도도 점검한다. LFS가 비활성화된 환경에서는 실제 바이너리 대신 포인터 텍스트만 받을 수 있다.

### 기존 큰 파일이 Git 이력에 남아 있음

`git lfs track`은 기존 전체 이력을 자동 변경하지 않는다. 대형 이력 정리나 `git lfs migrate`는 원격·팀원 클론에 영향을 주므로 원본 백업, 중단 시간, Force Push 여부를 계획한 뒤 수행한다.

## Issues와 Projects

### Issue가 Projects에 보이지 않음

1. Issue가 Project에 추가되어 있는지 확인한다.
2. Auto-add Workflow의 저장소·필터·활성 상태를 확인한다.
3. 현재 View 필터(`assignee`, `iteration`, `status`)가 해당 Issue를 숨기고 있지 않은지 확인한다.
4. 사용자와 Project의 접근 권한을 확인한다.

### Issue가 닫혔는데 QA는 아직 끝나지 않음

프로젝트 기본 워크플로가 Done으로 변경했을 수 있다. **코드 완료와 게임플레이 검증 완료를 분리**하는 정책을 도입하거나, Issue의 자동 닫기 키워드 사용을 조정한다.

### 팀원에게 아무 작업도 보이지 않음

`assignee:@me` 필터에 해당하는 Issue가 존재하는지, 실제 할당이 되었는지, 다른 프로젝트에서 생성되지는 않았는지, 저장소 읽기 권한이 있는지 확인한다.

## Actions

### Actions 탭에서 수동 실행 버튼이 안 보임

- 파일이 `.github/workflows/` 안의 YAML인지 확인한다.
- `workflow_dispatch`가 선언되어 있는지 확인한다.
- 일반적으로 기본 브랜치에서 해당 워크플로가 인식되어야 한다는 조건과 사용자 권한을 확인한다.
- YAML 문법을 검사한다.

### Job이 대기(Queued) 상태임

Runner 레이블과 실제 연결된 Runner, 동시 실행 한도, 조직 정책을 확인한다. Self-hosted Runner가 꺼져 있거나 `runs-on` 레이블이 일치하지 않으면 시작되지 않을 수 있다.

### Workflow는 성공했는데 게임 빌드 파일이 없음

테스트만 수행한 것은 아닌지, 빌드 출력 경로가 다른지, Artifact `path`가 실제 파일을 가리키는지 확인한다. 빈 Artifact 업로드를 성공으로 처리하지 않도록 `if-no-files-found: error` 등을 적용한다.

### Unity CI에서 에디터 실행 실패

정확한 Unity 버전, 플랫폼 모듈, 유효한 라이선스 활성화, OS, Editor 경로, 권한을 확인한다. 테스트 실패와 에디터 실행 실패를 분리해서 로그를 수집한다.

### GitHub Pages가 게시되지 않음

`Settings → Pages → Source: GitHub Actions`를 확인한다. Actions 실행에서 MkDocs 빌드 실패와 `deploy-pages` 권한·환경 오류를 구분하고, `mkdocs.yml`의 `site_url` 및 경로 설정을 확인한다. 공개 범위와 요금 정책도 확인한다.

## 문제 분석 기록 양식

```markdown
# 문제 제목
- 발생 위치/기능:
- 저장소/브랜치/Commit SHA:
- Unity 버전 / OS:
- 실행 또는 빌드 번호:
- 재현 절차:
- 기대 결과:
- 실제 결과:
- 에러 로그(민감 정보 제외):
- 확인한 가설과 결과:
- 수정 방법:
- 회귀 테스트 결과:
```

문제가 반복된다면 해결 후 관련 Issue를 닫기 전에 재발 방지 규칙·테스트가 추가되었는지 확인한다.

## 확장판 추가 진단

### Notifications에 아무것도 나오지 않는다

- 작업이 실제 내 GitHub 계정에 할당되었는지 확인한다.
- `@mention` 이름이 정확한지 확인한다.
- 해당 Issue/PR에 접근할 권한이 있는지 확인한다.
- 알림 설정에서 웹·이메일·모바일 수신 설정을 점검한다.
- 해당 대화의 구독/구독 해제 상태를 확인한다.

### Projects에 새 Issue가 자동으로 추가되지 않는다

- 프로젝트의 `Workflows → Auto-add`를 활성화했는지 확인한다.
- 대상 Repository와 조건 필터가 올바른지 확인한다.
- 필터에서 지정한 Label이 Issue에 있는지 확인한다.
- 자동화 적용 **이전부터 존재한 Issue**는 소급해 추가되지 않을 수 있다. 새 테스트 Issue로 검증한다.
- 플랜별 Auto-add 제한과 접근 권한을 확인한다.

### PR 체크는 통과했는데 게임에서 버그가 발생한다

- Workflow가 정말 Unity 테스트·빌드를 수행했는지 확인한다. 단순한 README 검사였을 수 있다.
- PR의 검사 대상 브랜치와 실제 병합한 소스 버전을 확인한다.
- Unity Editor 실행, Play Mode, 실제 Player 빌드에서 재현되는지 구분한다.
- 해당 문제를 버그 Issue로 기록하고, 자동 테스트로 재현 가능한 부분을 따로 작성한다.

### Actions가 Permission 오류를 낸다

- Workflow/Job의 `permissions` 범위를 점검한다.
- PR의 출처가 포크인지, 외부 사용자가 실행한 이벤트인지 확인한다.
- Organization/Repository의 Actions 정책과 토큰 설정을 확인한다.
- 원인을 모른 채 높은 권한이나 Secrets를 추가하지 않는다.

### Dependabot이 Unity 패키지 취약점을 표시하지 않는다

- Unity Package Manager나 Asset Store 패키지가 자동으로 지원된다고 가정하지 않는다.
- 공식 지원 생태계 목록을 확인한다.
- Unity 패키지 버전과 보안 공지는 별도로 검토한다.

### 단일 HTML에서는 링크가 이상하다

- `single-book.html`은 단일 파일이며 목차 이동은 문서 내부 앵커를 사용한다.
- 오프라인 장별 사이트는 `site/index.html`에서 시작해 폴더 구조를 통째로 유지해야 한다.
- MkDocs 배포는 제공된 GitHub Pages Workflow와 `mkdocs.yml`의 URL을 별도 확인한다.
