---
name: pitch
description: Use when about to write or expand code, to clamp the change to the smallest edit that solves only the stated problem and ask before inventing helpers, abstractions, or extra scope.
---

# Pitch

Constrain the approach before you write or expand code.

Solve only the problem that was asked. The smallest change that does that job is the whole plan.

Before changing anything, state the pitch:

1. Restate the asked-for problem in one or two sentences.
2. Propose the smallest change that solves only that problem.
3. List what you will not do.

Prefer editing existing code over adding new files or layers when that solves the ask.

If the request is ambiguous, or a wider change would help, ask before expanding. Do not silently widen scope.

Do not start implementing until the pitch is stated. After it is stated, proceed with that plan unless the user redirects.

This is the pre-flight clamp. It is not a review of work already done.

- `/challenge` tries to break work after it exists.
- `/prove-it` verifies work after it exists.
- `/pitch` decides the smallest change before the code exists.

## Core Rule

**Solve only what was asked. Ask before inventing.**

State this before coding:

**Ask:** the problem in one or two sentences.

**Smallest plan:** the minimal change.

**Won't do:** explicit non-goals, including invented helpers, drive-by cleanups, new abstractions, unrelated refactors, and speculative edge-case machinery.

Then implement that plan unless the user stops you.
