# 컴포넌트: [한글명] ([English Name])

<!--
작성 규칙
- Figma(읽기 전용)에서 확인한 값만 쓴다. 추정하지 않는다 — 확인 못 한 값은 docs/handoff.md에 올리고 이 문서에는 쓰지 않는다.
- 값은 토큰 이름으로 쓴다(`color/primary/default`, `spacing/16`). 토큰에 바인딩되지 않은 원시 값이 Figma에 있으면 그대로 적고 handoff에 "토큰 미바인딩"으로 올린다.
- framework-neutral로 쓴다. Flutter 클래스·파라미터 이름을 쓰지 않는다 — 그건 lib/AGENTS.md와 코드의 몫이다.
- 도구·세션 기록("MCP로 확인함" 등)을 남기지 않는다. 이력은 docs/HISTORY.md에.
- 해당 없는 절은 지운다. 이 주석도 지운다.
-->

## 개요

[무엇을 하는 컴포넌트인지 1~2문장. 비슷한 컴포넌트와 구분되는 점.]

> 참조: Figma 페이지 `NN — [Name]`, 세트 `[Component Set]` ([축] × [축] = N variant).

---

## 변형

| 축 | 값 |
| --- | --- |
| **[Style]** | `[Primary]` / `[Secondary]` |
| **[Size]** | `[Large]` / `[Medium]` |
| **Disabled** | `False` / `True` |

→ N × N × 2 = **N variant**. (기본값 `[Style]=[Primary]` · `[Size]=[Large]` · `Disabled=False`)

## 사이즈

| Size | 높이 | 패딩 (좌우 / 상하) | 타이포 | 아이콘 |
| --- | --- | --- | --- | --- |
| **[Large]** | [N]px | `spacing/[n]` / `spacing/[n]` | `text/[role]/[role]-[px]` | [N]px |

## 색상 (변형 × 상태)

| | 배경 | 텍스트·아이콘 | 보더 |
| --- | --- | --- | --- |
| **[Primary]** | `color/[...]` | `color/[...]` | — |
| **[Primary] + Disabled** | `color/[...]` | `color/[...]` | — |

## 토큰 바인딩

| 속성 | 바인딩 |
| --- | --- |
| cornerRadius | `radius/[n]` |
| gap | `spacing/[n]` |
| 배경 fill | … |

## 구성 요소 · 아이콘

| 요소 | 표시 조건 | 내용 |
| --- | --- | --- |
| Leading Icon | `Show Leading` = true | `01 — Icons`의 UI 아이콘, 색은 텍스트와 동일 |

## 레이아웃 규칙

- [Hug / Fill, 최소·최대 너비, 줄바꿈·말줄임 규칙 등]

## 접근성 계약

| 항목 | 계약 |
| --- | --- |
| role | `[button / checkbox / …]` |
| name | [어디서 오는가 — 라벨 텍스트, 별도 레이블 등] |
| state | [`Disabled=True`은 `disabled` 등] |
| action | `activate` |

## 사용 원칙

| 원칙 | 설명 |
| --- | --- |
| [언제 쓰나] | [다른 컴포넌트 대신 이것을 쓰는 경우] |
