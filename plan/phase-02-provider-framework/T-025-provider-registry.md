# T-025 — Provider registry with enable/disable and status

> Phase 02 · Provider framework · **Depends on:** T-024, T-018 · **Parallel-safe:** yes · **Est. agent time:** 45-90 min

## Goal

Hold the live set of providers in memory and in Room: enable, disable, expose status, and survive a restart.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `persistence-room` | registry persistence, stable ordering, no duplicate ids |
| `testing` | enable/disable and reload-after-restart tests |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/ProviderRegistry.kt` with a `StateFlow<List<ProviderState>>`
- Room entity for owner overrides (enabled flag, notes) separate from the shipped manifest

## Steps

1. Merge shipped manifests with owner overrides at load time; overrides win per field.
2. Keep the registry immutable in the API surface: expose snapshots, not mutable collections.
3. Status per provider: enabled, disabled-by-owner, invalid-manifest, needs-key, needs-attention.
4. Test that disabling a provider removes it from routing immediately without a restart.

## Acceptance criteria

- [ ] Enabling and disabling a provider takes effect without a server restart
- [ ] A provider with no usable key reports `needs-key` rather than silently failing
- [ ] Registry state survives a restart

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ProviderRegistry*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-025 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-025 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-025: Provider registry with enable/disable and status"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

One authoritative registry drives routing, the UI and the provider endpoints.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-025.log`.
