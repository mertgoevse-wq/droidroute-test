# T-118 — MCP configuration discovery

> Phase 09 · MCP & plugins · **Depends on:** T-107 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Read the MCP configuration of Claude Code, Freebuff/Codex-style tools and Cursor-style projects, tolerating format differences.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `mcp-protocol` | the real configuration shapes of each host tool |
| `security-audit` | configuration files contain environment secrets — read names, never values |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `mcp/Discovery.kt` covering the paths listed in docs/07-mcp-plugins.md
- A tolerant parser that reports 'unknown format' with the file and line instead of dropping a server

## Steps

1. Read each candidate path through the Termux bridge (or shared storage where accessible).
2. Parse both JSON and TOML shapes; extract id, transport, command/url, env key names, enabled state.
3. Never copy an environment value into DroidRoute's storage — names only.
4. Report per-file results so a missing file is distinguishable from a parse failure.

## Acceptance criteria

- [ ] Servers from at least two different host formats are discovered
- [ ] A malformed file produces a specific error naming the file and the reason
- [ ] No environment value is copied (asserted with a canary value in a fixture)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Discovery*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-118 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-118 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-118: MCP configuration discovery"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Existing MCP servers are found from where they already live.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-118.log`.
