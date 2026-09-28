# T-046 — Provider: OpenRouter with free-model tagging

> Phase 03 · Provider catalog · **Depends on:** T-027, T-029, T-032 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Connect OpenRouter and tag its free models so the `free_first` strategy can prefer them.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | the free/paid distinction in its model list and the correct attribution headers |
| `llm-routing` | how the free tag feeds candidate ordering |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/openrouter.json` with base `https://openrouter.ai/api/v1`
- Model tagging so `:free` variants are recognised without hard-coded id lists

## Steps

1. Derive free-ness from the model metadata when available; otherwise from the documented id suffix.
2. Send the optional attribution headers the provider requests.
3. Confirm that the free subset is visible in `/v1/models` with the free tag.

## Acceptance criteria

- [ ] Free models are tagged and preferred under `free_first`
- [ ] No free model id is hard-coded; tagging survives a model-list refresh
- [ ] Attribution headers are sent when configured

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*openrouter*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-046 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-046 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-046: Provider: OpenRouter with free-model tagging"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A large free model pool is available and correctly prioritised.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-046.log`.
