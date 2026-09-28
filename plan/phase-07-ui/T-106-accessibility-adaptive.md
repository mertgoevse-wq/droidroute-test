# T-106 — Accessibility and adaptive layout pass

> Phase 07 · UI · **Depends on:** T-091, T-092, T-093, T-094, T-096, T-097, T-098, T-099, T-100, T-102, T-103, T-104, T-105 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Make every screen usable with a screen reader, large fonts, one hand, and on a tablet or folded device.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | content descriptions, focus order, adaptive layouts |
| `performance-android` | no layout thrash at large font scales |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Content descriptions on every interactive element
- Layout bookkeeping in the UI component status file

## Steps

1. Audit each screen with a screen reader; fix missing or misleading descriptions.
2. Test at 200 % font scale and fix truncation and overlap.
3. Add tablet-width layouts where a list+detail split is clearly better (providers, logs).
4. Verify minimum touch target sizes.

## Acceptance criteria

- [ ] Every interactive element has a meaningful description
- [ ] No screen breaks at 200 % font scale
- [ ] Touch targets meet the documented minimum size

## Verification

```bash
./gradlew :app:lintDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-106 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-106 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-106: Accessibility and adaptive layout pass"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The UI works for a one-handed user with large fonts and for a screen reader.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-106.log`.
