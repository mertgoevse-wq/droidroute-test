# T-081 — Key pool and quota ledger

> Phase 06 · Routing · **Depends on:** T-030, T-032 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Track per-key quota windows, park exhausted keys with a reset time, and select keys by remaining quota then latency.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | ledger semantics: windows, unknown windows, reset detection |
| `testing` | window mathematics and parking/resume tests |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/QuotaLedger.kt` (daily, hourly, monthly, unknown windows)
- `routing/KeySelector.kt` with the documented ordering rule

## Steps

1. Model a window as `{type, start, limit, used, reset_at}`; treat `unknown` as learn-on-the-fly.
2. Park rather than delete an exhausted key; a parked key is skipped and shown with its reset time.
3. Order selection by remaining quota, then latency, then oldest last-use.
4. Persist the ledger so a restart does not forget today's consumption.

## Acceptance criteria

- [ ] An exhausted key is parked with a reset time and skipped by selection (asserted)
- [ ] After the window resets the key becomes selectable again without a restart
- [ ] Ledger state survives a restart (asserted with a reload test)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*QuotaLedger*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-081 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-081 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-081: Key pool and quota ledger"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Quotas are tracked rather than discovered by failure.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-081.log`.
