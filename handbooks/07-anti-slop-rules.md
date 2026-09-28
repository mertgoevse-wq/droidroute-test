# Anti-Slop Rules

Binding for every agent, every task, every commit. Each rule names the violation and the correct behaviour.

## 1. No placeholder implementations

**Violation:** `// TODO: implement later`, `throw NotImplementedError()`, a function returning hard-coded fake data so a test passes.
**Correct:** implement it, or — if the task explicitly says to create a seam — create a documented adapter with a single `not_supported` error path and register it in `status/DECISIONS.md`.

## 2. No invented endpoints, URLs, model names or fields

**Violation:** writing `https://api.someprovider.com/v1` because it looks plausible; guessing a request field name.
**Correct:** the task says to read the provider's documentation; if it is unreachable, stop the task and record it. A wrong URL produces a provider that silently never works — worse than a missing one.

## 3. No unrequested scope

**Violation:** reformatting a file you did not have to touch, renaming someone else's identifiers, "while I was here" refactors, mass dependency upgrades.
**Correct:** change exactly what the task names. If you find a genuine defect outside scope, write it into `status/ERRORS.md` and leave the code alone.

## 4. No unverified completion

**Violation:** ticking acceptance boxes because the code compiles; writing "tests pass" without running them.
**Correct:** run the verification command, paste the raw result into the task log, then tick.

## 5. No silent failures

**Violation:** `catch (e: Exception) { /* ignore */ }`, `|| true` on a check.
**Correct:** handle it or log it with a reason. Every swallowed exception appears in the log with `level: warn` and a `result` explaining why it is safe to continue.

## 6. No duplicated truth

**Violation:** the same rule stated in `README.md`, `CLAUDE.md`, `AGENTS.md` and three handbooks, drifting apart.
**Correct:** state it once, link to it. The canonical homes are: architecture → `docs/01`, protocols → `docs/02`, routing → `docs/04`, security → `docs/05`, process → `docs/08` + `handbooks/`.

## 7. No filler prose

**Violation:** "In today's fast-paced world of AI…", restating the task title as a sentence, adjectives like *seamless*, *robust*, *powerful*, *cutting-edge*.
**Correct:** facts, decisions, rules, numbers. If a sentence does not change what the reader does, delete it.

## 8. No unverifiable claims

**Violation:** "This is 10× faster", "widely compatible", "production-ready".
**Correct:** a measured number with the measurement described, or nothing.

## 9. No test or check weakening

**Violation:** deleting a failing test, adding `@Ignore`, lowering a threshold, disabling lint or the secrets preflight to make a commit pass.
**Correct:** fix the cause. If the check itself is wrong, change it in its own task with the reasoning recorded in `status/DECISIONS.md`.

## 10. No template residue

**Violation:** files that still contain `<YOUR NAME>`, example text clearly not adapted, tables with rows nobody filled in.
**Correct:** every emitted file is fully resolved. A generator (if used) must produce complete files, not stubs.

## Self-check before committing

1. Does the diff contain only what the task named?
2. Are there any `TODO`, placeholder strings, or fake returns?
3. Did every acceptance criterion actually run?
4. Does every log line that should exist exist, and is it redacted?
5. Would a strict reviewer call any of this filler?

If any answer is uncomfortable, fix it before `scripts/step-commit.sh` runs.
