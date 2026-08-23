---
title: Recap
date: 2023-09-07
desc: 텍스트 요약을 위한 Java 라이브러리
skills:
- Java
- SpringBoot
urls:
- type: youtube
  name: 시연영상
  url: https://youtu.be/G4gBvF9SZR0?si=0LkR0duOn3Nrs9Mc
- type: github
  name: Library
  url: https://github.com/team-recap/recap
- type: github
  name: Examples
  url: https://github.com/team-recap/recap-examples
images:
- "/imgs/project/recap/logo.png"
---

<iframe width="100%" height="400" src="https://www.youtube.com/embed/G4gBvF9SZR0?si=2d3clAmmIaTNKztW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## 설명
> 입력된 텍스트에서 핵심 문장만 추출하는 형식으로 텍스트 요약을 진행하는 Java 라이브러리입니다. 텍스트 요약을 위해 **TextRank 알고리즘**을 사용하였고, 라이브러리 적용 예시를 시연하기 위해 예제 프로젝트를 제작하였습니다.

## 개발 내용
### 텍스트 요약 **라이브러리 제작**
* **TextRank 알고리즘을 사용하여 텍스트 요약 라이브러리 제작함**
* 핵심 문장을 추출하기 위한 문장 간 유사도를 측정하는 계산법으로 코사인과 자카드 유사도 방법을 제공함
* 형태소 분석기 외에는 다른 라이브러리에 대한 의존성이 없도록 구현하여 낮은 의존도를 가질 수 있도록 구현함

### Recap 라이브러리를 사용한 웹 서비스 제작
* 라이브러리 적용 예시를 시연하기 위해 **카카오톡 채팅방 내의 채팅 기록을 추출하여 웹 사이트 내에 입력하면 채팅 텍스트를 요약해 주는 웹 서비스를 제작함**