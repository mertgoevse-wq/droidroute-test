# T-148 — Combo engine and virtual auto models

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-083, T-084, T-089 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Implement combos — named chains of `(provider, model)` steps routed across automatically — and the virtual models `auto`, `auto/coding`, `auto/fast`, `auto/cheap`, `auto/offline`, `auto/smart`, `auto/lkgp`.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | combo semantics, step ordering, and how a combo differs from an alias |
| `droidroute-verification` | virtual-model behaviour tests, including an exhausted-first-step case |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `routing/combo/ComboEngine.kt` and the virtual auto models with their scoring presets
- Combo pins at the top of `/v1/models`, and `/v1/routing/explain` shows the resolved step

## Steps

1. Model a combo as ordered steps with per-step strategy overrides and a failure policy.
2. Implement the virtual presets from documentation, not from intuition: each one names its optimisation target.
3. Preserve last-known-good stickiness for `auto/lkgp` and keep `auto/chaos` explicitly experimental.
4. Test: first step exhausted → second answers; all steps failing → one error naming every step.

## Acceptance criteria

- [ ] A requested virtual model resolves to a documented, explainable step
- [ ] Quota exhaustion moves the combo to the next step without a client-visible failure
- [ ] `auto/lkgp` reuses the last successful step when it is healthy (asserted)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Combo*'
curl -fsS 'http://127.0.0.1:8787/v1/routing/explain?model=auto/fast'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-148 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-148 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-148: Combo engine and virtual auto models"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The flagship OmniRoute capability — combos and zero-config auto models — is available.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-148.log`.
