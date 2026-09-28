# T-059 — HuggingFace account

> Phase 04 · Accounts & OAuth · **Depends on:** T-055 · **Parallel-safe:** yes · **Est. agent time:** 45-90 min

## Goal

Connect HuggingFace via OAuth so hosted inference models are available under the owner's account.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `oauth-device-flow` | HuggingFace OAuth endpoints and token handling |
| `provider-integration` | which inference endpoint the account grants |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/huggingface-account.json` with `auth.type: oauth-hf`
- Setup doc with the OAuth app configuration

## Steps

1. Implement the flow using the documented endpoints and scopes.
2. Validate with a call to the inference surface and record which models responded.
3. Record whether the account also unlocks dataset or repo scopes that DroidRoute does not need.

## Acceptance criteria

- [ ] The flow completes and a live inference call succeeds, or the blocker is logged
- [ ] Only inference-related scopes are requested
- [ ] The account appears in the UI as its own entity, distinct from a pasted HF token

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*huggingface*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-059 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-059 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-059: HuggingFace account"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

HuggingFace models are reachable under the owner's own account.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-059.log`.
