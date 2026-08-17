# TASK 04 — Home과 About

## 목표

시안의 Home / About 화면을 구현한다. 프로젝트·수상 경력 목록은 컬렉션에서 읽고, 소개·기술 스택·활동 이력 같은 고정 문구는 템플릿에 직접 적는다.

## 선행

TASK 02, TASK 03.

## 작업

1. `_includes/intro-block.html` — Home과 About이 공유하는 상단 블록을 분리한다. 대표 문구와 지표 3칸이 들어간다. 두 화면에 똑같이 나오는 유일한 덩어리라서 include로 뺀다.
   - 시안 최상단의 `NOW - 에듀테크 기업에서 근무 중` 배지는 구현하지 않는다. 초록 점과 링 효과도 함께 뺀다. 대표 문구가 블록의 첫 요소가 된다.
   - 대표 문구 끝의 마침표는 강조색(`--accent`)이므로 `<span>`으로 감싼다.
   - 지표 3칸은 `2년 / 경력`, `Node · JS/TS / 주요 스택`, `Kubernetes / 관심 분야`.
2. `index.html` (Home)
   - `intro-block` include
   - 소개 문단 2개. `<strong>` 강조가 들어가므로 마크업 그대로 적는다.
   - `최근 글` 섹션 — `site.posts | limit: 5`. 각 항목은 `YYYY.MM.DD`, 카테고리, 제목, 발췌 90자.
   - 섹션 헤더 우측에 `/posts/`로 가는 `전체 보기 →`
3. `about.html`
   - `intro-block` include
   - `기술 스택` — 칩 7개(Node.js, Express.js, Nest.js, React.js, MongoDB, Docker, Git)를 마크업에 직접 적는다.
   - `프로젝트` — `site.projects | sort: 'date' | reverse`. 각 행은 이름(min-width 96px) + `desc`, 상세 주소로 링크.
   - `수상 경력` — `site.awards | sort: 'date' | reverse`. 각 행은 `YYYY.MM.DD`(min-width 78px) + 제목 + `prize.name` 배지.
   - `활동` — 시안의 4건(구름톤 유니브 2기 2024, UCLab 학부연구생 2023, 멋쟁이사자처럼 11기 2023, GDSC in SCH 2019)을 연도 + 기관명 + 불릿 목록 형태로 직접 적는다. UCLab 항목의 시연 영상 링크(`https://youtu.be/zasIZqjEoMA`)를 유지한다.
4. `_sass/_home.scss`, `_sass/_about.scss` — 시안 인라인 스타일을 클래스로 옮긴다. 섹션 라벨(11.5px / 600 / 0.14em / uppercase / border-bottom)은 두 화면과 Posts가 공유하므로 `_layout.scss`의 공용 클래스로 뺀다.
5. 좁은 화면 대응 — 지표 박스, 프로젝트 행, 수상 경력 행의 640px 미만 스택 처리를 02-PLAN대로 구현한다.

## 완료 조건

- About의 프로젝트 목록 10개, 수상 경력 목록 6개가 폴더 내용과 정확히 일치한다.
- 두 목록의 모든 항목이 상세 페이지로 이동한다.
- Home 최근 글 5편이 최신순으로 나오고 발췌가 HTML 태그 없이 표시된다.
- 소개 블록이 Home과 About에서 한 벌의 마크업으로 렌더링된다.
- 시안과 나란히 두었을 때 색·자간·간격이 일치한다.

## 커밋

`feat: implement home and about pages from collections`
