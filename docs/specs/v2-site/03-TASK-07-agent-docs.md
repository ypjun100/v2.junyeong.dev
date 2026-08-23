# TASK 07 — 에이전트 안내 문서

## 목표

이 저장소를 처음 여는 에이전트가 문서 하나만 읽고 빌드·실행·글 추가·검증을 수행할 수 있게 만든다.

## 선행

TASK 01 ~ 06. 실제로 만들어진 구조를 문서에 반영해야 하므로 마지막에 쓴다.

## 작업

### `AGENTS.md` (정본)

다음 내용을 담는다.

1. **저장소 개요** — 무엇을 하는 사이트인지 두 문장.
2. **명령어** — `bundle install`, `bundle exec jekyll serve`, `bundle exec jekyll build --strict_front_matter`, `bundle exec htmlproofer _site --disable-external --allow-hash-href --ignore-missing-alt`.
3. **디렉터리 지도** — 각 디렉터리의 역할 한 줄씩. 특히 `content/` 아래 `_posts` / `_projects` / `_awards` 세 폴더가 곧 사이트의 세 목록이라는 점. `content/`는 `collections_dir`이며 이름에 밑줄을 붙이면 `_posts`가 조용히 유실된다는 경고를 함께 적는다.
4. **글 추가 방법** — 세 종류별로 파일을 어디에 어떤 이름으로 만들고 front matter에 무엇을 넣는지. 02-PLAN의 스키마 표를 그대로 싣는다. 필수/선택 구분을 명시한다.
5. **주소 규칙** — 세 종류의 permalink와, 기존 사이트 주소 호환을 위해 슬러그를 바꾸면 안 된다는 점.
6. **스타일 규칙** — 색은 `_sass/_tokens.scss`의 CSS 커스텀 프로퍼티만 쓴다. 템플릿에 인라인 스타일과 리터럴 hex를 넣지 않는다. 새 색이 필요하면 토큰을 먼저 추가한다.
7. **디자인 원본** — Claude Design 프로젝트 `73d527ff-67e3-41c5-8af1-2401d3b37e1c`의 `Junyeong Site.dc.html`이 시각 기준이며 `DesignSync`로 읽을 수 있다는 점.
8. **하지 말 것** — 목록을 템플릿에 하드코딩하지 않는다. 글 본문을 HTML로 옮기지 않는다. npm 빌드 툴체인을 도입하지 않는다. `_site/`를 커밋하지 않는다.
9. **변경 후 검증 절차** — 빌드 → htmlproofer → 세 컬렉션 개수 대조 → 375/768/1280px 육안 확인.

### `CLAUDE.md`

`AGENTS.md`를 정본으로 가리키고, Claude Code에서만 의미 있는 내용을 덧붙인다.

- 첫 줄에서 `AGENTS.md`를 읽으라고 지시한다.
- 스펙 워크플로 문서가 `docs/specs/{TASK-ID}/`에 있다는 점.
- 응답 언어는 한국어.
- `content/` 아래의 콘텐츠 파일은 저자의 글이므로 요청 없이 문장을 고치지 않는다는 점.

두 문서에서 같은 내용을 중복 서술하지 않는다. 규칙의 정본은 `AGENTS.md` 한 곳이다.

## 완료 조건

- `AGENTS.md`에 적힌 명령을 그대로 실행했을 때 전부 동작한다.
- `AGENTS.md`의 디렉터리 지도가 실제 저장소 구조와 일치한다.
- front matter 스키마 표가 실제 템플릿이 읽는 키와 일치한다.

## 커밋

`docs: add AGENTS.md and CLAUDE.md for agentic development`
