# T-035 — Provider framework test suite

> Phase 02 · Provider framework · **Depends on:** T-024, T-025, T-026, T-027, T-028, T-029, T-030, T-031, T-032, T-033, T-034 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Consolidate adapter, registry, discovery and key tests, and add the malformed-input cases that tend to be forgotten.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | coverage of error paths, no redundant tests, fast runtime |
| `provider-integration` | add one real-world quirk fixture per adapter family |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `app/src/test/…/provider/` suite with fixtures for success and every error class
- A `fixtures/` folder with representative provider payloads, secrets scrubbed

## Steps

1. Enumerate the failure modes: truncation, unexpected fields, HTML error pages, rate-limit bodies in three dialects.
2. Add one fixture per mode and assert the taxonomy value produced.
3. Remove tests that assert nothing and merge duplicated fixtures.
4. Keep the whole suite runnable offline.

## Acceptance criteria

- [ ] The suite runs offline and passes
- [ ] Every taxonomy value is produced by at least one test
- [ ] No fixture contains a real credential

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*provider*'
scripts/preflight-secrets.sh
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-035 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-035 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-035: Provider framework test suite"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The provider layer is provably robust against real upstream weirdness.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-035.log`.
