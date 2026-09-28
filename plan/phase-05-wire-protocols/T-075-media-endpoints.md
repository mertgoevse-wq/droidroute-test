# T-075 — Media endpoints (images, TTS, STT)

> Phase 05 · Wire protocols · **Depends on:** T-073, T-026 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Serve OpenAI-shaped media endpoints and route them only to providers that declare the capability.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | image generation, speech synthesis and transcription request shapes |
| `testing` | capability-gating tests plus a failure path for unsupported models |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `/v1/images/generations`, `/v1/audio/speech`, `/v1/audio/transcriptions`
- Capability gating so unsupported providers are never chosen

## Steps

1. Implement each endpoint against the normalised model where possible, with provider-specific mapping where not.
2. Refuse with a clear `not_supported` when no enabled provider declares the capability.
3. Handle binary responses without corrupting them through the JSON layer.

## Acceptance criteria

- [ ] Each endpoint works against at least one capable provider, or the blocker is logged per endpoint
- [ ] Requesting media from an incapable provider returns a clear error
- [ ] Binary payloads survive the round trip (checksum compared in a test)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Media*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-075 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-075 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-075: Media endpoints (images, TTS, STT)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Media is a first-class part of the gateway, not an afterthought.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-075.log`.
