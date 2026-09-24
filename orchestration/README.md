# Orchestration

Optional policy beside the seven Cricket commands. Portable v1 does not need this directory. `python3 cricket install` does not copy it. Nothing here invokes a command or selects a model.

## Call

```python
from orchestration.policy import decide

result = decide({
    "summary": "Add a name search for quests",
    "expected_files": 3,
    "changed_files": ["a.py", "b.py", "test_b.py"],
    "attempt": 1,
    "checks": [{"name": "pytest", "status": "PASSED"}],
})
```

`decide` returns `lane`, `decision`, `model`, `verified_completion`, `unresolved_failures`, `unrelated_failures`, `recommendations`, and `max_attempts`. `model` is always `null`. `max_attempts` is 2. The caller passes `attempt`. There is no loop inside `decide`.

Lanes are `FAST`, `STANDARD`, `DEEP`, and `ESCALATE`. Check states are `PASSED`, `FAILED`, `NOT RUN`, `NOT RELEVANT`, and `NOT AVAILABLE`.

A check may set `relation` to `RELATED`, `UNRELATED`, or `UNKNOWN`. Omitted relation is `UNKNOWN`. `FAILED` plus `RELATED` or `UNKNOWN` still drives `RETRY` or `ESCALATE`. `FAILED` plus `UNRELATED` is listed in `unrelated_failures` and does not retry, escalate, or clear a passed related check. The policy does not infer relation.

`COMPLETE` is not a `/prove-it` PASS. `verified_completion` is true only when a check was reported `PASSED` and no `RELATED` or `UNKNOWN` check failed. A task can be `COMPLETE` with `verified_completion: false`.

Recommendations name at most two of `prove-it`, `challenge`, and `drift`. They are not invoked. `pitch`, `chirp`, `senpai`, and `scrub` stay explicit.

`discover_checks(path)` reads a Makefile and returns target names. It does not run those targets.

## Check

```bash
python3 orchestration/check.py
```

## Known limitations

- The caller must increment `attempt`. Sending `1` again returns `RETRY` again.
- The words `session` and `architecture` mark the lane `DEEP`, even when the task is ordinary.
- Blast radius is invisible unless `expected_files` is set.
- Exactly twice the expected file count does not escalate. More than twice does.
- `COMPLETE` with `verified_completion: false` means no applicable check was reported passed. It does not mean the tests passed.
- This layer has not been run inside Cursor, Codex, or Antigravity.
