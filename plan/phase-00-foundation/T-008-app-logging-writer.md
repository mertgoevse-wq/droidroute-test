# T-008 — App-side log writer

> Phase 00 · Foundation · **Depends on:** T-004 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Implement the Kotlin logger that emits the same JSON-lines records as scripts/log-step.sh, through the same redactor, so runtime logs and agent logs are indistinguishable in shape.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | coroutine-safe appender, non-blocking writes, rotation hooks |
| `testing` | format conformance against a golden record produced by the shell script |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `logging/LogWriter.kt` and `logging/LogRecord.kt`
- `logging/Redactor.kt` shared by app and bridge
- A test comparing an app-written record's shape with a shell-written one

## Steps

1. Model the record exactly as documented in handbooks/05-logging-standard.md.
2. Write appends with a single writer coroutine to keep ordering without blocking callers.
3. Apply the redactor to every field before serialisation, not after.
4. Mirror records into `logs/tasks/` when the Termux integration is enabled and the path is writable.

## Acceptance criteria

- [ ] App record and shell record have identical keys and value shapes (asserted by a test)
- [ ] The redactor strips a planted key from a message field
- [ ] Writes do not block the caller (verified by a timing assertion in a test)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*LogWriter*'
./gradlew :app:testDebugUnitTest --tests '*Redactor*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-008 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-008 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-008: App-side log writer"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

App and agent logs share one format and one redactor; log evidence is now comparable across the two worlds.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-008.log`.
