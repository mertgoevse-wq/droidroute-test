# T-006 — Key vault (Keystore, AES-256-GCM)

> Phase 00 · Foundation · **Depends on:** T-005 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Implement the secret store described in docs/05-security.md: AES-256-GCM with a Keystore-wrapped key, per-record IV, one-time reveal, and the fixed mask format.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `security-audit` | review the crypto usage: key wrapping, IV uniqueness, no plaintext fallback path |
| `testing` | round-trip, tamper detection, mask format and canary tests |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `vault/KeyVault.kt` — put/get/delete/revealOnce, ciphertext persisted in app-private storage
- `vault/Masking.kt` — `first5••••last5` with the documented short-key rule
- Unit tests including a corrupted-ciphertext case and a canary that must never appear in output

## Steps

1. Generate or unwrap the AES key via Android Keystore with GCM and no user-authentication requirement.
2. Store ciphertext + IV + version per record; never a plaintext copy, never a deterministic IV.
3. Implement masking exactly as documented (5 visible at each end, `••••` for anything over 12 characters).
4. Implement `revealOnce` state tracking so the plaintext is surfaced once at entry time.
5. Write the canary test: a known key value must not appear in any log record the vault produces.

## Acceptance criteria

- [ ] Round-trip test passes; a modified ciphertext byte causes a decryption failure rather than silent garbage
- [ ] Masking never exposes more than 5 characters from either end
- [ ] Canary test passes (key value absent from all log output)
- [ ] No plaintext secret is written anywhere outside the in-memory result of `revealOnce`

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*KeyVault*'
./gradlew :app:testDebugUnitTest --tests '*Masking*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-006 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-006 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-006: Key vault (Keystore, AES-256-GCM)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Secrets can be stored and retrieved safely; every later storage of a credential goes through this API.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-006.log`.
