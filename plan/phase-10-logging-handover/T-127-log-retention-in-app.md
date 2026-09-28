# T-127 — Log retention and rotation inside the app

> Phase 10 · Logging & handover · **Depends on:** T-008, T-104 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Apply the documented retention (14 daily, 60 task logs, chain log forever) to app-written logs as well as script-written ones.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | rotation under concurrent writers without losing records |
| `testing` | rotation boundary tests and an interrupted-rotation test |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `logging/LogRotator.kt` implementing the same policy as scripts/weekly-cleanup.sh
- A test proving both implementations agree on the boundary cases

## Steps

1. Implement the same counts and the same archive destination as the shell script.
2. Rotate atomically: move complete files, never truncate a file being written.
3. Run rotation on a weekly schedule and on demand.
4. Assert parity with the shell script on the same fixture directory.

## Acceptance criteria

- [ ] The app and the script produce the same file set for the same fixture input
- [ ] An interrupted rotation leaves no lost records (asserted)
- [ ] `chain.log` is never rotated by either implementation

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*LogRotator*'
scripts/weekly-cleanup.sh --dry-run
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-127 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-127 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-127: Log retention and rotation inside the app"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Retention is one policy with two implementations that agree.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-127.log`.
