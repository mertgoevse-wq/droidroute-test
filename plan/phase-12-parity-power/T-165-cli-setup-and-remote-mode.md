# T-165 — CLI setup helpers and remote mode with scoped tokens

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-016, T-021, T-022 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Make connecting a client one command, and make a remote DroidRoute instance reachable with narrow tokens instead of full access.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-provider-manifest` | the connection details each client actually needs |
| `android-intent-security` | scoped tokens must be strictly narrower than the main key |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `scripts/setup-client.sh` supporting Claude Code, Freebuff/Codex-style, Gemini CLI and generic OpenAI clients
- Scoped tokens: read-only, model-restricted, budget-capped, expiring

## Steps

1. Generate the exact environment exports per client from the live configuration, never from constants.
2. Implement scoped tokens with a documented capability list and a hard expiry.
3. Test that a read-only token cannot perform an admin action or call a model outside its list.
4. Document the remote-mode flow for the tailnet and tunnel cases from docs/11-tbc-resolutions.md.

## Acceptance criteria

- [ ] One command configures each supported client and the result works
- [ ] A scoped token is refused outside its scope (asserted per scope type)
- [ ] Scoped tokens expire and cannot be extended by the holder

## Verification

```bash
bash scripts/setup-client.sh --client claude-code --dry-run
./gradlew :app:testDebugUnitTest --tests '*ScopedToken*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-165 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-165 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-165: CLI setup helpers and remote mode with scoped tokens"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Connecting a client is one command, and remote access never needs the master key.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-165.log`.
