# T-084 — Routing strategies

> Phase 06 · Routing · **Depends on:** T-079, T-081, T-032 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Implement the eight documented strategies and allow them to be composed.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | ordering rules as pure comparators, composable without ambiguity |
| `testing` | one test per strategy plus a composition test |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/strategy/` — free_first, fastest, cheapest, most_quota, healthiest, round_robin, priority, manual
- Composition mechanism so a chain of comparators is expressible as data

## Steps

1. Implement each strategy as a comparator over a candidate view (quota, latency, cost, health, tier).
2. Make composition explicit and ordered; document that the first comparator wins ties.
3. Default for Tier 1 to `free_first → most_quota → fastest`.
4. Test each strategy with synthetic candidate sets, including ties.

## Acceptance criteria

- [ ] Every strategy has a passing test with a deterministic expectation
- [ ] A composed chain resolves ties by the documented rule
- [ ] Changing the strategy changes ordering without restarting the server

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Strategy*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-084 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-084 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-084: Routing strategies"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Routing behaviour is owner-selectable and each option is proven.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-084.log`.
