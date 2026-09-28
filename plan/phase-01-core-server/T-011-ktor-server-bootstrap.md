# T-011 — Ktor server bootstrap

> Phase 01 · Core server · **Depends on:** T-007, T-003 · **Parallel-safe:** yes · **Est. agent time:** 45-90 min

## Goal

Mount an embedded Ktor CIO server: start, stop, and answer a minimal `/health` with version, uptime, port and bind mode. No provider or protocol logic yet.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ktor-server` | CIO engine, plugin installation, graceful shutdown |
| `testing` | start/stop lifecycle test and a health route test |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/HttpServer.kt` — start/stop taking a `Port` and `BindMode`
- `server/routes/HealthRoutes.kt` returning version, uptime, bind mode, port
- Test asserting the listening socket is released on stop

## Steps

1. Create the CIO application with the JSON and status-pages plugins installed.
2. Bind according to `BindMode`; raise a typed error when binding fails instead of swallowing it.
3. Implement graceful shutdown that drains in-flight requests for a bounded time.
4. Expose start/stop so the service and the UI can drive it.

## Acceptance criteria

- [ ] `curl -fsS http://127.0.0.1:<port>/health` returns 200 with version, uptime, port, bind mode
- [ ] After stop, the port is free immediately (a second bind succeeds within a second)
- [ ] `./gradlew :app:dependencies` shows no Netty — CIO only

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*HttpServer*'
curl -fsS http://127.0.0.1:8787/health
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-011 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-011 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-011: Ktor server bootstrap"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A real HTTP server runs on the device and can be started and stopped programmatically.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-011.log`.
