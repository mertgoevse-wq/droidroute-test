# T-047 — Provider: Groq

> Phase 03 · Provider catalog · **Depends on:** T-027, T-032 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect Groq's free tier, which is the strongest candidate for the `fastest` strategy.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | free-tier limits and the correct base URL |
| `performance-android` | measure the actual latency advantage instead of assuming it |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/groq.json` with base `https://api.groq.com/openai/v1`
- A latency measurement recorded for comparison with other providers

## Steps

1. Validate a key and record the model list.
2. Measure time-to-first-byte for a short streaming prompt.
3. Record its rate-limit headers so the quota ledger can learn the window.

## Acceptance criteria

- [ ] A live validation succeeds or the blocker is logged
- [ ] Latency is recorded as a number
- [ ] Rate-limit header names are recorded for the ledger task

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-047 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-047 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-047: Provider: Groq"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A low-latency provider is connected with evidence for the `fastest` strategy.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-047.log`.
