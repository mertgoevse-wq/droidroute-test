# T-042 — Provider: TokenReply

> Phase 03 · Provider catalog · **Depends on:** T-027, T-031 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect TokenReply following the same evidence rule as TokenRouter.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | confirm base URL, auth header, model list |
| `testing` | fixture set for success and quota errors |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/tokenreply.json`
- Fixtures for its success and error shapes

## Steps

1. Read the provider's current documentation; do not reuse the URL from any other source.
2. Validate a key and record the model count.
3. Note any deviation from the OpenAI standard (extra required fields, different auth header).

## Acceptance criteria

- [ ] Only a confirmed base URL is committed
- [ ] A live validation ran or the blocker is logged
- [ ] Any non-standard requirement is captured as a manifest field, not as adapter special-case code

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-042 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-042 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-042: Provider: TokenReply"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

TokenReply is connected or explicitly blocked with a reason a later agent can act on.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-042.log`.
