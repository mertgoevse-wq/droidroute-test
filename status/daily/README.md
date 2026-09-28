# Daily summaries

One file per active day: `YYYY-MM-DD.md`. Written at the end of the day's last task (or when the chain stops) and committed with that task.

## Template

```markdown
# 2026-09-28

**Tasks completed:** T-001 … T-004
**Tasks started, not finished:** T-005 (stopped at step 2/6 — see ERRORS.md)
**Commits:** 4 (see git log)
**Blockers:** none | <one line>
**Next:** T-005

## Notes

- Anything the next session needs that does not fit the status files.
- Decisions taken today that changed the plan.
```

## Why

`status/PROGRESS.md` answers *what is done*. These files answer *what the day looked like* — which is what a human owner reads after a long autonomous run, and what a new agent skims to understand recent context. Kept short: if a day needs more than fifteen lines, the detail belongs in `logs/`.

Retention: newest 14 days (rotated by `scripts/weekly-cleanup.sh`).
