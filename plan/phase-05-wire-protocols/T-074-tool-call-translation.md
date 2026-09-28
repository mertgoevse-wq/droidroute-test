# T-074 — Tool call translation across dialects

> Phase 05 · Wire protocols · **Depends on:** T-067, T-070, T-073 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Make function calling work whichever dialect the client speaks and whichever the provider speaks.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | schema differences between OpenAI tools, Anthropic tools and Gemini functionDeclarations |
| `testing` | cross-dialect matrix test: 3 clients × 3 providers |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/tools/ToolTranslator.kt`
- A matrix test proving each dialect can drive each other dialect's tool format

## Steps

1. Translate tool schemas in both directions, preserving required/optional semantics.
2. Translate tool calls and tool results as content parts, not as a side channel.
3. Handle the case where a provider cannot do tools by returning a clear capability error.
4. Test the full matrix, including multi-call turns.

## Acceptance criteria

- [ ] The 3×3 matrix passes in tests
- [ ] A provider without tool support produces a capability error, not a malformed request
- [ ] Multi-call turns preserve ordering

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ToolTranslator*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-074 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-074 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-074: Tool call translation across dialects"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Agents can use tools through any dialect and any provider that supports them.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-074.log`.
