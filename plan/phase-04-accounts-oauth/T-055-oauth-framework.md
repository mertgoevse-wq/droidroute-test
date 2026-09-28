# T-055 — OAuth framework (PKCE, browser intent, redirect)

> Phase 04 · Accounts & OAuth · **Depends on:** T-006, T-030 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Build the shared OAuth machinery once: authorization-code with PKCE, a Custom Tab / browser intent, a loopback or custom-scheme redirect, and vault-backed token storage.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `oauth-device-flow` | PKCE, state parameter, redirect handling on Android |
| `security-audit` | no token in logs, no implicit flow, state verified on every callback |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/oauth/OAuthEngine.kt` — start(providerId), handleCallback(uri), refresh(accountId)
- Token storage via the vault: access token, refresh token, expiry, scopes

## Steps

1. Implement PKCE with S256 and a random state that is verified on return.
2. Open the authorization URL in a Custom Tab; accept the callback through a claimed intent filter.
3. Store tokens in the vault and expose only account metadata (scopes, expiry) elsewhere.
4. Collect a per-provider client id/secret from settings — never ship one in the repo.

## Acceptance criteria

- [ ] A mock provider completes the full flow and the token lands in the vault
- [ ] A callback with a wrong state parameter is rejected and logged
- [ ] No token value appears in any log line (canary test)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*OAuthEngine*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-055 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-055 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-055: OAuth framework (PKCE, browser intent, redirect)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

One OAuth implementation serves every account provider; adding one is configuration.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-055.log`.
