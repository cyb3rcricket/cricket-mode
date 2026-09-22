# /challenge

Tries to break the work just finished, then separates real findings from what held up.

## Setup

The user asked for `POST /invoices/:id/pay`: mark that invoice paid and email a receipt. The agent added the handler below and said it was done. The user ran `/challenge` and did not ask for a fix.

```text
function pay(req, res) {
  const invoice = db.getInvoice(req.params.id);
  db.markPaid(invoice.id, req.body.amount);
  sendReceipt(invoice.customerEmail, req.body.amount);
  res.status(200).json({ ok: true });
}
```

## Without /challenge

```text
Looks good. It loads the invoice, marks it paid for the amount in the body, sends the receipt, and returns 200. Happy to add tests if you want them.
```

## With /challenge

I tried to break `pay` against the request: mark that invoice paid, once, for its own amount, then email a receipt. There is no test for this route in the diff, so this is from reading the handler.

The function never reads `invoice.status`. Every call reaches `markPaid` and `sendReceipt`. A second request sends another receipt. I have not seen `markPaid`, so I am not claiming the ledger row is duplicated inside it. I am claiming this handler will try again.

The amount it passes is `req.body.amount`. `invoice.amount` is never read. A client can submit `1` for a $900 invoice, and this function will pass `1` through.

`sendReceipt` runs before the response, with no `catch` in this function. If the mailer throws, the client gets an error after `markPaid` has already been called, and a retry enters `pay` again. I did not run the mailer. That follows from the call order.

I looked for an auth check in this handler and did not find one. Whether a router wraps the route is outside the diff, so that is not a finding.

**Findings:** A repeat call always hits `markPaid` and `sendReceipt`; this function does not look at status. The amount passed in is the client's, not the invoice's. A receipt throw happens after `markPaid`, so a retry runs the handler again.

**Looks solid:** The id written is `invoice.id` from `getInvoice(req.params.id)`. This function does not take the invoice id from the body.

## What changed

- The reply tries repeat calls, a client-supplied amount, and a throwing mailer, instead of approving the happy path.
- Findings are tied to the handler. The unseen auth wrapper is left unchecked, not reported as a bug.
- Nothing is rewritten. The close is **Findings:** and **Looks solid:**.
