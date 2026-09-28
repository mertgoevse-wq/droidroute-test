# T-088 — Optional request hedging

> Phase 06 · Routing · **Depends on:** T-087 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Offer the opt-in hedge described in docs/04-routing.md, off by default, because it spends quota twice.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | cancellation semantics for the losing request |
| `testing` | assert exactly one upstream is charged when the hedge wins |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/Hedging.kt` behind a setting (default off)
- A clear UI warning that hedging multiplies quota consumption

## Steps

1. Start a second candidate if no first byte arrives within the configured delay.
2. Cancel the slower request and prove in a test that its usage is not recorded as a completed request.
3. Never hedge on providers whose quota is nearly exhausted.
4. Keep the feature off unless the owner enables it.

## Acceptance criteria

- [ ] With hedging off, exactly one upstream call is made (asserted)
- [ ] With hedging on, the winner is returned and the loser is cancelled (asserted)
- [ ] The setting default is off and the warning is shown in the UI

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Hedging*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-088 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-088 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-088: Optional request hedging"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A latency optimisation exists for the owner to opt into, with its cost stated.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-088.log`.
