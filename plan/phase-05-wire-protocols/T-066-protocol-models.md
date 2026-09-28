# T-066 — Shared protocol models and normalisation

> Phase 05 · Wire protocols · **Depends on:** T-026 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Define the internal message model that all three dialects translate into and out of, so additions never touch three parsers.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | content blocks, tool calls, attachments, stop reasons |
| `kotlin-core` | sealed hierarchies and serialization without nullable soup |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/model/` — NormalisedRequest, NormalisedMessage, ContentPart, ToolCall, NormalisedResponse, Usage
- Mapping notes in docs/02-protocols.md

## Steps

1. Model content as a sealed type: Text, Image, Audio, ToolUse, ToolResult.
2. Model stop reasons as an enum covering all three dialects' vocabularies.
3. Keep provider quirks out of this model — they belong in adapters.
4. Write round-trip tests: normalise → denormalise for each dialect preserves meaning.

## Acceptance criteria

- [ ] A request expressed in any dialect normalises to the same internal model (asserted)
- [ ] No nullable field exists that a dialect actually guarantees
- [ ] Round-trip tests pass for text, image, tool-call and tool-result content

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Normalis*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-066 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-066 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-066: Shared protocol models and normalisation"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

One internal model serves three dialects; protocol work no longer multiplies.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-066.log`.
