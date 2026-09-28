# T-017 — Request logging, request ids and redaction

> Phase 01 · Core server · **Depends on:** T-015, T-008 · **Parallel-safe:** yes · **Est. agent time:** 45-90 min

## Goal

Log every request with a `request_id`, latency, result and provider attempts, through the shared redactor, and return the id in `x-droidroute-request-id`.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ktor-server` | call interception, id propagation into the routing context |
| `testing` | canary test: a key sent as a header must not appear in any log line |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/RequestIdPlugin.kt` + `logging/RequestLog.kt`
- Log record schema documented in handbooks/05-logging-standard.md (extended with `request_id`)

## Steps

1. Generate the id at the gate, attach it to the call attributes and to every subsequent log record.
2. Log the outcome once per request (not per byte) with status, latency and attempt count.
3. Apply the redactor to headers and body excerpts before logging them.
4. Add the canary test that sends an `x-api-key` header and greps the log output for it.

## Acceptance criteria

- [ ] Every response carries `x-droidroute-request-id` matching a log record
- [ ] A request with a key header leaves no trace of the key in the logs
- [ ] Logging adds under 5 ms to a request (measured)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*RequestLog*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-017 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-017 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-017: Request logging, request ids and redaction"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Every request is traceable end to end without leaking a credential.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-017.log`.
