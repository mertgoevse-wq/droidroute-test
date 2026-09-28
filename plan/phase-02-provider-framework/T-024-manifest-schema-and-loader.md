# T-024 — Provider manifest schema and loader

> Phase 02 · Provider framework · **Depends on:** T-005, T-022 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Turn providers into data: define the manifest schema, load and validate it at startup, and fail with actionable messages on bad input.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | serialization model with defaults, strict validation, typed errors |
| `provider-integration` | keep the schema honest against real provider requirements |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/manifest/ProviderManifest.kt` matching the schema in docs/03-providers.md
- `provider/manifest/ManifestLoader.kt` with per-field validation messages
- Five example manifests under `assets/providers/*.example.json` (placeholders only)

## Steps

1. Model every field from docs/03-providers.md, including `tier`, `auth`, `models_source`, `tags`, `quota`.
2. Validate: id pattern, https base URL (except loopback), known compat value, auth type known.
3. Reject unknown fields loudly instead of ignoring them — a typo must not silently disable a setting.
4. Write the examples with placeholder keys that the secrets preflight accepts.

## Acceptance criteria

- [ ] A malformed manifest produces a message naming the field and the reason
- [ ] An unknown field is reported, not ignored
- [ ] `scripts/preflight-secrets.sh` passes on the example manifests

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ManifestLoader*'
scripts/preflight-secrets.sh
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-024 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-024 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-024: Provider manifest schema and loader"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Providers are declarative data with a validated schema.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-024.log`.
