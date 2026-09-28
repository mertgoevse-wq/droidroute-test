# T-044 — Provider: xKiro

> Phase 03 · Provider catalog · **Depends on:** T-027, T-031 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect xKiro, the 'every leading model, one API key' gateway, and validate its model breadth.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | confirm base URL and auth from the provider's own docs |
| `testing` | discovery fixture and one live validation |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/xkiro.json` with `tier: 1`, tag `credits`
- Recorded model count and confirmed base URL in the task log

## Steps

1. Read the provider's current documentation; do not reuse the URL from any other source.
2. Validate a key, record the model count and any model-id naming quirks.
3. Note whether the provider reports usage for cost accounting.

## Acceptance criteria

- [ ] The provider validates and lists models, or the blocker is logged
- [ ] Base URL and auth header are confirmed, not assumed
- [ ] Usage reporting availability is recorded

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-044 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-044 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-044: Provider: xKiro"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

xKiro is available to routing with confirmed connection details.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-044.log`.
