# /prove-it

Runs the change and closes with PASS, FAIL, or PARTIAL plus the evidence.

## Setup

`GET /customers?q=` with an empty `q` was returning every customer. The agent changed the handler to return an empty list when `q` is missing or blank. The user ran `/prove-it`.

## Without /prove-it

```text
This works. The handler trims `q` and returns `[]` when it is empty, so a blank search can no longer dump the table. The unit test covers it.
```

## With /prove-it

I ran the customer search tests, then the same request a client makes.

```text
$ npm test -- customers.search
 PASS  src/customers.search.test.js
  blank q returns no rows (18 ms)
  whitespace q returns no rows (11 ms)
  q=ada returns Ada Lovelace (14 ms)

Tests: 3 passed, 3 total
```

```text
$ curl -s "http://localhost:3000/customers?q="
[]

$ curl -s "http://localhost:3000/customers?q=%20%20"
[]

$ curl -s "http://localhost:3000/customers?q=ada"
[{"id":"cus_ada","name":"Ada Lovelace"}]
```

Blank and whitespace `q` match the bug you reported. A non-empty `q` still returns a row, so the guard did not wipe out real searches.

**PASS** — empty and whitespace `q` return `[]` in `customers.search.test.js` and on `GET /customers`. A non-empty `q` still returns the matching customer.

## What changed

- The reply runs the tests and the HTTP request instead of describing the handler.
- The evidence is the command output, including the search that should still return a row.
- The close is a **PASS** line that says what was verified.
