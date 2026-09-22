# /senpai

Teaches the work just done: what changed, how it works, why, and the pattern to reuse.

## Setup

`GET /orders` was timing out on pages past about 50,000 rows. The list already used `ORDER BY id DESC`. The user asked the agent to stop using `OFFSET`. The agent switched the route to a cursor and left the rest of the API in place. The user then ran `/senpai`.

## Without /senpai

```text
Done. GET /orders now takes ?cursor= instead of ?offset=. The response includes next_cursor. Tests updated.
```

## With /senpai

The list no longer says "skip the first N rows." It says "start after this order."

I replaced `offset` on `GET /orders` with a `cursor` query param and a `next_cursor` field on the response. Limits and the `id DESC` sort stayed.

`OFFSET 50000` makes the database walk 50,000 rows and throw them away before it returns a page. That gets slower the deeper someone goes. A cursor names the last order the client already has, and the query only reads rows after that one.

The handler does three things:

```text
GET /orders?limit=50&cursor=ord_1842

1. No cursor: start at the newest order.
2. Otherwise treat the cursor as an order id and read
   WHERE id < $cursor ORDER BY id DESC LIMIT 50.
3. If another row exists past this page, return its id as next_cursor.
   If not, next_cursor is null.
```

The cursor is the order id, not a page number. A page number goes stale if a row is inserted or deleted between requests. An id does not: the next page continues from the row the client last saw.

This shape matches the task. Deep `OFFSET` pages were the timeout, and the route already sorted by `id DESC`, so continuing from an id reused that order. Nothing else on the API had to move.

Next time, the part that stays is: remember the last row, ask for rows after it, and use null when there is no next row. The part that changes is which column you sort by and how that column is packed into the cursor. If the sort is not unique, the cursor needs a tie-breaker. Here `id` already is one.

## What changed

- The reply teaches skip-and-discard versus start-after-this-row, instead of announcing the new query param.
- The reason is the one from the task: deep `OFFSET` pages timed out, and the existing `id DESC` sort could carry the cursor.
- It names what to reuse (last row, rows after it, null when finished) and what changes next time (sort column, cursor encoding).
