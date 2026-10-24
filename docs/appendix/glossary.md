# 부록 B. 핵심 용어 사전

| 용어 | 뜻 | 혼동하기 쉬운 것 |
|---|---|---|
| Git | 로컬 중심 분산 버전 관리 프로그램 | GitHub 자체 |
| GitHub | 저장소 호스팅·협업 서비스 | Git 명령줄 프로그램 |
| Repository | 프로젝트 파일과 변경 이력의 단위 | Project 작업 보드 |
| Local Repository | 작업 컴퓨터의 Git 저장소 | GitHub 원격 저장소 |
| Remote Repository | GitHub 등에 위치한 저장소 | 로컬 작업 폴더 |
| Working Directory | 수정 중인 프로젝트 파일 | 스테이징된 변경 |
| Staging Area | 다음 커밋에 포함할 변경 목록 | 이미 원격 업로드한 상태 |
| Commit | 이력을 기록하는 단위 | Push |
| Push | 로컬 이력을 원격으로 보냄 | Commit |
| Fetch | 원격 이력을 가져와 갱신 | 작업 브랜치에 병합하는 Pull |
| Pull | Fetch 후 로컬과 통합 | 단순 조회 |
| Clone | 원격 저장소 복제 | ZIP 단발 다운로드 |
| Branch | 작업 이력을 나누는 참조 | 게임 개발 릴리스 버전 |
| Merge | 브랜치 이력 통합 | 파일 복사만 하는 작업 |
| Rebase | 커밋을 다른 기점에 재적용 | 안전한 무조건 되돌리기 |
| HEAD | 현재 Git 작업 위치의 참조 | 기본 브랜치 이름 |
| Pull Request | 변경 검토·통합 요청 | `git pull` 명령 |
| Code Review | 변경의 타당성과 품질 확인 | 자동 테스트 통과 |
| Issue | 기능·작업·버그의 추적 항목 | Projects의 전체 계획 |
| Sub-issue | 상위 Issue에 속하는 하위 작업 | 체크박스 문장 |
| Milestone | 목표 결과물이나 주요 시점의 묶음 | 시간 단위 Iteration |
| Iteration | 반복 개발 작업 기간 | 특정 출시 버전 |
| GitHub Projects | 이슈/PR을 관리하는 웹 기능 | 데스크톱 설치 프로그램 |
| GitHub Actions | 자동화 실행 서비스 | 자동 빌드를 보장하는 프로그램 |
| Workflow | Actions YAML 자동화 정의 | 단일 Step |
| Job | Runner에서 실행되는 작업 묶음 | 독립 파일 영구 저장소 |
| Step | Job에서 수행하는 단일 동작 | 전체 Workflow |
| Runner | Actions 작업을 실행하는 컴퓨터 | GitHub 저장소 |
| Artifact | 실행 결과로 저장한 파일 묶음 | Cache |
| Cache | 실행 사이 재사용하는 임시 데이터 | 영구 백업 |
| Git LFS | 대용량 파일을 별도 저장하도록 돕는 Git 확장 | 바이너리 자동 병합 도구 |
| `.gitignore` | 기본적으로 추적하지 않을 파일 패턴 | 이미 추적 중인 파일 삭제 기능 |
| `.gitattributes` | 파일 처리·LFS·병합 규칙 설정 | `.gitignore` |
| `.meta` / GUID | Unity 에셋의 고유 식별 및 임포트 정보 | 불필요한 캐시 |
| UnityYAMLMerge | Unity 직렬화 파일용 병합 도구 | 모든 충돌의 자동 해결책 |
| Edit Mode Test | Editor 중심 테스트 | 실제 전체 게임 체험 |
| Play Mode Test | 게임 프레임 기반 테스트 | 사용자 플레이테스트 |
| CI | 지속적 통합과 자동 검사 실천 | Actions 제품명 자체 |
| CD | 지속적 전달/배포 실천 | 무조건 자동 공개 출시 |
| Git Tag | 특정 커밋을 나타내는 참조 | GitHub Release 설명문 |
| Release | 버전별 배포 파일·정보 기록 | 커밋 전체 |
| ADR | 아키텍처 결정과 근거 기록 | 상세 코드 문서 전체 |
| GitHub App | 권한을 제한해 GitHub API에 접근하는 앱 인증 모델 | 사용자의 전체 PAT |
| Webhook | 이벤트 발생 시 외부에 HTTP 요청 전송 | 저장소 간 자동 동기화 |
| `AGENTS.md` | 일부 AI 도구가 읽는 프로젝트 지침 문서 | 모든 AI가 강제로 준수하는 표준 |
