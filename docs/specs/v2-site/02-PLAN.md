# 계획 — 포트폴리오 겸 블로그 사이트 v2

## 기술 스택과 제약

- Jekyll 4.x + GitHub Pages Actions 배포. GitHub Pages의 기본 Jekyll 빌더(3.9 고정)가 아니라 Actions에서 `bundle exec jekyll build`를 직접 돌려 최신 Jekyll과 임의 플러그인을 쓴다.
- 템플릿은 Liquid + 순수 HTML, 스타일은 SCSS(Jekyll 내장 Sass 처리), 스크립트는 프레임워크 없는 바닐라 JS. 빌드 툴체인(webpack, npm 등)을 추가하지 않는다.
- 시안(`Junyeong Site.dc.html`)은 인라인 스타일과 `sc-if` 조건 렌더링, 클라이언트 해시 라우팅으로 되어 있는 캔버스 산출물이다. 이를 그대로 옮기지 않고 서버 렌더링되는 실제 라우트로 재구성한다. 시안 최상위 컨테이너의 `position: absolute; left: 423px; top: 12px`는 캔버스 배치용이므로 제거한다.

### 시안 원본 접근

implement 단계에서 원본이 다시 필요하면 `DesignSync` 도구로 읽는다.

- `projectId`: `73d527ff-67e3-41c5-8af1-2401d3b37e1c`
- 주 파일: `Junyeong Site.dc.html`
- 아바타 이미지: `-joel-_2-3--msbu9nju-vxof.png`

## 저장소 구조

```
.
├── _config.yml
├── Gemfile
├── CNAME                        # v2.junyeong.dev
├── .github/workflows/pages.yml
├── AGENTS.md
├── CLAUDE.md
├── content/                     # collections_dir. 글 3종이 여기 모인다
│   ├── _posts/                  # 블로그 19편 (+ 작성 중 2편은 .gitignore)
│   ├── _projects/               # 프로젝트 6편
│   └── _awards/                 # 수상 경력 4편
├── _layouts/
│   ├── default.html             # <html> 셸 + 사이드바 + 본문 슬롯 + 푸터
│   ├── page.html                # Home/About/Posts 공용
│   └── post.html                # 블로그·프로젝트·수상 공용 상세
├── _includes/
│   ├── head.html
│   ├── sidebar.html             # 아바타 · 이름 · 직함 · 화면 이동 · 외부 링크
│   ├── intro-block.html         # 대표 문구 · 지표 2칸 (Home/About 공용)
│   ├── post-meta.html           # 날짜 · 읽기 시간 · 카테고리
│   ├── post-summary.html        # 요약 콜아웃 (front matter에 summary가 있을 때만)
│   ├── post-header-meta.html    # 기술 스택 · 수상 · 링크 라벨 그리드
│   ├── carousel.html            # 스크롤 스냅 이미지 캐러셀
│   └── post-tags.html
├── _sass/
│   ├── _tokens.scss             # CSS 커스텀 프로퍼티 전체
│   ├── _base.scss               # reset, 타이포, a/::selection
│   ├── _layout.scss             # 셸 그리드, 사이드바, 반응형 브레이크포인트
│   ├── _home.scss
│   ├── _about.scss
│   ├── _post-list.scss          # Posts 목록
│   └── _post.scss               # 글 상세
├── assets/
│   ├── css/main.scss
│   ├── js/nav.js                # 현재 경로 기준 nav 활성 표시 보조
│   └── img/avatar.png
├── imgs/                        # 글이 참조하는 이미지 (기존 경로 유지)
├── index.html                   # Home
├── about.html                   # About
└── posts.html                   # Posts (permalink: /posts/)
```

## 콘텐츠 모델

### 컬렉션 구성

글 3종은 `collections_dir: content` 아래에 모은다. `content/_posts`는 Jekyll 내장 포스트를 그대로 쓴다. 파일명 날짜 접두사에서 날짜가 파싱되고 `site.posts`가 최신순으로 정렬되어 나온다.

`content/_projects`와 `content/_awards`는 `_config.yml`의 `collections`로 선언한다. 컬렉션은 파일명에서 날짜를 파싱하지 않으므로 이관 시 front matter에 `date`를 명시적으로 넣는다.

**상위 폴더 이름은 밑줄로 시작하면 안 된다.** Jekyll 4.3.3에서 확인한 동작이다. `collections_dir`를 `_content`처럼 두면 `_projects`·`_awards`는 정상 생성되지만 `_posts`가 통째로 유실된다. 빌드는 성공하고 경고도 나오지 않는다. `entry_filter.rb`의 `SPECIAL_LEADING_CHAR_REGEX`가 `_`로 시작하는 항목을 디렉터리 순회에서 제외하는데, 컬렉션은 `collections_path`로 직접 읽혀 살아남는 반면 포스트는 순회를 타기 때문이다.

`content/`는 밑줄이 없지만 `_site`로 복사되지 않는다. Jekyll이 `collections_dir`를 출력 대상에서 자동으로 제외한다. `_layouts`, `_includes`, `_sass`는 컬렉션이 아니므로 루트에 남는다.

```yaml
collections_dir: content

collections:
  projects:
    output: true
    permalink: /project/:name
  awards:
    output: true
    permalink: /prize/:name

defaults:
  - scope: { path: "", type: posts }
    values: { layout: post, kind: blog }
  - scope: { path: "", type: projects }
    values: { layout: post, kind: project }
  - scope: { path: "", type: awards }
    values: { layout: post, kind: award }
```

`kind`는 `post.html` 하나가 세 종류를 분기 렌더링하는 데 쓰는 키다.

### 주소 체계

기존 두 사이트의 주소를 그대로 유지한다.

| 종류 | 주소 | 출처 |
| --- | --- | --- |
| 블로그 글 | `/posts/:title/` | `blog.junyeong.dev`의 Chirpy 기본값 |
| 프로젝트 | `/project/:name` | `junyeong.dev`의 `permalink: /:categories/:title` |
| 수상 경력 | `/prize/:name` | 위와 동일 |
| Home / About / Posts | `/`, `/about/`, `/posts/` | 신규 |

`:name`은 파일명에서 확장자와 날짜 접두사를 뺀 값이다. 이관 시 파일명을 기존 주소의 슬러그와 일치시킨다.

### Front matter 스키마

**블로그 (`content/_posts/YYYY-MM-DD-<slug>.md`)** — 원본 Chirpy 형식을 유지하고 선택 필드만 더한다.

```yaml
title: string            # 필수
date: YYYY-MM-DD HH:MM:SS +0900   # 선택. 없으면 파일명 날짜를 쓴다
categories: [string]     # post 헤더 메타에 첫 항목 표시
tags: [string]           # 하단 태그 칩
summary: [string]        # 선택. 있을 때만 요약 콜아웃 렌더링
```

블로그 글에는 대표 이미지 필드를 두지 않는다. 본문 안의 이미지만 쓰므로 글 목록과 상세 어디에도 썸네일이 나오지 않고, `jekyll-seo-tag`는 `og:image`를 생성하지 않는다.

**프로젝트 (`content/_projects/<slug>.md`)**

```yaml
title: string            # 필수
date: YYYY-MM-DD         # 필수 (이관 시 파일명 날짜에서 채움)
desc: string             # About 목록의 한 줄 설명
urls:                    # 선택. type은 github|news|website|link|youtube
  - { type: github, name: Github, url: https://... }
skills: [string]         # 선택. 헤더의 기술 스택 행
images: [string]         # 선택. 기존 carousels[].images[].image를 평탄화한 경로 배열
summary: [string]        # 선택
```

**수상 경력 (`content/_awards/<slug>.md`)**

```yaml
title: string            # 필수
date: YYYY-MM-DD         # 필수
prize:                   # 필수
  name: string           # 우수상, 대상, 총장상, 장관상
  type: gold|silver|bronze
urls: [...]              # 선택. 프로젝트와 동일 형식
images: [string]         # 선택
summary: [string]        # 선택
```

`skills`에서 `color`/`logoColor`/`logoName`은 img.shields.io 뱃지 전용 필드였으므로 이관 시 버리고 `name`만 남긴다. 칩은 사이트 자체 스타일로 그린다.

### 파생 값

- **읽기 시간** — 어절이 아니라 글자 수로 센다. 한국어는 어절 하나에 담기는 의미가 영어 단어보다 커서 어절 기준으로 재면 실제보다 훨씬 빠르게 나온다. `content | strip_html | strip_newlines | size`를 분당 500자로 나누고 1을 더해 올림과 1분 하한을 동시에 처리한다. `strip_html`을 빼면 HTML 태그까지 세어 값이 부풀려진다.
- **Home 최근 글 발췌** — `post.excerpt | strip_html | strip_newlines | truncate: 90`.
- **경력 연차** — 시작일을 1년차로 두고 기념일마다 올라간다. 곧 완료 연수 + 1이며, 표기는 `년차`가 아니라 `년`이다. 시작일은 `_config.yml`의 `career_start` 한 곳에 있고 Liquid와 스크립트가 같이 읽는다.

  `site.time`은 빌드 시각이라 방문 시점과 다르다. 그래서 서버에서 렌더한 값은 비어 보이지 않게 하는 기본값이고, 실제 표시는 인라인 스크립트가 읽는 사람의 시계로 다시 계산한다. 정기 재빌드는 두지 않는다.

  Liquid의 `if`는 조건 안의 필터 체인을 평가하지 못한다. `{% if site.time | date: "%m%d" | plus: 0 < start %}`처럼 쓰면 조건이 평가되지 않고 분기가 항상 실행되어 기념일 이후 값이 1년씩 적게 나온다. 비교할 값은 먼저 `assign`한다.
- **Posts 연도 그룹** — `site.posts | group_by_exp: "p", "p.date | date: '%Y'"`, 연도 내림차순.

## 고정 문구의 위치

프로필, 소개, 기술 스택, 활동 이력은 마크다운이 아니라 사람이 직접 고치는 고정 문구다. 이 문구들은 데이터 파일을 거치지 않고 템플릿에 그대로 적는다. 문구 안에 `<strong>`, `<br>`, `<a>` 마크업이 섞여 있어 템플릿에 있을 때 가장 읽고 고치기 쉽다.

같은 문구가 두 화면에 나오는 경우만 `_includes`로 뺀다. 중복 제거는 include가 담당하고, 그 위에 별도의 데이터 계층을 두지 않는다.

| 문구 | 적히는 곳 | 나오는 화면 |
| --- | --- | --- |
| 아바타, 이름, 직함, 화면 이동, 외부 링크 | `_includes/sidebar.html` | 전체 |
| 대표 문구, 지표 2칸 | `_includes/intro-block.html` | Home, About |
| 소개 문단 2개 | `index.html` | Home |
| 경력 1건과 성과 3건 | `about.html` | About |
| 기술 스택 칩 | `about.html` | About |

사이트 제목, 설명, 저자, 이메일은 `_config.yml`에 둔다. SEO 태그와 피드 플러그인이 그곳에서 읽어 가므로 템플릿과는 소비자가 다르다. 사이드바에서 이름과 이메일을 쓸 때는 `site.author`를 참조해 `_config.yml`과 어긋나지 않게 한다.

## 디자인 토큰

`_sass/_tokens.scss`에 CSS 커스텀 프로퍼티로 정의하고 모든 스타일이 이 값만 참조한다. 값은 시안에서 추출한 그대로다.

| 토큰 | 값 | 용도 |
| --- | --- | --- |
| `--bg` | `#0e1117` | 페이지 배경 |
| `--surface` | `#11151c` | 요약 콜아웃, 코드 블록 배경 |
| `--code-bg` | `#171c24` | 인라인 코드 배경 |
| `--border` | `#1e242e` | 구분선, 카드 테두리 |
| `--border-strong` | `#232a35` | 칩 테두리 |
| `--border-footer` | `#1a202a` | 푸터 상단선, 경력 성과 구분선 |
| `--border-divider` | `#2a323e` | 지표 행 세로 구분선 |
| `--text` | `#b3bcc8` | 본문 기본 |
| `--text-strong` | `#eaeff5` | 제목, 강조 |
| `--text-mid` | `#dbe2ea` | 목록 항목 제목, 지표 값 |
| `--text-soft` | `#aab3bf` | 읽는 텍스트 전반 — 글 본문, 소개 문단, 경력·프로젝트 불릿 |
| `--text-summary` | `#a7b0bc` | 요약 콜아웃 |
| `--text-chip` | `#9aa4b1` | 칩, 코드 블록 |
| `--text-list` | `#929ba8` | Posts 인트로 |
| `--muted` | `#6b7583` | 섹션 라벨, 보조 텍스트 |
| `--muted-dim` | `#5f6875` | 날짜, 메타 |
| `--muted-excerpt` | `#78818e` | Home 발췌 |
| `--muted-desc` | `#868f9c` | 프로젝트 설명 |
| `--muted-tag` | `#7b8492` | 글 하단 태그 |
| `--muted-footer` | `#4f5866` | 푸터 |
| `--sep` | `#3d4552` | 메타 구분점 |
| `--accent` | `#6fd88c` | 강조, 링크 |
| `--accent-hover` | `#9aebae` | 링크 호버 |
| `--accent-code` | `#9fe6b4` | 인라인 코드 글자 |
| `--accent-border` | `rgba(111,216,140,0.4)` | 개요 블록 세로선, 캐러셀 버튼 호버 |
| `--dot-idle` | `#2f3743` | 캐러셀 비활성 점 |
| `--font-ui` | `'IBM Plex Sans KR', sans-serif` | 사이드바, 지표 라벨 |
| `--font-content` | `'Nanum Myeongjo', serif` | 본문 전반, Home/About 제목 |
| `--font-post-title` | `'Nanum Myeongjo', serif` | 글 제목, heading |
| `--font-mono` | `'IBM Plex Mono', monospace` | 숫자·라틴만 있는 날짜, 코드 |
| `--font-mono-mixed` | `monospace` | 숫자와 한글이 한 줄에 같이 오는 메타 행 |
| `--tracking` | `0.015em` | 전역 자간 |

링크는 `text-decoration-color: rgba(111,216,140,0.45)`, `text-underline-offset: 3px`. `::selection`은 `background: rgba(111,216,140,0.28); color: #eef2f6`.

## 폰트 배송

폰트는 `assets/fonts/`에서 자체 호스팅하고 `script/build-fonts.py`가 서브셋을 생성한다. Google Fonts는 쓰지 않는다.

Google Fonts는 한글 패밀리를 유니코드 범위별 90~120개 조각으로 쪼개 서빙한다. 한국어 문장은 음절이 한글 영역 전체에 흩어져 있어서 한 페이지가 40개 가까운 파일을 외부 출처 두 곳에서 받아 온다. 자체 호스팅은 이를 웨이트당 파일 하나로 바꾸고, HTML을 이미 내려받은 같은 연결에서 처리한다.

서브셋은 역할에 따라 두 방식을 쓴다.

- **content** — `content/`의 글을 그리는 폰트. 어떤 글자가 나올지 미리 알 수 없으므로 현대 한글 음절 전체를 담고 `unicode-range`로 둘로 나눈다. 한국어 산문을 사실상 전부 덮는 KS X 1001 상용 2,350자는 항상 받고, 나머지 8,822자는 해당 글자가 페이지에 실제로 나올 때만 받는다. 그래서 누락되는 글자가 없다.
- **ui** — 사이드바와 몇몇 라벨만 그리는 폰트. 글자 집합이 확정되어 있어 그 글자로만 자른다. 스크립트는 `--font-ui`를 쓰는 클래스만 훑고, Liquid로 주입되는 값은 `_config.yml`에서 따로 읽는다. UI 영역에 새 한글 라벨을 추가하면 스크립트를 다시 돌려야 한다.

제목과 heading은 본문과 같은 Nanum Myeongjo를 쓴다. 그 덕에 모든 페이지가 동일한 6개 파일(847KB)만 쓰고, 첫 방문 이후에는 폰트 요청이 발생하지 않는다. Nanum Myeongjo는 400과 700만 제공하므로 글 제목은 시안의 900이 아니라 700이다.

IBM Plex Mono에는 한글이 없고 IBM Plex 계열에 Mono 한글판도 없다. 그래서 숫자와 한글이 한 줄에 같이 오는 메타 행은 IBM Plex Mono를 쓰지 않고 시스템 `monospace` 하나로 넘긴다. 섞어 쓰면 한 줄이 두 서체로 쪼개져 보인다. 숫자나 라틴만 있는 날짜와 코드 블록은 계속 IBM Plex Mono를 쓴다.

한국어 줄바꿈은 브라우저 기본값을 쓴다. `word-break`를 지정하지 않으므로 글자 단위로 끊긴다. `overflow-wrap: break-word`는 긴 URL이 컨테이너를 밀어내는 것만 막는다.

## 레이아웃과 반응형

기본 셸은 `max-width: 940px`, `padding: 76px 28px 110px`, 사이드바 `168px` + 본문 `flex: 1; max-width: 620px`, 둘 사이 `gap: 76px`. 사이드바는 `position: sticky; top: 76px`.

브레이크포인트는 세 단계로 둔다.

- **`>= 900px`** — 시안 그대로.
- **`< 900px`** — 사이드바를 본문 위로 올리고 `sticky` 해제. 아바타·이름·직함을 가로로 배치하고 화면 이동 링크를 가로 한 줄로 편다. 외부 링크도 가로 배치. 셸 `gap`을 `40px`로 줄인다.
- **`< 640px`** — 컨테이너 패딩 `48px 20px 72px`. Home/About 대표 문구 `40px → 28px`. 지표 박스는 세로 스택으로 바꾸고 `border-right` 대신 `border-bottom`을 쓴다. 수상 경력 행(날짜·제목·등급)은 세로 스택으로 바꿔 등급을 제목 아래에 둔다. 프로젝트 행도 이름·설명 세로 스택으로 바꾼다. 글 제목 `27px → 23px`, 본문 `16.5px → 16px`.

가로 스크롤 방지를 위해 코드 블록은 `overflow-x: auto`, 긴 URL 등에는 `overflow-wrap: anywhere`, 이미지는 `max-width: 100%`를 적용한다.

## 라우팅

시안의 해시 기반 SPA 전환은 실제 라우트로 대체한다. 사이드바 메뉴는 Home / About / Posts 세 개이며 각각 `/`, `/about/`, `/posts/`로 이동한다. 활성 상태는 Liquid에서 `page.url`을 비교해 결정하고, 상세 글에서는 `kind`가 `blog`이면 Posts가, `project`/`award`이면 About이 활성으로 보인다.

목록 `/posts/`와 개별 글 `/posts/:title/`은 같은 접두사를 공유하지만 충돌하지 않는다. `_site/posts/index.html`과 `_site/posts/<slug>/index.html`이 나란히 생성되며 Jekyll 4.3.3에서 경고가 나오지 않는 것을 확인했다.

`assets/js/nav.js`는 Liquid로 해결되지 않는 보조 동작만 담당한다. 현재는 좁은 화면에서의 사이드바 토글 정도이며, JS가 없어도 모든 콘텐츠가 읽히도록 만든다.

## `post.html` 렌더링 흐름

```
post.html                       kind == blog        kind == project / award
 ├─ 뒤로가기 링크               ← Posts             ← 프로젝트 / ← 수상 경력
 ├─ header
 │   ├─ h1                      page.title          page.title
 │   ├─ post__desc              —                   page.desc (project)
 │   ├─ post-meta.html          날짜·읽기시간·분류   —
 │   └─ post-header-meta.html   —                   기술 스택·수상·링크
 ├─ post-summary.html           page.summary 있을 때만
 ├─ carousel.html               —                   page.images 있을 때만
 ├─ post__body {{ content }}    일반 제목 크기       개요 블록 + 항목 섹션
 └─ post-tags.html              page.tags 있을 때만
```

프로젝트와 수상 경력은 블로그 글과 헤더가 다르다. 제목 아래에 `desc` 한 줄(프로젝트만)과 라벨/값 그리드가 오고, 그 아래 이미지 캐러셀이 붙는다. 그리드는 시안의 행별 grid 대신 하나의 grid로 만들어 라벨 열이 한 정의로 정렬되게 한다.

캐러셀은 스크롤 스냅 트랙이다. 스크립트가 transform을 소유하지 않으므로 JS가 없어도 좌우로 넘겨 볼 수 있고, 버튼과 점은 스크롤 위치를 움직이고 되비추기만 한다. 양 끝에서 감싸므로 첫 장에서 이전을 누르면 마지막으로 간다. 이미지가 한 장이면 트랙과 컨트롤 없이 이미지만 그린다.

높이는 고정하지 않는다. 시안의 290px + `object-fit: cover`는 스크린샷을 잘라냈다. 트랙은 가장 높은 이미지에 맞춰지고 각 이미지는 원본 비율을 유지한다.

버튼 화살표는 SVG로 그린다. `‹` `›` 글리프는 flex 중앙 정렬된 버튼에서 광학중심이 1.4px 아래에 놓여 처져 보인다.

프로젝트·수상 경력 본문의 강조는 `**굵게**`만 쓴다. `<mark>`(형광펜)와 백틱(코드 배경)을 섞으면 한 문단에 강조 방식이 세 가지가 되고, 이 두 컬렉션의 백틱은 코드가 아니라 용어 강조였다.

이후 이 규칙을 블로그 글까지 넓혔다. 이관해 온 글이 `<s>`를 형광펜으로 쓰고 있었는데 저자가 이 강조를 About의 강조와 같은 모양으로 맞추기로 해서, `<s>` 50개를 `**굵게**`로 바꾸고 `s`·`mark` 스타일과 그 배경색 토큰(`--accent-soft`)을 지웠다. 백틱 제약은 코드를 실제로 다루는 블로그 글에는 여전히 적용하지 않는다.

본문은 마크다운 구조를 그대로 읽어 시안의 두 덩어리를 만든다. `h2:has(+ blockquote)`로 개요 블록을, 나머지 `h2`로 섹션 라벨을, `h3`와 뒤따르는 목록으로 항목을 구성한다. 콘텐츠를 front matter로 옮기지 않아도 되고 문구를 문자열로 비교하지도 않는다. 이 규칙은 `.post--project`와 `.post--award`에만 걸리며 블로그 글은 일반 제목 크기를 유지한다.

헤더는 시안에 있는 행만 그린다. 프로젝트는 `기술 스택`과 `링크`, 수상 경력은 `수상`과 `링크`다. 시안의 `담당` 행과 기존 사이트의 참여자 표시는 두지 않으며, 대응하는 `role`·`people` 필드도 없다.

`content` 안의 마크다운은 `_post.scss`가 요소 선택자로 스타일링한다. 시안이 각 요소에 붙여 둔 인라인 스타일을 `h2`, `p`, `pre`, `code`, `ul`, `strong`, `em`, `blockquote`, `img`, `table` 선택자로 옮긴다. 기존 글이 `>` 인용을 자주 쓰므로 인용문은 반드시 다크 톤 스타일을 갖는다. `mark`도 처음에는 여기 있었으나 형광펜을 없애면서 함께 지웠다.

## 콘텐츠 이관

| 대상 | 원본 | 목적지 | 개수 |
| --- | --- | --- | --- |
| 블로그 글 | `~/project/blog.junyeong.dev/_posts/*.md` | `content/_posts/` | 21 |
| 블로그 이미지 | `~/project/blog.junyeong.dev/imgs/` | `imgs/` | 원본 경로 유지 |
| 프로젝트 | `~/project/junyeong.dev/_posts/project/*.md` | `content/_projects/` | 10 |
| 수상 경력 | `~/project/junyeong.dev/_posts/prize/*.md` | `content/_awards/` | 6 |
| 포트폴리오 이미지 | `~/project/junyeong.dev/imgs/{project,prize}/` | `imgs/{project,prize}/` | 원본 경로 유지 |

이관 시 각 파일에 적용할 변환:

- 프로젝트·수상: 파일명의 날짜 접두사를 `date` front matter로 옮기고 파일명은 슬러그만 남긴다. `layout`과 `categories` 줄은 `_config.yml` 기본값이 대신하므로 제거한다.
- 프로젝트·수상: `carousels[].images[].image`를 `images: [경로]` 배열로 평탄화하고, 본문의 `{% include carousel.html ... %}` 호출을 제거한다. 갤러리는 레이아웃이 그린다.
- 프로젝트: `skills[]`를 이름만 담은 평탄한 문자열 배열로 바꾼다. img.shields.io 뱃지용이던 `color`, `logoColor`, `logoName`은 버린다.
- 블로그: 19편 중 11편이 `<s>`를 형광펜으로 바꾸는 인라인 `<style>` 블록을 갖고 있다. 이 블록을 제거하고 `s` 스타일을 `_post.scss`에서 한 번만 정의한다. 본문 문장은 건드리지 않는다. (이후 형광펜 자체를 없애고 `<s>`를 `**굵게**`로 바꿨다. 「`post.html` 렌더링 흐름」 절에 경위를 적었다.)
- 블로그: `pin`, `math`, `mermaid` 등 Chirpy 전용 필드를 제거한다. Chirpy 전용 문법(`{: .prompt-tip }` 등)이 남아 있으면 인용문으로 바꾼다.
- 전체: 본문의 이미지 경로가 `/imgs/...` 절대 경로인지 확인하고 어긋난 것을 맞춘다.

## 검증 전략

정적 사이트라 단위 테스트 프레임워크를 두지 않는다. 대신 빌드 시점 검증을 자동화한다.

- `bundle exec jekyll build --strict_front_matter` — front matter 파싱 오류를 빌드 실패로 만든다.
- `bundle exec htmlproofer _site --disable-external` — 내부 링크와 이미지 참조 중 깨진 것을 잡는다. 외부 링크는 네트워크 의존성 때문에 CI에서 끈다.
- 개수 대조 — 빌드 후 `_site` 안의 `project/`, `prize/`, `posts/` 디렉터리 항목 수가 각 컬렉션의 파일 수와 일치하는지 확인한다. 배포본 기준 개수는 `git ls-files`로 센다.
- 반응형 육안 확인 — 375px, 768px, 1280px 폭에서 Home / About / Posts / 글 상세 네 화면.

CI 워크플로는 배포 전에 build와 htmlproofer를 순서대로 돌린다.

## 태스크 분할

| 파일 | 내용 |
| --- | --- |
| `03-TASK-01-scaffold.md` | Jekyll 뼈대, 의존성, 컬렉션·주소 설정, 로컬 실행 확인 |
| `03-TASK-02-design-system.md` | 토큰, 전역 스타일, 셸 레이아웃, 사이드바, 반응형 |
| `03-TASK-03-content-migration.md` | 마크다운 3종 + 이미지 이관 및 front matter 정규화 |
| `03-TASK-04-home-about.md` | Home, About, 두 화면 공용 소개 블록 |
| `03-TASK-05-blog-post.md` | Posts 목록, `post.html` 및 부속 include, 마크다운 본문 스타일 |
| `03-TASK-06-deploy.md` | CNAME, GitHub Pages Actions, 검증 단계 |
| `03-TASK-07-agent-docs.md` | `AGENTS.md`, `CLAUDE.md` |

01 → 02 → 03 순으로 진행한 뒤 04와 05를 잇고, 06과 07은 마지막에 붙인다. 04와 05는 03에 함께 의존하므로 03이 끝나기 전에는 실제 렌더링을 확인할 수 없다.
