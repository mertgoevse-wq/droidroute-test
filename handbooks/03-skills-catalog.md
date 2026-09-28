# Skills Catalog

Every task names at least two skills from this catalog (or a better one the host provides). A skill is an instruction pack, not a library. Use the specific skill over the generic one.

## Core build skills

| Skill | Purpose | Used in |
|---|---|---|
| `kotlin-core` | Idiomatic Kotlin 2.x: coroutines, flows, null-safety, data classes, sealed hierarchies | all app code |
| `android-compose-ui` | Compose + Material 3 screens, state hoisting, theming, previews | `plan/phase-07-ui/` |
| `android-platform` | Foreground service, notifications, permissions, Keystore, intents, doze | `phase-01`, `phase-05`, `phase-08` |
| `ktor-server` | Embedded Ktor/CIO server, routing DSL, plugins, SSE | `phase-01`, `phase-05` |
| `gradle-android` | Modules, version catalogs, flavors, signing, R8 | `phase-00`, `phase-11` |
| `persistence-room` | Entities, DAOs, migrations, transactions | `phase-01`, `phase-02` |

## Domain skills

| Skill | Purpose | Used in |
|---|---|---|
| `llm-gateway-protocols` | OpenAI/Anthropic/Gemini wire formats, streaming, tool calls, error mapping | `phase-05` |
| `provider-integration` | Reading a provider's real docs, writing a manifest, validating a key with a live call | `phase-02`, `phase-03` |
| `llm-routing` | Candidate ordering, scoring, quota ledgers, circuit breaking, aliasing | `phase-06` |
| `oauth-device-flow` | Google/GitHub/HuggingFace OAuth, token refresh, redirect handling on Android | `phase-04` |
| `local-inference` | llama.cpp/whisper.cpp runtime resolution, GGUF quantisation, RAM budgeting | `phase-08` |
| `mcp-protocol` | Discovery, stdio/http transports, JSON-RPC tool calls, schema handling | `phase-09` |
| `security-audit` | Secret handling, redaction, bind modes, permission minimisation, threat review | every phase, mandatory in `phase-11` |

## Process skills

| Skill | Purpose | Used in |
|---|---|---|
| `testing` | Unit/instrumented test design, failure injection, flakiness control | every task's verify workstream |
| `technical-writing` | Accurate, filler-free docs; decision records | all doc/status updates |
| `git-workflow` | Commit hygiene, checkpoint tags, push recovery, conflict avoidance | every commit |
| `ci-cd-github-actions` | Workflow authoring, caching, artifacts, signing secrets | `phase-00`, `phase-11` |
| `performance-android` | Battery, memory, wake-locks, startup time, Compose recomposition | `phase-07`, `phase-11` |

## Choosing for a task

The default trio is `implement-skill` + `testing` + `technical-writing`. Replace one when the task is clearly about something else: an OAuth task wants `oauth-device-flow` + `security-audit` + `testing`; an MCP task wants `mcp-protocol` + `testing` + `technical-writing`.

**Never** run a task with fewer than two parallel skills, and never without a verification skill.

## Skills the host may have

Claude Code and Freebuff each ship their own skill libraries; the inventory can differ from the names above. Before substituting, check the host's real inventory (Claude Code: its skill directory; Freebuff: `/plugins`-style listing). Prefer an installed skill with the same intent over a generic instruction. Record substitutions in the task log:

```
skill-substitution: security-audit → manual-checklist (host has no security skill installed)
```
