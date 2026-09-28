# Component: routing

**Purpose:** turn "which provider should answer this" into a deterministic, explainable, quota-aware decision — with failover the owner can trust.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-079 … T-090 |
| Owns | `com.droidroute.routing` |
| Depends on | provider-layer, protocols |

## Deliverables

- Candidate resolution: `provider/model`, aliases, bare model names.
- Strategies: `free_first`, `fastest`, `cheapest`, `most_quota`, `healthiest`, `round_robin`, `priority`, `manual` — composable.
- Key pool with quota ledgers, parking on exhaustion, cooldowns after `429`, per-key and per-model pinning.
- **Multi-provider key chaining**: one logical model backed by keys from several different gateways, switching automatically when a quota runs dry (the owner's headline requirement).
- Health scoring, circuit breaker, retry/backoff, optional hedging.
- Failover loop with attempt recording, plus `/v1/routing/explain` for every decision.

## Open risks

- Quota windows are mostly unknown up front; the ledger must learn from `429` and rate-limit headers rather than trust a static number.
- Mid-stream failover can duplicate a partial answer — the default (restart once, then surface) must never look like a complete response.

## Evidence log

_No entries yet._
