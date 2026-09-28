# T-010 — Documentation baseline and link integrity

> Phase 00 · Foundation · **Depends on:** T-001 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Guarantee that the documentation set is self-consistent: every relative link resolves, every doc referenced from README/AGENTS.md exists, and the German glossary covers every term a reader will meet in the docs.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `technical-writing` | check accuracy and remove any remaining filler |
| `testing` | extend the link checker to cover the glossary coverage rule |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Link checker extended to report broken relative links with file and target
- `docs/glossary-de.md` updated with any term introduced since the scaffold

## Steps

1. Run the link checker locally over the whole tree and fix every report.
2. Cross-read docs/ against status/components/ for stale statements about task ranges.
3. Add missing glossary entries for any new term (do not invent terms the docs do not use).

## Acceptance criteria

- [ ] Link checker reports zero broken relative links
- [ ] Every doc listed in AGENTS.md §10 exists
- [ ] No doc claims a task range that disagrees with plan/INDEX.md

## Verification

```bash
python3 tools/generate_plan.py --check
python3 tools/check_links.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-010 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-010 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-010: Documentation baseline and link integrity"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Documentation is internally consistent and machine-checked; drift now fails CI instead of confusing the next agent.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-010.log`.
