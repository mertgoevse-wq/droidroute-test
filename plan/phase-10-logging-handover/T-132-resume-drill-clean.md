# T-132 — Resume drill: clean handover

> Phase 10 · Logging & handover · **Depends on:** T-131 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Prove the handover works by continuing the plan in a fresh session using only the repository.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | design the drill so it cannot cheat by using session memory |
| `technical-writing` | record the drill result as evidence, including friction found |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A recorded drill: start a fresh session, read only `status/` and the target task, complete one real task
- A list of frictions found and the documentation fixes they produced

## Steps

1. Start a fresh session with no chat history, following handbooks/06-resume-protocol.md literally.
2. Complete the next task in the plan end to end.
3. Record every point where the documentation was insufficient, and fix the documentation.
4. Store the drill transcript summary in `status/daily/`.

## Acceptance criteria

- [ ] The task was completed using only repository content
- [ ] Every friction found produced a documentation change in the same commit
- [ ] The drill is recorded with the task id it completed

## Verification

```bash
python3 tools/verify_chain.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-132 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-132 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-132: Resume drill: clean handover"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The resume protocol is proven, not assumed.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-132.log`.
