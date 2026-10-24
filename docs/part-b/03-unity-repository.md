# 03. Unity 프로젝트를 GitHub에 업로드하기

## 3.1 Unity 프로젝트는 일반 소스 저장소와 무엇이 다른가?

Unity는 C# 코드뿐 아니라 씬, 프리팹, 머티리얼, 텍스처, 애니메이션, 오디오, 패키지 설정, 임포트 정보 등 다양한 자산을 참조한다. 파일의 **이름과 경로**뿐 아니라 `.meta` 안의 **GUID**를 사용해 참조를 유지한다. 따라서 스크립트 몇 개만 올려서는 프로젝트를 완전히 복원할 수 없다. Unity 저장소의 성공 기준은 **다른 컴퓨터 또는 깨끗한 폴더에서 Clone한 뒤 동일한 에디터 버전으로 열고 게임을 실행할 수 있는가**다.

### 핵심 프로젝트 폴더

| 경로 | 역할 | 일반적 Git 처리 |
|---|---|---|
| `Assets/` | 코드·씬·프리팹·리소스와 `.meta` | 추적 |
| `Packages/manifest.json` | 패키지 직접 의존성 | 추적 |
| `Packages/packages-lock.json` | 패키지 해결·고정 정보 | 대체로 추적 |
| `Packages/` 로컬 패키지 | 저장소에 포함하는 로컬 패키지 | 패키지 설계에 따라 추적 |
| `ProjectSettings/` | 프로젝트 전역 설정·에디터 버전 | 추적 |
| `UserSettings/` | 개인별 에디터 설정 | 대개 제외 |
| `Library/` | Unity 임포트 캐시·생성 정보 | 제외 |
| `Temp/`, `Obj/`, `Logs/` | 임시·중간 산출물 | 제외 |
| `Build/`, `Builds/` | 게임 빌드 산출물 | 통상 별도 보관 |

Unity 버전에 따라 `ProjectSettings` 설정 메뉴와 자동 생성 폴더의 세부 구조가 달라질 수 있다. 프로젝트에서 실제 발생하는 파일을 확인하고 공식 `Unity.gitignore`를 기초로 수정한다.

## 3.2 `.meta` 파일과 GUID

`Assets/Art/Sword.fbx`가 있으면 Unity는 보통 `Sword.fbx.meta` 파일을 만든다. `.meta`에는 GUID 및 임포트 관련 메타데이터가 들어 있다. 프리팹이 이 에셋을 참조할 때 GUID가 중요하므로 원본만 Git에 올리고 `.meta`를 빠뜨리면 참조가 깨질 수 있다.

**안전한 규칙**

1. `Assets` 안의 에셋을 이동·이름 변경할 때는 가능한 한 Unity Editor의 Project 창에서 처리한다.
2. 파일 시스템에서 직접 이동하는 경우 해당 `.meta` 파일도 함께 이동되는지 확인한다.
3. `.meta`는 전부 무시하는 규칙(`*.meta`)을 만들지 않는다.
4. 파일을 삭제할 때 고아 `.meta`가 남지 않았는지 확인한다.
5. GUID가 갑자기 바뀌거나 같은 GUID가 중복되면 참조 문제를 우선 조사한다.

C# 스크립트에도 `.meta`가 붙는다. 이름만 같게 새 파일을 만들었다고 기존 Unity 참조가 자동 보존되는 것은 아니다.

## 3.3 에디터 및 직렬화 설정

Unity Editor의 `Edit → Project Settings → Editor`에서 관련 항목을 확인한다. 버전에 따라 UI 표기가 달라질 수 있으므로 설치된 Unity의 매뉴얼을 함께 본다.

- **Visible Meta Files**: `.meta` 파일을 외부 버전 관리에 적절한 형태로 노출한다. 현대 Unity 버전에서 일부 선택 항목이 이전 버전과 다르게 보일 수 있다.
- **Asset Serialization / Force Text**: 가능한 씬·프리팹·에셋을 텍스트 기반으로 저장해 변경 비교·병합 가능성을 높인다. 모든 에셋이 텍스트로 바뀌는 것은 아니다.
- **Unity 에디터 버전**: `ProjectSettings/ProjectVersion.txt`에 기록된다. 팀원은 일치하는 버전을 Unity Hub로 설치한다.
- **스크립팅 환경**: API 호환성 수준, Define Symbols, 플랫폼별 설정의 차이가 빌드 실패 원인이 될 수 있다.

## 3.4 `.gitignore`를 설정하는 방법

[GitHub의 Unity.gitignore](https://github.com/github/gitignore/blob/main/Unity.gitignore)를 기반으로 저장소 루트에 `.gitignore`를 만든다. 아래는 **설명용 최소 예시**로, 실제로는 최신 공식 템플릿을 적용해야 한다.

```gitignore
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Ll]ogs/
[Uu]ser[Ss]ettings/
[Bb]uild/
[Bb]uilds/
.vs/
.idea/
*.csproj
*.sln
```

위 예시에는 패키지와 플랫폼별 예외가 모두 포함되어 있지 않다. 또 `.sln` 및 `.csproj`를 팀이 의도적으로 보관하는 경우엔 제외 규칙을 조정한다. `.gitignore`는 신규 **미추적 파일**에 적용되므로 이미 `Library`를 커밋해 버렸다면 다음처럼 추적을 해제해야 할 수 있다.

```bash
# 원본 파일을 로컬 디스크에서 삭제하지 않고 Git 추적에서 제외
git rm -r --cached Library
git add .gitignore
git commit -m "Stop tracking generated Unity cache"
```

`git rm --cached`의 대상 범위를 잘못 지정하면 의도치 않은 파일이 다음 커밋에서 저장소에서 삭제될 수 있다. 항상 `git status`와 `git diff --staged --stat`을 확인한다.

## 3.5 Unity 프로젝트 최초 업로드: 새 프로젝트

1. Unity Hub에서 정확한 에디터 버전을 선택하고 `AsterArena` 프로젝트를 만든다.
2. 프로젝트를 한 번 실행하고 씬 저장·컴파일이 정상인지 확인한다.
3. Unity Editor를 닫는다. 첫 설정 시 불필요한 파일 변동을 줄이기 위함이다.
4. 프로젝트 루트에 `.gitignore`, `.gitattributes`(필요시), `README.md`를 만든다.
5. Git 초기화 후 상태를 확인한다.

```bash
cd "C:/Work/AsterArena"
git init
git branch -M main
git status
git add Assets Packages ProjectSettings .gitignore README.md
git status
git diff --staged --stat
git commit -m "Initialize Unity project"
```

프로젝트에 따라 루트의 추가 필수 파일이 있다면 포함한다. `git add .`를 사용할 수도 있지만, **최초 커밋 때는 반드시 스테이징 파일 목록을 검토**하는 것이 좋다.

6. GitHub에서 `aster-arena` 비공개 빈 저장소를 생성한다.
7. 원격 저장소를 연결해 Push한다.

```bash
git remote add origin https://github.com/OWNER/aster-arena.git
git push -u origin main
```

8. GitHub 웹에서 `Assets/`, `Packages/`, `ProjectSettings/`가 올바르게 보이는지 확인한다.

## 3.6 기존 Unity 프로젝트를 옮길 때

기존에 UVCS로 관리하던 프로젝트를 Git으로 옮기고 싶다면 원본과 별도 작업 사본을 만들고 **관리 도구 전환을 테스트**한다. 두 시스템을 동일한 작업 폴더에 동시에 연결해 두면 메타데이터 충돌·혼란이 발생할 수 있으므로 계획 없이 섞어 운영하지 않는다.

- 기존 UVCS의 태그·브랜치·변경 이력을 얼마나 보존해야 하는지 정한다.
- Unity 버전과 외부 패키지·원본 에셋의 상태를 기록한다.
- 새 Git 저장소로 가져온 뒤 복제 테스트를 수행한다.
- 기존 UVCS는 전환 승인 전까지 읽기 전용 백업처럼 보존한다.
- 전환 날짜, 최종 UVCS 변경 번호, 최초 Git 커밋을 문서에 기록한다.

두 저장소 사이에 단순 파일 복사만 했다고 과거 변경 이력이 변환되는 것은 아니다. 이력 보존이 중요하면 별도 마이그레이션 계획이 필요하다.

## 3.7 깨끗한 폴더에서 복원 테스트

```bash
cd "C:/Work"
git clone https://github.com/OWNER/aster-arena.git AsterArena-Clone
```

Unity Hub에서 `Add project from disk` 등 해당 버전의 UI를 통해 `AsterArena-Clone`을 열고, 다음을 확인한다.

- Unity Hub가 요구하는 에디터 버전이 설치되어 있는가?
- Package Manager 오류 없이 패키지가 설치되는가?
- 콘솔에서 컴파일 오류가 발생하지 않는가?
- 주요 씬에 Missing Script, Missing Material이 생기지 않는가?
- 플레이어 이동·카메라·기본 UI가 정상 동작하는가?
- 실제 Player 빌드가 가능한가?

**복원 테스트는 원래 개발자의 `Library/` 캐시에 의존하지 않는다는 증거**다. 이 절차를 통과하지 못하면 GitHub에 파일을 올렸어도 협업 준비가 끝났다고 보기 어렵다.

## 3.8 Unity와 Git의 실무 주의점

- Unity Editor에서 파일을 편집하는 도중 다른 브랜치로 전환하지 않는 편이 안전하다. 브랜치 전환 전 저장·종료·상태 확인을 권장한다.
- 패키지 설치 후 `manifest.json`과 lockfile 변화를 확인한다.
- 코드를 삭제하거나 이름을 바꾼 뒤 C# 참조와 씬 연결이 깨지지 않는지 확인한다.
- 영문·대소문자 파일명 충돌은 운영체제별 차이로 문제를 일으킬 수 있다.
- 빌드 산출물을 소스 저장소에 반복 커밋하면 이력이 비대해지므로 Artifact/Releases 등 별도 경로를 사용한다.
- 유료 에셋은 라이선스 허용 범위를 확인한다. Private 저장소라도 팀원 간 공유가 계약 위반일 수 있다.

## 3.9 실습과 확인 기준

기본 3D Unity 프로젝트에 C# 스크립트, 씬, 프리팹, 텍스처를 각각 추가하고 커밋한다. 저장소에 `.meta`가 함께 존재하는지 확인한 후 완전히 다른 폴더에 복제해 실행한다. 임시로 `Library/`를 삭제해도 Unity가 다시 생성하는지 확인한다(원본 백업을 확보하고 테스트 사본에서 수행).

**확인할 결과:** GitHub 저장소만으로 프로젝트 복원이 가능하고 어떤 폴더가 소스이며 무엇이 생성 캐시인지 판단한다.

**공식 자료:** [Unity 외부 버전 관리](https://docs.unity3d.com/Manual/ExternalVersionControlSystemSupport.html), [Unity.gitignore](https://github.com/github/gitignore/blob/main/Unity.gitignore), [Unity 프로젝트 구조](https://docs.unity3d.com/Manual/ProjectView.html)
