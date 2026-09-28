# T-029 — Model discovery with manual fallback

> Phase 02 · Provider framework · **Depends on:** T-027, T-028 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Learn each provider's models at runtime via `/models`, with an honest manual path when discovery is unavailable.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | per-provider discovery quirks and pagination |
| `testing` | discovery fixtures, empty list, and the manual fallback path |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/ModelCatalog.kt` — per-provider model cache with timestamps and source (discovered/manual/static)
- Refresh action with a per-provider result summary

## Steps

1. Call the manifest's discovery path; parse leniently but never invent ids.
2. Cache results with a TTL and refresh on demand or on provider enable.
3. When discovery fails, keep the manifest's `fallback_models` and mark the source as `manual`.
4. Never mark a provider ready if it has zero known models and no manual list.

## Acceptance criteria

- [ ] A provider with a working `/models` shows its models after a refresh
- [ ] A provider whose discovery fails reports the reason and falls back to the static list
- [ ] The catalog never contains an id that no provider reported or the owner typed

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ModelCatalog*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-029 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-029 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-029: Model discovery with manual fallback"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Model ids come from the providers themselves, with a recorded source for every entry.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-029.log`.
