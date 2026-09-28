# T-130 — Chain log integrity verification

> Phase 10 · Logging & handover · **Depends on:** T-128 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Guarantee the handover spine is complete: every completed task has a commit, a log file and a status entry.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | cross-source consistency check across git, logs and status |
| `technical-writing` | a report that names exactly what is missing |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `tools/verify_chain.py` comparing plan, git log, logs/tasks and status/PROGRESS.md
- CI integration and a documented manual run

## Steps

1. For each task marked complete: assert a commit with the right subject exists, a task log exists, and the status lists it.
2. Report discrepancies with the task id and the missing artefact.
3. Allow a documented exemption list for tasks completed before this check existed, and mark it as such.

## Acceptance criteria

- [ ] The tool exits 0 on a consistent repository
- [ ] Deleting one task log makes it fail with a precise message (proven once, then reverted)
- [ ] Any exemption is explicit and dated

## Verification

```bash
python3 tools/verify_chain.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-130 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-130 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-130: Chain log integrity verification"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The evidence trail is verifiable, which is what makes the handover real.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-130.log`.
