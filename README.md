

# 🦗 Cricket Mode

Cricket Mode is a lightweight behavior layer for AI coding agents.

Instead of letting an agent jump straight from prompt to code, it gives you a disciplined way to clamp scope, challenge assumptions, verify the result with evidence, explain the work, and clean up what does not belong.

It is not a replacement for Codex, Gemini, Grok, Claude, or any other coding agent. It is a portable set of commands, skills, and adapters that brings the same small behaviors to Cursor, Codex, and Antigravity.

Use the smallest amount of intelligence necessary, and don’t call the work finished without evidence. The commands are independently useful. When a task benefits from a fuller pass, you can use the optional `plan → build → challenge → verify → explain → clean up` loop.

The goal is not to make agents do more. It’s to make them waste less, think at the right depth, and leave behind work you can actually trust.

## What you get

| Command | What it does |
| --- | --- |
| `/pitch` | Clamp scope before coding. |
| `/challenge` | Try to break completed work. |
| `/prove-it` | Verify real behavior with evidence. |
| `/senpai` | Learn the work that was just built. |
| `/scrub` | Remove agent residue without redesigning. |
| `/drift` | Find where the project disagrees with itself. |
| `/chirp` | Make the last explanation clearer. |

## Install

From this checkout, install one adapter into a project:

```bash
python3 cricket install cursor|codex|antigravity --target /path/to/project
```

Replace `cursor|codex|antigravity` with one supported host name. Cursor uses `.cursor/skills/`; Codex and Antigravity use `.agents/skills/`. The reference skill source in this checkout is `.agents/skills/<command>/`; copy a command from there into a compatible agent environment. Run `python3 cricket update --target /path/to/project` to refresh an installed contract copy.

Supported hosts are Cursor, Codex, and Antigravity.

## What it is not

Cricket Mode is not a coding agent or a required workflow. It is opt-in: use commands independently, and combine them only when a task benefits from the combination.

## Portable by design

Cricket Mode is split into two layers:

1. **Core behavior** — what each command means regardless of model, editor, or coding agent.
2. **Adapters** — thin platform-specific glue for Codex, Cursor, Antigravity, and future environments.

The goal is **behavioral portability, not identical plumbing**.

```text
                    Cricket Mode
                         │
                 core behavior contract
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Codex          Cursor       Antigravity
       adapter         adapter        adapter
```

The `.agents/skills/` directory remains the reference implementation. Portable adapters are in `adapters/`.

See **[Portable Cricket](docs/PORTABLE-CRICKET.md)** for the architecture and detailed status.

## Repository layout

```text
cricket-mode/
├── .agents/skills/           # current working skill implementations
├── core/
│   ├── README.md             # portable-core rules
│   └── COMMANDS.md           # platform-neutral behavior contract
├── adapters/
│   ├── README.md             # adapter contract
│   ├── codex/                # Codex skills invoked as $name
│   ├── cursor/               # Cursor skills wired to core/COMMANDS.md
│   └── antigravity/          # Antigravity skills invoked as /name
├── conformance/              # shared reply checks for the seven commands
├── orchestration/            # optional task policy; not installed with an adapter
├── docs/
│   └── PORTABLE-CRICKET.md   # architecture + detailed status
├── cricket                   # install or update one adapter
├── AGENTS.md
└── examples/
```

## Usage

Cursor and the Antigravity docs use a slash command. Codex uses `$name` or the `/skills` picker. The section headings in `core/COMMANDS.md` stay `/pitch` and the rest either way.

```text
/chirp
/senpai
/challenge
/prove-it
/drift
/scrub
/pitch
```

Codex spelling: `$chirp`, `$senpai`, `$challenge`, `$prove-it`, `$drift`, `$scrub`, `$pitch`.

The commands are intentionally small. They change how an agent approaches one moment; they are not a mandatory workflow framework.

## Examples

Annotated before/after transcripts in the `examples/` directory show how the skills change what the agent says and does.

## Suggested combos

These are optional habits, not a required workflow.

- **`/pitch`** before building to clamp scope.
- **`/challenge` then `/prove-it`** to attack the idea and then demand evidence.
- **`/senpai`** after non-trivial work to learn the pattern.
- **`/scrub`** after a messy agent turn to remove residue without redesign.
- **`/drift`** after broad changes to catch contradictions.
- **`/chirp`** after a dense explanation to restate it simply.

## Philosophy

Start with the smallest instruction that reliably changes behavior.

A Cricket command should have one clear job. The core defines meaning; adapters translate that meaning into each platform. Platform quirks should not leak into the core unless they reveal a real behavioral requirement.

Add complexity only when real use proves it is needed.

## Status

Three labels are kept apart:

- **IMPLEMENTED** — the files exist in this repository.
- **DETERMINISTICALLY VERIFIED** — a script in this repository exercised that behavior. The script does not open the host application.
- **LIVE VALIDATED** — the named host was run and the stated behavior was observed.

Portable v1 is complete. Orchestration is an optional policy beside the commands; it does not select a model or invoke a Cricket command, is not installed with an adapter, has not been live validated in a host app, and does not automatically classify tasks or escalate work.

| Piece | Status |
| --- | --- |
| Seven reference skills | IMPLEMENTED in `.agents/skills/` |
| Command contract | IMPLEMENTED. Reviewed against the reference skills and the existing examples |
| Codex adapter | IMPLEMENTED. DETERMINISTICALLY VERIFIED by `python3 adapters/codex/check.py`. LIVE VALIDATED for explicit `$pitch` and `$prove-it`; a normal prompt did not auto-trigger Cricket |
| Cursor adapter | IMPLEMENTED. DETERMINISTICALLY VERIFIED by `python3 adapters/cursor/check.py`. LIVE VALIDATED for explicit `/pitch` and `/prove-it`; a normal prompt did not auto-trigger Cricket |
| Antigravity adapter | IMPLEMENTED. DETERMINISTICALLY VERIFIED by `python3 adapters/antigravity/check.py`. LIVE VALIDATED for explicit `/pitch` and `/prove-it`; a normal prompt did not invoke Cricket, and one `/pitch` run also surfaced `challenge` |
| Shared conformance checks | DETERMINISTICALLY VERIFIED by `python3 conformance/check.py` and by each adapter check |
| Installer | IMPLEMENTED. DETERMINISTICALLY VERIFIED by `python3 cricket test`. Install and update tooling is complete. It still copies only the seven commands |
| Orchestration | IMPLEMENTED. DETERMINISTICALLY VERIFIED by `python3 orchestration/check.py`. Optional policy beside the commands |

## License

MIT
