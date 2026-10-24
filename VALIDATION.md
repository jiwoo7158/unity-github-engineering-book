# 확장판 검증 기록

검증 시점: 2026-10-24

## 수행한 구조 검사

- 기존 그래프 수정본 ZIP 안의 **모든 기존 docs/*.md 원고가 새 문서의 시작 부분에 그대로 보존**되어 있는지 확인했다. (index.md에만 확장판 소개가 추가됨)
- MkDocs 목차에 22개 페이지가 등록되어 있고 참조한 Markdown 파일이 모두 존재한다.
- 오프라인 장별 HTML의 상대 링크 및 이미지 경로가 모두 존재한다.
- 단일 HTML의 내부 목차 앵커가 존재하며 SVG 다이어그램 4개가 Data URI로 포함된다.
- 기존 4개 SVG, Mermaid 원본, 페이지 생성 스크립트, GitHub Pages Workflow를 보존했다.
- 예제 Issue Forms와 Actions YAML을 문법 수준에서 파싱했다.
- Markdown 코드펜스 짝이 맞는지 검사했다.
- 전체 ZIP 압축의 CRC 오류가 없는지 확인한다.

## 여기서 검증하지 못한 것

- **MkDocs Material의 실제 빌드**: 현재 작업 환경에 설치되어 있지 않다. 제공한 GitHub Pages Workflow 또는 `pip install -r requirements.txt`로 사용자 환경에서 확인한다.
- **실제 브라우저 화면 시각 검증**: 브라우저 자동 접속이 이 환경의 접근 정책에 의해 차단되어 완료하지 못했다. HTML DOM 구조, 링크, 이미지 파일은 검사했다.
- **Unity C# 컴파일과 Unity 빌드**: Unity Editor 및 사용자의 정확한 프로젝트/라이선스가 없으므로 실행 검증하지 않았다.
- **실제 GitHub Projects·Actions 실행**: 테스트 저장소에 직접 배포·실행하지 않았다. 플랜/조직 정책에 따라 UI와 사용 범위가 다를 수 있다.

## 학습 환경에서 권장하는 확인

1. `site/index.html`을 열어 07-A와 11-A 신규 장 및 SVG 흐름도를 확인한다.
2. `single-book.html`을 열어 책 검색과 목차 이동을 확인한다.
3. MkDocs 명령 `python -m mkdocs build --strict`로 사이트 빌드를 확인한다.
4. 새 게임 테스트 저장소에 `examples/github-config` 예제를 복사하여 템플릿·Actions 작동을 확인한다.
5. Unity 테스트 프로젝트에서 `examples/unity-ci`의 예제를 확인하고 Play Mode 또는 Edit Mode 테스트를 검증한다.
