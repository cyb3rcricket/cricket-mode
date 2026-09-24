# Portable Cricket

## Read this first if you are returning later

Cricket Mode started as seven small agent skills:

`/pitch`, `/chirp`, `/senpai`, `/challenge`, `/prove-it`, `/drift`, and `/scrub`.

The next direction is to make those behaviors **portable across coding agents** such as Codex, Cursor, and Antigravity.

The project is not trying to make every platform use identical files or identical command plumbing.

The project is trying to guarantee that the **meaning stays stable everywhere**.

That is the whole idea.

## Architecture

```text
User invokes Cricket behavior
          │
          ▼
   PLATFORM ADAPTER
 Codex / Cursor / Antigravity
          │
          ▼
 PORTABLE CORE CONTRACT
          │
          ▼
      CODING AGENT
          │
          ▼
 REAL TOOLS + REPO EVIDENCE
 tests / build / typecheck /
 lint / git diff / runtime
```

### Core

Location: `core/`

The core defines purpose, required behavior, boundaries, evidence expectations, and result semantics. It should not know where Cursor stores rules or how Codex discovers commands.

### Adapters

Location: `adapters/`

Adapters translate the core contract into a platform's instruction system. An adapter can change **how** a command is installed or invoked. It cannot change **what** the command means.

### Verification principle

Cricket prefers software facts to AI opinion whenever software can answer the question.

```text
Does it compile?       → compiler/build
Do tests pass?         → test runner
Are types valid?       → type checker
What changed?          → git diff
Does the UI flow work? → run the real flow
Should we retry?       → agent judgment may help
```

## What exists now

### Working reference implementation

`.agents/skills/` contains the seven current skills. These are the behavior already being tested. Do not throw them away while building portability.

### Portable contract

`core/COMMANDS.md` is the new neutral specification for what the seven commands mean.

### Adapter skeleton

`adapters/codex/`, `adapters/cursor/`, and `adapters/antigravity/` are **implementation placeholders**, not finished support.

## Deliberately not built yet

Do not assume these exist just because the scaffold exists:

- automatic Codex installation,
- automatic Cursor installation,
- automatic Antigravity installation,
- a universal command registry,
- a one-command installer,
- adapter conformance tests,
- model routing,
- Luna/Sol escalation,
- Jev integration,
- autonomous retry loops.

First make the existing seven behaviors portable. Then decide which orchestration ideas have earned their complexity.

## Implementation plan

### Phase 1 — confirm the contract

Review `core/COMMANDS.md` against the existing skill files and examples. Make sure the neutral wording preserves the behavior already wanted.

### Phase 2 — build one adapter end to end

Pick **one** environment. Do not build all three simultaneously.

Deliver: installation instructions, seven exposed behaviors, and no semantic fork from the core.

### Phase 3 — conformance tests

Create a small shared behavior matrix.

Examples:
- Did `/pitch` state non-goals before implementation?
- Did `/challenge` separate findings from possibilities?
- Did `/prove-it` execute behavior instead of merely reading code?
- Did `/scrub` avoid becoming a redesign?

### Phase 4 — second and third adapters

Use the first working adapter to define the repeatable adapter pattern, then implement the others.

### Phase 5 — installation/update tooling

Only after adapters work, consider a tiny installer such as:

```text
cricket install codex
cricket install cursor
cricket install antigravity
cricket update
```

Do not build a package manager unless reality demands one.

### Phase 6 — optional orchestration

After portability works, separately explore model routing, deterministic verification loops, retry/escalation, or other higher-level orchestration.

Those should sit above or beside Cricket commands rather than silently redefining them.

## Guardrails for Future Us

1. **One behavioral source of truth.** Do not maintain independent semantic copies for every platform.
2. **Portability is semantic, not cosmetic.** Different plumbing is fine; different meaning is not.
3. **Commands stay independent.** A user can choose only `/prove-it` if they want.
4. **Deterministic tools establish facts.**
5. **Do not overbuild installation before adapters exist.**

## Definition of portable-v1

- [ ] seven-command core contract reviewed
- [ ] Codex adapter working
- [ ] Cursor adapter working
- [ ] Antigravity adapter working
- [ ] install instructions for each
- [ ] same basic conformance checks across adapters
- [ ] platform limitations documented
- [ ] README no longer calls the adapters scaffolds

A one-command installer is useful but not required for portable-v1.

## If we get sidetracked, resume here

1. Read this file.
2. Read `core/COMMANDS.md`.
3. Inspect `.agents/skills/`.
4. Pick exactly one adapter.
5. Implement one command end-to-end.
6. Test it against the core contract.
7. Repeat for the other six.
8. Only then generalize installation or build the next adapter.

The central question is:

> **Can the user carry the same Cricket behavior from one coding agent to another without relearning what the command means?**

If yes, the architecture is working.
