# T-122 — HTTP and SSE transport

> Phase 09 · MCP & plugins · **Depends on:** T-120 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Call remote MCP servers over HTTP and consume SSE streams where a server uses them.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `mcp-protocol` | HTTP transport semantics and the SSE variant |
| `security-audit` | remote servers may need a token — store it in the vault like any other credential |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `mcp/HttpTransport.kt` and `mcp/SseTransport.kt`
- Per-server authentication configured through the vault

## Steps

1. Implement request/response over HTTP with correct headers and error propagation.
2. Consume SSE where the server sends a stream, without buffering indefinitely.
3. Store any server token in the vault and never in the registry file.
4. Test against a local stub server, not a third-party service.

## Acceptance criteria

- [ ] Both transports work against a local stub
- [ ] A server token is absent from the registry file (asserted)
- [ ] Timeouts behave as documented

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*HttpTransport*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-122 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-122 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-122: HTTP and SSE transport"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Remote MCP servers are usable without weakening credential handling.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-122.log`.
