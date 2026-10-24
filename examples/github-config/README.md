# GitHub 설정 양식 예제

파일들을 테스트 게임 저장소의 같은 경로로 복사하여 실습한다. 이 책 자체를 배포하는 저장소에는 적용하지 않는다.

- `.github/ISSUE_TEMPLATE/feature.yml`: 새 기능 요청 양식.
- `.github/ISSUE_TEMPLATE/bug.yml`: 버그 재현 양식.
- `.github/pull_request_template.md`: PR 검토 체크리스트.
- `.github/workflows/check-readme.yml`: README 존재 여부를 자동 확인하는 최소 Actions.

## 적용 후 확인

1. `feature`, `bug` 라벨이 저장소에 없으면 먼저 만들거나 템플릿의 `labels` 필드를 제거한다.
2. 예제 파일들을 GitHub 기본 브랜치에 반영한다.
3. Issues의 New issue에서 양식이 나타나는지 확인한다.
4. PR을 생성하여 템플릿과 Actions가 작동하는지 확인한다.
5. 보호된 브랜치·조직 정책·Actions 권한 설정 때문에 실행되지 않는 경우 해당 계정 설정을 점검한다.

`check-readme.yml`은 **Unity 테스트·빌드를 수행하지 않는다.** 실제 Unity CI는 09~10장의 전제 조건과 라이선스/Runner 구성을 충족한 뒤 별도 구축한다.
