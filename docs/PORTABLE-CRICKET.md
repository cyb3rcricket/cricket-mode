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

`core/COMMANDS.md` is the neutral specification for what the seven commands mean. It has been reviewed against `.agents/skills/` and the transcripts in `examples/`.

### Adapters

`adapters/cursor/`, `adapters/codex/`, and `adapters/antigravity/` expose the seven commands through each host's skill mechanism. All three read `core/COMMANDS.md`. Live Antigravity behavior is not verified from this environment.

### Conformance

`conformance/` checks a reply against one shared case per command. Adapters call it. It does not call a model.

## Deliberately not built yet

Do not assume these exist just because the scaffold exists:

- automatic Codex installation,
- automatic Cursor installation,
- automatic Antigravity installation,
- a universal command registry,
- a one-command installer,
- model routing,
- Luna/Sol escalation,
- Jev integration,
- autonomous retry loops.

First make the existing seven behaviors portable. Then decide which orchestration ideas have earned their complexity.

## Implementation plan

### Phase 1 — confirm the contract (done)

Reviewed `core/COMMANDS.md` against `.agents/skills/*/SKILL.md` and the transcripts in `examples/`. The contract now keeps the behaviors those sources already require, including the pitch stated before edits, chirp restating the previous reply, senpai teaching the mechanism, challenge separating findings from uninspected code, prove-it running the real behavior, and scrub closing with Residue, Keep, and Out of scope.

`examples/` has transcripts for `/chirp`, `/senpai`, `/challenge`, `/prove-it`, and `/drift`. `/pitch` and `/scrub` were checked against their skill files only. The reference skills were not rewritten.

### Phase 2 — build one adapter end to end (done)

Chose Cursor. The other adapters were left for later.

`adapters/cursor/` exposes all seven commands as Cursor Agent Skills. Each `SKILL.md` is wiring: it points at one shared contract file, which links to `core/COMMANDS.md`. Install steps, invocation, and limitations are in `adapters/cursor/README.md`. `adapters/cursor/check.py` installs that tree into a temporary project's `.cursor/skills/` and checks discovery plus the contract link.

### Phase 3 — conformance tests (done)

`conformance/` is the shared behavior matrix. One case per command supplies the fixture. `conformance/check.py` encodes the contract checks once. `python3 conformance/check.py` scores the bundled pass and fail replies. A later adapter imports `evaluate` instead of copying the rules. The checker does not call a model. The Codex and Antigravity adapter checks run this suite. Neither check opens the host application.

### Phase 4 — second and third adapters

**Codex (done).** `adapters/codex/` exposes the seven commands as Codex skills invoked with `$name`, not as `/name` slash commands. Each skill points at one shared contract file. `agents/openai.yaml` sets `allow_implicit_invocation: false`. Install steps and limitations are in `adapters/codex/README.md`. `adapters/codex/check.py` installs that tree into a temporary project's `.agents/skills/` and runs `conformance/check.py`.

**Antigravity (adapter written).** `adapters/antigravity/` exposes the seven commands as Antigravity skills. The documented invoke is `/name`. Official skill frontmatter has no switch that disables autonomous activation. `adapters/antigravity/check.py` installs the tree and runs `conformance/check.py`. Opening Antigravity is still required before calling the live behavior verified. See `adapters/antigravity/README.md`.

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

- [x] seven-command core contract reviewed
- [x] Codex adapter working
- [x] Cursor adapter working
- [ ] Antigravity adapter working
- [ ] install instructions for each
- [ ] same basic conformance checks across adapters
- [ ] platform limitations documented
- [ ] README no longer calls the adapters scaffolds

A one-command installer is useful but not required for portable-v1.

## If we get sidetracked, resume here

The Antigravity adapter is written. Resume at Phase 5: a small installer. Do not start Phase 6.

1. Read this file.
2. Read `adapters/antigravity/README.md` and `conformance/README.md`.
3. Add the small installer in Phase 5. Leave model routing and the other Phase 6 ideas alone.

The central question is:

> **Can the user carry the same Cricket behavior from one coding agent to another without relearning what the command means?**

If yes, the architecture is working.
