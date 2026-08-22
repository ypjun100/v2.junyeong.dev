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
| `assets/` | CSS 진입점, 아바타 |
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
| `skills` | 선택 | 문자열 배열. 칩으로 표시 |
| `people` | 선택 | 문자열 배열 |
| `urls` | 선택 | `{type, name, url}` 배열. `type`은 `github`·`news`·`website`·`youtube`·`link` |
| `images` | 선택 | 경로 배열. 본문 위 갤러리로 표시 |
| `summary` | 선택 | 블로그와 동일 |

**수상 경력** — `content/_awards/<슬러그>.md`

`title`, `date`가 필수이고 `prize: {name, type}`가 추가된다. `prize.name`은 헤더 메타에 강조색으로 표시된다. `people`, `urls`, `images`, `summary`는 프로젝트와 같다.

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

## 하지 말 것

- 목록을 템플릿에 하드코딩하지 않는다. 목록은 항상 컬렉션에서 나온다.
- 글 본문을 HTML로 옮기지 않는다.
- npm이나 번들러 같은 빌드 툴체인을 도입하지 않는다.
- `_site/`를 커밋하지 않는다.

## 변경 후 확인

1. `bundle exec jekyll build --strict_front_matter`가 경고 없이 통과한다.
2. `htmlproofer`가 통과한다.
3. 세 컬렉션의 파일 개수와 `_site/posts`·`_site/project`·`_site/prize`의 페이지 개수가 일치한다. `collections_dir` 설정이 어긋나도 빌드는 성공하므로 이 대조가 유일한 방어선이다. 배포본 기준 개수는 `git ls-files content/_posts | wc -l`로 센다. 로컬에는 `.gitignore`로 제외한 작성 중인 글이 섞여 있다.
4. 375px, 768px, 1280px에서 Home·About·Posts·글 상세를 눈으로 확인한다.
