# T-061 — `POST /v1/search` convenience endpoint

> Phase 04 · Accounts & OAuth · **Depends on:** T-060, T-015 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Expose DroidRoute's own search façade returning `{answer, citations[], model, provider}` so agents can search without knowing the provider.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | a stable, documented response shape |
| `testing` | routing to the search-capable provider, error when none is available |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/routes/SearchRoutes.kt`
- Documentation in docs/02-protocols.md including the response schema

## Steps

1. Route the request to providers declaring search capability, honouring the active strategy.
2. Return a clear `no_provider_available` error when no search-capable provider is enabled.
3. Include `request_id` and the provider used so the answer is traceable.
4. Document the endpoint with a request and response example that were both actually executed.

## Acceptance criteria

- [ ] The endpoint returns an answer with citations from a real provider
- [ ] Without a search provider it returns the documented error, not a 500
- [ ] The documented example matches a real captured response

## Verification

```bash
curl -fsS -X POST http://127.0.0.1:8787/v1/search -d '{"query":"test"}'
./gradlew :app:testDebugUnitTest --tests '*SearchRoutes*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-061 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-061 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-061: `POST /v1/search` convenience endpoint"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Agents have a provider-independent search entry point.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-061.log`.
