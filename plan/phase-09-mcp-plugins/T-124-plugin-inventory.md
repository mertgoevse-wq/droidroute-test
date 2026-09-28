# T-124 — Plugin and skill inventory endpoint

> Phase 09 · MCP & plugins · **Depends on:** T-120, T-031 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Expose what the host environment offers — skills, plugins, agent capabilities — so an agent does not guess or shell out.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `mcp-protocol` | what can be read reliably from a host environment |
| `security-audit` | an inventory must not expose secrets or private paths unnecessarily |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `GET /plugins` returning discovered skills/plugins with their source and availability
- Documentation of what is and is not reliable to detect

## Steps

1. Read host skill directories and plugin manifests through the bridge where paths are known.
2. Report only names, sources and availability — no file contents, no credentials.
3. Mark unreliable detections as such instead of guessing.

## Acceptance criteria

- [ ] `/plugins` returns the host inventory, or states precisely why it is unavailable
- [ ] No file contents or secrets appear in the response
- [ ] The docs state which detections are reliable

## Verification

```bash
curl -fsS http://127.0.0.1:8787/plugins | head -20
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-124 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-124 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-124: Plugin and skill inventory endpoint"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

An agent can see what tooling it has without leaving the gateway.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-124.log`.
