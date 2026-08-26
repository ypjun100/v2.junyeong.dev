# junyeong.dev

개인 포트폴리오 겸 기술 블로그입니다. 글은 모두 `content/` 아래의 마크다운 파일에서 읽어 옵니다.

## 로컬 실행

```bash
bundle install
bundle exec jekyll serve
```

`http://127.0.0.1:4000`에서 열립니다.

## 검증

```bash
bundle exec jekyll build --strict_front_matter
bundle exec htmlproofer _site --disable-external --allow-hash-href --ignore-missing-alt
```

## 배포

`main`에 푸시하면 `.github/workflows/pages.yml`이 빌드와 링크 검사를 거쳐 GitHub Pages로 배포합니다.

## 글 추가하기

작성 규칙과 front matter 스키마는 [AGENTS.md](AGENTS.md)에 있습니다.
