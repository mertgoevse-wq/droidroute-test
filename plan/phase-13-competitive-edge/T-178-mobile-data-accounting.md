# T-178 — Mobile-data accounting and budget

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-155, T-176 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Measure bytes per provider and per day, warn before the owner's mobile-data budget is exceeded, and enforce it when asked.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `performance-android` | byte accounting per request without buffering payloads |
| `droidroute-verification` | budget enforcement at the boundary plus a metered-vs-unmetered test |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Per-request byte accounting split by upload/download, tagged with the network type
- A monthly mobile-data budget with warn-once and a hard stop when configured

## Steps

1. Count bytes at the transport layer, not by measuring computed strings.
2. Attribute usage to provider and network type so unmetered traffic does not consume the budget.
3. Warn at the configured threshold once, then stop only if the policy says so.
4. Expose usage in the dashboard and in `/v1/usage`.

## Acceptance criteria

- [ ] Mobile-data usage is counted per provider and network type (asserted against a fixture)
- [ ] Wi-Fi traffic does not consume the mobile budget (asserted)
- [ ] The hard stop returns a policy error naming the budget and its reset

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*DataBudget*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-178 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-178 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-178: Mobile-data accounting and budget"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can see and cap what the gateway costs in mobile data, not only in tokens.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-178.log`.
