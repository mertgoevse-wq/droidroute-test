# T-031 — Key validation and invalid marking

> Phase 02 · Provider framework · **Depends on:** T-030, T-029 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Validate a key with one cheap call, mark it invalid on 401/403, and never persist the validation response.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | cheapest possible probe per provider |
| `security-audit` | ensure the probe response body cannot be logged or stored |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/KeyValidator.kt` returning a typed result: valid, invalid, unknown(reason)
- UI-facing status transitions recorded and logged (provider, label, outcome)

## Steps

1. Prefer a models list call; fall back to a one-token chat request where listing is unsupported.
2. On 401/403 mark invalid without deleting; on network failure mark unknown so the key is not blamed.
3. Log provider id, key label and outcome — never the key or the response body.
4. Validate on entry and on demand from the key list; never on a schedule that burns quota.

## Acceptance criteria

- [ ] An invalid key is marked invalid and excluded from rotation
- [ ] A network failure marks the key unknown, not invalid
- [ ] No validation response body appears in logs or the database

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*KeyValidator*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-031 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-031 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-031: Key validation and invalid marking"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Broken keys are identified precisely and quarantined without losing them.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-031.log`.
