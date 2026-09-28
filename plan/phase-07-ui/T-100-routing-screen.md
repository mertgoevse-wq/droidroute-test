# T-100 — Routing screen: strategies, aliases, key chains

> Phase 07 · UI · **Depends on:** T-080, T-083, T-084 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Let the owner control routing: pick a strategy (globally or per model), define aliases, and build multi-provider key chains.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | an editor for a nested structure without a wall of inputs |
| `llm-routing` | prevent configurations that cannot work (cycles, disabled providers, empty chains) |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/routing/RoutingScreen.kt` with strategy picker, alias editor and chain builder
- Validation feedback for impossible configurations

## Steps

1. Offer the eight strategies with a one-line explanation of each and a composed default.
2. Build an alias editor with candidate reordering and per-alias strategy override.
3. Build the key-chain editor: add links from any provider, reorder, label the chain.
4. Reject invalid configurations inline before saving.

## Acceptance criteria

- [ ] A change to the strategy takes effect without restarting the server
- [ ] An alias and a chain can each be created, saved and used from a client
- [ ] Invalid configurations are blocked with a reason

## Verification

```bash
./gradlew :app:assembleDebug
curl -fsS 'http://127.0.0.1:8787/v1/routing/explain?model=my-best'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-100 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-100 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-100: Routing screen: strategies, aliases, key chains"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner's headline routing requirement is fully controllable from the phone.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-100.log`.
