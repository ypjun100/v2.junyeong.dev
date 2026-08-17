# TASK 06 — 배포

## 목표

`main`에 푸시하면 `v2.junyeong.dev`로 자동 배포되게 만든다. 배포 전에 빌드와 링크 검증을 통과해야 한다.

## 선행

TASK 01 ~ 05.

## 작업

1. `CNAME` — `v2.junyeong.dev` 한 줄.
2. `.github/workflows/pages.yml`
   - 트리거: `push`(`main`), `workflow_dispatch`
   - 권한: `contents: read`, `pages: write`, `id-token: write`
   - `concurrency: { group: pages, cancel-in-progress: false }`
   - build 잡: `actions/checkout` → `ruby/setup-ruby`(`bundler-cache: true`) → `actions/configure-pages` → `bundle exec jekyll build --strict_front_matter` → `bundle exec htmlproofer _site --disable-external --allow-hash-href` → `actions/upload-pages-artifact`
   - deploy 잡: `actions/deploy-pages`, `environment: github-pages`
3. `_config.yml`의 `url`이 `https://v2.junyeong.dev`인지 확인한다.
4. `README.md` — 사이트 소개, 로컬 실행 명령, 배포 방식 세 문단.

## 사용자 승인이 필요한 단계

GitHub 원격 저장소가 아직 없다. 아래는 실행 전에 사용자에게 확인한다.

- `gh repo create`로 원격 저장소를 만드는 것
- 저장소 설정에서 Pages 소스를 `GitHub Actions`로 바꾸는 것
- `v2.junyeong.dev` DNS CNAME 레코드를 추가하는 것 (사용자가 직접 수행)

## 완료 조건

- 워크플로 파일이 로컬에서 `bundle exec jekyll build --strict_front_matter`와 `bundle exec htmlproofer _site --disable-external`을 통과하는 것과 동일한 명령을 쓴다.
- 두 명령을 로컬에서 실행해 통과를 확인한다.

## 커밋

`ci: add GitHub Pages deployment workflow and custom domain`
