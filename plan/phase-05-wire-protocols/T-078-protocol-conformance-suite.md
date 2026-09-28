# T-078 — Protocol conformance suite (golden files)

> Phase 05 · Wire protocols · **Depends on:** T-067, T-068, T-069, T-070, T-071, T-072, T-073, T-074, T-075, T-076, T-077 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Lock the three dialects with golden files so a later refactor cannot silently break a client.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | golden-file strategy, update workflow that requires a human decision |
| `llm-gateway-protocols` | capture real client traffic shapes, not invented ones |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `app/src/test/resources/golden/{openai,anthropic,gemini}/` request and response pairs
- A test that fails on any uncontrolled shape change

## Steps

1. Capture real request shapes from Claude Code and an OpenAI-compatible client where possible.
2. Store both request and response goldens; assert shape, not incidental values.
3. Document how to update a golden deliberately (never by rerunning a script blindly).
4. Add the suite to the CI verify job.

## Acceptance criteria

- [ ] The suite passes and is wired into CI
- [ ] Deliberately breaking one response field makes the suite fail (proven once, then reverted)
- [ ] Goldens contain no captured credentials

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Conformance*'
scripts/preflight-secrets.sh
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-078 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-078 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-078: Protocol conformance suite (golden files)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Protocol compatibility is enforced by tests rather than by hope.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-078.log`.
