# Skills Catalog

**Rule: at least two skills per task, in parallel, one of them verification.**

This catalog is grounded in what is actually installed. The live list is `status/TOOLING.md` (generated); this page explains *which ones to reach for and why*.

**Task files name role labels, not tool names** (`kotlin-core`, `provider-integration`, `testing`, …). [`handbooks/09-skill-resolution.md`](09-skill-resolution.md) is the table that turns each label into the installed skills, plugins and MCP servers to load, and `tools/check_skills.py` fails the build when a label has no row or a row points at something that is not installed. Resolve the labels there first; use this page to choose between the resulting tools.

## Project skills (authoritative here)

| Skill | Use for |
|---|---|
| `droidroute-task-runner` | executing any task from `plan/` end to end |
| `droidroute-verification` | the mandatory verification workstream |
| `droidroute-provider-manifest` | adding or changing a provider (phases 2–4) |
| `droidroute-routing` | routing, quotas, key chains, failover (phase 6, phase 12) |
| `droidroute-compose-ui` | any Compose screen or visual work (phase 7) |
| `droidroute-skill-scout` | finding the right tool before improvising |

Four matching subagents live in `.claude/agents/`: `implementer`, `verifier`, `chronicler`, `tooling-scout`. Dispatch at least `implementer` + `verifier` per task, and `chronicler` when docs, status or logs change.

## Global skills worth knowing (from the installed library)

**Android / Kotlin — the project's home domain**

| Skill | Use for |
|---|---|
| `mobile-android-design` | Material 3 structure and interaction defaults |
| `adaptive`, `edge-to-edge` | window sizes, insets, multi-pane, modern system bars |
| `testing-setup` | test infrastructure for a native Android app |
| `navigation-3`, `navigation-event` | navigation graphs and predictive back |
| `android-profiler`, `optimize` | jank, memory, battery, startup |
| `android-cli` | device/emulator control from the command line |
| `android-intent-security` | intent redirection and component exposure review |
| `r8-analyzer`, `agp-9-upgrade` | build and shrinker work |
| `play-policy-insights`, `restore-credentials`, `verified-email`, `ml-kit-genai-prompt-api`, `appfunctions` | specific platform integrations worth reading before writing custom code |
| `styles` | the Compose Styles API, useful for the theme layer |

**Design, UX and polish — for every screen**

`impeccable`, `design-review`, `design-analysis`, `critique`, `audit`, `polish`, `craft`, `typeset`, `layout`, `colorize`, `bolder`, `quieter`, `distill`, `clarify`, `animate`, `delight`, `accessibility`, `high-end-visual-design`, `minimalist-ui`, `web-design-guidelines`, plus the curated `design-library` (~60 indexed entries) for on-demand depth.

**Process — how the chain is run**

`planning-with-files` (and its language variants), `flylab-autonomous-orchestrator`, `autoresearch`, `karpathy-audit` / `karpathy-diff` / `karpathy-refactor` / `karpathy-wiki`, `low-effort-high-reward`, `feature-prioritization`, `project-stage-detect`, `full-output-enforcement`, `writing-guidelines`.

**AI behaviour — relevant because the product is an AI gateway**

`ai-governors` (human-in-the-loop control), `ai-identifiers`, `ai-inputs`, `ai-trust-builders`, `ai-tuners`, `ai-wayfinders`.

**Plugins that change how a session runs**

`context-mode` (context-window reduction, session continuity, indexed search), `superpowers` (systematic debugging, test-driven development, plan execution), `feature-dev`, `code-review`, `code-simplifier`, `frontend-design`, `skill-creator`. Check `status/TOOLING.md` for the current list and versions.

## Selection matrix by phase

| Phase | Primary skill | Verification / second stream |
|---|---|---|
| 00 Foundation | `planning-with-files` | `droidroute-verification`, `writing-guidelines` |
| 01 Core server | `mobile-android-design` + `android-intent-security` | `testing-setup` |
| 02 Provider framework | `droidroute-provider-manifest` | `droidroute-verification` |
| 03 Provider catalog | `droidroute-provider-manifest` | `droidroute-verification` |
| 04 Accounts & OAuth | `android-intent-security` | `testing-setup`, `droidroute-verification` |
| 05 Wire protocols | `droidroute-provider-manifest` | `testing-setup` |
| 06 Routing | `droidroute-routing` | `droidroute-verification`, `android-profiler` |
| 07 UI | `droidroute-compose-ui` + one design skill | `accessibility`, `optimize` |
| 08 Local models | `android-profiler` + `local-inference` guidance in `docs/06` | `testing-setup` |
| 09 MCP & plugins | `appfunctions` for capability thinking | `droidroute-verification` |
| 10 Logging & handover | `karpathy-wiki`, `writing-guidelines` | `droidroute-verification` |
| 11 Delivery | `audit` + `security-audit` intent via `android-intent-security` | `testing-setup`, `r8-analyzer` |
| 12 OmniRoute parity | `droidroute-routing`, `ai-governors` | `droidroute-verification`, `optimize` |
| 13 Competitive edge | `droidroute-provider-manifest`, `android-platform` | `droidroute-verification`, `android-profiler`, `android-intent-security` |

## Choosing well

1. **Resolve the label first.** A role label is stable; the tool behind it can change. [`handbooks/09-skill-resolution.md`](09-skill-resolution.md) owns that mapping, and `tools/check_skills.py` proves it still points at something installed.
2. **Specific beats generic.** `android-intent-security` outperforms a hand-rolled security checklist for intent review.
3. **Project beats global** where both apply — the project skill carries this repository's constraints.
4. **Verification is never optional.** One of the two streams must be able to say "no".
5. **Deviate, but log it:** `skill-substitution: <old> -> <new> (<reason>)`.
6. **Do not chain five skills "just in case".** Two or three focused streams beat a committee; extra streams cost context and produce conflicting edits.

## Searching beyond the installed set

```bash
npx skills find <query>                              # community index
npx skills add <owner/repo> --list                   # preview
npx skills add <owner/repo> --skill <name> --yes     # install (ask the owner first)
```

Community skills are unvetted. Never install one that needs credentials you do not hold, and never install silently — `handbooks/08-tooling-discovery.md` has the rule.
