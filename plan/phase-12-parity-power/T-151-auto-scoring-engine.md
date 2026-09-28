# T-151 — Multi-factor auto scoring engine

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-148, T-085, T-082 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Implement the live scoring engine behind the virtual `auto` models: weighted factors over health, quota, cost, latency, capability fit and session availability.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | factor weighting, normalisation and stability of the score |
| `android-profiler` | scoring must be cheap enough to run per request on a phone |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/auto/AutoScorer.kt` with an explicit, documented factor list and weights
- A per-request log line showing the factor contributions for the chosen candidate

## Steps

1. Define the factors and their weights in one place; the docs and code must agree in the same commit.
2. Normalise each factor into [0,1] and reject inputs that would divide by zero or exceed the range.
3. Cache the score briefly so a burst of requests does not recompute it per request.
4. Expose the factor breakdown through `/v1/routing/explain`, because an unexplainable score is a debugging trap.

## Acceptance criteria

- [ ] The score stays in range for boundary inputs (asserted)
- [ ] Each factor's contribution is visible in the explain output
- [ ] Scoring a candidate set of 50 costs under 5 ms (measured)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*AutoScorer*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-151 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-151 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-151: Multi-factor auto scoring engine"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The `auto` models make decisions that a human can inspect and argue with.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-151.log`.
