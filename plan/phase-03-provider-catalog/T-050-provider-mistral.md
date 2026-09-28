# T-050 — Provider: Mistral

> Phase 03 · Provider catalog · **Depends on:** T-027, T-029 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect Mistral's API including its free experimental tier.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | free-tier model naming and rate limits |
| `testing` | discovery fixture and one live validation |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/mistral.json` with base `https://api.mistral.ai/v1`
- Free-tier models tagged so `free_first` can prefer them

## Steps

1. Validate a key and record the model list.
2. Tag the free-tier models from the documented naming.
3. Record the rate-limit headers and window.

## Acceptance criteria

- [ ] The provider validates and its models appear
- [ ] Free-tier models are tagged without hard-coding ids that could change
- [ ] Rate-limit header names are recorded

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-050 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-050 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-050: Provider: Mistral"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Mistral is connected with its free tier preferred by the free-first strategy.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-050.log`.
