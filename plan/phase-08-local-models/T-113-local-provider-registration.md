# T-113 — Register local models as ordinary providers

> Phase 08 · Local models · **Depends on:** T-109, T-027 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Make a loaded local model indistinguishable from a hosted provider to routing, logging, usage and MCP.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-routing` | registration semantics: availability follows the process lifecycle |
| `testing` | routing test proving a local model is preferred under a suitable strategy |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Provider id `local/llamacpp/<model>` registered on load and removed on unload
- Capability declarations so local models are excluded from requests they cannot serve

## Steps

1. Register the running model with its real context window and capabilities.
2. Mark it available only while the process is healthy.
3. Ensure usage records mark local calls with zero cost and a `local` tag.
4. Test that a request can be routed to the local model and that it disappears from candidates on unload.

## Acceptance criteria

- [ ] A loaded model appears in `/v1/models` and answers through the normal routes
- [ ] Unloading removes it from the candidate list immediately
- [ ] Usage records are tagged `local` with cost 0

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*LocalProvider*'
curl -fsS http://127.0.0.1:8787/v1/models | grep local
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-113 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-113 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-113: Register local models as ordinary providers"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Local inference is a first-class route rather than a separate subsystem.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-113.log`.
