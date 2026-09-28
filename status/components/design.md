# Component: design

**Purpose:** keep the interface the decided instrument panel of [`docs/14-design-system.md`](../../docs/14-design-system.md) — measured, gated, and audited rather than asserted.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-185 … T-190 |
| Owns | tokens, the design gate, craft review, contrast and accessibility evidence, state completeness |
| Depends on | ui (phase 07), delivery (phase 11) |
| Canonical docs | [docs/14-design-system.md](../../docs/14-design-system.md) · [handbooks/07-anti-slop-rules.md](../../handbooks/07-anti-slop-rules.md) §11–§14 |

## Deliverables

- No visual value outside `ui/theme/Tokens.kt`; every spacing and radius on the scale, or documented as an exception (T-185).
- Every gate rule proven to fire on a real injected violation and reverted, with a clean tree afterwards (T-186).
- Both-mode screenshots per screen, a named focal element for each, and a closed finding list (T-187).
- Measured contrast for every used pair in both modes, TalkBack, 200 % font scale, reduced motion, hit areas (T-188).
- Loading, empty, error, partial and offline states per data-bearing screen, each produced on the device (T-189).
- Acceptance criterion A16 with linked evidence, plus a plain list of what is still not good (T-190).

## Open risks

- Contrast failures are usually fixed by moving text off a surface or dropping a type level. Both are forbidden: the fix is a token change (docs/14 §12).
- The Signalweg is the product's identity and also its most tempting decoration. If a review finds it moving without a request, or a lamp coloured without a health verdict, the finding outranks any visual improvement.
- The gate is mechanical. It cannot see flat hierarchy, monotone layout or a missing focal point — the four craft tests in docs/14 §11 are the only thing that catches those, and they require a human-readable screenshot, not a green check.
- Removing the design gate's rules to make a commit pass is the same class of violation as deleting a failing test (handbook §9).

## Evidence log

_No entries yet._
