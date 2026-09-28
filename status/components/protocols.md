# Component: protocols

**Purpose:** speak OpenAI, Anthropic and Gemini natively on one port, stream correctly, and map failures into each caller's dialect.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-066 … T-078 |
| Owns | `com.droidroute.protocol` |
| Depends on | core-server, routing |

## Deliverables

- Request/response models for all three surfaces, with kotlinx.serialization and lenient parsing for provider quirks.
- SSE streaming with 15 s heartbeats, client-disconnect propagation, and mid-stream failover behaviour.
- Tool/function-call translation in both directions (OpenAI `tools` ↔ Anthropic `tools` ↔ Gemini `functionDeclarations`).
- Media endpoints: images, TTS, STT — routed only to providers that declare the capability.
- Normalised error mapping (see `docs/02-protocols.md`) with a `droidroute` object carrying attempts, strategy and `request_id`.
- Token accounting: verbatim upstream usage where reported, estimated elsewhere, never mixed silently.

## Open risks

- Anthropic streaming event order is strict — Claude Code breaks on any deviation, so the encoder gets its own conformance tests.
- Some gateways return subtly non-conformant JSON; lenient parsing must not hide genuine errors.

## Evidence log

_No entries yet._
