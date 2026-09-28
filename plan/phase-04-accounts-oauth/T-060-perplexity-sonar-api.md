# T-060 — Perplexity Sonar through the official API

> Phase 04 · Accounts & OAuth · **Depends on:** T-027, T-029 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Implement the supported path: the Perplexity API key with the Sonar model family, search-mode fields, and citations preserved in the response.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | Sonar model names and the search-specific request fields |
| `testing` | fixtures that include a citations array |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/perplexity.json` with base `https://api.perplexity.ai` and models `sonar`, `sonar-pro`, `sonar-reasoning`, `sonar-deep-research`
- `search_mode` handling adding `search_recency_filter`, `search_domain_filter`, `return_citations`

## Steps

1. Extend the OpenAI-compatible adapter with an opt-in `search_mode` that adds the search fields.
2. Preserve `citations` in the normalised response instead of dropping unknown fields.
3. Record which Sonar models the owner's key can actually reach.

## Acceptance criteria

- [ ] A real Sonar call returns an answer with a non-empty citations array, or the blocker is logged
- [ ] `search_mode` is opt-in and never applied to non-search models
- [ ] Citations survive the normalisation step (asserted in a test)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*perplexity*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-060 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-060 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-060: Perplexity Sonar through the official API"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Perplexity search works through the supported API, with citations intact.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-060.log`.
