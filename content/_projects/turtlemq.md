---
title: TurtleMQ
date: 2023-11-01
desc: WebSocket을 기반한 메시지 브로커
skills:
- SpringBoot
people:
- 개인 프로젝트
urls:
- type: github
  name: Github
  url: https://github.com/ypjun100/TurtleMQ
images:
- "/imgs/project/turtlemq/architecture.png"
---

## 설명
> TurtleMQ는 **RabbitMQ**를 모티브로 제작된 Spring 애플리케이션입니다. 단일 컴퓨팅 환경에서 **병목현상**이 발생하는 것을 방지하기 위해 작업을 제공하는 클라이언트(**Producer**)와 작업을 처리하는 Worker(**Consumer**)로 분리합니다. 그리고 작업을 수행할 Worker들과 **웹소켓** 방식으로 연결되어 병렬 컴퓨팅 환경을 구성하고, Worker 노드들을 전반적으로 관리합니다.

## 개발 내용
### 통신 아키텍처 설계
* 클라이언트가 작업 요청 메시지를 보내면, TurtleMQ는 유휴 상태인 Worker에게 해당 메시지를 전달함
* Worker에서 작업이 완료되면 결과 메시지를 TurtleMQ로 전달하고, TurtleMQ는 클라이언트에게 해당 메시지를 전달함
* 이러한 **클라이언트와 Worker 간의 유기적인 통신을 위해 TurtleMQ에서 클라이언트와 Worker를 관리하도록 구현함**
* 이때 클라이언트와 Worker는 TurtleMQ에 등록 메시지를 보내고, 승인을 받아야만 정상적으로 데이터를 송신 및 수신할 수 있음
* 각 계층 간의 **모든 통신은 웹소켓을 기반하여 이루어지기 때문에 웹소켓을 지원하는 다양한 프로그래밍 언어 및 환경에서 TurtleMQ를 적용할 수 있음**

### 유휴 상태인 Worker에 메시지 전달
* **TurtleMQ가 클라이언트로부터 작업 요청 메시지를 받으면, 현재 유휴 상태인 적절한 Worker를 찾은 후 해당 Worker에게 메시지를 전달함**
* Worker의 유휴 상태 판단을 위해 웹소켓 세션이 유지된 Worker 중에서 작업 메시지를 전달받지 않은 Worker를 유휴 상태로 판단하고, 작업 메시지를 전달했지만 결과 메시지를 반환하지 않은 Worker를 작업 중이라고 판단함
* 모든 워커가 작업 중인 경우 들어온 작업 대기큐에 넣어짐

### 작업 중인 Worker의 세션이 끊기면 다른 Worker에게 작업 이관
* 특정 **Worker가 작업 중에 오류나 네트워크 문제로 인해 세션이 종료된 경우, 해당 Worker가 작업하고 있던 메시지를 그대로 다른 Worker에게 이관함**
* 이를 위해 TurtleMQ에서는 각 Worker가 작업 중인 메시지를 별도로 저장하고, 해당 Worker가 문제가 발생하면 해당 메시지를 그대로 다른 Worker에게 전달함
* 만약 연결이 끊긴 Worker가 다시 접속하여 작업 결과를 보낸다면 해당 결과는 무시하도록 구현함