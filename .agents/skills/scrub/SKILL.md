---
name: scrub
description: Use when cleaning up AI-generated residue left in recent work, such as narrating comments, speculative helpers, redundant wrappers, defensive over-engineering, leftover scaffolding, and docs that restate the code.
---

# Scrub

Find agent fingerprints left in the work just done.

Strip leftover AI habits that make the code noisier without solving the asked-for problem. Do not redesign the system.

Inspect the actual recent work, changed files, or current context. Do not invent a lecture about AI code in general.

## Look For

- narrating or restating comments,
- speculative helpers or abstractions not required by the asked-for change,
- redundant wrappers and pass-through layers,
- defensive try/catch or null guards that paper over real issues,
- leftover scaffolding, unused imports, and dead example code,
- docs or comments that duplicate what the code already says.

Separate real residue from intentional design. Do not invent problems.

For each finding, show the path and a snippet, why it looks like agent residue, and the surgical fix: delete, simplify, or inline.

Do not change code unless I ask. Propose the removal first.

If the right answer is a redesign, say so briefly and stop. That belongs to a different conversation.

Keep these jobs separate:

- `/drift` finds where the project disagrees with itself.
- `/challenge` tries to break the idea: bugs, weak assumptions, edge cases.
- `/scrub` finds leftover agent habits.

If something is a contradiction, say it is `/drift` territory and move on. If something is a bug or a weak assumption, say it is `/challenge` territory and move on.

## Core Rule

**Strip the agent fingerprints. Don't redesign the work.**

Finish with:

**Residue:** concrete findings with evidence and surgical fixes.

**Keep:** things that look intentional or load-bearing, briefly.

**Out of scope:** anything that belongs to `/drift` or `/challenge` instead.
