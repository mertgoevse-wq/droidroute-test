# T-068 — OpenAI streaming (SSE)

> Phase 05 · Wire protocols · **Depends on:** T-067 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Stream `/v1/chat/completions` frames as they arrive, with heartbeats and cancellation propagation.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ktor-server` | response streaming without buffering, disconnect detection |
| `testing` | frame-order test and a cancellation test that proves upstream cancellation |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Streaming implementation plus `data: [DONE]` terminator
- A test asserting incremental delivery (first frame before the last is generated)

## Steps

1. Flush immediately per frame; never accumulate a buffer to 'simplify' the code.
2. Emit a heartbeat comment every 15 seconds so doze and proxies do not drop the stream.
3. On client disconnect, cancel the upstream call so quota is not spent on an abandoned answer.
4. Keep content-type and cache headers exactly as OpenAI's clients expect.

## Acceptance criteria

- [ ] Frames arrive incrementally (asserted by timestamps in a test)
- [ ] A client disconnect cancels the upstream request
- [ ] `data: [DONE]` is always the final frame on success

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Streaming*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-068 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-068 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-068: OpenAI streaming (SSE)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Streaming is incremental, robust to doze, and does not waste quota.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-068.log`.
