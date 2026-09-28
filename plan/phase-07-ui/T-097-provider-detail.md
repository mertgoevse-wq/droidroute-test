# T-097 — Provider detail screen

> Phase 07 · UI · **Depends on:** T-096, T-032, T-082 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Everything about one provider in one place: models, keys, quota windows, health numbers, event history.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | information density with a clear hierarchy |
| `llm-routing` | present quota and health numbers in a way that explains routing decisions |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/providers/ProviderDetailScreen.kt`
- Actions: refresh models, validate keys, disable provider, delete custom provider

## Steps

1. Show the model list with capability tags (tools, vision, embeddings, free).
2. Show keys masked, with status and last-used timestamps.
3. Show quota state per key including whether the window is known or estimated.
4. Link to the explain view filtered to this provider.

## Acceptance criteria

- [ ] All displayed values are live, not cached placeholders
- [ ] A disabled provider's detail screen explains why it is disabled
- [ ] Destructive actions require confirmation

## Verification

```bash
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-097 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-097 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-097: Provider detail screen"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Any provider question is answerable from one screen.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-097.log`.
