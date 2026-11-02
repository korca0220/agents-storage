# AGENTS.md — Skills & Policies

<INSTRUCTIONS>

## Available Skills

스킬은 `SKILL.md`에 정의된 로컬 지시 묶음입니다. 아래 목록에서 스킬을 고르고, 필요하면 파일을 열어 전체 지시를 확인합니다.

스킬을 추가할 때는 이 목록과 루트 `AGENTS.md`의 Skills 표를 함께 갱신합니다.

---

### {{skill-name}}

{{이 스킬이 하는 일 1~2줄. 어떤 규칙을 함께 적용하는지}}

- **트리거**: "{{이렇게 말하면}}", "{{이렇게 말해도}}"
- **컨텍스트**: `.agents/skills/{{skill-name}}/references/`
- **파일**: `.agents/skills/{{skill-name}}/SKILL.md`

---

## 스킬로 만들 만한 것

- 같은 파일 묶음을 매번 같은 모양으로 만드는 작업 (API 연결, 엔티티, 테스트 뼈대)
- ADR이 정한 패턴을 코드로 옮기는 작업 (레이어 구조, DI 등록)
- 디자인 도구에서 화면을 가져와 구현하는 작업
- PR 생성처럼 형식이 정해진 작업

Invariant에 "X는 Y 스킬을 거친다"라고 묶어 두면 에이전트가 스킬을 건너뛰지 않습니다.

---

## Policies

- [`policies/`](./policies/) — 에이전트 산출물 기준 등 스킬보다 넓게 적용되는 정책

</INSTRUCTIONS>
