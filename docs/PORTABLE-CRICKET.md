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

`.agents/skills/` contains the seven reference skills. They stay in place. `python3 cricket` will not overwrite them.

### Portable contract

`core/COMMANDS.md` is the neutral specification for what the seven commands mean. It has been reviewed against `.agents/skills/` and the transcripts in `examples/`.

### Adapters

`adapters/cursor/`, `adapters/codex/`, and `adapters/antigravity/` expose the seven commands through each host's skill mechanism. All three read `core/COMMANDS.md`. The adapter checks do not open the hosts. Live sessions for Cursor, Codex, and Antigravity are recorded below. Portable v1 is complete.

### Conformance

`conformance/` checks a reply against one shared case per command. The Cursor, Codex, and Antigravity checks call it. The conformance checker does not call a model.

## Deliberately not built yet

Do not assume these exist:

- a universal command registry,
- model routing,
- Luna/Sol escalation,
- Jev integration,
- autonomous retry loops.

The seven behaviors have adapters, an installer, and recorded live sessions. `orchestration/` is an optional policy beside those commands. It does not route models, and it does not retry on its own.

## Implementation plan

### Phase 1 — confirm the contract (done)

Reviewed `core/COMMANDS.md` against `.agents/skills/*/SKILL.md` and the transcripts in `examples/`. The contract now keeps the behaviors those sources already require, including the pitch stated before edits, chirp restating the previous reply, senpai teaching the mechanism, challenge separating findings from uninspected code, prove-it running the real behavior, and scrub closing with Residue, Keep, and Out of scope.

`examples/` has transcripts for `/chirp`, `/senpai`, `/challenge`, `/prove-it`, and `/drift`. `/pitch` and `/scrub` were checked against their skill files only. The reference skills were not rewritten.

### Phase 2 — build one adapter end to end (done)

Chose Cursor. The other adapters were left for later.

`adapters/cursor/` exposes all seven commands as Cursor Agent Skills. Each `SKILL.md` is wiring: it points at one shared contract file. In this repository that file is a symlink to `core/COMMANDS.md`. Install steps, invocation, and limitations are in `adapters/cursor/README.md`. `adapters/cursor/check.py` installs that tree into a temporary project's `.cursor/skills/`, checks discovery plus the contract copy, and then runs `conformance/check.py`. That script does not open Cursor. The live session is recorded under Live sessions.

### Phase 3 — conformance tests (done)

`conformance/` is the shared behavior matrix. One case per command supplies the fixture. `conformance/check.py` encodes the contract checks once. `python3 conformance/check.py` scores the bundled pass and fail replies. A later adapter imports `evaluate` instead of copying the rules. The checker does not call a model. The Cursor, Codex, and Antigravity adapter checks run this suite. None of them opens the host application.

### Phase 4 — second and third adapters

**Codex (done).** `adapters/codex/` exposes the seven commands as Codex skills invoked with `$name`, not as `/name` slash commands. Each skill points at one shared contract file. `agents/openai.yaml` sets `allow_implicit_invocation: false`. Install steps and limitations are in `adapters/codex/README.md`. `adapters/codex/check.py` installs that tree into a temporary project's `.agents/skills/` and runs `conformance/check.py`. That script does not open Codex. The live session is recorded under Live sessions.

**Antigravity (done).** `adapters/antigravity/` exposes the seven commands as Antigravity skills. The documented invoke is `/name`. Official skill frontmatter has no switch that disables autonomous activation. `adapters/antigravity/check.py` installs the tree and runs `conformance/check.py`. That script does not open Antigravity. The live session, including one `/pitch` run that also surfaced `challenge`, is recorded under Live sessions and in `adapters/antigravity/README.md`.

### Phase 5 — installation/update tooling (done)

`python3 cricket` copies one adapter out of this checkout. It is not a package manager. The contract bytes always come from `core/COMMANDS.md`. The script never writes that file.

```text
python3 cricket install cursor --target /path/to/project
python3 cricket install codex --target /path/to/project
python3 cricket install antigravity --target /path/to/project
python3 cricket update --target /path/to/project
python3 cricket test
```

`--target` defaults to the current directory. The command is `python3 cricket` because the script has no install step of its own.

| Adapter | Files created or replaced |
| --- | --- |
| cursor | `.cursor/skills/<command>/SKILL.md` and `.cursor/skills/cricket-contract/COMMANDS.md` |
| codex | `.agents/skills/<command>/SKILL.md`, `.agents/skills/<command>/agents/openai.yaml`, and `.agents/skills/cricket-contract/COMMANDS.md` |
| antigravity | `.agents/skills/<command>/SKILL.md` and `.agents/skills/cricket-contract/COMMANDS.md` |

`<command>` is `pitch`, `chirp`, `senpai`, `challenge`, `prove-it`, `drift`, and `scrub`. Each installed `SKILL.md` contains the line `Cricket adapter: cursor`, `Cricket adapter: codex`, or `Cricket adapter: antigravity`. That line is how the script tells an adapter install from a reference skill.

`update` replaces an installed `cricket-contract/COMMANDS.md` from `core/COMMANDS.md` when `pitch/SKILL.md` carries one of those lines. It does not replace skill files.

A repeat install of the same adapter replaces that adapter's skill folders and writes the contract again. If `COMMANDS.md` is a symlink, the script unlinks it and writes a regular file. It does not copy through the link.

Codex and Antigravity both use `.agents/skills`. This repository keeps its reference skills in that same directory. Those reference files are not stamped, and Codex and Antigravity stamps are different. The installer refuses the install when any of the seven skill paths is unstamped or stamped for the other host, and it writes nothing. It does not merge the two adapters, and it does not overwrite the reference skills. Install Codex or Antigravity into another project. Cursor writes `.cursor/skills`, so it can sit beside `.agents/skills`.

`python3 cricket test` runs those cases in a temporary directory.

### Phase 6 — optional orchestration

`orchestration/policy.py` is a pure function. The caller supplies the summary, `expected_files`, `changed_files`, `attempt`, and check results. A result dict comes out. `decide` does not read the repo, store attempts, run checks, invoke Cricket, or select a model. `model` is always null. There is no vendor model mapping. `max_attempts` is 2. There is no loop inside `decide`.

Lanes, in order: `ESCALATE` when more than twice the expected files changed; otherwise `DEEP` only for the whole word `auth`; otherwise `FAST` for at most one changed file; otherwise `STANDARD`. `session` and `architecture` do not select a lane.

`FAILED` with `RELATED`, `UNKNOWN`, or no relation is a task failure. `FAILED` with `UNRELATED` stays visible and does not retry or escalate. Decision order: more than twice the expected file count is `ESCALATE`; otherwise a task failure is `RETRY` on attempt 1 and `ESCALATE` after that; otherwise `NOT RUN` is `BLOCKED`; otherwise `COMPLETE`.

`COMPLETE` is not a `/prove-it` PASS. `verified_completion` is true only when a check was reported `PASSED` and no related or unknown check failed. Recommendations may name `prove-it`, `challenge`, or `drift`, at most two, and nothing is invoked. A `COMPLETE` task that is not `DEEP` recommends nothing. `pitch`, `chirp`, `senpai`, and `scrub` stay explicit. The installer still copies only the seven commands. `core/COMMANDS.md` does not mention lanes. Details and the call example are in `orchestration/README.md`.

Known limits, left in place: the caller must increment `attempt`, and a missing attempt or `0` is treated as 1; a passing `auth` task still recommends `challenge`; blast radius needs `expected_files`; exactly twice the expected count does not escalate; `COMPLETE` with `verified_completion: false` is not a passed test; this layer has not been run inside a host.

## Guardrails for Future Us

1. **One behavioral source of truth.** Do not maintain independent semantic copies for every platform.
2. **Portability is semantic, not cosmetic.** Different plumbing is fine; different meaning is not.
3. **Commands stay independent.** A user can choose only `/prove-it` if they want.
4. **Deterministic tools establish facts.**
5. **Do not overbuild installation before adapters exist.**

## Live sessions

These sessions are separate from the deterministic checks. The checks still do not open a host.

**Cursor — LIVE VALIDATED.** `/pitch` was explicitly invoked. Cursor loaded the Cricket skill and shared contract, and stated Ask / Smallest plan / Won't do before editing. A normal prompt without Cricket did not auto-trigger the skill. `/prove-it` performed real execution and file verification and ended with **PASS**.

**Codex — LIVE VALIDATED.** `$pitch` was explicitly invoked. Codex loaded the Cricket skill and followed the shared contract, and stated Ask / Smallest plan / Won't do before editing. A normal prompt without Cricket did not auto-trigger Cricket. `$prove-it` performed real filesystem verification and ended with **PASS**.

**Antigravity — LIVE VALIDATED.** `/pitch` was explicitly invoked. Antigravity loaded the installed `SKILL.md` and shared `COMMANDS.md`, stated Ask / Smallest plan / Won't do, and implemented the requested file. A normal prompt without Cricket did not invoke any Cricket skill. `/prove-it` performed real filesystem, content, and byte verification and ended with **PASS**. During that `/pitch` run, Antigravity also surfaced `challenge` as a used skill. That is observed host behavior on one explicit `/pitch` run. It is a platform-specific limitation, not a Portable v1 failure, because the normal prompt did not auto-run Cricket.

## Definition of portable-v1

Portable v1 is complete.

- **DONE** — seven-command core contract reviewed against the reference skills and the transcripts that exist.
- **DONE** — Codex adapter. Deterministic check passes. LIVE VALIDATED for `$pitch`, a normal prompt that did not auto-trigger Cricket, and `$prove-it` ending **PASS**.
- **DONE** — Cursor adapter. Deterministic check passes. LIVE VALIDATED for `/pitch`, a normal prompt that did not auto-trigger the skill, and `/prove-it` ending **PASS**.
- **DONE** — Antigravity adapter. Deterministic check passes. LIVE VALIDATED for `/pitch`, a normal prompt that did not invoke any Cricket skill, and `/prove-it` ending **PASS**. One `/pitch` run also surfaced `challenge`.
- **DONE** — install and update tooling. `python3 cricket install` and `python3 cricket update` are documented, and `python3 cricket test` covers them.
- **DONE** — same basic conformance checks across adapters. Cursor, Codex, and Antigravity checks run `conformance/check.py` and require each command's bundled pass fixture to return no rule failures.
- **DONE** — platform limitations documented in each adapter README, including the Antigravity `/pitch` observation.
- **DONE** — README does not call the adapters scaffolds.

Phase 6 policy is in `orchestration/`. Model routing, autonomous loops, and Phase 7 are not started.

## If we get sidetracked, resume here

Portable v1 is complete. The optional policy is in `orchestration/`. Do not start Phase 7 from this reconstruction.

`session` and `architecture` are not `DEEP` tokens. `auth` still is. Do not start Phase 7 from this note.

The central question is:

> **Can the user carry the same Cricket behavior from one coding agent to another without relearning what the command means?**

If yes, the architecture is working.
