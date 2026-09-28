# T-041 — Provider: TokenRouter

> Phase 03 · Provider catalog · **Depends on:** T-027, T-031 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect TokenRouter as a credit gateway with discovery-first model handling.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | confirm base URL and credit-account semantics |
| `testing` | discovery fixture and an insufficient-credit error fixture |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/tokenrouter.json`
- Fixture for its insufficient-credit response (maps to `QuotaExceeded`)

## Steps

1. Read the provider's current documentation; do not reuse the URL from any other source. The base URL is not public knowledge — do not guess it; leave the task blocked and logged if it cannot be confirmed.
2. Add the credit-exhausted response to the taxonomy fixtures.
3. Record how credits are displayed so the dashboard can show remaining balance when the provider exposes it.

## Acceptance criteria

- [ ] The manifest uses only a confirmed base URL
- [ ] Credit exhaustion parks the key instead of marking it invalid
- [ ] Any uncertainty about the provider's API is recorded in the task log, not papered over

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-041 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-041 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-041: Provider: TokenRouter"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

TokenRouter is either working with confirmed details, or explicitly blocked with evidence.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-041.log`.
