# T-109 — llama-server process lifecycle

> Phase 08 · Local models · **Depends on:** T-108 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Start, monitor and stop llama-server per model, with idle unload, and prove the port is released on stop.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `local-inference` | process supervision, port allocation, log capture |
| `testing` | start/stop/restart tests, including a crashed-process recovery test |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `local/LlamaProcess.kt` — load, unload, status, log tail; idle unload after N minutes
- Port allocation from a reserved local range, one per loaded model

## Steps

1. Start the process with the documented flags (context, threads, no mlock) and capture its output.
2. Detect readiness by polling `/health` on the model port, not by sleeping.
3. Unload cleanly; if the process died, report the reason and its stderr tail.
4. Unload on idle and on memory-pressure callbacks.

## Acceptance criteria

- [ ] A loaded model answers a completion through its local port
- [ ] Stopping releases the port within a second
- [ ] A crashed process is detected and reported rather than silently leaving a dead provider

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*LlamaProcess*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-109 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-109 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-109: llama-server process lifecycle"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Local models have a managed lifecycle with observable state.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-109.log`.
