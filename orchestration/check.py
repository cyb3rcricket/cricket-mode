#!/usr/bin/env python3
"""Run the orchestration fixtures. Does not call a model or a host app."""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

from policy import decide, discover_checks

ROOT = Path(__file__).resolve().parent
VENDOR_WORDS = ("grok", "gemini", "luna", "sol")
EXPLICIT_ONLY = {"pitch", "chirp", "senpai", "scrub"}


def main() -> int:
    failures = []
    cases = json.loads((ROOT / "cases.json").read_text())
    policy_text = (ROOT / "policy.py").read_text().lower()
    for word in VENDOR_WORDS:
        if re.search(rf"\b{word}\b", policy_text):
            failures.append(f"policy.py contains vendor word {word}")

    for case in cases:
        got = decide(case["task"])
        if got != case["expect"]:
            failures.append(f"{case['name']}: got {got}, expected {case['expect']}")
        if case["task"].get("attempt", 1) >= 2 and got["decision"] == "RETRY":
            failures.append(f"{case['name']}: attempt >= 2 returned RETRY")
        if got["model"] is not None:
            failures.append(f"{case['name']}: model is {got['model']}")
        if len(got["recommendations"]) > 2:
            failures.append(f"{case['name']}: more than two recommendations")
        if EXPLICIT_ONLY.intersection(got["recommendations"]):
            failures.append(f"{case['name']}: explicit command was recommended")
        print(f"{case['name']:20} {'ok' if got == case['expect'] else 'mismatch'}")

    discover_error = _check_discover()
    print(f"{'discover-checks':20} {'ok' if discover_error is None else 'mismatch'}")
    if discover_error:
        failures.append(discover_error)

    count = len(cases) + 1
    if failures:
        print("FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("PASS")
    print(f"{count} fixtures")
    return 0


def _check_discover() -> str | None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "Makefile").write_text(
            "test:\n\tpython3 explode.py\nlint:\n\tpython3 explode.py\n"
            "build:\n\tpython3 explode.py\npytest:\n\tpython3 explode.py\n"
        )
        (root / "explode.py").write_text(
            "from pathlib import Path\n"
            "Path('ran.txt').write_text('ran')\n"
            "raise SystemExit(1)\n"
        )
        names = discover_checks(root)
        if (root / "ran.txt").exists():
            return "discover_checks executed explode.py"
        expected = ["test", "lint", "build", "pytest"]
        if names != expected:
            return f"discover_checks returned {names}, expected {expected}"
    return None


if __name__ == "__main__":
    sys.exit(main())
