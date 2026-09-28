# T-182 — Debug capture mode (redacted, time-bounded)

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-017, T-104 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

A troubleshooting mode that records full request and response payloads — redacted, bounded, auto-expiring — so a broken provider can be diagnosed without guesswork.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-verification` | redaction canary on captured payloads and an expiry test |
| `android-intent-security` | capture is the most sensitive data the app holds; bound it in time and scope |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `logging/DebugCapture.kt` with a maximum capture window, a byte ceiling and automatic expiry
- A capture viewer with export, sharing the redactor with the log pipeline

## Steps

1. Capture only after an explicit enable, with a visible countdown in the notification.
2. Apply the redactor to every captured field and record the redaction counts per payload.
3. Enforce a byte ceiling and a time ceiling; delete automatically when either is reached.
4. Make exported captures pass the secrets preflight before leaving the app.

## Acceptance criteria

- [ ] Capture is off by default and expires automatically (asserted)
- [ ] A canary key in a captured payload is redacted (asserted)
- [ ] An exported capture passes `scripts/preflight-secrets.sh`

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*DebugCapture*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-182 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-182 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-182: Debug capture mode (redacted, time-bounded)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Diagnosing a misbehaving provider does not require guessing or leaking credentials.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-182.log`.
