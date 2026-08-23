# Meta

- Track Type: B
- Base branch: main
- Working branch: feature/v2-site-jekyll-portfolio
- PR URL: https://github.com/ypjun100/v2.junyeong.dev/pull/1
- Status: reviewed

## 비고

- 저장소는 빈 디렉터리에서 `git init -b main`으로 새로 만들었다. `main`은 승인된 스펙 커밋 하나만 갖고 있고 구현은 전부 working branch에 있다.
- 원격 저장소 `ypjun100/v2.junyeong.dev`를 사용자 승인 후 public으로 생성했다.
- 2026-08-23 코드 리뷰에서 전체 `main...HEAD` diff, PR 피드백, 깨끗한 체크아웃 빌드, 375·768·1280px 화면을 확인했다. 이미지 확대 모달의 키보드 접근성과 읽기 시간의 500자 경계 계산을 수정하고 구현과 어긋난 스펙·PR 설명을 갱신했다.
- 기존 글 이미지의 alt 누락과 캐러셀 위치 점의 작은 터치 영역은 콘텐츠 이관·시각 밀도와 맞물린 잔여 접근성 항목으로 남겼다.
- 2026-08-23 후속 리뷰(직전 리뷰 이후 커밋 4개 포함 전체 diff 재검토): 라이트박스 키보드 개선이 포인터 세션의 닫기에서 원본 이미지에 포커스 링을 되살리던 것을 세션 단위 억제로 고쳤고, CI에 개수 대조를 추가했으며, 스펙 문서의 이력 서술을 현재 동작 서술로 정리했다.
- 배포 전에 사용자가 직접 해야 하는 일이 남아 있다. 저장소 설정에서 Pages 소스를 GitHub Actions로 바꾸는 것, 그리고 `v2.junyeong.dev` DNS CNAME 레코드를 추가하는 것.
