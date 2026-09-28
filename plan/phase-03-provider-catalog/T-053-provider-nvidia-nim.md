# T-053 — Provider: NVIDIA NIM

> Phase 03 · Provider catalog · **Depends on:** T-027, T-032 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect NVIDIA NIM and record its credit model so the dashboard can show remaining balance where exposed.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | base URL, auth, model list |
| `testing` | fixture for the credit-exhausted path |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/nvidia-nim.json` with base `https://integrate.api.nvidia.com/v1`
- Credit-state handling if the API exposes it

## Steps

1. Validate a key and record the model list.
2. Check whether remaining credits are queryable; if yes, wire that into the provider status.
3. Add the exhausted path to the router's quota fixtures.

## Acceptance criteria

- [ ] The provider validates and its models appear
- [ ] Credit state is either surfaced from real data or explicitly marked unavailable
- [ ] The exhausted path is covered by a test

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-053 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-053 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-053: Provider: NVIDIA NIM"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A credit-based provider is connected with honest balance reporting.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-053.log`.
