# TASK 03 — 콘텐츠 이관

## 목표

블로그 19편, 프로젝트 10편, 수상 경력 6편과 이미지 에셋을 v2 저장소로 옮기고 front matter를 02-PLAN의 스키마로 정규화한다.

## 선행

TASK 01.

## 작업

### 블로그 (19편)

1. `~/project/blog.junyeong.dev/_posts/*.md` 21개 중 작성이 끝난 19개를 `content/_posts/`로 복사한다. 파일명(`YYYY-MM-DD-<slug>.md`)을 바꾸지 않는다. 기존 주소가 슬러그에 묶여 있다.
2. `pin`, `math`, `mermaid`, `image`를 제거한다. `title`, `date`, `categories`, `tags`만 남긴다. `image`는 Chirpy의 대표 이미지 필드로 v2에서는 쓰지 않는다.
3. 본문에서 Chirpy 전용 문법(`{: .prompt-tip }`, `{: .prompt-warning }` 등)을 제거한다. 이 지시자는 바로 위 인용문에 붙는 것이라 줄만 지우면 일반 인용문이 된다. 지시자가 인용문 안에 `> {: .prompt-info }` 형태로 들어간 경우도 있으므로 두 형태를 모두 잡는다.
4. `<s>`를 형광펜으로 바꾸는 인라인 `<style>` 블록을 제거한다. `s` 스타일은 `_post.scss`가 한 번만 정의한다.
5. `~/project/blog.junyeong.dev/imgs/`를 `imgs/`로 복사한다. 본문이 `/imgs/YYYY-MM-DD/...` 형태로 참조하므로 경로 구조를 그대로 유지한다.

저자가 아직 쓰고 있는 두 편은 저장소에 넣지 않는다. `2026-03-21-FSD.md`와 `2026-04-25-생애-첫-미국-여행기-2.md`이며, 워킹 트리에는 두고 `.gitignore`로 제외해 로컬에서만 미리 볼 수 있게 한다. 글이 완성되면 `.gitignore`의 해당 줄을 지우는 것으로 공개된다.

### 프로젝트 (10편)

1. `~/project/junyeong.dev/_posts/project/*.md`를 `content/_projects/`로 복사한다. `.blank`는 옮기지 않는다.
2. 파일명 `YYYY-M-D-<slug>.md`에서 날짜 접두사를 떼어 `<slug>.md`로 바꾸고, 뗀 날짜를 `date: YYYY-MM-DD` front matter로 넣는다. 슬러그는 기존 주소(`/project/turtlemq` 등)와 정확히 일치해야 한다.
3. `layout`, `categories` 줄을 제거한다. `_config.yml` 기본값이 대신한다.
4. `skills[]`를 이름만 담은 평탄한 문자열 배열로 바꾼다. `color`, `logoColor`, `logoName`은 버린다.
5. `carousels[].images[].image`를 `images: [경로, ...]` 평탄 배열로 바꾼다.
6. 본문 첫 줄의 `{% include carousel.html ... %}` 호출을 제거한다. 갤러리는 레이아웃이 렌더링한다.
7. `desc`, `urls`, `people`은 그대로 둔다.

### 수상 경력 (6편)

`content/_awards/`로 복사한 뒤 프로젝트와 동일한 변환을 적용한다. 추가로 `prize: { name, type }`을 그대로 유지하고, 주석 처리된 `carousels` 블록과 `{% include carousel.html %}` 주석은 삭제한다.

### 이미지

`~/project/junyeong.dev/imgs/project/`와 `imgs/prize/`를 `imgs/` 아래 같은 구조로 복사한다. `.DS_Store`는 옮기지 않는다.

## 검증

- `content/_posts` 19개, `content/_projects` 10개, `content/_awards` 6개.
- 슬러그 대조 — `content/_projects`의 파일명 10개가 `lawy, turtlemq, recap, wavetimer, gomoku-ai, receipt, tape, reminder, spinmaze, doosong`와 일치한다.
- `bundle exec jekyll build --strict_front_matter` 성공. 빌드 후 `_site/posts` 19개, `_site/project` 10개, `_site/prize` 6개를 센다. `collections_dir` 설정이 잘못되면 빌드는 성공하면서 목록만 비므로 개수 확인이 유일한 방어선이다.
- 본문에서 참조하는 모든 `/imgs/...` 경로가 실제 파일로 존재한다.

이 문서는 이관 시점의 기록이다. 이후 저자가 프로젝트 4편(Receipt, TAPE, SPINMAZE, 두송중학교 앱)과 수상 경력 2편(2024 사회문제해결 자원봉사 해커톤, 2023 캡스톤디자인 및 AI 해커톤 경진대회)을 지웠으므로 현재 저장소의 개수는 여기 적힌 값과 다르다.

## 커밋

이관 단위로 세 번에 나눈다.

- `content: migrate 19 blog posts from blog.junyeong.dev`
- `content: migrate 10 projects and 6 awards from junyeong.dev`
- `content: migrate image assets for posts, projects, and awards`
