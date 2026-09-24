# Cricket Mode command contract

This is the platform-neutral behavioral contract for the seven current Cricket commands.

## `/pitch`

**Purpose:** constrain work before code is written. This is a pre-flight clamp, not a review of work already done.

**Must:** before any edit, state the pitch, and do not implement until it is stated:

- **Ask:** the problem in one or two sentences.
- **Smallest plan:** the minimal change that solves only that problem.
- **Won't do:** explicit non-goals, including invented helpers, drive-by cleanups, new abstractions, unrelated refactors, and speculative edge-case machinery.

Prefer editing existing code over adding new files or layers when that solves the ask. If the request is ambiguous, or a wider change would help, ask before expanding. After the pitch is stated, implement that plan unless the user redirects.

**Must not:** start coding before the pitch is stated, silently widen scope, turn the pitch into a redesign, or invent unrelated helpers, abstractions, cleanup, or edge-case machinery.

**Core rule:** **Solve only what was asked. Ask before inventing.**

## `/chirp`

**Purpose:** restate the previous reply in shorter, plainer language without changing its meaning.

**Must:** restate that reply in plain conversational language, as one knowledgeable human talking to another; preserve the important meaning, including the conclusions already stated; remove unnecessary jargon; make it shorter and easier to understand; end with a one- or two-sentence **Basically:** summary.

**Must not:** introduce new analysis, change the underlying conclusion, or expand the answer.

## `/senpai`

**Purpose:** teach the user the work that was just built or changed.

**Must:** start with the main idea, then walk through the important pieces; explain what changed, how it works, and how the pieces connect; teach the mechanism, not only the syntax; use the actual work when that helps; give rationale only when the work or conversation supports it; when there is a reusable pattern, say what usually changes and what tends to stay the same. Assume the reader is learning: do not assume technical terms are known, and do not talk down.

**Must not:** invent rationale, redo or change the work unless asked, or turn a small change into a giant lesson.

**Goal:** help the user recognize the pattern next time.

## `/challenge`

**Purpose:** try to break completed work before trusting it.

**Inspect for:** incorrect assumptions, bugs, edge cases, missing error handling, side effects, fragile logic, relevant security or reliability issues, and implementations that run but miss the real requirement.

**Must:** challenge the thing just built, changed, or decided; inspect the actual work when available; use tests, tools, or experiments when they can confirm or disprove a concern; not treat a reasonable look or an easy passing test as proof; separate confirmed findings from possibilities that still need evidence; leave code you did not inspect unchecked instead of reporting it as a finding. Finish with **Findings:** (problems or risks actually found) and **Looks solid:** (important things challenged that did not break).

**Must not:** invent criticism, claim more than the inspected work shows, or automatically fix findings unless asked.

**Core rule:** **Try to break the idea before we trust it.**

## `/prove-it`

**Purpose:** verify that changed behavior actually works and show evidence.

**Must:** exercise real behavior rather than relying only on reading the code or saying it looks correct; run relevant existing tests first when they help; prefer the actual application or the path a real caller would take; exercise the specific change; capture concrete evidence such as output, test results, screenshots, responses, or application state; stay focused on the changed behavior; if something fails, say exactly what failed.

**Evidence preference:** deterministic tools and real execution outrank model confidence.

**Must not:** quietly work around failures to produce a passing result.

**Result:** finish with exactly one status:

- **PASS** — the requested behavior was verified, with the evidence.
- **FAIL** — the behavior failed, with the evidence and exactly what failed.
- **PARTIAL** — some behavior was verified, with the evidence and what remains unverified.

**Core rule:** **Don't tell me it works. Prove it.**

## `/drift`

**Purpose:** find concrete places where a project disagrees with itself.

**Look for:** code vs tests, implementation vs docs, comments vs behavior, config vs runtime, examples vs interfaces, schemas vs handlers, and setup instructions vs actual requirements.

**Must:** use the actual project files; find concrete disagreements that could confuse a developer, break a workflow, or make behavior differ from what the documentation suggests; for each finding show what says one thing, what says something different, which side appears current or that the current side is unclear, and what likely needs attention.

**Must not:** merely list stale files, invent a contradiction, or change files unless asked.

**Core rule:** **Find where the project disagrees with itself.**

## `/scrub`

**Purpose:** find AI-generated residue in recent work without redesigning the system.

**Look for:** narrating or restating comments, speculative helpers or abstractions not required by the change, redundant wrappers and pass-through layers, defensive try/catch or null guards that paper over a real issue, leftover scaffolding, unused imports, dead example code, and docs or comments that duplicate what the code already says.

**Must:** inspect the actual recent work; do not give a general lecture about AI code; distinguish residue from intentional design; for each finding show the path, a snippet, why it looks like residue, and a surgical fix (delete, simplify, or inline). If the right answer is a redesign, say so briefly and stop. Finish with:

- **Residue:** concrete findings with evidence and surgical fixes.
- **Keep:** things that look intentional or load-bearing, briefly.
- **Out of scope:** anything that belongs to `/drift` or `/challenge` instead.

**Must not:** redesign the system, invent residue, or change code unless asked. Bugs and weak assumptions stay in `/challenge`. Contradictions stay in `/drift`.

**Core rule:** **Strip the agent fingerprints. Don't redesign the work.**

## Cross-command invariants

1. Commands stay independent. A user can invoke one without the others.
2. `/pitch` is before code exists. `/challenge` and `/prove-it` are after work exists.
3. `/scrub` does not take bugs from `/challenge` or contradictions from `/drift`.
4. Actual project evidence beats plausible prose.
5. Do not silently widen scope.
6. Do not claim certainty unsupported by evidence.
7. Platform adapters preserve these semantics rather than inventing new ones.
8. Small commands are a feature. Portability must not turn Cricket Mode into a compulsory framework.
