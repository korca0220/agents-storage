# ADR (Architecture Decision Records)

기술 선택의 배경과 이유를 기록합니다. 사람에게는 히스토리이고, 에이전트에게는 **잘못된 방향으로 제안하지 않게 막는 맥락**입니다. 에이전트는 "이 프로젝트가 왜 이렇게 생겼는지" 모르면 더 흔한 방식으로 바꾸자고 제안합니다.

## 언제 쓰는가

- 되돌리기 어려운 기술 선택 (상태 관리, 라우팅, 데이터 레이어 구조)
- 에이전트가 반복해서 다른 방향을 제안할 때
- 리뷰에서 "이건 왜 이렇게 했어요?"가 두 번 나왔을 때

## 형식

파일명: `NNN-title.md`. 채운 예시는 [`examples/adr-001-state-management.md`](../../examples/adr-001-state-management.md)에 있습니다.

```markdown
# ADR-NNN: 제목

- **상태**: Proposed / Accepted / Deprecated / Superseded
- **날짜**: YYYY-MM-DD

## 결정

한 줄 요약.

## 배경

왜 이 결정이 필요했는가.

## 선택지

검토한 대안들.

## 결정 이유

왜 이것을 선택했는가.

## 결과

이 결정으로 생기는 트레이드오프.
```

## 운영 규칙

- 번호는 재사용하지 않습니다. 채택되지 않은 초안의 번호는 결번으로 둡니다.
- 결정이 바뀌면 기존 ADR을 고치지 않고 새 ADR을 쓴 뒤 기존 것을 `Superseded by ADR-NNN`으로 바꿉니다.
- `AGENTS.md`의 Invariant에는 규칙만 적고 근거는 ADR로 링크합니다.

## 목록

| # | 제목 | 상태 |
| --- | --- | --- |
| [001](./001-xxx.md) | {{제목}} | Accepted |
