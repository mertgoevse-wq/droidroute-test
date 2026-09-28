# T-082 — Quota learning from `429` and rate-limit headers

> Phase 06 · Routing · **Depends on:** T-081, T-077 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Learn windows the manifests do not know, from real responses, without ever trusting a guess over evidence.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | which headers and bodies reliably indicate a limit and a reset |
| `testing` | fixtures for three providers' limit dialects |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/QuotaLearner.kt` updating the ledger from responses
- Fixtures covering `Retry-After`, `x-ratelimit-*` and body-only limit signals

## Steps

1. Prefer explicit reset timestamps, then relative retry hints, then a conservative default.
2. Record the evidence that produced each learned value so the dashboard can show where it came from.
3. Never lower a known limit because a provider was lenient once.
4. Test with fixtures from at least three different dialects.

## Acceptance criteria

- [ ] A `429` with `Retry-After` parks the key for that duration and records the evidence
- [ ] A `429` without headers parks for a conservative default and marks the value as estimated
- [ ] Learned values persist and are visible in `/v1/usage`

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*QuotaLearner*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-082 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-082 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-082: Quota learning from `429` and rate-limit headers"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The ledger improves from experience and shows its sources.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-082.log`.
