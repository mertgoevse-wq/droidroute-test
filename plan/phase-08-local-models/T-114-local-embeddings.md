# T-114 — Local embedding models

> Phase 08 · Local models · **Depends on:** T-113, T-076 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Expose local embedding models through `/v1/embeddings` using the same runtime.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `local-inference` | embedding mode flags and batching for the local runtime |
| `testing` | dimension and determinism assertions |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Embedding mode registration with the `embeddings` capability tag
- A test asserting deterministic vectors for identical input

## Steps

1. Start the runtime in embedding mode for models that support it.
2. Tag them so chat routing never selects them (reusing the Phase 5 rule).
3. Verify batching behaviour and vector dimensions.

## Acceptance criteria

- [ ] Local embeddings return vectors of the expected dimension
- [ ] Identical input yields identical output (determinism asserted)
- [ ] Embedding models never appear as chat candidates

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*LocalEmbeddings*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-114 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-114 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-114: Local embedding models"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Local embedding models are usable for search and indexing work.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-114.log`.
