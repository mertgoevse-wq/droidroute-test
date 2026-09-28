# T-007 — Foreground service skeleton

> Phase 00 · Foundation · **Depends on:** T-003 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Create the service that will host the server: startForeground with the dataSync type, a persistent notification, START_STICKY, and a clean stop path — with no server logic yet.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-platform` | service type declaration, notification channel, START_STICKY semantics |
| `testing` | instrumented check that the service starts, notifies and stops |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/DroidRouteService.kt` with start/stop/state callbacks
- Notification channel + ongoing notification showing port, bind mode and request count placeholders
- `POST_NOTIFICATIONS` runtime permission request on first start

## Steps

1. Declare the service in the manifest with `foregroundServiceType="dataSync"`.
2. Create the notification channel and an ongoing, low-importance notification.
3. Implement START_STICKY with an explicit stop action in the notification.
4. Expose a `StateFlow<ServiceState>` for the UI to observe.

## Acceptance criteria

- [ ] Starting the service from a debug action keeps it alive with the screen off for at least 10 minutes
- [ ] Stopping it removes the notification and releases resources
- [ ] No `IllegalStateException` about foreground service types on Android 14+

## Verification

```bash
./gradlew :app:assembleDebug
adb shell dumpsys activity services com.droidroute.app | head -40
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-007 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-007 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-007: Foreground service skeleton"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A correctly typed foreground service exists; the server can be mounted into it by the next phase.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-007.log`.
