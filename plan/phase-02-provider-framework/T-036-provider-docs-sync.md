# T-036 — Keep docs/03-providers.md in sync with the manifests

> Phase 02 · Provider framework · **Depends on:** T-035 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Make the provider documentation checkable: a script compares the doc table with the shipped manifests so they cannot drift.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `technical-writing` | table that states what exists, no aspirational entries |
| `testing` | a check script wired into the repo-hygiene workflow |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `tools/check_providers.py` — compares manifest ids with the Tier tables in docs/03-providers.md
- Workflow step so a drift fails CI

## Steps

1. Parse the manifest ids from `assets/providers/` and the ids listed in the doc tables.
2. Report ids present in one place and not the other, grouped by tier.
3. Add the check to `.github/workflows/repo-hygiene.yml`.
4. Fix any drift found while writing the check.

## Acceptance criteria

- [ ] The script exits 0 on a consistent tree
- [ ] Removing a row from the doc makes the script fail (proven once, then reverted)
- [ ] CI runs the check

## Verification

```bash
python3 tools/check_providers.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-036 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-036 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-036: Keep docs/03-providers.md in sync with the manifests"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The provider catalogue in the docs is machine-verified against what actually ships.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-036.log`.
