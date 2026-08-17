---
title: TAPE
date: 2019-09-01
desc: 비속어를 자동으로 필터링하는 비디오 플랫폼
skills:
- Python
people:
- 비속어 필터링 구현 1명
- 백엔드 2명
- 앱 개발 1명
urls:
- type: youtube
  name: 프로젝트 소개 영상
  url: https://www.youtube.com/watch?v=PqWzZ2TTLXk
- type: github
  name: Github
  url: https://github.com/ypjun100/TAPE
images:
- "/imgs/project/tape/tape1.png"
- "/imgs/project/tape/tape2.png"
- "/imgs/project/tape/tape3.png"
---

## 설명
> 영상 매체에서 그대로 송출되는 비속어를 학생들이 그대로 따라 하는 것을 방지하기 위해, 동영상을 업로드하면 서버에서 자동으로 비속어를 비프음으로 필터링한 뒤 온라인에 게재하는 형식의 비속어에 안전한 동영상 플랫폼입니다.

## 주요 개발 내용
### 비속어 필터링 기능
* 영상이 입력으로 들어오면 해당 영상의 음성에서 비속어만을 필터링하는 과정을 담당함
* 인공지능 모델을 구현하는 것보다 API를 이용하는 것이 용이하다고 판단하여, `Google Cloud API`의 타임스탬프 기능을 이용하여 특정 단어의 시작 시간과 종료 시간을 파악함
* <mark>비속어를 탐색하여 단어의 시작 시간부터 종료 시간까지의 음성을 비프음으로 대체함</mark>
* 음성을 비프음으로 변환하기 위해 `ffmpeg`를 사용하여 비디오 파일에서 오디오를 추출하고, 비프음으로 교체하는 작업을 진행함
* Google API에 업로드할 수 있는 오디오 파일 길이 제한이 있었기 때문에 비디오 하나를 처리하기 위해 한 오디오 파일을 여러 개로 잘라 업로드를 진행함
* 하지만 이러한 방식은 소요시간이 오래 걸리기 때문에 이를 해결하기 위해 <mark>파이썬의 threading 모듈을 사용하여 업로드를 병렬로 진행하여 빠른 처리 방식을 구현함</mark>