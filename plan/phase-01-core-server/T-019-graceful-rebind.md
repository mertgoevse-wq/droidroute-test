# T-019 — Graceful rebind on configuration change

> Phase 01 · Core server · **Depends on:** T-018, T-013 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Changing port or bind mode while running performs a drain → rebind → resume instead of a hard restart.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ktor-server` | drain semantics, readiness flag, minimal client-visible gap |
| `testing` | test that an in-flight request completes across a rebind |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/Rebind.kt` implementing the drain/rebind/resume sequence
- Readiness flag reflected in `/health` during the gap

## Steps

1. Stop accepting new connections, let in-flight requests finish within a bounded window.
2. Release the old socket, bind the new configuration, flip readiness back on.
3. If the new bind fails, return to the previous working configuration and report the failure.
4. Log one record per rebind with old and new configuration.

## Acceptance criteria

- [ ] An in-flight request completes successfully across a rebind
- [ ] A failing rebind rolls back to the previous configuration, still serving
- [ ] The rebind is logged with both configurations

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Rebind*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-019 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-019 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-019: Graceful rebind on configuration change"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Port and bind-mode changes are safe to make while agents are connected.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-019.log`.
