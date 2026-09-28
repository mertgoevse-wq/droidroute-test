# T-126 — MCP documentation and owner guide

> Phase 09 · MCP & plugins · **Depends on:** T-125 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Document, in the owner's language as well, how MCP servers are discovered, what the app does with them, and how to add one permanently.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `technical-writing` | accurate, complete, no filler |
| `mcp-protocol` | verify every claim against the implementation |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `docs/07-mcp-plugins.md` finalised against the implementation
- German summary entries in docs/glossary-de.md for any new term

## Steps

1. Walk through each documented behaviour and verify it matches the code.
2. Add the 'how to add a server permanently' recipe with a worked example.
3. Document the degraded behaviour when Termux is unavailable.

## Acceptance criteria

- [ ] Every statement in the doc is verifiable in the implementation
- [ ] The recipe produces a working server when followed literally
- [ ] No term appears in the doc that the glossary does not explain

## Verification

```bash
python3 tools/check_links.py
./gradlew :app:testDebugUnitTest --tests '*mcp*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-126 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-126 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-126: MCP documentation and owner guide"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

MCP usage is documented for both an agent and the owner, and the doc is true.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-126.log`.
