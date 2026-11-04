# AGENTS.md — {{프로젝트명}}

{{프로젝트 한 줄 소개}}

이 파일은 세션 시작에 **자동으로** 컨텍스트에 들어옵니다. 모든 세션이 비용을 치르므로 **적용 범위가 좁은 규칙은 해당 디렉터리의 중첩 `AGENTS.md`로 내립니다.**

나머지 규칙 문서는 "읽으세요"라는 지시가 아니라 **하네스가 적용 시점에 컨텍스트로 넣는 방식**으로 전달됩니다. 각각 세션당 1회입니다.

| 문서 | 들어오는 시점 |
| --- | --- |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md) — 커밋, PR 규칙 | `git commit`, `gh pr create`, `gh pr edit` 중 먼저 오는 것 |
| [`docs/coding-conventions.md`](./docs/coding-conventions.md) — lint로 못 잡는 규약 | `*.{{확장자}}`를 처음 만질 때 |
| 스킬 카탈로그 ([`.agents/AGENTS.md`](./.agents/AGENTS.md)) | 이름과 설명은 세션 내내, 본문은 호출 시 |

**훅이 돌지 않는 환경도 있습니다. 규칙이 컨텍스트에 없으면 그 문서를 직접 읽습니다.**

---

## 프로젝트 개요

- **제품**: {{무엇을 만드는가}}
- **현재 상태**: {{골격만 있음 / 운영 중 등}}
- **주요 기술**: {{언어, 프레임워크}} — [ADR-001](./docs/adr/001-xxx.md)
- **상태 관리, DI, 라우팅**: {{...}} — [ADR-002](./docs/adr/002-xxx.md)

---

## 일반 작업 원칙

**신중함을 속도보다 우선**하지만, 트리비얼한 작업에는 판단을 적용합니다.

### 1. Think Before Coding — 가정하지 말고 드러낸다

- 가정은 명시한다. 불확실하면 묻는다.
- 해석이 둘 이상이면 한쪽을 조용히 고르지 말고 모두 제시한다.
- 더 단순한 접근이 보이면 말한다. 필요하면 반대한다.
- 모호하면 멈춘다. 무엇이 헷갈리는지 이름 붙여서 묻는다.

### 2. Simplicity First — 요청된 만큼만

- 요청 외의 기능, 단일 사용처 추상화, 요청되지 않은 설정 가능성을 넣지 않는다.
- 일어날 수 없는 시나리오의 에러 처리를 넣지 않는다.
- 자가 검증: "시니어 엔지니어가 보면 과설계라고 할까?" → Yes면 단순화.

### 3. Surgical Changes — 필요한 곳만 건드린다

- 인접 코드, 주석, 포맷을 "개선"하지 않는다. 기존 스타일에 맞춘다.
- 관련 없는 dead code는 지우지 말고 언급만 한다.
- 본인 변경이 만든 미사용 import, 변수, 함수만 제거한다.
- 테스트: 변경된 모든 줄이 요청과 직접 연결되는가?

### 4. Goal-Driven Execution — 검증 가능한 성공 기준

- "검증 추가" → "잘못된 입력 케이스 테스트 작성 후 통과"
- "버그 수정" → "버그 재현 테스트 작성 후 통과"
- 다단계 작업은 `1. [단계] → 검증: [체크]` 형태로 계획을 먼저 적는다.

---

## 디렉터리 구조

- `{{경로}}/` — {{역할}}
- `docs/` — ADR, exec-plan, 코딩 컨벤션 등 하네스 문서
- `.agents/` — 하네스 중립 자산: 스킬 카탈로그, 정책, 스킬, 훅 스크립트. `hooks/inject_rules.py`는 Claude Code와 Codex가 **같은 파일을 호출한다**
- `.claude/` — Claude Code 하네스. `skills/`는 `../.agents/skills`로 가는 심볼릭 링크이므로 스킬은 `.agents/skills`에서만 수정한다
- `.codex/` — Codex 하네스. `hooks.json`이 같은 스크립트를 호출한다
- `CLAUDE.md` — `@AGENTS.md` import만 둔다. **규칙을 여기 적지 않는다.** 중첩 `AGENTS.md`를 만들면 짝이 되는 `CLAUDE.md`도 함께 만든다

---

## 빌드, 실행 명령어

```bash
# 의존성 설치
{{명령}}

# 테스트
{{명령}}

# Lint, 포맷
{{명령}}

# 실행
{{명령}}
```

---

## Invariant (절대 규칙)

어떤 상황에서도 어기지 않는 규칙입니다. 각 항목은 **규칙과 강제 수단만** 담고, 근거와 예외는 링크된 ADR, 스킬이 정본입니다.

| # | 규칙 | 강제 수단 |
| --- | --- | --- |
| 1 | {{규칙}} | {{lint / 테스트 / 문서 — ADR-NNN}} |
| 2 | 코드 생성 결과물은 직접 수정하지 않는다. 생성 명령으로 재생성한다 | {{생성 명령}} |
| 3 | 코드 변경 PR을 열기 전 품질 게이트를 로컬에서 통과시킨다 | 문서 — [`CONTRIBUTING.md`](./CONTRIBUTING.md) |

---

## 작업 흐름 (Generator–Evaluator)

같은 에이전트가 자기 결과를 평가하면 "대체로 잘 됐다"로 치우칩니다. 큰 변경은 **구현자(Generator)** 와 **평가자(Evaluator)** 를 나눕니다.

| 크기 | exec-plan | Generator–Evaluator 분리 |
| --- | --- | --- |
| 트리비얼 (타이포, 문구 한 줄) | 생략 | 생략 |
| 소형 (단일 파일, 단일 기능) | 선택 | 선택 (자기 리뷰만 권장) |
| 중형 (여러 파일, 한 피처) | 권장 | 권장 |
| 대형 (여러 패키지, 스키마 변경) | **필수** | **필수** |

**중형 이상**이면 [`docs/exec-plans/_TEMPLATE.md`](./docs/exec-plans/_TEMPLATE.md)와 [`docs/agent-workflow.md`](./docs/agent-workflow.md)를 함께 엽니다.

**하네스 파일**(`AGENTS.md`, `CLAUDE.md`, `.agents/**`, `.claude/**`, `.codex/**`, `docs/adr/**`, `docs/coding-conventions.md`, `CONTRIBUTING.md`)을 바꿨으면 [`docs/agent-workflow.md`](./docs/agent-workflow.md)의 "하네스 변경 후 점검"을 수행합니다.

### 커밋, PR 작성

정본은 [`CONTRIBUTING.md`](./CONTRIBUTING.md)입니다. 요약을 여기 두지 않습니다 (정본과 어긋납니다). **규칙이 컨텍스트에 없으면 첫 커밋 전에 직접 읽습니다.**

---

## Skills

카탈로그: [`.agents/AGENTS.md`](./.agents/AGENTS.md)

| 스킬 | 트리거 예시 |
| --- | --- |
| `{{skill-name}}` | "{{이렇게 말하면 실행}}" |

---

## 참고 문서

- 코딩 컨벤션 → [`docs/coding-conventions.md`](./docs/coding-conventions.md)
- 커밋, PR 규칙 → [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- 아키텍처 결정 → [`docs/adr/`](./docs/adr/)
- 실행 계획 → [`docs/exec-plans/`](./docs/exec-plans/)
- 작업 흐름 상세 → [`docs/agent-workflow.md`](./docs/agent-workflow.md)
