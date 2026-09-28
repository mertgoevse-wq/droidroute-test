# T-208 — Clone-from-scratch verification and freeze

> Phase 17 · One-tap access, key issuing & tooling coverage · **Depends on:** T-202, T-205, T-207 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Prove the handover works from nothing: clone into an empty directory, run the bootstrap, pass every check, and complete one task end to end as a fresh agent. Then freeze it and state what is not finished.

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
| `git-workflow` | a clean clone, a clean tree and a push that loses nothing |
| `droidroute-verification` | the drill: does a stranger with only the repository succeed? |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A recorded clone-from-scratch run: clone → `scripts/bootstrap.sh` → every check green → one task completed
- The freeze statement in `status/PROGRESS.md`, with the exact commit and the open items
- Owner instructions updated for the new folder name and the clone path

## Steps

1. Clone the repository into an empty directory under the new name and run the bootstrap exactly as documented.
2. Run every checker and paste the raw output into the task log — including the design gate's self-test.
3. Dispatch a fresh agent with only the repository: it reads the state files and completes one task from the plan.
4. Record the drill as a document a future agent can repeat, including what was confusing about it.
5. Freeze: name the commit, list what is unfinished, and update the owner instructions.

## Acceptance criteria

- [ ] A fresh clone passes `scripts/bootstrap.sh` with no manual step (paste the output)
- [ ] A fresh agent completed one task using only the repository (recorded)
- [ ] The new folder name appears in every instruction and no stale path remains
- [ ] The freeze statement names what is unfinished instead of implying completion

## Verification

```bash
bash scripts/bootstrap.sh
python3 tools/check_plan_consistency.py
python3 tools/generate_plan.py --check
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-208.log`)
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

- `scripts/log-step.sh T-208 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-208 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-208: Clone-from-scratch verification and freeze"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Someone with nothing but the clone URL can take over, and the repository says truthfully where it stands.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-208.log`.
