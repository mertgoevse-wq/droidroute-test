# CLAUDE.md — Claude Code entry point

**Before anything else: read [`AGENTS.md`](AGENTS.md).** It holds the canonical rules (boot sequence, task loop, minimum two parallel skills, logging, git protocol, prohibitions). This file only adds what is specific to Claude Code.

## Claude Code specifics

**Subagents.** Four are defined in [`.claude/agents/`](.claude/agents/): `implementer`, `verifier`, `chronicler`, `tooling-scout`. Dispatch at least `implementer` + `verifier` per task, add `chronicler` when docs/status/logs change, and `tooling-scout` when the right tool is unclear. Launch them in one message so they run concurrently. Give each subagent the task id, its workstream name, its exclusive file list, and the acceptance lines it owns. Never let two subagents edit the same file in one round.

**Skills.** Prefer an installed skill over ad-hoc instructions. Read [`status/TOOLING.md`](status/TOOLING.md) (generated) to see what is actually installed — 100+ global skills, the project skills in [`.claude/skills/`](.claude/skills/), plugins such as `superpowers` and `context-mode`, plus any MCP servers. The selection matrix per phase is [`handbooks/03-skills-catalog.md`](handbooks/03-skills-catalog.md); the rules are [`handbooks/08-tooling-discovery.md`](handbooks/08-tooling-discovery.md); and [`handbooks/09-skill-resolution.md`](handbooks/09-skill-resolution.md) turns each role label a task names (`kotlin-core`, `provider-integration`, …) into the concrete installed skills, plugins and MCP servers to load — every token there is checked against the inventory by `tools/check_skills.py`. If you substitute or install, log `skill-substitution: <old> → <new> (<reason>)` and ask before installing anything from the community index.

**Project skills override global ones.** When both cover the same ground, the project skill wins because it encodes this repository's constraints. Six are installed: `droidroute-task-runner`, `droidroute-verification`, `droidroute-provider-manifest`, `droidroute-routing`, `droidroute-compose-ui`, `droidroute-skill-scout`.

**MCP.** Use a connected MCP tool before writing code that does the same thing. Project servers live in `.mcp.json` (template: [`.mcp.json.example`](.mcp.json.example)); all project servers are auto-enabled by `.claude/settings.json`. Check the MCP section of `status/TOOLING.md` — if it says none are configured, proceed without inventing one.

**Plan mode.** Use it to read the task file and its dependencies before writing anything. The task file's *Steps* section is a suggestion; *Acceptance criteria* is the contract.

**Shell continuity.** Termux has no persistent daemon across sessions — assume nothing about the previous session except what is in `git log`, `logs/`, and `status/`.

**Context budget.** Do not read all 184 task files. Read `status/NEXT.md`, the target task, its `Depends on` tasks' *Acceptance criteria* only, and the docs the task links to.

## The loop in Claude Code terms

```bash
cat status/HANDOVER.md status/PROGRESS.md status/NEXT.md status/ERRORS.md; git status --short
grep -E '^(## Summary|\| Global skills|\| MCP servers)' -A2 status/TOOLING.md   # what tools exist
python3 scripts/discover_tooling.py --check-fresh || python3 scripts/discover_tooling.py   # refresh if stale
cat plan/<phase>/T-0xx-*.md
# dispatch subagents: implementer + verifier in parallel (add chronicler for doc/status work)
# integrate, then verify:
./gradlew :app:testDebugUnitTest        # or the task's own command
scripts/log-step.sh T-0xx "test" "gradle tests" "pass" --actor verify
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
