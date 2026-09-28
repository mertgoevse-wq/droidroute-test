# T-083 — Multi-provider key chaining

> Phase 06 · Routing · **Depends on:** T-081, T-082, T-080 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

The owner's headline requirement: bind a model to keys from several different providers so an exhausted quota automatically hands over to the next one.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | chain semantics: a logical model backed by heterogeneous candidates |
| `testing` | end-to-end chain test: first key exhausted → second provider answers |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/KeyChain.kt` — an ordered chain of `(provider, key, model)` with per-link quota and health
- UI-facing chain model and validation rules

## Steps

1. Allow a chain to mix providers and model ids, since gateways expose different names for equivalent models.
2. Evaluate each link's usability before the request (parked key, open breaker, disabled provider).
3. Fail over within the chain before considering unrelated candidates.
4. Test a three-link chain where the first two are exhausted and the third answers.

## Acceptance criteria

- [ ] With two exhausted links the third answers, and the switch is visible in the attempt list
- [ ] A chain entry pointing at a disabled provider is skipped, not fatal
- [ ] The chain's behaviour is asserted by an automated test, not only observed by hand

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*KeyChain*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-083 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-083 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-083: Multi-provider key chaining"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

One logical model can be backed by a pool spanning multiple gateways, switching automatically.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-083.log`.
