# T-001 — Repository hygiene and baseline checks

> Phase 00 · Foundation · **Depends on:** — (entry task) · **Parallel-safe:** yes · **Est. agent time:** 20-40 min

## Goal

Make the tooling trustworthy before any app code exists. Every script in scripts/ runs cleanly, the secrets preflight blocks a planted key, the step logger writes a well-formed record, and the CI workflows are green on the current tree.

## Read first (context budget)

- [`status/NEXT.md`](../../status/NEXT.md) — the next task and the pre-flight commands
- [`status/ERRORS.md`](../../status/ERRORS.md) — must have no open entry for this task
- [`handbooks/09-skill-resolution.md`](../../handbooks/09-skill-resolution.md) — what each skill label below means on this machine
- [`docs/11-tbc-resolutions.md`](../../docs/11-tbc-resolutions.md) — decisions already settled; not re-opened
- this file, top to bottom, plus the *Acceptance criteria* of every `Depends on` task

Do not read the rest of the plan to "get oriented" — the entry point is this file plus the documents linked here. If the work genuinely needs another document, read that one and nothing more.

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

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-001.log`)
- [ ] No placeholder, no invented endpoint/URL/model/field, no edit outside the files this task names
- [ ] Nothing was weakened to make a check pass (no deleted test, no raised threshold, no disabled rule)
- [ ] `status/PROGRESS.md` and `status/NEXT.md` updated in the same commit as the work
- [ ] `scripts/preflight-secrets.sh` clean
- [ ] UI work only: `python3 tools/check_design_slop.py` passes and the four craft tests ran ([docs/14-design-system.md](../../docs/14-design-system.md) §11)

## Rules that always apply

- Prohibitions and the quality bar: [handbooks/07-anti-slop-rules.md](../../handbooks/07-anti-slop-rules.md) (placeholders, invented endpoints, unrequested scope, weakened checks)
- At least two skills **in parallel** as subagents, one of them verification: [AGENTS.md](../../AGENTS.md) §4
- Log every meaningful step, commit and push exactly once for this task: [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md) · [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md)
- No secret in the repository, ever: `scripts/preflight-secrets.sh` must pass
- A new dependency, a deviation, or a settled decision goes into [status/DECISIONS.md](../../status/DECISIONS.md) in the same commit
- Missing tool for the job? Search before improvising: [handbooks/08-tooling-discovery.md](../../handbooks/08-tooling-discovery.md)

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-001 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-001 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-001: Repository hygiene and baseline checks"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Tooling proven: preflight blocks secrets, logging writes valid JSON records, cleanup is safe, CI is green.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-001.log`.
