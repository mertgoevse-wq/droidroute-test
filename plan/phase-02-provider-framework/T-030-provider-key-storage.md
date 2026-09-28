# T-030 — Per-provider key storage and pool model

> Phase 02 · Provider framework · **Depends on:** T-006, T-025 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Store multiple labelled keys per provider, in the vault, with the metadata routing needs (label, status, quota window).

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `security-audit` | vault-only plaintext, metadata without secrets |
| `persistence-room` | key metadata table, cascade delete with the provider |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `store/ProviderKeyEntity.kt` + DAO (provider id, label, vault ref, status, window, created, lastUsed)
- `provider/KeyPool.kt` skeleton with add/remove/list by provider

## Steps

1. Store only a vault reference in Room; the material itself lives in the vault.
2. Model status: active, parked(reset_at), invalid, unchecked.
3. Implement cascade delete so removing a provider removes its keys and quotas in one transaction.
4. Expose masked representations for the UI, computed on demand, never stored.

## Acceptance criteria

- [ ] No plaintext key exists outside the vault (verified by inspecting the database file)
- [ ] Deleting a provider removes its key rows and quota rows in one transaction
- [ ] The UI-facing list contains only masked values

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*KeyPool*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-030 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-030 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-030: Per-provider key storage and pool model"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Multiple keys per provider are the normal case, and none of them is stored in the clear.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-030.log`.
