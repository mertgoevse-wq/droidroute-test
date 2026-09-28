# T-039 — Provider: APInex

> Phase 03 · Provider catalog · **Depends on:** T-027, T-031 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect the APInex gateway with daily-reset free model limits.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | confirm base URL and the daily limit semantics |
| `testing` | fixture plus rate-limit body handling |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/apinex.json` with `quota.window: daily` and tag `free`
- A fixture reproducing its daily-limit response so the router can park the key

## Steps

1. Read the provider's current documentation; do not reuse the URL from any other source. Confirm the base URL (documented as `https://apinex.bond/v1`).
2. Capture a real rate-limit response and turn it into a fixture for the error taxonomy.
3. Confirm whether the limit resets on a fixed clock or a rolling window and record it.

## Acceptance criteria

- [ ] The provider validates and lists models
- [ ] The limit response maps to `QuotaExceeded` in a test
- [ ] The recorded reset semantics match what the provider documents

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*apinex*'
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-039 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-039 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-039: Provider: APInex"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A daily-limited free gateway is connected and the router knows how to park it.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-039.log`.
