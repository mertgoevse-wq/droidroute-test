# T-096 — Providers list, filters and one-click connect

> Phase 07 · UI · **Depends on:** T-025, T-031, T-033 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

List every provider with its state and give free providers a one-tap connect flow that validates before enabling.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | list rendering with filters, search and clear per-row state |
| `provider-integration` | the one-click sequence: open key page, return, validate, enable |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/providers/ProvidersScreen.kt` with tier/tag filters and search
- One-click connect flow for providers tagged `one-click`

## Steps

1. Show per row: name, tier, state (enabled, needs-key, parked, breaker open), model count.
2. Implement connect: open the key page, accept the returned key, validate, then enable on success.
3. Never enable a provider whose validation failed; show the reason instead.
4. Add the custom-provider entry point at the top of the list.

## Acceptance criteria

- [ ] A failing validation leaves the provider disabled with the reason visible
- [ ] Filters and search work across tier and tags
- [ ] A successful one-click connect results in a working provider in one flow

## Verification

```bash
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-096 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-096 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-096: Providers list, filters and one-click connect"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Connecting a free provider takes one flow instead of a research session.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-096.log`.
