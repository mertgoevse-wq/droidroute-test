# T-112 — Memory estimation, warnings and trim handling

> Phase 08 · Local models · **Depends on:** T-109, T-110 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Implement the no-limit-but-no-surprises policy: estimate RAM need, warn with numbers, and unload under memory pressure.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `local-inference` | KV cache estimation from context, layers and head dimension |
| `android-platform` | onTrimMemory handling and what to unload first |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `local/MemoryGuard.kt` — estimate, colour-coded warning, unload ranking
- Warning screen with the concrete numbers and the recommended smaller context

## Steps

1. Estimate need = file size + KV cache + overhead, and compare with available memory.
2. Warn at the documented thresholds with actual numbers and a 'load anyway' action.
3. On memory pressure, unload idle models first, then the least recently used, and only then the active one.
4. Never kill a model mid-request without logging why.

## Acceptance criteria

- [ ] A too-large model produces the documented warning with real numbers, and loading anyway is possible
- [ ] Under simulated memory pressure the idle model is unloaded first
- [ ] No unload happens without a log record naming the reason

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*MemoryGuard*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-112 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-112 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-112: Memory estimation, warnings and trim handling"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can run any model size and always knows the risk before starting.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-112.log`.
