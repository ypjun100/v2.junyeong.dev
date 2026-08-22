# TASK 02 — 디자인 시스템과 셸 레이아웃

## 목표

시안의 색·타이포·간격을 토큰으로 고정하고, 모든 화면이 공유하는 셸(사이드바 + 본문 + 푸터)을 완성한다. 반응형 대응도 여기서 끝낸다.

## 선행

TASK 01.

## 작업

1. `_sass/_tokens.scss` — 02-PLAN의 토큰 표를 `:root` CSS 커스텀 프로퍼티로 그대로 옮긴다. 이후 모든 SCSS는 리터럴 색상값을 쓰지 않고 이 변수만 참조한다.
2. `_sass/_base.scss`
   - `html, body { margin: 0; padding: 0; background: var(--bg); }`, `* { box-sizing: border-box; }`
   - 전역 `color: var(--text)`, `font-family: var(--font-content)`, `letter-spacing: var(--tracking)`
   - 링크 기본/호버, `::selection`
   - `img { max-width: 100%; }`, `overflow-wrap: anywhere`
3. `_includes/head.html`
   - `<meta charset>`, viewport, `{% seo %}`, 피드 링크
   - `assets/fonts/`의 자체 호스팅 woff2 preload. 02-PLAN의 폰트 배송 절 참조
   - `assets/css/main.scss` 링크
4. `_includes/sidebar.html` — 아바타(46px 원형), 이름, 직함, Home / About / Posts 링크, 외부 링크(GitHub · LinkedIn · 이메일). 문구는 마크업에 직접 적는다. 이름과 이메일만 `site.author`를 참조해 `_config.yml`과 어긋나지 않게 한다. 활성 링크 판정은 `page.url`과 `page.kind` 기준.
5. `_layouts/default.html` — `<html lang="ko">` + head + 셸 컨테이너 + 사이드바 + `{{ content }}` + 푸터(`© {{ site.time | date: '%Y' }} Junyeong Yun`).
6. `_layouts/page.html` — `default`를 상속하고 본문 컬럼만 감싼다.
7. `_sass/_layout.scss` — 02-PLAN의 셸 치수와 세 브레이크포인트(`>= 900px`, `< 900px`, `< 640px`)를 구현한다. 시안 최상위의 `position: absolute; left: 423px; top: 12px`는 넣지 않는다.
8. `assets/css/main.scss` — front matter 두 줄 뒤에 `_sass` 파티션을 `@use`로 불러온다.
9. `assets/img/avatar.png` — 시안의 `-joel-_2-3--msbu9nju-vxof.png`를 `DesignSync`로 받아 배치한다.

## 완료 조건

- 세 화면 모두에서 사이드바·푸터가 시안과 동일하게 보인다.
- 375px / 768px / 1280px에서 가로 스크롤이 없고 사이드바와 본문이 겹치지 않는다.
- SCSS 어디에도 하드코딩된 hex 색상이 없다(`_tokens.scss` 제외).

## 커밋

`feat: add design tokens, page shell, and responsive layout`
