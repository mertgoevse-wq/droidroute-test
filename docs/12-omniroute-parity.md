# OmniRoute Parity Matrix

DroidRoute is **not** a port of [OmniRoute](https://github.com/diegosouzapw/OmniRoute). It reaches functional parity and then adds what the owner asked for on top. This document is the contract for that claim: every row names the task that delivers it, or says plainly that it is not planned and why.

> Verified against OmniRoute's own README and feature pages (359 providers, 1200+ models, quota-aware auto-fallback, adaptive admission, token compression, MCP/A2A, combos, 19 routing strategies, cost telemetry). **Parity is the floor, never the ceiling.**

Legend: **P** = parity (same capability) · **+** = beyond OmniRoute · **–** = not planned (with reason)

## Core routing

| # | OmniRoute capability | DroidRoute | Task |
|---|---|---|---|
| 1 | One OpenAI-compatible endpoint on localhost | **P** — plus Anthropic and Gemini surfaces on the same port | T-011, T-067, T-070, T-073 |
| 2 | 352+ providers, 150+ free, 1200+ models | **P** — manifest-driven catalogue, owner-extensible without an app update | T-024…T-054 |
| 3 | Quota-aware auto-fallback | **P** — candidate chain with quota, health and breaker awareness | T-081, T-087 |
| 4 | Combos: chains of models routed across automatically | **P** | T-148 |
| 5 | Virtual combos: `auto`, `auto/coding`, `auto/fast`, `auto/cheap`, `auto/offline`, `auto/smart`, `auto/lkgp`, `auto/chaos` | **P** | T-148, T-151 |
| 6 | 19 routing strategies (priority, fill-first, weighted, round-robin, p2c, least-used, random, strict-random, cost-optimized, headroom, reset-window, reset-aware, context-relay, context-optimized, cache-optimized, lkgp, auto, fusion, pipeline) | **P** — all 19 | T-084, T-149, T-150 |
| 7 | 16-factor auto scoring engine | **P** | T-151 |
| 8 | Three independent resilience layers | **P** — breaker, retry policy, admission control | T-086, T-152 |
| 9 | Adaptive admission / overload protection (queue instead of 503) | **P** | T-152 |
| 10 | Atomic RPM rolling leases per connection | **P** | T-152 |
| 11 | Quota-Share routing across pooled keys (work-conserving) | **P** | T-156 |
| 12 | **Multiple keys per model, across different providers** | **+** beyond OmniRoute's pool model: a logical model bound to a chain spanning independent gateways | T-083 |
| 13 | Model aliases / owner-defined names | **P** — aliases with per-alias strategy | T-080 |
| 14 | Canonical `/v1/models` ordering (provider-grouped, combos first) | **P** | T-164 |
| 15 | `last-known-good` provider stickiness | **P** (`lkgp` strategy) | T-149 |

## Quota, cost and telemetry

| # | OmniRoute capability | DroidRoute | Task |
|---|---|---|---|
| 16 | Quota telemetry, live dashboard | **P** — plus a free-tier catalogue view | T-095, T-164 |
| 17 | Cost telemetry headers on every endpoint (`X-OmniRoute-*`) | **P** as `X-DroidRoute-*`, including cache-hit savings | T-155 |
| 18 | Per-key USD spend quotas | **P** | T-155 |
| 19 | Honest flat-rate handling (subscription providers read $0) | **P** — same rule, plus "what would this have cost" for free tiers | T-155, T-095 |
| 20 | Free-tier methodology and catalogue (`/dashboard/free-tiers`) | **P** — with per-provider reset semantics and learned windows | T-082, T-164 |
| 21 | Prompt-cache hit maximisation (prefix pinning) | **P** | T-154 |
| 22 | Token compression (RTK + Caveman, 12 engines, 15–95 % savings) | **P** — a smaller, measurable, opt-out-able engine set | T-153 |

## Media and modalities

| # | OmniRoute capability | DroidRoute | Task |
|---|---|---|---|
| 23 | Vision + audio + video modality bridge | **P** | T-160 |
| 24 | Image generation endpoints | **P** | T-075 |
| 25 | Video generation endpoint | **P** | T-162 |
| 26 | Speech synthesis and transcription | **P** — plus on-device whisper.cpp | T-075, T-115 |
| 27 | `/v1/ocr` | **P** | T-161 |
| 28 | `/v1/audio/translations` | **P** | T-161 |
| 29 | Embeddings | **P** — hosted and on-device | T-076, T-114 |

## Agents, MCP and A2A

| # | OmniRoute capability | DroidRoute | Task |
|---|---|---|---|
| 30 | MCP support (server side) | **P** — DroidRoute federates the agent's existing servers instead of only exposing its own | T-118…T-126 |
| 31 | A2A delegation to an agent fleet | **P** — inbound A2A with capability advertisement | T-163 |
| 32 | `omniroute run` launches 7 CLIs; 13 setup commands; 10 configure targets | **P** — a setup command per client (Claude Code, Freebuff, Codex-style, Gemini CLI, generic OpenAI) | T-165 |
| 33 | MCP/A2A control panel | **P** — connectors screen with real state | T-123 |

## Platform, accounts and safety

| # | OmniRoute capability | DroidRoute | Task |
|---|---|---|---|
| 34 | Subscription / coding-plan connections (OAuth) | **P** — Google AI Pro, GitHub, HuggingFace, plus provider OAuth | T-055…T-059 |
| 35 | Subscription accounts used without an API key | **P** where the provider allows it; **honest labelling** where it does not | T-062, T-056 |
| 36 | Perplexity search integration | **P** — Sonar with citations, plus a search façade endpoint | T-060, T-061 |
| 37 | Web-search last resort | **P** — optional provider-independent fallback | T-161 |
| 38 | Prompt-injection guard on every LLM route | **P** | T-158 |
| 39 | Credential-masking guardrail (redact leaked secrets both directions) | **P** — and the same redactor protects this repository's logs | T-159, T-008 |
| 40 | Memory subsystem (opt-in, vector, decay) | **P** — local only, opt-in, per-request off switch | T-157 |
| 41 | OIDC/basic login gate for the dashboard | **P** in app terms — client keys plus device-credential protection for secrets | T-016, T-099 |
| 42 | Remote mode with scoped tokens | **P** | T-165 |
| 43 | Reverse-proxy basePath support | **P** | T-152 |
| 44 | Multi-language UI (browser auto-detect, i18n) | **P** — German default, English available | T-093 |
| 45 | Desktop/PWA front-end | **+** — a native Android app, a foreground service and an on-device model runtime instead | T-007, T-011 |
| 46 | Free-tier signup guidance / provider coupons | **P** — one-click connect with the provider's own key page | T-096 |
| 47 | Ollama-style local model card | **P** — llama.cpp managed on-device | T-107…T-117 |
| 48 | Radar opt-in catalog overlay | **–** — the owner wants local-only behaviour; a remote catalogue overlay is a network dependency this project deliberately avoids. Revisit only if the provider list proves too static. | — |
| 49 | Transparent MITM/TPROXY decrypt for CLIs ignoring proxy env | **–** — requires a CA in the device trust store and intercepts TLS on a personal phone. The point of DroidRoute is a *local* endpoint that clients are configured to use, not traffic interception. | — |
| 50 | Cloud agent endpoints (Codex Cloud, Cursor, Devin, Jules) | **–** — those are vendor-hosted agent services, not model providers. Out of scope until a task proves a concrete use. | — |
| 51 | ~1.62 B free tokens/month marketing headline | **P** in substance — the free-tier catalogue and quota ledger make the real number visible instead of asserted | T-164, T-082 |

## The owner's wishes, beyond parity

These are requirements from the interview that OmniRoute does not offer at all:

| Wish | DroidRoute | Task |
|---|---|---|
| Native Android app, not a desktop/PWA server | Kotlin + Compose with a foreground service | T-007, T-091 |
| Keys stored hardware-encrypted, revealed once, then masked `first5••••last5` | Keystore vault and a dedicated key UX | T-006, T-099 |
| Local models of any size, with honest RAM warnings instead of an artificial cap | llama.cpp via Termux, memory guard, curated catalogue | T-107…T-117 |
| 135+ project files that let an agent rebuild/resume the whole product autonomously | 208-task plan across 18 phases, plus handbooks, bootstrap and status automation | `plan/`, `handbooks/`, `scripts/bootstrap.sh`, `KICKOFF.md` |
| Minimum two skills per task, run in parallel via subagents | `handbooks/02`, `.claude/agents/`, `.claude/skills/` | T-001…T-165 (every task) |
| Every step logged, committed and pushed; any model can take over | logging standard, step commits, handover bundle, resume drills | T-127…T-135 |
| Global + project discovery of plugins, MCP servers and skills | `scripts/discover_tooling.py`, `status/TOOLING.md` | T-166 |
| Role labels in the plan resolve to installed skills/plugins/MCP servers, enforced by a checker | `handbooks/09-skill-resolution.md`, `tools/check_skills.py` | T-166 |
| Everything the other routers do, with the gaps named | `docs/13-competitive-landscape.md` | T-167 … T-184 |
| An interface built from a written design system, with a gate that fails the build on banned aesthetics | `docs/14-design-system.md`, `tools/check_design_slop.py` | T-185 … T-190 |
| One code word that hands the whole build to an agent | `KICKOFF.md` | — |
| Security and privacy audit with a test per threat | `docs/16-threat-model.md`, `docs/17-security-audit.md` | T-191 … T-196 |
| Screenshots analysed by a machine, a README gallery CI keeps true, a launch video from the real product | `design/`, `tools/analyse_shots.py`, `plugin:brag` | T-197 … T-202 |
| Free start with one tap, DroidRoute keys that nobody can read back, tooling coverage as a reviewed decision | `KICKOFF.md`, `status/TOOLING-COVERAGE.md` | T-203 … T-208 |
| Routing decision explainable from the phone | `/v1/routing/explain` and the explain viewer | T-089, T-101 |

## How this list is maintained

A feature is only marked `P` when its task exists in `plan/` and its acceptance criteria are specific. Marketing claims from any provider are not evidence — `handbooks/07-anti-slop-rules.md` forbids repeating them as fact.

When a parity task is re-scoped, edit this table in the same commit. The table is checked against the plan by `python3 tools/check_providers.py` for provider rows and manually for the rest; a row that names a non-existent task is a defect.
