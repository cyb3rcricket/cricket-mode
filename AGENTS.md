# Cricket Mode agent guidance

Cricket Mode is a lightweight, portable behavior layer for coding agents: a set of small, opt-in commands that help clamp scope, challenge assumptions, verify work, explain changes, and clean up without imposing a required workflow.

## Project rule

Preserve the distinction between **core behavior** and **platform adapters**.

- `core/` defines what a Cricket command means.
- `.agents/skills/` contains the current working reference implementations.
- `adapters/` contains platform-specific glue.
- `docs/PORTABLE-CRICKET.md` is the architecture and continuation plan.
- `orchestration/` is an optional policy beside the commands. Portable v1 does not require it.

Do not make a platform-specific behavior part of the core unless it is genuinely required for the command's meaning.

## Commands are opt-in

Do not silently run every Cricket behavior on every task.

When a user explicitly invokes a Cricket command, or clearly asks for that command's behavior, follow `core/COMMANDS.md`.

The commands must remain independently useful.

## Evidence rule

Prefer deterministic evidence when software can answer the question: tests for test results, build tools for compilation, type checkers for types, linters for lint, `git diff` for changes, and the real application path for user-visible behavior.

AI judgment may interpret evidence or handle uncertainty, but it should not replace a relevant deterministic check.

## Portability rule

Adapters may translate command discovery, invocation syntax, instruction placement, tool wiring, and installation mechanics.

Adapters must not quietly redefine a command's purpose, scope boundary, evidence requirement, or result semantics.

If a platform cannot support a behavior exactly, document the limitation instead of pretending parity exists.

## Keep Cricket small

Cricket Mode is not a mandatory agent framework.

`orchestration/policy.py` is the optional Phase 6 policy. It recommends a lane and, at most, existing Cricket commands. It does not select a model, run tests, or invoke those commands. Do not turn it into a router or an autonomous loop unless a later phase says so.
