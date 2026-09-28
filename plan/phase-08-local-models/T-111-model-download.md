# T-111 — Model download with resume and checksum

> Phase 08 · Local models · **Depends on:** T-110, T-007 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Download a curated model reliably on a phone connection: resumable, checksum-verified, with progress in the foreground service.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | resumable HTTP with range requests and a bounded retry policy |
| `security-audit` | verify the checksum before the file is offered as usable |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `local/ModelDownloader.kt` with pause/resume/cancel and progress in the notification
- Checksum verification with a clear failure that deletes the partial file

## Steps

1. Implement range-based resume so an interrupted download continues instead of restarting.
2. Verify size and checksum before marking the model usable.
3. Report progress through the existing foreground notification.
4. Handle storage-exhaustion by stopping cleanly and reporting remaining space.

## Acceptance criteria

- [ ] An interrupted download resumes and completes with a verified checksum
- [ ] A corrupted download is rejected and does not appear as usable
- [ ] Progress is visible in the notification while the app is backgrounded

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ModelDownloader*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-111 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-111 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-111: Model download with resume and checksum"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Model acquisition survives a flaky phone connection.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-111.log`.
