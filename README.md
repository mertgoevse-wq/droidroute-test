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

Built for a Galaxy A56 running Termux + proot-Debian, designed to reach functional parity with [OmniRoute](https://github.com/diegosouzapw/OmniRoute) and go past it.

## What it does

| | |
|---|---|
| **One endpoint, three wire formats** | OpenAI `/v1/*`, Anthropic `/v1/messages`, Gemini `/v1beta/*` + media (images, audio) |
| **Provider breadth** | OmniRoute's provider set plus the owner's named extras: **Bynara**, **FreeLLMAPI**, **APInex**, **GoRouter**, **xKiro**, **TokenRouter**, **TokenReply**, **FastRouter**, **Experiential Labs** — manifest-driven, extensible without an app update |
| **Bring your own provider** | Form: base URL, compat, key → models discovered automatically, manual fallback |
| **Subscription accounts** | Google AI Pro (OAuth), Perplexity **Sonar** search, GitHub Copilot, HuggingFace |
| **Failover that actually fails over** | Automatic candidate chain on timeout, `401`, `429`, `5xx` |
| **Quota-aware key rotation** | Multiple keys per model, **even across different providers** — one quota runs dry, the next switches in automatically |
| **Routing strategies** | `free_first`, `fastest`, `cheapest`, `most_quota`, `healthiest`, `round_robin`, `priority`, `manual` — composable, explainable via `/v1/routing/explain` |
| **Local models** | llama.cpp in Termux (embedded runtime later), no artificial size cap — with honest RAM warnings |
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

## This repository builds itself

This repo is not documentation *about* DroidRoute — it is the build plan. [`plan/`](plan/INDEX.md) holds **147 task files**; an agent (Claude Code or Freebuff) executes them in order, using **at least two skills in parallel via subagents** per task, logging every step and committing + pushing after each one. Any other model can resume from [`status/`](status/PROGRESS.md) alone.

| Start here | Purpose |
|---|---|
| [`AGENTS.md`](AGENTS.md) | operating rules for any coding agent (canonical) |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code entry point |
| [`plan/INDEX.md`](plan/INDEX.md) | all 147 tasks, phases and dependencies |
| [`status/PROGRESS.md`](status/PROGRESS.md) | what is done — resume from here |
| [`handbooks/`](handbooks/01-agent-handbook.md) | agent handbook, subagent orchestration, git + logging protocol |
| [`docs/droidroute-spec.md`](docs/droidroute-spec.md) | the original master specification |

## Repository layout

```
docs/        architecture, protocols, providers, routing, security, acceptance, TBC resolutions, DE glossary
handbooks/   agent handbook, subagent orchestration, skills catalog, git + logging + resume protocol, anti-slop rules
plan/        147 task files in 12 phases, plus INDEX.md
status/      PROGRESS · NEXT · DECISIONS · ERRORS · per-component state · daily summaries
logs/        chain log, per-task logs, daily roll-ups (pruned weekly)
scripts/     step-commit, log-step, secrets preflight, weekly cleanup, termux setup, local APK build
tools/       plan generator + phase data (how the 147 task files are produced from the spec)
.github/     build-apk + repo-hygiene workflows, issue/PR templates
```

## Ground rules

- **No secret ever enters this repository.** A pre-commit preflight enforces it.
- **No placeholders, no invented URLs, no unrequested refactors.** See [`handbooks/07-anti-slop-rules.md`](handbooks/07-anti-slop-rules.md).
- **Every step is logged, committed and pushed** so work is never trapped in one session.

## License

MIT — see [`LICENSE`](LICENSE).
