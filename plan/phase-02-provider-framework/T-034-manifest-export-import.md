# T-034 — Manifest export and import without secrets

> Phase 02 · Provider framework · **Depends on:** T-033 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Export provider definitions (including custom ones) to share or re-import on a new device, and prove no secret travels with them.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `security-audit` | prove the export cannot contain key material |
| `technical-writing` | document the export format and the import precedence |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/ManifestExchange.kt` — export to a file, import with conflict handling
- Documented precedence: imported manifest < owner override < manual edit

## Steps

1. Serialise only manifest fields; never the vault reference, never a masked key.
2. On import, report conflicts (same id, different base URL) and require a decision.
3. Test with a canary: export a provider that has a key and assert the key string is absent.
4. Document the flow in docs/03-providers.md and the German glossary if a new term appears.

## Acceptance criteria

- [ ] An exported file imports on a fresh database and reproduces the provider
- [ ] Canary test passes: the key value is absent from the export
- [ ] Conflicting ids are surfaced, never silently overwritten

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ManifestExchange*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-034 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-034 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-034: Manifest export and import without secrets"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Provider configuration is portable; secrets are not.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-034.log`.
