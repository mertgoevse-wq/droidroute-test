# T-018 — Configuration persistence and post-mortem rehydration

> Phase 01 · Core server · **Depends on:** T-012, T-005, T-006 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

After a process kill, the server restarts with the same port, bind mode, auth mode and enabled providers, and says so in a start record.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `persistence-room` | read-on-start transaction, consistent snapshot |
| `android-platform` | process-death detection and restart policy |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/StartupSnapshot.kt` — reads settings, providers and keys before binding
- Startup log record stating what was restored and what failed to restore

## Steps

1. Read the whole configuration before binding the socket so the first request already has a full context.
2. Handle partially corrupt state (unknown provider id, missing key) by disabling that entry and logging it.
3. Record a start line in the log with port, bind mode, auth mode and provider count.
4. Test by force-killing the process and restarting the service.

## Acceptance criteria

- [ ] After `am force-stop` and restart, the same port and enabled providers are active
- [ ] A deliberately corrupted provider row is disabled with a logged reason, and the server still starts
- [ ] The startup record exists in the app log

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*StartupSnapshot*'
adb shell am force-stop com.droidroute.app
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-018 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-018 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-018: Configuration persistence and post-mortem rehydration"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The server is crash-tolerant: a kill changes nothing the owner has to re-enter.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-018.log`.
