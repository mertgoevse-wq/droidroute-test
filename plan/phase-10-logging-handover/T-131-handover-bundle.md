# T-131 — Handover evidence bundle

> Phase 10 · Logging & handover · **Depends on:** T-130, T-129 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Produce one file an arriving agent reads first: current state, next task, open errors, last decisions and where the evidence lives.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | deterministic bundle generation with redaction applied |
| `technical-writing` | content chosen for a reader with no context |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `tools/handover_bundle.py` writing `status/HANDOVER.md`
- A check that the bundle is regenerated whenever a task completes

## Steps

1. Compose from PROGRESS, NEXT, ERRORS, the tail of chain.log and the recent decisions.
2. Apply the redactor; the bundle is committed, so it must be safe.
3. Keep it short enough to read in two minutes, with links for depth.
4. Regenerate it in `scripts/step-commit.sh` so it is never stale.

## Acceptance criteria

- [ ] `status/HANDOVER.md` is regenerated and committed with every task commit
- [ ] The bundle contains no secret-shaped value (canary)
- [ ] A reader can state the next action after reading only the bundle

## Verification

```bash
python3 tools/handover_bundle.py && scripts/preflight-secrets.sh
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-131 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-131 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-131: Handover evidence bundle"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Arriving at this project cold takes two minutes instead of twenty.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-131.log`.
