# T-006 — Key vault (Keystore, AES-256-GCM)

> Phase 00 · Foundation · **Depends on:** T-005 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Implement the secret store described in docs/05-security.md: AES-256-GCM with a Keystore-wrapped key, per-record IV, one-time reveal, and the fixed mask format.

## Read first (context budget)

- [`status/NEXT.md`](../../status/NEXT.md) — the next task and the pre-flight commands
- [`status/ERRORS.md`](../../status/ERRORS.md) — must have no open entry for this task
- [`handbooks/09-skill-resolution.md`](../../handbooks/09-skill-resolution.md) — what each skill label below means on this machine
- [`docs/11-tbc-resolutions.md`](../../docs/11-tbc-resolutions.md) — decisions already settled; not re-opened
- this file, top to bottom, plus the *Acceptance criteria* of every `Depends on` task

Do not read the rest of the plan to "get oriented" — the entry point is this file plus the documents linked here. If the work genuinely needs another document, read that one and nothing more.

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

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-006.log`)
- [ ] No placeholder, no invented endpoint/URL/model/field, no edit outside the files this task names
- [ ] Nothing was weakened to make a check pass (no deleted test, no raised threshold, no disabled rule)
- [ ] `status/PROGRESS.md` and `status/NEXT.md` updated in the same commit as the work
- [ ] `scripts/preflight-secrets.sh` clean
- [ ] UI work only: `python3 tools/check_design_slop.py` passes and the four craft tests ran ([docs/14-design-system.md](../../docs/14-design-system.md) §11)

## Rules that always apply

- Prohibitions and the quality bar: [handbooks/07-anti-slop-rules.md](../../handbooks/07-anti-slop-rules.md) (placeholders, invented endpoints, unrequested scope, weakened checks)
- At least two skills **in parallel** as subagents, one of them verification: [AGENTS.md](../../AGENTS.md) §4
- Log every meaningful step, commit and push exactly once for this task: [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md) · [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md)
- No secret in the repository, ever: `scripts/preflight-secrets.sh` must pass
- A new dependency, a deviation, or a settled decision goes into [status/DECISIONS.md](../../status/DECISIONS.md) in the same commit
- Missing tool for the job? Search before improvising: [handbooks/08-tooling-discovery.md](../../handbooks/08-tooling-discovery.md)

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-006 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-006 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-006: Key vault (Keystore, AES-256-GCM)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Secrets can be stored and retrieved safely; every later storage of a credential goes through this API.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-006.log`.
