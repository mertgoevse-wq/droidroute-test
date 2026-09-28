# T-015 — Auth gate middleware

> Phase 01 · Core server · **Depends on:** T-014 · **Parallel-safe:** yes · **Est. agent time:** 45-90 min

## Goal

Install one middleware that enforces the configured auth mode for every route: no header, api-key bearer, or OAuth-issued short-lived token.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ktor-server` | route interceptor, timing-safe comparison, 401 shape per protocol surface |
| `security-audit` | constant-time comparison and no key material in error bodies |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/AuthGate.kt` — accepts `Authorization: Bearer` and `x-api-key`
- 401 responses shaped per calling surface (OpenAI, Anthropic, Gemini)

## Steps

1. Hash incoming keys with the stored salt and compare in constant time.
2. Exempt nothing except `/health` in local mode; in any non-local mode exempt nothing at all.
3. Shape the 401 body for the surface that was called so clients parse it correctly.
4. Never echo the presented key or its prefix in the response or the log.

## Acceptance criteria

- [ ] With api-key mode, a request without or with a wrong key gets a 401 in the correct dialect
- [ ] A correct key is accepted within 5 ms overhead (measured in a test)
- [ ] No response body or log line contains any part of the presented key

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*AuthGate*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-015 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-015 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-015: Auth gate middleware"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Every route is behind one gate with one policy source.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-015.log`.
