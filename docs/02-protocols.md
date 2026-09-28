# Wire Protocols

DroidRoute exposes four surfaces on one port. Everything is JSON, everything streams where it makes sense.

## 1. OpenAI-compatible

| Endpoint | Method | Notes |
|---|---|---|
| `/v1/models` | GET | merged catalog of every enabled provider |
| `/v1/chat/completions` | POST | streaming (`stream: true`, SSE `data:` frames, `data: [DONE]`) and non-streaming |
| `/v1/completions` | POST | legacy text completion, mapped where supported |
| `/v1/embeddings` | POST | embedding models incl. local |
| `/v1/images/generations` | POST | image models |
| `/v1/audio/speech` | POST | TTS where supported |
| `/v1/audio/transcriptions` | POST | STT where supported |

Request fields honoured: `model`, `messages`, `stream`, `temperature`, `top_p`, `max_tokens`, `stop`, `tools`, `tool_choice`, `response_format`, `seed`, `user`.
DroidRoute extensions (namespaced, ignored by strict clients): `droidroute.strategy`, `droidroute.provider`, `droidroute.key_id`, `droidroute.fallbacks`.

## 2. Anthropic-compatible

| Endpoint | Method | Notes |
|---|---|---|
| `/v1/messages` | POST | required by Claude Code; supports `stream: true` SSE (`message_start`, `content_block_delta`, `message_stop`) |
| `/v1/messages/count_tokens` | POST | token estimate, provider-reported when available |

Mapped fields: `model`, `system`, `messages` (with `content` blocks: text, image, tool_use, tool_result), `max_tokens`, `temperature`, `top_k`, `stop_sequences`, `tools`, `tool_choice`, `stream`.
`anthropic-version` header is accepted and echoed in errors; `x-api-key` and `Authorization: Bearer` are both accepted when API-key auth is on.

## 3. Google Gemini-compatible

| Endpoint | Method | Notes |
|---|---|---|
| `/v1beta/models` | GET | Gemini-style model list |
| `/v1beta/models/{model}:generateContent` | POST | non-streaming |
| `/v1beta/models/{model}:streamGenerateContent` | POST | SSE streaming, `alt=sse` |

Mapped fields: `contents[]` (`parts`: `text`, `inlineData`, `functionCall`, `functionResponse`), `systemInstruction`, `generationConfig` (`temperature`, `topP`, `topK`, `maxOutputTokens`, `stopSequences`), `tools`.

## 4. DroidRoute-native helpers

| Endpoint | Purpose |
|---|---|
| `GET /health` | liveness, version, uptime, bound mode |
| `GET /v1/usage` | tokens per provider, today + 7 days, errors, p50/p95 latency |
| `GET /v1/providers` | registry with status (no secrets) |
| `GET /v1/routing/explain?model=…` | why the router would pick what it would pick right now |
| `POST /v1/search` | Perplexity-style search façade (answer + citations) |
| `GET /mcp/servers`, `GET /mcp/tools`, `POST /mcp/{id}` | MCP federation (see `docs/07-mcp-plugins.md`) |
| `POST /admin/reload` | re-read manifests/providers without restart (API-key protected) |

## Cross-cutting rules

**Auth gate.** Three modes, configurable per client group: `none` (localhost only), `api_key` (header `Authorization: Bearer <key>` or `x-api-key`), `oauth` (device/browser flow issuing short-lived tokens). External bind forces `api_key` at minimum.

**Streaming.** SSE with `Content-Type: text/event-stream`, no buffering, heartbeats every 15 s so Android's doze mode does not drop long generations. Client disconnect propagates upstream cancellation to save quota.

**Error mapping.** Upstream errors are normalised to the format of the surface that was called:

| Upstream | OpenAI surface | Anthropic surface | Gemini surface |
|---|---|---|---|
| 401/403 | `401 authentication_error` | `401 authentication_error` | `401 PERMISSION_DENIED` |
| 429 | `429 rate_limit_error` | `429 rate_limit_error` | `429 RESOURCE_EXHAUSTED` |
| 5xx after failover | `503 upstream_unavailable` | `529 overloaded_error` | `503 UNAVAILABLE` |
| no candidate | `503 no_provider_available` | `529 overloaded_error` | `503 UNAVAILABLE` |

Every error body carries a `droidroute` object: `{ "attempts": [...], "strategy": "...", "request_id": "..." }` so a failing chain is debuggable from the client side.

**Model naming.** Canonical ids are `provider/model` (e.g. `bynara/qwen-3.8-max-free`). A bare model name (`gpt-4o-mini`) resolves through the router's alias table, which can map one name to a prioritised list of candidates. Aliases are owner-editable, and `/v1/routing/explain` shows the resolution.

**Media.** Image and audio endpoints accept and return the same shapes as OpenAI's, translating to provider-specific formats internally. Providers without media support are simply not offered as candidates for those calls.

**Token counting.** When an upstream reports usage, it is recorded verbatim. When it does not, DroidRoute estimates with a local tokenizer and marks the record `estimated: true` — never silently mixing the two.

**Idempotency.** Every request gets a `request_id` (also returned in `x-droidroute-request-id`); retries carry it in logs so a duplicate is never counted twice in usage statistics.
