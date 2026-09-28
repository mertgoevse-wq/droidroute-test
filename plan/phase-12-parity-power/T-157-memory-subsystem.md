# T-157 — Memory subsystem (opt-in, local)

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-066, T-006 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Optional project memory: store reusable facts and decisions locally, retrieve them into prompts, and allow a per-request off switch.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ai-governors` | memory is user data: consent, transparency, deletion and control |
| `droidroute-verification` | isolation tests: memory never leaks between client keys, and off means off |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `memory/` store with an on/off setting (default off), per-request opt-out and a delete-everything action
- Documented retrieval rule stating exactly what may be injected and when

## Steps

1. Store entries locally with a type (fact, preference, decision) and a decay policy.
2. Inject only when the request opts in and never silently for unrelated clients.
3. Implement and test the off switch as a hard gate, not a default-value convention.
4. Document the privacy boundary in docs/05-security.md and the German glossary.

## Acceptance criteria

- [ ] Memory is off by default and a request with the opt-out flag never receives injected content (asserted)
- [ ] Delete-everything removes all entries and is logged
- [ ] The retrieval rule in the docs matches the implementation

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Memory*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-157 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-157 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-157: Memory subsystem (opt-in, local)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Memory exists as a controlled feature with a stated boundary, not an invisible side channel.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-157.log`.
