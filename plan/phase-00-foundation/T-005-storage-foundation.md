# T-005 — Storage foundation (Room + DataStore)

> Phase 00 · Foundation · **Depends on:** T-004 · **Parallel-safe:** yes · **Est. agent time:** 45-90 min

## Goal

Provide the persistence seams: DataStore for preferences (port, bind mode, language, strategy) and Room for structured data (providers, keys metadata, quota ledgers, usage records, logs index).

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `persistence-room` | entities, DAOs, migrations strategy, transaction boundaries |
| `testing` | in-memory database tests for each DAO |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `store/AppDatabase.kt` with entities: Provider, ProviderKey, QuotaLedger, UsageRecord, RoutingAlias
- `store/SettingsStore.kt` backed by DataStore for scalar preferences
- DAO tests using an in-memory database

## Steps

1. Define entities with explicit column names and indexes on the fields the router queries (provider id, key id, window start).
2. Write DAOs with suspend functions and `@Transaction` where two tables must change together.
3. Add a migration policy note: schema version 1 ships with no migration, and every later change needs one.
4. Test insert/read/update for each DAO and the cascade delete of a provider's keys.

## Acceptance criteria

- [ ] `./gradlew :app:testDebugUnitTest` passes, including the new DAO tests
- [ ] Deleting a provider deletes its keys and quota ledgers (asserted in a test)
- [ ] No preference is stored in Room that belongs in DataStore, and vice versa

## Verification

```bash
./gradlew :app:testDebugUnitTest
grep -rn 'Entity(' app/src/main/kotlin/com/droidroute/store/ | wc -l
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-005 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-005 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-005: Storage foundation (Room + DataStore)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Persistence seams exist and are tested; later tasks store data instead of inventing their own storage.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-005.log`.
