# T-004 — Package structure and module boundaries

> Phase 00 · Foundation · **Depends on:** T-003 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Lay down the package layout the rest of the plan assumes, with each package owning one responsibility and a single public entry point, so later tasks never guess where code goes.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | create the packages with minimal, honest seams (no empty placeholder classes) |
| `technical-writing` | record the layout in docs/01-architecture.md's layer table |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Packages under `com.droidroute`: `server`, `protocol`, `provider`, `routing`, `vault`, `store`, `mcp`, `local`, `bridge`, `ui`, `logging`
- One `README.md`-level note per package is not required — the architecture table is the single source

## Steps

1. Create the packages with their first real type only where the task needs it — do not add empty files.
2. Define shared value types that multiple layers need (RequestId, ProviderId, ModelId, Capability) in their owning package.
3. Confirm `docs/01-architecture.md` lists exactly these packages and no others.

## Acceptance criteria

- [ ] Every package named in `docs/01-architecture.md` exists in the source tree
- [ ] No package contains an empty or placeholder class
- [ ] `./gradlew :app:assembleDebug` still succeeds

## Verification

```bash
./gradlew :app:assembleDebug
find app/src/main/kotlin/com/droidroute -maxdepth 1 -type d | sort
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-004 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-004 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-004: Package structure and module boundaries"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The layer boundaries from the architecture doc exist in code and are stable for later tasks.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-004.log`.
