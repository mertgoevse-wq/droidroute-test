# T-013 — Configurable port with collision handling

> Phase 01 · Core server · **Depends on:** T-012, T-005 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Make the port owner-editable (default 8787), validate it, and offer the next free port when the chosen one is taken.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-platform` | acceptable-port-range validation and a real bind probe |
| `testing` | validation table tests plus a collision case |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/PortAllocator.kt` — validation (1024–65535) and next-free-port search
- DataStore-backed port setting with validation errors surfaced to the UI

## Steps

1. Validate the range and reject privileged and reserved ports with specific messages.
2. Probe by binding and immediately releasing; never by guessing from a static list.
3. Offer the next free port when the chosen one is busy, but never change the setting without consent.
4. Update `scripts/termux-setup.sh` guidance shown in the UI when the port changes.

## Acceptance criteria

- [ ] Setting 80 or 70000 is rejected with a message naming the valid range
- [ ] With a busy port the app suggests the next free one and the suggestion actually binds
- [ ] The persisted port survives a process restart

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*PortAllocator*'
grep -n '8787' app/src/main/kotlin/com/droidroute/store/SettingsStore.kt
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-013 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-013 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-013: Configurable port with collision handling"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The default port is 8787, owner-editable, validated, and collision-safe.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-013.log`.
