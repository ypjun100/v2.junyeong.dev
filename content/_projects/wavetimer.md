---
title: wavetimer
date: 2023-03-30
desc: 파동 효과를 활용한 웹 Pomodoro 타이머
skills:
- React
people:
- 개인 프로젝트
urls:
- type: website
  name: wavetimer
  url: https://wavetimer.junyeong.dev
- type: website
  name: 프로젝트 회고
  url: https://blog.junyeong.dev/posts/wavetimer-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%9A%8C%EA%B3%A0/
- type: github
  name: Github
  url: https://github.com/ypjun100/wavetimer-front
images:
- "/imgs/project/wavetimer/wavetimer.gif"
---

## 설명
> 화면 내에 차있는 물의 양으로 타이머의 시간이 얼마나 남았는지를 한눈에 확인할 수 있는 Pomodoro 타이머입니다. 파동 효과를 구현하기 위해 직접 파동 방정식을 이용하여 이를 구현하였고, 파동을 렌더링 하기 위해 Pixi.js 그래픽 라이브러리를 사용하였습니다.

## 개발 내용
### Pixi.js 라이브러리를 활용한 배경의 파동 효과 구현
* 기존에는 기본 canvas를 사용하여 파동을 렌더링하도록 구현함
* 하지만 타이머의 텍스트가 배경에 따라 색상이 바뀌는 텍스트 블렌딩 효과가 브라우저별로 다르다는 것을 확인함
* 이를 해결하기 위해 **기본 canvas가 아닌 Pixi.js 그래픽 라이브러리를 이용해 파동을 재구현하여 해당 문제를 해결함**

### 요청 애니메이션을 차례대로 실행할 수 있도록 **애니메이션 큐** 구현
* 시간에 따라 물의 양이 늘거나 줄어드는 애니메이션을 구현하는 과정에서 만약 애니메이션이 동시에 요청이 들어온 경우, 요청들이 동시에 비동기적으로 시작되는 문제가 발생했음
* 이를 해결하기 위해 **한차례에 하나의 애니메이션만 실행되도록 애니메이션 큐를 구현함**
* [문제 해결 과정 소개](https://blog.junyeong.dev/posts/wavetimer-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%9A%8C%EA%B3%A0/#3-%EC%95%A0%EB%8B%88%EB%A9%94%EC%9D%B4%EC%85%98-%ED%81%90)

### 사파리 브라우저 효과음 구현
* 타이머가 종료되는 경우 종료 효과음을 재생해야 했음
* 크롬 브라우저의 경우 웹 사이트 내에서 언제든지 개발자가 원하는 시간에 사운드를 재생할 수 있지만, 사파리 브라우저의 경우 사용자가 직접 웹에서 오디오를 트리거(클릭 or 터치) 하는 경우에만 오디오를 재생시킬 수 있음
* 이를 해결하기 위해, 사용자가 타이머 종료 효과음을 듣기 위해서는 무조건 'start' 버튼을 클릭해야 한다는 점에 착안하여, **'start' 버튼을 누를 때 아무 소리가 들리지 않는 빈 사운드를 계속 재생시키다 타이머가 종료되면 빈 사운드를 종료 효과 사운드로 교체하는 트릭을 구현함**