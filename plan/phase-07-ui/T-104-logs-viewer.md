# T-104 — Logs viewer with redaction indicator and export

> Phase 07 · UI · **Depends on:** T-008, T-017 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Read the gateway's own logs in the app, with a visible assurance that they are redacted, and export them for the repository.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | paging through large logs without loading them all |
| `security-audit` | an export must not be a new leak path |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/logs/LogsScreen.kt` with filters (level, provider, task) and export
- A redaction badge stating that the redactor ran on every line

## Steps

1. Stream/paginate log reads so a large file does not exhaust memory.
2. Filter by level, provider id and request id.
3. Export through the share sheet after re-running the redactor over the content.
4. Never offer an export that bypasses redaction.

## Acceptance criteria

- [ ] A large log file can be browsed without an out-of-memory crash
- [ ] Exported content passes the secrets preflight
- [ ] Filters work on real records

## Verification

```bash
./gradlew :app:assembleDebug
scripts/preflight-secrets.sh
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-104 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-104 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-104: Logs viewer with redaction indicator and export"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Logs are readable on the phone and safe to export.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-104.log`.
