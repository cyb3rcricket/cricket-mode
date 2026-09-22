# /drift

Points at concrete places where the project contradicts itself.

## Setup

The user ran `/drift` in a notifications worker. The agent read the README, the worker config, and the consumer. Nothing was edited.

## Without /drift

```text
I skimmed the repo. The README, the config, and the worker all talk about retries and the queue. Nothing jumped out as stale. You may want a docs pass later.
```

## With /drift

Two spots disagree.

**Retry limit**

- `README.md` says a failed send is retried 5 times, then dropped.
- `config/worker.toml` sets `max_retries = 3`.
- `src/worker.js` uses that field (`const attempts = config.max_retries`). There is no `5` in the worker.
- Current behavior is 3 retries. The README is the outlier.
- Attention: document 3, or change `max_retries` if 5 is the real policy. I did not change either file.

**Queue name**

- `README.md` tells operators to watch the `notifications` queue.
- `src/worker.js` consumes `config.queue_name`, and `config/worker.toml` sets `queue_name = "notifications.v2"`.
- The consumer that actually runs is `notifications.v2`. The README names a queue this config does not use.
- Attention: a dashboard on `notifications` can look idle while `notifications.v2` backs up. The docs need the name the config sets.

No test asserts either number or name, so the tests are not a third side of this.

## What changed

- The reply quotes the files that disagree, instead of calling the docs "maybe stale."
- Each finding says which side matches the running worker, and what a person should look at.
- Nothing is edited.
