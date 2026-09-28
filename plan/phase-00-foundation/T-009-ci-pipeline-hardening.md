# T-009 — CI pipeline hardening

> Phase 00 · Foundation · **Depends on:** T-003 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Make the workflows dependable: Gradle caching, artifact retention, scaffold gating that disappears automatically once the project exists, and documented signing secrets.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ci-cd-github-actions` | workflow logic, caching, artifact and release steps |
| `security-audit` | confirm no secret is echoed and signing inputs come only from secrets |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Updated `.github/workflows/build-apk.yml` with caching and honest gating
- `docs/signing.md` — which repository secrets must exist before the first `v*` tag

## Steps

1. Enable Gradle caching and pin action versions.
2. Verify the release job fails loudly when signing secrets are absent (it must not produce an unsigned release).
3. Confirm the workflow never prints an environment variable that could contain a secret.
4. Record the required secret names in docs/signing.md, including how to generate the keystore base64.

## Acceptance criteria

- [ ] A push produces a green `verify` job and an `apk-debug` artifact
- [ ] Removing a signing secret makes the release job fail with an explicit message
- [ ] `docs/signing.md` names every required secret

## Verification

```bash
gh run list --workflow=build-apk.yml --limit 3
gh secret list
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-009 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-009 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-009: CI pipeline hardening"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

CI is trustworthy: it fails when it should and never publishes an unsigned release.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-009.log`.
