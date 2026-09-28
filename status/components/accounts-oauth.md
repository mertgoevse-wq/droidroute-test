# Component: accounts-oauth

**Purpose:** connect subscription accounts — not just API keys — and be honest about which of them have a supported programmatic path.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-055 … T-065 |
| Owns | `com.droidroute.provider.oauth` |
| Depends on | provider-layer, vault |

## Deliverables

- OAuth flows for Google (AI Pro / Gemini), GitHub (Copilot), HuggingFace, with browser intent + redirect handling and refresh-token storage in the vault.
- Perplexity **Sonar** via API key (Tier A): OpenAI-compatible adapter with `search_mode`, citations surfaced, plus `POST /v1/search`.
- Perplexity account mode (Tier B): experimental, off by default, clearly labelled, never used by the routing engine automatically.
- Token refresh scheduler with backoff; a failed refresh marks the account `needs_attention` instead of failing requests silently.
- Account state in the UI: connected, expiring soon, needs re-login.

## Open risks

- Subscription accounts change their authentication surface without notice; the design must degrade to "provider unavailable with a clear reason", never to a crash.
- Google OAuth client registration is required before the flow can be tested end to end — that step needs the owner's Google account.

## Evidence log

_No entries yet._
