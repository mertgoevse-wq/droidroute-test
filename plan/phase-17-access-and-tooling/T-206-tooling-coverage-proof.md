# T-206 — Proof that every applicable skill, plugin and MCP server is used

> Phase 17 · One-tap access, key issuing & tooling coverage · **Depends on:** T-166, T-190 · **Parallel-safe:** yes · **Est. agent time:** 150-300 min

## Goal

Stop the build agents from using the three tools they remember. Decide, per installed skill, plugin and MCP server, whether it applies — and record used / declined-with-reason for each, with CI failing on "undecided".

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
| `droidroute-skill-scout` | matching an installed tool to the work it actually improves |
| `droidroute-verification` | a coverage report that can be re-run and compared, not a narrative |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `tools/tooling_coverage.py` — joins `status/tooling.json` with a committed decisions file and reports undecided entries
- `status/TOOLING-COVERAGE.md` — every installed skill, plugin and MCP server with used / declined + reason, and where it was used
- CI step that fails while any entry is undecided

## Steps

1. Generate the candidate list from the inventory, grouped by domain, so nothing is missed by not being remembered.
2. For each candidate, record a decision: `used` with the phase and task id where it applied, or `declined` with a one-line reason.
3. Make the report check itself: an entry present in the inventory but absent from the decisions fails, and so does a decision for a tool that is no longer installed.
4. Review the declined list once with fresh eyes — a tool declined in phase 3 may apply in phase 12, and the reason must say why not.

## Acceptance criteria

- [ ] Every installed skill, plugin and MCP server has a decision with a reason
- [ ] Every `used` entry names where it was used (phase or task id)
- [ ] CI fails while an entry is undecided (proven once, then reverted)
- [ ] The report is regenerated in the same commit as any inventory change

## Verification

```bash
python3 tools/tooling_coverage.py --check
python3 tools/check_plan_consistency.py
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-206.log`)
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

- `scripts/log-step.sh T-206 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-206 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-206: Proof that every applicable skill, plugin and MCP server is used"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Tool usage is a reviewed decision per tool instead of a habit — and the gaps are named.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-206.log`.
