# PlusVet Design System Reference

This document describes the PlusVet UI design system defined in `packages/ui`. When writing a Sprint Contract, map all design elements to these tokens and components.

---

## 1. Colors — `DColors`

Usage: `DColors.{name}.color`

### Grayscale
| Token | Hex | Visual |
|-------|-----|--------|
| `DColors.white` | `#FFFFFF` | White |
| `DColors.text` | `#151515` | Near-black (default text) |
| `DColors.logoBg` | `#1F242D` | Dark navy (logo background) |
| `DColors.deepGray` | `#647585` | Medium-dark gray (secondary text) |
| `DColors.gray` | `#8B98A5` | Medium gray (placeholder, icons) |
| `DColors.lightGray` | `#D3D5E1` | Light gray (borders, dividers) |
| `DColors.smoke` | `#ECEEF5` | Very light gray (sub button bg, disabled bg) |
| `DColors.mist` | `#F7FAFC` | Near-white (page/card background) |

### Brand Colors
| Token | Hex | Use Case |
|-------|-----|----------|
| `DColors.blue` | `#0093FF` | Primary / Point (CTA buttons, active states) |
| `DColors.lightBlue` | `#BAECFF` | Light blue (highlights, tags) |
| `DColors.deepBlue` | `#006CCF` | Dark blue (pressed state) |
| `DColors.skyBlue` | `#C1DCFC` | Sky blue (subtle accents) |
| `DColors.deepSkyBlue` | `#7DB4F5` | Medium blue |
| `DColors.red` | `#E83636` | Warning / Error / Danger |
| `DColors.lightRed` | `#FFA8A8` | Light red (error highlight) |
| `DColors.deepRed` | `#BE1818` | Deep red |
| `DColors.green` | `#05B92D` | Success / Positive |
| `DColors.lightGreen` | `#9CDCAA` | Light green |
| `DColors.yellow` | `#FCB318` | Caution / Warning (mild) |
| `DColors.lightYellow` | `#FFE4AB` | Light yellow |
| `DColors.orange` | `#FF830E` | Orange accent |
| `DColors.brown` | `#C07E30` | Brown |
| `DColors.lightBrown` | `#E8C7A1` | Light brown |
| `DColors.purple` | `#9A40E0` | Purple accent |
| `DColors.lightPurple` | `#D3A9F3` | Light purple |
| `DColors.khaki` | `#9BC100` | Khaki/Olive |
| `DColors.turquoise` | `#02C4EE` | Turquoise |
| `DColors.pink` | `#EE488E` | Pink |

### Special Purpose (Overlays)
| Token | Value | Use Case |
|-------|-------|----------|
| `DColors.cover` | white 70% | Content overlay |
| `DColors.coverHover` | white 50% | Hover overlay |
| `DColors.dim` | black 40% | Modal backdrop |
| `DColors.dimLight` | black 10% | Subtle dimming |
| `DColors.barrier` | black 40% | Full-screen barrier |

---

## 2. Typography — `DTextSize`

Usage: `DText.{textXXX}("label")` or `DTextSize.textXXB`

Font: **Pretendard** | Weight: B = bold (700), M = medium (500)

### For Headings / Large Display
| Token | Size | Line Height | Weight |
|-------|------|-------------|--------|
| `DTextSize.text55B` | 55px | 88 | Bold |
| `DTextSize.text40B` | 40px | 64 | Bold |
| `DTextSize.text35M` | 35px | 56 | Medium |
| `DTextSize.text30B` | 30px | 48 | Bold |
| `DTextSize.text23B` | 23px | 37 | Bold |
| `DTextSize.text23M` | 23px | 37 | Medium |

### For Components (Most Common)
| Token | Size | Line Height | Weight | DSize Equivalent |
|-------|------|-------------|--------|-----------------|
| `DTextSize.text20B` | 20px | 32 | Bold | DSize.l (bold) |
| `DTextSize.text20M` | 20px | 32 | Medium | DSize.l (medium) |
| `DTextSize.text17B` | 17px | 27 | Bold | DSize.m (bold) |
| `DTextSize.text17M` | 17px | 27 | Medium | DSize.m (medium) |
| `DTextSize.text15B` | 15px | 24 | Bold | — |
| `DTextSize.text15M` | 15px | 24 | Medium | — |
| `DTextSize.text14B` | 14px | 22 | Bold | DSize.s (bold) |
| `DTextSize.text14M` | 14px | 22 | Medium | DSize.s (medium) |
| `DTextSize.text13B` | 13px | 21 | Bold | — |
| `DTextSize.text13M` | 13px | 21 | Medium | — |
| `DTextSize.text12B` | 12px | 19 | Bold | DSize.xs (bold) |
| `DTextSize.text12M` | 12px | 19 | Medium | DSize.xs (medium) |
| `DTextSize.text11B` | 11px | 18 | Bold | — |
| `DTextSize.text11M` | 11px | 18 | Medium | — |
| `DTextSize.text10M` | 10px | 16 | Medium | — |

### Kiosk / Large Display (특수 목적)
`text65B`, `text50B`, `text50M`, `text45B`, `text30M` — 일반 모바일 화면에는 사용하지 않음.

### Text Type + Size Matrix (DTextType)
`DTextType`으로 역할 기반 텍스트 크기를 정의할 수 있음:

| DTextType | XS | S | M | L |
|-----------|-----|---|---|---|
| `subText` | text11M | text12M | text14M | text23M |
| `body` | text12M | text14M | text17M | text30M |
| `bodyLarge` | text14M | text17M | text20M | text35M |
| `title` | text17B | text20B | text23B | text45B |

---

## 3. Sizing System — `DSize`

모든 컴포넌트는 DSize enum으로 크기를 통일해 관리.

| Property | `DSize.l` | `DSize.m` | `DSize.s` | `DSize.xs` |
|----------|-----------|-----------|-----------|------------|
| Height | 60px | 47px | 34px | 25px |
| Border Radius | 9px | 7px | 5px | 3px |
| Vertical Padding | 14px | 10px | 6px | 3px |
| Horizontal Padding | 19px | 15px | 11px | 7px |
| Text (Bold) | text20B | text17B | text14B | text12B |
| Text (Medium) | text20M | text17M | text14M | text12M |

---

## 4. Button Styles — `DStyle`

`DBasicButton`에서 사용하는 스타일 enum.

| Style | Background | Text Color | Use Case |
|-------|-----------|------------|----------|
| `DStyle.point` | `DColors.blue` | white | Primary CTA |
| `DStyle.sub` | `DColors.smoke` | `DColors.deepGray` | Secondary action |
| `DStyle.text` | transparent | `DColors.deepGray` | Tertiary / Text button |
| `DStyle.warning` | `DColors.red` | white | Destructive action |

---

## 5. Component Catalog

### Buttons

#### `DBasicButton` — 직사각형 버튼
```
DBasicButton.{l|m|s|xs}(
  "label",
  style: DStyle.{point|sub|text|warning},
  onTap: () {},
  disabled: false,
  width: null,  // null = wrap content
)
```
- 모든 DSize 지원 (l, m, s, xs)
- `width` 지정 시 full-width 가능

#### `DRoundButton` — 알약형(Pill) 버튼
```
DRoundButton.{m|s|xs}(
  "label",
  style: DRoundButtonStyle.{primary|gray|transparent},
  designIcon: DSvgIcons.Plus,   // optional
  reversed: false,               // icon 우측 배치
  subText: "",                   // 부제 텍스트
  onTap: () {},
  disabled: false,
)
```
- DSize.l 미지원
- `DRoundButtonStyle.primary` = blue bg / white text
- `DRoundButtonStyle.gray` = smoke bg / deepGray text
- `DRoundButtonStyle.transparent` = no bg / deepGray text

#### `DOutlineButton` — 아웃라인 버튼 (custom)
- 테두리만 있는 버튼 스타일

---

### Form Controls

#### `DInputField` — 텍스트 입력 필드
```
DInputField.{l|m|s|xs}(
  controller,
  label: "라벨",         // optional
  hintText: "힌트",
  required: false,
  readOnly: false,
  errorText: null,
  useClearMode: false,   // X 버튼으로 전체 삭제
  autoGrow: false,       // 내용 따라 높이 자동 확장
  minLines: 1,
  maxLines: null,
  expands: false,        // 부모 높이 채우기
  heightScaleFactor: 1,  // 고정 줄 수 기반 높이
  keyboardType: TextInputType.text,
  textAlign: TextAlign.start,
  suffixText: null,
  onChanged: (v) {},
  onTap: null,           // readOnly일 때 사용
)
```

#### `DCheckBox` — 체크박스
```
DCheckBox.{l|m|s|xs}(
  checked: false,
  label: "라벨",                    // optional
  labelTextType: DTextType.body,
  onCheckChanged: (checked) {},
  disabled: false,
)
```

#### `DToggle` — 스위치 토글
```
DToggle.{xs|m}(
  value: false,
  onChanged: (v) {},
)
```
- m 사이즈는 ON/OFF 텍스트 표시

#### `DRadioButton` — 라디오 버튼
- 단일 선택 옵션

---

### Display / Layout

#### `DText` — 텍스트 위젯
```
DText.{textSizeName}(
  "텍스트",
  color: DColors.text.color,   // optional
  maxLines: 1,
  overflow: TextOverflow.ellipsis,
)
```
예: `DText.text14M("서브텍스트", color: DColors.deepGray.color)`

#### `DCard` — 카드 컨테이너
```
DCard.{xs|s|m|l}(
  child: ...,
  borderColor: DColors.lightGray.color,
  backgroundColor: DColors.white.color,
  onTap: () {},
)
```

#### `DDivider` — 구분선
- 수평/수직 divider
- 기본 색상 `DColors.smoke`

#### `DBadge` — 뱃지/카운트
```
DBadge.{s|xs}(
  count: 5,
  backgroundColor: DColors.blue.color,
)
```
- dot 모드 지원 (count 없이 점만)

#### `DCircle` — 원형 컨테이너
- 아이콘/아바타 배경으로 사용

---

### Navigation / Selection

#### `DOutlinedTabGroup` — 아웃라인 탭
#### `DRoundedTabGroup` — 둥근 탭 (pill-style)
#### `DTextTabGroup` — 텍스트 탭
```
D***TabGroup(
  tabs: [DTab(id: "a", label: "탭1"), ...],
  selectedId: "a",
  onSelected: (id) {},
)
```

#### `DDropDownButton` — 드롭다운 (design system)
#### `DTextDropdownButton` — 텍스트 드롭다운 (custom)

---

### Overlays

#### `DDialog` — 기본 다이얼로그
#### `DSimpleDialog` — 단순 메시지 다이얼로그
#### `DChoiceDialog` — 선택 다이얼로그 (단일/다중 선택)

#### `DBottomSheet` — 바텀시트
#### `DFloatingBottomSheet` — 플로팅 바텀시트

#### `DToast` — 토스트 메시지
```
DToast.show(context, message: "저장되었습니다.");
```

---

### Icons — `DSvgIcon` / `DSvgIcons`

```
DSvgIcon(
  DSvgIcons.Plus,
  color: DColors.blue.color,
  size: 20,
)
```

주요 아이콘 목록:
`AddReservation`, `Alarm`, `ArrowLeft`, `ArrowRight`, `Back`, `Calendar`, `Chart`, `Chat`, `Check`, `CheckCircle`, `Close`, `CloseCircle`, `Delete`, `Edit`, `Filter`, `Folder`, `Graph`, `Help`, `History`, `Home`, `Image`, `Information`, `Lock`, `Mail`, `Menu`, `Minus`, `MinusCircle`, `More`, `Paper`, `Pen`, `People`, `Phone`, `Plus`, `PlusCircle`, `Print`, `Profile`, `Refresh`, `Save`, `Schedule`, `Search`, `Send`, `Settings`, `Share`, `Star`, `Time`, `Upload`, `Warning` 등 100+ 아이콘

기타 SVG 카테고리:
- `DSvgFace` — 동물 얼굴 아이콘
- `DSvgBuilding` — 건물/시설 아이콘
- `DSvgObjectIcon` — 오브젝트 아이콘
- `DSvgPlayer` — 애니메이션 플레이어

---

## 6. Layout Patterns

### 공통 가로 여백
```dart
const EdgeInsets horizontalEdgeInset = EdgeInsets.symmetric(horizontal: 20);
```

### 기본 아이콘 사이즈
```dart
const double defaultIconSize = 25;
```

### 기본 트랜지션
```dart
const Duration defaultTransitionDuration = Duration(milliseconds: 200);
```

### 일반적인 페이지 레이아웃
```
Scaffold
  └── Column
       ├── AppBar (또는 커스텀 헤더)
       ├── Expanded
       │    └── SingleChildScrollView / ListView
       │         └── Padding(horizontal: 20)
       │              └── 콘텐츠
       └── BottomBar (버튼 등)
```

### 카드 리스트 패턴
```
ListView.separated
  item: DCard.m(...)
  separator: DDivider() 또는 SizedBox(height: N)
```

---

## 7. 다크모드

다크모드는 `DColors$Dark` / `DStaticColors$Dark`로 정의됨.
Sprint Contract 작성 시 라이트모드 기준으로 작성하고, 다크모드 대응 필요 여부를 Implementation Notes에 명시.
