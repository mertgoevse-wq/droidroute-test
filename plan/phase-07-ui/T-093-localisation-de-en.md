# T-093 — Localisation: German default, English available

> Phase 07 · UI · **Depends on:** T-091 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Ship both languages through Android resources, with German as the default and no hard-coded user-facing strings.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | string resources, plural handling, per-locale formatting |
| `technical-writing` | German copy that is plain and correct, not machine-literal |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `values/strings.xml` (German default) and `values-en/strings.xml`
- A lint rule or check that fails on hard-coded user-facing text

## Steps

1. Extract every user-facing string; no literals in composables.
2. Write the German copy first as the default resource set, then the English translations.
3. Use plurals and locale-aware formatting for counts, numbers and timestamps.
4. Add the check so future work cannot bypass localisation.

## Acceptance criteria

- [ ] Switching the device language switches the UI
- [ ] No user-facing string literal remains in a composable (checked)
- [ ] German copy reads naturally to a native speaker, with technical terms kept as they are

## Verification

```bash
./gradlew :app:lintDebug
grep -rn 'Text("' app/src/main/kotlin/com/droidroute/ui | head
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-093 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-093 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-093: Localisation: German default, English available"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner reads German by default and English is one setting away.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-093.log`.
