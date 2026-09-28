# T-167 — Automatic provider detection from any URL

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-024, T-029, T-033 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Turn 'any possible provider' into one paste: probe an endpoint, infer whether it speaks OpenAI, Anthropic, Gemini or the OpenAI Responses shape, discover its models, and generate a validated manifest the owner can review.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-provider-manifest` | the probe order, the signals per dialect, and what must be confirmed by a human |
| `droidroute-verification` | probe tests against four local stub servers in the four dialects, plus hostile inputs |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/detect/ProviderProbe.kt` — dialect inference, model discovery, capability sniffing
- A review screen showing the generated manifest with each inferred field marked inferred vs confirmed

## Steps

1. Probe in a fixed order: `/models`, then a one-token chat call per dialect, then an Anthropic `/v1/messages` probe.
2. Infer the dialect from the response shape, not from the URL string — never guess from a domain name.
3. Mark every inferred field as inferred; require the owner to confirm before the provider is enabled.
4. Refuse to save a manifest whose endpoints returned 404 for every probe, and say which paths were tried.

## Acceptance criteria

- [ ] Each of the four stub dialects is detected correctly (asserted)
- [ ] An endpoint that answers nothing produces a failure listing every probed path
- [ ] No provider is enabled without a confirmed base URL and at least one successful call

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ProviderProbe*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-167 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-167 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-167: Automatic provider detection from any URL"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Adding an unknown provider is one paste plus one confirmation instead of reading documentation for an hour.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-167.log`.
