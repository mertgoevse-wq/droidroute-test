"""Phase 02 — Provider framework: manifests, adapters, discovery, keys, health."""

from common import Phase, Task

PHASE = Phase(
    number=2,
    slug="provider-framework",
    title="Provider framework",
    summary="Manifest-driven registry, generic adapters, model discovery, key lifecycle and health.",
)

TASKS = [
    Task(
        id=24,
        slug="manifest-schema-and-loader",
        title="Provider manifest schema and loader",
        goal="Turn providers into data: define the manifest schema, load and validate it at startup, and fail with actionable messages on bad input.",
        deps=[5, 22],
        est="50-100 min",
        skills=[
            ("kotlin-core", "serialization model with defaults, strict validation, typed errors"),
            ("provider-integration", "keep the schema honest against real provider requirements"),
        ],
        deliverables=[
            "`provider/manifest/ProviderManifest.kt` matching the schema in docs/03-providers.md",
            "`provider/manifest/ManifestLoader.kt` with per-field validation messages",
            "Five example manifests under `assets/providers/*.example.json` (placeholders only)",
        ],
        steps=[
            "Model every field from docs/03-providers.md, including `tier`, `auth`, `models_source`, `tags`, `quota`.",
            "Validate: id pattern, https base URL (except loopback), known compat value, auth type known.",
            "Reject unknown fields loudly instead of ignoring them — a typo must not silently disable a setting.",
            "Write the examples with placeholder keys that the secrets preflight accepts.",
        ],
        accept=[
            "A malformed manifest produces a message naming the field and the reason",
            "An unknown field is reported, not ignored",
            "`scripts/preflight-secrets.sh` passes on the example manifests",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ManifestLoader*'",
            "scripts/preflight-secrets.sh",
        ],
        state="Providers are declarative data with a validated schema.",
    ),
    Task(
        id=25,
        slug="provider-registry",
        title="Provider registry with enable/disable and status",
        goal="Hold the live set of providers in memory and in Room: enable, disable, expose status, and survive a restart.",
        deps=[24, 18],
        est="45-90 min",
        skills=[
            ("persistence-room", "registry persistence, stable ordering, no duplicate ids"),
            ("testing", "enable/disable and reload-after-restart tests"),
        ],
        deliverables=[
            "`provider/ProviderRegistry.kt` with a `StateFlow<List<ProviderState>>`",
            "Room entity for owner overrides (enabled flag, notes) separate from the shipped manifest",
        ],
        steps=[
            "Merge shipped manifests with owner overrides at load time; overrides win per field.",
            "Keep the registry immutable in the API surface: expose snapshots, not mutable collections.",
            "Status per provider: enabled, disabled-by-owner, invalid-manifest, needs-key, needs-attention.",
            "Test that disabling a provider removes it from routing immediately without a restart.",
        ],
        accept=[
            "Enabling and disabling a provider takes effect without a server restart",
            "A provider with no usable key reports `needs-key` rather than silently failing",
            "Registry state survives a restart",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ProviderRegistry*'",
        ],
        state="One authoritative registry drives routing, the UI and the provider endpoints.",
    ),
    Task(
        id=26,
        slug="adapter-interface",
        title="Adapter interface and capability model",
        goal="Define what every adapter must implement and how capabilities are declared, so routing can ask precise questions.",
        deps=[25],
        est="40-80 min",
        skills=[
            ("kotlin-core", "sealed capability model, suspend interface, error taxonomy"),
            ("llm-gateway-protocols", "capability set that matches real provider differences"),
        ],
        deliverables=[
            "`provider/ProviderAdapter.kt` — `chat`, `stream`, `models`, `validateKey`, `capabilities`",
            "`provider/Capabilities.kt` — chat, streaming, tools, vision, images, tts, stt, embeddings, longContext",
            "`provider/ProviderError.kt` — QuotaExceeded, AuthError, Timeout, RateLimited, ServerError, BadRequest",
        ],
        steps=[
            "Keep the interface free of wire-format details: adapters exchange normalised messages.",
            "Make the error taxonomy exhaustive, because routing keys its decisions on it.",
            "Declare capabilities as data so a manifest can override the adapter's defaults.",
            "Document the contract in docs/03-providers.md.",
        ],
        accept=[
            "Every adapter error maps to exactly one taxonomy value (asserted by a test)",
            "Capabilities are queryable per provider and per model",
            "The interface has no protocol-specific type in its signature",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ProviderError*'",
        ],
        state="Adapters are interchangeable and the router can reason about them without special cases.",
    ),
    Task(
        id=27,
        slug="openai-compatible-adapter",
        title="Generic OpenAI-compatible adapter",
        goal="Implement the adapter that covers the majority of providers: bearer auth, `/chat/completions`, streaming, tools, model list.",
        deps=[26],
        est="80-150 min",
        skills=[
            ("llm-gateway-protocols", "request/response shapes, streaming frames, usage reporting"),
            ("testing", "fixture-driven tests plus one live call against a free provider"),
        ],
        deliverables=[
            "`provider/adapters/OpenAiCompatibleAdapter.kt`",
            "Fixtures for success, tool call, streaming chunks, and the four error classes",
        ],
        steps=[
            "Build requests from normalised messages; pass through `tools`, `response_format`, `seed` when supported.",
            "Parse streaming frames, tolerate provider-specific extras, and surface usage when present.",
            "Map HTTP status plus body to the error taxonomy, including the 'quota exhausted' variants gateways use.",
            "Support per-provider extra headers and a configurable auth header (some gateways differ).",
        ],
        accept=[
            "Fixture tests cover success, streaming, tool call, 401, 429, 500 and malformed JSON",
            "One live call against a free provider succeeds (skipped with a logged reason when no key exists)",
            "Streaming frames are emitted as soon as they arrive, not buffered to the end",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*OpenAiCompatibleAdapter*'",
        ],
        state="Most providers work through one adapter; only genuine differences need their own code.",
    ),
    Task(
        id=28,
        slug="anthropic-compatible-adapter",
        title="Generic Anthropic-compatible adapter",
        goal="Implement the Anthropic-shaped adapter for providers that offer that surface (needed by Claude Code and by several gateways).",
        deps=[26],
        est="60-120 min",
        skills=[
            ("llm-gateway-protocols", "`/v1/messages` semantics, system prompts, content blocks"),
            ("testing", "conformance fixtures for streaming event order"),
        ],
        deliverables=[
            "`provider/adapters/AnthropicCompatibleAdapter.kt`",
            "Fixtures for message start/delta/stop and tool_use blocks",
        ],
        steps=[
            "Translate normalised messages into Anthropic content blocks including images and tool results.",
            "Handle the `anthropic-version` header per the provider's requirement.",
            "Preserve `cache_control` markers when a provider supports prompt caching.",
            "Map the `overloaded_error` shape used by some gateways to the taxonomy.",
        ],
        accept=[
            "Fixture tests pass for text, image, tool_use and error shapes",
            "Streaming event order matches the Anthropic specification in the fixtures",
            "A provider using only the Anthropic surface can be called after this task",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*AnthropicCompatibleAdapter*'",
        ],
        state="Anthropic-shaped gateways are first-class providers.",
    ),
    Task(
        id=29,
        slug="model-discovery",
        title="Model discovery with manual fallback",
        goal="Learn each provider's models at runtime via `/models`, with an honest manual path when discovery is unavailable.",
        deps=[27, 28],
        est="50-100 min",
        skills=[
            ("provider-integration", "per-provider discovery quirks and pagination"),
            ("testing", "discovery fixtures, empty list, and the manual fallback path"),
        ],
        deliverables=[
            "`provider/ModelCatalog.kt` — per-provider model cache with timestamps and source (discovered/manual/static)",
            "Refresh action with a per-provider result summary",
        ],
        steps=[
            "Call the manifest's discovery path; parse leniently but never invent ids.",
            "Cache results with a TTL and refresh on demand or on provider enable.",
            "When discovery fails, keep the manifest's `fallback_models` and mark the source as `manual`.",
            "Never mark a provider ready if it has zero known models and no manual list.",
        ],
        accept=[
            "A provider with a working `/models` shows its models after a refresh",
            "A provider whose discovery fails reports the reason and falls back to the static list",
            "The catalog never contains an id that no provider reported or the owner typed",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ModelCatalog*'",
        ],
        state="Model ids come from the providers themselves, with a recorded source for every entry.",
    ),
    Task(
        id=30,
        slug="provider-key-storage",
        title="Per-provider key storage and pool model",
        goal="Store multiple labelled keys per provider, in the vault, with the metadata routing needs (label, status, quota window).",
        deps=[6, 25],
        est="50-100 min",
        skills=[
            ("security-audit", "vault-only plaintext, metadata without secrets"),
            ("persistence-room", "key metadata table, cascade delete with the provider"),
        ],
        deliverables=[
            "`store/ProviderKeyEntity.kt` + DAO (provider id, label, vault ref, status, window, created, lastUsed)",
            "`provider/KeyPool.kt` skeleton with add/remove/list by provider",
        ],
        steps=[
            "Store only a vault reference in Room; the material itself lives in the vault.",
            "Model status: active, parked(reset_at), invalid, unchecked.",
            "Implement cascade delete so removing a provider removes its keys and quotas in one transaction.",
            "Expose masked representations for the UI, computed on demand, never stored.",
        ],
        accept=[
            "No plaintext key exists outside the vault (verified by inspecting the database file)",
            "Deleting a provider removes its key rows and quota rows in one transaction",
            "The UI-facing list contains only masked values",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*KeyPool*'",
        ],
        state="Multiple keys per provider are the normal case, and none of them is stored in the clear.",
    ),
    Task(
        id=31,
        slug="key-validation",
        title="Key validation and invalid marking",
        goal="Validate a key with one cheap call, mark it invalid on 401/403, and never persist the validation response.",
        deps=[30, 29],
        est="40-80 min",
        skills=[
            ("provider-integration", "cheapest possible probe per provider"),
            ("security-audit", "ensure the probe response body cannot be logged or stored"),
        ],
        deliverables=[
            "`provider/KeyValidator.kt` returning a typed result: valid, invalid, unknown(reason)",
            "UI-facing status transitions recorded and logged (provider, label, outcome)",
        ],
        steps=[
            "Prefer a models list call; fall back to a one-token chat request where listing is unsupported.",
            "On 401/403 mark invalid without deleting; on network failure mark unknown so the key is not blamed.",
            "Log provider id, key label and outcome — never the key or the response body.",
            "Validate on entry and on demand from the key list; never on a schedule that burns quota.",
        ],
        accept=[
            "An invalid key is marked invalid and excluded from rotation",
            "A network failure marks the key unknown, not invalid",
            "No validation response body appears in logs or the database",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*KeyValidator*'",
        ],
        state="Broken keys are identified precisely and quarantined without losing them.",
    ),
    Task(
        id=32,
        slug="provider-health-probe",
        title="Provider health probe and status surfacing",
        goal="Give every provider a measurable health signal that routing and the dashboard can both use.",
        deps=[31],
        est="40-80 min",
        skills=[
            ("llm-routing", "define the signals that actually predict a good candidate"),
            ("kotlin-core", "rolling window implementation with bounded memory"),
        ],
        deliverables=[
            "`provider/HealthTracker.kt` — rolling success rate, p50/p95 latency, last error, consecutive failures",
            "Health exposure in `/v1/providers` and in the registry state flow",
        ],
        steps=[
            "Keep a bounded window per provider (and per key) so memory cannot grow without limit.",
            "Ignore client-cancelled requests when computing success rate.",
            "Decay old failures so a recovered provider is not punished forever.",
            "Expose the numbers, not a colour: the UI decides how to present them.",
        ],
        accept=[
            "Health numbers update after a real request and are visible in `/v1/providers`",
            "The window is bounded (asserted by a test feeding more samples than the window)",
            "Cancelled requests do not lower the success rate",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*HealthTracker*'",
            "curl -fsS http://127.0.0.1:8787/v1/providers",
        ],
        state="Health is measured, bounded and available to routing and UI alike.",
    ),
    Task(
        id=33,
        slug="custom-provider-crud",
        title="Custom provider create/edit/delete",
        goal="Let the owner add any OpenAI- or Anthropic-compatible endpoint through a form, with discovery and a manual model list.",
        deps=[24, 29, 30],
        est="60-120 min",
        skills=[
            ("provider-integration", "the fields that actually matter for a custom endpoint"),
            ("testing", "create/edit/delete round trip plus validation failures"),
        ],
        deliverables=[
            "`provider/CustomProviderService.kt` — create, update, delete, discover models",
            "Persisted as an owner manifest in Room, distinct from shipped manifests",
        ],
        steps=[
            "Accept name, base URL, compat, auth type, default headers, optional model list.",
            "Validate the URL shape and refuse plaintext http except for loopback addresses.",
            "Run discovery on save and report the result inline; on failure keep the manual list path.",
            "Deleting removes keys, quotas and usage rows in one transaction, with a confirmation step.",
        ],
        accept=[
            "A custom OpenAI-compatible endpoint can be added and used to answer a request",
            "An http:// non-loopback URL is rejected with a clear message",
            "Deleting the provider leaves no orphan rows",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*CustomProvider*'",
        ],
        state="The owner can extend the provider set without waiting for an app update.",
    ),
    Task(
        id=34,
        slug="manifest-export-import",
        title="Manifest export and import without secrets",
        goal="Export provider definitions (including custom ones) to share or re-import on a new device, and prove no secret travels with them.",
        deps=[33],
        est="40-80 min",
        skills=[
            ("security-audit", "prove the export cannot contain key material"),
            ("technical-writing", "document the export format and the import precedence"),
        ],
        deliverables=[
            "`provider/ManifestExchange.kt` — export to a file, import with conflict handling",
            "Documented precedence: imported manifest < owner override < manual edit",
        ],
        steps=[
            "Serialise only manifest fields; never the vault reference, never a masked key.",
            "On import, report conflicts (same id, different base URL) and require a decision.",
            "Test with a canary: export a provider that has a key and assert the key string is absent.",
            "Document the flow in docs/03-providers.md and the German glossary if a new term appears.",
        ],
        accept=[
            "An exported file imports on a fresh database and reproduces the provider",
            "Canary test passes: the key value is absent from the export",
            "Conflicting ids are surfaced, never silently overwritten",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ManifestExchange*'",
        ],
        state="Provider configuration is portable; secrets are not.",
    ),
    Task(
        id=35,
        slug="provider-framework-tests",
        title="Provider framework test suite",
        goal="Consolidate adapter, registry, discovery and key tests, and add the malformed-input cases that tend to be forgotten.",
        deps=[24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34],
        est="60-120 min",
        skills=[
            ("testing", "coverage of error paths, no redundant tests, fast runtime"),
            ("provider-integration", "add one real-world quirk fixture per adapter family"),
        ],
        deliverables=[
            "`app/src/test/…/provider/` suite with fixtures for success and every error class",
            "A `fixtures/` folder with representative provider payloads, secrets scrubbed",
        ],
        steps=[
            "Enumerate the failure modes: truncation, unexpected fields, HTML error pages, rate-limit bodies in three dialects.",
            "Add one fixture per mode and assert the taxonomy value produced.",
            "Remove tests that assert nothing and merge duplicated fixtures.",
            "Keep the whole suite runnable offline.",
        ],
        accept=[
            "The suite runs offline and passes",
            "Every taxonomy value is produced by at least one test",
            "No fixture contains a real credential",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*provider*'",
            "scripts/preflight-secrets.sh",
        ],
        state="The provider layer is provably robust against real upstream weirdness.",
    ),
    Task(
        id=36,
        slug="provider-docs-sync",
        title="Keep docs/03-providers.md in sync with the manifests",
        goal="Make the provider documentation checkable: a script compares the doc table with the shipped manifests so they cannot drift.",
        deps=[35],
        est="30-60 min",
        skills=[
            ("technical-writing", "table that states what exists, no aspirational entries"),
            ("testing", "a check script wired into the repo-hygiene workflow"),
        ],
        deliverables=[
            "`tools/check_providers.py` — compares manifest ids with the Tier tables in docs/03-providers.md",
            "Workflow step so a drift fails CI",
        ],
        steps=[
            "Parse the manifest ids from `assets/providers/` and the ids listed in the doc tables.",
            "Report ids present in one place and not the other, grouped by tier.",
            "Add the check to `.github/workflows/repo-hygiene.yml`.",
            "Fix any drift found while writing the check.",
        ],
        accept=[
            "The script exits 0 on a consistent tree",
            "Removing a row from the doc makes the script fail (proven once, then reverted)",
            "CI runs the check",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="The provider catalogue in the docs is machine-verified against what actually ships.",
    ),
]
