# T-040 — Provider: GoRouter

> Phase 03 · Provider catalog · **Depends on:** T-027, T-028, T-031 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Connect GoRouter, which offers both an OpenAI-compatible and an Anthropic-compatible surface.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | two surfaces from one account — one provider, two manifests or one dual manifest |
| `testing` | call both surfaces and assert consistent behaviour |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/gorouter.json` declaring both surfaces
- Decision record if the dual-surface shape needs an extension to the manifest schema

## Steps

1. Read the provider's current documentation; do not reuse the URL from any other source. Confirm both endpoint paths and whether one key covers both.
2. If two surfaces are needed, register them as `gorouter` and `gorouter-anthropic` with a shared account note.
3. Validate both with a live call and record latency for each.

## Acceptance criteria

- [ ] Both surfaces work or the unusable one is explicitly disabled with a reason
- [ ] The routing engine can use either surface for the same logical model
- [ ] Latency of both is recorded in the task log

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*gorouter*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-040 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-040 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-040: Provider: GoRouter"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A dual-surface gateway is fully available to both protocol families.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-040.log`.
