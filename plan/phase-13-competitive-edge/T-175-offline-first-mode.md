# T-175 — Offline-first mode with queued cloud requests

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-113, T-152 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Answer from a local model when there is no connectivity, queue what only a cloud provider can do, and replay it when the network returns — with the owner informed, never silently.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-platform` | connectivity callbacks and airplane mode across Android versions |
| `droidroute-verification` | offline, return-to-online, queue overflow and cancelled-queue paths |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/OfflinePolicy.kt` with a documented decision table: connectivity × local availability × request type
- A bounded queue with per-item expiry, visible in the UI, cancellable per item

## Steps

1. Decide per request: serve locally, queue, or fail immediately with a clear offline error.
2. Bound the queue by count and age; drop with a logged reason instead of growing forever.
3. Replay on connectivity return in submission order, respecting budgets and quotas.
4. Tell the owner in the response and the UI when an answer came from the local model because the network was gone.

## Acceptance criteria

- [ ] With connectivity off and a model loaded, a request is answered locally and labelled as such
- [ ] With connectivity off and no model, a cloud-only request is queued and replayable, or refused with a clear reason
- [ ] The queue is bounded and expiry is enforced (asserted)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*OfflinePolicy*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-175 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-175 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-175: Offline-first mode with queued cloud requests"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The gateway keeps working with no network, which no competitor intends to do.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-175.log`.
