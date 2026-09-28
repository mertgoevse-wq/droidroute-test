# T-103 — Settings: tunnel checklists and Termux permission

> Phase 07 · UI · **Depends on:** T-091, T-021, T-014 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Give the owner the two access-extension paths: a tunnel checklist for LAN and external use, and the Termux RUN_COMMAND permission request with an accurate statement of what is and is not available.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-platform` | requesting the Termux RUN_COMMAND permission and detecting its absence |
| `technical-writing` | tunnel setup steps that match each provider's current documentation |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/settings/IntegrationsScreen.kt`
- Tunnel checklists for Tailscale and Cloudflare Tunnel with a live reachability check
- Termux availability and permission state, with the degraded path explained

## Steps

1. Detect whether Termux and its permission are available; state the degraded path when they are not.
2. Show the tunnel checklist with a verification step the owner can run and paste back.
3. Show the current external URL when a tunnel is detected.
4. Never enable an external bind as a side effect of enabling a tunnel — keep the two decisions separate.

## Acceptance criteria

- [ ] The screen states accurately whether Termux and its permission are available
- [ ] The tunnel checklist ends with a verification that actually proves reachability
- [ ] Enabling a tunnel does not silently change the bind mode

## Verification

```bash
./gradlew :app:assembleDebug
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-103 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-103 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-103: Settings: tunnel checklists and Termux permission"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Integrations are enabled with proof, not with hope.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-103.log`.
