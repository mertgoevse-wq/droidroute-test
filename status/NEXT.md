# Next Task

**Resume here:** [`T-001 — Repository hygiene and baseline checks`](../plan/phase-00-foundation/T-001-repository-hygiene.md)

| | |
|---|---|
| Phase | 00 — Foundation |
| Depends on | — (first task) |
| Parallel-safe | yes |
| Est. agent time | 20–40 min |

## Why this one

The plan's first task exists to prove the tooling works before any app code exists: the secrets preflight, the step logger, the commit + push script and the CI workflows all get exercised on a change that cannot break a build. Everything downstream depends on that chain being trustworthy.

## Before you start

```bash
git status --short          # must be clean
cat status/ERRORS.md        # must have no open entries
scripts/preflight-secrets.sh
```

## After it is done

Update this file to point at `T-002`, tick T-001 in [`PROGRESS.md`](PROGRESS.md), and commit both in the same commit as the task:

```bash
scripts/step-commit.sh "T-001: repository hygiene and baseline checks"
```
