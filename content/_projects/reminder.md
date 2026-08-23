---
title: REMINDER
date: 2018-08-06
desc: 버릇 교정을 도와주는 머신러닝 기반 IOT 디바이스
skills:
- Tensorflow
- Arduino
people:
- 머신러닝 엔지니어 1명
- 아두이노 개발 1명
- 앱 개발 1명
images:
- "/imgs/project/reminder/reminder1.jpg"
- "/imgs/project/reminder/reminder2.jpg"
---

<iframe width="100%" height="400" src="https://www.youtube.com/embed/vB_ea0pDKl4?si=qmNag3m7wo9y7Iy1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## 설명
> 손톱을 물어뜯거나 머리를 긁는 등의 버릇을 교정할 수 있도록 손목에 착용하는 **아두이노 디바이스**를 제작하였습니다. 이 디바이스를 착용한 상태에서 버릇을 행하면 디바이스 내의 진동모터를 통해 진동을 주는 형식으로 사용자에게 알립니다. 그리고 디바이스는 앱과 연동되어 앱 내에서는 오늘 버릇에 대한 통계를 확인할 수 있습니다.

## 주요 담당 내용
### 리더
* 팀원들의 자유로운 아이디어 제안을 장려할 수 있는 환경을 구축함
* 팀원이 겪고 있는 이슈사항에 대해 팀원 혼자 해결하기 보다 모두가 같이 모여 이야기하며 해결할 수 있도록 함

### 머신러닝 엔지니어 및 아두이노 코딩
* **아두이노**에서 도출된 **가속도 센서값**을 이용해 **딥러닝 모델**을 사용하여 버릇 탐지

## 개발 내용
### 아두이노 디바이스 제작
* **사용자가 손을 움직일 때 들어오는 가속도 센서값을 저장했다가, 움직임이 끝났을 때 블루투스 통신을 이용해 휴대폰으로 전송되도록 구현함**
* 가속도 센서값을 보정하기 위한 **보정 필터**를 사용함

### 버릇 탐지 딥러닝 모델 구현
* 기존에는 가속도 센서를 통해 얻을 수 있는 기울기 값만으로 버릇 탐지를 진행했지만, 사용자의 자세에 따라 기울기 값의 차이가 큰 것을 확인함
* 이 문제를 해결하기 위해 기울기 값이 아닌 가속도 센서의 원천 데이터인 3축 가속도 값으로 딥러닝 모델을 학습시킴
* 이 과정을 위해 손톱 물어뜯기, 옆 머리 긁기, 뒷 목 긁기 행동을 반복하여 데이터를 수집함
* **CNN(Convolutional Neural Network) 모델을 사용하여 모델 구축 후 안드로이드 애플리케이션에 탑재함**