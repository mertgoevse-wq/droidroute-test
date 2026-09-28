# T-102 — Settings: server, access and client keys

> Phase 07 · UI · **Depends on:** T-013, T-014, T-016, T-021 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Own the server configuration from the app: port, bind mode, auth mode, client keys, and the connection helper.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | settings that show the consequence of a choice before it is applied |
| `security-audit` | the auth-floor warning must be unmissable and un-bypassable |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/settings/ServerSettingsScreen.kt`
- Client key management (create, name, revoke, last used)

## Steps

1. Change the port with live validation and a clear note that agents must be re-pointed.
2. Change the bind mode with the auth consequence stated inline; require the explicit consent checkbox for external.
3. Manage client keys with the plaintext returned exactly once.
4. Link to the connection helper with values matching the current configuration.

## Acceptance criteria

- [ ] Port and bind changes apply without a full restart (via the rebind path)
- [ ] External mode cannot be enabled without the consent checkbox
- [ ] A new client key is shown once and appears masked afterwards

## Verification

```bash
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-102 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-102 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-102: Settings: server, access and client keys"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

All server access configuration lives in one place with its consequences stated.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-102.log`.
