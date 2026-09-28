"""Phase 05 — Wire protocols: OpenAI, Anthropic and Gemini on one port, plus media and error mapping."""

from common import Phase, Task

PHASE = Phase(
    number=5,
    slug="wire-protocols",
    title="Wire protocols",
    summary="Three request/response dialects, streaming, tool calls, media, and one error taxonomy.",
)

TASKS = [
    Task(
        id=66,
        slug="protocol-models",
        title="Shared protocol models and normalisation",
        goal="Define the internal message model that all three dialects translate into and out of, so additions never touch three parsers.",
        deps=[26],
        est="60-120 min",
        skills=[
            ("llm-gateway-protocols", "content blocks, tool calls, attachments, stop reasons"),
            ("kotlin-core", "sealed hierarchies and serialization without nullable soup"),
        ],
        deliverables=[
            "`protocol/model/` — NormalisedRequest, NormalisedMessage, ContentPart, ToolCall, NormalisedResponse, Usage",
            "Mapping notes in docs/02-protocols.md",
        ],
        steps=[
            "Model content as a sealed type: Text, Image, Audio, ToolUse, ToolResult.",
            "Model stop reasons as an enum covering all three dialects' vocabularies.",
            "Keep provider quirks out of this model — they belong in adapters.",
            "Write round-trip tests: normalise → denormalise for each dialect preserves meaning.",
        ],
        accept=[
            "A request expressed in any dialect normalises to the same internal model (asserted)",
            "No nullable field exists that a dialect actually guarantees",
            "Round-trip tests pass for text, image, tool-call and tool-result content",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Normalis*'",
        ],
        state="One internal model serves three dialects; protocol work no longer multiplies.",
    ),
    Task(
        id=67,
        slug="openai-chat-completions",
        title="OpenAI chat completions (non-streaming)",
        goal="Serve `/v1/chat/completions` end to end, routed through the provider layer, with usage recorded.",
        deps=[66, 27],
        est="60-120 min",
        skills=[
            ("llm-gateway-protocols", "response shape, finish reasons, usage block"),
            ("testing", "golden response test plus a routing integration test"),
        ],
        deliverables=[
            "`protocol/openai/ChatCompletionsRoute.kt`",
            "Golden request/response fixtures",
        ],
        steps=[
            "Parse the request leniently (clients send extras) but validate the required fields strictly.",
            "Resolve the model through routing (a stub candidate list is acceptable until Phase 6 lands).",
            "Return a response whose shape matches the golden fixture byte-for-shape.",
            "Record usage and cost fields on the usage record.",
        ],
        accept=[
            "A real or fixture-backed request returns a schema-correct response",
            "Unknown request fields are tolerated, missing required fields produce a 400 in OpenAI's error shape",
            "Usage is recorded when the provider reports it",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ChatCompletions*'",
        ],
        state="The primary OpenAI route works end to end.",
    ),
    Task(
        id=68,
        slug="openai-streaming-sse",
        title="OpenAI streaming (SSE)",
        goal="Stream `/v1/chat/completions` frames as they arrive, with heartbeats and cancellation propagation.",
        deps=[67],
        est="60-120 min",
        skills=[
            ("ktor-server", "response streaming without buffering, disconnect detection"),
            ("testing", "frame-order test and a cancellation test that proves upstream cancellation"),
        ],
        deliverables=[
            "Streaming implementation plus `data: [DONE]` terminator",
            "A test asserting incremental delivery (first frame before the last is generated)",
        ],
        steps=[
            "Flush immediately per frame; never accumulate a buffer to 'simplify' the code.",
            "Emit a heartbeat comment every 15 seconds so doze and proxies do not drop the stream.",
            "On client disconnect, cancel the upstream call so quota is not spent on an abandoned answer.",
            "Keep content-type and cache headers exactly as OpenAI's clients expect.",
        ],
        accept=[
            "Frames arrive incrementally (asserted by timestamps in a test)",
            "A client disconnect cancels the upstream request",
            "`data: [DONE]` is always the final frame on success",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Streaming*'",
        ],
        state="Streaming is incremental, robust to doze, and does not waste quota.",
    ),
    Task(
        id=69,
        slug="openai-models-and-completions",
        title="OpenAI models list and legacy completions",
        goal="Serve `/v1/models` from the live catalog and map `/v1/completions` onto chat where a provider lacks a legacy endpoint.",
        deps=[29, 67],
        est="40-80 min",
        skills=[
            ("llm-gateway-protocols", "model object shape and the legacy prompt interface"),
            ("testing", "catalog test plus a legacy-to-chat mapping test"),
        ],
        deliverables=[
            "`/v1/models` returning the merged catalog with `provider/model` ids",
            "`/v1/completions` mapped onto chat messages with a documented prompt template",
        ],
        steps=[
            "Expose one id per model per provider, matching the canonical naming rule.",
            "Map a raw prompt to a single user message; document that this is a compatibility shim, not a native path.",
            "Return an empty list rather than an error when no provider is enabled.",
        ],
        accept=[
            "`/v1/models` lists every enabled provider's models with canonical ids",
            "A legacy completion request returns a readable answer",
            "The prompt-to-message mapping is documented in docs/02-protocols.md",
        ],
        verify=[
            "curl -fsS http://127.0.0.1:8787/v1/models | head -20",
        ],
        state="Model listing and the legacy surface are available to older clients.",
    ),
    Task(
        id=70,
        slug="anthropic-messages",
        title="Anthropic messages (non-streaming)",
        goal="Serve `/v1/messages` — the route Claude Code depends on — including system prompts, content blocks and tool results.",
        deps=[66, 27, 28],
        est="90-150 min",
        skills=[
            ("llm-gateway-protocols", "message shape, content blocks, stop reasons"),
            ("testing", "golden fixture plus a Claude-Code-shaped request test"),
        ],
        deliverables=[
            "`protocol/anthropic/MessagesRoute.kt`",
            "A fixture captured from a real Claude Code request shape",
        ],
        steps=[
            "Parse `system`, `messages`, `tools`, `tool_choice`, `max_tokens`, `stop_sequences`.",
            "Translate content blocks including `tool_use` and `tool_result` into the normalised model.",
            "Return the Anthropic response shape with `stop_reason` and `usage` fields present.",
            "Accept both `x-api-key` and bearer auth through the existing gate.",
        ],
        accept=[
            "A Claude-Code-shaped request receives a response the client accepts",
            "Tool call and tool result blocks survive the round trip",
            "Missing `max_tokens` produces Anthropic's error shape, not a 500",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*MessagesRoute*'",
        ],
        state="Claude Code can talk to DroidRoute on its native protocol.",
    ),
    Task(
        id=71,
        slug="anthropic-streaming-conformance",
        title="Anthropic streaming conformance",
        goal="Emit the exact Anthropic SSE event sequence (`message_start`, `content_block_start`, deltas, `message_stop`) that strict clients require.",
        deps=[70, 68],
        est="80-150 min",
        skills=[
            ("llm-gateway-protocols", "event order and field names are part of the contract"),
            ("testing", "event-sequence assertion, including tool-call streaming"),
        ],
        deliverables=[
            "Streaming encoder for the Anthropic dialect",
            "A test that asserts the full event order for text and for a tool call",
        ],
        steps=[
            "Emit `message_start` before any content, with the correct initial usage.",
            "Emit `content_block_start`/`delta`/`stop` per block, in order, including tool_use blocks.",
            "Emit `message_delta` with the final stop reason and usage, then `message_stop`.",
            "Never reorder or skip events for speed.",
        ],
        accept=[
            "The event sequence matches the specification in a golden-file test",
            "Tool-call streaming produces valid `input_json_delta` frames",
            "A strict client (Claude Code or an equivalent test harness) consumes the stream without error",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*AnthropicStream*'",
        ],
        state="The strictest streaming contract in the project is honoured.",
    ),
    Task(
        id=72,
        slug="count-tokens",
        title="`/v1/messages/count_tokens`",
        goal="Provide a token estimate so clients that pre-check context fit get an answer instead of an error.",
        deps=[70],
        est="40-80 min",
        skills=[
            ("llm-gateway-protocols", "the request/response shape of the counting endpoint"),
            ("testing", "estimate-vs-provider comparison test"),
        ],
        deliverables=[
            "`CountTokensRoute` returning `{input_tokens: n}`",
            "A documented note on estimate accuracy and its source",
        ],
        steps=[
            "Use provider-reported counts when the provider exposes them.",
            "Otherwise estimate locally and label the result as an estimate in the log.",
            "Never block the endpoint on a provider round trip when a local estimate is available.",
        ],
        accept=[
            "The endpoint returns a number for any valid message list",
            "Provider-reported and locally estimated counts are distinguishable in the logs",
            "Accuracy of the estimate is stated, with the method used",
        ],
        verify=[
            "curl -fsS -X POST http://127.0.0.1:8787/v1/messages/count_tokens -d '{\"messages\":[]}'",
        ],
        state="Clients can budget context before spending tokens.",
    ),
    Task(
        id=73,
        slug="gemini-surface",
        title="Gemini surface (`/v1beta`)",
        goal="Serve the Gemini-style endpoints so Google-shaped software can connect directly, including streaming with `alt=sse`.",
        deps=[66, 27],
        est="90-150 min",
        skills=[
            ("llm-gateway-protocols", "contents/parts shape, generationConfig, tool declarations"),
            ("testing", "fixture parity between Gemini and OpenAI requests for the same intent"),
        ],
        deliverables=[
            "`protocol/gemini/GenerateContentRoute.kt` with streaming support",
            "`/v1beta/models` listing",
        ],
        steps=[
            "Map `contents[]`/`parts[]` including `inlineData` and function calls.",
            "Implement `:generateContent` and `:streamGenerateContent` on the same model resolution path.",
            "Return Gemini-shaped errors for this surface (the taxonomy maps per surface).",
        ],
        accept=[
            "Both endpoints answer a real request; streaming emits incremental chunks",
            "An image part round-trips through the normalised model",
            "Errors on this surface use Gemini's shape",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Gemini*'",
        ],
        state="All three dialects are live on one port.",
    ),
    Task(
        id=74,
        slug="tool-call-translation",
        title="Tool call translation across dialects",
        goal="Make function calling work whichever dialect the client speaks and whichever the provider speaks.",
        deps=[67, 70, 73],
        est="80-150 min",
        skills=[
            ("llm-gateway-protocols", "schema differences between OpenAI tools, Anthropic tools and Gemini functionDeclarations"),
            ("testing", "cross-dialect matrix test: 3 clients × 3 providers"),
        ],
        deliverables=[
            "`protocol/tools/ToolTranslator.kt`",
            "A matrix test proving each dialect can drive each other dialect's tool format",
        ],
        steps=[
            "Translate tool schemas in both directions, preserving required/optional semantics.",
            "Translate tool calls and tool results as content parts, not as a side channel.",
            "Handle the case where a provider cannot do tools by returning a clear capability error.",
            "Test the full matrix, including multi-call turns.",
        ],
        accept=[
            "The 3×3 matrix passes in tests",
            "A provider without tool support produces a capability error, not a malformed request",
            "Multi-call turns preserve ordering",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ToolTranslator*'",
        ],
        state="Agents can use tools through any dialect and any provider that supports them.",
    ),
    Task(
        id=75,
        slug="media-endpoints",
        title="Media endpoints (images, TTS, STT)",
        goal="Serve OpenAI-shaped media endpoints and route them only to providers that declare the capability.",
        deps=[73, 26],
        est="80-150 min",
        skills=[
            ("llm-gateway-protocols", "image generation, speech synthesis and transcription request shapes"),
            ("testing", "capability-gating tests plus a failure path for unsupported models"),
        ],
        deliverables=[
            "`/v1/images/generations`, `/v1/audio/speech`, `/v1/audio/transcriptions`",
            "Capability gating so unsupported providers are never chosen",
        ],
        steps=[
            "Implement each endpoint against the normalised model where possible, with provider-specific mapping where not.",
            "Refuse with a clear `not_supported` when no enabled provider declares the capability.",
            "Handle binary responses without corrupting them through the JSON layer.",
        ],
        accept=[
            "Each endpoint works against at least one capable provider, or the blocker is logged per endpoint",
            "Requesting media from an incapable provider returns a clear error",
            "Binary payloads survive the round trip (checksum compared in a test)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Media*'",
        ],
        state="Media is a first-class part of the gateway, not an afterthought.",
    ),
    Task(
        id=76,
        slug="embeddings-endpoint",
        title="Embeddings endpoint",
        goal="Serve `/v1/embeddings` for hosted providers and for local embedding models.",
        deps=[66, 29],
        est="40-80 min",
        skills=[
            ("llm-gateway-protocols", "embedding request/response shape and batching"),
            ("testing", "dimension and ordering assertions plus a batching test"),
        ],
        deliverables=[
            "`/v1/embeddings` with input batching",
            "Capability tagging so chat routing never selects an embedding model",
        ],
        steps=[
            "Accept string and array inputs; preserve input order in the response with correct indices.",
            "Batch according to the provider's limit, not arbitrarily.",
            "Tag embedding models so the router keeps them out of chat candidate lists.",
        ],
        accept=[
            "Order and count are preserved for batched inputs (asserted)",
            "Embedding models never appear as chat candidates (asserted)",
            "Vector dimensions are returned exactly as the provider sent them",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Embeddings*'",
        ],
        state="Embeddings work for hosted and local models, with correct routing isolation.",
    ),
    Task(
        id=77,
        slug="error-mapping",
        title="Unified error mapping and the `droidroute` error object",
        goal="Normalise every failure into the calling dialect's shape and attach the attempt list so a failing chain is debuggable from the client.",
        deps=[67, 70, 73, 26],
        est="60-120 min",
        skills=[
            ("llm-gateway-protocols", "error shapes per dialect, including Anthropic's overloaded_error"),
            ("testing", "a mapping table test covering every taxonomy value × every surface"),
        ],
        deliverables=[
            "`protocol/errors/ErrorMapper.kt`",
            "Documentation table in docs/02-protocols.md (already sketched there — now made true)",
        ],
        steps=[
            "Map each taxonomy value per surface as documented.",
            "Attach `{attempts, strategy, request_id}` to every error body.",
            "Guarantee that a 5xx never leaks a stack trace or an upstream URL containing a key.",
            "Test the full mapping table.",
        ],
        accept=[
            "Every taxonomy value maps per surface and is asserted by a test",
            "No error body contains a key, a token or a stack trace",
            "The `droidroute` object is present on all error responses",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ErrorMapper*'",
        ],
        state="Clients can parse every failure, and the owner can see why the chain failed.",
    ),
    Task(
        id=78,
        slug="protocol-conformance-suite",
        title="Protocol conformance suite (golden files)",
        goal="Lock the three dialects with golden files so a later refactor cannot silently break a client.",
        deps=[67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77],
        est="80-150 min",
        skills=[
            ("testing", "golden-file strategy, update workflow that requires a human decision"),
            ("llm-gateway-protocols", "capture real client traffic shapes, not invented ones"),
        ],
        deliverables=[
            "`app/src/test/resources/golden/{openai,anthropic,gemini}/` request and response pairs",
            "A test that fails on any uncontrolled shape change",
        ],
        steps=[
            "Capture real request shapes from Claude Code and an OpenAI-compatible client where possible.",
            "Store both request and response goldens; assert shape, not incidental values.",
            "Document how to update a golden deliberately (never by rerunning a script blindly).",
            "Add the suite to the CI verify job.",
        ],
        accept=[
            "The suite passes and is wired into CI",
            "Deliberately breaking one response field makes the suite fail (proven once, then reverted)",
            "Goldens contain no captured credentials",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Conformance*'",
            "scripts/preflight-secrets.sh",
        ],
        state="Protocol compatibility is enforced by tests rather than by hope.",
    ),
]
