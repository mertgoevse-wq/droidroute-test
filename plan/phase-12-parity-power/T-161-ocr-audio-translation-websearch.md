# T-161 — OCR, audio translation and web-search fallback

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-075, T-160 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Complete the media surface: document OCR, speech translation, and an optional last-resort web search that does not depend on one provider.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-provider-manifest` | add the capable providers with confirmed endpoints |
| `droidroute-verification` | each endpoint works or reports a precise unsupported error |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `/v1/ocr`, `/v1/audio/translations`, and a web-search fallback used only when no search provider is enabled
- Manifest entries for the providers that serve each capability

## Steps

1. Implement OCR against capable providers, preserving page and layout metadata where the provider returns it.
2. Implement audio translation as transcription plus translation with the two steps visible in the log.
3. Implement the search fallback with explicit rate limiting and a clear statement of what it sends where.
4. Document each endpoint with an example that was actually executed.

## Acceptance criteria

- [ ] Each endpoint returns a real result or a precise unsupported error
- [ ] The search fallback is opt-in and rate-limited
- [ ] Documented examples match captured output

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Ocr*' --tests '*Translation*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-161 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-161 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-161: OCR, audio translation and web-search fallback"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The media surface is complete enough that a client does not need a second gateway.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-161.log`.
