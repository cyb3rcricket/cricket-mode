# 🦗 Cricket Mode!

Small, focused agent behaviors for working better with coding agents.

Cricket Mode adds command-sized behaviors for common moments in AI-assisted development: simplify an explanation, teach the code that was just written, challenge an implementation, prove that something actually works, find where a project has drifted out of sync, scrub leftover agent fingerprints, or clamp scope to the asked-for change before you build.

Each behavior does one thing.

## Skills

| Command | What it does |
| --- | --- |
| `/chirp` | Makes the last explanation simpler, shorter, and easier to understand. |
| `/senpai` | Teaches you what the agent just built, how it works, why it was done that way, and the reusable pattern behind it. |
| `/challenge` | Tries to break the work before you trust it. |
| `/prove-it` | Verifies real behavior and shows evidence instead of merely claiming the work is correct. |
| `/drift` | Finds places where the project no longer agrees with itself. |
| `/scrub` | Finds leftover agent fingerprints and proposes surgical removal. |
| `/pitch` | Clamps the work to the smallest change that solves the stated problem before coding begins. |

## Why Cricket Mode?

Coding agents produce a lot of work quickly. That creates recurring problems: dense explanations, code you did not learn from, plausible bugs, weak verification, repository drift, AI residue, and agents inventing scope that was never requested.

Cricket Mode gives each moment a small, explicit command.

```text
/chirp      Make the last answer click.
/senpai     Teach me what you just built.
/challenge  Try to break it before we trust it.
/prove-it   Don't tell me it works. Prove it.
/drift      Find where the project disagrees with itself.
/scrub      Strip the agent fingerprints. Don't redesign the work.
/pitch      Solve only what was asked. Ask before inventing.
```

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

See **[Portable Cricket](docs/PORTABLE-CRICKET.md)** for the architecture, current status, and exact continuation plan. It is intentionally written so the project can be resumed after a long break without reconstructing the idea from chat history.

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
├── docs/
│   └── PORTABLE-CRICKET.md   # architecture + resume plan
├── cricket                   # install or update one adapter
├── AGENTS.md
└── examples/
```

## Installation today

The currently working reference skills live in `.agents/skills/`.

Copy any skill you want into an agent environment that supports the current skill format. You can install only the skills you want.

**Important:** Cursor, Codex, and Antigravity adapters are implemented. From this checkout, `python3 cricket install cursor|codex|antigravity --target /path/to/project` copies one adapter. `python3 cricket update --target /path/to/project` refreshes an installed contract copy. Install notes are in each adapter README. Shared reply checks are in `conformance/`. Cursor, Codex, and Antigravity themselves were not opened from this environment.

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
- **DETERMINISTICALLY VERIFIED** — a script in this repository exercised that behavior. No host application was opened.
- **REQUIRES LIVE PLATFORM VALIDATION** — only Cursor, Codex, or Antigravity itself can prove it.

| Piece | Status |
| --- | --- |
| Seven reference skills | IMPLEMENTED in `.agents/skills/` |
| Command contract | IMPLEMENTED. Reviewed against the reference skills and the existing examples |
| Codex adapter | IMPLEMENTED. DETERMINISTICALLY VERIFIED by `python3 adapters/codex/check.py` (`$name` skills plus conformance). REQUIRES LIVE CODEX VALIDATION |
| Cursor adapter | IMPLEMENTED. DETERMINISTICALLY VERIFIED by `python3 adapters/cursor/check.py` (explicit `/name` skills, a contract copy, and conformance). REQUIRES LIVE CURSOR VALIDATION |
| Antigravity adapter | IMPLEMENTED. DETERMINISTICALLY VERIFIED by `python3 adapters/antigravity/check.py` (`/name` skills plus conformance). REQUIRES LIVE ANTIGRAVITY VALIDATION |
| Shared conformance checks | DETERMINISTICALLY VERIFIED by `python3 conformance/check.py` and by each adapter check |
| Installer | IMPLEMENTED. DETERMINISTICALLY VERIFIED by `python3 cricket test` |

## License

MIT
