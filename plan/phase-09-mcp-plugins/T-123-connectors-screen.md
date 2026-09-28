# T-123 — Connectors screen

> Phase 09 · MCP & plugins · **Depends on:** T-120, T-103 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Show every connector (provider, GitHub, tunnel, search) with its real state, and let the owner enable or disable it.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | a screen that shows health honestly, including 'configured but unreachable' |
| `technical-writing` | one line per connector explaining what it enables |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/connectors/ConnectorsScreen.kt`
- Per-connector state source wired to real checks, not to optimistic flags

## Steps

1. List connectors with their state and the last check time.
2. Provide a 'test' action per connector that performs a real check and shows the result.
3. Distinguish 'not configured' from 'configured but failing' — they need different owner actions.
4. Link each connector to the relevant setup documentation.

## Acceptance criteria

- [ ] Every connector's state comes from a real check
- [ ] A failing connector names the failure, not just a red dot
- [ ] Enabling a connector never silently changes another setting

## Verification

```bash
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-123 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-123 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-123: Connectors screen"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can see the whole integration surface and its real health.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-123.log`.
