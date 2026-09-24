# Antigravity adapter

**Status: implemented. Slash-command discovery is deterministically checked. Live Antigravity behavior is not.**

Antigravity exposes reusable project behavior as [Agent Skills](https://antigravity.google/docs/skills). A skill is a folder with `SKILL.md`. Workspace skills live in `.agents/skills/<name>/`. Antigravity 2.0, the Antigravity CLI, and the Antigravity IDE all document that path. `.agent/skills` is a legacy path Antigravity still reads. This adapter installs only the current path.

The skill file is wiring. The behavior is `core/COMMANDS.md`.

## How Antigravity discovers a command

At the start of a conversation Antigravity lists each skill's name and description. The documented manual invoke is a slash command. The CLI also turns every skill into a slash command in the TUI.

| Command | Installed path | Documented invoke |
| --- | --- | --- |
| pitch | `.agents/skills/pitch/SKILL.md` | `/pitch` |
| chirp | `.agents/skills/chirp/SKILL.md` | `/chirp` |
| senpai | `.agents/skills/senpai/SKILL.md` | `/senpai` |
| challenge | `.agents/skills/challenge/SKILL.md` | `/challenge` |
| prove-it | `.agents/skills/prove-it/SKILL.md` | `/prove-it` |
| drift | `.agents/skills/drift/SKILL.md` | `/drift` |
| scrub | `.agents/skills/scrub/SKILL.md` | `/scrub` |

You can also mention the skill by name. Official docs say the agent may read the skill without that, when the description looks relevant.

On invoke, the skill tells the agent to read `.agents/skills/cricket-contract/COMMANDS.md` and follow that command's section plus the cross-command invariants. In this repository `adapters/antigravity/skills/cricket-contract/COMMANDS.md` is a symlink whose target is `../../../../core/COMMANDS.md`.

`cricket-contract/` has no `SKILL.md`, so it is not an eighth skill.

Rules are a different mechanism. A rule with `trigger: manual` loads only on an `@` mention, and it is not a `/pitch` slash command. Workflows under `.agents/workflows/` are deprecated. This adapter uses skills.

## Install

From a cricket-mode checkout, into a project that is not this repository:

```bash
TARGET=/path/to/your/project
mkdir -p "$TARGET/.agents/skills"
cp -a adapters/antigravity/skills/. "$TARGET/.agents/skills/"
rm -f "$TARGET/.agents/skills/cricket-contract/COMMANDS.md"
cp core/COMMANDS.md "$TARGET/.agents/skills/cricket-contract/COMMANDS.md"
```

Remove the copied symlink before copying the contract. Copying onto that symlink can follow it and overwrite `core/COMMANDS.md`.

Do not install this tree onto the cricket-mode repo's `.agents/skills/`. That directory is the reference implementation. Codex reads the same path, so one project can hold the Codex wrappers or these wrappers, not both.

To pick up a newer contract, copy `core/COMMANDS.md` over `.agents/skills/cricket-contract/COMMANDS.md` again.

## Usage

In the Antigravity prompt, the documented command is:

```text
/pitch
/chirp
/senpai
/challenge
/prove-it
/drift
/scrub
```

## Limitations

- Autonomous activation is on. Antigravity's skill frontmatter documents `name` and `description` only. There is no documented switch corresponding to Cursor's `disable-model-invocation` or Codex's `allow_implicit_invocation: false`. These descriptions say to apply the skill only when the user types the slash command. Whether Antigravity obeys that is not something this repository can prove.
- `.agents/skills` is shared with Codex and with this repo's reference skills. Installing here overwrites whatever skill folder has the same name.
- Legacy `.agent/skills` is still scanned. This adapter does not write it. A project that also has `.agent/skills/<name>` can load a second copy.
- Antigravity does not grade the reply shape. `adapters/antigravity/check.py` installs the tree and runs `conformance/check.py`. It does not open Antigravity.
- This is not a one-command installer.

## REQUIRES LIVE ANTIGRAVITY VALIDATION

1. From a cricket-mode checkout, install into an empty project with the commands above.
2. Open that project in Antigravity.
3. Start a prompt and type `/pitch`. Confirm the skill is offered and that the reply follows the `/pitch` section of `.agents/skills/cricket-contract/COMMANDS.md`.
4. In a new prompt, ask to clamp a code change without typing `/pitch`. Record whether Antigravity loads the skill anyway.
5. Repeat step 3 for `/chirp`, `/senpai`, `/challenge`, `/prove-it`, `/drift`, and `/scrub`.

## Check

From the repository root:

```bash
python3 adapters/antigravity/check.py
```

The script installs the tree into a temporary project's `.agents/skills/`, checks the seven skill files and the contract copy, and runs the shared conformance checker. A passing run does not mean Antigravity was opened.
