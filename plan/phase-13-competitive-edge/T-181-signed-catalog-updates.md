# T-181 — Catalog updates without an app release

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-164, T-180 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Provider knowledge and model lists change weekly — update them between releases with signed packs, verified against an embedded key, with the bundled copy as the offline fallback.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-provider-manifest` | which catalog fields are safe to update remotely and which are not |
| `droidroute-verification` | tampered pack, stale pack, missing key and offline-fallback tests |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `catalog/` pack format covering provider manifests and model lists, signed by the owner's key
- A documented update policy: check interval, offline behaviour, and how a bad pack is rolled back

## Steps

1. Define the pack format and what it may change; never let a pack add executable code or a credential.
2. Verify signature and freshness before applying; keep the previous state for one-step rollback.
3. Apply atomically: a partially applied pack must not be possible.
4. Document, for the owner, exactly how to publish a pack.

## Acceptance criteria

- [ ] A valid pack updates providers without an app update (demonstrated once)
- [ ] A tampered or expired pack is rejected and the previous state stays in force (asserted)
- [ ] A pack can never introduce credentials or code (asserted by schema validation)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*CatalogPack*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-181 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-181 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-181: Catalog updates without an app release"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The app stays current between releases without becoming a remote-code channel.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-181.log`.
