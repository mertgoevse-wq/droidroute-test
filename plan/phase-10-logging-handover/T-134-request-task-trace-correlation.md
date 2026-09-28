# T-134 — Correlate runtime requests with build tasks

> Phase 10 · Logging & handover · **Depends on:** T-017, T-131 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Make it possible to join a runtime log line to the build task that produced the code path, for debugging after a handover.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `kotlin-core` | inject the build revision and task id into runtime records without churn |
| `testing` | assert the correlation fields exist and stay redacted |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Build metadata (git sha, build time) available at runtime and included in log records
- A documented way to go from a runtime record to the task that introduced the code

## Steps

1. Generate the git sha into the build at compile time.
2. Include it in every runtime log record and in `/health`.
3. Document the lookup: sha → commit → task id.

## Acceptance criteria

- [ ] A runtime record contains the build sha
- [ ] `/health` reports the same sha as the installed build
- [ ] The lookup procedure is documented and was performed once as evidence

## Verification

```bash
curl -fsS http://127.0.0.1:8787/health | grep -i sha
git log --oneline -1
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-134 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-134 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-134: Correlate runtime requests with build tasks"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Runtime behaviour can be traced back to the build that introduced it.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-134.log`.
