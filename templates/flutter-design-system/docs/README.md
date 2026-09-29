# docs/ — 디자인 시스템 명세

framework-neutral 명세 모음. **여기가 먼저, `lib/` 코드는 그다음.** 원본은 Figma({{figma_url}})이고, 이 폴더는 Figma를 읽기 전용으로 확인해 동기화한 결과다.

- [`foundations/`](foundations/00-INDEX.md) — 토큰 명세. 구현 상태는 `foundations/00-INDEX.md`에서 추적한다.
- [`components/`](components/00-INDEX.md) — 컴포넌트 명세(`01-...md` ~). 구현 상태는 `components/00-INDEX.md`에서 추적한다. 번호는 Figma 페이지 번호를 따른다.
- [`handoff.md`](handoff.md) — Figma 쪽에서 고쳐야 할 불일치·공백. 디자이너에게 전달할 목록이다.
- [`HISTORY.md`](HISTORY.md) — 개발 쪽 결정 이력.
- 새 문서는 각 폴더의 `_TEMPLATE.md`로 시작한다.
- 코드로 옮기는 규칙은 [`../lib/AGENTS.md`](../lib/AGENTS.md).
