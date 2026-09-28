# T-085 — Health scoring and persistence

> Phase 06 · Routing · **Depends on:** T-032, T-081 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Compute the composite health score documented in docs/04-routing.md and persist it across restarts.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | weighting, decay and normalisation that behave sensibly at the extremes |
| `testing` | boundary tests: all success, all failure, one slow outlier |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/HealthScore.kt` with the documented weights
- Persisted scores with a decay policy on load

## Steps

1. Implement the score exactly as documented or update the doc in the same commit — never both drift.
2. Decay stale penalties so a recovered provider is not permanently punished.
3. Test the extreme cases so the score cannot exceed its range or divide by zero.
4. Expose the score components, not only the aggregate.

## Acceptance criteria

- [ ] Score stays within [0,1] for the boundary inputs (asserted)
- [ ] A provider recovering after failures returns to a competitive score within the documented decay period
- [ ] The implementation and docs/04-routing.md agree

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*HealthScore*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-085 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-085 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-085: Health scoring and persistence"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Health is a single, documented number that routing and the dashboard both trust.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-085.log`.
