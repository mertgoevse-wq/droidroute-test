# T-056 — Google account (AI Pro / Gemini)

> Phase 04 · Accounts & OAuth · **Depends on:** T-055, T-049 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Connect the owner's Google AI Pro account through OAuth so Gemini models are usable under the subscription.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `oauth-device-flow` | Google OAuth specifics: scopes, consent screen, refresh semantics |
| `provider-integration` | which endpoint the subscription actually grants access to |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/google-account.json` with `auth.type: oauth-google`
- Setup doc `docs/accounts/google.md` covering client id creation and consent-screen configuration

## Steps

1. Determine from Google's current documentation which API surface the subscription grants, and record it.
2. Request the minimum scopes needed for that surface.
3. Complete the flow, then make one real call and record which models answered.
4. Document clearly what the subscription does and does not unlock for programmatic use.

## Acceptance criteria

- [ ] A real call succeeds through the OAuth account, or the limitation is documented with evidence
- [ ] Requested scopes are the minimum needed
- [ ] The setup doc lists every step the owner must perform in the Google console

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*google*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-056 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-056 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-056: Google account (AI Pro / Gemini)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The Google subscription is connected where it can be, and the limits are documented where it cannot.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-056.log`.
