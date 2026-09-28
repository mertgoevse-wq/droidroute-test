# Agent Handbook

You are building **DroidRoute**. This is the operating manual. Follow it literally; where it is silent, prefer the smallest change that satisfies the task.

## 0. First five minutes

```bash
cat status/HANDOVER.md      # two-minute state summary, if present
cat status/PROGRESS.md      # what is already done
cat status/NEXT.md          # what to do next
cat status/ERRORS.md        # what is currently broken, if anything
cat status/TOOLING.md       # which skills, plugins and MCP servers you actually have
tail -n 50 logs/chain.log   # what happened last
git status --short          # is the tree clean?
cat docs/11-tbc-resolutions.md   # the decisions you must not re-litigate
```

If `python3 scripts/discover_tooling.py --check` fails, regenerate the inventory first: an out-of-date list makes you skip tools that exist.

If the tree is not clean, understand the uncommitted diff before writing anything. Never discard someone else's in-progress work with a reset.

## 1. Pick the task

- The next task is the one named in `status/NEXT.md`. Confirm its dependencies (`Depends on:`) are actually satisfied — check for the delivered files, not just for a tick in `PROGRESS.md`.
- If a dependency is missing, do that one first and say so in the log.
- Do not reorder tasks to "optimise" the plan. Order encodes dependency.

## 2. Read the task file completely

Every task file has: Goal · Skills · Deliverables · Steps · Acceptance criteria · Verification · Logging & Git · State after success. Read all of it before touching code. The acceptance criteria are the contract; the steps are a suggestion of how to get there.

## 3. Work with at least two parallel subagents

See [`handbooks/02-subagent-orchestration.md`](02-subagent-orchestration.md). Summary: split the task into separable workstreams (typically implement / test / document), give each a stated skill, run them in parallel, integrate in the main context. Four subagents are ready to dispatch in `.claude/agents/`: `implementer`, `verifier`, `chronicler`, `tooling-scout`. Never drop below two parallel workstreams plus one verification stream.

## 4. Verify before claiming

Run the task's Verification commands verbatim. Record the command and its output in the task log. A criterion is ticked only when you saw it pass. Never tick a box because the code "looks right".

## 5. Log everything

`scripts/log-step.sh T-0xx "<action>" "<result>"` after every meaningful step (file written, test run, error hit). Format and rules: `handbooks/05-logging-standard.md`. Redaction is automatic; if you are about to log a raw key, don't.

## 6. Commit and push

```bash
scripts/step-commit.sh "T-0xx: <task title>"
```

This stages, commits, tags a checkpoint and pushes — in one shot. If it fails, follow `handbooks/04-git-protocol.md` ("push failure").

## 7. Update the status files

In the same commit: tick the task in `status/PROGRESS.md`, set the next task in `status/NEXT.md`, append any design decision to `status/DECISIONS.md`, append any unresolved breakage to `status/ERRORS.md`.

## 8. Stop conditions

Stop the chain and report when:

- an acceptance criterion cannot be satisfied after one honest repair attempt,
- a decision is needed that the spec does not cover and would change user-visible behaviour,
- the same command fails twice for environmental reasons (no network, missing tool),
- a task turns out to be wrong (then fix the plan: edit the task file, log why, and continue — a wrong task is a plan bug, not a licence to improvise).

Never continue past a broken invariant. A chain that stops with a clear `status/ERRORS.md` entry is worth more than a chain that silently produces a broken app.

## 9. Things that are never allowed

- Committing a real secret, ever, under any circumstance.
- Placeholder implementations (see `handbooks/07-anti-slop-rules.md`).
- Inventing provider URLs, model names or API fields.
- Editing files outside the task's scope.
- Force-pushing or rewriting history.
- Disabling tests, lint rules or security checks to make a task pass.

## 10. Definition of done for your task

- All acceptance boxes ticked with evidence.
- Logs written, status files updated.
- Commit pushed.
- The repository is in a state where the *next* agent can start with no context from you.
