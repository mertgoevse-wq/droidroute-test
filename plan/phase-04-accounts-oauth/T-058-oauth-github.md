# T-058 — GitHub account (Copilot / Models)

> Phase 04 · Accounts & OAuth · **Depends on:** T-055, T-051 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Connect a GitHub account via OAuth so Copilot- and Models-backed providers can use it without a pasted token.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `oauth-device-flow` | GitHub OAuth app setup and scope minimisation |
| `security-audit` | the account grants repository access — keep scopes minimal and document them |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/github-account.json` with `auth.type: oauth-github`
- Setup doc with the exact OAuth app settings and required scopes

## Steps

1. Request the minimum scopes needed for the models endpoint; avoid repository scopes entirely if possible.
2. Complete the flow and validate with a models call.
3. Document that the token is stored in the vault and revocable from GitHub's side.

## Acceptance criteria

- [ ] A live call succeeds through the OAuth account, or the blocker is documented
- [ ] No repository scope is requested unless proven necessary
- [ ] The setup doc names every scope and why it is needed

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*github*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-058 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-058 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-058: GitHub account (Copilot / Models)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

GitHub-backed models are reachable without a hand-pasted personal access token.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-058.log`.
