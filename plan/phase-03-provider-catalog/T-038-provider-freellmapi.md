# T-038 — Provider: FreeLLMAPI

> Phase 03 · Provider catalog · **Depends on:** T-027, T-031 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Support the self-hosted FreeLLMAPI instance that pools many free provider tiers behind one endpoint.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | self-hosted base URL configuration and its onboarding flow |
| `technical-writing` | the Termux/Debian steps to run the instance locally |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/freellmapi.json` with a loopback default base URL
- `docs/providers/freellmapi.md` — how to run it, where its keys live, how to verify it

## Steps

1. Read the provider's current documentation; do not reuse the URL from any other source. Record the default local port and the path prefix it serves.
2. Allow an http:// loopback base URL (the manifest validator already permits loopback).
3. Document that its upstream keys are managed by the FreeLLMAPI instance, not by DroidRoute.
4. Validate with a models call against a running instance, or log that none was reachable.

## Acceptance criteria

- [ ] A loopback base URL is accepted while remote plaintext http is still rejected
- [ ] The doc explains the split of responsibilities between DroidRoute and FreeLLMAPI
- [ ] Validation either succeeds or records the exact reason it could not run

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-038 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-038 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-038: Provider: FreeLLMAPI"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The free-tier aggregator is usable as a normal provider.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-038.log`.
