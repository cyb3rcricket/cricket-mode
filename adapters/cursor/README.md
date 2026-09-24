# Cursor adapter — scaffold

**Status: planned / not implemented yet.**

This directory is reserved for the Cursor-specific layer that will expose Cricket Mode's platform-neutral commands without changing their behavior.

## Intended responsibilities

- document the supported Cursor instruction/command placement,
- expose or map all seven Cricket commands,
- translate the portable contract into Cursor-native mechanisms,
- document installation and update steps,
- document platform-specific limitations,
- add a minimal conformance test.

## Do not duplicate the core

Command semantics belong in `../../core/COMMANDS.md`.

The current working reference implementations remain in `../../.agents/skills/`.

Prefer generation, links, or thin wrappers over maintaining a second hand-edited copy of every command.

## Completion condition

Do not change this status to implemented until all seven commands have been exercised in Cursor and their behavior matches the core contract.
