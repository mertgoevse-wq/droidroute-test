# Subagent Orchestration

**Rule: minimum two skills working in parallel per task, always with one verification workstream.**

## The standard split

Most tasks decompose cleanly into three workstreams:

| Workstream | Role | Typical skills |
|---|---|---|
| **Implement** | produces the deliverable | language/framework skill for the module |
| **Verify** | writes tests, tries to falsify the implementation | testing, security, performance |
| **Document/Integrate** | wires it into the app, updates docs and status | docs, build, integration |

For UI tasks the split becomes *structure / visual polish / accessibility*. For provider tasks it becomes *manifest+adapter / live validation call / error-path tests*. For routing tasks: *selection logic / scoring maths / failure-injection tests*.

## How to dispatch

1. **Write the contract first.** Before spawning anything, state the interface each workstream must produce (file path, function signature, JSON shape). Ambiguous contracts cause conflicting edits.
2. **Give each subagent**: the task id, its workstream name, the exact files it may write, the acceptance lines it owns, and the verification command it must run.
3. **Run them in parallel** when their file sets are disjoint.
4. **Serialise deliberately** when they collide. Say so in the log: `serialised: implement → verify (shared file: Router.kt)`.
5. **Integrate in the main context.** The main agent owns the final diff; subagents never commit.

## Collision rules

- Two subagents never write the same file in the same round.
- Tests live in separate files from implementation (`*Test.kt`), which makes implement/verify naturally parallel.
- Documentation updates go to files nobody else touches that round.
- If a shared file must change, one workstream owns it and the other submits a patch description instead of editing.

## Skill selection

Each task file suggests skills with a stated role. That suggestion is a **default with freedom to deviate** — but never below the two-parallel-workstream floor. If you substitute, log the substitution and the reason. `handbooks/03-skills-catalog.md` lists the skills this project relies on; the host's real inventory may be larger, and you should prefer a specific skill over a generic one.

## Verification workstream is not optional

The verification workstream must try to **break** the implementation, not confirm it:

- write the failing case first where practical,
- test the error paths the task names (timeout, `429`, malformed response, empty model list),
- check the redaction canary is absent from logs,
- run the acceptance command and paste the raw output into the log.

## Cost and quota discipline

Parallel subagents multiply token usage. Therefore:

- Set a budget per task in the task header (`Est. agent time`) and keep the subagents proportional to it.
- Prefer local/cheap models for mechanical workstreams when the host supports model selection, and reserve the strong model for the integrate step.
- Never run hedging or duplicate full-context reads across subagents; hand each one the exact excerpt it needs.

## Reporting format from a subagent

```
task: T-042
workstream: verify
status: pass | fail | blocked
files: app/src/test/kotlin/.../QuotaLedgerTest.kt
evidence: ./gradlew testDebugUnitTest --tests '*QuotaLedgerTest' → 6 passed
notes: 429 handling verified; unknown-window key left untested (no fixture)
```

The main agent folds these into `logs/tasks/T-042.log` and `status/*`.
