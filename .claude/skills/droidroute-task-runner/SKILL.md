---
name: droidroute-task-runner
description: Execute one DroidRoute task file from plan/ end to end - read dependencies, dispatch parallel skills as subagents, verify, log, commit and update status. Use at the start of every task in this repository, or whenever the user says "continue with the next task", "do T-0xx" or "keep the chain going".
---

# Run one DroidRoute task

## Before touching code

```bash
cat status/HANDOVER.md status/NEXT.md status/ERRORS.md 2>/dev/null
tail -n 40 logs/chain.log
git status --short
cat plan/<phase>/T-0xx-<slug>.md
```

Read the task file completely — Goal, Skills, Deliverables, Steps, Acceptance criteria, Verification, Handover.
**Acceptance criteria are the contract; Steps are a suggestion.**

## Confirm the dependency is real

For every id in `Depends on:` check the delivered artefact exists (file, test, endpoint) — never trust a tick in `status/PROGRESS.md` alone. If something is missing, do that task first and log the reordering.

## Choose at least two skills

Read `status/TOOLING.md` for what is actually installed, then pick:

| Workstream | Preferred skills |
|---|---|
| Kotlin/Android implementation | `mobile-android-design`, `adaptive`, `testing-setup`, `android-cli` |
| Protocol / provider work | `droidroute-provider-manifest`, `droidroute-routing` |
| UI | `droidroute-compose-ui` + a design skill from the library |
| Verification | `droidroute-verification`, `ruthless testing` habits from `superpowers` |

The task file suggests skills; you may substitute, but never go below two parallel workstreams and never skip verification. Log any substitution.

## Execute

1. Dispatch the workstreams as **parallel subagents** (see `.claude/agents/`), giving each an exclusive file list.
2. Integrate their output yourself; subagents never commit.
3. Run every command in the task's **Verification** block verbatim and paste the raw output into the log.
4. Tick acceptance boxes only for criteria you actually observed passing.

## Close

```bash
scripts/log-step.sh T-0xx "test" "<command>" "pass" --actor verify
# update status/PROGRESS.md, status/NEXT.md (+ DECISIONS.md / ERRORS.md when relevant)
scripts/step-commit.sh "T-0xx: <exact task title>"
```

If a criterion cannot be met after one honest repair attempt: append to `status/ERRORS.md` and **stop the chain**. A clear stop beats a silent break.

## Never

Commit a secret, invent a provider URL, touch files outside the task, weaken a test, or force-push.
