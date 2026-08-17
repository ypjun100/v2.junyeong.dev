---
title: Java의 Constant Pool과 String Constant Pool
date: 2024-08-21 16:47:00 +0900
categories: [고찰시리즈]
tags: []
---
#### 요약
* Constant Pool은 바이트코드에 삽입될 수 없는 리터럴 및 참조 정보 데이터가 저장되는 곳으로, 컴파일 타임에 Constant Pool 테이블로 변환된다.
* 컴파일러에 의해 생성된 Constant Pool 테이블은 런타임 시점에 한 번 더 Runtime Constant Pool로 변환되며, 이때 문자열 리터럴은 별도로 String Constant Pool에 저장된다.
* String Constant Pool에 저장되는 동일한 문자열 리터럴은 단 한 번만 저장되며, 이를 참조하는 객체는 동일한 레퍼런스를 갖게 된다.

---

## 서론

```java
class HelloWorld {
    public static void main(String[] args) {
        String str1 = "Hello!";
        String str2 = "Hello!";
        
        System.out.println(str1 == str2); // -> true
    }
}
```

객체지향 메커니즘에서 우리는 흔히 서로 다른 두 객체는 다른 레퍼런스를 가진다고 알고 있었다. 하지만 동일한 문자열 리터럴을 갖는 두 개의 문자열 객체를 생성한 뒤에 이를 비교하는 연산을 진행하는 위 코드에서는 `true`를 반환한다. 분명히 코드에서 `str1`과 `str2`는 같은 문자열 리터럴을 갖기만 할 뿐, 서로 독립적으로 생성되었기 때문에 다른 객체에게 영향을 미치지 않는다. 그렇다면 **어떻게 두 객체는 동일한 레퍼런스를 갖게 되는 것일까?**

이번 글에서는 동일한 문자열 리터럴을 갖는 객체가 동일한 레퍼런스를 참조하게 된다는 궁금증을 해결하기 위해, 이에 대한 해결책의 근간이 되는 Java의 Constant Pool에 대해 자세히 알아볼 것이다. 그 이후에 우리의 궁금증을 해결해 줄 수 있는 String Constant Pool에 대해 알아보며 마무리를 지을 것이다.

전반적으로 이번 글에서 배우는 개념들은 우리가 코드를 작성하면서 자주 마주칠 일이 없는 것들이기 때문에, 어쩌면 문제에 대한 공감을 하지 못할 수도 있다. 그렇기 때문에 굳이 이 글을 정독하는 것보다는 자신이 궁금했던 개념들 혹은 흥미로운 개념들에 대해서만 읽고 그 이후 궁금한 내용들을 직접 찾아보며 공부하길 바란다.

_그럼 시작해보자!_

## Constant Pool

Java의 컴파일 타임 이후에 생성되는 클래스 파일(`.class`) 내에는 바이트코드[^fn-bytecode]와 Constant Pool이 저장된다. 이때 코드에서 사용된 문자열 혹은 숫자 리터럴의 경우 바이트코드에 저장되기에는 용량이 크기 때문에, 이를 별도의 장소인 Constant Pool에 저장하게 된다. 즉, <s>Constant Pool은 이렇게 바이트코드에 탑재되기엔 용량이 큰 리터럴(상수) 데이터가 저장되는 공간</s>으로, 바이트코드에서는 Constant Pool 내의 데이터를 참조하게 된다.

> **Constant Pool에 저장되는 데이터 유형**
> * 숫자 리터럴
> * 문자열 리터럴
> * 클래스 참조
> * 필드 참조
> * 메서드 참조


### Constant Pool 테이블

Constant Pool은 <s>바이트코드에서 데이터를 참조하기 쉽도록 컴파일러에 의해 테이블 형태로 아래와 같이 클래스 파일 내부에 저장되는데, 이를 Constant Pool 테이블이라고 한다.</s> 그리고 이 테이블 내에는 해당 클래스 파일에서 사용되는 리터럴 데이터와 참조 정보들이 저장된다.

```
Constant pool:
   #1 = Methodref          #2.#3          // java/lang/Object."<init>":()V
   #2 = Class              #4             // java/lang/Object
   #3 = NameAndType        #5:#6          // "<init>":()V
   #4 = Utf8               java/lang/Object
   #5 = Utf8               <init>
   #6 = Utf8               ()V
   #7 = Fieldref           #8.#9          // java/lang/System.out:Ljava/io/PrintStream;
   #8 = Class              #10            // java/lang/System
   #9 = NameAndType        #11:#12        // out:Ljava/io/PrintStream;
  #10 = Utf8               java/lang/System
  #11 = Utf8               out
  #12 = Utf8               Ljava/io/PrintStream;
  #13 = String             #14            // Hello World!
  #14 = Utf8               Hello World!
  #15 = Methodref          #16.#17        // java/io/PrintStream.println:(Ljava/lang/String;)V
  #16 = Class              #18            // java/io/PrintStream
  #17 = NameAndType        #19:#20        // println:(Ljava/lang/String;)V
  #18 = Utf8               java/io/PrintStream
  #19 = Utf8               println
  #20 = Utf8               (Ljava/lang/String;)V
  #21 = Class              #22            // HelloWorld
  #22 = Utf8               HelloWorld
  #23 = Utf8               Code
  #24 = Utf8               LineNumberTable
  #25 = Utf8               main
  #26 = Utf8               ([Ljava/lang/String;)V
  #27 = Utf8               SourceFile
  #28 = Utf8               HelloWorld.java
```

> `javap -v` 명령을 통해 클래스 파일 내에 저장된 Constant Pool 테이블을 확인할 수 있다.

위의 Constant Pool 테이블은 컴파일러에 의해 생성된 `HelloWorld` 클래스의 Constant Pool 테이블이다. 이 클래스에서는 단순히 "Hello World!" 문자열을 출력하고 있기 때문에, `#14`번 레퍼런스 인덱스에 해당 문자열 리터럴을 저장하고 있음을 확인할 수 있다. 또한, 문자열을 출력하기 위한 `System.out.println()` 메서드의 참조 정보가 `#16` ~ `#20`번 인덱스에 저장된 것을 확인할 수 있다. 그리고 이 테이블을 가지고 런타임 시점에 JVM은 뒤에서 후술할 Runtime Constant Pool을 생성하게 된다.

### Runtime Constant Pool

<img src="/imgs/2024-08-21/jvm-memory-structure-old.png"/>
_Java 8 이전의 JVM 메모리 구조<br>[https://8iggy.tistory.com/229](https://8iggy.tistory.com/229){:target="_blank"}_

런타임 시점에 클래스 로더[^fn-classloader]는 리터럴 및 참조 정보 데이터를 참조하기 위해 Constant Pool 테이블에 저장된 데이터들을 Runtime Constant Pool에 저장한다. 여기서 살짝 헷갈릴 수도 있는데 간단하게, 컴파일 타임에 생성된 <s>Constant Pool 테이블을 가지고 런타임에서 Runtime Constant Pool을 생성한다고 보면 된다.</s> 이때 Runtime Constant Pool은 Constant Pool 테이블과 마찬가지로 클래스별로 다른 풀이 생성되며, 생성된 풀을 통해 JVM은 클래스에서 사용되는 리터럴, 메서드 및 클래스에 대한 실제 메모리 주소를 찾아 이를 참조하게 된다.

Runtime Constant Pool은 JVM 메모리 구조 중에 메서드 영역(Metaspace 영역)에 생성되며, 프로그램이 종료될 때까지 메모리에 유지된다. Java 8 이전에 Runtime Constant Pool은 Permanent Heap 영역에 저장되었으나, 해당 영역의 경우 Heap 영역과 달리 동적으로 사이즈를 늘리거나 줄일 수 없는 고정 크기를 할당받기 때문에 런타임 중에 Permanent Heap의 메모리 부족으로 OOM(Out of Memory) 문제가 발생되는 경우가 잦았다.

> Permanent Heap 영역은 Heap 영역에 포함된 상태이긴 하나 일반적으로 Heap 영역과는 구분하여 설명한다. 그 예시로 오라클 문서에서는 Heap 영역에 포함되어 있기는 하나 Heap 영역과는 다르게 간주하며, 논리적으로는 Heap의 한 부분이라고 설명한다.

<img src="/imgs/2024-08-21/jvm-memory-structure-new.png"/>
_Java 8 이후의 JVM 메모리 구조<br>[https://deveric.tistory.com/123](https://deveric.tistory.com/123){:target="_blank"}_

따라서, Java 8 이후에 Runtime Constant Pool은 메서드 영역으로 이전하게 되었으며, 이 영역은 JVM이 직접 관리하며 필요에 따라 메모리를 추가로 할당할 수 있어, 이전에 발생한 OOM 문제를 해결할 수 있었다.

## String Constant Pool

```java
class HelloWorld {
    public static void main(String[] args) {
        String str1 = "Hello!";
        String str2 = "Hello!";
        
        System.out.println(str1 == str2); // -> true
    }
}
```

다시 이 글의 주제인 '동일한 문자열 리터럴을 갖는 객체는 동일한 레퍼런스를 참조한다.'로 돌아가 보자. 분명히 코드에서 `str1`과 `str2` 문자열 객체는 독립적으로 생성되었지만, `str1 == str2` 연산에서는 `true`를 반환한다. 이를 자세히 분석해 보기 위해 해당 클래스를 컴파일 한 뒤에 생성되는 Constant Pool 테이블을 확인해 보자.

```
Constant pool:
   #1 = Methodref          #2.#3          // java/lang/Object."<init>":()V
   #2 = Class              #4             // java/lang/Object
   #3 = NameAndType        #5:#6          // "<init>":()V
   #4 = Utf8               java/lang/Object
   #5 = Utf8               <init>
   #6 = Utf8               ()V
   #7 = String             #8             // Hello!
   #8 = Utf8               Hello!
   #9 = Fieldref           #10.#11        // java/lang/System.out:Ljava/io/PrintStream;
  #10 = Class              #12            // java/lang/System
  #11 = NameAndType        #13:#14        // out:Ljava/io/PrintStream;
  #12 = Utf8               java/lang/System
  #13 = Utf8               out
  #14 = Utf8               Ljava/io/PrintStream;
  #15 = Methodref          #16.#17        // java/io/PrintStream.println:(Z)V
  #16 = Class              #18            // java/io/PrintStream
  #17 = NameAndType        #19:#20        // println:(Z)V
  #18 = Utf8               java/io/PrintStream
  #19 = Utf8               println
  #20 = Utf8               (Z)V
  #21 = Class              #22            // HelloWorld
  #22 = Utf8               HelloWorld
  #23 = Utf8               Code
  #24 = Utf8               LineNumberTable
  #25 = Utf8               main
  #26 = Utf8               ([Ljava/lang/String;)V
  #27 = Utf8               StackMapTable
  #28 = Class              #29            // "[Ljava/lang/String;"
  #29 = Utf8               [Ljava/lang/String;
  #30 = Class              #31            // java/lang/String
  #31 = Utf8               java/lang/String
  #32 = Utf8               SourceFile
  #33 = Utf8               HelloWorld.java
```

Constant Pool 테이블을 보면 특이한 점이 있는데, 코드에서는 "Hello!"라는 문자열 리터럴을 두 번 정의했으나, 테이블 내에서 이 리터럴을 저장하는 곳은 `#8`번 인덱스밖에 없다는 것이다. 이 말은 즉슨, `str1`과 `str2` 모두 `#8`번 인덱스를 참조하고 있다는 의미가 되며, 이러한 이유로 `str1 == str2` 연산이 `true`를 반환하는 것은 올바른 결과로 보인다.

<img src="/imgs/2024-08-21/strings-in-memory.png"/>
_문자열 리터럴 관점의 JVM 메모리 구조<br>[https://deveric.tistory.com/123](https://deveric.tistory.com/123){:target="_blank"}_

그리고 이러한 결과는 JVM 메모리 구조 상으로도 일치하는 결과이다. JVM의 Heap 메모리에는 문자열 리터럴을 저장하기 위한 String Constant Pool이라는 영역이 따로 존재하며, 클래스 내의 문자열 객체는 String Constant Pool 내에 저장된 리터럴을 참조하게 된다. <s>이 과정에서 동일한 문자열 리터럴은 저장 공간의 낭비를 방지하기 위해 풀 내에 단 하나의 리터럴만 생성되기 때문에 str1과 str2가 동일한 참조를 가질 수 있었던 것이다.</s>

> Java 8 이전에는 String Constant Pool과 Runtime Constant Pool이 동일하게 Permanent Heap 영역에 저장됐으나, Java 8 이후부터 Runtime Constant Pool이 메서드 영역으로 이전됐기 때문에 이제는 이 둘을 구분하여 설명한다.

> **Just My Opinion**<br>
> String Constant Pool이 Runtime Constant Pool과 같은 메서드 영역으로 함께 이전되지 않은 이유는 아무래도 Garbage Collection과 관련이 있을 것 같다. 문자열의 경우 런타임 중에 사용자에 의해 생성되고, 소멸되어야 하는 경우가 잦기 때문에 GC가 개입할 수 있는 힙 메모리에 String Constant Pool을 위치시켜 더 이상 사용되지 않는 문자열을 GC가 삭제할 수 있게끔 할 수 있을 것이다. 반면에, 객체 및 메서드의 참조 정보를 저장하는 Runtime Constant Pool의 경우 런타임 중에 생성이 될 수는 있지만 쉽게 소멸이 되지는 않는 형식이기 때문에 메모리 확장에 용이한 메서드 영역에 저장이 되는 게 아닐까 싶다.

```java
class HelloWorld {
    public static void main(String[] args) {
        String str1 = "Hello!";
        String str2 = "Hello!";
        String str3 = new String("Hello!");
        String str4 = new String("Hello!");
        
        System.out.println(str1 == str2); // -> true
        System.out.println(str1 == str3); // -> false
        System.out.println(str3 == str4); // -> false
    }
}
```

이때 주의해야 할 점은 문자열 객체의 생성 방식에 따라 문자열 리터럴이 String Constant Pool에 저장될 수도 있고, Heap 영역에 저장될 수도 있다는 것이다. 위 코드에서 `str1`과 `str2`가 참조하고 있는 리터럴의 경우 String Constant Pool에 저장이 되지만, `str3`과 `str4`와 같이 <s>생성자를 이용한 문자열 리터럴은 String Constant Pool이 아닌 보통 객체를 생성할 때와 마찬가지로 Heap 영역에 저장된다.</s>

따라서, `str1`과 `str3`을 비교하는 연산에서 `str1`의 리터럴은 String Constant Pool에 저장되지만, `str3`의 리터럴은 Heap에 저장되기 때문에 두 객체를 비교하는 연산에서 `false`를 반환하는 것이다. 그리고 생성자를 이용한 문자열 리터럴의 경우 동일한 문자열을 가지는 경우에도 리터럴이 Heap 영역에 따로 저장되기 때문에, `str3`과 `str4`를 비교하는 연산에서 `false`를 반환하는 것을 확인할 수 있다.

> `new String("Hello!").intern()` 방식으로 문자열 리터럴을 생성한다면, 해당 리터럴은 힙 영역이 아닌 String Constant Pool 내에 저장된다.

## 결론

<img src="/imgs/2024-08-21/infinite-road.jpg"/>

이번 글에서는 '동일한 문자열 리터럴을 갖는 객체는 동일한 레퍼런스를 참고한다.'라는 주제를 바탕으로, 주제의 근간이 되는 Constant Pool으로부터 시작하여, 컴파일 시점에 바이트코드에 삽입될 수 없는 리터럴과 참조 정보들을 저장하기 위한 Constant Pool 테이블을 알아보고, 런타임 시점에 이 테이블의 데이터가 그대로 Runtime Constant Pool로 옮겨진다는 사실을 알게 되었다.

이때 문자열 리터럴의 경우 Heap 영역 내에 존재하는 String Constant Pool 내에 따로 저장되며, 풀 내에 동일한 문자열 리터럴은 저장 공간의 낭비를 막기 위해 단 하나만 존재한다는 것 또한 알게 되었다. 그리고 이를 통해 <s>동일한 문자열 리터럴을 갖는 객체는 String Constant Pool 내의 동일한 문자열 리터럴을 참조하기 때문에 동일한 레퍼런스를 참조하게 된다는</s> 결론을 얻게 되었다.

여태까지 그래왔듯이 프로그래밍 언어는 시간이 흐를수록 개발자가 프로그래밍 언어의 내부 구현까지 공부할 필요가 없도록 변화될 것이다. 어쩌면 이러한 흐름은 개발자가 좀 더 편하게 개발하고 빠르게 프로덕트를 구현할 수 있다는 이점이 있었기에 그 흐름을 그대로 유지할 수 있었을 것이다. 그리고 나 또한 이번 글을 통해서 코드를 작성하는 실력이 늘기를 바라거나 이를 읽는 독자의 코드 실력이 늘 것이라고 기대하진 않는다.

다만, Java에서 사용한 아키텍처를 공부하며 얻은 인사이트를 바탕으로 나중에 실제로 본인의 아키텍처를 설계할 때에 큰 도움이 될 것이라 생각한다. 어떻게 보면 Java에서 적용된 아키텍처나 개념들은 이미 사용자들에 의해 사용되고, 검증이 완료된 아키텍처이기 때문에 이를 바탕으로 본인의 것을 만들어 나간다면 좀 더 신뢰할 수 있는 무언가를 만들어 낼 수 있지 않겠는가.

그렇기 때문에 우리가 무심코 공부했던 개념들을 다시 살펴보고, 작동 원리에 대해 자세히 공부해 보는 것이 중요하다고 생각한다. 그래서 할 수 있다면 앞으로도 이런 나의 궁금증을 바탕으로 어떤 개념을 깊게 공부해 보는 글을 종종 작성해 볼 생각이다. _그럼 다음 글에서 보자! 👋_

#### References
1. [https://blog.jamesdbloom.com/JVMInternals.html#constant_pool](https://blog.jamesdbloom.com/JVMInternals.html#constant_pool){:target="_blank"}
2. [https://velog.io/@ddangle/Java-%EB%9F%B0%ED%83%80%EC%9E%84-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%98%81%EC%97%ADRuntime-Data-Area%EC%97%90-%EB%8C%80%ED%95%B4](https://velog.io/@ddangle/Java-%EB%9F%B0%ED%83%80%EC%9E%84-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%98%81%EC%97%ADRuntime-Data-Area%EC%97%90-%EB%8C%80%ED%95%B4){:target="_blank"}
3. [https://8iggy.tistory.com/229](https://8iggy.tistory.com/229){:target="_blank"}
4. [https://blog.naver.com/adamdoha/222817943149](https://blog.naver.com/adamdoha/222817943149){:target="_blank"}
5. [https://le2ksy.tistory.com/30](https://le2ksy.tistory.com/30){:target="_blank"}
6. [https://deveric.tistory.com/123](https://deveric.tistory.com/123){:target="_blank"}
7. [https://velog.io/@ddangle/Java-%EB%9F%B0%ED%83%80%EC%9E%84-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%98%81%EC%97%ADRuntime-Data-Area%EC%97%90-%EB%8C%80%ED%95%B4](https://velog.io/@ddangle/Java-%EB%9F%B0%ED%83%80%EC%9E%84-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%98%81%EC%97%ADRuntime-Data-Area%EC%97%90-%EB%8C%80%ED%95%B4){:target="_blank"}

---
[^fn-bytecode]: 고급 언어로 작성된 소스 코드를 JVM이 이해할 수 있는 언어로 변환된 코드를 말한다.
[^fn-classloader]: 런타임 중에 필요한 Java 클래스를 동적으로 JVM의 메서드 영역으로 로드하는 역할을 담당한다.