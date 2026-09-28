# Component: provider-layer

**Purpose:** turn an upstream provider into a manifest plus a thin adapter, so adding one is data entry, not a release.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-024 … T-054 |
| Owns | `com.droidroute.provider` |
| Depends on | core-server (server + storage), vault (keystore) |

## Deliverables

- Manifest schema + loader (`assets/providers/*.json`), validation with actionable error messages.
- Adapter interface: `call`, `stream`, `models`, `validateKey`, `capabilities`.
- Generic OpenAI-compatible and Anthropic-compatible adapters — the majority of providers need nothing else.
- Model discovery (`/models`) with a manual fallback; no guessed model ids.
- Tier 1 catalog (Bynara, FreeLLMAPI, APInex, GoRouter, TokenRouter, TokenReply, FastRouter, xKiro, Experiential, OpenRouter, Groq, Cerebras, Google AI Studio, Mistral, GitHub Models, Cloudflare, NVIDIA) and Tier 2 majors.
- Custom provider form + manifest export/import (secrets excluded).
- Key validation calls that never persist a response body.

## Open risks

- Several Tier 1 gateways are small operations whose base URLs and quirks must be read from their own docs at implementation time; a wrong URL is worse than a missing provider, so each one gets a live validation task.
- Free tiers change without notice — the quota window is learned at runtime, never hard-coded as truth.

## Evidence log

_No entries yet._
