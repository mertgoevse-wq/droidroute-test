# T-119 — Aggregated MCP registry with change watching

> Phase 09 · MCP & plugins · **Depends on:** T-118, T-005 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Merge discovered servers into one registry with source precedence, and refresh when a watched file changes.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `mcp-protocol` | precedence rules and id collision handling |
| `kotlin-core` | file watching without busy looping or draining battery |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `mcp/Registry.kt` writing `~/.droidroute/mcp.registry.json`
- Precedence: bundled defaults < host configs < owner-defined entries

## Steps

1. Merge with deterministic precedence and record the source of every entry.
2. Watch the configuration files with a debounce so a burst of writes causes one refresh.
3. Keep owner-defined entries when a host config disappears.
4. Write the registry atomically so a crash cannot leave a truncated file.

## Acceptance criteria

- [ ] Owner-defined entries override host entries with the same id
- [ ] Editing a host configuration refreshes the registry within a few seconds
- [ ] The registry file is never left partially written (asserted by writing under fault injection)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Registry*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-119 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-119 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-119: Aggregated MCP registry with change watching"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

One registry is the single truth about which MCP servers exist.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-119.log`.
