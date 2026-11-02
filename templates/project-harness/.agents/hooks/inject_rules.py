#!/usr/bin/env python3
"""규칙이 적용되기 시작하는 순간에 그 정본 문서를 에이전트 컨텍스트에 넣는다.

Claude Code와 Codex가 같은 파일을 호출한다. 규칙을 두 하네스에 복사하지 않고 훅
로직도 한 벌만 두기 위해서다 — 두 벌로 두면 한쪽만 고쳐지는 드리프트가 생긴다.

왜 세션 시작이 아닌가: 세션 앞머리에서 한 번 읽은 규칙은 긴 작업 뒤에 잊히고, 그
세션에서 쓰이지도 않을 문서를 매번 넣으면 토큰만 쓴다. 규칙은 적용되기 시작하는
순간에 닿아야 한다. 반대로 같은 문서를 반복해서 넣는 것도 낭비이므로 에이전트별
식별자를 받을 수 있을 때 규칙당 한 번만 넣는다.

적용 방법: 아래 `_CODE_EXTENSIONS`를 프로젝트 언어에 맞게 바꾸고, `_RULES`에서
쓰지 않는 문서는 지운다. 문서 파일이 없으면 그 규칙은 조용히 건너뛴다.
"""

import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Callable, Iterator, NamedTuple, Optional

_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

# 하네스의 훅 출력 상한. 넘으면 앞부분 프리뷰만 남고 나머지는 아무 신호 없이 사라진다.
# 잘린 규칙은 안 넣은 것보다 위험하다 — 뒷부분 규칙이 존재하지 않는 것처럼 보이기
# 때문이다. 그래서 상한을 넘으면 본문 대신 "직접 읽어라"는 경고를 내보낸다.
# 문서 크기를 CI·테스트로 9,000자 정도에서 먼저 막아 두면 이 경고를 볼 일이 없다.
_HOOK_OUTPUT_LIMIT = 10_000

# 셸 연산자로 명령을 자른 뒤 토큰으로 읽는다. 정규식 하나로 매칭하면 전역 옵션
# (`git -C <path> commit`, `gh --repo o/r pr create`)을 놓치는데, 옵션 형태를 정규식에
# 계속 덧붙이는 것보다 "전역 옵션을 건너뛰고 첫 서브커맨드를 본다"가 읽기도 쉽고
# 빠지는 형태도 없다.
_SEGMENT = re.compile(r"[;&|\n()]+")

# 값을 별도 토큰으로 받는 전역 옵션. 건너뛸 때 뒤 토큰까지 함께 넘겨야 한다.
_GIT_VALUE_OPTIONS = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--config-env"})
_GH_VALUE_OPTIONS = frozenset({"-R", "--repo"})

# `FOO=bar git commit` 처럼 앞에 붙는 환경변수 할당.
_ENV_ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")

# 따옴표로 감싼 구간은 셸에게 데이터지 호출이 아니다. 인자로 넘어가는 문자열 안의
# `gh pr create` 를 실제 호출로 오인하지 않도록 내용만 비우고 자리는 남긴다.
# 셸 인용 규칙 전부를 흉내내지는 않는다 — heredoc 본문처럼 따옴표 밖에 그대로
# 놓이는 형태는 여전히 잡힌다. 그 경우 규칙이 필요 시점보다 일찍 들어갈 뿐이다.
_QUOTED_SPAN = re.compile(r"'[^']*'|\"[^\"]*\"", re.DOTALL)

# 코딩 컨벤션을 주입할 소스 확장자. 프로젝트 언어에 맞게 바꾼다 (예: ("ts", "tsx")).
_CODE_EXTENSIONS = ("dart",)

# 소스 경로가 tool_input 어디에 있든 잡는다. 하네스마다 편집을 표현하는 모양이
# 달라서다 — Claude Code는 `file_path`, Codex는 `apply_patch` 본문, 그리고 두 하네스
# 모두 `sed`·`cat` 같은 Bash 경유 편집을 쓴다. 읽기만 하는 명령에도 걸리지만, 잘못
# 걸렸을 때의 결과는 "규칙이 조금 일찍 들어옴"이라 정확도보다 누락 없음을 택한다.
_CODE_PATH = re.compile(r"[\w./-]*\.(?:" + "|".join(map(re.escape, _CODE_EXTENSIONS)) + r")\b")

_AGENT_SCOPE_KEYS = ("agent_id", "transcript_path")


class Rule(NamedTuple):
    """문서 하나와, 그 문서의 규칙이 적용되기 시작하는 순간."""

    doc: str
    marker: str
    intro: str
    applies: Callable[[dict], bool]


def _strings(value: object) -> Iterator[str]:
    """tool_input 안의 모든 문자열 값. 하네스마다 키 이름이 달라 전부 훑는다."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _subcommand(tokens: list[str], value_options: frozenset) -> list[str]:
    """전역 옵션을 건너뛰고 서브커맨드부터 반환한다."""
    index = 1
    while index < len(tokens) and tokens[index].startswith("-"):
        index += 2 if tokens[index] in value_options else 1
    return tokens[index:]


def _is_commit_or_pr(event: dict) -> bool:
    command = event.get("tool_input", {}).get("command") if isinstance(event.get("tool_input"), dict) else None
    if not isinstance(command, str):
        return False

    for segment in _SEGMENT.split(_QUOTED_SPAN.sub("''", command)):
        tokens = [t for t in segment.split() if not _ENV_ASSIGNMENT.match(t)]
        if not tokens:
            continue

        if tokens[0] == "git":
            rest = _subcommand(tokens, _GIT_VALUE_OPTIONS)
            if rest and rest[0] == "commit":
                return True
        elif tokens[0] == "gh":
            rest = _subcommand(tokens, _GH_VALUE_OPTIONS)
            if len(rest) >= 2 and rest[0] == "pr" and rest[1] in {"create", "edit"}:
                return True

    return False


def _touches_code(event: dict) -> bool:
    return any(_CODE_PATH.search(text) for text in _strings(event.get("tool_input")))


# 순서가 곧 우선순위다. 한 호출에서 둘 다 걸리면 **하나만** 내보낸다 — 두 문서를
# 합치면 훅 출력 상한을 넘기 때문이다. 못 내보낸 쪽은 마커를 찍지 않으므로 다음
# 매칭 때 발동한다. 커밋·PR을 앞에 두는 이유는 그 순간이 지금 일어나는 행위라서다.
# 코드 편집은 이미 지나간 일이고, 보통 커밋보다 먼저 걸려 이미 주입돼 있다.
_RULES = (
    Rule(
        doc="CONTRIBUTING.md",
        marker="contributing",
        intro=(
            "아래는 이 저장소의 커밋, PR 규칙(CONTRIBUTING.md) 전문입니다. "
            "지금부터의 커밋 메시지와 커밋 단위, PR을 열 때의 제목과 본문, 라벨을 이 규칙에 맞추세요.\n\n"
        ),
        applies=_is_commit_or_pr,
    ),
    Rule(
        doc="docs/coding-conventions.md",
        marker="coding-conventions",
        intro=(
            "아래는 이 저장소의 코딩 컨벤션(docs/coding-conventions.md) 전문입니다. "
            "lint로 잡히지 않는 규약과 패턴이므로, 지금부터의 코드를 이 규칙에 맞추세요.\n\n"
        ),
        applies=_touches_code,
    ),
)


def _agent_scope(event: dict) -> Optional[str]:
    """에이전트별 식별자. 부모와 서브에이전트가 공유하는 session_id는 쓰지 않는다."""
    for key in _AGENT_SCOPE_KEYS:
        value = event.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _claim(marker: str, agent_scope: Optional[str]) -> bool:
    """에이전트별 1회. 식별자가 없으면 누락보다 중복 주입을 택한다."""
    if agent_scope is None:
        return True

    digest = hashlib.sha256(agent_scope.encode()).hexdigest()
    path = Path(tempfile.gettempdir()) / f"agent-rules-{_REPOSITORY_ROOT.name}-{marker}-{digest}"
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        return False
    except OSError:
        # 마커를 못 만들면 중복 주입은 토큰만 더 쓸 뿐이므로 주입 쪽을 택한다.
        return True

    os.close(descriptor)
    return True


def _payload(rule: Rule, doc: Path) -> str:
    body = rule.intro + doc.read_text(encoding="utf-8")
    if len(body) <= _HOOK_OUTPUT_LIMIT:
        return body

    return (
        f"⚠️ 이 저장소의 규칙 문서({rule.doc})가 훅 출력 상한을 넘어 본문을 주입하지 못했습니다 "
        f"— {len(body):,}자 / 상한 {_HOOK_OUTPUT_LIMIT:,}자.\n\n"
        f"잘린 규칙을 그대로 주입하면 뒷부분 규칙이 존재하지 않는 것처럼 보여 조용히 어기게 되므로 "
        f"본문 대신 이 경고를 보냅니다.\n"
        f"지금 `{rule.doc}`를 직접 읽고 그 규칙에 맞추세요."
    )


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return

    if not isinstance(event, dict):
        return

    agent_scope = _agent_scope(event)

    for rule in _RULES:
        doc = _REPOSITORY_ROOT / rule.doc
        if not doc.is_file() or not rule.applies(event):
            continue
        if not _claim(rule.marker, agent_scope):
            continue

        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "additionalContext": _payload(rule, doc),
                    }
                },
                ensure_ascii=False,
            )
        )
        return


if __name__ == "__main__":
    main()
