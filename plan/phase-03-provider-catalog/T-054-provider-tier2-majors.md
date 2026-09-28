# T-054 — Provider: Tier 2 majors batch

> Phase 03 · Provider catalog · **Depends on:** T-027, T-028, T-029 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Add manifests for the paid and subscription providers the owner may hold keys for: OpenAI, Anthropic, Gemini, xAI, DeepSeek, DashScope/Qwen, Together, Fireworks, DeepInfra, Novita, Hyperbolic, Nebius, SambaNova, Cohere, AI21, Scaleway, Chutes, Kluster.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | confirm each base URL from its own documentation; batch the work but verify each |
| `testing` | one fixture per provider family plus a sweep test asserting every manifest loads |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- One manifest per provider in `assets/providers/`
- A test that loads every shipped manifest and asserts it validates

## Steps

1. Work in batches of four providers; confirm each base URL and auth style before writing its manifest.
2. Mark providers whose details could not be confirmed as `draft: true` and keep them disabled by default.
3. Add each entry to the docs/03-providers.md table in the same commit.
4. Run the sweep test so a typo in any manifest fails the build.

## Acceptance criteria

- [ ] `tools/check_providers.py` passes with the docs in sync
- [ ] Every manifest validates; unconfirmed ones are marked draft and disabled
- [ ] No base URL was copied from another manifest without confirmation

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ManifestSweep*'
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-054 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-054 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-054: Provider: Tier 2 majors batch"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The provider catalogue is broad, validated and honest about what is unconfirmed.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-054.log`.
