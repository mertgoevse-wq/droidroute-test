# T-001 — Repository hygiene and baseline checks

> Phase 00 · Foundation · **Depends on:** — (entry task) · **Parallel-safe:** yes · **Est. agent time:** 20-40 min

## Goal

Make the tooling trustworthy before any app code exists. Every script in scripts/ runs cleanly, the secrets preflight blocks a planted key, the step logger writes a well-formed record, and the CI workflows are green on the current tree.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `git-workflow` | exercise the commit/tag/push path and the ignore rules |
| `testing` | plant a fake key and prove the preflight rejects it |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `logs/chain.log` seeded with a genesis record explaining the scaffold
- `status/ERRORS.md` and `status/DECISIONS.md` verified writable by the tooling

## Steps

1. Run `scripts/preflight-secrets.sh`; confirm it scans every tracked and untracked file.
2. Temporarily add a file containing a `sk-` shaped value, confirm the preflight fails, then remove it.
3. Run `scripts/log-step.sh T-001 "verify" "preflight" "pass"` and inspect the JSON record.
4. Run `scripts/weekly-cleanup.sh --dry-run` and confirm it reports without moving anything.
5. Confirm `.gitignore` keeps build output, keystores, model files and `logs/archive/` out of the tree.

## Acceptance criteria

- [ ] `scripts/preflight-secrets.sh` exits 0 on the clean tree and 1 on the planted key
- [ ] `logs/chain.log` contains a well-formed record with `ts`, `task`, `actor`, `action`, `result`
- [ ] `git status --short` is clean after the commit
- [ ] Both workflows show a completed run for the pushed commit (or a documented reason why not)

## Verification

```bash
scripts/preflight-secrets.sh
scripts/weekly-cleanup.sh --dry-run
tail -n 3 logs/chain.log
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-001 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-001 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-001: Repository hygiene and baseline checks"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Tooling proven: preflight blocks secrets, logging writes valid JSON records, cleanup is safe, CI is green.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-001.log`.
