# AGENTS.md

윤준영의 포트폴리오 겸 기술 블로그입니다. Jekyll 4로 만든 정적 사이트이며, 프로젝트·수상 경력·블로그 글이 모두 `content/` 아래의 마크다운 파일에서 나옵니다.

## 명령어

```bash
bundle install                                    # 의존성 설치
bundle exec jekyll serve                          # 로컬 서버 (127.0.0.1:4000)
bundle exec jekyll build --strict_front_matter    # 빌드. front matter 오류를 실패로 만든다
bundle exec htmlproofer _site --disable-external --allow-hash-href --ignore-missing-alt
```

`--ignore-missing-alt`는 기존 글의 이미지 상당수에 alt가 없기 때문에 붙인다. 검사 목적은 깨진 링크와 이미지 참조를 잡는 것이다.

## 디렉터리

| 경로 | 역할 |
| --- | --- |
| `content/_posts/` | 블로그 글. 파일명 `YYYY-MM-DD-<슬러그>.md` |
| `content/_projects/` | 프로젝트. 파일명 `<슬러그>.md` |
| `content/_awards/` | 수상 경력. 파일명 `<슬러그>.md` |
| `_layouts/` | `default`(셸), `page`(Home·About·Posts), `post`(글 3종 공용) |
| `_includes/` | 사이드바, 소개 블록, 글 상세 부속 조각 |
| `_sass/` | `_tokens.scss`가 색·타이포를 정의하고 나머지가 소비한다 |
| `assets/` | CSS 진입점, 아바타, 자체 호스팅 폰트 |
| `script/` | 폰트 서브셋 생성 스크립트. 사이트 빌드와는 무관하다 |
| `imgs/` | 글이 참조하는 이미지 |
| `docs/specs/` | 작업 스펙. 사이트에는 배포되지 않는다 |

`content/`는 `_config.yml`의 `collections_dir`다. **이 이름에 밑줄을 붙이면 안 된다.** Jekyll은 소스 트리를 훑을 때 밑줄로 시작하는 항목을 건너뛰므로, `_content`로 바꾸면 `_projects`와 `_awards`는 정상 생성되는 반면 `content/_posts`의 글이 전부 사라진다. 빌드는 성공하고 경고도 나오지 않는다.

## 글 추가하기

세 폴더에 파일을 하나 만들면 목록과 상세 페이지가 자동으로 생긴다. 템플릿은 건드리지 않는다.

**블로그** — `content/_posts/YYYY-MM-DD-<슬러그>.md`

| 키 | 필수 | 설명 |
| --- | --- | --- |
| `title` | 필수 | 글 제목 |
| `date` | 선택 | 없으면 파일명 날짜를 쓴다 |
| `categories` | 선택 | 헤더 메타에 표시 |
| `tags` | 선택 | 본문 하단 태그 칩 |
| `summary` | 선택 | 문자열 배열. 있을 때만 요약 콜아웃이 그려진다 |

**프로젝트** — `content/_projects/<슬러그>.md`

| 키 | 필수 | 설명 |
| --- | --- | --- |
| `title` | 필수 | 프로젝트 이름 |
| `date` | 필수 | `YYYY-MM-DD`. About 목록 정렬 기준 |
| `desc` | 필수 | About 목록과 헤더 메타에 쓰이는 한 줄 설명 |
| `skills` | 선택 | 문자열 배열. 헤더의 `기술 스택` 행에 ` · `로 이어 표시 |
| `urls` | 선택 | `{name, url}` 배열. 헤더의 `링크` 행. `type`은 지금 쓰이지 않는다 |
| `images` | 선택 | 경로 배열. 헤더 아래. 1장이면 그냥 이미지, 2장 이상이면 캐러셀 |
| `summary` | 선택 | 블로그와 동일 |

**수상 경력** — `content/_awards/<슬러그>.md`

`title`, `date`가 필수이고 `prize: {name, type}`가 추가된다. `prize.name`은 헤더의 `수상` 행에 나온다. `urls`, `images`, `summary`는 프로젝트와 같다. `desc`와 `skills`는 쓰지 않는다.

**프로젝트와 수상 경력 본문의 구조가 스타일과 맞물려 있다.** 시안이 요구하는 두 덩어리를 마크다운 구조에서 그대로 읽어 내기 때문이다.

- `## 설명` 바로 아래에 `>` 인용문을 두면 강조색 세로선이 붙은 개요 블록이 된다. 판정은 `h2:has(+ blockquote)`로 하므로 제목 문구는 자유롭지만 **인용문이 h2 바로 다음에 와야** 한다.
- 그 밖의 `##`는 구분선이 있는 섹션 라벨이 된다.
- `###`는 앞에 강조색 삼각형이 붙는 항목 제목이 되고, **바로 뒤의 `*` 목록**이 그 항목의 불릿으로 스타일링된다.

이 구조를 벗어나면 글이 깨지지는 않지만 시안과 다르게 보인다. 블로그 글에는 적용되지 않으며 일반 제목 크기를 그대로 쓴다.

강조는 세 컬렉션 모두 `**굵게**`로 쓴다. About의 경력 항목과 같은 스타일(`--text-mid` / 600)로 나온다. 형광펜은 없다. 이관 당시 블로그 글은 `<s>`를 형광펜으로 쓰고 있었고 `s`·`mark`에 배경색 스타일이 있었으나, 한 문단에 강조 방식이 여럿 생기는 것을 피해 전부 `**굵게**`로 합쳤다. 지금 `<s>`는 스타일이 없어 본래 뜻인 취소선으로 나온다.

프로젝트·수상 경력 본문에서는 백틱도 쓰지 않는다. 이 두 컬렉션에서 백틱으로 감싼 것들은 코드가 아니라 제품명·용어 강조였다. 블로그 글은 코드를 실제로 다루므로 이 제약을 받지 않는다.

**작성 중인 글** — 아직 공개하지 않을 글은 `content/_posts/`에 그대로 두고 `.gitignore`에 경로를 적는다. 로컬 `jekyll serve`에서는 보이지만 저장소와 배포본에는 들어가지 않는다. 공개할 때 `.gitignore`에서 그 줄을 지운다. 이 때문에 워킹 트리의 글 수가 저장소의 글 수보다 많을 수 있다.

## 주소

| 종류 | 주소 |
| --- | --- |
| 블로그 글 | `/posts/<슬러그>/` |
| 프로젝트 | `/project/<슬러그>` |
| 수상 경력 | `/prize/<슬러그>` |
| 화면 | `/`, `/about/`, `/posts/` |

기존 `junyeong.dev`와 `blog.junyeong.dev`에서 넘어온 주소다. **기존 글의 파일명을 바꾸면 외부에 걸린 링크가 깨진다.**

## 스타일

색과 서체는 `_sass/_tokens.scss`의 CSS 커스텀 프로퍼티로만 다룬다. 템플릿에 인라인 스타일을 넣지 않고, SCSS에 리터럴 hex를 쓰지 않는다. 새 색이 필요하면 토큰을 먼저 추가한다.

시각 기준은 Claude Design 프로젝트 `73d527ff-67e3-41c5-8af1-2401d3b37e1c`의 `Junyeong Site.dc.html`이며 `DesignSync` 도구로 읽을 수 있다. 시안에 없는 화면 폭 대응은 `_sass/_layout.scss`의 900px·640px 브레이크포인트를 따른다.

## 폰트

폰트는 `assets/fonts/`에서 자체 호스팅한다. Google Fonts는 쓰지 않는다. `_sass/_fonts.scss`는 생성 파일이므로 직접 고치지 않는다.

서브셋을 다시 만들어야 하는 경우는 두 가지다. **템플릿에 새 한글 라벨을 추가했을 때**, 그리고 **폰트나 웨이트를 바꿨을 때**다. 글을 추가할 때는 다시 만들 필요가 없다 — 본문용 폰트는 현대 한글 음절 전체를 담고 있다.

```bash
python3 -m venv .venv && .venv/bin/pip install fonttools brotli
.venv/bin/python script/build-fonts.py
```

원본 TTF는 스크립트가 내려받고 저장소에 넣지 않는다. 생성물인 `assets/fonts/*.woff2`와 `_sass/_fonts.scss`는 커밋한다.

본문용 폰트는 `unicode-range`로 두 파일로 나뉜다. KS X 1001 상용 2,350자는 항상 받고, 나머지 8,822자는 그 글자가 페이지에 나올 때만 받는다. 그래서 어떤 글자도 폴백으로 떨어지지 않는다.

UI 폰트(IBM Plex Sans KR)는 그 서체가 실제로 그리는 29자로만 잘려 있다. 대상은 사이드바 전체와 `section-label`·`section-head__more`·`intro__stat-label`·`chip` 요소이며, 스크립트가 이 클래스들만 훑는다. 본문은 `--font-content`로 그려지므로 글 내용이나 경력 설명 같은 긴 한글은 여기 들어가지 않는다.

**UI 영역에 새 한글 라벨을 넣고 스크립트를 돌리지 않으면 그 글자만 조용히 다른 서체로 렌더링된다.** 스크립트가 서브셋 글자 수를 출력하니 값이 늘었는지 확인한다.

라벨을 Liquid로 출력하는 경우(`{{ site.title }}` 등)는 템플릿에 리터럴이 없어 스크래핑에 잡히지 않는다. `UI_CONFIG_KEYS`에 해당 `_config.yml` 키를 추가해야 한다. 새 UI 클래스를 만들었다면 `UI_ELEMENT_PATTERNS`에도 추가한다.

## 하지 말 것

- 목록을 템플릿에 하드코딩하지 않는다. 목록은 항상 컬렉션에서 나온다.
- 글 본문을 HTML로 옮기지 않는다.
- npm이나 번들러 같은 빌드 툴체인을 도입하지 않는다. `script/build-fonts.py`는 사이트 빌드가 아니라 에셋 준비용이며 배포 경로에 들어가지 않는다.
- `_site/`를 커밋하지 않는다.

## 변경 후 확인

1. `bundle exec jekyll build --strict_front_matter`가 경고 없이 통과한다.
2. `htmlproofer`가 통과한다.
3. 세 컬렉션의 파일 개수와 `_site/posts`·`_site/project`·`_site/prize`의 페이지 개수가 일치한다. `collections_dir` 설정이 어긋나도 빌드는 성공하므로 이 대조가 유일한 방어선이다. 배포본 기준 개수는 `git ls-files content/_posts | wc -l`로 센다. 로컬에는 `.gitignore`로 제외한 작성 중인 글이 섞여 있다.
4. 375px, 768px, 1280px에서 Home·About·Posts·글 상세를 눈으로 확인한다.
