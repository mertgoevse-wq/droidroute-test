# T-136 — Performance pass

> Phase 11 · Delivery · **Depends on:** T-109, T-094, T-106 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Measure and improve the three costs that matter on a phone: idle battery, memory ceiling and cold start.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `performance-android` | measure before changing anything; keep the before/after numbers |
| `kotlin-core` | reduce allocations and recompositions in the hot paths found |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A before/after measurement table recorded in status/components/core-server.md
- Fixes for the worst offenders, each with its own measurement

## Steps

1. Measure idle drain with one connected agent and no traffic over an hour.
2. Measure peak memory with a local model loaded and with a long stream in flight.
3. Measure cold start to a listening socket.
4. Fix the largest cost first and re-measure; do not batch unfocused changes.

## Acceptance criteria

- [ ] All three metrics are recorded with real numbers and the measurement method
- [ ] At least the largest measured cost is improved, with the delta stated
- [ ] No optimisation is claimed without a measurement

## Verification

```bash
adb shell dumpsys batterystats --charged com.droidroute.app | head -20
adb shell dumpsys meminfo com.droidroute.app | head -20
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-136 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-136 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-136: Performance pass"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Performance claims are numbers in the repository, not adjectives in a commit message.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-136.log`.
