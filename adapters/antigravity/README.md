# Antigravity adapter

**Status: implemented. Discovery and conformance are deterministically checked. LIVE VALIDATED for the session below.**

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
python3 cricket install antigravity --target /path/to/your/project
```

The same copy by hand:

```bash
TARGET=/path/to/your/project
mkdir -p "$TARGET/.agents/skills"
cp -a adapters/antigravity/skills/. "$TARGET/.agents/skills/"
rm -f "$TARGET/.agents/skills/cricket-contract/COMMANDS.md"
cp core/COMMANDS.md "$TARGET/.agents/skills/cricket-contract/COMMANDS.md"
```

Remove the copied symlink before copying the contract. Copying onto that symlink can follow it and overwrite `core/COMMANDS.md`.

Do not install this tree onto the cricket-mode repo's `.agents/skills/`. That directory is the reference implementation. `python3 cricket install antigravity` refuses to replace an unstamped skill. Codex reads the same path, so one project can hold the Codex wrappers or these wrappers, not both.

To pick up a newer contract, run `python3 cricket update --target /path/to/your/project`, or copy `core/COMMANDS.md` over `.agents/skills/cricket-contract/COMMANDS.md` again.

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

- Antigravity's skill frontmatter documents `name` and `description` only. There is no documented switch corresponding to Cursor's `disable-model-invocation` or Codex's `allow_implicit_invocation: false`. In the live session, a normal prompt did not invoke any Cricket skill. During the explicit `/pitch` run, Antigravity also surfaced `challenge` as a used skill. That is one observed run, not a finding that normal prompts auto-run Cricket.
- `.agents/skills` is shared with Codex and with this repo's reference skills. The installer refuses that overwrite. A hand copy still replaces a same-named skill folder.
- Legacy `.agent/skills` is still scanned. This adapter does not write it. A project that also has `.agent/skills/<name>` can load a second copy.
- Antigravity does not grade the reply shape. `adapters/antigravity/check.py` installs the tree and runs `conformance/check.py`. It does not open Antigravity.
- `python3 cricket install antigravity` writes only this adapter. `python3 cricket update` refreshes the installed contract copy and leaves the skill files in place.

## Live session

- `/pitch` was explicitly invoked. Antigravity loaded the installed `SKILL.md` and shared `COMMANDS.md`, stated Ask / Smallest plan / Won't do, and implemented the requested file.
- A normal prompt without Cricket did not invoke any Cricket skill.
- `/prove-it` performed real filesystem, content, and byte verification and ended with **PASS**.
- During that `/pitch` run, Antigravity also surfaced `challenge` as a used skill. The normal prompt did not auto-run Cricket.

## Check

From the repository root:

```bash
python3 adapters/antigravity/check.py
```

The script installs the tree into a temporary project's `.agents/skills/`, checks the seven skill files and the contract copy, and runs the shared conformance checker. A passing run does not mean Antigravity was opened.
