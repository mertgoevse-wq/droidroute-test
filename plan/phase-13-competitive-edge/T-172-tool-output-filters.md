# T-172 — Tool-output compression filters (lossless tool results)

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-153 · **Parallel-safe:** yes · **Est. agent time:** 180-300 min

## Goal

Compress the tool results that eat prompts — `git diff`, `git status`, `grep`, `find`, `ls`, `tree`, log dumps — with auto-detection, a per-request bypass header, and a guarantee that a failing filter keeps the original text.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-routing` | where in the request pipeline this runs: before dialect translation, per tool result |
| `droidroute-verification` | losslessness proofs per filter and a fail-open test for each |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/compression/filters/` — one filter per output family, each with its own tests
- Automatic filter selection from the head of the tool result, and `X-DroidRoute-Token-Saver: off` as a bypass

## Steps

1. Implement each filter to be reversible and to bail out if the result is not smaller.
2. Select the filter from the content itself, not from a path or a caller-supplied hint.
3. Record per-filter savings so the owner can see which filters actually pay off on their workload.
4. Test: identical semantic content, smaller payload, and the filter that throws keeps the original.

## Acceptance criteria

- [ ] Every filter is lossless on its fixture corpus (round-trip asserted)
- [ ] A throwing filter leaves the original content untouched and logs the failure
- [ ] The bypass header disables all filters for that request (asserted)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*ToolFilter*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-172 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-172 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-172: Tool-output compression filters (lossless tool results)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The single biggest token cost in agent traffic — tool output — is cut without changing what the model sees.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-172.log`.
