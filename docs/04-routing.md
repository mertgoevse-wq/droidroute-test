# Routing & Failover

The router turns a request for a model into an ordered list of candidates `(provider, key, model)` and walks that list until one succeeds.

## Candidate resolution

```
request.model
   │
   ├─ "provider/model"  ──────────────▶ exact candidate
   ├─ alias hit         ──────────────▶ owner-defined candidate list
   └─ bare model name   ──────────────▶ every enabled provider offering it,
                                        ordered by the active strategy
```

`GET /v1/routing/explain?model=…` returns the exact list, the strategy used, and *why* each candidate sits where it does. This is the debugging tool — when routing surprises you, it should never be guesswork.

## Strategies (owner-selectable, per model or global)

| Strategy | Ordering rule | Good for |
|---|---|---|
| `free_first` | tier 1 before tier 2 before tier 3; within a tier, most remaining quota first | everyday work, keeps paid credit untouched |
| `fastest` | lowest rolling p50 latency over the last N requests | interactive coding |
| `cheapest` | lowest known/estimated cost per 1k tokens; free counts as 0 | bulk work |
| `most_quota` | largest remaining today's quota relative to window | avoiding mid-task `429`s |
| `priority` | owner-defined explicit order per model | precise control |
| `healthiest` | highest composite health score (success rate, latency, quota) | unattended long runs |
| `round_robin` | rotate evenly across equal-ranked candidates | spreading load across keys |
| `manual` | never failover; the named provider or nothing | benchmarks, A/B tests |

Strategies compose: `free_first` then `most_quota` then `fastest` is a valid chain and the default for Tier 1.

## Health score

Per `(provider, key)` pair, over a sliding window (default 200 requests / 24 h):

```
score = 0.5·success_rate + 0.3·(1 − latency_norm) + 0.2·quota_remaining_norm
```

- `success_rate` ignores client-side cancellations.
- `latency_norm` is `min(p50 / 5000 ms, 1)`.
- A `429` or `5xx` applies an immediate exponential penalty that decays over 10 minutes.
- Scores are persisted so a restart does not forget a bad provider.

## Key pool and quota rotation

The heart of the owner's requirement: *when one quota is used up, the next key switches in automatically.*

- Keys are grouped per provider; each key has its own quota ledger with a window (`daily` = resets at local midnight, `hourly`, `monthly`, or `unknown`).
- Known windows come from the manifest (`quota.hint_tokens`); unknown ones are learned from `429` responses and `x-ratelimit-*` headers.
- A key that hits its limit is **parked** with `reset_at`, never deleted. The UI shows `parked until 00:00`.
- Selection inside a provider: highest remaining quota, then lowest latency, then oldest last-use (so all keys get exercised).
- A key can also be pinned for a model (`this model must use key K`) or excluded for a model.
- Keys can come from **different providers** — the pool is *not* scoped to one vendor, which is exactly how the owner wants to chain e.g. three free gateways behind one logical model.

## Failover loop

```
for candidate in resolved_list:
    if not candidate.is_usable(): continue      # parked key, open circuit breaker
    try:
        stream = candidate.call(request)
        on_first_byte: return stream            # success, stop searching
    except QuotaExceeded:  park_key(); continue
    except AuthError:      mark_key_invalid(); continue
    except Timeout:        penalise(candidate); continue
    except ServerError:    penalise(candidate); continue
raise NoProviderAvailable(attempts)
```

- Retries per candidate: configurable (default 1) with exponential backoff + jitter; quota errors never retry on the same key.
- **Mid-stream failure:** configurable. Default = restart the completion once on the next candidate; if that also fails, surface an error that names every attempt. Never silently return a truncated answer.
- **Circuit breaker:** after N consecutive failures a provider is opened for a cooldown (default 3 failures / 60 s), then half-opened with a single probe request.
- **Hedging (opt-in):** if the first candidate has not produced a first byte within X ms, a second candidate is started in parallel; the loser is cancelled. Off by default — it spends quota twice.

## Cost and quota awareness

- Manifests carry optional pricing (`cost_in`, `cost_out` per 1M tokens). Usage records store tokens × price → the dashboard can show spend per provider and per day.
- Free providers are recorded with cost `0` so "what would this have cost" is always answerable.
- A monthly budget cap per provider (optional) hard-stops a provider when exceeded, regardless of strategy.

## Model aliases

```json
{
  "my-best": { "candidates": ["bynara/qwen-3.8-max-free", "experiential/gpt-6-astra", "openai/gpt-4o"], "strategy": "free_first" },
  "fast-small": { "candidates": ["groq/llama-3.3-70b", "local/llamacpp/llama-3-3b"], "strategy": "fastest" }
}
```

Aliases are owner-editable in the UI and stored in the database (not in the repo). DroidRoute's own internal calls (e.g. summarising a log) use fixed aliases so they never steal the owner's best model by accident — unless the owner opts in.

## Observability

- Every routing decision is one structured log record: candidates considered, chosen, attempt outcome, latency, tokens, cost, `request_id`.
- `status/DECISIONS.md` in the repository records *routing design* decisions (not runtime data), so a future agent understands why the default order is what it is.
- The dashboard shows live: active providers, parked keys with reset times, today's tokens per provider, error rate, p50/p95 latency.
