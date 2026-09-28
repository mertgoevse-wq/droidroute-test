# T-090 — Routing test suite with failure injection

> Phase 06 · Routing · **Depends on:** T-079, T-080, T-081, T-082, T-083, T-084, T-085, T-086, T-087, T-088, T-089 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Consolidate the phase's tests into a fault-injection suite that proves the chain behaves under every failure mode.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | fault injection matrix, determinism, no flaky timing assertions |
| `llm-routing` | identify the scenarios that matter and drop the ones that only look thorough |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `app/src/test/…/routing/` suite with a fake provider harness
- A scenario table documented in the suite header: quota, auth, timeout, mid-stream, hedging

## Steps

1. Build a fake provider that can be scripted to fail at a chosen point.
2. Cover: quota exhaustion mid-chain, auth revocation, timeout before first byte, failure after first byte, breaker flapping.
3. Ensure the suite is deterministic — no sleeps, use virtual time.
4. Run it in CI and record the timing.

## Acceptance criteria

- [ ] Every scenario in the table has a test
- [ ] The suite is deterministic across 20 consecutive runs
- [ ] No test depends on a real provider or the network

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*routing*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-090 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-090 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-090: Routing test suite with failure injection"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The routing engine's failure behaviour is proven, which is the point of the whole component.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-090.log`.
