---
title: Apple PencilKit Framework에 대한 고찰
date: 2023-05-15 20:55:00 +0800
categories: [고찰시리즈, UIKit]
tags: [Swift]
---
#### 요약
* PencilKit은 손쉽게 필기 기능을 제작할 수 있도록 Apple에서 제공하는 프레임워크이다.
* Metal API와 필기 예측 기술을 통해 낮은 필기 지연율을 제공한다.
* 다만, 프레임워크에서 제공하는 기능이 적어 다양한 기능을 구현하기는 힘들다.

---

## 서론
최근 나는 노트 앱 개발을 위해 여러 자료를 찾아보고 있다. 특히, [Notability](https://notability.com/ko)나 [GoodNotes](https://www.goodnotes.com/)와 같이 다양한 기능들을 제공하고 싶었기 때문에, 먼저 아이패드에서 기본적으로 제공하는 노트 앱에 대해 알아보다 PencilKit이라는 프레임워크를 찾게되었다.


## PencilKit
> "PencilKit은 Apple의 모든 OS에서 사용할 수 있는 프레임워크입니다. 이를 노트 앱에서 사용함으로써 낮은 지연율(low latency)을 제공합니다."
> <span style="color: gray;">\- WWDC22 'Introducing PencilKit' 中</span>

[PencilKit](https://developer.apple.com/documentation/pencilkit)은 Apple에서 제공하는 프레임워크로 개발자가 쉽게 노트 앱을 제작할 수 있도록 도와준다. 대표적으로 Apple의 OS에서 제공되는 기본 '노트'앱이 PenilKit을 사용하며, '미리보기' 앱에서 마크업기능과 아이패드에서 스크린샷을 찍은 후 스크린 샷 위에 그릴 때에도 PencilKit을 사용한다. 그리고 PencilKit에서는 손가락, 애플펜슬(1세대, 2세대), 크래용펜 등 여러 입력 장치를 지원하고, 펜의 기울기, 필압, 제스처를 인식하여 자연스러운 필기 경험을 제공한다.![](/imgs/2023-05-15/latency-is-critical.png) 모두가 알듯이 펜의 필기 지연율은 유저 경험에 굉장히 중요한 요소 중 하나이다. 실제로 애플 펜슬은 240Hz 속도로 필기 데이터를 패드로 전송하지만, 위 사진과 같이 노란색 갭이 생기기 마련이다. 따라서 PencilKit에서는 아래의 기술들을 통해 이 갭을 최소화하였다.
* **Metal API**
[Metal API](https://developer.apple.com/metal/)는 Apple에서 제공하는 프레임워크로 3D 그래픽 처리를 위해 기기의 GPU에 바로 접근할 수 있게하여 low-level 및 low-overhead를 제공한다. 대표적인 비교군으로 [Vulkan](https://www.vulkan.org/)과 [DirectX](https://learn.microsoft.com/ko-kr/windows/win32/directx)가 있다.
UIKit은 보통 터치 이벤트를 60Hz의 속도로 처리하기 때문에 PencilKit에서는 UIKit이 아닌 Metal API를 활용하여 더 높은 속도로 터치 이벤트를 처리할 수 있도록 한다.

* **필기 예측**
PencilKit에서는 Metal API사용과 더불어 사용자의 이전 펜슬 위치 데이터를 통해 이후의 펜슬 위치를 예측함으로써 필기 지연율을 낮춘다. 그러나 아쉽게도 이를 어떻게 구현했는지에 대한 설명은 찾을 수 없었다.

## 장점
* **쉬운 구현**
Apple WWDC의 PencilKit을 소개하는 영상에서 프레임워크를 단 3줄의 코드로 사용할 수 있다고 소개한다. 물론 추가적인 기능을 구현하면 더 많은 코드를 작성해야겠지만, 이것또한 PencilKit에서 제공하는 함수를 이용하면 쉽게 구현이 가능하다.

* **낮은 지연율**
위에서 설명했던 것과 같이 Metal API와 필기 예측 기술을 통해 낮은 지연율을 제공한다.
[참고 영상](https://youtu.be/8qFK-mgYIU8)

## 단점 ![](/imgs/2023-05-15/delegate.png)
* **부족한 제공 기능**
PencilKit의 [PKCanvasViewDelegate를 소개하는 문서](https://developer.apple.com/documentation/pencilkit/pkcanvasviewdelegate)를 살펴보자. 문서에 나와있듯, 사용자의 입력에 대한 이벤트를 받는 함수는 사용자가 그리기 시작할 때 발생하는 이벤트(canvasViewDidBeginUsingTool)와 사용자가 그리기를 끝냈을 때 발생하는 이벤트(canvasViewDidEndUsingTool)로 총 2개 밖에 없다... 따라서 만약 사용자가 무언가를 그리고 있는 경우 별다른 이벤트를 받을 수 없다는 말이다.
예시로 기본 노트 앱에서는 도형을 그린 후 펜슬을 터치한 상태로 계속 유지하면 자동으로 도형으로 변환해주는 기능이 있다. 하지만 PencilKit에서는 사용자의 입력 장치가 화면 터치를 하고 있을 때는 별다른 이벤트를 받을 수 없으므로 이 기능을 구현할 수 없을 것이다.

## 결론
정리를 해보자면 PencilKit은 Metal API와 필기 예측 기술을 통해 낮은 필기 지연율을 제공하지만, 프레임워크 내에서 제공하는 기능들이 한정적이다.

이와같이 PencilKit은 장단점이 분명한 프레임워크이기 때문에 자신이 개발할 앱의 특징에 맞게 PencilKit의 사용 유무를 결정해야한다. 만약 자신이 기본적인 드로잉에 충실한 앱을 개발하고자 하면 PencilKit이 최고의 선택지일 수 있으나, 나와 같이 PencilKit에서 기본적으로 제공하는 기능으로는 기능 구현이 부족한 경우에는 [다른 대안](https://developer.apple.com/documentation/uikit/touches_presses_and_gestures/leveraging_touch_input_for_drawing_apps)을 찾는 것이 최선의 선택일 것이다.
<br>


---
**References** <br>[https://developer.apple.com/videos/play/wwdc2019/221/](https://developer.apple.com/videos/play/wwdc2019/221/)<br>[https://developer.apple.com/documentation/uikit/pencil_interactions/handling_input_from_apple_pencil](https://developer.apple.com/documentation/uikit/pencil_interactions/handling_input_from_apple_pencil)<br>[https://haningya.tistory.com/305](https://haningya.tistory.com/305)<br>[https://blog.mathpresso.com/ios-pencilkit을-활용한-drawing-노트-개발기-d50019d42041](https://blog.mathpresso.com/ios-pencilkit을-활용한-drawing-노트-개발기-d50019d42041)
