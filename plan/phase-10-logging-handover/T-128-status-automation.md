# T-128 — Status file automation

> Phase 10 · Logging & handover · **Depends on:** T-017, T-009 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Make `status/PROGRESS.md` and `status/NEXT.md` update themselves from the plan and the logs, so they cannot go stale through forgetfulness.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | deterministic generation with a stable diff (no timestamp churn) |
| `technical-writing` | status content that answers the three questions an arriving agent has |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `tools/update_status.py` — reads plan/, logs/ and git to regenerate the two files
- A CI check that fails when the generated status disagrees with reality

## Steps

1. Derive completed tasks from the commit subjects (`T-0xx:`) and log records, not from a hand-kept list.
2. Regenerate PROGRESS and NEXT with a stable ordering and no volatile fields.
3. Add `--check` mode and wire it into repo-hygiene.
4. Document the flow in docs/08-workflow.md, replacing any manual instruction that contradicts it.

## Acceptance criteria

- [ ] Running the tool twice produces no diff
- [ ] `--check` fails when a completed task is missing from the status files (proven once, then reverted)
- [ ] CI runs the check

## Verification

```bash
python3 tools/update_status.py && git diff --exit-code status/
python3 tools/update_status.py --check
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-128 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-128 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-128: Status file automation"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The status files are always true, because they are derived.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-128.log`.
