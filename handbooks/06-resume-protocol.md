# Resume Protocol

Any model, any program, no chat history. This is the procedure.

## Cold start checklist

```bash
# 1. Where are we?
cat status/PROGRESS.md          # tasks completed, with commit shas
cat status/NEXT.md              # the exact next task id and why
cat status/DECISIONS.md         # decisions already made — do not re-open them
cat status/ERRORS.md            # known breakage and its state

# 2. What happened last?
tail -n 80 logs/chain.log

# 3. Is the tree safe?
git status --short
git log --oneline -15
git tag --list 'checkpoint/*' | tail -3

# 4. Read the task you are about to do, in full
cat plan/<phase>/T-0xx-*.md
```

## Decision table

| Situation | Action |
|---|---|
| Tree clean, `NEXT.md` set | proceed with that task |
| Tree clean, `NEXT.md` stale (its task is already committed) | recompute the next task from `PROGRESS.md`, fix `NEXT.md` in your first commit |
| Uncommitted changes | read the diff. If it is a partial attempt at the current task, finish it. If it is unrelated or unintelligible, log it, move it to `logs/archive/uncommitted-<ts>.patch` (`git diff > …`, then `git checkout -- .`), and proceed cleanly |
| Last task's commit is missing but the work is done | verify by running the task's verification commands; if they pass, commit with that task's message |
| Push failed earlier | `git pull --rebase --autostash && git push`; if it conflicts, stop and report |
| A dependency's deliverable is absent | do the dependency first; log the reordering |
| `ERRORS.md` has an open entry | resolve it before new work, unless the entry says "accepted risk" |

## Half-finished task handling

A task can be interrupted at any step. Determine progress from the task log, not from guessing:

```bash
grep '"task":"T-042"' logs/tasks/T-042.log | tail -20
```

- The log's last `write`/`test` records tell you which steps finished.
- Acceptance boxes that are ticked **in the repository** are the ones a previous agent evidenced. Treat unticked as not done.
- Re-run the verification commands before continuing. A half-applied change that "looks done" is the most common source of silent breakage.

## Resuming in a different tool

The protocol is tool-agnostic on purpose. The only things a new tool needs are:

1. `CLAUDE.md` (Claude Code) or `AGENTS.md` (anything else) for behaviour rules,
2. `status/` for position,
3. `plan/` for the work,
4. `handbooks/` for the process.

If the new tool cannot run scripts, it performs the equivalent commands by hand and states that in the log (`actor: main`, `extra: {"script_bypassed": true}`) — but it still must not commit a secret and still must not force-push.

## Owner takeover

The owner may pause the chain at any task boundary. Nothing in the design requires a session to stay alive:

- Commits and tags are pushed, so the repository is the single source of truth.
- The app under construction is not needed to continue building it.
- `status/NEXT.md` is the "resume here" marker; it is updated in the same commit as the completed task, so it is never ahead of reality by more than one commit.

## Handover note template

When stopping deliberately (budget, ambiguity, environment), append to `status/ERRORS.md` or `status/PROGRESS.md`:

```
STOPPED: T-042 step 3/6
REASON: provider docs unreachable (offline)
STATE: QuotaLedger.kt written, untested, uncommitted → see logs/archive/uncommitted-*.patch
NEXT: rerun T-042 verification, then continue at step 4
```

That note plus `status/NEXT.md` is what makes the "any other model can continue" promise real.
