# T-153 — Token compression engines

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-068, T-081 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Reduce prompt cost measurably: lossless-first filters for code and logs, optional lossy packs, an inflation guard, per-request opt-out, and a reported savings number.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | where compression may be applied without changing the answer's meaning |
| `droidroute-verification` | savings measurement plus a fidelity test proving no semantic change for the lossless path |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/compression/` engine set with an explicit engine list and per-engine enable flags
- `X-DroidRoute-Tokens-Saved` style reporting and an inflation guard

## Steps

1. Implement lossless filters first (whitespace, duplicate log lines, repeated boilerplate) — they are safe and provable.
2. Add lossy packs behind explicit opt-in with a fidelity gate: if the check fails, send the original.
3. Never compress tool schemas or system instructions in a way that changes behaviour; document the exclusions.
4. Measure savings on a real request and record the number in the task log.

## Acceptance criteria

- [ ] Lossless compression is provably reversible (round-trip test)
- [ ] The inflation guard prevents a compressed prompt from being larger than the original
- [ ] Savings are reported per request and measured in the task log

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Compression*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-153 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-153 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-153: Token compression engines"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Prompt cost drops measurably without surprising changes to answers.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-153.log`.
