---
name: ui-sprint-contract
description: "This skill should be used when the user wants to create a UI Sprint Contract, convert a Figma design or CSS to a Flutter spec, asks to document a UI design for development, mentions 'sprint contract', or uploads a design screenshot for Flutter implementation."
argument-hint: "<screen-name> [figma-url or description]"
allowed-tools: [Read]
---

# UI Sprint Contract 생성 스킬

디자인 인풋(Figma 스크린샷, CSS, 텍스트 설명)을 받아 PlusVet의 Flutter 디자인 시스템에 맞는 Sprint Contract를 작성합니다.

## 실행 순서

### Step 1: 디자인 시스템 로드

`references/design_system.md`를 Read하여 PlusVet 디자인 시스템(DColors, DTextSize, DSize, DStyle, 컴포넌트 목록)을 파악합니다.

### Step 2: 출력 템플릿 로드

`assets/sprint_contract_template.md`를 Read하여 Sprint Contract의 출력 구조를 파악합니다.

### Step 3: 인풋 분석

사용자가 제공한 인풋을 분석합니다:

- **Figma 스크린샷**: 화면에 보이는 요소를 하나씩 식별 — 레이아웃, 텍스트, 버튼, 입력창, 아이콘, 색상, 간격
- **CSS**: `background-color`, `font-size`, `font-weight`, `border-radius`, `padding` 등의 값을 디자인 토큰으로 매핑
- **텍스트 설명**: 요구사항을 레이아웃과 컴포넌트 단위로 분해

### Step 4: 디자인 토큰 매핑

분석한 디자인 요소를 PlusVet 디자인 시스템에 매핑합니다.

**색상 매핑 기준:**
- `#0093FF` 또는 blue 계열 CTA → `DColors.blue`
- `#E83636` 또는 red/error → `DColors.red`
- `#151515` 또는 진한 텍스트 → `DColors.text`
- `#647585` 또는 보조 텍스트 → `DColors.deepGray`
- `#ECEEF5` 또는 연한 회색 배경 → `DColors.smoke`
- `#F7FAFC` 또는 페이지 배경 → `DColors.mist`
- `#D3D5E1` 또는 구분선 → `DColors.lightGray`
- 정확히 매핑되지 않으면 가장 가까운 토큰 선택 후 Open Questions에 기록

**폰트 크기 매핑 기준:**
- 정확히 일치하는 `DTextSize` 토큰 우선 선택
- Bold(700) → B suffix, Medium(500) → M suffix
- 예: `font-size: 14px; font-weight: 500` → `DTextSize.text14M`
- 정확한 크기가 없으면 가장 가까운 값 선택하고 주석 추가

**컴포넌트 선택 기준:**
- 직사각형 버튼 → `DBasicButton`
- 알약형 버튼 → `DRoundButton`
- 텍스트 입력 → `DInputField`
- 체크박스 → `DCheckBox`
- 스위치 → `DToggle`
- 탭 바 → `D{Outlined|Rounded|Text}TabGroup`
- 카드/컨테이너 → `DCard`
- 구분선 → `DDivider`
- 아이콘 → `DSvgIcon(DSvgIcons.XXX)`
- 배지/카운트 → `DBadge`

**사이즈 선택 기준:**
- height ≈ 60px → `DSize.l`
- height ≈ 47px → `DSize.m`
- height ≈ 34px → `DSize.s`
- height ≈ 25px → `DSize.xs`

### Step 5: Sprint Contract 작성

`assets/sprint_contract_template.md`의 구조를 그대로 따라 Sprint Contract를 작성합니다.

**필수 규칙:**
- 모든 위젯 이름은 `packages/ui`의 실제 클래스명 사용 (임의로 만들지 않기)
- 색상은 반드시 `DColors.xxx` 토큰으로 표기 (hex 직접 사용 금지)
- 폰트는 반드시 `DTextSize.textXXX` 토큰으로 표기
- 크기는 반드시 `DSize.{l|m|s|xs}`로 표기
- 디자인 시스템에 없는 커스텀 요소는 Implementation Notes에 `[커스텀 필요]`로 명시
- 불확실한 부분은 추정 후 Open Questions에 기록

### Step 6: 최종 출력

완성된 Sprint Contract를 마크다운으로 출력합니다.
출력 후 다음을 안내합니다:
- Open Questions 중 디자이너/기획자가 답변해야 하는 항목
- 디자인 시스템에서 정확히 매핑되지 않은 항목 (있는 경우)
