# T-152 — Adaptive admission, overload protection and rolling leases

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-087 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Queue heavyweight requests instead of rejecting them, enforce per-connection rolling RPM leases, and support a reverse-proxy base path.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ktor-server` | admission queueing, backpressure and bounded waiting |
| `droidroute-verification` | overload tests: burst above the limit, queue drain, lease rollover |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/Admission.kt` with a bounded queue, explicit wait policy and a truthful 429 only when the queue is full
- Rolling RPM leases per client key, enforced with per-request atomic accounting
- Configurable base path for reverse-proxy deployments

## Steps

1. Model admission as a bounded queue with a documented maximum wait; never wait unbounded.
2. Implement the rolling lease so a burst is spread rather than rejected, and log every throttled decision.
3. Honour a configured base path on every route and in generated snippets.
4. Test a burst above the limit and assert that queued requests complete rather than fail.

## Acceptance criteria

- [ ] A burst above the RPM limit drains through the queue instead of 503-ing
- [ ] The queue has a hard bound and a 429 that names the limit when exceeded
- [ ] The base path works for all four protocol surfaces

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Admission*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-152 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-152 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-152: Adaptive admission, overload protection and rolling leases"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The gateway stays useful under load instead of failing loudly at the first spike.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-152.log`.
