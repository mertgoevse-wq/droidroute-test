# T-073 — Gemini surface (`/v1beta`)

> Phase 05 · Wire protocols · **Depends on:** T-066, T-027 · **Parallel-safe:** yes · **Est. agent time:** 90-150 min

## Goal

Serve the Gemini-style endpoints so Google-shaped software can connect directly, including streaming with `alt=sse`.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | contents/parts shape, generationConfig, tool declarations |
| `testing` | fixture parity between Gemini and OpenAI requests for the same intent |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/gemini/GenerateContentRoute.kt` with streaming support
- `/v1beta/models` listing

## Steps

1. Map `contents[]`/`parts[]` including `inlineData` and function calls.
2. Implement `:generateContent` and `:streamGenerateContent` on the same model resolution path.
3. Return Gemini-shaped errors for this surface (the taxonomy maps per surface).

## Acceptance criteria

- [ ] Both endpoints answer a real request; streaming emits incremental chunks
- [ ] An image part round-trips through the normalised model
- [ ] Errors on this surface use Gemini's shape

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Gemini*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-073 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-073 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-073: Gemini surface (`/v1beta`)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

All three dialects are live on one port.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-073.log`.
