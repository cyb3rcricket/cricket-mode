# Codex adapter

**Status: implemented.**

Codex exposes Cricket as [Agent Skills](https://developers.openai.com/codex/skills). Each command is a skill the user invokes as `$name`, or by choosing it in the `/skills` picker. The skill file is wiring. The behavior is `core/COMMANDS.md`.

Codex does not register these as `/pitch`-style slash commands. Deprecated custom prompts under `~/.codex/prompts` can still look like slash commands, and this adapter does not use them.

Antigravity is not part of this adapter.

## How Codex discovers a command

Codex scans `.agents/skills` from the current directory up to the repository root. A skill is a folder whose `SKILL.md` has a `name` that matches the folder. Codex starts with the name, description, and path, and loads the body when the skill is used.

| Command | Installed path | Invoke |
| --- | --- | --- |
| pitch | `.agents/skills/pitch/SKILL.md` | `$pitch` |
| chirp | `.agents/skills/chirp/SKILL.md` | `$chirp` |
| senpai | `.agents/skills/senpai/SKILL.md` | `$senpai` |
| challenge | `.agents/skills/challenge/SKILL.md` | `$challenge` |
| prove-it | `.agents/skills/prove-it/SKILL.md` | `$prove-it` |
| drift | `.agents/skills/drift/SKILL.md` | `$drift` |
| scrub | `.agents/skills/scrub/SKILL.md` | `$scrub` |

Each skill has `agents/openai.yaml` with `allow_implicit_invocation: false`. Codex will not run it from the description alone. `$name` still works.

On invoke, the skill tells Codex to read `.agents/skills/cricket-contract/COMMANDS.md` and follow that command's section plus the cross-command invariants. The section headings in the contract stay `/pitch` and the rest. That is the behavior name. It is not a Codex slash command. In this repository `adapters/codex/skills/cricket-contract/COMMANDS.md` is a symlink whose target is `../../../../core/COMMANDS.md`.

`cricket-contract/` has no `SKILL.md`, so Codex does not treat it as an eighth skill.

## Install

From a cricket-mode checkout, into the project that should grow the commands:

```bash
TARGET=/path/to/your/project
mkdir -p "$TARGET/.agents/skills"
cp -a adapters/codex/skills/. "$TARGET/.agents/skills/"
rm -f "$TARGET/.agents/skills/cricket-contract/COMMANDS.md"
cp core/COMMANDS.md "$TARGET/.agents/skills/cricket-contract/COMMANDS.md"
```

Remove the copied symlink before copying the contract. Copying onto that symlink can follow it and overwrite `core/COMMANDS.md`. After the remove-and-copy, the installed tree works without this repository beside it.

You can copy one command's folder plus `cricket-contract/` if you only want that command.

To pick up a newer contract, copy `core/COMMANDS.md` over `.agents/skills/cricket-contract/COMMANDS.md` again. The skill files stay as they are. Codex usually notices the change. If the new skill does not appear, restart Codex.

## Usage

In the Codex CLI or IDE extension:

```text
$pitch
$chirp
$senpai
$challenge
$prove-it
$drift
$scrub
```

`/skills` opens the picker. The commands stay independent. Invoking one does not invoke the others.

## Limitations

- Invocation is `$name` or the `/skills` picker. A `/pitch` slash command is not created. Cursor's `/pitch` spelling is a different host mechanism for the same contract section.
- Codex turns implicit invocation on unless `agents/openai.yaml` sets `allow_implicit_invocation: false`. These skills set that. A copied skill without that file can run because the description matched.
- This repository's `.agents/skills/` tree is the older reference copy. Codex loads it when you launch Codex here. Those files do not set `allow_implicit_invocation: false`, and they carry their own wording. Installing this adapter into that same tree overwrites them. Install it into the project where you want the contract-backed commands.
- The copied tree includes a symlink at `cricket-contract/COMMANDS.md`. Remove it with `rm -f`, then `cp core/COMMANDS.md` onto that path. Leaving the symlink points at this repository's `core/COMMANDS.md`.
- Codex does not grade the reply shape. `adapters/codex/check.py` installs the tree and then runs `conformance/check.py` on the shared reply fixtures. It does not ask Codex to write those replies.
- Codex can shorten or omit skill descriptions when many skills are installed. These seven descriptions are one line each.
- Two skills with the same name in different scopes both appear. Codex does not merge them.
- This is not a one-command installer.

## Check

From the repository root:

```bash
python3 adapters/codex/check.py
```

The script installs the tree into a temporary project's `.agents/skills/`, discovers the seven skills, checks the invocation policy, and runs the shared conformance checker.
