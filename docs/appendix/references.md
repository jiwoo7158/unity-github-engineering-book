# 부록 D. 공식 자료와 검증 범위

이 책은 **2026-10-16 기준** 공개된 GitHub·Unity·Git·MkDocs 관련 공식 문서의 기능 분류와 사용 방식을 참고하여 작성했다. 예시는 이 책을 만들기 위해 독립적으로 작성한 학습용 설명이며, 공식 문서의 페이지 전체를 복제하지 않는다.

## Git 기본과 GitHub 저장소

- [Git 공식 문서](https://git-scm.com/docs)
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [GitHub 시작하기](https://docs.github.com/en/get-started)
- [GitHub Repositories](https://docs.github.com/en/repositories)
- [GitHub Desktop](https://docs.github.com/en/desktop)
- [GitHub 공식 Unity.gitignore](https://github.com/github/gitignore/blob/main/Unity.gitignore)

## Unity 프로젝트와 에셋

- [Unity Manual](https://docs.unity3d.com/Manual/index.html)
- [Unity Smart Merge](https://docs.unity3d.com/Manual/SmartMerge.html)
- [GitHub Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [Git LFS 설정](https://docs.github.com/en/repositories/working-with-files/managing-large-files/configuring-git-large-file-storage)
- [Unity Test Framework](https://docs.unity3d.com/Packages/com.unity.test-framework@latest)
- [Unity Editor 명령줄 인수](https://docs.unity3d.com/Manual/EditorCommandLineArguments.html)
- [Unity BuildPipeline.BuildPlayer](https://docs.unity3d.com/ScriptReference/BuildPipeline.BuildPlayer.html)

## 팀 협업과 프로젝트 관리

- [GitHub Pull Requests](https://docs.github.com/en/pull-requests)
- [GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues)
- [GitHub Issue Sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)
- [GitHub Issue Dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies)
- [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Projects 기본 자동화](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations)
- [Projects를 Actions로 자동화](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/automating-projects-using-actions)

## GitHub Actions와 배포

- [GitHub Actions](https://docs.github.com/en/actions)
- [Workflow 문법](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Actions 보안](https://docs.github.com/en/actions/security-for-github-actions)
- [GitHub Pages 게시 소스 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

## 고급 자동화와 AI

- [GitHub REST API](https://docs.github.com/en/rest)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [GitHub CLI](https://cli.github.com/manual/)
- [GitHub Copilot 사용자 지정 지침](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)

## 검증이 필요한 항목

- GitHub와 Unity의 **요금·스토리지·Actions 사용량·Pages 공개 범위**는 변동 가능성이 있으므로 최신 가격표와 계정 상태를 확인해야 한다.
- Unity 에디터의 **설치 경로, 빌드 API, 테스트 CLI, 라이선스 인증**은 버전별로 다르다. 사용 중인 Unity 버전의 문서를 우선한다.
- GitHub Projects의 **필드·권한·UI**는 저장소/조직 권한과 기능 출시 상태에 따라 달라질 수 있다.
- 각 장의 YAML 및 C# 예시는 **교육용이며 실제 사용자 환경에서 실행 검증된 완성 프로젝트는 아니다**. 로컬 실습→로그 분석→작업 환경에 맞춘 조정을 전제로 한다.

## 소프트웨어공학 관점의 원칙

본서가 사용하는 요구사항 → 구현 → 리뷰 → 테스트 → 빌드 → 배포는 **개발 과정의 추적성과 재현성을 높이는 실무 흐름**이다. GitHub 자체가 게임 기획의 재미, 일정의 현실성, 팀원의 동기, 출시 품질을 자동으로 보증한다는 의미는 아니다. 게임 특유의 플레이 경험 검증은 별도 설계·관찰·실험이 필요하다.

## 2026-10-24 확장 내용의 공식 문서

아래 내용은 이번 보강판에서 새로 다룬 GitHub 기능과 관련된 1차 문서다. 각 기능의 메뉴 위치, 요금제·접근 권한, API·설정 지원 범위는 시간이 지나면서 바뀔 수 있다.

- [알림 개요와 설정](https://docs.github.com/en/subscriptions-and-notifications/concepts/about-notifications)
- [Inbox 검색 필터 지원 범위](https://docs.github.com/en/subscriptions-and-notifications/reference/inbox-filters)
- [Discussions 카테고리 관리](https://docs.github.com/en/discussions/managing-discussions-for-your-community/managing-categories-for-discussions)
- [Projects Status Updates](https://docs.github.com/en/issues/planning-and-tracking-with-projects/sharing-project-updates)
- [Projects 기본 자동화](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations)
- [Projects Auto-add와 제한](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically)
- [Issue Forms YAML 문법](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [Rulesets 관련 규칙 목록](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Actions Workflow 문법](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Actions 보안 설정](https://docs.github.com/en/actions/security-for-github-actions)
- [Code Search 사용법](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax)
- [파일 History와 Blame](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files)
- [Dependabot 지원 생태계 목록](https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems)
- [Dependabot alerts](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-dependabot-alerts)
- [Unity 명령줄 빌드](https://docs.unity3d.com/kr/current/Manual/build-command-line.html)

### 이 책에서 확인하지 못한 부분

이 문서 패키지를 생성하는 환경에는 사용자의 GitHub 저장소 관리자 권한과 정확한 Unity 프로젝트/라이선스 정보가 없다. 따라서 **실제 GitHub 프로젝트 화면 설정, GitHub Actions 실행 비용, Unity 빌드 성공, 스토어 배포 성공을 실측 검증하지 않았다.** YAML과 코드 예제는 학습용 구성으로 제공하며 테스트 프로젝트에 적용해 검증해야 한다.
