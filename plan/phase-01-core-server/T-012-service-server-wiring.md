# T-012 — Service ↔ server wiring and lifecycle states

> Phase 01 · Core server · **Depends on:** T-011, T-007 · **Parallel-safe:** yes · **Est. agent time:** 45-90 min

## Goal

Connect the foreground service to the server so a single source of truth exists for 'running', 'starting', 'stopping', 'failed', including the notification text.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-platform` | service state machine, notification updates from a StateFlow |
| `kotlin-core` | coroutine scopes, cancellation on stop, no leaking collectors |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/ServerController.kt` owning the state machine and the server instance
- Notification that reflects real state (port, bind mode, request counter, last error)

## Steps

1. Model the state as a sealed type: Starting, Running, Stopping, Stopped, Failed(reason).
2. Drive start/stop from the service's onStartCommand and its stop action; cancel the scope on stop.
3. Update the notification from the state flow, rate-limited so it is not redrawn per request.
4. Surface a failure reason in the notification text instead of a generic error.

## Acceptance criteria

- [ ] Toggling start/stop repeatedly leaves exactly one server instance running
- [ ] A deliberate bind failure (port already in use) produces state `Failed` with a readable reason
- [ ] The notification text matches `/health` while running

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ServerController*'
adb shell dumpsys notification --noredact | grep -A3 droidroute
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-012 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-012 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-012: Service ↔ server wiring and lifecycle states"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The service owns the server lifecycle; everything else observes one state machine.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-012.log`.
