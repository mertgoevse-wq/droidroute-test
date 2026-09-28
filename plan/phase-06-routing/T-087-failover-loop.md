# T-087 — Failover loop and mid-stream policy

> Phase 06 · Routing · **Depends on:** T-084, T-086, T-068, T-071 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Walk the candidate list on failure, and define exactly what happens when a stream dies after the first byte.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | attempt bookkeeping and the mid-stream decision |
| `testing` | failure-injection tests for each failure point: before, during and after the first byte |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/FailoverExecutor.kt`
- Documented mid-stream policy: restart once on the next candidate, then surface an error naming all attempts

## Steps

1. Iterate candidates, skipping unusable ones, with retries only where the policy allows.
2. Before the first byte, failover is invisible to the client.
3. After the first byte, follow the documented policy and never present a truncated answer as complete.
4. Record every attempt in the response's `droidroute` object and in the log.

## Acceptance criteria

- [ ] A failure before the first byte transparently fails over (asserted)
- [ ] A mid-stream failure restarts once, then returns an error naming every attempt (asserted)
- [ ] The attempt list is present in the response for a failing chain

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*FailoverExecutor*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-087 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-087 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-087: Failover loop and mid-stream policy"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Failover is defined precisely, including the hard case, and is provable.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-087.log`.
