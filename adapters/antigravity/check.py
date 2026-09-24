#!/usr/bin/env python3
"""Install the Antigravity adapter and check discovery plus conformance.

Antigravity loads workspace skills from `.agents/skills/<name>/SKILL.md` and
documents `/name` as the slash command. This script does not launch Antigravity.
"""

from __future__ import annotations

import filecmp
import shutil
import subprocess
import sys
import tempfile
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

FORK_MARKERS = [
    "Solve only what was asked. Ask before inventing.",
    "**Basically:**",
    "**Findings:**",
    "**Looks solid:**",
    "**PASS**",
    "**FAIL**",
    "**PARTIAL**",
    "**Residue:**",
    "**Keep:**",
    "**Out of scope:**",
    "Strip the agent fingerprints. Don't redesign the work.",
    "Don't tell me it works. Prove it.",
    "Try to break the idea before we trust it.",
    "Find where the project disagrees with itself.",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_frontmatter(text: str, path: Path) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise SystemExit(f"{path}: missing opening frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise SystemExit(f"{path}: missing closing frontmatter")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise SystemExit(f"{path}: bad frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data, text[end + 5 :]


def expected_body(name: str) -> str:
    return (
        f"\n# /{name}\n\n"
        f"Antigravity wiring for Cricket `{name}`. This file does not define the behavior.\n\n"
        f"Cricket adapter: antigravity\n\n"
        f"Antigravity documents this skill as the `/{name}` slash command. "
        f"It also lists the skill for autonomous activation. The documented "
        f"frontmatter has no switch that turns that activation off.\n\n"
        f"Read `../cricket-contract/COMMANDS.md`. Follow only the section headed "
        f"`/{name}` and the section headed `Cross-command invariants`. If that file "
        f"is missing or unreadable, stop and say the Cricket contract is not installed.\n\n"
        f"Do not invent a different purpose, scope boundary, evidence requirement, "
        f"or result shape.\n"
    )


def install(source: Path, target_skills: Path, core: Path) -> None:
    target_skills.mkdir(parents=True)
    subprocess.run(["cp", "-a", f"{source}/.", str(target_skills)], check=True)
    materialized = target_skills / "cricket-contract" / "COMMANDS.md"
    materialized.unlink()
    shutil.copyfile(core, materialized)


def main() -> int:
    root = repo_root()
    source = root / "adapters" / "antigravity" / "skills"
    core = root / "core" / "COMMANDS.md"
    link = source / "cricket-contract" / "COMMANDS.md"
    failures: list[str] = []
    if not link.is_symlink() or link.resolve() != core.resolve():
        failures.append(f"{link} is not a symlink to core/COMMANDS.md")

    sys.path.insert(0, str(root))
    from conformance import evaluate, load_cases

    with tempfile.TemporaryDirectory(prefix="cricket-antigravity-") as tmp:
        project = Path(tmp) / "project"
        skills_root = project / ".agents" / "skills"
        before = core.read_bytes()
        install(source, skills_root, core)
        if core.read_bytes() != before:
            failures.append("install changed core/COMMANDS.md")
        installed_contract = skills_root / "cricket-contract" / "COMMANDS.md"
        if installed_contract.is_symlink() or not filecmp.cmp(installed_contract, core, shallow=False):
            failures.append("installed contract is not a real copy of core/COMMANDS.md")

        found = {path.parent.name: path for path in skills_root.rglob("SKILL.md")}
        if sorted(found) != sorted(COMMANDS):
            failures.append(f"discovered {sorted(found)}, expected {sorted(COMMANDS)}")
        contract_text = installed_contract.read_text()
        for name in COMMANDS:
            if name not in found:
                continue
            path = found[name]
            text = path.read_text()
            meta, body = parse_frontmatter(text, path)
            if "disable-model-invocation" in text:
                failures.append(f"{name}: claims Cursor's disable-model-invocation")
            if meta.get("name") != name:
                failures.append(f"{name}: frontmatter name is {meta.get('name')!r}")
            if f"/{name}" not in meta.get("description", ""):
                failures.append(f"{name}: description does not name /{name}")
            if body != expected_body(name):
                failures.append(f"{name}: skill body is not the thin wrapper")
            for marker in FORK_MARKERS:
                if marker in body or marker in meta.get("description", ""):
                    failures.append(f"{name}: semantic fork marker in skill: {marker}")
            if (path.parent / "agents" / "openai.yaml").exists():
                failures.append(f"{name}: includes Codex openai.yaml")
            if f"## `/{name}`" not in contract_text:
                failures.append(f"{name}: installed contract missing section /{name}")
            print(f"/{name}  discover={path.relative_to(project)}  invoke=/{name}")

        installed_contract.unlink()
        for name in COMMANDS:
            contract_path = (skills_root / name / "../cricket-contract/COMMANDS.md").resolve()
            if contract_path.exists():
                failures.append(f"{name}: contract still readable after removal")
        installed_contract.write_bytes(before)

    print(f"installed contract bytes: {len(before)}")
    for case in load_cases():
        sample = next(item for item in case["samples"] if item["fail"] == [])
        got = evaluate(case["command"], sample["reply"], case)
        print(f"/{case['command']}  conformance-pass={got or 'ok'}")
        if got != []:
            failures.append(f"{case['command']} pass sample failed conformance: {got}")

    suite = subprocess.run(
        [sys.executable, str(root / "conformance" / "check.py")],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if suite.returncode != 0:
        failures.append("conformance/check.py failed")
        print(suite.stdout)
        print(suite.stderr)
    else:
        print("conformance/check.py PASS")

    if failures:
        print("FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("PASS")
    print("installed 7 Antigravity skills; pass samples match conformance/")
    print("deterministic check only; this script does not open Antigravity")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as exc:
        print(f"FAIL\n- command failed: {exc}")
        sys.exit(1)
