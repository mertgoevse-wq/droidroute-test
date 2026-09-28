# T-144 — Release pipeline and first tagged release

> Phase 11 · Delivery · **Depends on:** T-143 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Cut the first real release: signing configured, workflow verified, artifacts and checksums published.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ci-cd-github-actions` | tag → build → sign → release, with a rollback path |
| `security-audit` | confirm signing material is only in repository secrets and never logged |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A `v0.1.0` release with APK and SHA256SUMS
- CHANGELOG entry for the release

## Steps

1. Confirm the signing secrets exist and that the workflow refuses to build without them.
2. Tag the release through `scripts/step-commit.sh --tag`.
3. Verify the published artifact's checksum against a local download.
4. Record how to roll back to the previous APK.

## Acceptance criteria

- [ ] The release exists with an installable signed APK and a checksum file
- [ ] The checksum of the downloaded file matches
- [ ] No signing material appears in any log or artifact

## Verification

```bash
gh release view v0.1.0
gh release download v0.1.0 --pattern '*.apk' -D /tmp/droidroute-release && sha256sum /tmp/droidroute-release/*.apk
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-144 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-144 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-144: Release pipeline and first tagged release"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

DroidRoute has shipped a verifiable release, built by CI from a tagged commit.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-144.log`.
