# T-139 — Test suite consolidation and coverage review

> Phase 11 · Delivery · **Depends on:** T-136, T-138 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

One coherent suite: fast unit tests, meaningful instrumented tests, no redundant or flaky ones.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | remove duplicates, fix flakiness, keep runtime honest |
| `technical-writing` | document what is tested and, more usefully, what is not |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A consolidated suite with recorded runtime
- A coverage note stating known gaps in plain terms

## Steps

1. Run the full suite repeatedly to surface flakiness; fix or delete flaky tests rather than retrying.
2. Remove tests whose assertions could not fail.
3. Record the run time and the intentional gaps.
4. Make sure CI runs the same suite the developer runs locally.

## Acceptance criteria

- [ ] The full suite passes ten consecutive runs
- [ ] Runtime is recorded and reasonable for CI
- [ ] Gaps are documented honestly

## Verification

```bash
./gradlew :app:testDebugUnitTest --rerun-tasks
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-139 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-139 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-139: Test suite consolidation and coverage review"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The suite is trustworthy, which means a failure now means something.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-139.log`.
