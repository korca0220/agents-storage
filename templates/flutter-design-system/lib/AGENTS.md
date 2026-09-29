# lib/ — Flutter/Dart 코드 생성 규칙

> Figma가 SSOT이고 `docs/`는 그 명세다. 이 문서는 **확정된 명세만** Flutter 코드로 옮기는 규칙이다. 명세에 없는 값·컴포넌트를 추가하지 않는다. 명세가 비어 있거나 모순이면 코드로 메우지 말고 [`../docs/handoff.md`](../docs/handoff.md)에 올린다.

## 1. 네이밍

- public 클래스는 `{{PREFIX}}` 접두사: `{{PREFIX}}Button`, `{{PREFIX}}Colors`, `{{PREFIX}}TextStyle` …
- 파일명은 snake_case + `{{prefix}}_` 접두사: `{{prefix}}_button.dart`, `{{prefix}}_colors.dart`.
- 컴포넌트당 폴더 하나: `lib/src/components/button/{{prefix}}_button.dart`.
  - 문서 하나가 위젯 여러 개를 다루면 같은 폴더 안에서 위젯별로 파일을 나눈다.
- 폴더·파일명에 문서 번호(NN)를 붙이지 않는다.

## 2. 토큰 클래스 패턴

토큰은 인스턴스화할 수 없는 static holder로 만든다.

```dart
abstract final class {{PREFIX}}Spacing {
  {{PREFIX}}Spacing._();

  static const x4 = 4.0;
}
```

### 2-1. Color

**Figma 변수 컬렉션 구조를 그대로 옮긴다.** Primitive·Semantic 컬렉션이 따로 있으면 클래스와 파일도 나눈다.

| 레이어 | Figma 컬렉션 | Dart 클래스 | 파일 | 배럴 export |
| --- | --- | --- | --- | --- |
| Primitive | _(예: `Color / Primitives`)_ | `{{PREFIX}}PrimitiveColors` | `{{prefix}}_primitive_colors.dart` | **하지 않는다** |
| Semantic | _(예: `Color / Semantic`)_ | `{{PREFIX}}Colors` | `{{prefix}}_colors.dart` | 한다 |

```dart
// {{prefix}}_colors.dart — semantic은 primitive를 alias로 가리킨다
abstract final class {{PREFIX}}Colors {
  {{PREFIX}}Colors._();

  static const primaryDefault = {{PREFIX}}PrimitiveColors.blue500;
}
```

- 매핑: `color/primary/default` → `{{PREFIX}}Colors.primaryDefault` (`color/` 접두사를 떼고 그룹+역할을 camelCase). `color/Blue/500` → `blue500`.
- **Primitive 직접 참조는 명세가 primitive를 지정한 곳에서만** 허용한다 — 색 자체가 변형 축이거나 디자이너가 semantic 치환을 배제한 고정색인 경우다. 허용 목록을 아래 표로 관리하고, 표에 없는 위치의 primitive 참조는 위반이다.

  | 위치 | 명세 | 문서 | 근거 |
  | --- | --- | --- | --- |
  | _(없으면 비워 둔다)_ | | | |

- 감사: `grep -rl "{{prefix}}_primitive_colors" lib/src/components/` 결과 수가 위 표의 컴포넌트 수와 같아야 한다. 그래서 두 클래스를 한 파일로 합치거나 `part`로 묶지 않는다 — import 줄이 감사 훅이다.
- Primitive를 배럴에서 export하지 않는다. 앱이 primitive를 원하면 그 화면에 필요한 것은 디자인 시스템 컴포넌트라는 신호다.
- Figma에 컬렉션이 하나뿐이면 `{{PREFIX}}Colors` 하나로 두고 이 절의 예외 표는 지운다.

### 2-2. Typography

```dart
abstract final class {{PREFIX}}TextStyle {
  {{PREFIX}}TextStyle._();

  static const _family = '{{font_family}}';

  /// text/body/body-17 — 17px / Medium / LH130%
  static const body17 = TextStyle(
    fontSize: 17,
    fontWeight: FontWeight.w500,
    height: 1.30,
    letterSpacing: 0,
    leadingDistribution: TextLeadingDistribution.even,
    fontFamily: _family,
    package: '{{package}}',
  );
}
```

- 매핑: `text/{역할}/{역할}-{px}` → `{{PREFIX}}TextStyle.{역할}{px}` (하이픈은 camelCase).
- **`letterSpacing`·`leadingDistribution: even`은 기본값 같아 보여도 반드시 적는다.** 비워 두면 Material `DefaultTextStyle`의 자간(0.25 등)이 병합되고, Flutter 기본 leading 분배(`proportional`)가 Figma의 위아래 균등 분배와 달라 baseline이 어긋난다.
- 패키지가 폰트를 선언하므로 모든 스타일에 `package: '{{package}}'`를 지정한다.

### 2-3. Text / Theme

- `{{PREFIX}}Text`는 `{{PREFIX}}TextStyle`로 문자열을 그리는 편의 위젯이다. Figma 컴포넌트가 아니므로 컴포넌트 수에 넣지 않는다. 역할명과 같은 named constructor를 두고, 크기·굵기·줄높이 재정의 API를 열지 않는다. 색 기본값은 `{{PREFIX}}Colors.textPrimary`처럼 semantic으로 둔다.
- `{{PREFIX}}Theme.light()`는 Material `TextTheme` 슬롯을 전부 `{{PREFIX}}TextStyle`로 채운다. 폰트만 바꾸고 Material 기본 메트릭을 남기면 `{{PREFIX}}Text`를 거치지 않는 텍스트(일반 `Text`, `TextField` 힌트, `SnackBar`·`Dialog`)가 스펙 밖으로 그려진다. 매핑은 패밀리 안에서 크기 내림차순으로 한다.

### 2-4. Spacing / Radius

- 숫자 스케일은 `x{n}` 접두로 통일한다: `spacing/24` → `{{PREFIX}}Spacing.x24`, `radius/12` → `{{PREFIX}}Radius.x12`. `radius/full`은 `xFull`(예: `9999.0`).
- 값 타입은 `double`.
- 크기 토큰이 Figma에 없으면 클래스를 만들지 않고 명세의 px 리터럴을 쓴다.

### 2-5. Shadow

- `Elevation/1` → `{{PREFIX}}Shadow.elevation1`처럼 `List<BoxShadow>` 상수로 둔다. Figma의 DROP_SHADOW 겹 수·순서를 그대로 옮긴다.

## 3. 공개 API

- 배럴(`lib/{{package}}.dart`)은 semantic 컬러와 단일 계층 토큰, 컴포넌트를 export한다. primitive는 export하지 않는다.
- 패키지 밖은 `package:{{package}}/{{package}}.dart`만 import한다. `src/` 직접 import 금지.
- 문자열 렌더링은 `{{PREFIX}}Text`를 쓰고, `TextField.style`처럼 `TextStyle`을 요구하는 API에서만 `{{PREFIX}}TextStyle`을 직접 쓴다.

## 4. 상호작용 컴포넌트 상태

```dart
class {{PREFIX}}Toggle extends StatelessWidget {
  const {{PREFIX}}Toggle({super.key, required this.value, required this.onChanged, this.disabled = false});

  final bool value;
  final ValueChanged<bool> onChanged; // non-null 필수
  final bool disabled;                // true = disabled 토큰 렌더 + 입력 무시
}
```

- **값 상태는 밖에 둔다.** 무엇을 골랐는지·켰는지는 호출부가 가진다. 커스텀 Controller 클래스를 만들지 않는다(Flutter 표준 컨트롤러는 예외).
- **탐색·표시 상태는 안에 둘 수 있다.** 판별 기준: 호출부가 그 값을 읽어 무언가 판단하는가. 읽지 않고 콜백으로 받아 되돌려주기만 한다면 안에 둔다. 초기화가 필요하면 호출부가 `Key`로 새로 만든다.
- **disabled는 명시적 `bool` 필드**로 표현한다. 콜백은 non-null 필수이고, `disabled: true`면 disabled 토큰으로 그리고 입력을 무시한다(`Semantics.enabled: false` 포함). 콜백 `null` = disabled 관례는 쓰지 않는다.
  - 예외: 복합 컴포넌트가 하위 기능 유무를 nullable 콜백으로 표현하는 것은 허용한다(예: 행 선택 미지원 = `onRowSelected: null`).
- 명세에 없는 hover/focus/pressed 상태를 만들지 않는다. Disabled 시각 처리는 명세를 따른다 — 명세가 opacity를 지정했을 때만 `Opacity`를 쓴다.

## 5. Variant / Size

- 변형 축은 **enum**으로: `{{PREFIX}}ButtonStyle { primary, secondary }`, `{{PREFIX}}ButtonSize { large, medium }`. 문자열 variant 금지.
- Figma variant 축 값을 lowerCamelCase로 그대로 옮긴다.
- State가 Default/Disabled뿐이면 State enum을 만들지 않고 §4의 `disabled` 필드로 충분하다.

## 6. 아이콘 슬롯

Figma의 `BOOLEAN`(표시 여부) + `INSTANCE_SWAP`(아이콘 교체) 조합은 **nullable 아이콘 데이터 파라미터 하나**로 합친다.

```dart
final {{PREFIX}}IconData? leadingIcon; // null = 표시 안 함
```

- 아이콘 색은 컴포넌트가 상태별 토큰으로 주입한다 — 호출부가 색을 정하지 않는다. 그래서 슬롯 타입을 임의 `Widget`이 아니라 아이콘 데이터로 좁힌다.
- 슬롯에 아이콘이 아닌 컴포넌트(프로필 등)도 들어가는 명세면 `Widget?`을 쓴다.
- 아이콘 자산은 Figma의 확정 컴포넌트를 SVG로 export한 것만 쓴다. 캡처·재드로잉·추정 SVG 금지.

## 7. 레이아웃과 보더

`Container`는 `decoration`의 보더 두께를 패딩에 합산한다. 명세 크기·패딩이 보더 유무와 무관해야 하면 배경·라디우스는 `decoration`, 보더는 `foregroundDecoration`으로 나누거나 `DecoratedBox` + `Padding`을 쓴다.

## 8. 테스트 정책

- 시각·골든·일반 위젯 테스트는 두지 않는다.
- 명세의 **접근성 계약 표**(role·name·state·action)를 `test/semantics/`의 Semantics 테스트로 보호한다. `matchesSemantics`로 계약 항목만 단언한다.
- `test/semantics/coverage_matrix_test.dart`가 모든 컴포넌트 문서 번호를 다음 넷 중 하나로 분류한다. 컴포넌트를 추가·삭제하면 이 표도 고친다.

  | 분류 | 뜻 |
  | --- | --- |
  | `contract` | 자기 Semantics 계약을 가지며 테스트한다 |
  | `conditional` | 슬롯 구성에 따라 계약이 달라진다 — 대표 구성만 테스트한다 |
  | `delegated` | 자기 노드가 없고 부모·자식 컴포넌트가 계약을 가진다 |
  | `excluded` | 장식·구조 전용이라 접근성 노드를 노출하지 않는다 |

## 9. 미해결 이슈

명세 공백·구현 보류 항목만 적는다. 디자이너 확인이 필요한 것은 [`../docs/handoff.md`](../docs/handoff.md)로 보낸다.

| 항목 | 현재 상태 / 후속 결정 |
| --- | --- |
| | |
