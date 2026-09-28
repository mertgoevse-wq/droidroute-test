# T-037 — Provider: Bynara / NaraRouter (priority)

> Phase 03 · Provider catalog · **Depends on:** T-027, T-029, T-031 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Wire the owner's highest-priority gateway first: free tier, ~7M tokens/day, ~50 models, OpenAI-compatible. Manifest, one-click connect, live validation.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | confirm base URL, auth header and model list from the provider's own site |
| `testing` | fixture plus a live validation call, skipped cleanly without a key |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/bynara.json` with `tier: 1`, `auth.type: bearer`, discovery on `/models`
- `quota.window: daily` with the documented hint

## Steps

1. Read the provider's current documentation; do not reuse the URL from any other source. Base URL is documented as `https://router.bynara.id/v1` — confirm it before committing.
2. Register the provider in docs/03-providers.md with its tag `free` and `one-click`.
3. Validate a real key with a models-list call and record the model count in the task log.
4. Record the quota reset behaviour observed from the provider's response headers.

## Acceptance criteria

- [ ] The provider appears in `/v1/providers` as Tier 1 with `free` and `one-click` tags
- [ ] A live key validates and lists a non-zero model count (or the task logs why it could not be tested)
- [ ] The manifest contains no hard-coded model list that contradicts discovery

## Verification

```bash
python3 tools/check_providers.py
./gradlew :app:testDebugUnitTest --tests '*bynara*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-037 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-037 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-037: Provider: Bynara / NaraRouter (priority)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner's primary free gateway is connected, validated and routable.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-037.log`.
