# T-076 — Embeddings endpoint

> Phase 05 · Wire protocols · **Depends on:** T-066, T-029 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Serve `/v1/embeddings` for hosted providers and for local embedding models.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | embedding request/response shape and batching |
| `testing` | dimension and ordering assertions plus a batching test |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `/v1/embeddings` with input batching
- Capability tagging so chat routing never selects an embedding model

## Steps

1. Accept string and array inputs; preserve input order in the response with correct indices.
2. Batch according to the provider's limit, not arbitrarily.
3. Tag embedding models so the router keeps them out of chat candidate lists.

## Acceptance criteria

- [ ] Order and count are preserved for batched inputs (asserted)
- [ ] Embedding models never appear as chat candidates (asserted)
- [ ] Vector dimensions are returned exactly as the provider sent them

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Embeddings*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-076 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-076 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-076: Embeddings endpoint"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Embeddings work for hosted and local models, with correct routing isolation.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-076.log`.
