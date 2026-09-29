---
name: design-system-creator
description: >-
  Figma 디자인 시스템(URL·파일·노드)을 원본으로 받아 templates/flutter-design-system 템플릿으로
  Flutter 디자인 시스템 패키지를 새로 만든다 — 템플릿 복사·치환, Figma 인벤토리, framework-neutral
  명세(md) 작성, 토큰·컴포넌트 코드 생성, Semantics 계약 테스트, 정합성 검증, 디자이너 인계까지.
  "디자인 시스템 만들어줘", "이 피그마로 ui 패키지 만들어줘", "design system 생성", Figma 디자인 시스템
  링크와 함께 패키지를 새로 만들자는 요청에 사용한다. 이미 있는 패키지를 Figma에 맞춰 고치는 일에는 쓰지 않는다.
---

# 디자인 시스템 생성 (design-system-creator)

Figma 디자인 시스템을 **원본(SSOT)**으로, [`templates/flutter-design-system`](../../templates/flutter-design-system/TEMPLATE.md) 구조의 Flutter 패키지를 만든다. 순서는 **명세 먼저, 코드는 그다음**이다.

템플릿 위치: 이 스킬 파일 기준 `../../templates/flutter-design-system/`(agents-storage 레포 구조). 스킬만 따로 설치돼 있어 그 경로가 없으면 `https://github.com/korca0220/agents-storage`를 임시 폴더에 clone해 템플릿을 가져온다.

## 절대 경계

- **Figma는 읽기 전용이다.** 메타데이터·변수·스타일·스크린샷·SVG export만 한다. 노드·변수·스타일을 생성·수정·삭제하는 API를 호출하지 않는다. 사용자가 Figma 수정을 요청해도 직접 하지 않고 `docs/handoff.md`에 올린다.
- **값을 추정하지 않는다.** Figma에서 확인한 값만 명세에 쓴다. 확인 못 한 값은 handoff에 올리고 명세·코드 어디에도 채워 넣지 않는다.
- **명세에 없는 것을 코드에 만들지 않는다.** 명세가 비었거나 모순이면 멈추고 handoff에 올린다.
- 이 스킬은 **새 패키지 생성**용이다. 기존 패키지 동기화에는 그 레포의 AGENTS.md 규칙이나 전용 스킬을 쓴다.

## 0. 입력 확인

사용자에게 받는다(없으면 묻는다):

| 입력 | 예 |
| --- | --- |
| Figma 디자인 시스템 URL | `https://www.figma.com/design/<fileKey>/...` |
| 만들 위치 | 모노레포 `packages/ui`, 새 레포 루트 등 |
| `{{PREFIX}}` / `{{prefix}}` | `VD` / `vd` |
| `{{package}}` | `ui` |
| `{{product}}` | 제품 이름 |
| `{{font_family}}` | Figma Text Style의 폰트 (확인 후 제안해도 된다) |
| 대상 플랫폼 | `ios,android` |

**Figma 접근을 먼저 확인한다.** Figma MCP 읽기 도구(메타데이터·변수 정의·디자인 컨텍스트·스크린샷)로 파일의 페이지 목록을 한 번 읽어 본다.
- 읽히면 진행한다.
- 막히면(권한·호출 한도) 대체 입력을 요청한다: Dev Mode의 Inspect → Code(CSS) 붙여넣기, 변수 export JSON, 페이지별 스크린샷. 대체 입력으로 진행하면 그 사실을 `HISTORY.md` 초기 항목에 남긴다.

## 1. 템플릿 인스턴스화

1. 템플릿을 대상 위치로 복사한다. 대상이 비어 있지 않으면 멈추고 묻는다.
2. placeholder를 파일 내용과 **경로 이름** 모두에서 치환한다(`lib/{{package}}.dart` → `lib/ui.dart`). `{{figma_url}}`도 채운다.
3. `TEMPLATE.md`를 지운다.
4. `example/`에서 `flutter create --platforms=<대상> .`로 플랫폼 폴더를 만든다(`lib/`는 덮어쓰지 않도록 생성 후 확인).
5. 모노레포면 워크스페이스 설정(melos 등)에 패키지를 등록하고, 루트 lint 설정이 있으면 `analysis_options.yaml`을 루트 include로 바꾼다.
6. 검증: `node scripts/verify-docs.mjs` 통과(잔여 placeholder 0), `flutter pub get`·`flutter analyze` 통과.

## 2. 인벤토리 — 범위 확정 게이트

Figma를 읽어 목록만 만든다(값은 아직 쓰지 않는다).

- **Foundations**: 변수 컬렉션(이름·변수 수·mode 수), Text Style·Effect Style 목록.
- **Components**: 페이지 번호·이름·그룹, Component Set과 variant 축.
- **결정 후보**: 컬러 계층(컬렉션 구조), 테마 모드(mode 수), 상호작용 상태(명세에 hover/pressed가 있는가), 크기 토큰 유무.

`docs/foundations/00-INDEX.md`·`docs/components/00-INDEX.md`에 행을 만들고(상태 ⏳), 사용자에게 보여 준 뒤 **범위와 결정 후보의 확정을 받고 멈춘다.** 범위 밖으로 둘 것(예: 작업 중 페이지, 웹 전용 컴포넌트)은 ⛔와 이유를 적는다.

확정되면 `AGENTS.md` §결정 사항 표와 `lib/AGENTS.md` §2-1을 채운다.

## 3. 명세 작성 (docs)

- Foundation → Component 순서. 각 문서는 폴더의 `_TEMPLATE.md`로 시작하고 Figma에서 확인한 값만 쓴다.
- 파일 이름은 `NN-kebab-name.md`, 번호는 Figma 페이지 번호를 따른다.
- 토큰에 바인딩되지 않은 원시 값, 축 이름 불일치, 빠진 상태, 접근성 정보 공백은 handoff에 올린다.
- 각 컴포넌트 문서에 **접근성 계약 표**를 반드시 채운다 — 테스트의 입력이다. Figma에 근거가 없으면 컴포넌트 종류의 플랫폼 관례로 초안을 쓰고 handoff에 "확인 필요"로 올린다.
- 검증: `node scripts/verify-docs.mjs`.

컴포넌트가 많으면(대략 15개 이상) 그룹별로 나눠 작성하고 그룹마다 검증 세션에 명세 검토를 맡긴다(아래 §6).

## 4. 토큰 코드 (lib/src/foundations)

- `lib/AGENTS.md` §2 규칙대로 토큰 클래스를 만든다. 값은 Figma 변수에서 옮기고, semantic은 primitive alias로 쓴다.
- `{{PREFIX}}Text`·`{{PREFIX}}Theme.light()`를 만든다(§2-3 — Material `TextTheme` 슬롯 전부 매핑).
- 배럴에 export를 추가하고, example의 테마를 `{{PREFIX}}Theme.light()`로 바꾸고, Foundations 쇼케이스(Colors·Typography·Spacing·Radius·Shadow)를 등록한다.
- 검증: `flutter analyze`, `verify-docs.mjs`, 쇼케이스를 Figma 스크린샷과 나란히 비교할 수 있게 사용자에게 안내.

## 5. 컴포넌트 코드 (lib/src/components)

- 아이콘을 먼저 한다 — 다른 컴포넌트의 슬롯이 아이콘 데이터를 받는다. SVG는 Figma의 확정 컴포넌트를 export한 것만 `assets/icons/`에 둔다.
- 그룹별로 구현한다. 컴포넌트마다:
  1. 명세 → 위젯(`lib/AGENTS.md` §4~7: 컨트롤드 상태, enum 변형, 아이콘 슬롯, 보더 레이아웃)
  2. 배럴 export
  3. 쇼케이스 — 모든 변형 축과 Disabled를 한 화면에
  4. Semantics 테스트(명세의 접근성 계약 표) + `coverage_matrix_test.dart` 분류
  5. INDEX 상태 ✅
- 그룹이 서로 독립이면 병렬로 나눈다. 파일 소유가 겹치지 않게 그룹 단위로 나누고, 배럴·`gallery_data.dart`·INDEX 같은 공유 파일은 마스터가 마지막에 합친다.
- 검증: `flutter analyze`, `flutter test test/semantics`, `verify-docs.mjs`.

## 6. 세션 운영

규모가 크므로 `start-task` 스킬의 **대형** 규칙을 따른다(설치돼 있으면 그 스킬을 읽는다).

- 마스터(이 세션): 입력 확인·인벤토리·결정·공유 파일 병합·보고. 사소한 수정은 직접 한다.
- 구현 세션: §3 그룹별 명세, §5 그룹별 컴포넌트. 그룹이 독립이면 둘로 나눠 병렬.
- 검증 세션: **새 컨텍스트**로 명세 그룹마다 1회, 컴포넌트 그룹마다 1회. 넘기는 것은 Figma 링크(해당 페이지)·명세·diff뿐이다.
  - 명세 검증: Figma 실측과 값 대조(샘플이 아니라 전 변형), 토큰 이름이 foundation에 실재하는가, 접근성 계약 표가 비어 있지 않은가, handoff 누락.
  - 코드 검증: 명세 ↔ 코드 값 대조, `lib/AGENTS.md` 규칙(primitive 참조 허용 목록, 컨트롤드 상태, disabled 필드, 아이콘 색 주입), Semantics 테스트가 계약 항목을 전부 단언하는가, 쇼케이스가 모든 변형을 펼치는가.
- Orca·서브에이전트가 없으면 그룹 단위로 순차 진행하고, 검증 spec을 파일로 남겨 사용자에게 새 세션 실행을 요청한다. 마스터가 자기 결과를 검증하지 않는다.

## 7. 완료 보고

다음 순서로 보고한다.

1. 만든 위치와 결정 사항(`AGENTS.md` §결정 사항 요약)
2. 범위: foundations N종 · components N종 (✅/⏳/⛔ 개수, ⛔ 이유)
3. 검증 결과: `flutter analyze`, `flutter test test/semantics`, `node scripts/verify-docs.mjs` — 실패·생략은 그대로 적는다
4. **Figma 무수정 확인**
5. 디자이너 인계: `docs/handoff.md` 건수와 요약
6. 사용자 확인 항목: 예제 앱에서 Figma 스크린샷과 수동 대조(특히 타이포 baseline·그림자·보더 두께)

커밋·푸시·PR은 사용자가 요청할 때만 한다.
