# Build plan — 208 tasks

The execution order is the numeric order of the task ids. Each task is one commit
and one log file. Rules: [AGENTS.md](../AGENTS.md) · process: [docs/08-workflow.md](../docs/08-workflow.md) ·
resume: [handbooks/06-resume-protocol.md](../handbooks/06-resume-protocol.md).

**Start at [T-001](phase-00-foundation/T-001-repository-hygiene.md).** `status/NEXT.md` always names the next task.

| Phase | Tasks | Count | Focus |
|---|---|---|---|
| [00 — Foundation](phase-00-foundation/) | T-001 … T-010 | 10 | Toolchain, Gradle scaffold, storage and vault foundations, and CI that tells the truth. |
| [01 — Core server](phase-01-core-server/) | T-011 … T-023 | 13 | Embedded Ktor server, lifecycle, configurable port, bind modes, auth gate, request logging. |
| [02 — Provider framework](phase-02-provider-framework/) | T-024 … T-036 | 13 | Manifest-driven registry, generic adapters, model discovery, key lifecycle and health. |
| [03 — Provider catalog](phase-03-provider-catalog/) | T-037 … T-054 | 18 | Manifest + live validation for each Tier 1 free gateway, then the Tier 2 majors. |
| [04 — Accounts & OAuth](phase-04-accounts-oauth/) | T-055 … T-065 | 11 | OAuth flows, token refresh, subscription accounts, Perplexity Sonar search. |
| [05 — Wire protocols](phase-05-wire-protocols/) | T-066 … T-078 | 13 | Three request/response dialects, streaming, tool calls, media, and one error taxonomy. |
| [06 — Routing](phase-06-routing/) | T-079 … T-090 | 12 | Candidate resolution, strategies, quota ledgers, multi-key chaining, failover and explainability. |
| [07 — UI](phase-07-ui/) | T-091 … T-106 | 16 | Compose shell, dashboard, provider and key management, routing controls, settings, onboarding. |
| [08 — Local models](phase-08-local-models/) | T-107 … T-117 | 11 | Termux bridge, runtime resolution, model catalog, memory guard, and special-purpose models. |
| [09 — MCP & plugins](phase-09-mcp-plugins/) | T-118 … T-126 | 9 | Discover MCP servers from the host environment, aggregate them, and bridge tool calls over the local API. |
| [10 — Logging & handover](phase-10-logging-handover/) | T-127 … T-135 | 9 | Retention, status automation, evidence bundles and adversarial resume drills. |
| [11 — Delivery](phase-11-delivery/) | T-136 … T-147 | 12 | Performance and security hardening, the acceptance run, the release pipeline and owner documentation. |
| [12 — OmniRoute parity & power features](phase-12-parity-power/) | T-148 … T-166 | 19 | Combos, all 19 strategies, fusion/pipeline, compression, cost telemetry, guardrails, memory, A2A, tooling wiring. |
| [13 — Competitive absorption & Android edge](phase-13-competitive-edge/) | T-167 … T-184 | 18 | Any-provider detection, migration importers, local-first providers, extra wire surfaces, token savers, affinity, offline mode, phone-awareness, self-update. |
| [14 — Design audit & release polish](phase-14-design-audit/) | T-185 … T-190 | 6 | Token conformance, a proven gate, screen-by-screen craft review, measured contrast and accessibility, state completeness, design acceptance. |
| [15 — Security & privacy audit](phase-15-security-audit/) | T-191 … T-196 | 6 | Threat model and test mapping, static analysis and licences, vault crypto review, network exposure, component and data-at-rest review, signing and audit trail. |
| [16 — Visual evidence & launch](phase-16-visual-evidence/) | T-197 … T-202 | 6 | Screenshot harness, automatic visual analysis, visual Q&A loop, README gallery, launch video via brag, launch assets. |
| [17 — One-tap access, key issuing & tooling coverage](phase-17-access-and-tooling/) | T-203 … T-208 | 6 | One-tap free start, device-code sign-in, local-only key issuing for DroidRoute itself, tooling coverage proof, the reusable workflow plugin, and the clone-from-scratch freeze. |

## All tasks

### Phase 00 — Foundation

Toolchain, Gradle scaffold, storage and vault foundations, and CI that tells the truth.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-001](phase-00-foundation/T-001-repository-hygiene.md) | Repository hygiene and baseline checks | — (entry task) | yes |
| [T-002](phase-00-foundation/T-002-android-toolchain.md) | Android toolchain and build prerequisites | T-001 | yes |
| [T-003](phase-00-foundation/T-003-gradle-project-skeleton.md) | Gradle project skeleton | T-002 | yes |
| [T-004](phase-00-foundation/T-004-package-structure.md) | Package structure and module boundaries | T-003 | yes |
| [T-005](phase-00-foundation/T-005-storage-foundation.md) | Storage foundation (Room + DataStore) | T-004 | yes |
| [T-006](phase-00-foundation/T-006-key-vault.md) | Key vault (Keystore, AES-256-GCM) | T-005 | yes |
| [T-007](phase-00-foundation/T-007-foreground-service-skeleton.md) | Foreground service skeleton | T-003 | yes |
| [T-008](phase-00-foundation/T-008-app-logging-writer.md) | App-side log writer | T-004 | yes |
| [T-009](phase-00-foundation/T-009-ci-pipeline-hardening.md) | CI pipeline hardening | T-003 | yes |
| [T-010](phase-00-foundation/T-010-docs-baseline-and-linkcheck.md) | Documentation baseline and link integrity | T-001 | yes |

### Phase 01 — Core server

Embedded Ktor server, lifecycle, configurable port, bind modes, auth gate, request logging.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-011](phase-01-core-server/T-011-ktor-server-bootstrap.md) | Ktor server bootstrap | T-007, T-003 | yes |
| [T-012](phase-01-core-server/T-012-service-server-wiring.md) | Service ↔ server wiring and lifecycle states | T-011, T-007 | yes |
| [T-013](phase-01-core-server/T-013-port-configuration.md) | Configurable port with collision handling | T-012, T-005 | yes |
| [T-014](phase-01-core-server/T-014-bind-modes-and-auth-floor.md) | Bind modes and the enforced auth floor | T-013 | yes |
| [T-015](phase-01-core-server/T-015-auth-gate-middleware.md) | Auth gate middleware | T-014 | yes |
| [T-016](phase-01-core-server/T-016-client-api-keys.md) | Client API key generation, hashing and revocation | T-015, T-006 | yes |
| [T-017](phase-01-core-server/T-017-request-logging-middleware.md) | Request logging, request ids and redaction | T-015, T-008 | yes |
| [T-018](phase-01-core-server/T-018-config-persistence-rehydration.md) | Configuration persistence and post-mortem rehydration | T-012, T-005, T-006 | yes |
| [T-019](phase-01-core-server/T-019-graceful-rebind.md) | Graceful rebind on configuration change | T-018, T-013 | yes |
| [T-020](phase-01-core-server/T-020-autostart-and-doze.md) | Optional autostart and doze resilience | T-018 | yes |
| [T-021](phase-01-core-server/T-021-connection-helper.md) | Connection helper (URLs, snippets, QR) | T-013, T-016 | yes |
| [T-022](phase-01-core-server/T-022-admin-endpoints.md) | Admin endpoints and reload path | T-017, T-018 | yes |
| [T-023](phase-01-core-server/T-023-core-server-test-suite.md) | Core server test suite and service lifecycle evidence | T-011, T-012, T-013, T-014, T-015, T-016, T-017, T-018, T-019, T-020, T-021, T-022 | yes |

### Phase 02 — Provider framework

Manifest-driven registry, generic adapters, model discovery, key lifecycle and health.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-024](phase-02-provider-framework/T-024-manifest-schema-and-loader.md) | Provider manifest schema and loader | T-005, T-022 | yes |
| [T-025](phase-02-provider-framework/T-025-provider-registry.md) | Provider registry with enable/disable and status | T-024, T-018 | yes |
| [T-026](phase-02-provider-framework/T-026-adapter-interface.md) | Adapter interface and capability model | T-025 | yes |
| [T-027](phase-02-provider-framework/T-027-openai-compatible-adapter.md) | Generic OpenAI-compatible adapter | T-026 | yes |
| [T-028](phase-02-provider-framework/T-028-anthropic-compatible-adapter.md) | Generic Anthropic-compatible adapter | T-026 | yes |
| [T-029](phase-02-provider-framework/T-029-model-discovery.md) | Model discovery with manual fallback | T-027, T-028 | yes |
| [T-030](phase-02-provider-framework/T-030-provider-key-storage.md) | Per-provider key storage and pool model | T-006, T-025 | yes |
| [T-031](phase-02-provider-framework/T-031-key-validation.md) | Key validation and invalid marking | T-030, T-029 | yes |
| [T-032](phase-02-provider-framework/T-032-provider-health-probe.md) | Provider health probe and status surfacing | T-031 | yes |
| [T-033](phase-02-provider-framework/T-033-custom-provider-crud.md) | Custom provider create/edit/delete | T-024, T-029, T-030 | yes |
| [T-034](phase-02-provider-framework/T-034-manifest-export-import.md) | Manifest export and import without secrets | T-033 | yes |
| [T-035](phase-02-provider-framework/T-035-provider-framework-tests.md) | Provider framework test suite | T-024, T-025, T-026, T-027, T-028, T-029, T-030, T-031, T-032, T-033, T-034 | yes |
| [T-036](phase-02-provider-framework/T-036-provider-docs-sync.md) | Keep docs/03-providers.md in sync with the manifests | T-035 | yes |

### Phase 03 — Provider catalog

Manifest + live validation for each Tier 1 free gateway, then the Tier 2 majors.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-037](phase-03-provider-catalog/T-037-provider-bynara.md) | Provider: Bynara / NaraRouter (priority) | T-027, T-029, T-031 | yes |
| [T-038](phase-03-provider-catalog/T-038-provider-freellmapi.md) | Provider: FreeLLMAPI | T-027, T-031 | yes |
| [T-039](phase-03-provider-catalog/T-039-provider-apinex.md) | Provider: APInex | T-027, T-031 | yes |
| [T-040](phase-03-provider-catalog/T-040-provider-gorouter.md) | Provider: GoRouter | T-027, T-028, T-031 | yes |
| [T-041](phase-03-provider-catalog/T-041-provider-tokenrouter.md) | Provider: TokenRouter | T-027, T-031 | yes |
| [T-042](phase-03-provider-catalog/T-042-provider-tokenreply.md) | Provider: TokenReply | T-027, T-031 | yes |
| [T-043](phase-03-provider-catalog/T-043-provider-fastrouter.md) | Provider: FastRouter | T-027, T-031 | yes |
| [T-044](phase-03-provider-catalog/T-044-provider-xkiro.md) | Provider: xKiro | T-027, T-031 | yes |
| [T-045](phase-03-provider-catalog/T-045-provider-experiential-labs.md) | Provider: Experiential Labs | T-027, T-031 | yes |
| [T-046](phase-03-provider-catalog/T-046-provider-openrouter.md) | Provider: OpenRouter with free-model tagging | T-027, T-029, T-032 | yes |
| [T-047](phase-03-provider-catalog/T-047-provider-groq.md) | Provider: Groq | T-027, T-032 | yes |
| [T-048](phase-03-provider-catalog/T-048-provider-cerebras.md) | Provider: Cerebras | T-027, T-032 | yes |
| [T-049](phase-03-provider-catalog/T-049-provider-google-ai-studio.md) | Provider: Google AI Studio (free-tier key) | T-028, T-030 | yes |
| [T-050](phase-03-provider-catalog/T-050-provider-mistral.md) | Provider: Mistral | T-027, T-029 | yes |
| [T-051](phase-03-provider-catalog/T-051-provider-github-models.md) | Provider: GitHub Models | T-027, T-030 | yes |
| [T-052](phase-03-provider-catalog/T-052-provider-cloudflare-workers-ai.md) | Provider: Cloudflare Workers AI | T-027, T-033 | yes |
| [T-053](phase-03-provider-catalog/T-053-provider-nvidia-nim.md) | Provider: NVIDIA NIM | T-027, T-032 | yes |
| [T-054](phase-03-provider-catalog/T-054-provider-tier2-majors.md) | Provider: Tier 2 majors batch | T-027, T-028, T-029 | yes |

### Phase 04 — Accounts & OAuth

OAuth flows, token refresh, subscription accounts, Perplexity Sonar search.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-055](phase-04-accounts-oauth/T-055-oauth-framework.md) | OAuth framework (PKCE, browser intent, redirect) | T-006, T-030 | yes |
| [T-056](phase-04-accounts-oauth/T-056-oauth-google.md) | Google account (AI Pro / Gemini) | T-055, T-049 | yes |
| [T-057](phase-04-accounts-oauth/T-057-token-refresh-and-failure-states.md) | Token refresh scheduler and failure states | T-055, T-056 | yes |
| [T-058](phase-04-accounts-oauth/T-058-oauth-github.md) | GitHub account (Copilot / Models) | T-055, T-051 | yes |
| [T-059](phase-04-accounts-oauth/T-059-oauth-huggingface.md) | HuggingFace account | T-055 | yes |
| [T-060](phase-04-accounts-oauth/T-060-perplexity-sonar-api.md) | Perplexity Sonar through the official API | T-027, T-029 | yes |
| [T-061](phase-04-accounts-oauth/T-061-search-endpoint.md) | `POST /v1/search` convenience endpoint | T-060, T-015 | yes |
| [T-062](phase-04-accounts-oauth/T-062-perplexity-account-mode-experimental.md) | Perplexity account mode (experimental, off by default) | T-060 | yes |
| [T-063](phase-04-accounts-oauth/T-063-account-state-ui-data.md) | Account state model and `needs_attention` surfacing | T-057, T-058, T-059 | yes |
| [T-064](phase-04-accounts-oauth/T-064-oauth-test-suite.md) | OAuth test suite with a mock provider | T-055, T-056, T-057, T-058, T-059, T-062 | yes |
| [T-065](phase-04-accounts-oauth/T-065-accounts-documentation-de.md) | Account setup documentation for the owner | T-064 | yes |

### Phase 05 — Wire protocols

Three request/response dialects, streaming, tool calls, media, and one error taxonomy.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-066](phase-05-wire-protocols/T-066-protocol-models.md) | Shared protocol models and normalisation | T-026 | yes |
| [T-067](phase-05-wire-protocols/T-067-openai-chat-completions.md) | OpenAI chat completions (non-streaming) | T-066, T-027 | yes |
| [T-068](phase-05-wire-protocols/T-068-openai-streaming-sse.md) | OpenAI streaming (SSE) | T-067 | yes |
| [T-069](phase-05-wire-protocols/T-069-openai-models-and-completions.md) | OpenAI models list and legacy completions | T-029, T-067 | yes |
| [T-070](phase-05-wire-protocols/T-070-anthropic-messages.md) | Anthropic messages (non-streaming) | T-066, T-027, T-028 | yes |
| [T-071](phase-05-wire-protocols/T-071-anthropic-streaming-conformance.md) | Anthropic streaming conformance | T-070, T-068 | yes |
| [T-072](phase-05-wire-protocols/T-072-count-tokens.md) | `/v1/messages/count_tokens` | T-070 | yes |
| [T-073](phase-05-wire-protocols/T-073-gemini-surface.md) | Gemini surface (`/v1beta`) | T-066, T-027 | yes |
| [T-074](phase-05-wire-protocols/T-074-tool-call-translation.md) | Tool call translation across dialects | T-067, T-070, T-073 | yes |
| [T-075](phase-05-wire-protocols/T-075-media-endpoints.md) | Media endpoints (images, TTS, STT) | T-073, T-026 | yes |
| [T-076](phase-05-wire-protocols/T-076-embeddings-endpoint.md) | Embeddings endpoint | T-066, T-029 | yes |
| [T-077](phase-05-wire-protocols/T-077-error-mapping.md) | Unified error mapping and the `droidroute` error object | T-067, T-070, T-073, T-026 | yes |
| [T-078](phase-05-wire-protocols/T-078-protocol-conformance-suite.md) | Protocol conformance suite (golden files) | T-067, T-068, T-069, T-070, T-071, T-072, T-073, T-074, T-075, T-076, T-077 | yes |

### Phase 06 — Routing

Candidate resolution, strategies, quota ledgers, multi-key chaining, failover and explainability.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-079](phase-06-routing/T-079-candidate-resolution.md) | Candidate resolution and canonical model ids | T-029, T-025 | yes |
| [T-080](phase-06-routing/T-080-aliases-and-model-groups.md) | Aliases and model groups | T-079 | yes |
| [T-081](phase-06-routing/T-081-key-pool-quota-ledger.md) | Key pool and quota ledger | T-030, T-032 | yes |
| [T-082](phase-06-routing/T-082-quota-learning.md) | Quota learning from `429` and rate-limit headers | T-081, T-077 | yes |
| [T-083](phase-06-routing/T-083-multi-provider-key-chaining.md) | Multi-provider key chaining | T-081, T-082, T-080 | yes |
| [T-084](phase-06-routing/T-084-routing-strategies.md) | Routing strategies | T-079, T-081, T-032 | yes |
| [T-085](phase-06-routing/T-085-health-scoring.md) | Health scoring and persistence | T-032, T-081 | yes |
| [T-086](phase-06-routing/T-086-circuit-breaker-retry.md) | Circuit breaker and retry policy | T-085 | yes |
| [T-087](phase-06-routing/T-087-failover-loop.md) | Failover loop and mid-stream policy | T-084, T-086, T-068, T-071 | yes |
| [T-088](phase-06-routing/T-088-hedging-optional.md) | Optional request hedging | T-087 | yes |
| [T-089](phase-06-routing/T-089-routing-explain.md) | `/v1/routing/explain` and decision logging | T-087, T-084 | yes |
| [T-090](phase-06-routing/T-090-routing-test-suite.md) | Routing test suite with failure injection | T-079, T-080, T-081, T-082, T-083, T-084, T-085, T-086, T-087, T-088, T-089 | yes |

### Phase 07 — UI

Compose shell, dashboard, provider and key management, routing controls, settings, onboarding.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-091](phase-07-ui/T-091-app-shell-navigation.md) | App shell and navigation | T-007, T-012 | yes |
| [T-092](phase-07-ui/T-092-theme-and-visuals.md) | Theme, dark/light and typography | T-091 | yes |
| [T-093](phase-07-ui/T-093-localisation-de-en.md) | Localisation: German default, English available | T-091 | yes |
| [T-094](phase-07-ui/T-094-dashboard-screen.md) | Dashboard screen | T-092, T-032, T-089 | yes |
| [T-095](phase-07-ui/T-095-usage-charts.md) | Daily and weekly usage views | T-094, T-081 | yes |
| [T-096](phase-07-ui/T-096-providers-list.md) | Providers list, filters and one-click connect | T-025, T-031, T-033 | yes |
| [T-097](phase-07-ui/T-097-provider-detail.md) | Provider detail screen | T-096, T-032, T-082 | yes |
| [T-098](phase-07-ui/T-098-custom-provider-form.md) | Custom provider form with discovery | T-033, T-096 | yes |
| [T-099](phase-07-ui/T-099-keys-screen.md) | Keys screen: masking, one-time reveal, clipboard | T-006, T-016, T-096 | yes |
| [T-100](phase-07-ui/T-100-routing-screen.md) | Routing screen: strategies, aliases, key chains | T-080, T-083, T-084 | yes |
| [T-101](phase-07-ui/T-101-routing-explain-viewer.md) | Routing explain viewer | T-089, T-100 | yes |
| [T-102](phase-07-ui/T-102-settings-server-and-keys.md) | Settings: server, access and client keys | T-013, T-014, T-016, T-021 | yes |
| [T-103](phase-07-ui/T-103-settings-integrations.md) | Settings: tunnel checklists and Termux permission | T-091, T-021, T-014 | yes |
| [T-104](phase-07-ui/T-104-logs-viewer.md) | Logs viewer with redaction indicator and export | T-008, T-017 | yes |
| [T-105](phase-07-ui/T-105-onboarding.md) | First-run onboarding | T-096, T-099, T-102 | yes |
| [T-106](phase-07-ui/T-106-accessibility-adaptive.md) | Accessibility and adaptive layout pass | T-091, T-092, T-093, T-094, T-096, T-097, T-098, T-099, T-100, T-102, T-103, T-104, T-105 | yes |

### Phase 08 — Local models

Termux bridge, runtime resolution, model catalog, memory guard, and special-purpose models.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-107](phase-08-local-models/T-107-termux-bridge.md) | Termux bridge (RUN_COMMAND intent with HTTP fallback) | T-103, T-022 | yes |
| [T-108](phase-08-local-models/T-108-llama-runtime-resolution.md) | llama.cpp runtime resolution | T-107 | yes |
| [T-109](phase-08-local-models/T-109-llama-process-lifecycle.md) | llama-server process lifecycle | T-108 | yes |
| [T-110](phase-08-local-models/T-110-model-catalog.md) | Model catalog and curated list | T-109, T-005 | yes |
| [T-111](phase-08-local-models/T-111-model-download.md) | Model download with resume and checksum | T-110, T-007 | yes |
| [T-112](phase-08-local-models/T-112-memory-guard.md) | Memory estimation, warnings and trim handling | T-109, T-110 | yes |
| [T-113](phase-08-local-models/T-113-local-provider-registration.md) | Register local models as ordinary providers | T-109, T-027 | yes |
| [T-114](phase-08-local-models/T-114-local-embeddings.md) | Local embedding models | T-113, T-076 | yes |
| [T-115](phase-08-local-models/T-115-local-speech.md) | Speech models (STT and TTS) | T-108, T-075 | yes |
| [T-116](phase-08-local-models/T-116-local-vision.md) | Local vision models | T-113, T-112 | yes |
| [T-117](phase-08-local-models/T-117-embedded-runtime-spike.md) | Embedded (JNI) runtime spike and decision | T-113 | yes |

### Phase 09 — MCP & plugins

Discover MCP servers from the host environment, aggregate them, and bridge tool calls over the local API.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-118](phase-09-mcp-plugins/T-118-mcp-discovery.md) | MCP configuration discovery | T-107 | yes |
| [T-119](phase-09-mcp-plugins/T-119-mcp-registry.md) | Aggregated MCP registry with change watching | T-118, T-005 | yes |
| [T-120](phase-09-mcp-plugins/T-120-mcp-bridge-api.md) | MCP bridge API | T-119, T-015, T-022 | yes |
| [T-121](phase-09-mcp-plugins/T-121-mcp-stdio-transport.md) | stdio transport launcher with timeouts and reaping | T-120 | yes |
| [T-122](phase-09-mcp-plugins/T-122-mcp-http-transport.md) | HTTP and SSE transport | T-120 | yes |
| [T-123](phase-09-mcp-plugins/T-123-connectors-screen.md) | Connectors screen | T-120, T-103 | yes |
| [T-124](phase-09-mcp-plugins/T-124-plugin-inventory.md) | Plugin and skill inventory endpoint | T-120, T-031 | yes |
| [T-125](phase-09-mcp-plugins/T-125-mcp-tests.md) | MCP test suite | T-118, T-119, T-120, T-121, T-122, T-123, T-124 | yes |
| [T-126](phase-09-mcp-plugins/T-126-mcp-documentation-de.md) | MCP documentation and owner guide | T-125 | yes |

### Phase 10 — Logging & handover

Retention, status automation, evidence bundles and adversarial resume drills.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-127](phase-10-logging-handover/T-127-log-retention-in-app.md) | Log retention and rotation inside the app | T-008, T-104 | yes |
| [T-128](phase-10-logging-handover/T-128-status-automation.md) | Status file automation | T-017, T-009 | yes |
| [T-129](phase-10-logging-handover/T-129-daily-summary-generation.md) | Daily summary generation | T-128 | yes |
| [T-130](phase-10-logging-handover/T-130-chain-log-integrity.md) | Chain log integrity verification | T-128 | yes |
| [T-131](phase-10-logging-handover/T-131-handover-bundle.md) | Handover evidence bundle | T-130, T-129 | yes |
| [T-132](phase-10-logging-handover/T-132-resume-drill-clean.md) | Resume drill: clean handover | T-131 | yes |
| [T-133](phase-10-logging-handover/T-133-resume-drill-interrupted.md) | Resume drill: interrupted mid-task | T-132 | yes |
| [T-134](phase-10-logging-handover/T-134-request-task-trace-correlation.md) | Correlate runtime requests with build tasks | T-017, T-131 | yes |
| [T-135](phase-10-logging-handover/T-135-handover-docs-verification.md) | Handover documentation verification | T-132, T-133, T-134 | yes |

### Phase 11 — Delivery

Performance and security hardening, the acceptance run, the release pipeline and owner documentation.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-136](phase-11-delivery/T-136-performance-pass.md) | Performance pass | T-109, T-094, T-106 | yes |
| [T-137](phase-11-delivery/T-137-security-review.md) | Security review against docs/05-security.md | T-099, T-120, T-112 | yes |
| [T-138](phase-11-delivery/T-138-dependency-licence-review.md) | Dependency and licence review | T-136, T-137 | yes |
| [T-139](phase-11-delivery/T-139-test-suite-consolidation.md) | Test suite consolidation and coverage review | T-136, T-138 | yes |
| [T-140](phase-11-delivery/T-140-acceptance-run-1.md) | Acceptance run A1–A3 (server, agents, providers) | T-139, T-021, T-096 | yes |
| [T-141](phase-11-delivery/T-141-acceptance-run-2.md) | Acceptance run A4–A6 (accounts, failover, dashboard) | T-140 | yes |
| [T-142](phase-11-delivery/T-142-acceptance-run-3.md) | Acceptance run A7–A9 (local models, MCP, repository) | T-141 | yes |
| [T-143](phase-11-delivery/T-143-acceptance-run-4.md) | Acceptance run A10–A12 (handover, build, hygiene) | T-142, T-133 | yes |
| [T-144](phase-11-delivery/T-144-release-pipeline.md) | Release pipeline and first tagged release | T-143 | yes |
| [T-145](phase-11-delivery/T-145-owner-documentation.md) | Owner documentation in German | T-144 | yes |
| [T-146](phase-11-delivery/T-146-repository-beauty-pass.md) | Repository presentation pass | T-145 | yes |
| [T-147](phase-11-delivery/T-147-chain-closure.md) | Chain closure and final handover statement | T-146 | yes |

### Phase 12 — OmniRoute parity & power features

Combos, all 19 strategies, fusion/pipeline, compression, cost telemetry, guardrails, memory, A2A, tooling wiring.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-148](phase-12-parity-power/T-148-combo-engine.md) | Combo engine and virtual auto models | T-083, T-084, T-089 | yes |
| [T-149](phase-12-parity-power/T-149-full-strategy-set.md) | Complete the 19-strategy set | T-148 | yes |
| [T-150](phase-12-parity-power/T-150-fusion-and-pipeline.md) | Fusion and pipeline strategies | T-149 | yes |
| [T-151](phase-12-parity-power/T-151-auto-scoring-engine.md) | Multi-factor auto scoring engine | T-148, T-085, T-082 | yes |
| [T-152](phase-12-parity-power/T-152-admission-control.md) | Adaptive admission, overload protection and rolling leases | T-087 | yes |
| [T-153](phase-12-parity-power/T-153-token-compression.md) | Token compression engines | T-068, T-081 | yes |
| [T-154](phase-12-parity-power/T-154-prompt-cache-pinning.md) | Prompt-cache pinning and cache-hit telemetry | T-149, T-081 | yes |
| [T-155](phase-12-parity-power/T-155-cost-telemetry.md) | Cost telemetry headers and per-key USD budgets | T-095, T-081, T-017 | yes |
| [T-156](phase-12-parity-power/T-156-quota-share.md) | Quota-Share across pooled keys | T-081, T-083 | yes |
| [T-157](phase-12-parity-power/T-157-memory-subsystem.md) | Memory subsystem (opt-in, local) | T-066, T-006 | yes |
| [T-158](phase-12-parity-power/T-158-prompt-injection-guard.md) | Prompt-injection guard | T-066, T-077 | yes |
| [T-159](phase-12-parity-power/T-159-credential-masking-guardrail.md) | Credential-masking guardrail | T-008, T-066 | yes |
| [T-160](phase-12-parity-power/T-160-modality-bridge.md) | Modality bridge (vision, audio, video) | T-075, T-073, T-026 | yes |
| [T-161](phase-12-parity-power/T-161-ocr-audio-translation-websearch.md) | OCR, audio translation and web-search fallback | T-075, T-160 | yes |
| [T-162](phase-12-parity-power/T-162-video-generation.md) | Video generation endpoint | T-160, T-075 | yes |
| [T-163](phase-12-parity-power/T-163-a2a-server.md) | A2A server for agent delegation | T-120, T-151 | yes |
| [T-164](phase-12-parity-power/T-164-models-ordering-and-free-tier-view.md) | Canonical model ordering and free-tier catalogue view | T-069, T-082, T-095 | yes |
| [T-165](phase-12-parity-power/T-165-cli-setup-and-remote-mode.md) | CLI setup helpers and remote mode with scoped tokens | T-016, T-021, T-022 | yes |
| [T-166](phase-12-parity-power/T-166-build-agent-tooling-wiring.md) | Build-agent tooling wiring (skills, plugins, MCP) | T-131 | yes |

### Phase 13 — Competitive absorption & Android edge

Any-provider detection, migration importers, local-first providers, extra wire surfaces, token savers, affinity, offline mode, phone-awareness, self-update.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-167](phase-13-competitive-edge/T-167-provider-autodetection.md) | Automatic provider detection from any URL | T-024, T-029, T-033 | yes |
| [T-168](phase-13-competitive-edge/T-168-migration-importers.md) | Migration importers from other routers | T-024, T-033 | yes |
| [T-169](phase-13-competitive-edge/T-169-local-first-and-noauth-providers.md) | Local-first and no-auth providers, with fail-closed semantics | T-025, T-027, T-031, T-113 | yes |
| [T-170](phase-13-competitive-edge/T-170-extra-wire-surfaces.md) | Extra wire surfaces: OpenAI Responses API and Vertex AI | T-066, T-027, T-055 | yes |
| [T-171](phase-13-competitive-edge/T-171-subscription-login-adapters.md) | Subscription login adapters and multi-account pools | T-057, T-081, T-030 | yes |
| [T-172](phase-13-competitive-edge/T-172-tool-output-filters.md) | Tool-output compression filters (lossless tool results) | T-153 | yes |
| [T-173](phase-13-competitive-edge/T-173-response-style-presets.md) | Response-style presets (terse and minimal-code), opt-in | T-153, T-066 | yes |
| [T-174](phase-13-competitive-edge/T-174-conversation-affinity.md) | Conversation affinity (sticky provider) | T-154, T-087 | yes |
| [T-175](phase-13-competitive-edge/T-175-offline-first-mode.md) | Offline-first mode with queued cloud requests | T-113, T-152 | yes |
| [T-176](phase-13-competitive-edge/T-176-phone-aware-routing.md) | Battery, thermal and network-aware routing | T-113, T-084 | yes |
| [T-177](phase-13-competitive-edge/T-177-android-surfaces.md) | Quick Settings tile, widget, share sheet and text-selection action | T-105, T-091 | yes |
| [T-178](phase-13-competitive-edge/T-178-mobile-data-accounting.md) | Mobile-data accounting and budget | T-155, T-176 | yes |
| [T-179](phase-13-competitive-edge/T-179-offline-model-catalog.md) | Offline model catalog pack | T-110, T-111 | yes |
| [T-180](phase-13-competitive-edge/T-180-in-app-updater.md) | In-app updater with signature verification and rollback | T-144, T-009 | yes |
| [T-181](phase-13-competitive-edge/T-181-signed-catalog-updates.md) | Catalog updates without an app release | T-164, T-180 | yes |
| [T-182](phase-13-competitive-edge/T-182-debug-capture-mode.md) | Debug capture mode (redacted, time-bounded) | T-017, T-104 | yes |
| [T-183](phase-13-competitive-edge/T-183-qr-config-portability.md) | Config portability by QR code (no cloud) | T-034, T-006 | yes |
| [T-184](phase-13-competitive-edge/T-184-native-benchmark.md) | Native-versus-service benchmark on this device | T-136, T-180 | yes |

### Phase 14 — Design audit & release polish

Token conformance, a proven gate, screen-by-screen craft review, measured contrast and accessibility, state completeness, design acceptance.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-185](phase-14-design-audit/T-185-token-conformance-audit.md) | Token conformance audit across the whole UI | T-092, T-106 | yes |
| [T-186](phase-14-design-audit/T-186-prove-the-gate-bites.md) | Prove the design gate bites on the real source tree | T-185 | yes |
| [T-187](phase-14-design-audit/T-187-craft-review-and-fixes.md) | Screen-by-screen craft review with the four tests | T-185 | yes |
| [T-188](phase-14-design-audit/T-188-contrast-and-accessibility-evidence.md) | Measured contrast, motion and accessibility evidence | T-106 | yes |
| [T-189](phase-14-design-audit/T-189-state-completeness-pass.md) | State completeness pass (loading, empty, error, partial, offline) | T-187 | yes |
| [T-190](phase-14-design-audit/T-190-design-acceptance.md) | Design acceptance and the closing statement | T-186, T-188, T-189 | yes |

### Phase 15 — Security & privacy audit

Threat model and test mapping, static analysis and licences, vault crypto review, network exposure, component and data-at-rest review, signing and audit trail.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-191](phase-15-security-audit/T-191-threat-model.md) | Threat model and test mapping | T-014, T-021, T-165 | yes |
| [T-192](phase-15-security-audit/T-192-static-analysis-and-dependencies.md) | Static analysis, dependencies and licences | T-009, T-136, T-144 | yes |
| [T-193](phase-15-security-audit/T-193-vault-crypto-review.md) | Secret storage and vault crypto review | T-006, T-159, T-165 | yes |
| [T-194](phase-15-security-audit/T-194-network-exposure-audit.md) | Network surface and exposure audit | T-014, T-021, T-165 | yes |
| [T-195](phase-15-security-audit/T-195-component-intent-and-at-rest-review.md) | Components, intents and data at rest | T-098, T-099, T-103, T-104 | yes |
| [T-196](phase-15-security-audit/T-196-signing-supply-chain-audit-trail.md) | Signing, CI permissions and the audit trail | T-144, T-165, T-180 | yes |

### Phase 16 — Visual evidence & launch

Screenshot harness, automatic visual analysis, visual Q&A loop, README gallery, launch video via brag, launch assets.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-197](phase-16-visual-evidence/T-197-screenshot-harness.md) | Deterministic screenshot harness | T-106, T-190 | yes |
| [T-198](phase-16-visual-evidence/T-198-automatic-visual-analysis.md) | Automatic visual analysis of every screenshot | T-197 | yes |
| [T-199](phase-16-visual-evidence/T-199-visual-qa-loop.md) | Visual Q&A loop with findings and fixes | T-197, T-198 | yes |
| [T-200](phase-16-visual-evidence/T-200-readme-gallery.md) | README gallery that cannot go stale | T-197, T-199 | yes |
| [T-201](phase-16-visual-evidence/T-201-launch-video-brag.md) | Launch video with the brag plugin | T-200 | yes |
| [T-202](phase-16-visual-evidence/T-202-launch-assets-and-visual-acceptance.md) | Launch assets and visual acceptance | T-201 | yes |

### Phase 17 — One-tap access, key issuing & tooling coverage

One-tap free start, device-code sign-in, local-only key issuing for DroidRoute itself, tooling coverage proof, the reusable workflow plugin, and the clone-from-scratch freeze.

| Task | Title | Depends on | Parallel |
|---|---|---|---|
| [T-203](phase-17-access-and-tooling/T-203-one-tap-free-start.md) | One-tap free start with no account | T-096, T-105, T-169 | yes |
| [T-204](phase-17-access-and-tooling/T-204-device-code-sign-in.md) | One-tap sign-in with the device code flow | T-057, T-171 | yes |
| [T-205](phase-17-access-and-tooling/T-205-local-only-key-issuing.md) | DroidRoute key issuing, readable by nobody | T-016, T-021, T-099, T-165, T-193 | yes |
| [T-206](phase-17-access-and-tooling/T-206-tooling-coverage-proof.md) | Proof that every applicable skill, plugin and MCP server is used | T-166, T-190 | yes |
| [T-207](phase-17-access-and-tooling/T-207-workflow-plugin-and-publish.md) | Reusable build workflow: consume it here, publish it as `routin` | T-166, T-206 | yes |
| [T-208](phase-17-access-and-tooling/T-208-clone-from-scratch-freeze.md) | Clone-from-scratch verification and freeze | T-202, T-205, T-207 | yes |
## Generated file

This index and every task file are produced by `tools/generate_plan.py` from `tools/plan_data/`.
Edit the data, run the generator, commit both. CI fails when the tree and the data disagree
(`.github/workflows/repo-hygiene.yml` → *Plan integrity*).
