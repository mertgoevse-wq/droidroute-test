# T-099 — Keys screen: masking, one-time reveal, clipboard

> Phase 07 · UI · **Depends on:** T-006, T-016, T-096 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Implement the key handling UX exactly as documented: masked by default, revealed once, device-credential protected on repeat reveal, clipboard auto-clear.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | the interaction details that make masking trustworthy |
| `security-audit` | FLAG_SECURE, clipboard timer, no key in a toast or snackbar |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/keys/KeysScreen.kt` with add, validate, mask, reveal, revoke
- Screenshot protection on this screen only

## Steps

1. Show `first5••••last5` and nothing more until an explicit reveal.
2. Require device-credential confirmation for a second reveal and log the action (not the value).
3. Copy to clipboard with a visible 60-second countdown and an immediate clear action.
4. Never place a key in a notification, a snackbar, or an intent extra.

## Acceptance criteria

- [ ] The masked form is the default on every entry to the screen
- [ ] A repeated reveal requires the device credential
- [ ] The clipboard is cleared after 60 seconds without requiring the app to stay open

## Verification

```bash
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-099 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-099 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-099: Keys screen: masking, one-time reveal, clipboard"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Key handling is safe to demonstrate to someone looking over your shoulder.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-099.log`.
