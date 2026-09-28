# T-014 — Bind modes and the enforced auth floor

> Phase 01 · Core server · **Depends on:** T-013 · **Parallel-safe:** yes · **Est. agent time:** 45-90 min

## Goal

Implement the three bind modes from docs/05-security.md and enforce, in code, that a non-local bind can never run without an API key.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `security-audit` | attack the floor: prove no code path reaches a LAN bind with auth=none |
| `testing` | unit tests for every (bind mode × auth mode) combination |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/BindPolicy.kt` — the matrix and the refusal path
- Refusal recorded through the app logger with a clear reason

## Steps

1. Encode the matrix: local allows none/api_key/oauth; lan and external require api_key or oauth.
2. Refuse at start time, not at request time, and report the refusal in the notification and the UI.
3. Require the explicit confirmation for external mode (checkbox in the UI, persisted as consent).
4. Write the matrix tests so a future refactor cannot lower the floor silently.

## Acceptance criteria

- [ ] Every (bind mode × auth mode) pair behaves as documented, asserted by tests
- [ ] An attempt to run LAN + none fails to start and logs the refusal
- [ ] External mode without recorded consent does not start

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*BindPolicy*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-014 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-014 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-014: Bind modes and the enforced auth floor"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The app cannot be tricked into exposing an unauthenticated port.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-014.log`.
