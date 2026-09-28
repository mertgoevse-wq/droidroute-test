# T-080 — Aliases and model groups

> Phase 06 · Routing · **Depends on:** T-079 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Let the owner define names like `my-best` that expand into a prioritised candidate list with its own strategy.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | alias semantics, precedence, and strategy override per alias |
| `persistence-room` | alias storage and validation |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/AliasResolver.kt` + Room entity for aliases
- Validation preventing alias cycles and self-reference

## Steps

1. Define an alias as `{name, candidates[], strategy?, pinnedProvider?}`.
2. Reject cycles at save time with a readable message instead of failing at request time.
3. Expose aliases in the model list so clients can request them like any model.
4. Never let an alias silently fall back to a model the owner did not list.

## Acceptance criteria

- [ ] An alias request routes to the first working candidate in its order
- [ ] A cyclic alias definition is rejected at save time
- [ ] Aliases appear in `/v1/models` and resolve through `/v1/routing/explain`

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*AliasResolver*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-080 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-080 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-080: Aliases and model groups"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can express intent ('best free model') once and reuse it everywhere.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-080.log`.
