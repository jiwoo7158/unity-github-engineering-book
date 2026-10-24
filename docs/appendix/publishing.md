# 부록 E. MkDocs로 책을 읽고 GitHub Pages에 게시하기

이 교재는 Markdown 원본인 `docs/` 폴더와 사이트 설정인 `mkdocs.yml`을 기본 구조로 한다. **MkDocs는 Markdown을 HTML 사이트로 만드는 도구**이고 **Material for MkDocs는 그 사이트의 테마**다. GitHub Pages는 만들어진 HTML을 웹에서 제공하는 GitHub의 정적 웹 호스팅 서비스다.

## 1. 설치 없이 읽기

책 ZIP의 `site/index.html`을 브라우저로 열면 오프라인용 HTML 목차에서 각 장으로 이동할 수 있다. 이 HTML은 별도 정적 변환본이며, 온라인 MkDocs Material 사이트와 인터페이스가 완전히 같지는 않다. Markdown 원본이 필요하면 `BOOK.md`를 VS Code의 Markdown Preview로 열 수 있다.

## 2. MkDocs 로컬 미리보기

1. Python 3.10 이상 설치.
2. 책 저장소 폴더 열기.
3. 가상환경 생성 및 패키지 설치.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m mkdocs serve
```

가상환경 실행 정책 때문에 활성화가 어려우면 `.venv\Scripts\python.exe -m pip install -r requirements.txt`처럼 가상환경의 Python을 직접 사용할 수도 있다.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m mkdocs serve
```

명령 실행 결과에 출력되는 로컬 주소(통상 `http://127.0.0.1:8000`)를 브라우저에서 연다. 저장한 Markdown 변경은 개발 서버에서 다시 반영될 수 있다.

## 3. 정적 파일 빌드

```bash
python -m mkdocs build --strict --site-dir _pages
```

이 명령은 검색 색인·스타일·HTML 페이지를 `_pages/`에 생성한다. `--strict`는 경고를 오류로 취급하므로 메뉴 경로·문서 링크 등을 검증하는 데 도움이 된다. 이 책의 사이트 설정은 `mkdocs.yml`에 들어 있다.

## 4. GitHub Pages로 게시하기

1. 새 GitHub 저장소를 만들고 본 교재의 파일(숨겨진 `.github` 포함)을 업로드한다.
2. `mkdocs.yml`의 아래 값을 자신의 저장소로 교체한다.

```yaml
site_url: https://YOUR_ACCOUNT.github.io/YOUR_REPOSITORY/
repo_url: https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY
repo_name: YOUR_ACCOUNT/YOUR_REPOSITORY
```

3. 저장소에서 `Settings → Pages`로 이동한다.
4. `Build and deployment → Source`를 **GitHub Actions**로 선택한다.
5. `Actions → Publish book to GitHub Pages`에서 **Run workflow**를 누르거나 `main`에 문서 변경을 푸시한다.
6. `Actions` 실행이 완료되면 `Settings → Pages`의 게시 URL을 연다.

배포 Workflow는 `.github/workflows/docs-pages.yml` 파일로 제공한다. **이 Workflow는 책의 문서를 게시하는 용도**이며 Unity 게임의 빌드·테스트를 실행하지 않는다.

### Workflow의 주요 동작

- 저장소를 체크아웃한다.
- Python을 준비한다.
- `requirements.txt`의 MkDocs Material을 설치한다.
- `mkdocs build --strict`로 문서를 빌드한다.
- `upload-pages-artifact`로 게시할 파일을 올린다.
- `deploy-pages`로 GitHub Pages에 배포한다.

## 5. 게시할 때 주의할 점

- **공개 범위:** GitHub Pages는 웹 페이지를 게시하는 서비스다. 저장소가 Private이어도 웹사이트 공개 범위는 별도 정책이 적용될 수 있으니 기밀 내용을 넣지 않는다.
- **분리 권장:** 실제 게임 저장소와 학습 교재 저장소를 분리하면 대용량 에셋/라이선스/접근 권한 관리가 쉬워진다.
- **LFS:** Pages에서 LFS 원본 파일을 웹사이트 리소스처럼 직접 제공하는 구성은 적절하지 않다. 책에는 일반 이미지/작은 정적 파일만 사용한다.
- **브랜치:** 제공 Workflow는 기본 브랜치 `main`을 기준으로 작성했다. 다른 브랜치를 사용하면 수정한다.
- **검증:** 이 환경에서는 외부 패키지를 설치할 네트워크를 사용할 수 없어 실제 MkDocs CLI 빌드를 수행하지 못했다. 대신 Markdown 구조·내부 링크·정적 오프라인 HTML을 검증했다. 게시 전 실제 GitHub Actions 결과를 확인한다.

## 6. 수정·확장 방법

본문은 `docs/part-a`에서 `docs/part-f` 및 `docs/appendix`에 있으며, 목차 순서는 `mkdocs.yml → nav`에서 수정한다. 장을 추가할 때는 원고 작성→목차 등록→로컬 `mkdocs build --strict`→PR 검토→Pages 게시 순서로 진행한다. `BOOK.md`와 오프라인 `site/`는 함께 제공된 생성 스크립트를 실행해 다시 만들 수 있다(생성 환경에 `mistune` 필요).

**공식 자료:** [MkDocs Material](https://squidfunk.github.io/mkdocs-material/creating-your-site/), [Material 게시](https://squidfunk.github.io/mkdocs-material/publishing-your-site/), [GitHub Pages 구성](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)


## 흐름도(Mermaid)가 코드 블록으로 표시되는 문제

초기 오프라인 HTML 생성기에서는 Mermaid를 일반 코드 블록으로 출력하는 문제가 있었다. 수정판에서는 편집용 원본을 `docs/assets/diagrams/*.mmd`로 보존하고, 문서 본문은 미리 렌더링한 `*.svg`를 참조한다. 따라서 MkDocs·GitHub·로컬 HTML에서도 JavaScript 없이 흐름도가 표시된다.

SVG 그림 내용을 바꾸려면 Graphviz의 `dot` 명령이 설치된 환경에서 `python scripts/render_diagrams.py`를 실행한 후, `python scripts/build_offline.py`와 `python scripts/build_single_html.py`를 다시 실행한다. 이미 생성된 SVG를 읽는 데 Graphviz 설치는 필요 없다.
