# T-166 — Build-agent tooling wiring (skills, plugins, MCP)

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-131 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Keep the build agents fully wired: the generated tooling inventory stays current, project skills and subagents cover every phase, MCP servers are used when present, and CI fails when the inventory is stale.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-skill-scout` | verify the inventory matches the installed libraries and fill gaps |
| `karpathy-audit` | audit the instruction files for contradictions and dead weight after the growth |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `status/TOOLING.md` regenerated and wired into CI (`--check`)
- Project skills and subagents reviewed against the 13 phases; gaps filled or explicitly noted

## Steps

1. Run `python3 scripts/discover_tooling.py` and commit the refreshed inventory.
2. Add the `--check` step to `.github/workflows/repo-hygiene.yml` so a stale inventory fails CI.
3. Walk each phase in `handbooks/03-skills-catalog.md` and confirm a real skill exists for its primary and verification stream.
4. Verify the docs point at the inventory rather than repeating skill names that may drift.

## Acceptance criteria

- [ ] CI fails when `status/TOOLING.md` is stale (proven once, then reverted)
- [ ] Every phase names skills that exist in the inventory
- [ ] No document duplicates the inventory as a hard-coded list of names without linking to it

## Verification

```bash
python3 scripts/discover_tooling.py --check
python3 tools/check_links.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-166 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-166 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-166: Build-agent tooling wiring (skills, plugins, MCP)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The build agents can always see, and are required to use, the skills and tools that exist.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-166.log`.
