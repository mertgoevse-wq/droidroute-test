# T-032 — Provider health probe and status surfacing

> Phase 02 · Provider framework · **Depends on:** T-031 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Give every provider a measurable health signal that routing and the dashboard can both use.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | define the signals that actually predict a good candidate |
| `kotlin-core` | rolling window implementation with bounded memory |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/HealthTracker.kt` — rolling success rate, p50/p95 latency, last error, consecutive failures
- Health exposure in `/v1/providers` and in the registry state flow

## Steps

1. Keep a bounded window per provider (and per key) so memory cannot grow without limit.
2. Ignore client-cancelled requests when computing success rate.
3. Decay old failures so a recovered provider is not punished forever.
4. Expose the numbers, not a colour: the UI decides how to present them.

## Acceptance criteria

- [ ] Health numbers update after a real request and are visible in `/v1/providers`
- [ ] The window is bounded (asserted by a test feeding more samples than the window)
- [ ] Cancelled requests do not lower the success rate

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*HealthTracker*'
curl -fsS http://127.0.0.1:8787/v1/providers
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-032 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-032 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-032: Provider health probe and status surfacing"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Health is measured, bounded and available to routing and UI alike.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-032.log`.
