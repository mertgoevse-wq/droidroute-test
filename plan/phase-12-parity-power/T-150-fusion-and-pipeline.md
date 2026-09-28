# T-150 — Fusion and pipeline strategies

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-149 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Implement the two multi-model strategies: fusion (panel plus judge) and pipeline (each step feeds the next).

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | fan-out, cancellation and the judge protocol |
| `droidroute-verification` | cost assertions: exactly N calls for a panel of N, and cancellation on partial failure |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/strategy/Fusion.kt` and `Pipeline.kt`
- Usage accounting that records every panel member's cost separately

## Steps

1. Fan out to the panel with a shared deadline; cancel stragglers rather than waiting indefinitely.
2. Send the panel answers to a judge model with an explicit, documented prompt contract.
3. For pipeline, pass each step's output as the next step's input and record intermediate artefacts in the log.
4. Make both strategies refuse to run silently expensive combinations without an explicit opt-in.

## Acceptance criteria

- [ ] Fusion calls exactly the panel size plus one judge (asserted by call counting)
- [ ] A failed panel member does not fail the whole fusion request unless all fail
- [ ] Pipeline passes output forward correctly, and every step's usage is recorded

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Fusion*' --tests '*Pipeline*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-150 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-150 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-150: Fusion and pipeline strategies"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Multi-model routing is available with explicit cost accounting.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-150.log`.
