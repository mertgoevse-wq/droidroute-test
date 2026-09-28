# T-023 — Core server test suite and service lifecycle evidence

> Phase 01 · Core server · **Depends on:** T-011, T-012, T-013, T-014, T-015, T-016, T-017, T-018, T-019, T-020, T-021, T-022 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Consolidate the phase's tests into one suite and prove the service lifecycle on-device with recorded evidence.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | fill coverage gaps, remove duplication, keep the suite fast |
| `android-platform` | instrumented service lifecycle test with an evidence capture |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `app/src/test/…/server/` suite covering gate, policy, port, rebind, keys, logging
- `app/src/androidTest/…/ServiceLifecycleTest.kt` with a recorded evidence snippet

## Steps

1. Run the whole suite and close the gaps the phase's tasks left open.
2. Add the instrumented test that starts the service, hits `/health`, stops it, and asserts the port is free.
3. Store the evidence output under `logs/` as part of the task log.
4. Remove any test that asserts nothing meaningful.

## Acceptance criteria

- [ ] `./gradlew testDebugUnitTest` passes with the new suite
- [ ] The instrumented test passes on the device or an emulator, with output recorded
- [ ] No test depends on network access or the owner's credentials

## Verification

```bash
./gradlew :app:testDebugUnitTest
./gradlew :app:connectedDebugAndroidTest
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-023 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-023 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-023: Core server test suite and service lifecycle evidence"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Phase 1 is provable: the server, its gate, its policy and its lifecycle all have evidence.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-023.log`.
