# T-145 — Owner documentation in German

> Phase 11 · Delivery · **Depends on:** T-144 · **Parallel-safe:** yes · **Est. agent time:** 80-150 min

## Goal

Document for the owner, in plain German, how to install, configure and use the app day to day.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `technical-writing` | plain German, technical terms kept and explained |
| `technical-writing` | verify every step was actually performed at least once |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `docs/owner-guide-de.md`: install, first run, connect Claude Code and Freebuff, add a provider, local models, MCP, troubleshooting
- Glossary additions for any new term

## Steps

1. Write for a reader who has the app installed but has forgotten the setup.
2. Include the exact commands with the real default port, and the German explanation of what each does.
3. Add a troubleshooting section from real failures encountered during the build.
4. Keep every step tested: mark any untested step as untested rather than implying it was verified.

## Acceptance criteria

- [ ] Every step was executed at least once and is described accurately
- [ ] The German text uses plain words with technical terms explained
- [ ] The troubleshooting section lists failures that actually occurred

## Verification

```bash
python3 tools/check_links.py
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-145 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-145 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-145: Owner documentation in German"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The owner can operate DroidRoute without reading the source or asking an agent.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-145.log`.
