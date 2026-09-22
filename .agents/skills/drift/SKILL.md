---
name: drift
description: Finds places where a project no longer agrees with itself.
---

# Drift

Find where this project has drifted out of sync with itself.

Look for contradictions between:

- code and tests,
- implementation and documentation,
- comments and actual behavior,
- configuration and runtime behavior,
- examples and current interfaces,
- schemas and handlers,
- setup instructions and real requirements.

Do not just list stale files.

Find concrete disagreements that could confuse a developer, break a workflow, or make the project behave differently than its documentation suggests.

For each finding, show:

- what says one thing,
- what says something different,
- which behavior appears current based on the available evidence, or say when it is unclear,
- and what likely needs attention.

Use the actual project files as evidence.

Do not change anything unless I ask.

## Core Rule

**Find where the project disagrees with itself.**