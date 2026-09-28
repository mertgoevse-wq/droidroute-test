<div align="center">

# DroidRoute

**Your phone is the gateway. Every model, one endpoint.**

[![Build APK](https://github.com/mertgoevse-wq/droidroute/actions/workflows/build-apk.yml/badge.svg)](https://github.com/mertgoevse-wq/droidroute/actions/workflows/build-apk.yml)
[![Repo hygiene](https://github.com/mertgoevse-wq/droidroute/actions/workflows/repo-hygiene.yml/badge.svg)](https://github.com/mertgoevse-wq/droidroute/actions/workflows/repo-hygiene.yml)
[![Kotlin](https://img.shields.io/badge/Kotlin-2.0-7F52FF?logo=kotlin&logoColor=white)](https://kotlinlang.org)
[![Android](https://img.shields.io/badge/Android-minSdk%2026%20%C2%B7%20target%2035-3DDC84?logo=android&logoColor=white)](https://developer.android.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)

</div>

---

DroidRoute is an **Android-native AI gateway**. It runs a local server on your phone and speaks the three formats coding agents already understand — **OpenAI**, **Anthropic** and **Gemini** — so Claude Code, Freebuff and anything else can point at `http://127.0.0.1:8787` and stop caring which provider paid for the answer.

Built for a Galaxy A56 running Termux + proot-Debian, designed to reach functional parity with [OmniRoute](https://github.com/diegosouzapw/OmniRoute), absorb what [9Router](https://github.com/decolua/9router), CLIProxyAPI and LiteLLM do — natively, with no Node or Python runtime — and then go past all of them.

## What it does

| | |
|---|---|
| **One endpoint, three wire formats** | OpenAI `/v1/*`, Anthropic `/v1/messages`, Gemini `/v1beta/*` + media (images, audio) |
| **Provider breadth** | OmniRoute's provider set plus the owner's named extras: **Bynara**, **FreeLLMAPI**, **APInex**, **GoRouter**, **xKiro**, **TokenRouter**, **TokenReply**, **FastRouter**, **Experiential Labs** — manifest-driven, extensible without an app update |
| **Bring your own provider** | Form: base URL, compat, key → models discovered automatically, manual fallback |
| **Any provider, one paste** | Probe an unknown endpoint and infer its dialect (OpenAI, Anthropic, Gemini, Responses), discover its models, generate a manifest to confirm |
| **Migration importers** | Paste a config from OmniRoute, 9Router, LiteLLM, one-api/new-api or CLIProxyAPI and keep working |
| **Offline-first** | With a local model loaded, answer with no connectivity; queue what only a cloud provider can do and replay it when the network returns |
| **Phone-aware routing** | Battery floor, thermal ceiling and a metered-connection policy — decisions no server-side gateway can make |
| **Conversation affinity** | Pin a conversation to one provider so provider-side prompt caches survive instead of being re-billed on every model switch |
| **Android surfaces** | Quick Settings tile, home-screen widget, share sheet and text-selection action |
| **Updates itself** | Checks its own GitHub releases, verifies the APK signature, installs, and can roll back; provider knowledge arrives as signed catalog packs between releases |
| **Offline model catalog** | Sizes, quants, licences, checksums and device-fit scores, usable in airplane mode |
| **Subscription accounts** | Google AI Pro (OAuth), Perplexity **Sonar** search, GitHub Copilot, HuggingFace |
| **Failover that actually fails over** | Automatic candidate chain on timeout, `401`, `429`, `5xx` |
| **Quota-aware key rotation** | Multiple keys per model, **even across different providers** — one quota runs dry, the next switches in automatically |
| **Combos & auto models** | Named model chains plus zero-config virtual models (`auto`, `auto/coding`, `auto/fast`, `auto/cheap`, `auto/offline`, `auto/smart`, `auto/lkgp`) |
| **19 routing strategies** | priority, fill-first, weighted, round-robin, p2c, least-used, random, strict-random, cost-optimized, headroom, reset-window, reset-aware, context-relay, context-optimized, cache-optimized, lkgp, auto, fusion, pipeline — all composable and explainable via `/v1/routing/explain` |
| **Cost & quota telemetry** | per-provider tokens, cache-hit savings, `X-DroidRoute-*` headers, per-key USD budgets |
| **Guardrails** | prompt-injection screening and credential masking, both with a documented scope |
| **Local models** | llama.cpp in Termux (embedded runtime later), no artificial size cap — with honest RAM warnings |
| **Mobile-data accounting** | Bytes per provider and per network type, with a monthly budget and an optional hard stop |
| **Config portability** | Move a whole setup to a new phone by QR code, encrypted under a passphrase — no account, no cloud |
| **MCP federation** | Discovers the MCP servers Claude Code and Freebuff already use, aggregates them, and bridges tool calls over `POST /mcp/{id}` |
| **Security** | Keys in the Android Keystore, revealed once, then masked `first5••••last5`. Nothing secret ever reaches this repo |
| **Bilingual UI** | Deutsch (default) + English |

## Architecture in one picture

```
Claude Code ─┐                                    ┌─▶ Bynara · FreeLLMAPI · APInex · GoRouter
Freebuff ────┼──▶ http://127.0.0.1:8787 ───────────┼─▶ OpenRouter · Groq · Cerebras · Gemini
other agents ┘    OpenAI · Anthropic · Gemini      └─▶ OpenAI · Anthropic · Perplexity · …
                  ▲
                  │  Kotlin/Compose app · foreground service · Keystore vault
                  └─ llama.cpp (Termux) · MCP servers · connectors
```

Details: [`docs/01-architecture.md`](docs/01-architecture.md) · [`docs/02-protocols.md`](docs/02-protocols.md) · [`docs/04-routing.md`](docs/04-routing.md)

## Quick start

1. **Install** — download the debug APK from the latest [build run](https://github.com/mertgoevse-wq/droidroute/actions/workflows/build-apk.yml) (Artifacts) or build it yourself: `./gradlew :app:assembleDebug`.
2. **Configure** — set the port (default `8787`) and bind mode (default: local only).
3. **Connect a provider** — one-click for a free gateway, or paste a key. Keys are masked after entry.
4. **Point your agents at it:**

```bash
# Termux / proot-Debian
export ANTHROPIC_BASE_URL=http://127.0.0.1:8787
export OPENAI_BASE_URL=http://127.0.0.1:8787/v1
# scripts/termux-setup.sh --persist  does this for you
```

5. **Verify** — `curl http://127.0.0.1:8787/health`

## Letting an agent build it

Open a terminal in this folder, start Claude Code, and give it the code word from [`KICKOFF.md`](KICKOFF.md):

```text
Anlauf-8787
```

It reads the rules, picks up where the state files say, and works through the plan task by task — two skills in parallel per task, every step logged, one commit and push per task, resumable at any point.

## This repository builds itself

This repo is not documentation *about* DroidRoute — it is the build plan. [`plan/`](plan/INDEX.md) holds **190 task files** across 15 phases; an agent (Claude Code or Freebuff) executes them in order, using **at least two skills in parallel via subagents** per task, logging every step and committing + pushing after each one. Any other model can resume from [`status/`](status/PROGRESS.md) alone.

| Start here | Purpose |
|---|---|
| [`AGENTS.md`](AGENTS.md) | operating rules for any coding agent (canonical) |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code entry point |
| [`KICKOFF.md`](KICKOFF.md) | **the start file** — hand its code word to an agent and it builds the whole project |
| [`plan/INDEX.md`](plan/INDEX.md) | all 190 tasks, phases and dependencies |
| [`status/PROGRESS.md`](status/PROGRESS.md) | what is done — resume from here |
| [`status/TOOLING.md`](status/TOOLING.md) | which skills, plugins and MCP servers are installed and how to use them |
| [`.claude/skills/`](.claude/skills/) | six project skills (task runner, verification, provider, routing, UI, scout) |
| [`.claude/agents/`](.claude/agents/) | four subagents: implementer, verifier, chronicler, tooling-scout |
| [`handbooks/`](handbooks/01-agent-handbook.md) | agent handbook, subagent orchestration, skills catalog, git + logging protocol, tooling discovery, skill resolution |
| [`handbooks/09-skill-resolution.md`](handbooks/09-skill-resolution.md) | which role label a task names means which installed skill, plugin or MCP server |
| [`docs/12-omniroute-parity.md`](docs/12-omniroute-parity.md) | OmniRoute feature parity, and what DroidRoute does beyond it |
| [`docs/13-competitive-landscape.md`](docs/13-competitive-landscape.md) | 9Router, CLIProxyAPI, LiteLLM and friends: what is absorbed, what is different, what is refused |
| [`docs/droidroute-spec.md`](docs/droidroute-spec.md) | the original master specification |

## Repository layout

```
.claude/     project skills, four subagents, settings (permissions, project MCP auto-enable)
docs/        architecture, protocols, providers, routing, security, acceptance, OmniRoute parity, competitive landscape, TBC resolutions, DE glossary
handbooks/   agent handbook, subagent orchestration, skills catalog, git + logging + resume protocol, tooling discovery, anti-slop rules
plan/        190 task files in 15 phases, plus INDEX.md
status/      PROGRESS · NEXT · DECISIONS · ERRORS · TOOLING (generated inventory) · per-component state · daily summaries
logs/        chain log, per-task logs, daily roll-ups (pruned weekly)
scripts/     step-commit, log-step, secrets preflight, tooling discovery, weekly cleanup, termux setup, local APK build
tools/       plan generator + phase data (how the 190 task files are produced from the spec), link, skill, design and consistency checkers
.github/     build-apk + repo-hygiene workflows, issue/PR templates
```

## Ground rules

- **No secret ever enters this repository.** A pre-commit preflight enforces it, and MCP environment values are recorded by name only.
- **No placeholders, no invented URLs, no unrequested refactors.** See [`handbooks/07-anti-slop-rules.md`](handbooks/07-anti-slop-rules.md).
- **Every step is logged, committed and pushed** so work is never trapped in one session.
- **Use the tools that exist.** The build agents read the generated inventory ([`status/TOOLING.md`](status/TOOLING.md)) before writing their own procedure — MCP server, then project skill, then global skill.

## License

MIT — see [`LICENSE`](LICENSE).
