# T-117 — Embedded (JNI) runtime spike and decision

> Phase 08 · Local models · **Depends on:** T-113 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Answer whether an embedded llama.cpp is worth building, with evidence, and record the decision rather than the intention.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `local-inference` | JNI integration shape, build complexity, ABI constraints |
| `performance-android` | measure the difference in start time and memory against the Termux path |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A spike branch or a documented experiment (not merged code, if the answer is no)
- A decision entry in status/DECISIONS.md with go or no-go and the evidence

## Steps

1. Assess build complexity honestly: toolchain, binary size, licence obligations.
2. Measure the two paths' start latency and memory if a prototype is feasible within the spike budget.
3. Write the decision with numbers and constraints, including what would change the answer.

## Acceptance criteria

- [ ] A decision exists in status/DECISIONS.md with evidence or an explicit statement of what could not be measured
- [ ] No half-integrated JNI code is left on main
- [ ] The task states clearly whether a future agent should revisit it

## Verification

```bash
grep -n 'embedded' status/DECISIONS.md
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-117 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-117 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-117: Embedded (JNI) runtime spike and decision"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The embedded runtime question is settled with evidence instead of being forgotten.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-117.log`.
