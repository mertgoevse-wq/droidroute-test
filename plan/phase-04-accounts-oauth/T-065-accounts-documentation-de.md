# T-065 — Account setup documentation for the owner

> Phase 04 · Accounts & OAuth · **Depends on:** T-064 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Write the German-language setup guidance the owner needs for each account, since every OAuth app registration happens outside this repository.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `technical-writing` | precise console steps, no filler, screenshots only if genuinely needed |
| `oauth-device-flow` | verify every step is current before writing it down |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `docs/accounts/README.md` (English, canonical) plus a German summary section per provider
- An entry in docs/glossary-de.md for any new term introduced

## Steps

1. For each account (Google, GitHub, HuggingFace, Perplexity), list: where to register the app, which scopes, which redirect, where to paste the client id.
2. State explicitly which steps the owner must do and which the app does.
3. Note what happens if a step is skipped.
4. Keep English as the canonical text and add the German short version, consistent with the project's language rule.

## Acceptance criteria

- [ ] Every account has a complete, ordered setup list
- [ ] Each step names the exact screen or command
- [ ] No step is described that the code does not actually require

## Verification

```bash
python3 tools/check_links.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-065 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-065 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-065: Account setup documentation for the owner"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can register every OAuth app without guessing, and a future agent can follow the same doc.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-065.log`.
