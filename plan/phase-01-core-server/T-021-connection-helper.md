# T-021 — Connection helper (URLs, snippets, QR)

> Phase 01 · Core server · **Depends on:** T-013, T-016 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Show the owner exactly what to paste into Claude Code and Freebuff, for the current port and auth mode, including a QR code for a LAN client.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-compose-ui` | screen with copy-to-clipboard actions and a QR rendering |
| `technical-writing` | snippets that are correct for each auth mode |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/connections/ConnectionHelperScreen.kt`
- Copyable snippets: env exports, `curl` health check, MCP client config

## Steps

1. Render the values from the live configuration, never from constants.
2. Include the auth header in the snippet only when auth is not `none`.
3. Provide a QR code for the LAN URL when the bind mode allows it.
4. Add a 'run this to verify' one-liner whose output the owner can paste back.

## Acceptance criteria

- [ ] Snippets match the running configuration (verified by changing the port and re-reading the screen)
- [ ] Every snippet copies to the clipboard with one tap
- [ ] The verification one-liner actually succeeds against the running server

## Verification

```bash
./gradlew :app:assembleDebug
curl -fsS http://127.0.0.1:8787/health
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-021 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-021 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-021: Connection helper (URLs, snippets, QR)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Connecting an agent is a copy-paste operation with no guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-021.log`.
