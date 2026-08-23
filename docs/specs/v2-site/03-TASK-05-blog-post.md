# TASK 05 — Posts 목록과 글 상세

## 목표

Posts 목록 화면과, 블로그·프로젝트·수상 경력이 공유하는 글 상세 화면을 구현한다. 시안에 하드코딩되어 있던 `Java의 Constant Pool과 String Constant Pool` 본문은 마크다운에서 읽어 렌더링되도록 대체한다.

## 선행

TASK 02, TASK 03.

## 작업

### Posts 목록

1. `posts.html` — front matter에 `permalink: /posts/`. 인트로 한 줄 뒤에 `site.posts`를 연도별로 묶어 출력한다. 연도 내림차순, 연도 안에서도 최신순.
2. 각 항목은 `MM.DD`(mono, min-width 44px) + 제목. 연도 헤더는 mono 12px / 0.1em / border-bottom.
3. `_sass/_post-list.scss`.

목록 `/posts/`와 개별 글 `/posts/:title/`은 충돌하지 않는다. 02-PLAN의 라우팅 절 참조.

### 글 상세

4. `_layouts/post.html` — 02-PLAN의 렌더링 흐름대로 구성한다. `page.kind`로 세 종류를 분기한다.
5. `_includes/post-meta.html` — 블로그에만 `YYYY.MM.DD` · 읽기 시간 · 카테고리를 그린다. 읽기 시간은 글자 수를 분당 500자로 올림하되 정확한 배수는 과대 계산하지 않는다.
6. `_includes/post-summary.html` — `page.summary`가 있을 때만 요약 콜아웃을 그린다. 라벨은 `요약`, 강조색 mono. 없으면 아무것도 출력하지 않는다.
7. `_includes/post-header-meta.html` — 프로젝트는 기술 스택·링크, 수상 경력은 수상 등급·링크를 라벨/값 그리드로 그린다. 참여자와 담당 정보는 표시하지 않는다.
8. `_includes/carousel.html` — 이미지가 한 장이면 그대로 출력하고, 두 장 이상이면 스크롤 스냅 트랙·좌우 버튼·현재 위치 점을 그린다. 첫 이미지로 시작하며 터치 스와이프와 키보드 스크롤을 지원한다.
9. `_includes/lightbox.html` — 링크로 감싸지 않은 본문·캐러셀 이미지를 클릭하거나 Enter/Space로 열 수 있는 확대 모달. 모달 안에서 포커스를 순환하고 Escape로 닫은 뒤 원래 이미지로 돌려준다.
10. `_includes/post-tags.html` — `page.tags` 칩. 상단 `border-top`, `#태그` 형태.
11. `_sass/_post.scss` — 마크다운 본문 요소 스타일. 시안의 인라인 스타일을 선택자로 옮긴다.
    - `h2` 19px / 700 / `--font-post-title` / `--text-strong`
    - `p` 16.5px / 1.85 / `--text-soft`, 블록 간 간격 34px
    - `pre` 패딩 20px 22px / `--surface` / `--border` / radius 6px / `overflow-x: auto` / mono 13.5px
    - 인라인 `code` mono 14px / 패딩 2px 6px / radius 4px / `--code-bg` / `--accent-code`
    - `ul`, `ol` padding-left 20px, 항목 간 7px
    - `strong` `--text-mid` / 600, `em` `--text-mid` / `font-style: normal`
    - `blockquote` 좌측 강조색 보더 + `--surface` 배경. 기존 글이 요약에 `>`를 자주 쓴다.
    - `table`, `hr`, `img`, `a`
    - Rouge 하이라이트 클래스는 시안 코드 블록의 톤(`--text-chip` 본문, `--muted-dim` 주석)에 맞춰 최소한으로만 색을 준다.
12. 뒤로가기 링크 — 블로그는 `← Posts`, 프로젝트는 `← 프로젝트`, 수상 경력은 `← 수상 경력`으로 표기하며 프로젝트·수상 링크는 `/about/`으로 돌아간다.

## 완료 조건

- `/posts/`에 19편이 연도별로 나오고, `/posts/Java의-Constant-Pool과-String-Constant-Pool/`이 마크다운 본문으로 렌더링되며 시안의 Post 화면과 시각적으로 일치한다.
- 프로젝트·수상 경력 상세가 이미지와 외부 링크, 각 종류에 맞는 기술 스택 또는 수상 등급을 표시한다.
- 시안 어디에도 하드코딩된 글 본문이 남아 있지 않다.
- 375px에서 코드 블록이 가로 스크롤로 처리되고 페이지 전체는 가로 스크롤이 없다.

## 커밋

- `feat: implement posts index grouped by year`
- `feat: implement shared post layout for blog, projects, and awards`
- `style: add markdown content styles matching the dark design`
