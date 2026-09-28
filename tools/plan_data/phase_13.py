"""Phase 13 — Competitive absorption and Android-native differentiators (the v0.3 milestone).

Absorbs what 9Router, OmniRoute, CLIProxyAPI, LiteLLM and friends have that
DroidRoute lacks (docs/13-competitive-landscape.md), then adds the capabilities
none of them have: phone-awareness, offline-first operation, self-update with
rollback, and catalogs that stay current without an app release.
"""

from common import Phase, Task

PHASE = Phase(
    number=13,
    slug="competitive-edge",
    title="Competitive absorption & Android edge",
    summary="Any-provider detection, migration importers, local-first providers, extra wire surfaces, token savers, affinity, offline mode, phone-awareness, self-update.",
)

TASKS = [
    Task(
        id=167,
        slug="provider-autodetection",
        title="Automatic provider detection from any URL",
        goal=(
            "Turn 'any possible provider' into one paste: probe an endpoint, infer whether it speaks OpenAI, Anthropic, "
            "Gemini or the OpenAI Responses shape, discover its models, and generate a validated manifest the owner can review."
        ),
        deps=[24, 29, 33],
        est="120-240 min",
        skills=[
            ("droidroute-provider-manifest", "the probe order, the signals per dialect, and what must be confirmed by a human"),
            ("droidroute-verification", "probe tests against four local stub servers in the four dialects, plus hostile inputs"),
        ],
        deliverables=[
            "`provider/detect/ProviderProbe.kt` — dialect inference, model discovery, capability sniffing",
            "A review screen showing the generated manifest with each inferred field marked inferred vs confirmed",
        ],
        steps=[
            "Probe in a fixed order: `/models`, then a one-token chat call per dialect, then an Anthropic `/v1/messages` probe.",
            "Infer the dialect from the response shape, not from the URL string — never guess from a domain name.",
            "Mark every inferred field as inferred; require the owner to confirm before the provider is enabled.",
            "Refuse to save a manifest whose endpoints returned 404 for every probe, and say which paths were tried.",
        ],
        accept=[
            "Each of the four stub dialects is detected correctly (asserted)",
            "An endpoint that answers nothing produces a failure listing every probed path",
            "No provider is enabled without a confirmed base URL and at least one successful call",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ProviderProbe*'",
        ],
        state="Adding an unknown provider is one paste plus one confirmation instead of reading documentation for an hour.",
    ),
    Task(
        id=168,
        slug="migration-importers",
        title="Migration importers from other routers",
        goal=(
            "Import an existing router configuration so switching is a paste: OmniRoute, 9Router, LiteLLM, one-api/new-api "
            "and CLIProxyAPI formats, with secrets flagged rather than imported silently."
        ),
        deps=[24, 33],
        est="120-240 min",
        skills=[
            ("droidroute-provider-manifest", "the real config shapes of each tool, and what maps cleanly to a manifest"),
            ("droidroute-verification", "fixtures per format, including a file with embedded secrets"),
        ],
        deliverables=[
            "`provider/import/Importer.kt` with one parser per supported tool",
            "An import report: what was recognised, what was skipped, and what needs the owner's key",
        ],
        steps=[
            "Parse each format into the internal model without inventing fields that the source did not contain.",
            "Detect embedded credentials and move them to the vault instead of copying them into an importable manifest file.",
            "Report unmapped settings explicitly rather than dropping them silently.",
            "Test with fixtures for each format, including a partially broken file.",
        ],
        accept=[
            "Each supported format imports its providers with correct base URLs (asserted per fixture)",
            "A credential found in the source is stored in the vault and never written to disk",
            "Unrecognised entries are listed in the report, not dropped",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Importer*'",
        ],
        state="Moving from a competitor is a paste with a report, not a weekend of retyping.",
    ),
    Task(
        id=169,
        slug="local-first-and-noauth-providers",
        title="Local-first and no-auth providers, with fail-closed semantics",
        goal=(
            "Support no-auth free providers and self-hosted endpoints (STT, TTS, embeddings, llama-server, vLLM), and make the "
            "rule explicit: a local provider never silently falls back to a cloud provider."
        ),
        deps=[25, 27, 31, 113],
        est="120-240 min",
        skills=[
            ("droidroute-provider-manifest", "self-hosted endpoint shapes and the base-URL pitfalls that break them"),
            ("droidroute-verification", "fail-closed tests: a misconfigured local provider must error, never reroute to a cloud host"),
        ],
        deliverables=[
            "Provider category `local` with a required base URL and no cloud fallback",
            "No-auth provider support: auth type `none`, model auto-fetch, one-click connect without a key",
        ],
        steps=[
            "Model `local` providers so a missing base URL is a configuration error, not a default endpoint.",
            "Implement no-auth providers with discovery only and a clear warning that they are third-party free tiers.",
            "Extend the candidate selector so a `local` provider is never replaced by a cloud candidate without the owner's policy saying so.",
            "Test: a local provider with a broken URL fails the request and names the misconfiguration.",
        ],
        accept=[
            "A local provider with a missing or wrong base URL errors and never calls a cloud host (asserted)",
            "A no-auth provider connects and lists models without a key",
            "The self-hosted path is documented with the exact URL conventions that work",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*LocalFirst*'",
        ],
        state="Local inference is respected, and a typo cannot quietly send the owner's text to a third party.",
    ),
    Task(
        id=170,
        slug="extra-wire-surfaces",
        title="Extra wire surfaces: OpenAI Responses API and Vertex AI",
        goal="Add the surfaces competitors speak that DroidRoute does not: the OpenAI Responses shape and Google Vertex AI with Application Default Credentials.",
        deps=[66, 27, 55],
        est="120-240 min",
        skills=[
            ("llm-gateway-protocols", "Responses API event model and the Vertex request shape"),
            ("droidroute-verification", "golden files per surface plus credential-failure paths"),
        ],
        deliverables=[
            "`/v1/responses` decoding and streaming to the normalised model",
            "Vertex AI provider path supporting ADC (`authorized_user`) alongside service-account credentials",
        ],
        steps=[
            "Map Responses-style input/output items onto the normalised model without losing tool calls.",
            "Implement Vertex auth resolution: ADC first, then service account, and report which one was used.",
            "Add golden files for both surfaces and wire them into the conformance suite.",
            "Never log the credential material; log only the credential type.",
        ],
        accept=[
            "A Responses-shaped request round-trips through the normalised model (asserted)",
            "Vertex auth resolves via ADC on the device, or the failure names what was missing",
            "Credential type appears in logs; credential material does not",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Responses*' --tests '*Vertex*'",
        ],
        state="Two more client and provider dialects work, covering the surfaces competitors advertise.",
    ),
    Task(
        id=171,
        slug="subscription-login-adapters",
        title="Subscription login adapters and multi-account pools",
        goal=(
            "Connect CLI-subscription identities (Claude Code, Codex, GitHub Copilot, Cursor, Antigravity-style) and hold several "
            "accounts per provider, rotating them with the same quota ledger used for API keys."
        ),
        deps=[57, 81, 30],
        est="180-300 min",
        skills=[
            ("oauth-device-flow", "each tool's real login flow, token storage and refresh semantics"),
            ("ai-governors", "using a subscription programmatically has terms — surface them, never hide them"),
        ],
        deliverables=[
            "`provider/accounts/SubscriptionAdapter.kt` with a per-tool login flow",
            "Multi-account pools: several accounts per provider, selected by the quota ledger and health score",
        ],
        steps=[
            "Implement one flow at a time, validating against the tool's own current documentation.",
            "Store every account's tokens in the vault, keyed by account label, never in a shared blob.",
            "Extend the key pool to accounts so rotation and parking work identically for both.",
            "State plainly, in the UI and the docs, what each subscription permits programmatically.",
        ],
        accept=[
            "Each implemented adapter completes a login and answers a request, or is documented as not feasible with the reason",
            "Two accounts on one provider rotate by quota (asserted)",
            "The terms note exists per adapter and is shown before the first login",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*SubscriptionAdapter*'",
        ],
        state="Subscription-based routing — what 9Router, CLIProxyAPI and dario are built around — works natively.",
    ),
    Task(
        id=172,
        slug="tool-output-filters",
        title="Tool-output compression filters (lossless tool results)",
        goal=(
            "Compress the tool results that eat prompts — `git diff`, `git status`, `grep`, `find`, `ls`, `tree`, log dumps — "
            "with auto-detection, a per-request bypass header, and a guarantee that a failing filter keeps the original text."
        ),
        deps=[153],
        est="180-300 min",
        skills=[
            ("droidroute-routing", "where in the request pipeline this runs: before dialect translation, per tool result"),
            ("droidroute-verification", "losslessness proofs per filter and a fail-open test for each"),
        ],
        deliverables=[
            "`protocol/compression/filters/` — one filter per output family, each with its own tests",
            "Automatic filter selection from the head of the tool result, and `X-DroidRoute-Token-Saver: off` as a bypass",
        ],
        steps=[
            "Implement each filter to be reversible and to bail out if the result is not smaller.",
            "Select the filter from the content itself, not from a path or a caller-supplied hint.",
            "Record per-filter savings so the owner can see which filters actually pay off on their workload.",
            "Test: identical semantic content, smaller payload, and the filter that throws keeps the original.",
        ],
        accept=[
            "Every filter is lossless on its fixture corpus (round-trip asserted)",
            "A throwing filter leaves the original content untouched and logs the failure",
            "The bypass header disables all filters for that request (asserted)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ToolFilter*'",
        ],
        state="The single biggest token cost in agent traffic — tool output — is cut without changing what the model sees.",
    ),
    Task(
        id=173,
        slug="response-style-presets",
        title="Response-style presets (terse and minimal-code), opt-in",
        goal=(
            "Offer the brevity modes competitors inject by default — terse answers, minimal YAGNI-first code — as explicit, "
            "opt-in presets with a hard carve-out for safety, validation and anything the owner asked for."
        ),
        deps=[153, 66],
        est="90-180 min",
        skills=[
            ("droidroute-verification", "prove the preset never overrides an explicit instruction and never strips safety guidance"),
            ("ai-governors", "a style mode that changes answers without consent is a defect; make the boundary visible"),
        ],
        deliverables=[
            "Presets `off` (default), `concise`, `minimal-code` with documented injected text",
            "Per-alias and per-request selection; the preset used is reported in the response headers",
        ],
        steps=[
            "Write each preset's injected instruction as a file, reviewed like code, with the carve-outs stated inline.",
            "Default to `off` and require an explicit selection per alias or per request.",
            "Guarantee that an explicit owner instruction wins over the preset (asserted with a fixture).",
            "Report the active preset so the owner can see why an answer came back terse.",
        ],
        accept=[
            "Default is `off` and no request gets a preset it did not ask for (asserted)",
            "An explicit instruction in the request is not overridden by the preset (asserted)",
            "The active preset is visible in the response headers and the log",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*StylePreset*'",
        ],
        state="Token-saving answer styles exist without silently rewriting the owner's instructions.",
    ),
    Task(
        id=174,
        slug="conversation-affinity",
        title="Conversation affinity (sticky provider)",
        goal=(
            "Fix the most repeated complaint about this class of router: switching models mid-conversation resends context and "
            "loses provider-side cache. Pin a conversation to a provider while it is healthy, and say plainly when the pin breaks."
        ),
        deps=[154, 87],
        est="120-240 min",
        skills=[
            ("droidroute-routing", "affinity as a soft constraint with an explicit override order"),
            ("droidroute-verification", "affinity holds, affinity yields on quota, and the switch is recorded with a reason"),
        ],
        deliverables=[
            "`routing/Affinity.kt` keyed by a conversation fingerprint, with a documented precedence against quota, budget and health",
            "A per-conversation record: current provider, switches, and the reason for each switch",
        ],
        steps=[
            "Derive the fingerprint from stable request elements without storing prompt content beyond a hash.",
            "Keep the pin while the provider is healthy and inside budget; break it for quota, breaker or explicit override.",
            "Record every switch with its reason so the owner can see why the cache was lost.",
            "Expire fingerprints so the store cannot grow without bound.",
        ],
        accept=[
            "A conversation stays on one provider across several turns (asserted)",
            "An exhausted quota breaks the pin and the switch reason is recorded (asserted)",
            "No prompt content is stored — only a fingerprint (asserted by inspecting the store)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Affinity*'",
        ],
        state="Provider switching stops quietly destroying prompt cache and re-billing the same context.",
    ),
    Task(
        id=175,
        slug="offline-first-mode",
        title="Offline-first mode with queued cloud requests",
        goal=(
            "Answer from a local model when there is no connectivity, queue what only a cloud provider can do, and replay it when "
            "the network returns — with the owner informed, never silently."
        ),
        deps=[113, 152],
        est="120-240 min",
        skills=[
            ("android-platform", "connectivity callbacks and airplane mode across Android versions"),
            ("droidroute-verification", "offline, return-to-online, queue overflow and cancelled-queue paths"),
        ],
        deliverables=[
            "`routing/OfflinePolicy.kt` with a documented decision table: connectivity × local availability × request type",
            "A bounded queue with per-item expiry, visible in the UI, cancellable per item",
        ],
        steps=[
            "Decide per request: serve locally, queue, or fail immediately with a clear offline error.",
            "Bound the queue by count and age; drop with a logged reason instead of growing forever.",
            "Replay on connectivity return in submission order, respecting budgets and quotas.",
            "Tell the owner in the response and the UI when an answer came from the local model because the network was gone.",
        ],
        accept=[
            "With connectivity off and a model loaded, a request is answered locally and labelled as such",
            "With connectivity off and no model, a cloud-only request is queued and replayable, or refused with a clear reason",
            "The queue is bounded and expiry is enforced (asserted)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*OfflinePolicy*'",
        ],
        state="The gateway keeps working with no network, which no competitor intends to do.",
    ),
    Task(
        id=176,
        slug="phone-aware-routing",
        title="Battery, thermal and network-aware routing",
        goal=(
            "Use what only a phone knows: prefer local or cheap candidates when the battery is low, avoid loading a large model "
            "when the device is hot, and honour a policy for metered connections."
        ),
        deps=[113, 84],
        est="120-240 min",
        skills=[
            ("android-platform", "BatteryManager, thermal status, ConnectivityManager metered detection"),
            ("performance-android", "measure the actual cost difference before claiming a benefit"),
        ],
        deliverables=[
            "`routing/DeviceState.kt` exposing battery level/charging, thermal status, metered state and network type",
            "Configurable policies: `battery_floor`, `thermal_ceiling`, `metered_policy` (allow / ask / block)",
        ],
        steps=[
            "Read device state through the platform APIs and expose it as candidate-selection inputs.",
            "Implement policies as routing constraints with a reason string, so each decision is explainable.",
            "Refuse a local model load above the thermal ceiling with a message naming the temperature class.",
            "Measure and record the effect of the metered policy on data usage.",
        ],
        accept=[
            "Below the battery floor, a local or free candidate is preferred with the reason visible (asserted)",
            "A blocked metered request returns a clear policy error instead of silently spending mobile data",
            "Thermal refusal names the thermal status and what to do about it",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*DeviceState*'",
            "adb shell dumpsys battery | head -5",
        ],
        state="Routing decisions respect the device they run on — a capability no server-side gateway has.",
    ),
    Task(
        id=177,
        slug="android-surfaces",
        title="Quick Settings tile, widget, share sheet and text-selection action",
        goal="Make DroidRoute reachable in one gesture: toggle from Quick Settings, see today's usage on the home screen, and send selected text or a shared image to the local model.",
        deps=[105, 91],
        est="120-240 min",
        skills=[
            ("android-compose-ui", "widget and tile are separate UI systems; keep them thin"),
            ("performance-android", "a widget must not poll; update on events only"),
        ],
        deliverables=[
            "Quick Settings tile starting/stopping the server, reflecting real state",
            "Home-screen widget: server state, today's tokens, parked keys count",
            "Share-sheet target and text-selection action that route through the local model first",
        ],
        steps=[
            "Implement the tile and widget over the existing service state, with no logic of their own.",
            "Handle the share intent for text and images, preferring a local model and falling back per policy.",
            "Update the widget on state changes only, never on a timer.",
            "Test each surface on the device and record screenshots as evidence.",
        ],
        accept=[
            "The tile reflects the real service state within a second of a change",
            "A shared text or image gets an answer without opening the app",
            "The widget produces no periodic wakeups (verified with battery stats over an hour)",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "adb shell dumpsys batterystats --charged com.droidroute.app | head -20",
        ],
        state="DroidRoute behaves like a phone app, not a service you visit.",
    ),
    Task(
        id=178,
        slug="mobile-data-accounting",
        title="Mobile-data accounting and budget",
        goal="Measure bytes per provider and per day, warn before the owner's mobile-data budget is exceeded, and enforce it when asked.",
        deps=[155, 176],
        est="90-180 min",
        skills=[
            ("performance-android", "byte accounting per request without buffering payloads"),
            ("droidroute-verification", "budget enforcement at the boundary plus a metered-vs-unmetered test"),
        ],
        deliverables=[
            "Per-request byte accounting split by upload/download, tagged with the network type",
            "A monthly mobile-data budget with warn-once and a hard stop when configured",
        ],
        steps=[
            "Count bytes at the transport layer, not by measuring computed strings.",
            "Attribute usage to provider and network type so unmetered traffic does not consume the budget.",
            "Warn at the configured threshold once, then stop only if the policy says so.",
            "Expose usage in the dashboard and in `/v1/usage`.",
        ],
        accept=[
            "Mobile-data usage is counted per provider and network type (asserted against a fixture)",
            "Wi-Fi traffic does not consume the mobile budget (asserted)",
            "The hard stop returns a policy error naming the budget and its reset",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*DataBudget*'",
        ],
        state="The owner can see and cap what the gateway costs in mobile data, not only in tokens.",
    ),
    Task(
        id=179,
        slug="offline-model-catalog",
        title="Offline model catalog pack",
        goal=(
            "An own catalog that works with no internet: sizes, quants, licences, checksums, device-fit scores, and an optional "
            "signed update — so the owner can pick a model that fits this phone without visiting a website."
        ),
        deps=[110, 111],
        est="150-300 min",
        skills=[
            ("local-inference", "accurate metadata per model family and realistic expectations on 8 GB"),
            ("droidroute-verification", "hash verification, tampered-pack rejection and the no-network path"),
        ],
        deliverables=[
            "`assets/catalog/models.json` bundled and fully offline-usable",
            "A signed optional update pack with checksum verification and rollback to the bundled copy",
        ],
        steps=[
            "Define the catalog schema: id, family, parameters, quant, file size, context, licence, source URL, SHA-256.",
            "Score each entry against this device's available RAM at read time, not at authoring time.",
            "Verify a downloaded update pack against an embedded public key before accepting it.",
            "Keep the bundled copy authoritative when no update is present or verification fails.",
        ],
        accept=[
            "The catalog is fully usable in airplane mode (verified with the radio off)",
            "A tampered update pack is rejected and the bundled catalog stays in force (asserted)",
            "Every entry names a licence and a checksum",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ModelCatalogPack*'",
        ],
        state="Choosing a local model is a browsing experience that works offline and cannot be poisoned.",
    ),
    Task(
        id=180,
        slug="in-app-updater",
        title="In-app updater with signature verification and rollback",
        goal=(
            "Always update-ready: check GitHub releases for a newer build, verify the APK signature against the expected signer, "
            "install through the system installer, and keep the previous build for rollback."
        ),
        deps=[144, 9],
        est="120-240 min",
        skills=[
            ("android-platform", "package installer intents, version comparison and signature checking"),
            ("android-intent-security", "an updater is a remote-code path: signature verification is non-negotiable"),
        ],
        deliverables=[
            "`update/UpdateChecker.kt` with channel selection (stable / pre-release), version comparison and release notes",
            "Signature verification against the pinned signing certificate, plus a rollback path to the kept previous APK",
        ],
        steps=[
            "Compare `versionCode` from the release metadata, never from a string comparison of tag names.",
            "Verify the downloaded APK's signing certificate matches the pinned one before offering the install.",
            "Show release notes and require an explicit install action; never install silently.",
            "Keep the previous APK and offer a one-tap rollback with a warning about data compatibility.",
        ],
        accept=[
            "A newer release is detected and its signature verified before install (asserted with a fixture and a real run)",
            "A wrong-signature APK is refused with a clear message and never offered for install",
            "Rollback installs the kept previous build",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*UpdateChecker*'",
            "gh release list --limit 3",
        ],
        state="The app updates itself from its own releases, with the integrity check that makes that safe.",
    ),
    Task(
        id=181,
        slug="signed-catalog-updates",
        title="Catalog updates without an app release",
        goal=(
            "Provider knowledge and model lists change weekly — update them between releases with signed packs, verified against "
            "an embedded key, with the bundled copy as the offline fallback."
        ),
        deps=[164, 180],
        est="120-240 min",
        skills=[
            ("droidroute-provider-manifest", "which catalog fields are safe to update remotely and which are not"),
            ("droidroute-verification", "tampered pack, stale pack, missing key and offline-fallback tests"),
        ],
        deliverables=[
            "`catalog/` pack format covering provider manifests and model lists, signed by the owner's key",
            "A documented update policy: check interval, offline behaviour, and how a bad pack is rolled back",
        ],
        steps=[
            "Define the pack format and what it may change; never let a pack add executable code or a credential.",
            "Verify signature and freshness before applying; keep the previous state for one-step rollback.",
            "Apply atomically: a partially applied pack must not be possible.",
            "Document, for the owner, exactly how to publish a pack.",
        ],
        accept=[
            "A valid pack updates providers without an app update (demonstrated once)",
            "A tampered or expired pack is rejected and the previous state stays in force (asserted)",
            "A pack can never introduce credentials or code (asserted by schema validation)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*CatalogPack*'",
        ],
        state="The app stays current between releases without becoming a remote-code channel.",
    ),
    Task(
        id=182,
        slug="debug-capture-mode",
        title="Debug capture mode (redacted, time-bounded)",
        goal="A troubleshooting mode that records full request and response payloads — redacted, bounded, auto-expiring — so a broken provider can be diagnosed without guesswork.",
        deps=[17, 104],
        est="90-180 min",
        skills=[
            ("droidroute-verification", "redaction canary on captured payloads and an expiry test"),
            ("android-intent-security", "capture is the most sensitive data the app holds; bound it in time and scope"),
        ],
        deliverables=[
            "`logging/DebugCapture.kt` with a maximum capture window, a byte ceiling and automatic expiry",
            "A capture viewer with export, sharing the redactor with the log pipeline",
        ],
        steps=[
            "Capture only after an explicit enable, with a visible countdown in the notification.",
            "Apply the redactor to every captured field and record the redaction counts per payload.",
            "Enforce a byte ceiling and a time ceiling; delete automatically when either is reached.",
            "Make exported captures pass the secrets preflight before leaving the app.",
        ],
        accept=[
            "Capture is off by default and expires automatically (asserted)",
            "A canary key in a captured payload is redacted (asserted)",
            "An exported capture passes `scripts/preflight-secrets.sh`",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*DebugCapture*'",
        ],
        state="Diagnosing a misbehaving provider does not require guessing or leaking credentials.",
    ),
    Task(
        id=183,
        slug="qr-config-portability",
        title="Config portability by QR code (no cloud)",
        goal="Move a full configuration to a new phone by scanning a QR code, with secrets encrypted under a passphrase — no account, no cloud, no copy of the keys anywhere else.",
        deps=[34, 6],
        est="120-240 min",
        skills=[
            ("android-intent-security", "the export is the highest-value artefact in the app; treat its encryption as the feature"),
            ("droidroute-verification", "wrong-passphrase, tampered-bundle, oversized-bundle and round-trip tests"),
        ],
        deliverables=[
            "`transfer/QrBundle.kt` — encrypted bundle, chunked into scannable QR frames",
            "An import flow that verifies the bundle before applying and never partially applies it",
        ],
        steps=[
            "Encrypt the bundle with a key derived from a passphrase using a documented KDF and parameters.",
            "Chunk the ciphertext into QR frames with an index and a checksum; the scanning phone reassembles and verifies.",
            "Apply atomically and refuse a bundle whose checksum or version does not match.",
            "Document what the bundle contains and what it deliberately excludes.",
        ],
        accept=[
            "A full configuration transfers between two app instances via QR (demonstrated once)",
            "A wrong passphrase and a tampered frame both fail cleanly without partial application (asserted)",
            "No cloud service or account is involved (verified by inspecting the network calls during transfer)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*QrBundle*'",
        ],
        state="Device migration is local, encrypted and account-free — unlike the cloud sync competitors offer.",
    ),
    Task(
        id=184,
        slug="native-benchmark",
        title="Native-versus-service benchmark on this device",
        goal=(
            "Measure the claim that a native Android gateway beats running a Node-based router on the same phone: memory, idle "
            "battery, cold start and request overhead — with numbers, or with an honest retraction."
        ),
        deps=[136, 180],
        est="150-300 min",
        skills=[
            ("performance-android", "a fair measurement protocol: same workload, same device state, multiple runs"),
            ("technical-writing", "publish the method and the numbers, including where the native approach loses"),
        ],
        deliverables=[
            "A benchmark protocol and results table in `docs/14-benchmark.md`",
            "A recorded comparison against a Node-based router on the A56, or a documented reason the comparison could not be run",
        ],
        steps=[
            "Define the workload: idle with one connected agent, a fixed prompt sequence, a cold start.",
            "Measure the same workload on both implementations on the same device, with the same thermal starting point.",
            "Report median and spread, not a best-case single run.",
            "If the native version does not win on a metric, say so — a retracted claim beats a false one.",
        ],
        accept=[
            "The protocol is written so a third party could repeat it",
            "Numbers are reported with spread, not as single values",
            "Any metric where the native approach loses is stated explicitly",
        ],
        verify=[
            "adb shell dumpsys meminfo com.droidroute.app | head -20",
            "adb shell dumpsys batterystats --charged com.droidroute.app | head -20",
        ],
        state="The core claim of this project is either backed by numbers or corrected in public.",
    ),
]
