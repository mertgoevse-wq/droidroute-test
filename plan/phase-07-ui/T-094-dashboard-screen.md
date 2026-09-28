# T-094 — Dashboard screen

> Phase 07 · UI · **Depends on:** T-092, T-032, T-089 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Show the state of the whole system at a glance: server, bind mode, connected clients, per-provider tokens, errors, latency.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | dense but readable layout, honest empty states |
| `performance-android` | refresh cadence that does not drain the battery in the foreground |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/dashboard/DashboardScreen.kt` with live sections and pull-to-refresh
- Empty state that says what to do first (connect a provider)

## Steps

1. Render server state, port, bind mode and current client keys in use.
2. Render per-provider tokens today, error count and p50/p95 latency from `/v1/usage`.
3. Show parked keys with their reset times so a quiet provider is explainable.
4. Poll at a sane interval (e.g. 5 s in the foreground, paused in the background).

## Acceptance criteria

- [ ] Numbers on the dashboard match `/v1/usage` for the same window
- [ ] A parked key is visible with its reset time
- [ ] The empty state names the next action instead of showing zeros

## Verification

```bash
./gradlew :app:assembleDebug
curl -fsS http://127.0.0.1:8787/v1/usage
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-094 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-094 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-094: Dashboard screen"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can see what the gateway is doing without reading logs.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-094.log`.
