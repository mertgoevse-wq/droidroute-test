# T-120 — MCP bridge API

> Phase 09 · MCP & plugins · **Depends on:** T-119, T-015, T-022 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Serve the registry and pass JSON-RPC through: `/mcp/servers`, `/mcp/tools`, `/mcp/{id}`, `/mcp/refresh`.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `mcp-protocol` | JSON-RPC framing, `initialize`, `tools/list`, `tools/call` |
| `security-audit` | the bridge must not become an unauthenticated command channel |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/routes/McpRoutes.kt`
- A flattened tool index at `/mcp/tools` with server attribution

## Steps

1. Implement the four endpoints with the documented shapes.
2. Require api-key auth for `tools/call`, regardless of bind mode.
3. Support `?server=` on `/mcp/tools` to filter the index.
4. Return tool-level errors as MCP errors, not as DroidRoute errors, so clients parse them correctly.

## Acceptance criteria

- [ ] A `tools/call` reaches a real server and returns its result
- [ ] `tools/call` without a key is rejected in every bind mode
- [ ] The tool index attributes every tool to its server

## Verification

```bash
curl -fsS http://127.0.0.1:8787/mcp/servers
./gradlew :app:testDebugUnitTest --tests '*McpRoutes*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-120 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-120 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-120: MCP bridge API"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Agents can discover and call every connected MCP tool through one endpoint.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-120.log`.
