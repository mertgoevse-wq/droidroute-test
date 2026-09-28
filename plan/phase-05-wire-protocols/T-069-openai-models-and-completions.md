# T-069 — OpenAI models list and legacy completions

> Phase 05 · Wire protocols · **Depends on:** T-029, T-067 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Serve `/v1/models` from the live catalog and map `/v1/completions` onto chat where a provider lacks a legacy endpoint.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `llm-gateway-protocols` | model object shape and the legacy prompt interface |
| `testing` | catalog test plus a legacy-to-chat mapping test |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `/v1/models` returning the merged catalog with `provider/model` ids
- `/v1/completions` mapped onto chat messages with a documented prompt template

## Steps

1. Expose one id per model per provider, matching the canonical naming rule.
2. Map a raw prompt to a single user message; document that this is a compatibility shim, not a native path.
3. Return an empty list rather than an error when no provider is enabled.

## Acceptance criteria

- [ ] `/v1/models` lists every enabled provider's models with canonical ids
- [ ] A legacy completion request returns a readable answer
- [ ] The prompt-to-message mapping is documented in docs/02-protocols.md

## Verification

```bash
curl -fsS http://127.0.0.1:8787/v1/models | head -20
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-069 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-069 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-069: OpenAI models list and legacy completions"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Model listing and the legacy surface are available to older clients.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-069.log`.
