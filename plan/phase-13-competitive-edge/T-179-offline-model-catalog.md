# T-179 — Offline model catalog pack

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-110, T-111 · **Parallel-safe:** yes · **Est. agent time:** 150-300 min

## Goal

An own catalog that works with no internet: sizes, quants, licences, checksums, device-fit scores, and an optional signed update — so the owner can pick a model that fits this phone without visiting a website.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `local-inference` | accurate metadata per model family and realistic expectations on 8 GB |
| `droidroute-verification` | hash verification, tampered-pack rejection and the no-network path |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `assets/catalog/models.json` bundled and fully offline-usable
- A signed optional update pack with checksum verification and rollback to the bundled copy

## Steps

1. Define the catalog schema: id, family, parameters, quant, file size, context, licence, source URL, SHA-256.
2. Score each entry against this device's available RAM at read time, not at authoring time.
3. Verify a downloaded update pack against an embedded public key before accepting it.
4. Keep the bundled copy authoritative when no update is present or verification fails.

## Acceptance criteria

- [ ] The catalog is fully usable in airplane mode (verified with the radio off)
- [ ] A tampered update pack is rejected and the bundled catalog stays in force (asserted)
- [ ] Every entry names a licence and a checksum

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ModelCatalogPack*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-179 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-179 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-179: Offline model catalog pack"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Choosing a local model is a browsing experience that works offline and cannot be poisoned.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-179.log`.
