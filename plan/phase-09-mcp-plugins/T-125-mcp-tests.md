# T-125 — MCP test suite

> Phase 09 · MCP & plugins · **Depends on:** T-118, T-119, T-120, T-121, T-122, T-123, T-124 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Prove discovery, registry precedence, both transports and the auth rules, including the dead-server path.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | fixtures for each host config format, stub servers, dead-server behaviour |
| `security-audit` | assert the auth rule and the absence of environment values in the registry |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `app/src/test/…/mcp/` suite with config fixtures and stub servers
- A canary test for environment values

## Steps

1. Add fixtures for each supported configuration format, including one malformed file.
2. Add stub stdio and HTTP servers to drive both transports offline.
3. Assert: precedence, auth requirement on `tools/call`, timeout kill, reaping, redaction.
4. Keep the suite offline and deterministic.

## Acceptance criteria

- [ ] All MCP behaviour is covered by offline tests
- [ ] The canary test proves no environment value reaches the registry
- [ ] A dead server degrades gracefully in a test rather than hanging

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*mcp*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-125 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-125 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-125: MCP test suite"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

MCP federation is proven, including the paths that only fail in production otherwise.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-125.log`.
