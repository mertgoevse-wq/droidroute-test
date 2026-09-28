# T-043 — Provider: FastRouter

> Phase 03 · Provider catalog · **Depends on:** T-027, T-031 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect FastRouter, a latency-oriented router front-end.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | confirm base URL and whether it proxies other gateways |
| `performance-android` | it claims low latency — measure it rather than repeat the claim |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/fastrouter.json`
- A latency measurement from a real call, recorded in the task log

## Steps

1. Read the provider's current documentation; do not reuse the URL from any other source.
2. Measure time-to-first-byte for a short prompt and store the number.
3. Confirm whether it needs any special header to select an upstream model family.

## Acceptance criteria

- [ ] The manifest uses only confirmed values
- [ ] A measured latency number exists (or the blocker is logged)
- [ ] No marketing claim from the provider is repeated in the docs as fact

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-043 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-043 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-043: Provider: FastRouter"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

FastRouter is connected with a measured latency figure, not an assumed one.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-043.log`.
