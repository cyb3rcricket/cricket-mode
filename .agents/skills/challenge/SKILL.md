---
name: challenge
description: Use when recent work looks finished but should not be trusted yet — inspect it for bugs, weak assumptions, edge cases, missing error handling, and side effects, and report findings without fixing unless asked.
---

# Challenge

Challenge the thing you just built, changed, or decided.

Do not assume it is correct just because it looks reasonable or passed an easy test.

Try to find what could be wrong.

## Look For

- incorrect assumptions,
- bugs and edge cases,
- missing error handling,
- unintended side effects,
- fragile logic,
- security or reliability problems when relevant,
- cases where the implementation technically works but does not solve the real problem.

Inspect the actual code or work when available.

Use tests, tools, or experiments when they can confirm or disprove a concern.

Do not invent problems just to be critical. Separate real findings from possibilities that still need evidence.

Do not automatically fix anything unless I ask.

## Core Rule

**Try to break the idea before we trust it.**

Finish with:

**Findings:** the problems or risks you actually found.

**Looks solid:** anything important you challenged but could not break.