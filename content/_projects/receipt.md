---
title: Receipt
date: 2020-11-28
desc: 더치페이를 위한 계좌번호 공유 서비스
skills:
- ExpressJS
- React
urls:
- type: website
  name: receipt
  url: https://receipt.junyeong.dev
images:
- "/imgs/project/receipt/IMG_3578.PNG"
- "/imgs/project/receipt/IMG_3579.PNG"
- "/imgs/project/receipt/IMG_3580.PNG"
---

## 설명
> 더치페이를 할 때 매번 각자의 몫을 계산하고 계좌번호를 보내는 작업을 한번에 보내줄 수 있도록 도와주는 웹 서비스입니다. 총 가격, 인원과 사전에 등록한 입금 계좌를 선택한 뒤 이 정보들을 카카오톡으로 공유하여 입금하는 사람이 쉽게 텍스트를 복사하여 입금을 할 수 있도록 합니다.

## 주요 개발 내용
### 카카오톡 API를 사용한 메시지 전송
* 카카오톡 메시지를 받은 사용자가 쉽게 계좌번호를 복사할 수 있도록 [Kakao Developers](https://developers.kakao.com/)에서 메시지 템플릿을 설정
* 해당 메시지 템플릿을 사용하여 웹 내에서 `카카오톡 API`를 통해 카카오톡과 연동하여 메시지를 전송할 수 있도록 구현

### Redis를 활용한 사용자 로그인 세션 관리
* `Express.js`와 `Redis` 서버를 연동하여 로그인 한 사용자의 세션을 관리
* 세션을 관리하므로써 사용자가 페이지를 새로고침해도 로그인을 유지할 수 있도록 함

### RESTful API 구현
* 클라이언트와 서버 간 `RESTful API`를 통해 통신할 수 있도록 구현

### SPA(Single Page Application) 구현
* `React.js`의 `라우팅 기능`을 사용하여 `SPA`` 구현

### Redux를 활용한 상태 관리
* `React.js`에서 뷰 간의 상태 공유를 위해 `Redux`` 사용