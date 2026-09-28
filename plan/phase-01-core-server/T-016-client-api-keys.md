# T-016 — Client API key generation, hashing and revocation

> Phase 01 · Core server · **Depends on:** T-015, T-006 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Let the owner mint named client keys (`dr_…`), stored hashed, individually revocable, with last-used tracking.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `security-audit` | salted hashing, one-time display, no plaintext retention |
| `persistence-room` | Room entity + DAO for client keys and their usage timestamps |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `store/ClientKeyEntity.kt` + DAO (name, salt, hash, created, lastUsed, revoked)
- `server/ClientKeyService.kt` — mint (returns plaintext once), verify, revoke, list

## Steps

1. Generate `dr_` + 32 random characters using a cryptographically secure source.
2. Store salt + SHA-256 hash only; return the plaintext exactly once from the mint call.
3. Update `lastUsed` at most once per minute per key to avoid write amplification.
4. Revocation takes effect immediately for new requests and is logged with the key name, never the value.

## Acceptance criteria

- [ ] The plaintext key is returned once and is unrecoverable afterwards
- [ ] A revoked key is rejected while other keys keep working
- [ ] `lastUsed` updates are visible in the UI within a minute of use

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ClientKey*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-016 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-016 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-016: Client API key generation, hashing and revocation"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Client authentication is per-machine and per-agent, revocable without restarting the server.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-016.log`.
