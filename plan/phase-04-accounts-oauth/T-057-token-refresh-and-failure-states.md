# T-057 — Token refresh scheduler and failure states

> Phase 04 · Accounts & OAuth · **Depends on:** T-055, T-056 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Refresh tokens before expiry, back off on failure, and surface `needs_attention` instead of failing requests mysteriously.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | scheduled refresh without wake-lock abuse; single-flight refresh per account |
| `testing` | expiry, refresh failure, revoked refresh token, clock skew |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/oauth/TokenRefresher.kt` with exponential backoff and jitter
- Account state enum: connected, expiring, refreshing, needs_attention(reason)

## Steps

1. Refresh 5 minutes before expiry and on any 401 from the provider.
2. Single-flight per account so ten parallel requests cause one refresh, not ten.
3. On `invalid_grant`, mark `needs_attention` and stop retrying until the owner re-authorises.
4. Log every refresh outcome with provider, account label and reason.

## Acceptance criteria

- [ ] An expiring token is refreshed without a failed request
- [ ] Concurrent requests trigger exactly one refresh (asserted by a test)
- [ ] A revoked refresh token results in `needs_attention`, not a retry storm

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*TokenRefresher*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-057 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-057 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-057: Token refresh scheduler and failure states"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Subscription accounts stay connected across restarts and degrade visibly, never silently.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-057.log`.
