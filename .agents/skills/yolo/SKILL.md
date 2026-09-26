---
name: yolo
description: Use when the user wants one complete Cricket pass on a single task — pitch, build, challenge, prove-it, then senpai and scrub if it actually passed. Not sticky. Not a license to invent scope or auto-fix findings.
---

# YOLO

Run one complete Cricket pass, then walk off.

The name is a joke. The gates are not. Do not treat `/yolo` as "just ship it."

## Order

1. `/pitch` — state Ask / Smallest plan / Won't do. No edits before that.
2. Build only that plan.
3. `/challenge` — try to break it. Do not patch unless asked.
4. `/prove-it` — real behavior, real evidence, exactly one of PASS, FAIL, PARTIAL.
5. On PASS only: `/senpai`, then `/scrub`.
6. Stop.

`/drift` and `/chirp` stay out unless asked.

## Stops

- Ambiguous ask → pitch cannot be stated → wait.
- Challenge findings → stop. Report them. Do not "go ahead and fix."
- Prove-it FAIL → stop.
- Scope starting to grow → ask before inventing.

A PARTIAL is not a PASS. Say what is unverified. Do not continue into senpai/scrub as if it shipped.

## Must not

- Stay on after this pass
- Become a mode, router, or /goal replacement
- Skip challenge or prove-it because the name sounds brave
- Redesign during scrub
- Quietly work around a failed check

## Close

Use each child command's required close, then:

**YOLO:** COMPLETE | STOPPED at `<step>` | BLOCKED (`why`)

## Core Rule

**YOLO the sequence. Not the judgment.**
