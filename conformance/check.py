#!/usr/bin/env python3
"""Deterministic checks for the seven Cricket commands.

The rules live here once. A case in cases.json is a fixture plus the
phrases that fixture cares about. evaluate() scores a reply text.
It does not call a model.

Future adapters should import evaluate and pass the reply they collected.
Producing that reply is the adapter's job.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

COMMANDS = [
    "pitch",
    "chirp",
    "senpai",
    "challenge",
    "prove-it",
    "drift",
    "scrub",
]

# Labels as written in core/COMMANDS.md. Reply checks and the contract
# presence check both use this list.
LABELS = {
    "pitch": ["**Ask:**", "**Smallest plan:**", "**Won't do:**"],
    "chirp": ["**Basically:**"],
    "senpai": [],
    "challenge": ["**Findings:**", "**Looks solid:**"],
    "prove-it": ["**PASS**", "**FAIL**", "**PARTIAL**"],
    "drift": [],
    "scrub": ["**Residue:**", "**Keep:**", "**Out of scope:**"],
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def cases_path() -> Path:
    return Path(__file__).resolve().parent / "cases.json"


def load_cases() -> list[dict]:
    data = json.loads(cases_path().read_text())
    commands = [case["command"] for case in data]
    if commands != COMMANDS:
        raise SystemExit(f"cases.json commands are {commands}, expected {COMMANDS}")
    return data


def evaluate(command: str, reply: str, case: dict) -> list[str]:
    if command != case["command"]:
        raise ValueError(f"command {command} does not match case {case['command']}")
    checks = {
        "pitch": check_pitch,
        "chirp": check_chirp,
        "senpai": check_senpai,
        "challenge": check_challenge,
        "prove-it": check_prove_it,
        "drift": check_drift,
        "scrub": check_scrub,
    }
    if command not in checks:
        raise ValueError(f"unknown command {command}")
    return checks[command](reply, case)


def check_pitch(reply: str, case: dict) -> list[str]:
    failed = []
    labels = LABELS["pitch"]
    indexes = [reply.find(label) for label in labels]
    if any(index < 0 for index in indexes) or indexes != sorted(indexes):
        failed.append("pitch.labels")
    ask = reply.find("**Ask:**")
    if ask >= 0:
        before = reply[:ask]
        if "```" in before or any(phrase in before for phrase in case["forbidden"]):
            failed.append("pitch.before")
    wont = _after(reply, "**Won't do:**", "```")
    if any(phrase not in wont for phrase in case["wont_do"]):
        failed.append("pitch.scope")
    after_ask = reply[ask:] if ask >= 0 else reply
    if any(phrase in after_ask for phrase in case["forbidden"]):
        failed.append("pitch.no_widen")
    return failed


def check_chirp(reply: str, case: dict) -> list[str]:
    failed = []
    if len(reply.split()) >= len(case["previous"].split()):
        failed.append("chirp.shorter")
    match = re.search(r"\*\*Basically:\*\*\s*(.+)\Z", reply, re.S)
    sentences = []
    tail = ""
    if match:
        tail = match.group(1).strip()
        sentences = [part for part in re.split(r"(?<=[.!?])\s+", tail) if part]
    if match is None or "\n\n" in tail or not 1 <= len(sentences) <= 2:
        failed.append("chirp.basically")
    if any(phrase not in reply for phrase in case["keep"]):
        failed.append("chirp.keeps")
    if any(phrase in reply for phrase in case["drop"]):
        failed.append("chirp.drops")
    return failed


def check_senpai(reply: str, case: dict) -> list[str]:
    failed = []
    if any(phrase not in reply for phrase in case["mechanism"]):
        failed.append("senpai.mechanism")
    if case["pattern"] not in reply:
        failed.append("senpai.pattern")
    if case["stays"] not in reply:
        failed.append("senpai.stays")
    if case["changes"] not in reply:
        failed.append("senpai.changes")
    return failed


def check_challenge(reply: str, case: dict) -> list[str]:
    failed = []
    findings = _between(reply, "**Findings:**", "**Looks solid:**")
    looks = _after(reply, "**Looks solid:**", None)
    if findings is None or not looks.strip():
        failed.append("challenge.closes")
    body = findings or ""
    if any(phrase not in body for phrase in case["findings"]):
        failed.append("challenge.confirmed")
    if findings is not None and any(phrase in findings for phrase in case["not_findings"]):
        failed.append("challenge.possibility")
    if any(phrase in reply for phrase in case["fix_markers"]):
        failed.append("challenge.no_fix")
    return failed


def check_prove_it(reply: str, case: dict) -> list[str]:
    failed = []
    found = re.findall(r"\*\*(PASS|FAIL|PARTIAL)\*\*", reply)
    last = [line for line in reply.splitlines() if line.strip()]
    last_line = last[-1] if last else ""
    if found != [case["status"]] or f"**{case['status']}**" not in last_line:
        failed.append("proveit.status")
    if any(phrase not in reply for phrase in case["evidence"]):
        failed.append("proveit.evidence")
    return failed


def check_drift(reply: str, case: dict) -> list[str]:
    failed = []
    if any(phrase not in reply for phrase in case["sides"]):
        failed.append("drift.sides")
    return failed


def check_scrub(reply: str, case: dict) -> list[str]:
    failed = []
    residue = _between(reply, "**Residue:**", "**Keep:**")
    keep = _between(reply, "**Keep:**", "**Out of scope:**")
    outside = _after(reply, "**Out of scope:**", None)
    if residue is None or keep is None or not outside.strip():
        failed.append("scrub.closes")
    residue_body = residue or ""
    if case["path"] not in residue_body or case["snippet"] not in residue_body:
        failed.append("scrub.concrete")
    lowered = residue_body.lower()
    if not any(word in lowered for word in ("delete", "simplify", "inline")):
        failed.append("scrub.surgical")
    if case["redesign"] in residue_body:
        failed.append("scrub.no_redesign")
    outside_body = outside if outside else ""
    separated = True
    for phrase in case["out_of_scope"]:
        if phrase not in outside_body or phrase in residue_body:
            separated = False
    if not separated:
        failed.append("scrub.separated")
    return failed


def contract_gaps() -> list[str]:
    text = (repo_root() / "core" / "COMMANDS.md").read_text()
    gaps = []
    for command, labels in LABELS.items():
        heading = f"## `/{command}`"
        start = text.find(heading)
        if start < 0:
            gaps.append(f"{command}: missing {heading}")
            continue
        rest = text[start + len(heading) :]
        nxt = rest.find("\n## ")
        section = rest if nxt < 0 else rest[:nxt]
        for label in labels:
            if label not in section:
                gaps.append(f"{command}: contract section missing {label}")
    return gaps


def _after(text: str, marker: str, stop: str | None) -> str:
    start = text.find(marker)
    if start < 0:
        return ""
    rest = text[start + len(marker) :]
    if stop is None:
        return rest
    cut = rest.find(stop)
    return rest if cut < 0 else rest[:cut]


def _between(text: str, start_marker: str, end_marker: str) -> str | None:
    start = text.find(start_marker)
    if start < 0:
        return None
    rest = text[start + len(start_marker) :]
    end = rest.find(end_marker)
    if end < 0:
        return None
    return rest[:end]


def main() -> int:
    failures: list[str] = []
    for gap in contract_gaps():
        failures.append(gap)
    for case in load_cases():
        for sample in case["samples"]:
            got = evaluate(case["command"], sample["reply"], case)
            expected = sample["fail"]
            status = "ok" if got == expected else "mismatch"
            print(f"{case['command']:10} {sample['name']:22} {status:8} {got or '-'}")
            if got != expected:
                failures.append(
                    f"{case['command']} {sample['name']}: got {got}, expected {expected}"
                )
    if failures:
        print("FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("PASS")
    print(f"checked {len(COMMANDS)} commands against core/COMMANDS.md and cases.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
