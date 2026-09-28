# T-171 — Subscription login adapters and multi-account pools

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-057, T-081, T-030 · **Parallel-safe:** yes · **Est. agent time:** 180-300 min

## Goal

Connect CLI-subscription identities (Claude Code, Codex, GitHub Copilot, Cursor, Antigravity-style) and hold several accounts per provider, rotating them with the same quota ledger used for API keys.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `oauth-device-flow` | each tool's real login flow, token storage and refresh semantics |
| `ai-governors` | using a subscription programmatically has terms — surface them, never hide them |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/accounts/SubscriptionAdapter.kt` with a per-tool login flow
- Multi-account pools: several accounts per provider, selected by the quota ledger and health score

## Steps

1. Implement one flow at a time, validating against the tool's own current documentation.
2. Store every account's tokens in the vault, keyed by account label, never in a shared blob.
3. Extend the key pool to accounts so rotation and parking work identically for both.
4. State plainly, in the UI and the docs, what each subscription permits programmatically.

## Acceptance criteria

- [ ] Each implemented adapter completes a login and answers a request, or is documented as not feasible with the reason
- [ ] Two accounts on one provider rotate by quota (asserted)
- [ ] The terms note exists per adapter and is shown before the first login

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*SubscriptionAdapter*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-171 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-171 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-171: Subscription login adapters and multi-account pools"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Subscription-based routing — what 9Router, CLIProxyAPI and dario are built around — works natively.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-171.log`.
