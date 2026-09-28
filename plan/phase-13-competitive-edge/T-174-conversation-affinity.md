# T-174 — Conversation affinity (sticky provider)

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-154, T-087 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Fix the most repeated complaint about this class of router: switching models mid-conversation resends context and loses provider-side cache. Pin a conversation to a provider while it is healthy, and say plainly when the pin breaks.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | affinity as a soft constraint with an explicit override order |
| `droidroute-verification` | affinity holds, affinity yields on quota, and the switch is recorded with a reason |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/Affinity.kt` keyed by a conversation fingerprint, with a documented precedence against quota, budget and health
- A per-conversation record: current provider, switches, and the reason for each switch

## Steps

1. Derive the fingerprint from stable request elements without storing prompt content beyond a hash.
2. Keep the pin while the provider is healthy and inside budget; break it for quota, breaker or explicit override.
3. Record every switch with its reason so the owner can see why the cache was lost.
4. Expire fingerprints so the store cannot grow without bound.

## Acceptance criteria

- [ ] A conversation stays on one provider across several turns (asserted)
- [ ] An exhausted quota breaks the pin and the switch reason is recorded (asserted)
- [ ] No prompt content is stored — only a fingerprint (asserted by inspecting the store)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Affinity*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-174 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-174 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-174: Conversation affinity (sticky provider)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Provider switching stops quietly destroying prompt cache and re-billing the same context.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-174.log`.
