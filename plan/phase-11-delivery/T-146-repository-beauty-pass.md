# T-146 — Repository presentation pass

> Phase 11 · Delivery · **Depends on:** T-145 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Make the repository welcoming and accurate for a human: README, description, topics, templates, badges that reflect reality.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `technical-writing` | remove any claim that is not true; no marketing filler |
| `ci-cd-github-actions` | confirm badges point at workflows that actually exist and pass |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Final README with accurate badges, structure and quick start
- Repository description and topic list set on GitHub, issue and PR templates present

## Steps

1. Verify every badge URL resolves and its workflow exists.
2. Update the README's repository layout section against the real tree.
3. Set the repository description and topics through `gh repo edit`.
4. Confirm the templates render and match the actual process.

## Acceptance criteria

- [ ] No badge is broken and none claims a state that is not true
- [ ] The layout section matches the real directory tree
- [ ] Description and topics are set on the repository

## Verification

```bash
gh repo view --json description,repositoryTopics
python3 tools/check_links.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-146 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-146 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-146: Repository presentation pass"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The repository explains itself accurately to a human visitor and to an agent.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-146.log`.
