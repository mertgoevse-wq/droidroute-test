# T-133 — Resume drill: interrupted mid-task

> Phase 10 · Logging & handover · **Depends on:** T-132 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Prove the harder case: a task killed halfway leaves enough evidence for a different agent to finish it without guesswork.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | an adversarial drill: kill the session at an awkward step, uncommitted |
| `technical-writing` | verify the STOPPED note template is sufficient and improve it if not |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A recorded drill with a deliberately interrupted task and a successful takeover
- Any improvement to handbooks/06-resume-protocol.md that the drill proved necessary

## Steps

1. Begin a task, complete two or three steps, then stop without committing.
2. Append the STOPPED note exactly as the template prescribes.
3. In a fresh session, follow only the status files and finish the task.
4. Log whether the takeover was unambiguous; if not, fix the protocol.

## Acceptance criteria

- [ ] The takeover completed the task without inspecting session history
- [ ] The working tree state was recoverable exactly as the note described
- [ ] The protocol documentation changed if the drill exposed a gap

## Verification

```bash
cat status/ERRORS.md | tail -20
python3 tools/verify_chain.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-133 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-133 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-133: Resume drill: interrupted mid-task"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The worst realistic interruption is survivable with the documented artefacts alone.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-133.log`.
