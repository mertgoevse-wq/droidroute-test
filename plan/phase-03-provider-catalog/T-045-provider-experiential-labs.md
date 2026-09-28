# T-045 — Provider: Experiential Labs

> Phase 03 · Provider catalog · **Depends on:** T-027, T-031 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Connect Experiential Labs, including its ability to front the owner's own keys or a local model.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | confirm the API surface and the bring-your-own-key behaviour |
| `technical-writing` | document the two ways to use it (their keys vs the owner's keys) |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/experiential.json` with base `https://api.experientiallabs.ai/v1` confirmed
- Documentation of the bring-your-own-key mode and how it interacts with DroidRoute's own keys

## Steps

1. Read the provider's current documentation; do not reuse the URL from any other source.
2. Test a plain call and, if the mode exists, a call through a key DroidRoute itself stores.
3. Record whether its response includes trace or simulation identifiers worth surfacing.

## Acceptance criteria

- [ ] A live call succeeds or the blocker is logged
- [ ] The bring-your-own-key interaction is documented without ambiguity about who holds the secret
- [ ] No assumed field name is parsed without a fixture proving it

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-045 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-045 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-045: Provider: Experiential Labs"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Experiential Labs is connected and its key-ownership model is documented honestly.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-045.log`.
