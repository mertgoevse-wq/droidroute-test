# T-049 — Provider: Google AI Studio (free-tier key)

> Phase 03 · Provider catalog · **Depends on:** T-028, T-030 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Connect the Gemini API free tier via API key — separate from the AI Pro OAuth account handled in Phase 4.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | the Gemini API surface and its key parameter style |
| `testing` | fixture for its error envelope, which differs from OpenAI's |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/google-ai-studio.json` with base `https://generativelanguage.googleapis.com/v1beta`
- Gemini-style error parsing in the adapter path

## Steps

1. Support key-in-header and key-in-query styles, choosing the documented modern one.
2. Normalise the Gemini error envelope into the taxonomy (it is not OpenAI-shaped).
3. Confirm that this key and the Phase 4 OAuth account are distinct entities in the UI.

## Acceptance criteria

- [ ] A live call succeeds or the blocker is logged
- [ ] Gemini-shaped errors map correctly in a test
- [ ] The UI can hold both the API key account and the OAuth account without conflating them

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*google*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-049 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-049 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-049: Provider: Google AI Studio (free-tier key)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Google models are available both through the free key tier and (later) the Pro subscription.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-049.log`.
