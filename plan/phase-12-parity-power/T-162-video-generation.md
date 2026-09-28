# T-162 — Video generation endpoint

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-160, T-075 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Add a video generation surface with provider-specific mapping and an honest handling of long-running jobs.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-provider-manifest` | which providers offer video and how their job model works |
| `droidroute-verification` | job polling, timeout and cancellation behaviour |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `/v1/videos/generations` with a documented job lifecycle
- Per-provider mapping for asynchronous jobs where the provider needs polling

## Steps

1. Model the job lifecycle explicitly: submitted, running, ready, failed, cancelled.
2. Never hold a request open indefinitely; return a job handle and poll on demand.
3. Handle provider quotas and cost differences, and report them before submission.
4. Test with a stub provider that exercises both the ready and the failed path.

## Acceptance criteria

- [ ] A job can be submitted, polled and fetched (or the provider gap is logged with evidence)
- [ ] A failed job surfaces the provider's reason
- [ ] No request blocks for the full generation time

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*VideoJob*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-162 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-162 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-162: Video generation endpoint"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Video generation is available without holding HTTP connections open for minutes.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-162.log`.
