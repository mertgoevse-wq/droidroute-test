# T-169 — Local-first and no-auth providers, with fail-closed semantics

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-025, T-027, T-031, T-113 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Support no-auth free providers and self-hosted endpoints (STT, TTS, embeddings, llama-server, vLLM), and make the rule explicit: a local provider never silently falls back to a cloud provider.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-provider-manifest` | self-hosted endpoint shapes and the base-URL pitfalls that break them |
| `droidroute-verification` | fail-closed tests: a misconfigured local provider must error, never reroute to a cloud host |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Provider category `local` with a required base URL and no cloud fallback
- No-auth provider support: auth type `none`, model auto-fetch, one-click connect without a key

## Steps

1. Model `local` providers so a missing base URL is a configuration error, not a default endpoint.
2. Implement no-auth providers with discovery only and a clear warning that they are third-party free tiers.
3. Extend the candidate selector so a `local` provider is never replaced by a cloud candidate without the owner's policy saying so.
4. Test: a local provider with a broken URL fails the request and names the misconfiguration.

## Acceptance criteria

- [ ] A local provider with a missing or wrong base URL errors and never calls a cloud host (asserted)
- [ ] A no-auth provider connects and lists models without a key
- [ ] The self-hosted path is documented with the exact URL conventions that work

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*LocalFirst*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-169 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-169 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-169: Local-first and no-auth providers, with fail-closed semantics"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Local inference is respected, and a typo cannot quietly send the owner's text to a third party.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-169.log`.
