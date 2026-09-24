# Conformance

Platform-neutral checks for the seven Cricket commands. The rules live in `check.py`. The fixtures live in `cases.json`. An adapter should call this module instead of copying either one.

## Run

From the repository root:

```bash
python3 conformance/check.py
```

That run scores the pass and fail replies stored in `cases.json`. It also checks that the labels these rules require are still present in `core/COMMANDS.md`.

## Adapter use

```python
from conformance import evaluate, load_cases

for case in load_cases():
    reply = collect_reply(case["fixture"])  # the adapter does this
    failed = evaluate(case["command"], reply, case)
```

`evaluate` returns rule ids. An empty list means the reply matched that case. `collect_reply` is not part of this layer.

## What is deterministic

`evaluate` only reads the reply string and the case. It checks order and presence of the contract labels, required fixture phrases, word count for `/chirp`, a single closing status for `/prove-it`, and that `/scrub` keeps other commands' items out of **Residue:**.

The bundled samples are the proof that those rules fire. They are not model outputs.

## What still depends on a model

A live adapter has to produce the reply. This layer does not call a model, score embeddings, or decide that a reply is wise. Phrase checks can be satisfied by text that contains the required words and still misses the point, and they can miss a real problem that uses different words.

`/drift` does not inspect a git diff, so a reply can name both sides and still have edited a file. `/challenge` treats a rewrite as a fix only when it contains that case's `fix_markers`.

## Rules

| Command | Rule ids |
| --- | --- |
| `/pitch` | `pitch.labels`, `pitch.before`, `pitch.scope`, `pitch.no_widen` |
| `/chirp` | `chirp.shorter`, `chirp.basically`, `chirp.keeps`, `chirp.drops` |
| `/senpai` | `senpai.mechanism`, `senpai.pattern`, `senpai.stays`, `senpai.changes` |
| `/challenge` | `challenge.closes`, `challenge.confirmed`, `challenge.possibility`, `challenge.no_fix` |
| `/prove-it` | `proveit.status`, `proveit.evidence` |
| `/drift` | `drift.sides` |
| `/scrub` | `scrub.closes`, `scrub.concrete`, `scrub.surgical`, `scrub.no_redesign`, `scrub.separated` |
