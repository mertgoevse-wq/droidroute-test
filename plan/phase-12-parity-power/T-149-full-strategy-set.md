# T-149 — Complete the 19-strategy set

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-148 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Add the strategies not covered by T-084 — fill-first, weighted, p2c, least-used, random, strict-random, reset-window, reset-aware, context-relay, context-optimized, cache-optimized — and document every one.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | comparators over the candidate view; keep them pure and composable |
| `droidroute-verification` | deterministic expectation per strategy, including ties and single-candidate cases |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/strategy/` completed to 19 strategies
- `docs/04-routing.md` table matching the code exactly

## Steps

1. Implement each remaining strategy as a pure comparator over quota, latency, cost, health, reset time and context fit.
2. For randomised ones (random, strict-random, p2c, weighted), seed the generator so tests are deterministic.
3. Implement context-relay honestly: it hands off context, so state clearly what is preserved across the handoff.
4. Extend the strategy tests to cover all 19 with ties and a single candidate.

## Acceptance criteria

- [ ] All 19 strategies exist, each with a deterministic test
- [ ] `docs/04-routing.md` lists exactly the implemented set (checked by a test or the doc table)
- [ ] Randomised strategies are reproducible under a fixed seed

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Strategy*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-149 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-149 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-149: Complete the 19-strategy set"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Strategy parity with OmniRoute is complete and documented, not approximated.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-149.log`.
