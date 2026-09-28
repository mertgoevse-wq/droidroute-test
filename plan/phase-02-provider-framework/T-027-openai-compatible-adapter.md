# T-027 — Generic OpenAI-compatible adapter

> Phase 02 · Provider framework · **Depends on:** T-026 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Implement the adapter that covers the majority of providers: bearer auth, `/chat/completions`, streaming, tools, model list.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | request/response shapes, streaming frames, usage reporting |
| `testing` | fixture-driven tests plus one live call against a free provider |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/adapters/OpenAiCompatibleAdapter.kt`
- Fixtures for success, tool call, streaming chunks, and the four error classes

## Steps

1. Build requests from normalised messages; pass through `tools`, `response_format`, `seed` when supported.
2. Parse streaming frames, tolerate provider-specific extras, and surface usage when present.
3. Map HTTP status plus body to the error taxonomy, including the 'quota exhausted' variants gateways use.
4. Support per-provider extra headers and a configurable auth header (some gateways differ).

## Acceptance criteria

- [ ] Fixture tests cover success, streaming, tool call, 401, 429, 500 and malformed JSON
- [ ] One live call against a free provider succeeds (skipped with a logged reason when no key exists)
- [ ] Streaming frames are emitted as soon as they arrive, not buffered to the end

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*OpenAiCompatibleAdapter*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-027 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-027 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-027: Generic OpenAI-compatible adapter"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Most providers work through one adapter; only genuine differences need their own code.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-027.log`.
