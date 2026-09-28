# T-070 — Anthropic messages (non-streaming)

> Phase 05 · Wire protocols · **Depends on:** T-066, T-027, T-028 · **Parallel-safe:** yes · **Est. agent time:** 90-150 min

## Goal

Serve `/v1/messages` — the route Claude Code depends on — including system prompts, content blocks and tool results.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | message shape, content blocks, stop reasons |
| `testing` | golden fixture plus a Claude-Code-shaped request test |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/anthropic/MessagesRoute.kt`
- A fixture captured from a real Claude Code request shape

## Steps

1. Parse `system`, `messages`, `tools`, `tool_choice`, `max_tokens`, `stop_sequences`.
2. Translate content blocks including `tool_use` and `tool_result` into the normalised model.
3. Return the Anthropic response shape with `stop_reason` and `usage` fields present.
4. Accept both `x-api-key` and bearer auth through the existing gate.

## Acceptance criteria

- [ ] A Claude-Code-shaped request receives a response the client accepts
- [ ] Tool call and tool result blocks survive the round trip
- [ ] Missing `max_tokens` produces Anthropic's error shape, not a 500

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*MessagesRoute*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-070 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-070 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-070: Anthropic messages (non-streaming)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Claude Code can talk to DroidRoute on its native protocol.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-070.log`.
