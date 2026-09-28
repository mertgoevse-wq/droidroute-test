# T-089 — `/v1/routing/explain` and decision logging

> Phase 06 · Routing · **Depends on:** T-087, T-084 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Answer 'why did it pick that?' for any model, both as an API and as structured log records.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | explanation content that is actually useful for debugging |
| `technical-writing` | document the endpoint honestly, including what it does not reveal |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `/v1/routing/explain?model=…` returning candidates, order, strategy and per-candidate reasons
- One structured log record per routing decision

## Steps

1. Explain skipped candidates with the precise reason (parked until, breaker open, disabled, no quota).
2. Include the strategy chain that produced the order.
3. Expose the same information used at request time — explanations must not be reconstructed afterwards.
4. Log the decision with the request id so the two can be joined.

## Acceptance criteria

- [ ] For a model with three candidates the endpoint names each one and its reason for skipped ones
- [ ] The explanation matches what the failover loop actually did for a real request
- [ ] The decision log record contains the request id

## Verification

```bash
curl -fsS 'http://127.0.0.1:8787/v1/routing/explain?model=my-best'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-089 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-089 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-089: `/v1/routing/explain` and decision logging"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Routing is debuggable without reading code or guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-089.log`.
