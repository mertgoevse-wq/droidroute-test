# T-180 — In-app updater with signature verification and rollback

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-144, T-009 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Always update-ready: check GitHub releases for a newer build, verify the APK signature against the expected signer, install through the system installer, and keep the previous build for rollback.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-platform` | package installer intents, version comparison and signature checking |
| `android-intent-security` | an updater is a remote-code path: signature verification is non-negotiable |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `update/UpdateChecker.kt` with channel selection (stable / pre-release), version comparison and release notes
- Signature verification against the pinned signing certificate, plus a rollback path to the kept previous APK

## Steps

1. Compare `versionCode` from the release metadata, never from a string comparison of tag names.
2. Verify the downloaded APK's signing certificate matches the pinned one before offering the install.
3. Show release notes and require an explicit install action; never install silently.
4. Keep the previous APK and offer a one-tap rollback with a warning about data compatibility.

## Acceptance criteria

- [ ] A newer release is detected and its signature verified before install (asserted with a fixture and a real run)
- [ ] A wrong-signature APK is refused with a clear message and never offered for install
- [ ] Rollback installs the kept previous build

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*UpdateChecker*'
gh release list --limit 3
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-180 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-180 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-180: In-app updater with signature verification and rollback"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The app updates itself from its own releases, with the integrity check that makes that safe.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-180.log`.
