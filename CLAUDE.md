# CLAUDE.md — Claude Code entry point

**Before anything else: read [`AGENTS.md`](AGENTS.md).** It holds the canonical rules (boot sequence, task loop, minimum two parallel skills, logging, git protocol, prohibitions). This file only adds what is specific to Claude Code.

## Claude Code specifics

**Subagents.** Use the Task tool to run the task's skills in parallel — typically three: one implementing the deliverable, one writing and running tests, one updating integration/docs. Launch them in a single message so they run concurrently. Give each subagent the task id, its workstream name, its exclusive file list, and the acceptance lines it owns. Never let two subagents edit the same file in one round.

**Skills.** Prefer an installed skill over ad-hoc instructions. The catalog this project expects is [`handbooks/03-skills-catalog.md`](handbooks/03-skills-catalog.md); if you substitute, log `skill-substitution: <old> → <new> (<reason>)`.

**Plan mode.** Use it to read the task file and its dependencies before writing anything. The task file's *Steps* section is a suggestion; *Acceptance criteria* is the contract.

**Shell continuity.** Termux has no persistent daemon across sessions — assume nothing about the previous session except what is in `git log`, `logs/`, and `status/`.

**Context budget.** Do not read all 147 task files. Read `status/NEXT.md`, the target task, its `Depends on` tasks' *Acceptance criteria* only, and the docs the task links to.

## The loop in Claude Code terms

```bash
cat status/PROGRESS.md status/NEXT.md status/ERRORS.md; git status --short
cat plan/<phase>/T-0xx-*.md
# dispatch subagents (≥2 skills, parallel)
# integrate, then verify:
./gradlew :app:testDebugUnitTest        # or the task's own command
scripts/log-step.sh T-0xx "verify" "gradle tests" "pass"
scripts/step-commit.sh "T-0xx: <task title>"
```

## Project facts you must not re-derive

- App id `com.droidroute.app`, Kotlin 2.0 / AGP 8.7 / JDK 17, minSdk 26, target + compile SDK 35.
- Default port **8787**, user-configurable. Local-only bind by default; non-local bind requires an API key.
- Ktor 3 with the CIO engine — there is no Netty on Android.
- Secrets live in `KeyVault` (AES-256-GCM, Keystore-wrapped). Never plaintext, never in the repo.
- The owner is German-speaking: the app UI is German by default with English available; repository documents are English except `docs/glossary-de.md`.
- All settled open questions are in [`docs/11-tbc-resolutions.md`](docs/11-tbc-resolutions.md). If a task contradicts it, the task is wrong — fix the task file and log why.

## When the owner is present

They read German. Explain what you did in plain German, keep technical identifiers as they are, and name the next task id so they can follow along. Do not ask for permission to continue the chain unless a stop condition from `AGENTS.md` §9 applies.
