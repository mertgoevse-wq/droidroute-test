# T-116 — Local vision models

> Phase 08 · Local models · **Depends on:** T-113, T-112 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Support small multimodal models so image requests can be answered offline, with adjusted memory warnings.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `local-inference` | multimodal gguf handling and its extra memory cost |
| `testing` | image part round trip through the normalised model |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Vision capability declaration for local multimodal models
- Memory estimate adjusted for the vision encoder

## Steps

1. Detect multimodal capability from the model metadata or the owner's declaration.
2. Route image content parts to the local model when it is the chosen candidate.
3. Adjust the memory estimate and warnings accordingly.

## Acceptance criteria

- [ ] An image request can be answered by a local multimodal model
- [ ] Non-vision local models reject image content with a capability error
- [ ] Memory warnings reflect the higher need

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*LocalVision*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-116 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-116 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-116: Local vision models"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Offline image questions are possible, with honest resource expectations.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-116.log`.
