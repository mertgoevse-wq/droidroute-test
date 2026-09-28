# T-138 — Dependency and licence review

> Phase 11 · Delivery · **Depends on:** T-136, T-137 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Know exactly what ships, under which licence, and record any obligation the owner takes on.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `security-audit` | check for known-vulnerable versions before release |
| `technical-writing` | a licence inventory that a non-lawyer can read |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A dependency inventory with versions, licences and purpose
- A decision entry recording anything with an obligation (attribution, copyleft, commercial limits)

## Steps

1. List runtime dependencies from the Gradle report and record each licence.
2. Check each against its project's current licence text, not against a memory of it.
3. Record any obligation that affects how the owner may distribute the APK.
4. Remove any dependency that is unused — an unused dependency is pure liability.

## Acceptance criteria

- [ ] Every runtime dependency has a recorded licence and purpose
- [ ] Obligations are written down in status/DECISIONS.md
- [ ] No unused dependency remains

## Verification

```bash
./gradlew :app:dependencies --configuration releaseRuntimeClasspath | head -40
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-138 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-138 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-138: Dependency and licence review"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

What ships is known, and its obligations are recorded before release.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-138.log`.
