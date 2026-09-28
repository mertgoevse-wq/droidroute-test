# T-033 — Custom provider create/edit/delete

> Phase 02 · Provider framework · **Depends on:** T-024, T-029, T-030 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Let the owner add any OpenAI- or Anthropic-compatible endpoint through a form, with discovery and a manual model list.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | the fields that actually matter for a custom endpoint |
| `testing` | create/edit/delete round trip plus validation failures |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/CustomProviderService.kt` — create, update, delete, discover models
- Persisted as an owner manifest in Room, distinct from shipped manifests

## Steps

1. Accept name, base URL, compat, auth type, default headers, optional model list.
2. Validate the URL shape and refuse plaintext http except for loopback addresses.
3. Run discovery on save and report the result inline; on failure keep the manual list path.
4. Deleting removes keys, quotas and usage rows in one transaction, with a confirmation step.

## Acceptance criteria

- [ ] A custom OpenAI-compatible endpoint can be added and used to answer a request
- [ ] An http:// non-loopback URL is rejected with a clear message
- [ ] Deleting the provider leaves no orphan rows

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*CustomProvider*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-033 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-033 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-033: Custom provider create/edit/delete"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can extend the provider set without waiting for an app update.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-033.log`.
