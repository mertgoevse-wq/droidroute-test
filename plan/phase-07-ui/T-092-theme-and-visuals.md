# T-092 — Theme, dark/light and typography

> Phase 07 · UI · **Depends on:** T-091 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

A coherent Material 3 theme with dynamic colour, proper dark mode, and a typographic scale that stays readable on a phone.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | colour scheme, dynamic colour, typography scale |
| `performance-android` | no overdraw, no recomposition from theme objects |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/theme/` with light, dark and dynamic variants
- Status colours for provider health that are distinguishable in both modes

## Steps

1. Define light/dark schemes and enable dynamic colour on Android 12+ with a static fallback.
2. Give health states a colour plus a shape or label, so colour is never the only signal.
3. Verify contrast ratios for text on both schemes.
4. Document the palette in the design note inside the theme package.

## Acceptance criteria

- [ ] Both modes render every screen without unreadable text
- [ ] Health states are distinguishable without relying on colour alone
- [ ] Text contrast meets the documented ratio

## Verification

```bash
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-092 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-092 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-092: Theme, dark/light and typography"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The app looks intentional in both modes and stays legible.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-092.log`.
