# T-071 — Anthropic streaming conformance

> Phase 05 · Wire protocols · **Depends on:** T-070, T-068 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Emit the exact Anthropic SSE event sequence (`message_start`, `content_block_start`, deltas, `message_stop`) that strict clients require.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | event order and field names are part of the contract |
| `testing` | event-sequence assertion, including tool-call streaming |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Streaming encoder for the Anthropic dialect
- A test that asserts the full event order for text and for a tool call

## Steps

1. Emit `message_start` before any content, with the correct initial usage.
2. Emit `content_block_start`/`delta`/`stop` per block, in order, including tool_use blocks.
3. Emit `message_delta` with the final stop reason and usage, then `message_stop`.
4. Never reorder or skip events for speed.

## Acceptance criteria

- [ ] The event sequence matches the specification in a golden-file test
- [ ] Tool-call streaming produces valid `input_json_delta` frames
- [ ] A strict client (Claude Code or an equivalent test harness) consumes the stream without error

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*AnthropicStream*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-071 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-071 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-071: Anthropic streaming conformance"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The strictest streaming contract in the project is honoured.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-071.log`.
