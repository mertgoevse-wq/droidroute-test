# T-026 — Adapter interface and capability model

> Phase 02 · Provider framework · **Depends on:** T-025 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Define what every adapter must implement and how capabilities are declared, so routing can ask precise questions.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | sealed capability model, suspend interface, error taxonomy |
| `llm-gateway-protocols` | capability set that matches real provider differences |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/ProviderAdapter.kt` — `chat`, `stream`, `models`, `validateKey`, `capabilities`
- `provider/Capabilities.kt` — chat, streaming, tools, vision, images, tts, stt, embeddings, longContext
- `provider/ProviderError.kt` — QuotaExceeded, AuthError, Timeout, RateLimited, ServerError, BadRequest

## Steps

1. Keep the interface free of wire-format details: adapters exchange normalised messages.
2. Make the error taxonomy exhaustive, because routing keys its decisions on it.
3. Declare capabilities as data so a manifest can override the adapter's defaults.
4. Document the contract in docs/03-providers.md.

## Acceptance criteria

- [ ] Every adapter error maps to exactly one taxonomy value (asserted by a test)
- [ ] Capabilities are queryable per provider and per model
- [ ] The interface has no protocol-specific type in its signature

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ProviderError*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-026 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-026 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-026: Adapter interface and capability model"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Adapters are interchangeable and the router can reason about them without special cases.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-026.log`.
