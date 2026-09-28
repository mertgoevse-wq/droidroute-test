# T-140 — Acceptance run A1–A3 (server, agents, providers)

> Phase 11 · Delivery · **Depends on:** T-139, T-021, T-096 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Prove criteria A1 to A3 from docs/10-acceptance.md with raw evidence.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | run each criterion exactly as written and capture raw output |
| `technical-writing` | record evidence so a third party can reproduce it |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Evidence entries for A1, A2 and A3 in logs/tasks/T-140.log plus the acceptance document ticks

## Steps

1. A1: change the port, restart, confirm `/health` on the new port.
2. A2: point Claude Code and Freebuff at the server and complete one real prompt each.
3. A3: list the provider coverage, add a custom provider through the form, and use one-click connect.
4. Capture the raw command output for each, not a summary of it.

## Acceptance criteria

- [ ] A1, A2 and A3 are ticked with commands and raw output in the log
- [ ] Anything that failed is recorded as failed with the reason, not skipped
- [ ] A3 names exactly which providers the owner's credentials could validate

## Verification

```bash
curl -fsS http://127.0.0.1:8787/health
tail -n 40 logs/tasks/T-140.log
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-140 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-140 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-140: Acceptance run A1–A3 (server, agents, providers)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The first three acceptance criteria have reproducible evidence.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-140.log`.
