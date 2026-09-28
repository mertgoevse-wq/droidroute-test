# T-067 — OpenAI chat completions (non-streaming)

> Phase 05 · Wire protocols · **Depends on:** T-066, T-027 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Serve `/v1/chat/completions` end to end, routed through the provider layer, with usage recorded.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | response shape, finish reasons, usage block |
| `testing` | golden response test plus a routing integration test |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/openai/ChatCompletionsRoute.kt`
- Golden request/response fixtures

## Steps

1. Parse the request leniently (clients send extras) but validate the required fields strictly.
2. Resolve the model through routing (a stub candidate list is acceptable until Phase 6 lands).
3. Return a response whose shape matches the golden fixture byte-for-shape.
4. Record usage and cost fields on the usage record.

## Acceptance criteria

- [ ] A real or fixture-backed request returns a schema-correct response
- [ ] Unknown request fields are tolerated, missing required fields produce a 400 in OpenAI's error shape
- [ ] Usage is recorded when the provider reports it

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ChatCompletions*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-067 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-067 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-067: OpenAI chat completions (non-streaming)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The primary OpenAI route works end to end.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-067.log`.
