# Orchestration

Optional policy beside the seven Cricket commands. Portable v1 does not need this directory. `python3 cricket install` does not copy it. Nothing here invokes a command, selects a model, or stores attempts.

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

The caller supplies the summary, `expected_files`, `changed_files`, `attempt`, and check results. `decide` does not read the repo or run those checks.

`decide` returns `lane`, `decision`, `model`, `verified_completion`, `unresolved_failures`, `unrelated_failures`, `recommendations`, and `max_attempts`. `model` is always `null`. There is no vendor model name and no automatic model switch. `max_attempts` is 2. There is no loop inside `decide`.

Lanes, in order: `ESCALATE` when `changed_files` is more than twice `expected_files`; otherwise `DEEP` when the summary contains the whole word `auth`; otherwise `FAST` when at most one file changed; otherwise `STANDARD`. `session` and `architecture` do not select a lane.

Check states are `PASSED`, `FAILED`, `NOT RUN`, `NOT RELEVANT`, and `NOT AVAILABLE`.

A check may set `relation` to `RELATED`, `UNRELATED`, or `UNKNOWN`. An omitted or other relation is `UNKNOWN`. `FAILED` plus `RELATED` or `UNKNOWN` is a task failure. `FAILED` plus `UNRELATED` is listed in `unrelated_failures` and does not retry, escalate, or clear a passed related check. The policy does not infer relation.

Decision order: more than twice the expected file count is `ESCALATE`; otherwise a task failure is `RETRY` on attempt 1 and `ESCALATE` on attempt 2 or later; otherwise a `NOT RUN` check is `BLOCKED`; otherwise `COMPLETE`.

`COMPLETE` is not a `/prove-it` PASS. `verified_completion` is true only when a check was reported `PASSED` and no `RELATED` or `UNKNOWN` check failed. A task can be `COMPLETE` with `verified_completion: false`. File-count `ESCALATE` can still report `verified_completion: true` when the checks passed.

Recommendations are chosen from `drift`, `prove-it`, and `challenge`, in that order, and at most two are returned. They are not invoked. A `COMPLETE` task that is not `DEEP` recommends nothing. `pitch`, `chirp`, `senpai`, and `scrub` stay explicit.

## Check

```bash
python3 orchestration/check.py
```

## Known limitations

- The caller must increment `attempt`. Sending `1` again returns `RETRY` again. A missing attempt, or `0`, is treated as 1.
- `DEEP` is only the whole word `auth`. A passing `auth` task still recommends `challenge`.
- Blast radius is invisible unless `expected_files` is set.
- Exactly twice the expected file count does not escalate. More than twice does.
- `COMPLETE` with `verified_completion: false` means no applicable check was reported passed. It does not mean the tests passed.
- This layer has not been run inside Cursor, Codex, or Antigravity.
