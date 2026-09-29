# flutter-design-system 템플릿

Figma 디자인 시스템을 원본(SSOT)으로 삼는 Flutter 디자인 시스템 패키지의 **구조와 하네스 뼈대**다. 값(토큰·컴포넌트)은 들어 있지 않다 — [`design-system-creator`](../../skills/design-system-creator/SKILL.md) 스킬이 Figma를 읽어 채운다.

- 1차: 이전 Flutter 앱의 `packages/design_system` — 명세 템플릿·품질 기준·골든 테스트
- 2차: 사내 Flutter 앱 모노레포의 `packages/ui` — Figma SSOT, 명세 우선, Semantics 계약 테스트, 이력·인계 운영
- 이 템플릿은 2차 구조를 뼈대로 하고, 제품 전용 결정(접두사·예외 목록·이슈 번호)을 걷어낸 것이다.

## 채울 자리 (placeholder)

파일 내용과 **경로 이름** 모두에 쓰인다. 복사한 뒤 전부 치환하고, `scripts/verify-docs.mjs`가 남은 `{{`를 잡는다.

| placeholder | 뜻 | 예 (2차) |
| --- | --- | --- |
| `{{PREFIX}}` | public 클래스 접두사 (대문자) | `VD` |
| `{{prefix}}` | 파일명 접두사 (소문자) | `vd` |
| `{{package}}` | Dart 패키지 이름 = 배럴 파일 이름 | `ui` |
| `{{product}}` | 제품·디자인 시스템 이름 | `MyProduct` |
| `{{font_family}}` | 기본 폰트 패밀리 | `Pretendard` |
| `{{figma_url}}` | 디자인 시스템 Figma 파일 URL | `https://www.figma.com/design/...` |

## 구성

| 경로 | 역할 | 채우는 시점 |
| --- | --- | --- |
| `AGENTS.md` · `CLAUDE.md` | 패키지 진입점 — SSOT·워크플로우·핵심 규칙 | 복사 시 치환 + 결정 기록(§결정 사항) |
| `lib/AGENTS.md` · `lib/CLAUDE.md` | Flutter 코드 생성 규칙 | 복사 시 치환 + 컬러 계층 등 결정 반영 |
| `docs/README.md` · `docs/HISTORY.md` | 문서 지도 · 개발 쪽 결정 이력 | 생성 과정에서 기록 |
| `docs/handoff.md` | 디자이너 인계 목록 (Figma 쪽 불일치·공백) | 생성 과정에서 누적 |
| `docs/foundations/` · `docs/components/` | Figma와 동기화하는 명세 + `00-INDEX.md` 트래커 + `_TEMPLATE.md` | 인벤토리 → 명세 단계 |
| `lib/{{package}}.dart` · `lib/src/` | 배럴 + 토큰·컴포넌트 구현 | 코드 단계 |
| `test/semantics/` | 접근성 계약 테스트 + 커버리지 매트릭스 | 코드 단계 |
| `example/` | 컴포넌트 갤러리(쇼케이스) 앱 — Material 기본 위젯만 써서 DS 상태와 무관하게 빌드된다 | 코드 단계에서 쇼케이스 추가 |
| `scripts/verify-docs.mjs` | 문서 링크·INDEX↔파일·배럴 export·커버리지 매트릭스·잔여 placeholder 검사 | 그대로 사용 |
| `assets/` · `fonts/` | SVG 아이콘 · 폰트 | Figma export / 폰트 배치 |

`example/`의 플랫폼 폴더(ios·android 등)는 템플릿에 두지 않는다. 복사 후 `flutter create --platforms=<...> example`로 만든다.

## 사용

직접 쓰지 말고 [`design-system-creator`](../../skills/design-system-creator/SKILL.md) 스킬로 진행한다. 수동으로 쓸 때도 스킬의 단계 순서(인벤토리 → 명세 → 토큰 → 컴포넌트 → 검증)를 따른다.
