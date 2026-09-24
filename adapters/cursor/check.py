#!/usr/bin/env python3
"""Install the Cursor adapter and check that Cursor can discover it.

This is the adapter's minimum contract check. It copies the skill tree into
a temporary project's `.cursor/skills/` directory, then discovers `SKILL.md`
files the way Cursor does. It does not score model replies.
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

# Result-shape phrases that belong only in the shared contract.
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

SECTION_MARKERS = {
    "pitch": ["**Ask:**", "**Smallest plan:**", "**Won't do:**"],
    "chirp": ["**Basically:**"],
    "senpai": ["recognize the pattern next time"],
    "challenge": ["**Findings:**", "**Looks solid:**"],
    "prove-it": ["**PASS**", "**FAIL**", "**PARTIAL**"],
    "drift": ["what says one thing", "what says something different"],
    "scrub": ["**Residue:**", "**Keep:**", "**Out of scope:**"],
}


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
        f"Cursor wiring for Cricket `/{name}`. This file does not define the behavior.\n\n"
        f"Cricket adapter: cursor\n\n"
        f"Read `../cricket-contract/COMMANDS.md`. Follow only the section headed "
        f"`/{name}` and the section headed `Cross-command invariants`. If that file "
        f"is missing or unreadable, stop and say the Cricket contract is not installed.\n\n"
        f"Do not invent a different purpose, scope boundary, evidence requirement, "
        f"or result shape.\n"
    )


def section(contract: str, name: str) -> str:
    heading = f"## `/{name}`\n"
    start = contract.find(heading)
    if start < 0:
        raise SystemExit(f"core contract has no {heading.strip()} section")
    rest = contract[start + len(heading) :]
    nxt = rest.find("\n## ")
    return rest if nxt < 0 else rest[:nxt]


def install(source: Path, target_skills: Path) -> None:
    target_skills.mkdir(parents=True)
    subprocess.run(["cp", "-a", f"{source}/.", str(target_skills)], check=True)
    materialized = target_skills / "cricket-contract" / "COMMANDS.md"
    # Remove the copied symlink before writing. Copying onto it can follow
    # the link and overwrite core/COMMANDS.md.
    materialized.unlink()
    shutil.copyfile(repo_root() / "core" / "COMMANDS.md", materialized)


def discover(skills_root: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for path in sorted(skills_root.rglob("SKILL.md")):
        name = path.parent.name
        if name in found:
            raise SystemExit(f"duplicate skill name {name}: {path}")
        found[name] = path
    return found


def main() -> int:
    root = repo_root()
    source = root / "adapters" / "cursor" / "skills"
    core = root / "core" / "COMMANDS.md"
    link = source / "cricket-contract" / "COMMANDS.md"
    if not link.is_symlink():
        raise SystemExit(f"{link} is not a symlink to the core contract")
    if not link.resolve() == core.resolve():
        raise SystemExit(f"{link} resolves to {link.resolve()}, not {core}")

    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="cricket-cursor-") as tmp:
        project = Path(tmp) / "project"
        skills_root = project / ".cursor" / "skills"
        install(source, skills_root)
        installed_contract = skills_root / "cricket-contract" / "COMMANDS.md"
        if installed_contract.is_symlink():
            failures.append("installed contract is still a symlink")
        if not filecmp.cmp(installed_contract, core, shallow=False):
            failures.append("installed contract bytes differ from core/COMMANDS.md")

        contract_text = installed_contract.read_text()
        if "## Cross-command invariants" not in contract_text:
            failures.append("installed contract missing cross-command invariants")

        found = discover(skills_root)
        extra = sorted(set(found) - set(COMMANDS))
        missing = [name for name in COMMANDS if name not in found]
        if extra:
            failures.append(f"unexpected skills discovered: {extra}")
        if missing:
            failures.append(f"skills not discovered: {missing}")

        hidden = skills_root / "cricket-contract" / "COMMANDS.md"
        backup = hidden.read_bytes()
        hidden.unlink()
        for name in COMMANDS:
            if name not in found:
                continue
            skill_path = found[name]
            text = skill_path.read_text()
            meta, body = parse_frontmatter(text, skill_path)
            if meta.get("name") != name:
                failures.append(f"{name}: frontmatter name is {meta.get('name')!r}")
            if meta.get("disable-model-invocation") != "true":
                failures.append(f"{name}: disable-model-invocation is not true")
            if f"/{name}" not in meta.get("description", ""):
                failures.append(f"{name}: description does not name /{name}")
            if body != expected_body(name):
                failures.append(f"{name}: skill body is not the thin wrapper")
            for marker in FORK_MARKERS:
                if marker in body or marker in meta.get("description", ""):
                    failures.append(f"{name}: semantic fork marker in skill: {marker}")
            contract_path = (skill_path.parent / "../cricket-contract/COMMANDS.md").resolve()
            if contract_path.exists():
                failures.append(f"{name}: contract still readable after removal at {contract_path}")
            # The wrapper's only behavior source is that relative path.
            if "../cricket-contract/COMMANDS.md" not in body:
                failures.append(f"{name}: wrapper does not point at the contract")

        hidden.write_bytes(backup)
        print(f"installed: {skills_root}")
        print(f"contract: {installed_contract} ({installed_contract.stat().st_size} bytes, not a symlink)")
        for name in COMMANDS:
            if name not in found:
                continue
            skill_path = found[name]
            meta, _body = parse_frontmatter(skill_path.read_text(), skill_path)
            contract_path = (skill_path.parent / "../cricket-contract/COMMANDS.md").resolve()
            chunk = section(contract_path.read_text(), name)
            absent = [marker for marker in SECTION_MARKERS[name] if marker not in chunk]
            if absent:
                failures.append(f"{name}: contract section missing {absent}")
            rel = skill_path.relative_to(project)
            print(
                f"/{name}  discover={rel}  invoke=/{meta['name']}  "
                f"explicit={meta['disable-model-invocation']}  "
                f"section=## /{name} ({len(chunk)} chars)"
            )

    if failures:
        print("FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("PASS")
    print(f"discovered {len(COMMANDS)} Cursor skills; each resolved section is the core contract")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as exc:
        print(f"FAIL\n- command failed: {exc}")
        sys.exit(1)
