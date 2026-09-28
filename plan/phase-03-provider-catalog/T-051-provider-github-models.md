# T-051 — Provider: GitHub Models

> Phase 03 · Provider catalog · **Depends on:** T-027, T-030 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Connect GitHub Models using a GitHub token, reusing the OAuth work where a token is already available.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `provider-integration` | token requirements and the models endpoint |
| `security-audit` | a GitHub token is powerful — store it in the vault and scope it minimally |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/providers/github-models.json` with base `https://models.inference.ai.azure.com`
- A note in docs/05-security.md about the minimum token scope this provider needs

## Steps

1. Register the provider expecting a fine-grained token, not a broad personal access token.
2. Validate with a models call and record the model list.
3. Document the scope requirement and the reason.

## Acceptance criteria

- [ ] The provider validates with a minimally scoped token
- [ ] The token is stored only in the vault
- [ ] The required scope is documented

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-051 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-051 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-051: Provider: GitHub Models"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

GitHub-hosted models are available without a wide-scoped credential.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-051.log`.
