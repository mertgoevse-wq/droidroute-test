# T-160 — Modality bridge (vision, audio, video)

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-075, T-073, T-026 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Route non-text requests to a capable model automatically, converting between modality shapes where the provider differs.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | capability-driven candidate selection for non-text traffic |
| `droidroute-verification` | conversion round trips and the incapable-provider error path |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/bridge/ModalityBridge.kt` for vision, audio and video inputs
- Capability declarations extended with modality granularity per model

## Steps

1. Detect the modality of each content part and require the candidate to declare it.
2. Convert between dialect shapes (base64 inline data, URLs, file references) without corrupting bytes.
3. Reject unsupported combinations with a capability error naming what is missing.
4. Test each modality against a capable and an incapable provider.

## Acceptance criteria

- [ ] An image, an audio clip and a video reference each route to a capable model or fail with a precise reason
- [ ] Binary payloads survive conversion (checksum compared in a test)
- [ ] Capability declarations are per model, not per provider

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ModalityBridge*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-160 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-160 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-160: Modality bridge (vision, audio, video)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Non-text requests are first-class and routed by capability rather than by guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-160.log`.
