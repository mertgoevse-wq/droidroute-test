# T-079 — Candidate resolution and canonical model ids

> Phase 06 · Routing · **Depends on:** T-029, T-025 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Turn a requested model name into an ordered candidate list of `(provider, model)` pairs, deterministically.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | resolution rules and canonical id format |
| `testing` | resolution table tests including ambiguous and unknown names |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/CandidateResolver.kt`
- Canonical id rule implemented: `provider/model`, with bare names resolved through aliases

## Steps

1. Resolve `provider/model` exactly; reject a disabled provider with a clear reason.
2. Resolve a bare model name across every provider offering it, then order by the active strategy.
3. Return an empty list with a reason (not an exception) when nothing matches, so the error mapper can shape it.
4. Keep resolution pure and side-effect free so it is trivially testable.

## Acceptance criteria

- [ ] Resolution is deterministic for identical inputs (asserted by repeated calls in a test)
- [ ] An unknown model produces a `no_candidate` reason naming the model
- [ ] An ambiguous bare name resolves across all providers, not just the first

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*CandidateResolver*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-079 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-079 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-079: Candidate resolution and canonical model ids"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Every request has a defined candidate list before any network call happens.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-079.log`.
