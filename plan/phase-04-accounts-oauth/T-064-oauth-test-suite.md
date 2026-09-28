# T-064 — OAuth test suite with a mock provider

> Phase 04 · Accounts & OAuth · **Depends on:** T-055, T-056, T-057, T-058, T-059, T-062 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Test the whole OAuth path offline against a mock authorization server, including the failure cases that are painful to reproduce live.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | mock authorization server, token expiry, refresh failure, state mismatch |
| `security-audit` | assert the dangerous cases are rejected, not merely untested |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `app/src/test/…/oauth/` suite with a local mock server
- Documented coverage list inside the test file header

## Steps

1. Stand up an embedded mock server implementing the authorization-code exchange.
2. Test: happy path, wrong state, expired code, refresh success, refresh `invalid_grant`, clock skew.
3. Assert that no test writes a token to the log or the database in plaintext.
4. Keep the suite offline and fast.

## Acceptance criteria

- [ ] All OAuth failure modes are covered and asserted
- [ ] The suite runs offline in under 30 seconds
- [ ] The token-canary assertion is present and passes

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*oauth*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-064 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-064 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-064: OAuth test suite with a mock provider"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

OAuth is provable without touching a real account.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-064.log`.
