# T-166 — Build-agent tooling wiring (skills, plugins, MCP)

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-131 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Keep the build agents fully wired: the generated tooling inventory stays current, project skills and subagents cover every phase, MCP servers are used when present, and CI fails when the inventory is stale.

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
| `droidroute-skill-scout` | verify the inventory matches the installed libraries and fill gaps |
| `karpathy-audit` | audit the instruction files for contradictions and dead weight after the growth |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `status/TOOLING.md` regenerated, with `--check` wired into CI and `--check-fresh` documented for local use
- Project skills and subagents reviewed against the 14 phases; gaps filled or explicitly noted

## Steps

1. Run `python3 scripts/discover_tooling.py` and commit the refreshed inventory.
2. Confirm the CI step validates structure (`--check`) and that freshness is a local duty (`--check-fresh`) — a runner without agent configuration must not fail the build for a reason it cannot control.
3. Walk each phase in `handbooks/03-skills-catalog.md` and confirm a real skill exists for its primary and verification stream, resolving every role label through `handbooks/09-skill-resolution.md`.
4. Verify the docs point at the inventory rather than repeating skill names that may drift.

## Acceptance criteria

- [ ] CI fails when `status/TOOLING.md` is malformed, and passes on a runner with no agent configuration (proven once for each, then reverted)
- [ ] `--check-fresh` fails on the device when the inventory is out of date (proven once, then reverted)
- [ ] Every phase names skills that exist in the inventory

## Verification

```bash
python3 scripts/discover_tooling.py --check
python3 scripts/discover_tooling.py --check-fresh
python3 tools/check_links.py
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-166.log`)
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

- `scripts/log-step.sh T-166 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-166 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-166: Build-agent tooling wiring (skills, plugins, MCP)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The build agents can always see, and are required to use, the skills and tools that exist.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-166.log`.
