# T-184 — Native-versus-service benchmark on this device

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-136, T-180 · **Parallel-safe:** yes · **Est. agent time:** 150-300 min

## Goal

Measure the claim that a native Android gateway beats running a Node-based router on the same phone: memory, idle battery, cold start and request overhead — with numbers, or with an honest retraction.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `performance-android` | a fair measurement protocol: same workload, same device state, multiple runs |
| `technical-writing` | publish the method and the numbers, including where the native approach loses |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A benchmark protocol and results table in `docs/14-benchmark.md`
- A recorded comparison against a Node-based router on the A56, or a documented reason the comparison could not be run

## Steps

1. Define the workload: idle with one connected agent, a fixed prompt sequence, a cold start.
2. Measure the same workload on both implementations on the same device, with the same thermal starting point.
3. Report median and spread, not a best-case single run.
4. If the native version does not win on a metric, say so — a retracted claim beats a false one.

## Acceptance criteria

- [ ] The protocol is written so a third party could repeat it
- [ ] Numbers are reported with spread, not as single values
- [ ] Any metric where the native approach loses is stated explicitly

## Verification

```bash
adb shell dumpsys meminfo com.droidroute.app | head -20
adb shell dumpsys batterystats --charged com.droidroute.app | head -20
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-184 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-184 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-184: Native-versus-service benchmark on this device"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The core claim of this project is either backed by numbers or corrected in public.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-184.log`.
