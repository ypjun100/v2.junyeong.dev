# TASK 01 — Jekyll 뼈대

## 목표

빈 디렉터리에서 `bundle exec jekyll serve`가 뜨는 상태까지 만든다. 콘텐츠와 스타일은 아직 없다.

## 작업

1. `git init -b main`으로 저장소를 만들고 working branch `feature/v2-site-jekyll-portfolio`를 생성해 체크아웃한다.
2. `Gemfile` 작성.
   - `jekyll ~> 4.3`
   - `jekyll-feed`, `jekyll-seo-tag`, `jekyll-sitemap`
   - `:test` 그룹에 `html-proofer`
   - `webrick`(Ruby 3.x에서 `jekyll serve`에 필요)
3. `bundle install`로 `Gemfile.lock` 생성.
4. `_config.yml` 작성.
   - `title`, `description`, `author`, `lang: ko-KR`, `timezone: Asia/Seoul`
   - `url: https://v2.junyeong.dev`, `baseurl: ""`
   - `plugins` 목록
   - `collections_dir: content` — 밑줄로 시작하는 이름을 쓰면 `_posts`가 조용히 유실된다. 02-PLAN의 경고 참조
   - `collections`로 `projects`, `awards` 선언 (`output: true`, permalink는 02-PLAN 참조)
   - `defaults`로 세 종류에 `layout: post` 및 `kind` 부여
   - `permalink: /posts/:title/` (블로그)
   - `markdown: kramdown`, `highlighter: rouge`
   - `sass: { style: compressed }`
   - `exclude`에 `Gemfile*`, `README.md`, `docs/`, `vendor/`, `.github/`
5. `.gitignore` 작성 — `_site/`, `.jekyll-cache/`, `.jekyll-metadata`, `vendor/`, `.bundle/`, `.DS_Store`
6. 빈 골격 파일 배치 — `_layouts/default.html`, `_layouts/page.html`, `_layouts/post.html`, `_includes/head.html`, `assets/css/main.scss`(front matter 두 줄만), `index.html`, `about.html`, `posts.html`(`permalink: /posts/`). 각 파일은 자리만 잡고 최소 마크업만 넣는다.
7. `content/_posts/`, `content/_projects/`, `content/_awards/`, `_sass/`, `imgs/` 디렉터리를 만들고 빈 컬렉션이 빌드를 깨지 않는지 확인한다. 루트에 `_posts/`를 만들지 않는다. `collections_dir` 밖의 `_posts`는 `jekyll doctor`가 경고로 잡는다.

## 완료 조건

- `bundle exec jekyll build` 성공, 경고 없음.
- `bundle exec jekyll serve`로 `http://127.0.0.1:4000`에서 `/`, `/about/`, `/posts/` 세 경로가 200으로 응답한다.
- `_site/`가 커밋에 포함되지 않는다.

## 커밋

`chore: scaffold Jekyll project with collections and build config`
