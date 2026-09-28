# T-176 — Battery, thermal and network-aware routing

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-113, T-084 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Use what only a phone knows: prefer local or cheap candidates when the battery is low, avoid loading a large model when the device is hot, and honour a policy for metered connections.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-platform` | BatteryManager, thermal status, ConnectivityManager metered detection |
| `performance-android` | measure the actual cost difference before claiming a benefit |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/DeviceState.kt` exposing battery level/charging, thermal status, metered state and network type
- Configurable policies: `battery_floor`, `thermal_ceiling`, `metered_policy` (allow / ask / block)

## Steps

1. Read device state through the platform APIs and expose it as candidate-selection inputs.
2. Implement policies as routing constraints with a reason string, so each decision is explainable.
3. Refuse a local model load above the thermal ceiling with a message naming the temperature class.
4. Measure and record the effect of the metered policy on data usage.

## Acceptance criteria

- [ ] Below the battery floor, a local or free candidate is preferred with the reason visible (asserted)
- [ ] A blocked metered request returns a clear policy error instead of silently spending mobile data
- [ ] Thermal refusal names the thermal status and what to do about it

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*DeviceState*'
adb shell dumpsys battery | head -5
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-176 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-176 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-176: Battery, thermal and network-aware routing"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Routing decisions respect the device they run on — a capability no server-side gateway has.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-176.log`.
