# Sprint Contract: {화면/컴포넌트 이름}

> **버전**: 1.0 | **작성일**: {날짜} | **작성자**: {이름}
> **입력 소스**: {Figma URL / CSS 원본 / 스크린샷 첨부}

---

## 1. Overview

| 항목 | 내용 |
|------|------|
| **목적** | 이 화면/컴포넌트의 역할과 사용 맥락 |
| **화면 유형** | `Page` / `Dialog` / `BottomSheet` / `Component` |
| **진입 경로** | 어디서 이 화면으로 오는가 |
| **우선순위** | `P0` (즉시) / `P1` (이번 스프린트) / `P2` (다음 스프린트) |

---

## 2. Layout Structure

전체 레이아웃을 계층 구조로 기술합니다.

```
{예시:}
Scaffold
  └── AppBar
       └── title: "{화면 제목}"
  └── Body: Column
       ├── {섹션 A}: Row
       │    ├── {요소 1}
       │    └── {요소 2}
       ├── DDivider
       └── {섹션 B}: ListView
            └── {리스트 아이템} × N
  └── BottomBar
       └── DBasicButton.l("확인", style: DStyle.point)
```

> 주의: 스크롤 영역, 고정 영역(AppBar/BottomBar)을 명확히 구분할 것.

---

## 3. Component Specifications

각 UI 요소를 아래 테이블에 기술합니다.

| # | 역할 | Widget | Size | Style | 주요 Props |
|---|------|--------|------|-------|-----------|
| 1 | CTA 버튼 | `DBasicButton` | `DSize.l` | `DStyle.point` | `text: "저장"`, `width: double.infinity` |
| 2 | 취소 버튼 | `DBasicButton` | `DSize.m` | `DStyle.sub` | `text: "취소"` |
| 3 | 이름 입력 | `DInputField` | `DSize.m` | — | `label: "이름"`, `required: true`, `hintText: "이름을 입력하세요"` |
| 4 | 동의 체크 | `DCheckBox` | `DSize.s` | — | `label: "약관에 동의합니다"`, `checked: false` |
| 5 | 섹션 제목 | `DText` | `text17B` | — | `color: DColors.text` |
| 6 | 구분선 | `DDivider` | — | — | 기본 |

> 모든 위젯 이름은 `packages/ui`의 실제 클래스명을 사용할 것.

---

## 4. Design Tokens

### Colors
| 용도 | Token | Hex |
|------|-------|-----|
| 배경 | `DColors.mist` | `#F7FAFC` |
| 기본 텍스트 | `DColors.text` | `#151515` |
| 보조 텍스트 | `DColors.deepGray` | `#647585` |
| 구분선 | `DColors.lightGray` | `#D3D5E1` |
| 강조 | `DColors.blue` | `#0093FF` |
| 경고 | `DColors.red` | `#E83636` |

### Typography
| 용도 | Token | Size/Weight |
|------|-------|-------------|
| 페이지 제목 | `DTextSize.text20B` | 20px Bold |
| 섹션 제목 | `DTextSize.text17B` | 17px Bold |
| 본문 | `DTextSize.text14M` | 14px Medium |
| 보조 텍스트 | `DTextSize.text12M` | 12px Medium |

### Spacing
| 항목 | 값 |
|------|-----|
| 화면 좌우 여백 | 20px (`horizontalEdgeInset`) |
| 섹션 간격 | 24px |
| 컴포넌트 간격 | 12px |
| 카드 내부 여백 | `DSize.m.padding` (v:10, h:15) |

---

## 5. States & Interactions

각 인터랙티브 요소의 상태를 정의합니다.

### {요소명 예: 저장 버튼}
| 상태 | 설명 |
|------|------|
| **Normal** | `DStyle.point` — blue bg, white text |
| **Pressed** | opacity 0.8 (DDisabledWrapper 처리) |
| **Disabled** | `disabled: true` — opacity 0.4 |
| **Loading** | 버튼 비활성화 + 로딩 인디케이터 표시 |

### {요소명 예: 입력 필드}
| 상태 | 설명 |
|------|------|
| **Empty** | `hintText` 표시 |
| **Focused** | border highlight (blue) |
| **Filled** | 입력된 텍스트 표시 |
| **Error** | `errorText` 표시, red border |
| **Disabled** | `readOnly: true` |

---

## 6. Data & API

| 항목 | 내용 |
|------|------|
| **필요 데이터** | 이 화면에 표시할 데이터 목록 |
| **API 연동** | 연관된 API endpoint 또는 BLoC/Provider |
| **로컬 상태** | 화면 내부에서만 관리하는 상태 |

---

## 7. Implementation Notes

- [ ] 특이사항 1 (예: 스크롤 시 AppBar 축소 효과 필요)
- [ ] 특이사항 2 (예: 리스트 아이템 Drag & Drop 필요 → `DReorderableListView` 사용)
- [ ] 애니메이션 (예: 버튼 전환 200ms transition)
- [ ] 접근성 (예: 스크린리더 label 지정 필요)
- [ ] 다크모드 대응 여부

---

## 8. Open Questions

개발 시작 전 확인이 필요한 사항을 기록합니다.

- [ ] Q1: {질문 내용} — 담당자: {이름}
- [ ] Q2: {질문 내용} — 담당자: {이름}

---

## 9. Figma / Reference Links

| 자료 | 링크 |
|------|------|
| Figma 원본 | {URL} |
| 관련 화면 | {URL} |
| 디자인 가이드 | {URL} |
