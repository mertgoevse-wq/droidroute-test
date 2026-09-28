# Architecture

## Runtime picture

```
┌──────────────────────────── Galaxy A56 (Android 15) ────────────────────────────┐
│                                                                                │
│  ┌──────────────────────────┐        ┌──────────────────────────────────────┐  │
│  │  Claude Code (Termux)    │        │  DroidRoute (Kotlin/Compose)         │  │
│  │  ANTHROPIC_BASE_URL ─────┼──┐     │                                      │  │
│  └──────────────────────────┘  │     │  ┌────────────────────────────────┐  │  │
│  ┌──────────────────────────┐  │     │  │ Foreground service             │  │  │
│  │  Freebuff (Termux)       ├──┤     │  │  ├─ Ktor CIO server :8787      │  │  │
│  │  OPENAI_BASE_URL ────────┼──┼─────┼─▶│  ├─ Auth gate                  │  │  │
│  └──────────────────────────┘  │     │  │  ├─ Router engine              │  │  │
│  ┌──────────────────────────┐  │     │  │  ├─ Key vault (Keystore)       │  │  │
│  │  Other agents / apps     ├──┘     │  │  └─ Log writer                 │  │  │
│  └──────────────────────────┘        │  └────────────────────────────────┘  │  │
│                                      │  ┌────────────────────────────────┐  │  │
│  ┌──────────────────────────┐        │  │ Compose UI                     │  │  │
│  │ proot-Debian (llama.cpp) │◀───────┼──│  dashboard · providers · keys  │  │  │
│  └──────────────────────────┘  intent│  └────────────────────────────────┘  │  │
│                                      └───────────────┬──────────────────────┘  │
└──────────────────────────────────────────────────────┼─────────────────────────┘
                                                       │ HTTPS (chosen upstream)
                                                       ▼
                         Bynara · FreeLLMAPI · APInex · GoRouter · xKiro · TokenRouter
                         TokenReply · FastRouter · Experiential Labs · OpenRouter · Groq
                         Gemini · OpenAI · Anthropic · Perplexity · HuggingFace · …
```

## Layers

| Layer | Responsibility | Package |
|---|---|---|
| `server` | Ktor bootstrap, routing table, bind mode, graceful rebind | `com.droidroute.server` |
| `protocol` | Wire-format codecs: OpenAI, Anthropic, Gemini, media; SSE streaming | `com.droidroute.protocol` |
| `provider` | Adapter interface, manifest loader, per-provider transports | `com.droidroute.provider` |
| `routing` | Candidate selection, strategies, health, quota, key rotation, failover | `com.droidroute.routing` |
| `vault` | Keystore-wrapped secrets, 5/5 masking, one-time reveal | `com.droidroute.vault` |
| `store` | Room entities + DataStore preferences | `com.droidroute.store` |
| `mcp` | Discovery from Termux/Debian, registry, JSON-RPC bridge | `com.droidroute.mcp` |
| `local` | llama.cpp runtime resolution, process control, model catalog | `com.droidroute.local` |
| `bridge` | Termux RUN_COMMAND intent client + HTTP fallback | `com.droidroute.bridge` |
| `ui` | Compose screens, navigation, theme, de/en strings | `com.droidroute.ui` |
| `logging` | Structured step logs, task logs, rotation, weekly cleanup | `com.droidroute.logging` |

## Key data flows

**Agent request.** Agent → `POST /v1/messages` (Anthropic shape) → auth gate → protocol decoder → router picks candidate `(provider, key, model)` → provider adapter translates to upstream → upstream streams → protocol encoder streams SSE back. Every hop is recorded in the request log with latency, token counts (when the provider reports them) and outcome.

**Key rotation.** Router asks the key pool for the next usable key. The pool tracks per-key quota windows (daily/hourly), cooldowns after `429`, and per-key health. Exhausted keys are parked with a reset time, not deleted.

**Local model.** UI or router → `bridge` resolves the llama.cpp runtime → process started inside Termux/Debian → DroidRoute registers it as a normal provider (`local/llama.cpp`, OpenAI-compatible on `127.0.0.1:<port>`) so routing, logging and MCP all work identically.

**MCP.** On start: discovery reads the Termux/Debian config files → merged registry → `GET /mcp/servers` serves it → agents call tools through `POST /mcp/{id}`.

## Storage

| Data | Where | Encryption |
|---|---|---|
| Provider entries, keys, quota state | Room + vault | Key material in Keystore, ciphertext on disk |
| Preferences (port, bind mode, language, strategy) | DataStore | plain |
| Request/step logs | `files/logs/` in app-private dir, mirrored to `~/storage/shared/droidroute/logs` when the owner opts in | plaintext, secrets redacted |
| MCP registry | `~/.droidroute/mcp.registry.json` | secrets redacted |
| Local model catalog | Room + `~/.droidroute/models/` | plain |

## Concurrency model

- One coroutine scope per concern: `serverScope`, `routerScope`, `logScope`, `runtimeScope`.
- Streaming responses never block the router; the failover decision happens before the first byte is flushed. If an upstream fails *mid-stream*, the router can either surface the error or transparently restart the completion on the next candidate — configurable, default = restart once, then surface.
- Compose UI talks to the service through a bound-interface view model, never through the network.

## Failure modes designed for

| Failure | Behaviour |
|---|---|
| Android kills the app | Foreground service + START_STICKY; on restart, state is rehydrated from Room/vault, logs continue, `status/` files in the repo explain what happened |
| Upstream timeout / 5xx | Retry with backoff, then next candidate |
| `429` / quota exhausted | Key parked until reset, next key, then next provider |
| Port already in use | Detected at bind time; user is offered the next free port |
| Local model too large | Warned with memory estimate before start, never silently killed |
| Repo push fails | Commit stays local, error appended to `status/ERRORS.md`, retried on next step |
