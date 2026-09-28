# Skill Resolution — role labels to installed tools

A task file names **role labels** (`kotlin-core`, `provider-integration`, `testing`, …), not raw tool names.
A label is stable: it survives a library being renamed or a machine having a different set installed.
This page is the resolution table — **which installed skill, plugin or MCP server a label actually means.**

Rules: [handbooks/08-tooling-discovery.md](08-tooling-discovery.md) · inventory: [status/TOOLING.md](../status/TOOLING.md) · catalog: [handbooks/03-skills-catalog.md](03-skills-catalog.md)

## Why labels instead of hard-coded names

Hard-coded skill names in 184 files go stale the moment a library is renamed, and a stale name is worse than a role name because it fails silently: the agent loads nothing and improvises. A label resolves through this one table, and `tools/check_skills.py` fails the build when a plan label has no mapping, or when a mapping points at something that is not installed.

`status/TOOLING.md` is the generated list of **what exists on this machine right now**. This file is the mapping from **what the work needs** to that list. When the two disagree, the checker wins and this page gets fixed.

## Session baseline (load first, every session)

These plugins change how a session runs rather than what a task knows. The subagents load them before the task-specific skills.

| Tool | What it does here |
|---|---|
| `skill:droidroute-task-runner` | the task protocol every task follows — log, verify, commit, update status |
| `plugin:superpowers` | systematic debugging, test-first development, disciplined plan execution |
| `plugin:context-mode` | keeps a long chain inside the context window; session continuity |
| `plugin:code-review` | run before every task commit |
| `plugin:code-simplifier` | cleanup pass when a task added more than it needed |
| `plugin:feature-dev` | the shape of a non-trivial feature build |
| `plugin:claude-md-management` | keeps [CLAUDE.md](../CLAUDE.md) and [AGENTS.md](../AGENTS.md) honest as the repo grows |
| `plugin:skill-creator` | when a repeated task pattern deserves its own project skill |
| `plugin:context7` | current library documentation instead of remembered API shapes |

Token syntax: `skill:<name>` = a Claude skill (global or project), `plugin:<name>` = an installed plugin, `mcp:<name>` = a configured MCP server. Every token in this file is validated against the inventory.

## The resolution table

| Role label | Resolves to |
|---|---|
| `kotlin-core` | `plugin:jvm-languages`, `skill:styles` — no Kotlin skill is installed; run `npx skills find kotlin coroutines` before inventing conventions |
| `ktor-server` | `plugin:backend-development`, `plugin:api-scaffolding` |
| `gradle-android` | `skill:agp-9-upgrade`, `skill:r8-analyzer`, `plugin:dependency-management` |
| `android-platform` | `skill:adaptive`, `skill:edge-to-edge`, `skill:appfunctions`, `plugin:multi-platform-apps` |
| `android-compose-ui` | `skill:droidroute-compose-ui`, `skill:mobile-android-design`, `skill:styles`, `plugin:frontend-design` |
| `performance-android` | `skill:android-profiler`, `skill:optimize`, `plugin:application-performance` |
| `persistence-room` | `plugin:database-design`, `plugin:database-migrations`, `plugin:database-cloud-optimization` |
| `provider-integration` | `skill:droidroute-provider-manifest`, `plugin:api-scaffolding` |
| `llm-gateway-protocols` | `plugin:llm-application-dev`, `plugin:backend-api-security` |
| `llm-routing` | `skill:droidroute-routing`, `plugin:llm-application-dev` |
| `local-inference` | `plugin:llm-finetuning`, `plugin:machine-learning-ops`, `skill:ml-kit-genai-prompt-api` |
| `mcp-protocol` | `plugin:protect-mcp`, `plugin:context7` — live MCP servers come from [status/TOOLING.md](../status/TOOLING.md), never from memory |
| `oauth-device-flow` | `skill:verified-email`, `skill:restore-credentials`, `plugin:backend-api-security` |
| `testing` | `skill:testing-setup`, `plugin:unit-testing`, `plugin:tdd-workflows`, `plugin:api-testing-observability` |
| `security-audit` | `skill:android-intent-security`, `plugin:security-guidance`, `plugin:backend-api-security`, `plugin:signed-audit-trails` |
| `ci-cd-github-actions` | `plugin:cicd-automation`, `plugin:github`, `plugin:deployment-validation`, `plugin:deployment-strategies` |
| `git-workflow` | `plugin:git-pr-workflows`, `plugin:commit-commands`, `plugin:code-review` |
| `technical-writing` | `skill:writing-guidelines`, `skill:karpathy-wiki`, `plugin:documentation-standards`, `plugin:avoid-ai-writing` |
| `droidroute-verification` | `skill:droidroute-verification` |
| `droidroute-provider-manifest` | `skill:droidroute-provider-manifest` |
| `droidroute-routing` | `skill:droidroute-routing` |
| `droidroute-compose-ui` | `skill:droidroute-compose-ui` |
| `droidroute-skill-scout` | `skill:droidroute-skill-scout` |
| `ai-governors` | `skill:ai-governors` |
| `ai-trust-builders` | `skill:ai-trust-builders` |
| `android-intent-security` | `skill:android-intent-security` |
| `android-profiler` | `skill:android-profiler` |
| `karpathy-audit` | `skill:karpathy-audit` |

## Loading order in one task

1. Read the task file and `status/NEXT.md`.
2. Resolve both role labels through the table above.
3. Load `skill:droidroute-task-runner` and run the session baseline plugins' relevant parts (usually `superpowers` for test-first, `context-mode` for a long chain).
4. Dispatch `implementer` with the primary label's tools and `verifier` with the verification label's tools — in parallel, per [handbooks/02-subagent-orchestration.md](02-subagent-orchestration.md).
5. Check the inventory once for anything new: `python3 scripts/discover_tooling.py --check-fresh`. If it is stale, regenerate and commit.

## When nothing fits

Search before improvising:

```bash
npx skills find <query>                              # community index
npx skills add <owner/repo> --list                   # preview before installing
npx skills add <owner/repo> --skill <name> --yes      # install — ask the owner first
```

A community skill is unvetted and outside this repository's control. Never install one that needs credentials the owner does not hold, and never install silently.

If the gap is a repeated pattern in *this* project, write a project skill in `.claude/skills/` instead (use `plugin:skill-creator`), then add it to this table so the next agent finds it.

## Substituting a label

Deviating is allowed; hiding it is not. Record it in the task log and the commit body:

```
skill-substitution: testing -> debugging-toolkit (the failure is a runtime crash, not a missing test)
```

One line, in the log, in the same commit as the change.

## How this page is enforced

```bash
python3 tools/check_skills.py
```

- Fails if a label used in `plan/` has no row here.
- Fails if a `skill:` / `plugin:` / `mcp:` token here is not in `status/tooling.json`.
- Warns about rows that no task uses, so the table does not accumulate dead weight.

Wired into `.github/workflows/repo-hygiene.yml`. When you add a label to a task, add its row in the same commit.
