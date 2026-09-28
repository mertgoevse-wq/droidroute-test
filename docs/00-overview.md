# DroidRoute — Overview

## What it is

DroidRoute is an **Android-native AI gateway**. It runs a local HTTP server on the phone and speaks the three wire formats coding agents expect — **OpenAI**, **Anthropic** and **Google Gemini** — plus media endpoints. Claude Code, Freebuff and any other agent connect to `http://127.0.0.1:8787` and never need to know which upstream provider actually served the request.

It is *not* a port of OmniRoute. It reaches functional parity with OmniRoute and then goes further: multi-key quota rotation, health- and cost-aware routing, subscription (OAuth) accounts, on-device local models, and MCP/plugin/connector federation.

## Why it exists

The owner runs Claude Code and Freebuff inside Termux (proot-distro Debian) on a Galaxy A56, with accounts spread across a Google AI Pro subscription, Perplexity Pro, and a long list of credit-heavy gateways. Manually switching base URLs and keys per provider is the bottleneck. DroidRoute turns all of that into one endpoint with automatic failover.

## Scope at a glance

| Area | Summary | Detail |
|---|---|---|
| Local server | Foreground service, configurable port, localhost by default | `docs/01-architecture.md` |
| Wire formats | OpenAI + Anthropic + Gemini + media, streaming | `docs/02-protocols.md` |
| Providers | ~50 manifest-driven adapters, owner-extensible | `docs/03-providers.md` |
| Routing | Failover, multi-key rotation, strategies, health/cost | `docs/04-routing.md` |
| Security | Keystore vault, 5/5 masking, three auth modes | `docs/05-security.md` |
| Local models | llama.cpp via Termux, embedded later | `docs/06-local-models.md` |
| MCP | Discovery from Termux/Debian + own list, bridge API | `docs/07-mcp-plugins.md` |
| Build workflow | One-shot autonomous build, logged and pushed | `docs/08-workflow.md` |
| Release | GitHub Actions APK + Termux fallback | `docs/09-build-and-release.md` |
| Acceptance | 13 objective proof points | `docs/10-acceptance.md` |
| Decisions | All TBC points resolved | `docs/11-tbc-resolutions.md` |
| OmniRoute parity | Feature matrix: parity, beyond, or not planned with the reason | `docs/12-omniroute-parity.md` |
| Build-agent tooling | Which skills, plugins and MCP servers exist and how to use them | `status/TOOLING.md`, `handbooks/08-tooling-discovery.md` |

## Non-goals

- No multi-tenant hosting — one owner, one device.
- No Play Store release in v1 (sideloaded APK).
- No cloud control plane — nothing leaves the phone except the upstream API calls the owner configured.
- No plaintext secrets in the repository, ever.

## The build system

This repository is designed to be built by agents. `plan/` holds **166 task files** across 13 phases; `handbooks/` holds the orchestration rules; `status/` holds the resume state — including `status/TOOLING.md`, the generated inventory of installed skills, plugins and MCP servers, so an agent uses what exists instead of re-inventing it. A single agent (Claude Code *or* Freebuff) can execute the plan end to end: every task names at least two skills to run **in parallel via subagents** (four are predefined in `.claude/agents/`), and every completed step is logged, committed and pushed so any other model can take over mid-flight.

Start reading at [`CLAUDE.md`](../CLAUDE.md) (Claude Code) or [`AGENTS.md`](../AGENTS.md) (any other agent).

## Status

Planning phase complete, implementation not started. See [`status/PROGRESS.md`](../status/PROGRESS.md).
