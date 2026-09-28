# T-028 — Generic Anthropic-compatible adapter

> Phase 02 · Provider framework · **Depends on:** T-026 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Implement the Anthropic-shaped adapter for providers that offer that surface (needed by Claude Code and by several gateways).

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | `/v1/messages` semantics, system prompts, content blocks |
| `testing` | conformance fixtures for streaming event order |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/adapters/AnthropicCompatibleAdapter.kt`
- Fixtures for message start/delta/stop and tool_use blocks

## Steps

1. Translate normalised messages into Anthropic content blocks including images and tool results.
2. Handle the `anthropic-version` header per the provider's requirement.
3. Preserve `cache_control` markers when a provider supports prompt caching.
4. Map the `overloaded_error` shape used by some gateways to the taxonomy.

## Acceptance criteria

- [ ] Fixture tests pass for text, image, tool_use and error shapes
- [ ] Streaming event order matches the Anthropic specification in the fixtures
- [ ] A provider using only the Anthropic surface can be called after this task

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*AnthropicCompatibleAdapter*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-028 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-028 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-028: Generic Anthropic-compatible adapter"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Anthropic-shaped gateways are first-class providers.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-028.log`.
