# TASK 04 — Home과 About

## 목표

시안의 Home / About 화면을 구현한다. 프로젝트·수상 경력 목록은 컬렉션에서 읽고, 소개·기술 스택·활동 이력 같은 고정 문구는 템플릿에 직접 적는다.

## 선행

TASK 02, TASK 03.

## 작업

1. `_includes/intro-block.html` — Home과 About이 공유하는 상단 블록을 분리한다. 대표 문구와 지표 2칸이 들어간다. 두 화면에 똑같이 나오는 유일한 덩어리라서 include로 뺀다.
   - 시안 최상단의 `NOW - 에듀테크 기업에서 근무 중` 배지는 구현하지 않는다. 초록 점과 링 효과도 함께 뺀다. 대표 문구가 블록의 첫 요소가 된다.
   - 대표 문구 끝의 마침표는 강조색(`--accent`)이므로 `<span>`으로 감싼다.
   - 지표는 `경력`과 `관심 분야` 2칸이고 라벨이 값 위에 온다. 시안의 `주요 스택` 칸은 두지 않는다. 경력 값은 `_config.yml`의 `career_start`에서 계산하며 02-PLAN의 「파생 값」을 따른다.
2. `index.html` (Home)
   - `intro-block` include
   - 소개 문단 2개. 안에 `<a>`가 섞여 있어 템플릿에 그대로 적는다.
   - `최근 글` 섹션 — `site.posts | limit: 5`. 각 항목은 `YYYY.MM.DD`, 카테고리, 제목, 발췌 90자.
   - 섹션 헤더 우측에 `/posts/`로 가는 `전체 보기 →`
3. `about.html` — 섹션은 `경력`, `기술 스택`, `프로젝트`, `수상 경력` 순이다. 시안의 `활동` 섹션은 두지 않는다.
   - `intro-block` include
   - `경력` — 프로젝트·수상 경력과 달리 컬렉션이 아니라 마크업에 직접 적는 고정 문구다. 한 건뿐이라 스키마로 묶을 반복이 없다.
     - `.career__role` — `.career__company`와 `.career__position`을 한 줄에 둔 `.career__heading`, 그 아래 `.career__period`, 그 아래 `.career__lead` 요약 문단.
     - `.career__items` — 성과 3건. 각 `.career-item`은 `.career-item__title`과 바로 뒤의 `.career-item__points` 목록이다.
     - 항목 제목 앞의 강조색 삼각형은 타이핑하지 않고 그린다. 두 웹폰트 모두 U+25B8을 갖고 있지 않다. 프로젝트 본문의 `h3`가 같은 마커를 쓴다.
     - `.career-item__points`의 크기·행간·항목 간격은 프로젝트 본문 `개발 내용` 불릿과 같은 값이다. 파일이 갈라져 있어 한쪽만 고치면 어긋난다.
   - `기술 스택` — 칩 7개(Node.js, Express.js, Nest.js, React.js, MongoDB, Docker, Git)를 마크업에 직접 적는다.
   - `프로젝트` — `site.projects | sort: 'date' | reverse`. 각 행은 이름(min-width 96px) + `desc`, 상세 주소로 링크.
   - `수상 경력` — `site.awards | sort: 'date' | reverse`. 각 행은 `YYYY.MM.DD`(min-width 78px) + 제목 + `prize.name` 배지.
4. `_sass/_home.scss`, `_sass/_about.scss` — 시안 인라인 스타일을 클래스로 옮긴다. 섹션 라벨(11.5px / 600 / 0.14em / uppercase / border-bottom)은 두 화면과 Posts가 공유하므로 `_layout.scss`의 공용 클래스로 뺀다.
5. 좁은 화면 대응 — 지표 박스, 프로젝트 행, 수상 경력 행의 640px 미만 스택 처리를 02-PLAN대로 구현한다.

## 완료 조건

- About의 프로젝트 목록과 수상 경력 목록이 폴더 내용과 정확히 일치한다. 이관 당시 각각 10편과 6편이었고 이후 저자가 지워 지금은 6편과 4편이다.
- 두 목록의 모든 항목이 상세 페이지로 이동한다.
- Home 최근 글 5편이 최신순으로 나오고 발췌가 HTML 태그 없이 표시된다.
- 소개 블록이 Home과 About에서 한 벌의 마크업으로 렌더링된다.
- 시안과 나란히 두었을 때 색·자간·간격이 일치한다.

이 문서는 구현 이후의 변경을 반영해 고쳤다. 원래 작업에서는 지표가 3칸이었고, `활동` 섹션이 있었으며, `경력` 섹션은 없었다. 소개 문단의 `<strong>` 강조도 이후 저자가 뺐다.

## 커밋

`feat: implement home and about pages from collections`
