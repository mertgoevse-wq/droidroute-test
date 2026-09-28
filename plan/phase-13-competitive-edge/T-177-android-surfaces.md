# T-177 — Quick Settings tile, widget, share sheet and text-selection action

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-105, T-091 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Make DroidRoute reachable in one gesture: toggle from Quick Settings, see today's usage on the home screen, and send selected text or a shared image to the local model.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | widget and tile are separate UI systems; keep them thin |
| `performance-android` | a widget must not poll; update on events only |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Quick Settings tile starting/stopping the server, reflecting real state
- Home-screen widget: server state, today's tokens, parked keys count
- Share-sheet target and text-selection action that route through the local model first

## Steps

1. Implement the tile and widget over the existing service state, with no logic of their own.
2. Handle the share intent for text and images, preferring a local model and falling back per policy.
3. Update the widget on state changes only, never on a timer.
4. Test each surface on the device and record screenshots as evidence.

## Acceptance criteria

- [ ] The tile reflects the real service state within a second of a change
- [ ] A shared text or image gets an answer without opening the app
- [ ] The widget produces no periodic wakeups (verified with battery stats over an hour)

## Verification

```bash
./gradlew :app:assembleDebug
adb shell dumpsys batterystats --charged com.droidroute.app | head -20
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-177 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-177 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-177: Quick Settings tile, widget, share sheet and text-selection action"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

DroidRoute behaves like a phone app, not a service you visit.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-177.log`.
