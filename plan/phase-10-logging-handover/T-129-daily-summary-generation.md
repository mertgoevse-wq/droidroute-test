# T-129 — Daily summary generation

> Phase 10 · Logging & handover · **Depends on:** T-128 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Produce the daily summary files from the logs so the owner can read a day in fifteen lines.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | aggregation from log records into the documented template |
| `technical-writing` | summaries that state facts, not narration |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `tools/gen_daily_summary.py` writing `status/daily/YYYY-MM-DD.md`
- Template kept in sync with status/daily/README.md

## Steps

1. Aggregate completed tasks, started tasks, commits, blockers and the next task from the log records.
2. Refuse to invent content: a day with no records produces a file that says so.
3. Keep the output under the documented length.

## Acceptance criteria

- [ ] A generated summary matches the template exactly
- [ ] An empty day produces an honest empty summary
- [ ] Running it twice produces identical output

## Verification

```bash
python3 tools/gen_daily_summary.py --date 2026-09-28 && cat status/daily/2026-09-28.md
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-129 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-129 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-129: Daily summary generation"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can read a day of autonomous work in one screen.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-129.log`.
