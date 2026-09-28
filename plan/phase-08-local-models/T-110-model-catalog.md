# T-110 — Model catalog and curated list

> Phase 08 · Local models · **Depends on:** T-109, T-005 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Show what models exist locally and offer a curated set that is known to work on 8 GB.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `local-inference` | sane model choices for an 8 GB phone, with sizes and licences |
| `android-platform` | scanning owner-chosen folders through the storage access framework |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `local/ModelCatalog.kt` — scan `.gguf` files plus a bundled curated list with sizes and licences
- Compatibility badge per entry: comfortable, tight, risky

## Steps

1. Scan the owner's chosen folder and `~/.droidroute/models/` for `.gguf` files, reading metadata where possible.
2. Compose the curated list from models with published sizes and licences; no unattributed entries.
3. Compute the badge from the device's real available memory at scan time.
4. Persist the catalog with content hashes to detect file changes.

## Acceptance criteria

- [ ] Local files appear with their real sizes and quants
- [ ] Every curated entry names its source and licence
- [ ] Badges change when memory pressure changes

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ModelCatalog*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-110 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-110 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-110: Model catalog and curated list"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can pick a model that fits the device without guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-110.log`.
