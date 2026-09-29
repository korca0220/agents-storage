# [카테고리] ([Category])

<!--
작성 규칙
- Figma 변수·스타일(읽기 전용)에서 확인한 값만 쓴다. 컬렉션·mode·alias 관계를 그대로 옮긴다.
- 표의 "토큰"은 Figma 변수 이름 그대로 쓴다. Dart 이름은 쓰지 않는다(lib/AGENTS.md의 몫).
- 해당 없는 절은 지운다. 이 주석도 지운다.
-->

## 구조

- Figma 컬렉션: `[Collection]` ([N]개 변수, mode: [Light] …)
- 계층: [Primitive만 / Primitive → Semantic / 스타일(Text Style·Effect Style)]

## 토큰

| 토큰 | 값 | 용도 |
| --- | --- | --- |
| `[group]/[name]` | [값 또는 alias 대상] | [어디에 쓰는가] |

<!-- Semantic이면 값 칸에 alias 대상 primitive를 쓴다: `color/Blue/500` -->
<!-- Typography면 열을 바꾼다: 토큰 | 크기 | 굵기 | 줄높이 | 자간 -->
<!-- Shadow면 열을 바꾼다: 토큰 | 겹 | offset | blur | spread | color -->

## 사용 규칙

- [언제 어느 토큰을 쓰는가, 금지 사항]
