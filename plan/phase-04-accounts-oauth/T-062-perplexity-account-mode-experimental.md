# T-062 — Perplexity account mode (experimental, off by default)

> Phase 04 · Accounts & OAuth · **Depends on:** T-060 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Honour the owner's request to explore using the Pro subscription directly, while keeping it strictly opt-in, clearly labelled, and never used automatically by routing.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `security-audit` | session material is equivalent to a password — store it like one and document the risk |
| `provider-integration` | assess honestly whether the web session can be driven at all |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/experimental/SessionAccountAdapter.kt` behind `settings.experimentalAccountMode`
- A warning screen stating what this is, what it is not, and what can break

## Steps

1. Assess the approach and document the finding: is a session-driven call technically feasible and stable?
2. If it is not feasible, record that decision in status/DECISIONS.md and stop — do not ship a fake path.
3. If it is, implement it behind the flag with session material in the vault and mandatory owner confirmation.
4. Never place this adapter in the automatic routing candidate list.

## Acceptance criteria

- [ ] The feature is off by default and reachable only after an explicit, informed confirmation
- [ ] Routing never selects it automatically (asserted by a test)
- [ ] Either a working path or a documented negative finding exists — no half-implementation

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*SessionAccount*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-062 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-062 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-062: Perplexity account mode (experimental, off by default)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The experimental account mode exists as a labelled, opt-in risk — or as a documented 'not feasible' finding.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-062.log`.
