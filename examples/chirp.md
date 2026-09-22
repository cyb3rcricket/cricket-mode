# /chirp

Restates the previous reply in plain language and ends with the main idea.

## Setup

The checkout modal's close button sometimes does nothing after a sticky promo bar was added. The agent answered with a stacking-context explanation. The user then ran `/chirp`.

## Without /chirp

```text
The close control is a descendant of a stacking context created by the promo bar. The bar is position: sticky with z-index: 2, and the slide-in applies transform: translateZ(0). A transformed element forms a containing stacking context, so descendant z-index values are compared only with siblings inside that context. The modal's z-index: 1000 therefore never competes with the scrim. The scrim is a later sibling in the root context and paints above the entire bar, modal included. Hit-testing resolves to the scrim, which has no click handler, so the close button appears dead. Remove the transform from the bar, or portal the modal to a node directly under document.body so its z-index participates in the root stacking context.
```

## With /chirp

The close button is fine. The problem is which box is actually on top.

The promo bar uses a CSS `transform` that puts it in its own little layer. The modal lives inside that layer, so its "put me on top" number only competes with other things in the bar, not with the rest of the page. The dimmed backdrop sits outside that layer and covers the modal. Clicks land on the backdrop.

Two ways out: stop using that `transform` on the bar, or render the modal as a direct child of the page (`document.body`) so it stacks with the rest of the page.

**Basically:** A CSS `transform` on the promo bar traps the modal under the backdrop, so clicks never reach the close button.

## What changed

- Stacking-context and hit-testing jargon is replaced with which box is on top and where the click lands.
- Both fixes stay, in the same order, without the specification language.
- The reply ends with **Basically:** and a one-sentence takeaway.
