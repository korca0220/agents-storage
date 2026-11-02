@AGENTS.md

<!--
  Claude Code는 AGENTS.md를 직접 읽지 않으므로 import만 둔다.
  규칙은 여기 적지 않는다. 정본은 AGENTS.md다.
  이 HTML 주석은 컨텍스트 주입 전에 제거되므로 둬도 비용이 없다.
-->

## Claude Code

- 스킬의 단일 출처는 `.agents/skills`다. `.claude/skills`는 심볼릭 링크이므로 스킬을 추가, 수정할 때 건드리지 않는다.
- 규칙 문서는 적용 시점에 자동 주입된다 (`.claude/settings.json` → `.agents/hooks/inject_rules.py`, 문서당 세션 1회). 주입이 오지 않았다면 규칙이 없는 것이 아니라 훅이 동작하지 않은 것이므로 해당 문서를 직접 읽는다.
- 세션 시작에 무엇이 실제로 로드됐는지는 `/context`의 **Memory files** 목록으로 확인한다.
