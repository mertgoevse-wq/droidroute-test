# T-155 — Cost telemetry headers and per-key USD budgets

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-095, T-081, T-017 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Report tokens, cost and savings on every response, and let the owner cap spend per client key and per provider.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | cost attribution: which key, which provider, which price list |
| `droidroute-verification` | budget enforcement tests, including the hard stop and the recorded reason |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `X-DroidRoute-*` response headers: tokens in/out, cost estimate, cache savings, provider, attempt count
- Per-key and per-provider USD budgets with a hard stop and a clear error body

## Steps

1. Derive cost from the usage record and the manifest price list; mark unknown pricing as unknown rather than guessing.
2. Enforce budgets at admission time so a request that would exceed the cap is refused with a reason.
3. Keep subscription providers at $0 in cost analytics while still showing the notional value.
4. Test: a budget of $0.00 blocks paid providers but not free ones.

## Acceptance criteria

- [ ] Headers carry the documented fields on every successful response
- [ ] A key over budget is refused with a message naming the budget and the reset
- [ ] Unknown pricing is labelled unknown, never estimated silently

## Verification

```bash
curl -fsS -D - -o /dev/null http://127.0.0.1:8787/health | grep -i droidroute
./gradlew :app:testDebugUnitTest --tests '*Budget*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-155 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-155 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-155: Cost telemetry headers and per-key USD budgets"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can see and cap what the gateway spends, per key and per provider.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-155.log`.
