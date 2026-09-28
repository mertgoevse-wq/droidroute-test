# T-020 — Optional autostart and doze resilience

> Phase 01 · Core server · **Depends on:** T-018 · **Parallel-safe:** yes · **Est. agent time:** 45-90 min

## Goal

Offer opt-in start-on-boot, and keep the server responsive under doze without draining the battery.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-platform` | BOOT_COMPLETED receiver, doze behaviour, wake-lock discipline |
| `performance-android` | measure idle battery cost and set a bounded expectation |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/BootReceiver.kt` gated by an explicit owner setting (default off)
- Documented idle behaviour: what sleeps, what stays responsive, measured drain

## Steps

1. Register the boot receiver and respect the setting: never autostart without opt-in.
2. Ensure long SSE streams survive doze by using heartbeats rather than wake locks.
3. Measure: battery percentage delta per hour with one connected agent and no traffic.
4. Record the measurement in the component status file.

## Acceptance criteria

- [ ] With autostart on, the server runs after a reboot without opening the UI
- [ ] With autostart off, nothing starts after a reboot
- [ ] Idle drain is measured and recorded with a number, not an adjective

## Verification

```bash
adb shell dumpsys batterystats --charged com.droidroute.app | head -30
./gradlew :app:testDebugUnitTest --tests '*BootReceiver*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-020 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-020 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-020: Optional autostart and doze resilience"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Background behaviour is the owner's choice and its cost is documented with real numbers.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-020.log`.
