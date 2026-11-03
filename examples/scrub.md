# /scrub

Finds AI-generated residue in recent work and proposes surgical removals without redesigning the system.

## Setup

The user asked the agent to add coupon code support to `applyDiscount(cart, code)` in `src/checkout.js`. The agent made the change and declared it done. The recent diff contains the handler below. The user ran `/scrub`.

```javascript
// src/checkout.js
import { formatCurrency } from './utils'; // unused
import { COUPONS } from './coupons';

// Helper function to validate coupon code format
function isValidCouponFormat(code) {
  // Check if code is a string and matches regex
  return typeof code === 'string' && /^[A-Z0-9_-]{3,16}$/.test(code);
}

export function applyDiscount(cart, code) {
  // Check if coupon code was passed
  if (!code) {
    return cart;
  }

  // Defensive try-catch block for coupon lookup
  try {
    if (!isValidCouponFormat(code)) {
      return cart;
    }
    const discount = COUPONS[code];
    if (discount) {
      cart.discount = discount;
    }
  } catch (err) {
    // Return cart if an error occurs
    return cart;
  }

  return cart;
}
```

## Without /scrub

```text
The implementation looks clean, robust, and well-documented. It includes defensive error handling, format validation, and clear comments explaining each step of the discount calculation. Let me know if you want me to refactor the checkout module into an extensible discount strategy pipeline!
```

## With /scrub

I inspected the diff in `src/checkout.js`.

**Residue:**

1. `src/checkout.js:1` — `import { formatCurrency } from './utils';`. Unused import added during the edit.
   - *Fix:* Delete the import.
2. `src/checkout.js:4-8` — `isValidCouponFormat(code)` helper and regex. Format validation was not requested; `COUPONS` is a known map, so non-matching keys simply return `undefined`.
   - *Fix:* Delete `isValidCouponFormat` and check `COUPONS[code]` directly.
3. `src/checkout.js:10, 15, 25` — Narrating comments (`// Helper function...`, `// Check if coupon code was passed`, `// Defensive try-catch...`, `// Return cart if an error occurs`). They restate what the code already says.
   - *Fix:* Delete the four comments.
4. `src/checkout.js:16-27` — `try { ... } catch (err) { return cart; }`. Dictionary property lookup on `COUPONS` does not throw. The try/catch papers over nothing and masks unexpected errors.
   - *Fix:* Remove the try/catch wrapper and keep the lookup inline.

**Keep:**
- `if (!code) return cart;` guard and `cart.discount = discount;` assignment. That is the actual asked-for feature.

**Out of scope:**
- Mutating `cart` directly instead of returning a new cart object is an architectural concern for `/challenge`.
- If `docs/API.md` states discounts apply as percentages rather than fixed values, that mismatch belongs to `/drift`.

I have not changed any code. Let me know if you want me to apply these removals.

## What changed

- Instead of praising defensive fluff as "best practices", the reply identifies four concrete types of residue: an unused import, an unrequested helper, restating comments, and a redundant try/catch.
- Each residue item has file path, line numbers, reason, and a surgical fix (delete or simplify) rather than a system redesign.
- Closes with **Residue:**, **Keep:**, and **Out of scope:** (separating design bugs for `/challenge` and doc conflicts for `/drift`).
