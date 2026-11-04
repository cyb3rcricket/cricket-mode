# Claude Code adapter

**Status: implemented. Deterministic check passes. Live validation pending.**

Claude Code exposes Cricket through project skills. Each command is a skill the user invokes with `/name`. The skill file is wiring. The behavior is `core/COMMANDS.md`.

Codex, Cursor, and Antigravity are not part of this adapter.

## How Claude Code discovers a command

Claude Code loads every `SKILL.md` under the project's `.claude/skills/` directory. The frontmatter `name` becomes the slash command, which the user invokes as `/name`. The folder name is the command. The `name` field must match that folder.

Claude Code does not read `.agents/skills/` for this. The `.claude` path is its own, so this adapter cannot collide with a Codex or Antigravity install.

| Command | Installed path | Invoke |
| --- | --- | --- |
| `/pitch` | `.claude/skills/pitch/SKILL.md` | `/pitch` |
| `/chirp` | `.claude/skills/chirp/SKILL.md` | `/chirp` |
| `/senpai` | `.claude/skills/senpai/SKILL.md` | `/senpai` |
| `/challenge` | `.claude/skills/challenge/SKILL.md` | `/challenge` |
| `/prove-it` | `.claude/skills/prove-it/SKILL.md` | `/prove-it` |
| `/drift` | `.claude/skills/drift/SKILL.md` | `/drift` |
| `/scrub` | `.claude/skills/scrub/SKILL.md` | `/scrub` |

Each skill sets `disable-model-invocation: true`. Only the user can invoke the skill. Claude Code cannot load it on its own, and its description stays out of context until it is invoked. Typing a request that resembles the command does not run it.

On invoke, the skill tells the agent to read `.claude/skills/cricket-contract/COMMANDS.md` and follow that command's section plus the cross-command invariants. In this repository that file is a symlink to `../../../../core/COMMANDS.md`.

## Install

From a cricket-mode checkout:

```bash
python3 cricket install claude --target /path/to/your/project
```

On Windows (PowerShell), use `py` instead of `python3`:

```powershell
py cricket install claude --target \path\to\your\project
```

The same copy by hand:

```bash
TARGET=/path/to/your/project
mkdir -p "$TARGET/.claude/skills"
cp -a adapters/claude/skills/. "$TARGET/.claude/skills/"
rm -f "$TARGET/.claude/skills/cricket-contract/COMMANDS.md"
cp core/COMMANDS.md "$TARGET/.claude/skills/cricket-contract/COMMANDS.md"
```

Remove the copied symlink before copying the contract. Copying onto that symlink can follow it and overwrite `core/COMMANDS.md`. After the remove-and-copy, the installed tree works without this repository beside it.

Install at the project root `.claude/skills/`.

You can copy one command's folder plus `cricket-contract/` if you only want that command. The contract folder has no `SKILL.md`, so Claude Code does not treat it as an eighth command.

To pick up a newer contract, run `python3 cricket update --target /path/to/your/project` (or `py cricket update --target \path\to\your\project` on Windows), or copy `core/COMMANDS.md` over `.claude/skills/cricket-contract/COMMANDS.md` again. The seven skill files stay as they are.

## Usage

Type the slash command:

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

- Claude Code will not reject a reply that skips the contract's result shape. The skill instructs the agent. `adapters/claude/check.py` grades the bundled conformance fixtures. It does not grade a live Claude Code reply, and it does not open Claude Code. Live validation is pending.
- The copied tree includes a symlink at `cricket-contract/COMMANDS.md`. Remove it with `rm -f`, then `cp core/COMMANDS.md` onto that path. Leaving the symlink points at this repository's `core/COMMANDS.md`. Outside that layout the read fails, and the skill stops instead of inventing a behavior.
- `python3 cricket install claude` writes only this adapter. `python3 cricket update` refreshes the installed contract copy and leaves the seven skill files in place.
- This adapter does not write `.agents/skills/`. Codex and Antigravity use that path. A Claude Code install can sit beside them.

## Check

From the repository root:

```bash
python3 adapters/claude/check.py
```

The script installs the tree into a temporary project's `.claude/skills/`, discovers the seven `SKILL.md` files, resolves each contract section, and checks that the skill text does not carry a second copy of the command behavior. After that passes, it runs `conformance/check.py` and checks that each command's bundled pass fixture returns no rule failures. It does not open Claude Code.
