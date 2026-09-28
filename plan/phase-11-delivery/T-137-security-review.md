# T-137 — Security review against docs/05-security.md

> Phase 11 · Delivery · **Depends on:** T-099, T-120, T-112 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Verify every security claim in the documentation is true in the code, and fix what is not.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `security-audit` | adversarial review: assume each control is broken until proven otherwise |
| `testing` | turn each verified control into an automated assertion |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A control-by-control review table committed to the component status file
- Automated assertions for the redaction canary, auth floor, key masking and admin auth

## Steps

1. Walk each claim in docs/05-security.md and find its enforcing code path.
2. Attempt to break: unauthenticated admin call, non-local bind without a key, key leak into a log, key in an exported file.
3. Where a claim is not enforced, either enforce it or correct the documentation — never leave a false claim.
4. Add a test per control so a regression is caught.

## Acceptance criteria

- [ ] Every documented control has an enforcing test
- [ ] Each attempted break failed, or was fixed in this task
- [ ] No documentation claim is left unverified

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Security*'
scripts/preflight-secrets.sh
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-137 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-137 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-137: Security review against docs/05-security.md"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The security documentation is verified against behaviour, control by control.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-137.log`.
