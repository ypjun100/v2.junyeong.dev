---
title: Lawy
date: 2023-11-23
desc: 교통사고 사건정보 텍스트를 기반한 형량 예측 웹서비스
skills:
- SpringBoot
- Tensorflow
urls:
- type: github
  name: Github
  url: https://github.com/ypjun100/legal-precedent-analysis
images:
- "/imgs/project/lawy/prediction1.png"
- "/imgs/project/lawy/prediction2.png"
- "/imgs/project/lawy/summarization1.png"
- "/imgs/project/lawy/summarization2.png"
---

## 설명
> 사법 취약계층을 위한 판결 예측 웹 서비스입니다. 교통사고에 대한 정보를 텍스트 형태로 입력하면 딥러닝을 통해 텍스트를 분석하여 징역, 집행유예 여부, 벌금을 예측합니다. 또한, 판결문에서 핵심 문장만 추출하여 사용자에게 제공하는 판결문 요약 기능을 제공합니다.

## 개발 내용
<img src="/imgs/project/lawy/architecture.png" style="object-fit: cover; margin-bottom: 0;"/>

### 서비스 아키텍처 설계
* Java를 기반한 백엔드 시스템과 Python을 기반한 딥러닝 모델 간의 연동이 필요했음
* 또한, 딥러닝 모델이 예측값을 반환하기 위한 처리량이 많기 때문에 이를 단일 컴퓨터에서 진행하는 경우 병목현상이 발생했음
* 이 두 가지의 이슈를 해결하기 위해 작업을 제공하는 Client(Producer)와 작업을 처리하는 Worker(Consumer)를 분리한 뒤, 두 계층 간의 통신을 관리하는 메시지 브로커인 TurtleMQ를 제작함
* **클라이언트가 텍스트를 전송하면 서버를 거쳐 딥러닝 모델을 실행하는 Worker로 텍스트가 전송되고, Worker에서 도출된 딥러닝 모델의 예측 결과가 클라이언트로 반환됨**
* TurtleMQ는 클라이언트가 전송한 데이터를 유휴 상태인 Worker에게 전달 및 Worker로부터 반환된 데이터를 다시 클라이언트로 반환하는 역할을 수행함
* 이러한 아키텍처를 적용함으로써 단일 컴퓨팅 환경에서 발생하는 병목현상을 해결한 **병렬 컴퓨팅 아키텍처**를 구현할 수 있었음
* [TurtleMQ 프로젝트 소개](/project/turtlemq)

### **웹소켓**을 기반한 API 통신 구현
* Lawy 서비스와 Lawy Summarization 서비스에서 제공하는 API의 반환 시간은 입력 텍스트의 길이에 비례하여 빨라지거나 느려짐
* 따라서 **클라이언트의 요청에 대한 결과 반환을 서버에서 비동기적으로 전송하기 위해 양방향 통신을 기반으로 한 웹소켓을 이용하여 구현함**

### 판결문 요약 기능 제작
* 이전에 제작한 [Recap 라이브러리](/project/recap)를 사용하여 판결문 요약 기능을 제작함

<!-- <hr/>

### 웹 크롤링 및 데이터 전처리 수행
* **Selenium 라이브러리**를 이용하여 판결문 제공 서비스에서 판결문 37,000개를 수집함
* 판결문을 80번 크롤링 할 때마다 캡챠 인증이 발생하는 것을 해결하기 위해 2개의 계정으로 80번마다 계정을 바꿔서 한 번에 총 160개의 판결문을 가져올 수 있도록 구현함
* 수집된 데이터를 모델의 입력으로 사용하기 위해 아래의 데이터 전처리 작업을 수행함
  <img src="/imgs/project/lawy/data_preprocessing.png" style="object-fit: cover; margin-bottom: 0;"/> -->