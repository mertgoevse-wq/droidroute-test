# T-156 — Quota-Share across pooled keys

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-081, T-083 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Split one shared account's quota fairly across pooled keys, work-conserving, so idle slices are lent out instead of wasted.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | fair-share scheduling with lending, and the guarantee that lending never strands a slice |
| `droidroute-verification` | fairness assertions under skew: one heavy consumer, several light ones, all bounded |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/QuotaShare.kt` with a documented lending rule
- Explain output showing each key's slice, usage and lent amount

## Steps

1. Define slices per key over the shared window and track usage against the slice, not only the account total.
2. Lend unused slice capacity to the key that needs it, and reclaim it when the owner returns.
3. Never exceed the account's real limit while lending — the shared cap is a hard ceiling.
4. Test a skewed load and assert that no key is starved and no window is overspent.

## Acceptance criteria

- [ ] Skewed load does not starve any key (asserted)
- [ ] The shared account cap is never exceeded (asserted)
- [ ] The lending state is visible per key

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*QuotaShare*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-156 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-156 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-156: Quota-Share across pooled keys"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Shared accounts are used efficiently without one consumer eating the pool.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-156.log`.
