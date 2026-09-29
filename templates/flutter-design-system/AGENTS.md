# {{product}} 디자인 시스템

> 이 패키지에서 작업하는 사람·에이전트가 가장 먼저 읽는 문서다. Flutter 코드 생성 규칙의 상세는 [`lib/AGENTS.md`](lib/AGENTS.md).

## 패키지 개요

- **역할**: {{product}} 앱들이 공유하는 디자인 시스템 패키지 (`package:{{package}}`).
- **소스 오브 트루스**: Figma 디자인 시스템 — {{figma_url}}
  - `docs/foundations/`·`docs/components/`는 Figma와 동기화하는 **framework-neutral Markdown 명세**다.
  - 명세가 먼저, `lib/` 코드는 그다음이다. 명세에 없는 값·컴포넌트를 코드에 임의로 추가하지 않는다.
- **Figma는 읽기 전용**: 에이전트는 Figma를 조회·export만 한다. Figma 쪽 변경이 필요하면 [`docs/handoff.md`](docs/handoff.md)에 인계 항목으로 남긴다.

## 핵심 규칙

1. **네이밍 접두사는 `{{PREFIX}}`** — `{{PREFIX}}Button`, `{{PREFIX}}Colors`, `{{PREFIX}}TextStyle`, `{{PREFIX}}Text` …
2. **토큰 계층은 Figma 변수 컬렉션을 그대로 따른다** — Figma에 Primitive·Semantic 컬렉션이 따로 있으면 Dart도 클래스·파일을 1:1로 나눈다. 컴포넌트·앱은 Semantic을 기본으로 참조한다. 상세와 예외 관리는 [`lib/AGENTS.md`](lib/AGENTS.md) §2.
3. **테마 모드는 Figma 변수 mode로 정한다** — mode가 하나면 라이트 전용으로 두고 런타임 테마 전환 레이어를 만들지 않는다. 결정은 아래 §결정 사항에 기록한다.
4. **상호작용 컴포넌트의 값은 밖에 둔다** — 컨트롤드 + 콜백(`value`+`onChanged`, 버튼류는 `onPressed`). 커스텀 Controller 클래스 금지(Flutter 표준 컨트롤러는 예외). 값에 영향이 없는 탐색·표시 상태는 안에 둘 수 있다. 상세는 [`lib/AGENTS.md`](lib/AGENTS.md) §4.
5. **1 위젯 = 1 파일** — `docs/components/NN-name.md` ↔ `lib/src/components/name/`. 폴더·파일명에 문서 번호(NN)를 붙이지 않는다 — Figma 페이지 번호는 재넘버링이 잦다.
6. **검증** — 시각·골든·일반 위젯 테스트는 두지 않는다. 문서의 접근성 계약은 `test/semantics/`의 Semantics 테스트로 보호하고, 나머지는 정적 분석·[`scripts/verify-docs.mjs`](scripts/verify-docs.mjs)·예제 앱 수동 확인으로 검증한다.

## 결정 사항

패키지를 만들 때 Figma를 보고 정한 값이다. 바뀌면 여기와 [`docs/HISTORY.md`](docs/HISTORY.md)를 함께 고친다.

| 항목 | 결정 | 근거 |
| --- | --- | --- |
| 컬러 계층 | _(예: Primitive → Semantic 2계층)_ | _(Figma 변수 컬렉션 이름·개수)_ |
| 그 외 토큰 계층 | _(예: 타이포·스페이싱·레디우스·섀도우 단일 계층)_ | |
| 테마 모드 | _(예: 라이트 전용)_ | _(Figma 변수 mode 수)_ |
| 상호작용 상태 | _(예: Default/Disabled만 — hover/focus/pressed 없음)_ | _(명세·플랫폼)_ |
| 크기 토큰 | _(예: 토큰 없이 4배수 px 규칙)_ | |

## 토큰 네이밍

상세 규칙과 매핑표는 [`lib/AGENTS.md`](lib/AGENTS.md). 문서 토큰은 Figma 변수 이름을 그대로 쓰고(`color/primary/default`), Dart는 `{{PREFIX}}Colors.primaryDefault`처럼 camelCase로 옮긴다.

## 디렉터리

```
AGENTS.md                ← 이 문서
docs/
  README.md              문서 지도
  HISTORY.md             개발 쪽 결정 이력 (시간 역순)
  handoff.md             디자이너 인계 목록
  foundations/           Figma 동기화 명세 + 00-INDEX.md(구현 트래커) + _TEMPLATE.md
  components/            Figma 동기화 명세 + 00-INDEX.md(구현 트래커) + _TEMPLATE.md
lib/
  AGENTS.md              Flutter 코드 생성 규칙
  {{package}}.dart       public export (배럴)
  src/foundations/       토큰 클래스
  src/components/        컴포넌트 (폴더당 하나)
test/semantics/          접근성 계약 테스트
example/                 컴포넌트 갤러리 앱
scripts/verify-docs.mjs  문서·INDEX·배럴 정합성 검사
```

## 작업 흐름

- **Figma가 바뀌었을 때**: Figma(읽기 전용) 확인 → 명세 md 갱신 → INDEX·HISTORY 갱신 → 코드 반영 → 검증. 명세와 코드를 한 번에 바꾸더라도 명세를 먼저 고친다.
- **Figma와 md 중 어느 쪽이 맞는지 모호하면** 둘 다 고치지 않고 [`docs/handoff.md`](docs/handoff.md)에 불일치를 남긴다.
- **완료 전 확인**: `dart analyze`(또는 `flutter analyze`), `flutter test test/semantics`, `node scripts/verify-docs.mjs`.
