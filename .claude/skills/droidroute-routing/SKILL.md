---
name: droidroute-routing
description: Work on DroidRoute's routing engine - candidate resolution, strategies, quota ledgers, multi-provider key chaining, circuit breaking and failover. Use for plan/phase-06 tasks, or when the user mentions failover, key rotation, quotas, routing strategies, combos or "why did it pick that provider".
---

# Routing work

## Read the contract first

- `docs/04-routing.md` — the documented behaviour (strategies, health score formula, failover loop).
- `docs/12-omniroute-parity.md` — the feature parity target, including the strategy list OmniRoute calls its own.
- The task file — its acceptance criteria are the contract.

If implementation and documentation disagree, fix both in the same commit. A documented behaviour that the code does not have is a bug in whichever is cheaper to change.

## Core invariants

1. **Resolution is pure.** `CandidateResolver` has no side effects, so it is trivially testable.
2. **Parked, never deleted.** An exhausted key gets a `reset_at` and a reason; it comes back when the window resets.
3. **No retry after `QuotaExceeded` or `AuthError`** on the same key. Retry is for transient failures, with jitter and a bound.
4. **Failover before the first byte is invisible; after it, it follows the documented mid-stream policy** — restart once, then surface an error naming every attempt. Never present a truncated answer as complete.
5. **Every decision is explainable** through `/v1/routing/explain` and a structured log record carrying the `request_id`.
6. **Key chains may span different providers** — that is the owner's headline requirement, not an edge case.

## Testing shape

Use the fake-provider harness: script it to fail at a chosen point (before first byte, mid-stream, after completion), then assert the chain's behaviour and the recorded attempts. Deterministic tests only — no sleeps, use virtual time.

```bash
./gradlew :app:testDebugUnitTest --tests '*routing*'
```

## Cost and quota discipline

Routing decisions spend real quota. When adding a candidate to a path, ask whether the request could have been served by a cheaper or free candidate, and whether the choice is visible in `/v1/usage`.
