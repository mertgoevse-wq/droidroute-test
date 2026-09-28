# T-183 — Config portability by QR code (no cloud)

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-034, T-006 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Move a full configuration to a new phone by scanning a QR code, with secrets encrypted under a passphrase — no account, no cloud, no copy of the keys anywhere else.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-intent-security` | the export is the highest-value artefact in the app; treat its encryption as the feature |
| `droidroute-verification` | wrong-passphrase, tampered-bundle, oversized-bundle and round-trip tests |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `transfer/QrBundle.kt` — encrypted bundle, chunked into scannable QR frames
- An import flow that verifies the bundle before applying and never partially applies it

## Steps

1. Encrypt the bundle with a key derived from a passphrase using a documented KDF and parameters.
2. Chunk the ciphertext into QR frames with an index and a checksum; the scanning phone reassembles and verifies.
3. Apply atomically and refuse a bundle whose checksum or version does not match.
4. Document what the bundle contains and what it deliberately excludes.

## Acceptance criteria

- [ ] A full configuration transfers between two app instances via QR (demonstrated once)
- [ ] A wrong passphrase and a tampered frame both fail cleanly without partial application (asserted)
- [ ] No cloud service or account is involved (verified by inspecting the network calls during transfer)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*QrBundle*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-183 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-183 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-183: Config portability by QR code (no cloud)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Device migration is local, encrypted and account-free — unlike the cloud sync competitors offer.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-183.log`.
