# T-095 — Daily and weekly usage views

> Phase 07 · UI · **Depends on:** T-094, T-081 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Show token consumption and estimated cost per provider for today and the last seven days.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | simple, readable charts without a heavy charting dependency |
| `kotlin-core` | aggregation queries and caching that stay cheap on a phone |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/dashboard/UsageSection.kt` with a 7-day view and a per-provider breakdown
- Cost shown as estimated, explicitly labelled when prices are unknown

## Steps

1. Aggregate from the usage table with a bounded query (indexed by timestamp).
2. Show free providers with an explicit '0 (free)' rather than hiding them.
3. Mark estimates as estimates; never present a guess as a measurement.
4. Add a test comparing the aggregate with a hand-computed fixture.

## Acceptance criteria

- [ ] The aggregate matches a fixture dataset exactly
- [ ] Unknown pricing is labelled, not filled with a fabricated number
- [ ] The query stays under 50 ms for a month of records (measured)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*UsageAggregat*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-095 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-095 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-095: Daily and weekly usage views"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Consumption is visible per provider and day, with costs labelled honestly.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-095.log`.
