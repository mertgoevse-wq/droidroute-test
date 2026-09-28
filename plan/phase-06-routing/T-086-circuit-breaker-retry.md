# T-086 — Circuit breaker and retry policy

> Phase 06 · Routing · **Depends on:** T-085 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Open a provider after repeated failures, half-open it with a probe, and retry with bounded exponential backoff.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | breaker states and transitions without flapping |
| `testing` | state machine tests including the half-open probe |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/CircuitBreaker.kt` (closed, open, half-open)
- Retry policy with jitter, bounded attempts, and no retry on quota or auth errors

## Steps

1. Open after the configured consecutive failures; record the reason and time.
2. Half-open with one probe after the cooldown; close on success, reopen on failure with a longer cooldown.
3. Never retry the same key after a quota error; retry transient network errors with jitter.
4. Expose breaker state in `/v1/providers`.

## Acceptance criteria

- [ ] A failing provider is skipped after the threshold, without a request to it (asserted by call counting)
- [ ] A recovered provider is used again after the probe succeeds
- [ ] No retry happens after `QuotaExceeded` or `AuthError` (asserted)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*CircuitBreaker*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-086 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-086 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-086: Circuit breaker and retry policy"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Broken providers stop costing latency and quota.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-086.log`.
