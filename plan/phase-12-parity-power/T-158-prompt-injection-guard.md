# T-158 — Prompt-injection guard

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-066, T-077 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Screen inbound content for instruction-injection patterns on every LLM route, without pretending the heuristics are perfect.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ai-governors` | how to warn and block proportionately instead of silently mangling user content |
| `droidroute-verification` | a red-team corpus: tool-result injection, role confusion, delimiter escape |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/guard/InjectionGuard.kt` with a documented pattern set and an action per severity
- A red-team test corpus stored as fixtures and run in the suite

## Steps

1. Detect patterns in untrusted positions (tool results, retrieved documents) rather than in the owner's own text.
2. Choose per severity: annotate, warn in the response, or refuse — never silently rewrite the content.
3. Document the limits honestly: this reduces risk, it does not eliminate it.
4. Run the red-team fixtures and record the detection rate.

## Acceptance criteria

- [ ] Every fixture in the red-team corpus produces the documented action
- [ ] Owner-authored text is not modified (asserted with a control fixture)
- [ ] The scope and limits are documented without overstating the protection

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*InjectionGuard*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-158 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-158 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-158: Prompt-injection guard"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Injection attempts in untrusted content are handled proportionately and measurably.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-158.log`.
