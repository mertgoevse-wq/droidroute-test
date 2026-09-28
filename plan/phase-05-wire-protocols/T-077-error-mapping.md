# T-077 — Unified error mapping and the `droidroute` error object

> Phase 05 · Wire protocols · **Depends on:** T-067, T-070, T-073, T-026 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Normalise every failure into the calling dialect's shape and attach the attempt list so a failing chain is debuggable from the client.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | error shapes per dialect, including Anthropic's overloaded_error |
| `testing` | a mapping table test covering every taxonomy value × every surface |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/errors/ErrorMapper.kt`
- Documentation table in docs/02-protocols.md (already sketched there — now made true)

## Steps

1. Map each taxonomy value per surface as documented.
2. Attach `{attempts, strategy, request_id}` to every error body.
3. Guarantee that a 5xx never leaks a stack trace or an upstream URL containing a key.
4. Test the full mapping table.

## Acceptance criteria

- [ ] Every taxonomy value maps per surface and is asserted by a test
- [ ] No error body contains a key, a token or a stack trace
- [ ] The `droidroute` object is present on all error responses

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ErrorMapper*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-077 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-077 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-077: Unified error mapping and the `droidroute` error object"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Clients can parse every failure, and the owner can see why the chain failed.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-077.log`.
