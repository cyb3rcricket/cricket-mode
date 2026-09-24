"""Optional task policy beside the seven Cricket commands.

decide() reads a task dict and returns a decision dict. It does not call a
model, run tests, invoke Cricket, or remember earlier attempts.
"""

from __future__ import annotations

import re
from pathlib import Path

MAX_ATTEMPTS = 2

# Word boundaries so "author" is not "auth".
# "session" does not: a chat-history trim was classified DEEP from that word alone.
# "architecture" does not: a two-file schema/handler check was classified DEEP
# from that word alone.
_DEEP = re.compile(r"\bauth\b", re.IGNORECASE)
_RELATIONS = ("RELATED", "UNRELATED", "UNKNOWN")


def _relation(item: dict) -> str:
    """Caller-supplied link between a check and this task. Omitted means UNKNOWN."""
    relation = item.get("relation")
    if relation in _RELATIONS:
        return relation
    return "UNKNOWN"


def _check_name(item: dict) -> str:
    return item.get("name", "check")


def decide(task: dict) -> dict:
    """Return a lane and a decision for one task. No retry loop."""
    summary = str(task.get("summary") or "")
    changed = list(task.get("changed_files") or [])
    expected = task.get("expected_files")
    attempt = int(task.get("attempt") or 1)
    checks = list(task.get("checks") or [])

    deep = _DEEP.search(summary) is not None
    blown = expected is not None and len(changed) > int(expected) * 2
    if blown:
        lane = "ESCALATE"
    elif deep:
        lane = "DEEP"
    elif len(changed) <= 1:
        lane = "FAST"
    else:
        lane = "STANDARD"

    failed = [item for item in checks if item.get("status") == "FAILED"]
    actionable = [item for item in failed if _relation(item) != "UNRELATED"]
    unrelated = [item for item in failed if _relation(item) == "UNRELATED"]
    not_run = [item for item in checks if item.get("status") == "NOT RUN"]
    passed = [item for item in checks if item.get("status") == "PASSED"]

    if blown:
        decision = "ESCALATE"
    elif actionable and attempt <= 1:
        decision = "RETRY"
    elif actionable:
        decision = "ESCALATE"
    elif not_run:
        decision = "BLOCKED"
    else:
        decision = "COMPLETE"

    recommendations = []
    if blown:
        recommendations.append("drift")
    if (actionable and attempt <= 1) or not_run:
        recommendations.append("prove-it")
    if deep or (actionable and attempt >= 2):
        recommendations.append("challenge")

    ordered = []
    for name in recommendations:
        if name not in ordered:
            ordered.append(name)

    return {
        "lane": lane,
        "decision": decision,
        "model": None,
        "verified_completion": bool(passed) and not actionable,
        "unresolved_failures": [_check_name(item) for item in actionable],
        "unrelated_failures": [_check_name(item) for item in unrelated],
        "recommendations": ordered[:2],
        "max_attempts": MAX_ATTEMPTS,
    }


def discover_checks(root: Path | str) -> list[str]:
    """List declared check names. Read files only. Do not run them."""
    makefile = Path(root) / "Makefile"
    if not makefile.is_file():
        return []
    names = []
    text = makefile.read_text()
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or line[:1] in ("\t", " "):
            continue
        if ":" not in stripped:
            continue
        target = stripped.split(":", 1)[0].strip()
        if target and not target.startswith(".") and target not in names:
            names.append(target)
    if re.search(r"\bpytest\b", text) and "pytest" not in names:
        names.append("pytest")
    return names
