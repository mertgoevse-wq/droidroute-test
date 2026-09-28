# T-101 — Routing explain viewer

> Phase 07 · UI · **Depends on:** T-089, T-100 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Surface `/v1/routing/explain` in the UI so a surprise routing decision can be understood in seconds.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | present a candidate list with skip reasons compactly |
| `technical-writing` | reason labels that are precise, not vague ('parked until 00:00', not 'unavailable') |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/routing/ExplainSheet.kt` reachable from the dashboard and provider detail
- Reason vocabulary shared with the backend, not re-invented in the UI

## Steps

1. Render the ordered candidate list with the reason each skipped candidate was skipped.
2. Show the strategy chain that produced the order.
3. Let the owner re-run the explanation after a change without leaving the screen.

## Acceptance criteria

- [ ] Reasons match the API's reason strings exactly
- [ ] Skipped candidates are visually distinct from usable ones
- [ ] Refreshing the explanation reflects a just-made configuration change

## Verification

```bash
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-101 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-101 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-101: Routing explain viewer"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Routing is explained in the UI, backed by the same data the router used.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-101.log`.
