# T-091 — App shell and navigation

> Phase 07 · UI · **Depends on:** T-007, T-012 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Create the Material 3 shell with bottom navigation across Dashboard, Providers, Routing, Local, Settings, and a service-state banner shown everywhere.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | navigation host, scaffold, state hoisting |
| `performance-android` | keep the state banner from recomposing the whole tree per request |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/DroidRouteApp.kt` with the navigation graph and five destinations
- A persistent service-state banner (running, failed with reason, stopped)

## Steps

1. Build the scaffold with bottom navigation and per-destination view models.
2. Show the server state as a banner, tappable to start/stop.
3. Keep every screen reachable in one tap from the shell — no nested menus.
4. Add a Compose preview for each destination.

## Acceptance criteria

- [ ] Every destination is reachable and keeps its own scroll/state
- [ ] The banner shows the real service state, including a failure reason
- [ ] Screens render in previews

## Verification

```bash
./gradlew :app:assembleDebug
./gradlew :app:lintDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-091 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-091 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-091: App shell and navigation"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The navigation skeleton exists and later screens plug into it.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-091.log`.
