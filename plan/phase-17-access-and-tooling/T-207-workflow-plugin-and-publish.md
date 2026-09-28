# T-207 — Reusable build workflow: consume it here, publish it separately

> Phase 17 · One-tap access, key issuing & tooling coverage · **Depends on:** T-166, T-206 · **Parallel-safe:** yes · **Est. agent time:** 240-480 min

## Goal

Turn this repository's agent workflow into a reusable, installable artefact — skills, subagents, gate scripts and templates — use it from this project, and publish it in its own private repository containing nothing project-specific.

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
| `droidroute-skill-scout` | what belongs in a reusable workflow and what is only true for this project |
| `git-workflow` | keeping two repositories honest without copying files between them |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A workflow plugin (manifest + skills + subagents + gate scripts + templates) that installs into any project
- This repository consuming the plugin, with the duplicated parts removed and referenced instead
- Its own private GitHub repository, containing the workflow only — asserted by a leak check

## Steps

1. Separate the workflow from the project: the loop, the gates, the log protocol and the handover rules are generic; the design tokens, providers and acceptance criteria are not.
2. Package the generic part as a plugin with a manifest, so another agent can install it rather than copy it.
3. Make this repository consume the plugin and delete its own copies of anything the plugin now owns — two sources of truth is the failure mode to avoid.
4. Prove it runs: install it in a scratch project and complete one small task with it, recording the run.
5. Add a leak check to the plugin repository: no project name, no credential, no file from this project may appear in it.

## Acceptance criteria

- [ ] The plugin installs in a scratch project and completes a task end to end (recorded)
- [ ] This repository has no duplicate copy of anything the plugin owns
- [ ] The plugin repository contains no project-specific file, name or secret (asserted by its own check)
- [ ] Both repositories are private, and each documents how the other is updated

## Verification

```bash
python3 tools/check_plan_consistency.py
gh repo view --json name,visibility
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-207.log`)
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

- `scripts/log-step.sh T-207 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-207 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-207: Reusable build workflow: consume it here, publish it separately"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The build workflow is reusable and published on its own, while this project consumes it instead of forking it.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-207.log`.
