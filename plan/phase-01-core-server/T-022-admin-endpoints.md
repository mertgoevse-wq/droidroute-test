# T-022 — Admin endpoints and reload path

> Phase 01 · Core server · **Depends on:** T-017, T-018 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Provide `/v1/providers` and `/admin/reload` so tooling (and the owner) can inspect and refresh configuration without restarting the app.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ktor-server` | route design, key-protected admin surface |
| `security-audit` | admin routes must never expose key material or bypass the gate |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/routes/AdminRoutes.kt` — `/v1/providers`, `/admin/reload`, `/v1/usage` skeleton
- Admin routes require api-key auth in every bind mode

## Steps

1. Serve the provider registry without secrets (id, name, tier, enabled, status).
2. Implement reload: re-read manifests and settings, keep the socket open.
3. Require api-key auth for admin routes even in local mode.
4. Return a structured result naming what changed.

## Acceptance criteria

- [ ] `/v1/providers` lists providers with no key material present
- [ ] `/admin/reload` picks up a manifest change without a restart
- [ ] Admin routes reject an unauthenticated request in every bind mode

## Verification

```bash
curl -fsS http://127.0.0.1:8787/v1/providers
./gradlew :app:testDebugUnitTest --tests '*AdminRoutes*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-022 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-022 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-022: Admin endpoints and reload path"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Configuration is inspectable and reloadable at runtime, under auth, with no secret exposure.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-022.log`.
