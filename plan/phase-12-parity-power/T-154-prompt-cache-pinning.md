# T-154 — Prompt-cache pinning and cache-hit telemetry

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-149, T-081 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Pin reusable prompt prefixes to the same account so provider-side caches hit, and report the resulting savings.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | prefix stability as a routing constraint, and when it must yield to availability |
| `droidroute-verification` | cache-hit accounting tests, including the case where the pinned key is parked |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/CachePinner.kt` with a documented precedence against quota and health
- Cache-hit and savings fields in the usage record and the response headers

## Steps

1. Hash the reusable prefix and remember which key served it successfully.
2. Prefer that key while it is usable; fall back to availability rules the moment it is not.
3. Record cache-hit savings separately from token savings so the numbers are not conflated.
4. Expose the pin state in the explain output.

## Acceptance criteria

- [ ] Repeated requests with the same prefix prefer the same key (asserted)
- [ ] A parked pinned key falls back without failing the request
- [ ] Cache-hit savings appear in usage and headers

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*CachePinner*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-154 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-154 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-154: Prompt-cache pinning and cache-hit telemetry"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Provider-side caching is actively used instead of accidentally missed.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-154.log`.
