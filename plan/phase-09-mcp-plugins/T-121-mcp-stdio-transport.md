# T-121 — stdio transport launcher with timeouts and reaping

> Phase 09 · MCP & plugins · **Depends on:** T-120 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Launch stdio MCP servers inside Termux/Debian, keep them alive, and never let a stuck process block a task.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `mcp-protocol` | stdio framing, newline-delimited JSON-RPC, stderr capture |
| `kotlin-core` | process supervision with hard timeouts and guaranteed reaping |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `mcp/StdioTransport.kt` with per-server process supervision
- A hard request timeout and a kill-on-timeout policy with logging

## Steps

1. Start the server command in the Termux/Debian environment and keep stdin/stdout open.
2. Frame requests correctly and read responses without deadlocking on a chatty server.
3. Enforce per-call timeouts; kill and report rather than hanging.
4. Reap processes on shutdown and on server removal.

## Acceptance criteria

- [ ] A stdio server starts once and serves multiple calls
- [ ] A server that never responds is killed after the timeout and reported (asserted with a stub that sleeps)
- [ ] No orphan process remains after the app stops (verified on device)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*StdioTransport*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-121 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-121 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-121: stdio transport launcher with timeouts and reaping"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

stdio MCP servers are usable without risking a hung gateway.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-121.log`.
