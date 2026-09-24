# Cursor adapter

**Status: implemented.**

Cursor exposes Cricket through [Agent Skills](https://cursor.com/docs/skills). Each command is a skill the user invokes with `/name` in Agent chat. The skill file is wiring. The behavior is `core/COMMANDS.md`.

Codex and Antigravity are not part of this adapter.

## How Cursor discovers a command

Cursor loads every `SKILL.md` under the project's `.cursor/skills/` directory (and `.agents/skills/`, which this adapter does not use). The folder name is the command. The `name` field must match that folder.

| Command | Installed path | Invoke |
| --- | --- | --- |
| `/pitch` | `.cursor/skills/pitch/SKILL.md` | `/pitch` |
| `/chirp` | `.cursor/skills/chirp/SKILL.md` | `/chirp` |
| `/senpai` | `.cursor/skills/senpai/SKILL.md` | `/senpai` |
| `/challenge` | `.cursor/skills/challenge/SKILL.md` | `/challenge` |
| `/prove-it` | `.cursor/skills/prove-it/SKILL.md` | `/prove-it` |
| `/drift` | `.cursor/skills/drift/SKILL.md` | `/drift` |
| `/scrub` | `.cursor/skills/scrub/SKILL.md` | `/scrub` |

`@` can attach the same skill as context. That loads the same file.

Each skill sets `disable-model-invocation: true`, so Cursor includes it only when the user invokes it. Typing a request that resembles the command does not run it.

On invoke, the skill tells the agent to read `.cursor/skills/cricket-contract/COMMANDS.md` and follow that command's section plus the cross-command invariants. In this repository that file is a symlink to `../../../../core/COMMANDS.md`.

## Install

From a cricket-mode checkout, into the project that should grow the commands:

```bash
TARGET=/path/to/your/project
mkdir -p "$TARGET/.cursor/skills"
cp -a adapters/cursor/skills/. "$TARGET/.cursor/skills/"
rm -f "$TARGET/.cursor/skills/cricket-contract/COMMANDS.md"
cp core/COMMANDS.md "$TARGET/.cursor/skills/cricket-contract/COMMANDS.md"
```

Remove the copied symlink before copying the contract. Copying onto that symlink can follow it and overwrite `core/COMMANDS.md`. After the remove-and-copy, the installed tree works without this repository beside it.

Install at the project root `.cursor/skills/`. A `.cursor/skills/` directory nested inside a subdirectory is scoped to that subdirectory.

You can copy one command's folder plus `cricket-contract/` if you only want that command. The contract folder has no `SKILL.md`, so Cursor does not treat it as an eighth command.

To pick up a newer contract, copy `core/COMMANDS.md` over `.cursor/skills/cricket-contract/COMMANDS.md` again. The seven skill files stay as they are.

## Usage

In Agent chat, type the slash command:

```text
/pitch
/chirp
/senpai
/challenge
/prove-it
/drift
/scrub
```

The commands stay independent. Invoking one does not invoke the others.

## Limitations

- Cursor will not reject a reply that skips the contract's result shape. The skill instructs the agent. `adapters/cursor/check.py` does not grade a reply. `conformance/check.py` can grade a reply string against the shared cases.
- `.agents/skills/` in this repository is the older reference copy. Cursor loads it too. Those files do not set `disable-model-invocation`, and they carry their own wording. Installing this adapter into the cricket-mode repo can expose two skills with the same name. Install it into the project where you want the contract-backed commands.
- The copied tree includes a symlink at `cricket-contract/COMMANDS.md`. Remove it with `rm -f`, then `cp core/COMMANDS.md` onto that path. Leaving the symlink points at this repository's `core/COMMANDS.md`. Outside that layout the read fails, and the skill stops instead of inventing a behavior.
- This is not a one-command installer. Re-copy the contract file when it changes.
- Legacy `.cursor/commands/*.md` files are not this adapter. Cursor's current mechanism for this kind of explicit command is a skill with `disable-model-invocation: true`.

## Check

From the repository root:

```bash
python3 adapters/cursor/check.py
```

The script installs the tree into a temporary project's `.cursor/skills/`, discovers the seven `SKILL.md` files, resolves each contract section, and checks that the skill text does not carry a second copy of the command behavior. It does not score a model reply.
