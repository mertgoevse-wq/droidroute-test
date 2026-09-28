# Component: ui

**Purpose:** make a router configurable in a minute on a phone, without hiding what it is doing.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-091 … T-106 |
| Owns | `com.droidroute.ui` |
| Depends on | core-server, provider-layer, routing (via view models) |

## Deliverables

- App shell: Material 3, dark/light, bottom navigation (Dashboard · Providers · Routing · Local · Settings).
- Dashboard: server state, port, bind mode, connected agents, tokens per provider, today/week usage, error rate, p50/p95 latency.
- Providers: list with status, enable/disable, one-click connect for free providers, search/filter by tag, detail screen with models and keys.
- Keys: add, validate, mask (`first5••••last5`), reveal with device credential, copy with auto-clear, revoke.
- Provider form (custom providers) with model discovery and manual fallback.
- Routing: strategy picker per model/global, alias editor, key chains, `/v1/routing/explain` viewer.
- Settings: port, bind mode, auth mode and client keys, language (de/en), Termux integration, tunnel setup checklist, export/import.
- Logs viewer with redaction badge and export.

## Open risks

- Screens must never show a key accidentally in a screenshot or in the recents preview — `FLAG_SECURE` on the sensitive screens only.
- Compose recomposition under a streaming request must not tank the dashboard refresh.

## Evidence log

_No entries yet._
