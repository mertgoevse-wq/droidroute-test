# T-141 — Acceptance run A4–A6 (accounts, failover, dashboard)

> Phase 11 · Delivery · **Depends on:** T-140 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Prove criteria A4 to A6, including a real failover and a real key rotation.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | inject a 401 and an exhausted quota without breaking the working setup |
| `llm-routing` | interpret the attempt list and confirm it explains the observed behaviour |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Evidence entries for A4, A5 and A6

## Steps

1. A4: connect the Google account and run a Perplexity search returning citations.
2. A5: revoke a key temporarily and confirm the request still succeeds through the next candidate.
3. A6: compare the dashboard numbers with `/v1/usage` for the same window.
4. Record the attempt list from a failed-then-succeeded request.

## Acceptance criteria

- [ ] A4, A5 and A6 are ticked with evidence
- [ ] The failover evidence shows the specific next candidate that answered
- [ ] Dashboard figures match the API exactly

## Verification

```bash
curl -fsS -X POST http://127.0.0.1:8787/v1/search -d '{"query":"test"}'
curl -fsS http://127.0.0.1:8787/v1/usage
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-141 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-141 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-141: Acceptance run A4–A6 (accounts, failover, dashboard)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Failover and account connectivity are proven, which is the core of the product's value.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-141.log`.
