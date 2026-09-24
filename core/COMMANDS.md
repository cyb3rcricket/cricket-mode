# Cricket Mode command contract

This is the platform-neutral behavioral contract for the seven current Cricket commands.

## `/pitch`

**Purpose:** constrain work before code is written.

**Must:** restate the ask briefly; propose the smallest change that solves it; state explicit non-goals; prefer existing code over invented layers when sufficient; ask before silently widening ambiguous scope.

**Must not:** turn pre-flight planning into a redesign or invent unrelated helpers, abstractions, cleanup, or edge-case machinery.

**Core rule:** **Solve only what was asked. Ask before inventing.**

## `/chirp`

**Purpose:** restate a dense explanation in shorter, plainer language without changing its meaning.

**Must:** preserve important meaning, remove unnecessary jargon, become shorter and easier to understand, and end with a one- or two-sentence **Basically:** summary.

**Must not:** introduce new analysis, change the underlying conclusion, or expand the answer.

## `/senpai`

**Purpose:** teach the user the work that was just built or changed.

**Must:** explain what changed, how the important pieces work together, supported rationale, reusable patterns, and what tends to change versus stay the same.

**Must not:** invent rationale, redo the work unless asked, or turn a small change into an unnecessarily huge lesson.

**Goal:** help the user recognize the pattern next time.

## `/challenge`

**Purpose:** try to break completed work before trusting it.

**Inspect for:** incorrect assumptions, bugs, edge cases, missing error handling, side effects, fragile logic, relevant security/reliability issues, and implementations that run but miss the real requirement.

**Must:** inspect actual work when available; use tests/tools/experiments when useful; separate confirmed findings from possibilities; finish with concrete **Findings** and relevant **Looks solid** results.

**Must not:** invent criticism or automatically fix findings unless asked.

**Core rule:** **Try to break the idea before we trust it.**

## `/prove-it`

**Purpose:** verify that changed behavior actually works and show evidence.

**Must:** exercise real behavior when practical; run relevant tests; prefer the real user/caller path; capture concrete evidence; stay focused on changed behavior; expose failures instead of working around them.

**Evidence preference:** deterministic tools and real execution outrank model confidence.

**Result:** finish with exactly one status: **PASS**, **FAIL**, or **PARTIAL**, with evidence and any remaining gap.

**Core rule:** **Don't tell me it works. Prove it.**

## `/drift`

**Purpose:** find concrete places where a project disagrees with itself.

**Look for:** code vs tests, implementation vs docs, comments vs behavior, config vs runtime, examples vs interfaces, schemas vs handlers, and setup instructions vs actual requirements.

**Must:** show both sides of each disagreement, identify what appears current when evidence supports it, say when truth is unclear, and identify what likely needs attention.

**Must not:** merely list stale files or automatically change files unless asked.

**Core rule:** **Find where the project disagrees with itself.**

## `/scrub`

**Purpose:** find AI-generated residue in recent work without redesigning the system.

**Look for:** narrating comments, speculative helpers, redundant wrappers, defensive machinery hiding the real issue, leftover scaffolding, dead examples, unused imports, and docs that merely repeat code.

**Must:** inspect actual recent work; distinguish residue from intentional design; show evidence; propose surgical delete/simplify/inline actions; keep bugs in `/challenge` territory and contradictions in `/drift` territory.

**Must not:** redesign the system or automatically change code unless asked.

**Core rule:** **Strip the agent fingerprints. Don't redesign the work.**

## Cross-command invariants

1. Commands stay independent.
2. Actual project evidence beats plausible prose.
3. Do not silently widen scope.
4. Do not claim certainty unsupported by evidence.
5. Platform adapters preserve semantics rather than inventing new ones.
6. Small commands are a feature; portability must not turn Cricket Mode into a compulsory framework.
