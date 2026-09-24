# Cricket Mode core

This directory defines the **platform-neutral meaning** of Cricket Mode.

The core answers:

> If someone invokes `/prove-it`, what behavior should they get regardless of whether the agent is Codex, Cursor, Antigravity, or something else?

It does not answer where a platform stores instructions or how that platform discovers commands. Those are adapter questions.

## Source of truth

- `COMMANDS.md` is the portable behavioral contract.
- `.agents/skills/*/SKILL.md` are the current working reference implementations used to derive and test that contract.
- `adapters/` translates the contract into platform-specific forms.

Do not delete or rewrite the reference skills merely to make the directory structure look cleaner. They remain the reference copy.

## What belongs in core

Core may define purpose, triggers, required behavior, boundaries, evidence expectations, result shape, and relationships between commands.

Core should avoid vendor names, editor-specific paths, model names, API keys, installation mechanics, and assumptions about one product's command system.

## Design test

A rule is probably portable if this sentence still makes sense:

> Any capable coding agent could follow this rule if an adapter exposed it.

If it only makes sense for one product, it belongs in that product's adapter.
