# project-harness 템플릿

에이전트(Claude Code, Codex)와 함께 일하는 프로젝트에 깔아 두는 **하네스 뼈대**다. 내용은 비어 있고, `{{...}}` 자리를 프로젝트에 맞게 채워 쓴다.

- 원본: 운영 중인 사내 Flutter 앱 모노레포의 루트 하네스 (AGENTS.md, ADR, exec-plan, 시점 주입 훅)
- 이 템플릿은 그 구조를 뼈대로 하고, 제품 전용 결정(ADR 본문, Invariant 항목, 스킬, 이슈 키)을 걷어낸 것이다.
- Flutter + Melos 전용 설정은 `examples/`의 선택 항목으로 분리했다.

## 채울 자리 (placeholder)

| placeholder | 뜻 | 예 (원본) |
| --- | --- | --- |
| `{{프로젝트명}}` | 프로젝트 이름 | `My App` |
| `{{확장자}}` | 코딩 컨벤션을 주입할 소스 확장자 | `dart` |
| `{{명령}}` | 설치, 테스트, lint, 실행 명령 | `fvm dart run melos test` |
| `{{develop}}` | 기본 베이스 브랜치 | `develop` |
| `{{skill-name}}` | 스킬 이름 | `repository-usecase-patterns` |

`grep -rn "{{" .` 로 남은 자리를 찾는다. 확장자는 `.agents/hooks/inject_rules.py`의 `_CODE_EXTENSIONS`도 함께 바꾼다.

## 이 템플릿이 하는 일

| 문제 | 하네스가 하는 일 | 파일 |
| --- | --- | --- |
| 에이전트가 프로젝트 규칙을 모른다 | 세션 시작에 항상 읽히는 짧은 규칙 파일 | `AGENTS.md`, `CLAUDE.md` |
| 규칙 문서를 다 넣으면 컨텍스트가 넘친다 | 규칙이 필요한 순간에만 문서를 주입하는 훅 | `.agents/hooks/inject_rules.py` |
| 왜 이렇게 만들었는지 에이전트가 모른다 | 기술 결정 기록 | `docs/adr/` |
| 큰 작업이 중간에 흐트러진다 | 작업 전에 쓰는 계약서, 컨텍스트 리셋 시 인수인계 | `docs/exec-plans/` |
| 에이전트가 자기 결과를 후하게 평가한다 | 구현자와 평가자를 나누는 작업 흐름 | `docs/agent-workflow.md` |
| 커밋, PR 형식이 사람마다 다르다 | 커밋, PR 규칙 | `CONTRIBUTING.md` |

## 구조

```
project-harness/
├── TEMPLATE.md                   # 이 문서 (복사하지 않음)
├── AGENTS.md                     # 항상 로드되는 루트 규칙 (짧게 유지)
├── CLAUDE.md                     # Claude Code용. @AGENTS.md import만 둔다
├── CONTRIBUTING.md               # 커밋, PR 규칙 (git commit 직전에 주입)
├── docs/
│   ├── agent-workflow.md         # Generator-Evaluator 절차, 검증 명령
│   ├── coding-conventions.md     # lint로 못 잡는 규약 (소스 파일을 처음 만질 때 주입)
│   ├── adr/README.md             # ADR 형식과 목록
│   └── exec-plans/_TEMPLATE.md   # 실행 계획 템플릿
├── .agents/                      # 하네스 중립 자산 (스킬, 정책, 훅의 단일 출처)
│   ├── AGENTS.md                 # 스킬 카탈로그
│   ├── hooks/inject_rules.py     # 시점 주입 훅 (Claude Code, Codex 공용)
│   ├── policies/                 # 에이전트 산출물 기준 등
│   └── skills/_example-skill/    # 스킬 작성 예시
├── .claude/
│   ├── settings.json             # 훅 등록
│   ├── agents/reviewer.md        # 리뷰 서브에이전트 예시
│   └── skills -> ../.agents/skills   # 심볼릭 링크 (직접 만들어야 함, 아래 참고)
├── .codex/hooks.json             # Codex 훅 등록 (같은 스크립트 호출)
└── examples/                     # 채워 넣은 예시
```

## 적용 순서

1. 이 폴더 내용을 프로젝트 루트에 복사합니다. `TEMPLATE.md`와 `examples/`는 복사하지 않습니다.
2. 위 표의 `{{...}}` 자리를 채웁니다.
3. 스킬 심볼릭 링크를 만듭니다.
   ```bash
   ln -s ../.agents/skills .claude/skills
   ```
4. 훅 설정을 맞춥니다.
   - `.agents/hooks/inject_rules.py`의 `_CODE_EXTENSIONS`를 프로젝트 언어로 바꿉니다. 기본값은 `("dart",)`입니다.
   - `.claude/settings.json`, `.codex/hooks.json`의 `python3` 경로가 맞는지 확인합니다.
5. 처음에는 `AGENTS.md`의 Invariant를 비워 두고 시작해도 됩니다. 리뷰에서 같은 지적이 두 번 나오면 그때 한 줄씩 올립니다.

## 처음부터 다 채우지 않아도 됩니다

이 템플릿은 완성형이 아니라 **자라는 구조**를 보여 주는 용도입니다. 실제 프로젝트에서도 첫날에는 `AGENTS.md` 한 장과 ADR 몇 개로 시작했고, 나머지는 문제가 생길 때마다 하나씩 붙였습니다.

| 시점 | 추가한 것 |
| --- | --- |
| 첫날 | `AGENTS.md`, `CLAUDE.md`, ADR 2~3개, exec-plan 템플릿 |
| 리뷰가 쌓인 뒤 | `CONTRIBUTING.md`, `coding-conventions.md` |
| 같은 작업이 반복될 때 | `.agents/skills/` |
| 루트 규칙이 길어졌을 때 | 시점 주입 훅, 중첩 `AGENTS.md` |

## 주의할 점

- **Windows의 심볼릭 링크**: `git clone` 시 링크가 일반 텍스트 파일로 풀릴 수 있습니다. 개발자 모드를 켜고 `git config core.symlinks true` 후 다시 체크아웃하거나, 링크 대신 `.claude/skills`를 복사본으로 두고 동기화 스크립트를 쓰세요.
- **규칙은 한 곳에만**: `CLAUDE.md`에는 규칙을 적지 않습니다. 정본은 `AGENTS.md`입니다. 두 곳에 쓰면 반드시 어긋납니다.
- **루트 `AGENTS.md`는 짧게**: 모든 세션이 매번 읽으므로 길어질수록 비용이 듭니다. 특정 디렉터리에만 해당하는 규칙은 그 디렉터리의 중첩 `AGENTS.md`(+ 짝이 되는 `CLAUDE.md`)로 내립니다.
- **훅이 안 도는 환경**: 훅이 없어도 `AGENTS.md`에 "규칙이 컨텍스트에 없으면 직접 읽는다"고 적어 두었으므로 동작은 합니다. 다만 주입 시점이 보장되지 않습니다.

## 선택 항목 (스택 의존)

원본은 Flutter + Melos 모노레포라서 아래 항목은 스택에 맞을 때만 가져갑니다. 예시는 `examples/`에 있습니다.

- 품질 게이트 명령 (`fvm dart run melos ...`) → `examples/quality-gate-flutter-melos.md`
- 규칙 문서 크기 예산을 테스트로 강제하기 → 같은 파일 하단

## 예시

- [`examples/adr-001-state-management.md`](./examples/adr-001-state-management.md): ADR 한 편을 채운 모습
- [`examples/exec-plan-cursor-pagination.md`](./examples/exec-plan-cursor-pagination.md): exec-plan 한 편을 채운 모습
- [`examples/invariants.md`](./examples/invariants.md): Invariant 표에 들어갈 만한 규칙 예시
