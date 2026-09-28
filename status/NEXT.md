# Next Task

**Resume here:** [`T-002 — Android toolchain and build prerequisites`](../plan/phase-00-foundation/T-002-android-toolchain.md)

| | |
|---|---|
| Phase | 00 — Foundation |
| Depends on | T-001 |
| Parallel-safe | yes |
| Est. agent time | 20–40 min |

## Why this one

The plan's first task exists to prove the tooling works before any app code exists: the secrets preflight, the step logger, the commit + push script and the CI workflows all get exercised on a change that cannot break a build. Everything downstream depends on that chain being trustworthy.

## Before you start

```bash
git status --short                                # must be clean
cat status/ERRORS.md                              # must have no open entries
python3 scripts/discover_tooling.py --check-fresh  # tooling inventory must match this machine
python3 tools/check_plan_consistency.py           # plan, documents and tooling agree
scripts/preflight-secrets.sh
```

Resolve this task's two role labels (`git-workflow` + `testing`) through [`handbooks/09-skill-resolution.md`](../handbooks/09-skill-resolution.md) — that table turns each label into the installed skills, plugins and MCP servers to load, and `python3 tools/check_skills.py` proves the mapping still points at something installed. The project skills [`droidroute-task-runner`](../.claude/skills/droidroute-task-runner/SKILL.md) and [`droidroute-verification`](../.claude/skills/droidroute-verification/SKILL.md) apply to every task. The full inventory is [`status/TOOLING.md`](TOOLING.md).

## After it is done

Update this file to point at `T-003`, tick T-002 in [`PROGRESS.md`](PROGRESS.md), and commit both in the same commit as the task:

```bash
scripts/step-commit.sh "T-002: Android toolchain and build prerequisites"
```

## T-001 evidence

Preflight blocks planted keys (exit 1, FAIL line), passes clean in ~17s (optimised combined-scan path, semantics unchanged), `log-step.sh` writes well-formed JSON records, `weekly-cleanup.sh --dry-run` reports without moving anything. See `logs/tasks/T-001.log`.
