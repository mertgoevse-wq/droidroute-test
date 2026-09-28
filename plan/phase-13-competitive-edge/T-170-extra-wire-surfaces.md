# T-170 — Extra wire surfaces: OpenAI Responses API and Vertex AI

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-066, T-027, T-055 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Add the surfaces competitors speak that DroidRoute does not: the OpenAI Responses shape and Google Vertex AI with Application Default Credentials.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | Responses API event model and the Vertex request shape |
| `droidroute-verification` | golden files per surface plus credential-failure paths |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `/v1/responses` decoding and streaming to the normalised model
- Vertex AI provider path supporting ADC (`authorized_user`) alongside service-account credentials

## Steps

1. Map Responses-style input/output items onto the normalised model without losing tool calls.
2. Implement Vertex auth resolution: ADC first, then service account, and report which one was used.
3. Add golden files for both surfaces and wire them into the conformance suite.
4. Never log the credential material; log only the credential type.

## Acceptance criteria

- [ ] A Responses-shaped request round-trips through the normalised model (asserted)
- [ ] Vertex auth resolves via ADC on the device, or the failure names what was missing
- [ ] Credential type appears in logs; credential material does not

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Responses*' --tests '*Vertex*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-170 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-170 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-170: Extra wire surfaces: OpenAI Responses API and Vertex AI"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Two more client and provider dialects work, covering the surfaces competitors advertise.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-170.log`.
