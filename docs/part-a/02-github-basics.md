# 02. GitHub 기본 사용법

## 2.1 GitHub와 저장소의 관계

GitHub는 **Git 저장소를 호스팅**하면서 Issues, Projects, Pull Requests, Actions, Releases, 보안 기능 등 개발 협업 서비스를 제공한다. GitHub에 로그인하는 것은 Git을 설치하는 것과 다르고, GitHub Desktop은 이 서비스를 로컬에서 편하게 다루는 선택형 GUI 앱이다.

저장소 주소 예: `https://github.com/OWNER/aster-arena`. `OWNER`는 개인 계정이나 조직(Organization)이다. 브라우저에서 보이는 `Code`, `Issues`, `Pull requests`, `Actions`, `Projects` 등의 탭은 저장소 설정과 권한에 따라 표시 위치가 달라질 수 있다. 특히 Projects는 개인/조직 소유 프로젝트로 별도 존재하며 여러 저장소의 Issue와 PR을 모을 수 있다.

## 2.2 계정과 인증

GitHub 계정을 만든 후 2단계 인증을 활성화한다. 로컬 Git에서 HTTPS로 원격 저장소에 연결할 때 일반 계정 비밀번호를 직접 사용하는 방식과 GitHub 웹 로그인은 다르다. GitHub Desktop·Git Credential Manager 같은 인증 관리자 또는 SSH Key를 사용할 수 있다.

- **HTTPS**: `https://github.com/OWNER/REPO.git` 주소 사용. 인증 관리자가 토큰을 안전하게 관리할 수 있다.
- **SSH**: `git@github.com:OWNER/REPO.git` 주소 사용. 개인키는 사용자 기기에 보관하고 공개키를 GitHub 계정에 등록한다.
- **PAT(Fine-grained Personal Access Token)**: 특정 저장소/권한/기간을 제한한 토큰. 자동화에 불필요하게 광범위한 권한을 주지 않는다.
- **GitHub App**: 앱이 설치된 조직·저장소 범위에서 API를 접근하도록 하는 인증 모델. 고급 자동화에서 중요하다.

!!! danger "기밀 정보"
    PAT, SSH 개인키, Unity 라이선스 비밀 정보, Discord Webhook URL을 코드·Issue·스크린샷·Actions 로그에 노출하지 않는다. 유출된 비밀은 삭제 커밋만으로 해결되지 않으므로 즉시 폐기·재발급해야 한다.

## 2.3 저장소 생성과 공개 범위

웹사이트 우측 상단 `+ → New repository`에서 이름, 설명, 공개 여부를 선택한다. **Public**은 누구나 소스에 접근할 수 있고, **Private**은 권한 있는 사용자 중심으로 접근이 제한된다. 협업에 필요한 기능과 Pages 게시 가능성은 계정·조직 요금제 및 설정을 확인한다.

새 Unity 프로젝트를 올릴 때 초기화 옵션을 잘 선택해야 한다. 로컬에 이미 커밋이 있다면 GitHub에서 README를 추가한 빈 저장소를 동시에 만들지 않는 편이 첫 푸시 시 불필요한 이력 충돌을 줄인다. 초보자는 GitHub Desktop의 `File → Add local repository` 또는 `Create a repository`, 이어 `Publish repository` 흐름을 쓰면 편리하다.

```bash
# 이미 로컬 Git 저장소가 있는 경우의 예시
git branch -M main
git remote add origin https://github.com/OWNER/aster-arena.git
git remote -v
git push -u origin main
```

이미 `origin`이 연결되어 있다면 `remote add`를 다시 호출하지 않는다. `git remote -v`로 확인하고 필요한 경우 `git remote set-url origin URL`을 사용한다.

## 2.4 개인 Repository와 Organization

개인 저장소는 개인이 소유한다. Organization은 여러 저장소, 팀, 권한을 조직 단위로 관리하기 위한 공간이다. 소규모 팀도 프로젝트 소유권을 특정 팀원의 개인 계정에 묶지 않으려면 조직 저장소를 고려할 수 있다.

| 항목 | 개인 저장소 | 조직 저장소 |
|---|---|---|
| 소유권 | 개인 계정 중심 | 조직 중심 |
| 협업 | Collaborator 초대 | 조직 Team과 역할 설정 |
| 팀원 교체 | 소유자 의존 위험 확인 | 역할 및 권한 재배분 용이 |
| 관리 부담 | 상대적으로 작음 | 조직 설정 관리 필요 |

조직/저장소의 역할은 단순한 읽기 권한에서 관리 권한까지 다양하다. 최소 권한을 부여하고, 외부 협업자가 더 이상 참여하지 않을 때 접근을 회수하자.

## 2.5 기본 파일의 의미

- `README.md`: 프로젝트의 목적, 설치 환경, 실행 방법, 기여 절차를 안내한다. 기본 화면에 노출되므로 신규 팀원이 읽는 첫 문서다.
- `.gitignore`: 추적하지 않을 새 파일의 패턴을 정의한다. 이미 Git이 추적하는 파일을 나중에 적어도 **자동으로 추적 해제되지 않는다**.
- `.gitattributes`: 파일 속성, 줄바꿈 및 LFS 추적·병합 규칙을 정의한다.
- `LICENSE`: 외부 사용자가 소스 코드를 사용할 수 있는 법적 권한에 영향을 준다. 공개 저장소라는 사실만으로 자유롭게 재사용할 수 있다는 뜻은 아니다.
- `CONTRIBUTING.md`: 브랜치, PR, 테스트, 스타일, 커뮤니케이션 규칙.
- `.github/`: Issue·PR 템플릿, 워크플로, 기여 정책 등 GitHub 관련 설정을 보관한다.

## 2.6 웹에서 확인해야 할 화면

1. `Code`: 파일, 기본 브랜치, 최근 커밋, Clone 주소.
2. `Commits`: 변경 이력과 작성자, 특정 변경 비교.
3. `Branches`: 진행 중인 작업 분기와 통합 상태.
4. `Issues`: 할 일, 버그, 요구사항. 활성화하지 않았다면 저장소 설정 확인.
5. `Pull requests`: 제안된 코드 변경과 리뷰.
6. `Actions`: CI와 자동화 실행 결과.
7. `Settings`: 권한, 보호 정책, 웹 페이지 배포 및 프로젝트 관리 설정.
8. `Insights`: 저장소 활동 정보. Projects의 Insights와 구분.

## 2.7 로컬에서 Clone한 뒤 검증

```bash
git clone https://github.com/OWNER/aster-arena.git
cd aster-arena
git remote -v
git status
git branch -a
```

빈 저장소라면 실제 프로젝트 폴더와 구조가 다를 수 있다. Unity 프로젝트를 Clone하는 경우 `Assets`, `Packages`, `ProjectSettings`가 **저장소 루트**에 제대로 위치하는지 확인한다. `AsterArena/AsterArena/Assets`처럼 중첩된 구조를 의도치 않게 만드는 실수가 흔하다.

## 2.8 입문자가 자주 하는 실수

- 웹사이트의 `Upload files`로 큰 Unity 프로젝트를 여러 번 수동 업로드한다 → 버전 관리와 에셋 복원이 어려워진다.
- GitHub Desktop에서 Commit만 하고 Push하지 않는다 → 동료가 변경을 볼 수 없다.
- `git pull`을 무작정 반복한다 → 미커밋 변경이나 충돌의 원인을 놓친다.
- Public 저장소에 유료 에셋이나 라이선스 제한 파일을 넣는다 → 저작권·라이선스 문제가 생길 수 있다.
- 프로젝트 소유자 한 명만 모든 관리 권한을 가진다 → 팀원 교체와 장기 유지보수에 위험하다.

## 2.9 실습: 두 위치에서 같은 저장소 사용

1. 개인 Private 저장소를 생성한다.
2. 프로젝트 폴더에서 Git 이력을 만들고 원격 주소를 연결한다.
3. README를 커밋하고 푸시한다.
4. 다른 폴더로 Clone한다.
5. 두 번째 폴더에서 README를 수정해 푸시한다.
6. 첫 번째 폴더에서 Fetch/Pull을 하여 변화를 확인한다.
7. `git log --oneline`으로 커밋의 이동을 설명한다.

**확인할 결과:** 계정/프로그램/저장소의 차이를 말할 수 있고, 팀원 초대·인증·Clone·Push·Pull을 실제로 완료한다.

**공식 자료:** [GitHub 계정 시작하기](https://docs.github.com/en/get-started), [저장소 관리](https://docs.github.com/en/repositories), [GitHub Desktop](https://docs.github.com/en/desktop)

---

## 2.9 확장: Unity 팀을 위한 저장소 설정 점검

프로젝트가 개인 계정 저장소에 있는지, Organization 저장소에 있는지에 따라 권한과 관리자 책임이 달라진다. 개인 프로젝트를 실제 팀의 공동 작업으로 키우려면 다음 순서로 확인한다.

1. 저장소 `Settings`에서 **Public/Private** 상태를 확인한다.
2. `Collaborators` 또는 Organization의 `People/Teams`에서 누가 접근하는지 확인한다.
3. 팀원의 역할별로 필요한 최소 권한을 부여한다. `Read`는 확인 중심, `Write`는 코드 작업, `Maintain/Admin`은 더 큰 관리 권한을 포함하므로 무작정 모두에게 관리자 권한을 주지 않는다.
4. 저장소 기본 브랜치를 `main` 등 명확한 이름으로 합의한다.
5. Issues, Discussions, Projects 등 필요한 기능이 켜져 있는지 확인한다.
6. 프로젝트에서 공개하면 안 되는 소스와 에셋의 라이선스를 확인한다.
7. 복구 담당자, 백업 위치, 팀장이 졸업하거나 프로젝트에서 빠질 때의 소유권 이전 절차를 정한다.

**개인 저장소와 Organization의 차이**: 개인 저장소는 시작이 빠르지만, 계정 소유자에게 설정이 집중되기 쉽다. Organization은 팀 구성원·저장소 권한을 보다 체계적으로 관리할 수 있지만 초기 운영 부담이 생긴다. 어느 쪽이든 프로젝트의 장기적인 소유권과 접근 권한을 먼저 합의하자.

### GitHub Desktop을 사용하는 팀원과 CLI를 사용하는 팀원이 섞인 경우

명령줄이나 GUI의 선택은 서로 달라도 된다. 다만 저장소의 **공통 규칙은 같아야 한다**.

- 동일한 기본 브랜치와 브랜치 이름 정책을 사용한다.
- `.gitignore` 및 `.gitattributes` 규칙은 Repository에서 공유한다.
- `commit → push → PR → review → merge`가 실제로 같은 변경 결과를 만든다.
- 충돌 해결 후 Unity에서 프로젝트를 열어 확인한다.

**학습 확인:** 저장소를 팀원에게 전달하면서 '어떤 계정 권한이 필요한지', '코드는 어디에서 받을 수 있는지', '작업은 어느 화면에서 확인하는지'를 구두 설명 없이 문서로 전달할 수 있다.

**공식 자료:** [저장소 권한](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/managing-repository-settings) · [Organization](https://docs.github.com/en/organizations)
