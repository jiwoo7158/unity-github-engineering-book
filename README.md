# Unity 개발자를 위한 GitHub 실무 교과서

Unity 프로젝트를 GitHub로 관리하고, **요구사항 → 구현 → 검토 → 테스트 → 빌드 → 출시** 과정을 소규모 게임 개발팀에 적용할 수 있도록 만든 장별 실무 교재입니다.

## 지금 읽는 방법

- **설치 없이(장별 보기)**: `site/index.html`을 브라우저에서 엽니다. 좌측 목차·검색과 SVG 흐름도를 인터넷 없이 사용할 수 있습니다.
- **설치 없이(한 파일로 보기)**: `single-book.html`을 엽니다. 흐름도 SVG가 HTML 안에 내장되어 단일 파일만 있어도 표시됩니다.
- **Markdown으로**: `BOOK.md`를 VS Code 등에서 엽니다. 원고는 `docs/` 아래에 분리되어 있습니다.
- **웹 사이트로**: 아래 안내에 따라 MkDocs를 실행하거나 GitHub Pages로 배포합니다.

## 로컬 MkDocs 실행

Python 3.10 이상 설치 후 저장소 루트에서:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m mkdocs serve
```

macOS/Linux: `source .venv/bin/activate`를 사용합니다. 로컬 주소는 명령 실행 결과에 표시됩니다.

## GitHub Pages 배포

1. 이 책 저장소를 GitHub에 업로드합니다. 기본 브랜치 이름은 `main`이라고 가정합니다.
2. `mkdocs.yml`의 `site_url`, `repo_url`, `repo_name`을 본인 저장소로 수정합니다.
3. GitHub 저장소 `Settings → Pages → Build and deployment → Source`에서 **GitHub Actions**를 선택합니다.
4. `Actions → Publish book to GitHub Pages → Run workflow`를 실행하거나 `main`에 문서 변경을 푸시합니다.
5. Actions가 성공하면 `Settings → Pages`에서 게시 주소를 확인합니다.

배포된 Pages는 공개 웹사이트로 접근될 수 있습니다. 내부 프로젝트 기밀 또는 비공개 에셋을 이 저장소에 넣지 마세요. 비공개 저장소의 Pages 사용 가능 여부는 요금제·설정에 따라 다릅니다.

## 목차 구성

- A. Git과 GitHub 기초 (01~02)
- B. Unity 저장소와 에셋 관리 (03~04)
- C. 브랜치, PR, 리뷰 (05)
- D. Issues와 Projects (06~07)
- E. Actions, Unity 테스트와 자동 빌드 (08~10)
- F. 문서·보안, 고급 자동화·AI·연동 (11~12)
- 보강 장. 알림 관리(07-A), Discussions·상태 업데이트(07-B), 코드 검색·보안(11-A)
- 부록. 종합 실습, 문제 해결, 용어, 템플릿, 공식 자료, 게시 방법

**이 책은 학습·실습용이며 실제 Unity 게임 프로젝트의 코드나 빌드된 게임 자체가 포함된 것은 아닙니다.** 코드와 설정 예시는 프로젝트 환경에 맞게 검토 후 적용하세요.

## 다이어그램 표시 및 재생성

이 교재의 흐름도 4개는 `docs/assets/diagrams/*.svg` 이미지로 제공됩니다. GitHub Markdown, MkDocs Material, 오프라인 HTML 등에서 **Mermaid JavaScript를 불러오지 않아도 표시**됩니다. 다이어그램의 편집 가능한 원본은 같은 폴더의 `*.mmd` 파일로 보관합니다.

다이어그램을 수정할 때는 원본 `.mmd`를 수정한 뒤 [Graphviz](https://graphviz.org/download/)의 `dot` 명령을 사용할 수 있는 환경에서 다음 순서로 재생성합니다. 단순히 책을 읽거나 기존 HTML을 다시 생성하는 데 Graphviz는 필요하지 않습니다.

```bash
python scripts/render_diagrams.py
python scripts/build_offline.py
python scripts/build_single_html.py
```

`build_offline.py`는 `BOOK.md`와 `site/`의 장별 HTML을 재생성합니다. `build_single_html.py`는 `single-book.html`을 재생성합니다. 이 스크립트는 `mistune`과 `PyYAML`을 사용하며 `requirements.txt`에 포함했습니다. 원본 MkDocs는 `mkdocs.yml`과 `docs/`를 사용하며, 일반 빌드 결과는 `_mkdocs_site/`에 생성되어 제공된 오프라인 `site/`를 덮어쓰지 않습니다. GitHub Pages Workflow의 출력 폴더는 별도로 지정되어 있습니다.

원본 책의 Mermaid 코드 블록이 HTML에서 그대로 보이던 문제를 해결하기 위해 정적 SVG를 선택했습니다. 따라서 MkDocs의 Mermaid 렌더링 확장을 별도로 설정할 필요가 없습니다.

## 2026-10-24 확장판에서 추가된 내용

- 기존 12개 본문 장과 4개 정적 SVG 흐름도는 **삭제하지 않고 보존**했습니다.
- 05~10장 핵심 기능에 실제 설정/실습/문제 해결 절을 추가했습니다.
- 새로운 07-A(Notifications), 07-B(Discussions와 Projects 상태 보고), 11-A(Code Search·Blame·Dependabot·보안) 장을 추가했습니다.
- 02·04·11·12장에 저장소 운영, UVCS 전환 점검, 문서 원본, AI 협업 내용을 보강했습니다.
- `examples/`에는 복사해서 실습할 수 있는 Issue Forms, PR Template, 간단한 Actions, Unity 테스트·빌드 코드 조각을 넣었습니다. 전체 Unity 프로젝트는 **아니며**, 각 환경에 맞게 복사·설정·검증해야 합니다.
- `CHANGELOG.md`에 변경 내용을 기록했습니다.

**검증 범위:** 문서 링크·파일 구성·YAML 파싱 및 오프라인 HTML 생성은 로컬에서 검사할 수 있습니다. 실제 GitHub 계정의 권한 설정, Unity 테스트 실행과 자동 빌드, GitHub Pages의 배포 성공은 사용자 환경이 필요하므로 여기서 검증했다고 주장하지 않습니다.
