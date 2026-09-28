# T-098 — Custom provider form with discovery

> Phase 07 · UI · **Depends on:** T-033, T-096 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Add an arbitrary OpenAI- or Anthropic-compatible endpoint through a form that validates as it goes.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | form state, inline validation, keyboard types |
| `security-audit` | the key field must behave like a secret from the first keystroke |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/providers/CustomProviderForm.kt`
- Inline validation for URL, compat type and model list

## Steps

1. Validate the URL shape live and reject non-loopback plaintext http immediately.
2. Offer a discover-models action that reports what it found or why it failed.
3. Keep the key field masked with an explicit reveal, and clear it from memory on cancel.
4. On save, run validation and report the result without closing the screen on failure.

## Acceptance criteria

- [ ] A provider added through the form answers a request
- [ ] Validation failures are shown inline and distinct from network errors
- [ ] The key field is masked by default and never logged

## Verification

```bash
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-098 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-098 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-098: Custom provider form with discovery"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Custom providers are a form-filling exercise, not a config-file edit.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-098.log`.
