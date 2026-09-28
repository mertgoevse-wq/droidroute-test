# T-048 — Provider: Cerebras

> Phase 03 · Provider catalog · **Depends on:** T-027, T-032 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect Cerebras's free tier and record its throughput characteristics.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | base URL, key handling, model list |
| `testing` | fixture coverage for its error shapes |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/cerebras.json` with base `https://api.cerebras.ai/v1`
- Recorded model list and rate-limit headers

## Steps

1. Validate a key and record the model list, noting any model-id naming that differs from upstream names.
2. Record the rate-limit headers and the documented free-tier window.
3. Measure time-to-first-byte and tokens/second for a short response.

## Acceptance criteria

- [ ] The provider validates and its models appear in the catalog
- [ ] Throughput numbers are recorded
- [ ] Model naming quirks are captured so aliases can map them later

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-048 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-048 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-048: Provider: Cerebras"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A high-throughput free provider is available to routing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-048.log`.
