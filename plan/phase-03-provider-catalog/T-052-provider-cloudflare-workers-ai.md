# T-052 — Provider: Cloudflare Workers AI

> Phase 03 · Provider catalog · **Depends on:** T-027, T-033 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect Cloudflare Workers AI, whose base URL embeds an account id.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | account-scoped base URL template |
| `kotlin-core` | template substitution in the manifest without string concatenation bugs |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/cloudflare-workers-ai.json` with an account-id placeholder
- Manifest support for a templated base URL with a required setting

## Steps

1. Allow a `{account_id}` placeholder resolved from provider settings at load time.
2. Fail with a specific message when the setting is missing, rather than producing a broken URL.
3. Validate a key and record the free daily allowance.

## Acceptance criteria

- [ ] A missing account id produces a clear error and disables the provider
- [ ] With the id present, a live call succeeds or the blocker is logged
- [ ] No other manifest's base URL is templated, keeping the feature narrowly scoped

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Template*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-052 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-052 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-052: Provider: Cloudflare Workers AI"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Account-scoped providers can be expressed as data without per-provider code.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-052.log`.
