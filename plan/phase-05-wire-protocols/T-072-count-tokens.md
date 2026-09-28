# T-072 — `/v1/messages/count_tokens`

> Phase 05 · Wire protocols · **Depends on:** T-070 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Provide a token estimate so clients that pre-check context fit get an answer instead of an error.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | the request/response shape of the counting endpoint |
| `testing` | estimate-vs-provider comparison test |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `CountTokensRoute` returning `{input_tokens: n}`
- A documented note on estimate accuracy and its source

## Steps

1. Use provider-reported counts when the provider exposes them.
2. Otherwise estimate locally and label the result as an estimate in the log.
3. Never block the endpoint on a provider round trip when a local estimate is available.

## Acceptance criteria

- [ ] The endpoint returns a number for any valid message list
- [ ] Provider-reported and locally estimated counts are distinguishable in the logs
- [ ] Accuracy of the estimate is stated, with the method used

## Verification

```bash
curl -fsS -X POST http://127.0.0.1:8787/v1/messages/count_tokens -d '{"messages":[]}'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-072 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-072 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-072: `/v1/messages/count_tokens`"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Clients can budget context before spending tokens.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-072.log`.
