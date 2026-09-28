# Competitive Landscape

Researched from each project's own repository, release notes and community discussion. The point is not to copy feature lists; it is to know exactly what is table stakes, what is worth absorbing, and where DroidRoute can be genuinely different.

**Honesty note:** 9Router's own README states that its application package is private and that running from source is the expected local path. Its capability list below is therefore treated as *claims*, not as verified source. OmniRoute is MIT and public. Nothing is marked "absorbed" until a DroidRoute task exists for it.

## Who is in the field

| Project | What it actually is | Notable |
|---|---|---|
| **9Router** (`decolua/9router`, ~30k★) | Local Node proxy, port `20128`, dashboard | 40+ providers, 18 CLI tools, RTK token saver, Caveman/Ponytail prompt modes, 3-tier fallback, multi-account, self-hosted STT/TTS/embedding endpoints |
| **OmniRoute** (`diegosouzapw/OmniRoute`, MIT) | Local gateway, port `20128` | 359 providers, combos and virtual `auto` models, 19 routing strategies, quota-share, adaptive admission, compression, MCP/A2A |
| **CLIProxyAPI** (`router-for-me/CLIProxyAPI`) | Wraps CLI tools to expose OpenAI/Gemini/Claude/Codex/Grok-shaped APIs | Turns *subscription CLI tools* into endpoints rather than routing API keys |
| **LiteLLM** | Python proxy, the de-facto standard in teams | 100+ providers, keys/teams/budgets, virtual keys, logging integrations |
| **OpenRouter / Vercel AI Gateway** | Hosted aggregators | Breadth, one key, hosted billing — no local control, no subscriptions |
| **Portkey / Helicone / Kong / Bifrost / Envoy AI Gateway** | Enterprise gateways | Observability, policies, guardrails at scale; server-grade, not phone-grade |
| **one-api / new-api** | Self-hosted multi-tenant gateway with billing UI | User/tenant quotas, recharge model, wide provider list |
| **dario** | Routes an existing Claude Max subscription | Demonstrates that subscription-based routing is a real user need |

## Absorbed into DroidRoute

Everything below is table stakes: a router without these is not competitive. Each row names the task that delivers it.

| Capability | Where it comes from | DroidRoute task |
|---|---|---|
| Lossless compression of tool outputs (`git diff`, `grep`, `ls`, `tree`, log dedup, smart truncate) with auto-detect and fail-open | 9Router RTK | T-172 (extends T-153) |
| Short-response and minimal-code prompt presets | 9Router Caveman / Ponytail | T-173 |
| Tiered fallback: subscription → credit → free | 9Router, OmniRoute | T-148, T-084 |
| Multi-account pools per provider with rotation | 9Router, OmniRoute quota-share | T-171, T-156 |
| Format translation across dialects | 9Router, OmniRoute | T-066…T-077, T-170 |
| Real-time quota tracking with reset countdown | 9Router, OmniRoute | T-164 |
| Custom combos and virtual `auto` models | OmniRoute | T-148 |
| Additional wire surfaces: OpenAI Responses API, Vertex AI (ADC) | 9Router, OmniRoute | T-170 |
| Subscription/CLI login adapters (Claude Code, Codex, Copilot, Cursor, Antigravity-style) | 9Router, CLIProxyAPI, dario | T-171 |
| No-auth free providers with model auto-fetch | 9Router OpenCode Free | T-169 |
| Self-hosted STT / TTS / embeddings endpoints | 9Router | T-169 |
| "Never silently fall back to a cloud provider when a local one was configured" | 9Router (self-hosted embedding has no cloud fallback *by design*) | T-169 |
| Request/response debug capture | 9Router debug mode | T-182 |
| Broad CLI-client compatibility list | 9Router (18 tools), OmniRoute (`run` for 7) | T-165, T-184 |
| Observability: usage, cost, trends | everyone | T-095, T-155 |
| Guardrails: injection screening, credential masking | OmniRoute | T-158, T-159 |

## Where DroidRoute is deliberately different

These are not features on any of the above. Each is a task, and each is testable.

| Differentiator | Why nobody else has it | Task |
|---|---|---|
| **Native Android app, no Node runtime** | Every competitor is a Node/Python service run on a desktop, VPS or inside Termux. A foreground service with Kotlin/Compose is the only design that survives Android's process killer and costs a fraction of the battery. | T-007, T-011, T-184 (measured, not asserted) |
| **Battery-, thermal- and network-aware routing** | Desktop and server gateways have no notion of a battery. DroidRoute can prefer a local model when the battery is low, avoid loading a large model when the device is hot, and refuse metered traffic under a policy the owner set. | T-176 |
| **Conversation affinity (sticky provider)** | The most repeated complaint about 9Router/OmniRoute is that switching models mid-conversation resends context and burns quota. Affinity pins a conversation to a provider while it is healthy, so provider-side prompt caches survive — and says plainly when it breaks the pin and why. | T-174 |
| **Offline-first mode** | Competitors are network-bound. With a local model loaded, DroidRoute answers with no connectivity, queues what it cannot serve, and replays it when the network returns. | T-175 |
| **Automatic provider detection from any URL** | Everybody requires a hand-written provider entry. Probing an endpoint to infer whether it speaks OpenAI, Anthropic, Gemini or Responses, then generating a validated manifest, is a genuinely different onboarding path. | T-167 |
| **Migration importers** | Nobody imports another router's configuration. Moving from OmniRoute, 9Router, LiteLLM, one-api/new-api or CLIProxyAPI should be a paste, not a weekend. | T-168 |
| **Offline, signed, updatable model catalog** | Competitors assume a server with a GPU. A catalog that works with no internet, carries sizes, quants, hashes and licences, and is scored against *this device's* RAM is phone-specific. | T-179 |
| **App self-update with rollback** | These projects update by `npm install` or `docker pull`. A sideloaded APK that checks GitHub releases, verifies the signature, installs, and can roll back to the previous build is unusual — and it is what "always update-ready" means on Android. | T-180 |
| **Catalogs that update without an app release** | Provider and model knowledge changes weekly; shipping an APK for that is absurd. Signed catalog packs keep the app current between releases, with an offline fallback to the bundled copies. | T-181 |
| **Config portability by QR, no cloud** | 9Router syncs config through a cloud. DroidRoute exports an encrypted bundle as a QR code so a new phone is configured by scanning, with secrets never leaving the device. | T-183 |
| **Mobile-data accounting and budget** | Nobody meters bytes because nobody runs on a metered connection. | T-178 |
| **Android surfaces: Quick Settings tile, widget, share sheet, text-selection action** | This is the difference between a localhost service and a phone app. | T-177 |

## What we intentionally do not copy

| Rejected | Reason |
|---|---|
| Cloud config sync | A router holding the owner's credentials should not have an account. QR-based local transfer (T-183) covers the actual need. |
| Prompt-injection of *behavioural* personalities without opt-out | Caveman/Ponytail-style prompt modes are absorbed (T-173) but default **off** and never applied to requests that did not ask for them: silently changing the owner's output style is a defect, not a feature. |
| MITM/TPROXY TLS interception | Requires a CA in the device trust store and intercepts traffic. Still rejected (`docs/12-omniroute-parity.md`). |
| Marketing token headlines | Competitors print large free-token numbers. DroidRoute reports measured, per-provider reality (T-164) and labels estimates as estimates. |

## How this document stays true

- A row is only marked absorbed when the task exists in `plan/`.
- Competitor claims are attributed to the project that made them, never restated as fact.
- Community complaints (the context-resend problem, for example) are treated as design inputs, and the resulting task states what it changes rather than that it "solves" them.
- When a competitor adds something genuinely new, it gets a row here and, if worth building, a task — in that order.
