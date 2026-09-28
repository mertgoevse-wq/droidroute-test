# T-063 — Account state model and `needs_attention` surfacing

> Phase 04 · Accounts & OAuth · **Depends on:** T-057, T-058, T-059 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Give the UI everything it needs to show account health without exposing tokens: state, expiry, scopes, last error.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | state model without token leakage; expiry formatting |
| `android-compose-ui` | the shape the account screen needs, defined before the screen is built |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/oauth/AccountState.kt` and its exposure through `/v1/providers`
- Account list data source for the UI (no secrets)

## Steps

1. Model per account: provider id, label, state, expiry, scopes, last refresh result.
2. Expose it through the existing provider endpoint rather than a new one.
3. Add a test asserting the serialised account contains no token-shaped value.

## Acceptance criteria

- [ ] Accounts appear with their real state in `/v1/providers`
- [ ] An expiring account is visible before it fails
- [ ] No token material is present in the API response (canary test)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*AccountState*'
curl -fsS http://127.0.0.1:8787/v1/providers | grep -c token
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-063 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-063 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-063: Account state model and `needs_attention` surfacing"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Account health is visible and safe to display.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-063.log`.
