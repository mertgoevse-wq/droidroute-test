# T-105 — First-run onboarding

> Phase 07 · UI · **Depends on:** T-096, T-099, T-102 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Take a fresh install to a working endpoint in under five minutes with an honest, short flow.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | a short flow that never lies about what it set up |
| `performance-android` | no blocking work on the main thread during setup |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/onboarding/OnboardingFlow.kt`: notification permission → port → connect a free provider → verify
- A final verification step that makes a real request and shows the result

## Steps

1. Ask for the notification permission with the reason stated in one sentence.
2. Default the port to 8787 and explain how to change it later.
3. Offer one-click connect for a free provider and allow skipping.
4. End with a real request whose output is shown; never claim success without it.

## Acceptance criteria

- [ ] A fresh install reaches a verified working endpoint through the flow
- [ ] Skipping the provider connect leaves the app in a clear, functional state
- [ ] The final step performs a real call, not a simulated one

## Verification

```bash
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-105 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-105 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-105: First-run onboarding"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A new install is productive in minutes and the app never overstates what it configured.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-105.log`.
