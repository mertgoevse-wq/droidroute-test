# T-135 — Handover documentation verification

> Phase 10 · Logging & handover · **Depends on:** T-132, T-133, T-134 · **Parallel-safe:** yes · **Est. agent time:** 50-100 min

## Goal

Final check of the whole handover chain: an agent with no context can find, understand and act on every artefact.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `technical-writing` | walk the documentation as a stranger would, not as its author |
| `testing` | convert each documented claim into a checkable assertion |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A verified handover chain: README → AGENTS/CLAUDE → status → plan → handbooks
- Corrections committed for anything that failed the walkthrough

## Steps

1. Follow the documented entry path from README to a completed action.
2. Check that every link resolves and every named file exists.
3. Confirm the German glossary covers the terms a German-speaking owner will meet.

## Acceptance criteria

- [ ] The walkthrough completes without consulting any undocumented source
- [ ] All links resolve (checked by tooling)
- [ ] Corrections are committed, not merely noted

## Verification

```bash
python3 tools/check_links.py
python3 tools/verify_chain.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-135 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-135 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-135: Handover documentation verification"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The handover chain is verified end to end rather than believed.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-135.log`.
