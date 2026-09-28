# T-115 — Speech models (STT and TTS)

> Phase 08 · Local models · **Depends on:** T-108, T-075 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Add whisper.cpp transcription and a speech synthesis path, with a clear `not_supported` when only one side is available.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `local-inference` | whisper.cpp usage, model sizes and their accuracy trade-off |
| `testing` | transcription test with a bundled short sample, plus the unsupported path |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `local/SpeechRuntime.kt` for whisper.cpp resolution and invocation
- `/v1/audio/transcriptions` served locally; TTS either implemented or explicitly not_supported

## Steps

1. Resolve whisper.cpp following the same three-path strategy as llama.cpp.
2. Invoke it for uploaded audio and return the documented response shape.
3. For TTS, assess what is realistic on-device and either implement it or record the decision.
4. Ensure a sample audio file exists for tests and contains no personal data.

## Acceptance criteria

- [ ] A short audio sample transcribes correctly
- [ ] Missing TTS support returns `not_supported` naming the missing runtime
- [ ] No test asset contains personal audio

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Speech*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-115 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-115 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-115: Speech models (STT and TTS)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Speech in and out works locally, or its absence is stated precisely.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-115.log`.
