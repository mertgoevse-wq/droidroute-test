# T-147 — Chain closure and final handover statement

> Phase 11 · Delivery · **Depends on:** T-146 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Close the plan honestly: states what is complete, what is not, what is risky, and what a future agent should do next.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `technical-writing` | a closing statement without self-congratulation, stating gaps plainly |
| `testing` | final verification run of the whole chain tooling |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `status/CLOSURE.md`: what shipped, verification summary, known limitations, recommended next work
- Final status regeneration so PROGRESS, NEXT and HANDOVER reflect the closed chain

## Steps

1. Run the full verification set: tests, chain verification, link check, secrets preflight, plan check.
2. State every known limitation and every unverified claim explicitly.
3. Recommend the three most valuable next tasks with the reason each matters.
4. Regenerate the status artefacts and commit the closure.

## Acceptance criteria

- [ ] Every verification tool is run and its result recorded
- [ ] Limitations are stated without hedging, and unverified items are labelled as such
- [ ] The closure document names the next three tasks with reasons

## Verification

```bash
./gradlew :app:testDebugUnitTest
python3 tools/verify_chain.py
python3 tools/generate_plan.py --check
scripts/preflight-secrets.sh
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-147 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-147 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-147: Chain closure and final handover statement"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The plan is closed with an honest account of what exists, what was proven, and what remains.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-147.log`.
