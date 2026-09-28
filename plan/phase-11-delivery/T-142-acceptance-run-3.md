# T-142 — Acceptance run A7–A9 (local models, MCP, repository)

> Phase 11 · Delivery · **Depends on:** T-141 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Prove criteria A7 to A9: local inference, MCP federation, and the repository's own integrity.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | run the criteria literally, including the memory-warning case |
| `mcp-protocol` | verify the discovered server list against the host's own configuration |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Evidence entries for A7, A8 and A9

## Steps

1. A7: load a model at or under 4 GB, get a completion, then attempt an oversized model and capture the warning.
2. A8: compare `/mcp/servers` with the host configuration and call one tool end to end.
3. A9: confirm the repository is private, has ≥135 task files, and one commit per completed task.
4. Attach the screenshots A7 and A3 require.

## Acceptance criteria

- [ ] A7, A8 and A9 are ticked with evidence
- [ ] The MCP list matches the host configuration entry by entry
- [ ] The repository checks are run as commands, not asserted from memory

## Verification

```bash
gh repo view --json isPrivate,name
find plan -name 'T-*.md' | wc -l
git log --oneline | head -20
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-142 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-142 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-142: Acceptance run A7–A9 (local models, MCP, repository)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Local models, MCP and repository integrity are proven together.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-142.log`.
