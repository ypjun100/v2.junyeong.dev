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
5. `_includes/post-meta.html` — `YYYY.MM.DD` · 읽기 시간 · 세 번째 항목. 세 번째 항목은 `kind`에 따라 카테고리(blog) / `desc`(project) / `prize.name`(award).
6. `_includes/post-summary.html` — `page.summary`가 있을 때만 요약 콜아웃을 그린다. 라벨은 `요약`, 강조색 mono. 없으면 아무것도 출력하지 않는다.
7. `_includes/post-extras.html` — `kind != blog`일 때 외부 링크 행, 참여자, 스킬 칩을 그린다. 수상 등급은 헤더 메타가 강조색으로 이미 보여주므로 여기서 다시 그리지 않는다.
   - 외부 링크는 `url.type`(`github`, `news`, `website`, `link`, `youtube`)에 맞는 인라인 SVG 아이콘을 붙인다. 아이콘 `fill`은 `currentColor`로 두고 색은 CSS가 정한다.
   - 스킬 칩은 About 기술 스택 칩과 동일한 스타일(`--border-strong`, radius 4px, `--text-chip`)을 재사용한다.
   - 참여자는 사람 아이콘 + 쉼표로 이은 목록, `--muted-dim`.
8. `_includes/gallery.html` — `page.images`가 있을 때 이미지들을 세로로 쌓아 그린다. 각 이미지는 `border: 1px solid var(--border)`, `border-radius: 6px`, `max-width: 100%`.
9. `_includes/post-tags.html` — `page.tags` 칩. 상단 `border-top`, `#태그` 형태.
10. `_sass/_post.scss` — 마크다운 본문 요소 스타일. 시안의 인라인 스타일을 선택자로 옮긴다.
    - `h2` 19px / 700 / `--font-post-title` / `--text-strong`
    - `p` 16.5px / 1.85 / `--text-soft`, 블록 간 간격 34px
    - `pre` 패딩 20px 22px / `--surface` / `--border` / radius 6px / `overflow-x: auto` / mono 13.5px
    - 인라인 `code` mono 14px / 패딩 2px 6px / radius 4px / `--code-bg` / `--accent-code`
    - `ul`, `ol` padding-left 20px, 항목 간 7px
    - `strong` `--text-mid` / 600, `em` `--text-mid` / `font-style: normal`
    - `blockquote` 좌측 강조색 보더 + `--surface` 배경. 기존 글이 요약에 `>`를 자주 쓴다.
    - `mark` 강조색 계열 배경 + 밝은 글자. 기존 프로젝트 글이 핵심 문장에 `<mark>`를 쓴다.
    - `table`, `hr`, `img`, `a`
    - Rouge 하이라이트 클래스는 시안 코드 블록의 톤(`--text-chip` 본문, `--muted-dim` 주석)에 맞춰 최소한으로만 색을 준다.
11. 뒤로가기 링크 — `kind == blog`이면 `← Posts`(`/posts/`), 아니면 `← About`(`/about/`).

## 완료 조건

- `/posts/`에 19편이 연도별로 나오고, `/posts/Java의-Constant-Pool과-String-Constant-Pool/`이 마크다운 본문으로 렌더링되며 시안의 Post 화면과 시각적으로 일치한다.
- 프로젝트·수상 경력 상세가 스킬 칩, 이미지, 참여자, 외부 링크, 수상 등급을 모두 표시한다.
- 시안 어디에도 하드코딩된 글 본문이 남아 있지 않다.
- 375px에서 코드 블록이 가로 스크롤로 처리되고 페이지 전체는 가로 스크롤이 없다.

## 커밋

- `feat: implement posts index grouped by year`
- `feat: implement shared post layout for blog, projects, and awards`
- `style: add markdown content styles matching the dark design`
