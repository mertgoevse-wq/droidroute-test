# TBC Resolutions

All seven open points (TBC) from `droidroute-spec.md` §10 are resolved here. These decisions are **binding** for every task file in `plan/`.

---

## TBC-1 — Default port

**Decision:** default port **8787**, user-configurable in the app (range `1024–65535`, persisted).

- Why not 20128: OmniRoute's default stays free, so both can run side by side during migration and A/B comparison.
- The port lives in one place (`ServerConfig.port`, DataStore) and is read by: the embedded HTTP server, the foreground-service notification text, the QR/connection-helper screen, and `scripts/termux-setup.sh` (which writes the matching `ANTHROPIC_BASE_URL` / `OPENAI_BASE_URL` exports).
- Changing the port while running restarts the listener gracefully (drain → rebind → resume), never silently drops in-flight requests.

## TBC-2 — External access / tunnel

**Decision: two supported modes, both off by default.**

| Mode | How | Reachability | Guard |
|---|---|---|---|
| A — Tailscale (recommended) | Tailscale Android app joined to the owner's tailnet; DroidRoute binds `0.0.0.0` in "External access" mode | Device's tailnet IP + port, e.g. `http://100.x.y.z:8787` | API key mandatory; app refuses external bind without a key |
| B — Cloudflare Tunnel (optional) | `cloudflared` inside proot-Debian points at `http://127.0.0.1:8787` | Public `https://<name>.droidroute.dev`-style hostname | Cloudflare Access service token **and** DroidRoute API key |

Rationale: Tailscale needs no root, survives reboots, and never exposes a public port. Cloudflare Tunnel is offered for cases where a device without Tailscale must connect.

**Never** allow "external bind without API key" — the app hard-blocks it and logs the refusal.

## TBC-3 — Android SDK levels

**Decision:**

| Setting | Value |
|---|---|
| `minSdk` | 26 (Android 8.0) |
| `targetSdk` | 35 (Android 15 — the Galaxy A56 shipping level) |
| `compileSdk` | 35 |
| JDK | 17 (Temurin) |
| Kotlin | 2.0.x |
| AGP | 8.7.x |
| Compose | BOM `2024.09.x`, Material 3 |
| HTTP server | Ktor 3.x with CIO engine (embedded, no Netty) |
| Serialization | kotlinx.serialization |
| Storage | Room (structured) + DataStore (preferences) |
| Secrets | `KeyVault` — AES-256-GCM, key wrapped by Android Keystore, ciphertext in app-private files |

minSdk 26 keeps the foreground-service and Keystore APIs modern while still allowing older test devices. Anything requiring API 29+ (e.g. scoped storage quirks) is guarded by runtime checks in the task file that introduces it.

## TBC-4 — MCP / plugin / connector integration

**Decision: DroidRoute acts as MCP client *and* MCP bridge.**

Discovery (read-only, on every start and on manual refresh):

| Source | Path |
|---|---|
| Claude Code | `~/.claude.json`, `~/.claude/settings.json`, `<project>/.mcp.json`, `<project>/.claude/settings.json` |
| Freebuff / Codex-style | `~/.codex/config.toml`, `~/.config/freebuff/*.json` |
| Cursor-style | `<project>/.cursor/mcp.json` |
| Owner-defined | `~/.droidroute/mcp.json` (manual entries, wins on id collision) |

Aggregation: merged into `~/.droidroute/mcp.registry.json` with `source`, `transport` (`stdio` | `http` | `sse`), `command`/`url`, `enabled`, `last_status`, `tools[]`.

Exposure over the local API:

| Endpoint | Meaning |
|---|---|
| `GET /mcp/servers` | aggregated registry (secrets redacted) |
| `POST /mcp/servers/{id}/ping` | liveness + tool list refresh |
| `POST /mcp/{id}` | JSON-RPC pass-through (`initialize`, `tools/list`, `tools/call`) |
| `GET /mcp/tools` | flattened tool index across all enabled servers |

Rules: stdio servers are launched inside the Termux/Debian environment (never in the app process); secrets/env values are redacted in every HTTP response and never written into the repo.

## TBC-5 — Perplexity Sonar (Pro subscription)

**Decision: two tiers, honest about what the subscription does and does not give you.**

- **Tier A (default, official):** Perplexity API key → provider id `perplexity`, base `https://api.perplexity.ai`, models `sonar`, `sonar-pro`, `sonar-reasoning`, `sonar-reasoning-pro`, `sonar-deep-research`. OpenAI-compatible, so it reuses the generic adapter plus a `search_mode` flag that adds the `search_domain_filter`, `search_recency_filter` and `return_citations` fields, and surfaces citations in the response.
- **Tier B (experimental, off by default):** session/account mode that drives the Perplexity **web** session (cookie/token) to answer with the subscription. Only enabled behind `settings.experimentalAccountMode = true`, never used automatically by the routing engine, and displayed with a clear notice: this is not an official API, may break at any time, and may conflict with the provider's terms. It exists because the owner asked for it; it is never the default path.

Also exposed: `POST /v1/search` convenience endpoint (DroidRoute-specific) that returns `{answer, citations[], model, provider}` for direct search use.

## TBC-6 — llama.cpp binaries on aarch64 Android

**Decision: resolve at runtime, in this order, and record which one won.**

1. **Termux package** — `pkg install llama-cpp` (aarch64 build maintained by the Termux community). Preferred: smallest download, fastest setup.
2. **Build from source in proot-Debian** — `cmake -B build -DGGML_NATIVE=ON -DLLAMA_BUILD_SERVER=ON -DCMAKE_BUILD_TYPE=Release`, then `build/bin/llama-server`. Used when the package is missing or too old for the requested model architecture.
3. **Prebuilt upstream `llama-server` release** for `linux-arm64`, unpacked into `~/.droidroute/runtimes/llama.cpp/<version>/`.

The app never bundles binaries in the APK in v1 (keeps the APK small and avoids GPL/ABI surprises); instead it manages whichever runtime resolved. "Embedded runtime" (JNI) stays a post-v1 spike, tracked as its own task.

Runtime flags recorded per model: `-ngl` (GPU layers — Adreno/Mali via OpenCL/Vulkan where available), `-c` context, `-t` threads (A56: 4–6 sensible), `--mlock` off (RAM), `--host 127.0.0.1 --port <derived>`.

## TBC-7 — Provider priority for v1

**Decision: three tiers, free-and-working first (matches the owner's "Gratis zuerst" routing preference).**

**Tier 1 — free / credit-heavy gateways (first-class, one-click connect):**
Bynara / NaraRouter, FreeLLMAPI, APInex, GoRouter, TokenRouter, TokenReply, FastRouter, xKiro, Experiential Labs, OpenRouter (free models), Groq (free tier), Cerebras (free tier), Google AI Studio (free tier), Mistral (free tier), GitHub Models, Cloudflare Workers AI, NVIDIA NIM.

**Tier 2 — majors / paid keys and subscriptions:**
OpenAI, Anthropic, Google Gemini (AI Pro OAuth), Perplexity (see TBC-5), xAI, DeepSeek, Alibaba DashScope/Qwen, Together, Fireworks, DeepInfra, Novita, Hyperbolic, Nebius, SambaNova, Cohere, AI21, HuggingFace (OAuth + Inference), Scaleway, Chutes, Kluster.

**Tier 3 — long tail + local:**
any OpenAI- or Anthropic-compatible endpoint added by the owner via the provider form, plus local runtimes (llama.cpp in Termux, later embedded; Ollama/LM Studio endpoints on the LAN).

Every provider ships a manifest (`assets/providers/<id>.json`) so the registry is data, not code. Adding a Tier 3 provider needs no app update.

## TBC-8 — How the build agents find their tools (skills, plugins, MCP)

**Decision: discover, publish, reference — never hard-code.**

The owner requires that Claude Code (and Freebuff) find every plugin, MCP server and skill, globally and inside the project, and use the skill libraries intelligently. That list changes without a commit, so it is generated, not written by hand:

| Concern | Answer |
|---|---|
| Where does the list come from? | `python3 scripts/discover_tooling.py` scans `~/.claude/skills`, `.claude/skills`, `~/.claude/plugins/*.json`, `~/.claude/commands`, `~/.claude/design-skill-library`, `npx skills` availability, and MCP servers from `~/.claude.json` (user + per-project), `.mcp.json`, `.cursor/mcp.json`, `.vscode/mcp.json` |
| Where is it published? | `status/TOOLING.md` (readable) and `status/tooling.json` (machine), both committed |
| How does it stay true? | `--check` (structure) runs in CI, `--check-fresh` (matches this machine) runs on the device — a CI runner has no agent configuration, so content comparison there would fail for the wrong reason. A13 requires both |
| Precedence | project skill → project MCP → project subagent → global skill → global plugin → global MCP → community skill |
| How are skills applied? | at least two per task in parallel, one of them verification; four project subagents in `.claude/agents/` (`implementer`, `verifier`, `chronicler`, `tooling-scout`) |
| Community skills | `npx skills find/add` is available; installation requires the owner's confirmation and is logged |
| Secrets | MCP environment values are reported by **name only**, never by value |

Consequence for the product: DroidRoute itself does the same thing at runtime (`docs/07-mcp-plugins.md`), so the build-time behaviour and the shipped behaviour follow one rule instead of two.

## TBC-9 — Scope of the OmniRoute parity claim

**Decision: every parity row names a task, or says plainly that it is not planned and why.**

`docs/12-omniroute-parity.md` is the contract, verified against OmniRoute's own README. Parity is the floor, never the ceiling. Three OmniRoute capabilities are deliberately **not** planned, with the reason recorded in the matrix: the Radar catalogue overlay (needs a network dependency the owner does not want), transparent MITM/TPROXY TLS interception (requires a CA in the device trust store and intercepts traffic on a personal phone), and vendor cloud-agent endpoints (a different product category). Everything else maps to a task in `plan/`, with phase 12 closing the gap that phase 11 (v0.1) does not cover. Competitors beyond OmniRoute are handled by TBC-10.

## TBC-10 — How far the comparison to other routers goes

**Decision: absorb what is table stakes, refuse what conflicts with the owner's rules, and build what none of them can.**

`docs/13-competitive-landscape.md` compares DroidRoute against 9Router, OmniRoute, CLIProxyAPI, LiteLLM, the hosted aggregators and the enterprise gateways. Three rules came out of it:

| Rule | Consequence |
|---|---|
| Anything a competitor has that a router needs is a **task**, not a promise | Each absorbed capability names its task id in the matrix; a claim without a task is not allowed |
| Competitor claims are **attributed**, never restated as fact | 9Router's package is private, so its feature list is marked as claims in the comparison |
| A capability that changes the owner's output without consent is **refused** | Prompt-style presets exist (T-173) but default **off** and never apply to a request that did not ask for them; cloud config sync is refused in favour of QR transfer (T-183) |

The genuinely phone-specific work — battery/thermal/network-aware routing (T-176), offline-first mode (T-175), conversation affinity (T-174), self-update with signature verification (T-180, T-181), an offline model catalog (T-179), mobile-data budgeting (T-178) and the Android surfaces (T-177) — exists precisely because every competitor is a server-side service.

---

## Consequences for the task plan

- `plan/phase-01-core-server/` carries the port + bind-mode work (TBC-1, TBC-2).
- `plan/phase-02-provider-framework/` carries manifests + generic adapters (TBC-7).
- `plan/phase-04-accounts-oauth/` carries Tier A/B of Perplexity (TBC-5).
- `plan/phase-08-local-models/` carries the runtime resolution order (TBC-6).
- `plan/phase-09-mcp-plugins/` carries discovery + bridge (TBC-4).
- `plan/phase-11-delivery/` carries the SDK/CI matrix (TBC-3).
- `plan/phase-12-parity-power/` carries the OmniRoute parity work and the owner's extras (TBC-9), including the build-agent tooling wiring (TBC-8, T-166).
- `plan/phase-13-competitive-edge/` carries the competitor absorption and the Android-only differentiators (TBC-10): any-provider detection, migration importers, local-first providers, extra wire surfaces, subscription login adapters, tool-output filters, response-style presets, conversation affinity, offline-first mode, phone-aware routing, Android surfaces, mobile-data accounting, the offline model catalog, self-update, signed catalog packs, debug capture, QR config portability and the native benchmark.
- `handbooks/09-skill-resolution.md` carries the mapping from the role labels used in `plan/` to the installed skills, plugins and MCP servers (TBC-8).
