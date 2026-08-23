---
title: 오목 AI
date: 2022-11-16
desc: Minimax 알고리즘을 기반한 오목 AI 앱
skills:
- iOS
people:
- 개인 프로젝트
urls:
- type: github
  name: Github
  url: https://github.com/ypjun100/gomoku-ai
images:
- "/imgs/project/gomoku-ai/image1.png"
---

## 설명
> **Minimax 알고리즘**을 기반한 오목 AI를 iOS 앱으로 제작하였습니다.

## 개발 내용
### 몇 수 앞을 계산하는 Minimax 알고리즘 구현
* 틱택토나 오목과 같은 제로섬 게임의 AI를 구현하기 위한 **Minimax 알고리즘을 Swift 언어로 구현함**
* 파라미터 값의 변경을 통해 현재 수에서 앞으로 몇 수를 더 내다볼지 변경이 가능함

### UIGraphics를 활용하여 코드만으로 보드판 및 돌 렌더링
* 보드판과 돌을 표시하기 위해 이미지를 사용하는 것이 아닌, UIGraphics만 활용하여 보드판 및 돌을 렌더링 할 수 있도록 구현함

### UITapGestureRecognizer로 사용자 터치 이벤트 판단
* 사용자가 보드판 위 어느 위치에 착수하고 싶은지 판단하기 위해 GestureRecognizer를 이용하여 터치 좌표와 보드판의 위치를 참고하여 착수 위치를 계산함