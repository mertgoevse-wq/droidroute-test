# T-164 — Canonical model ordering and free-tier catalogue view

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-069, T-082, T-095 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Serve `/v1/models` in a stable, provider-grouped order with combos pinned first, and show the free-tier catalogue with real reset semantics.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | stable ordering that does not reshuffle per request |
| `droidroute-compose-ui` | a catalogue screen that states what is free and when it resets |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Deterministic `/v1/models` ordering: combos, then tier 1 grouped by provider, then the rest
- Free-tier screen: provider, models, window, reset time, remaining quota or an honest unknown

## Steps

1. Sort deterministically and test that two consecutive calls return identical order.
2. Show reset times in local time and mark learned windows as learned rather than published.
3. Never present an unknown remaining quota as a number.
4. Add the screen to the dashboard navigation.

## Acceptance criteria

- [ ] Model ordering is stable across calls (asserted)
- [ ] The free-tier screen matches `/v1/usage` for the same window
- [ ] Unknown values are labelled unknown

## Verification

```bash
curl -fsS http://127.0.0.1:8787/v1/models | head -30
./gradlew :app:testDebugUnitTest --tests '*ModelOrder*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-164 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-164 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-164: Canonical model ordering and free-tier catalogue view"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Clients see a stable catalogue and the owner sees the real free-tier picture.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-164.log`.
