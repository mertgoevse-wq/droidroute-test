"""Phase 01 — Core server: a Ktor server inside a foreground service, safely bound and properly gated."""

from common import Phase, Task

PHASE = Phase(
    number=1,
    slug="core-server",
    title="Core server",
    summary="Embedded Ktor server, lifecycle, configurable port, bind modes, auth gate, request logging.",
)

TASKS = [
    Task(
        id=11,
        slug="ktor-server-bootstrap",
        title="Ktor server bootstrap",
        goal=(
            "Mount an embedded Ktor CIO server: start, stop, and answer a minimal `/health` with version, "
            "uptime, port and bind mode. No provider or protocol logic yet."
        ),
        deps=[7, 3],
        est="45-90 min",
        skills=[
            ("ktor-server", "CIO engine, plugin installation, graceful shutdown"),
            ("testing", "start/stop lifecycle test and a health route test"),
        ],
        deliverables=[
            "`server/HttpServer.kt` — start/stop taking a `Port` and `BindMode`",
            "`server/routes/HealthRoutes.kt` returning version, uptime, bind mode, port",
            "Test asserting the listening socket is released on stop",
        ],
        steps=[
            "Create the CIO application with the JSON and status-pages plugins installed.",
            "Bind according to `BindMode`; raise a typed error when binding fails instead of swallowing it.",
            "Implement graceful shutdown that drains in-flight requests for a bounded time.",
            "Expose start/stop so the service and the UI can drive it.",
        ],
        accept=[
            "`curl -fsS http://127.0.0.1:<port>/health` returns 200 with version, uptime, port, bind mode",
            "After stop, the port is free immediately (a second bind succeeds within a second)",
            "`./gradlew :app:dependencies` shows no Netty — CIO only",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*HttpServer*'",
            "curl -fsS http://127.0.0.1:8787/health",
        ],
        state="A real HTTP server runs on the device and can be started and stopped programmatically.",
    ),
    Task(
        id=12,
        slug="service-server-wiring",
        title="Service ↔ server wiring and lifecycle states",
        goal=(
            "Connect the foreground service to the server so a single source of truth exists for "
            "'running', 'starting', 'stopping', 'failed', including the notification text."
        ),
        deps=[11, 7],
        est="45-90 min",
        skills=[
            ("android-platform", "service state machine, notification updates from a StateFlow"),
            ("kotlin-core", "coroutine scopes, cancellation on stop, no leaking collectors"),
        ],
        deliverables=[
            "`server/ServerController.kt` owning the state machine and the server instance",
            "Notification that reflects real state (port, bind mode, request counter, last error)",
        ],
        steps=[
            "Model the state as a sealed type: Starting, Running, Stopping, Stopped, Failed(reason).",
            "Drive start/stop from the service's onStartCommand and its stop action; cancel the scope on stop.",
            "Update the notification from the state flow, rate-limited so it is not redrawn per request.",
            "Surface a failure reason in the notification text instead of a generic error.",
        ],
        accept=[
            "Toggling start/stop repeatedly leaves exactly one server instance running",
            "A deliberate bind failure (port already in use) produces state `Failed` with a readable reason",
            "The notification text matches `/health` while running",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ServerController*'",
            "adb shell dumpsys notification --noredact | grep -A3 droidroute",
        ],
        state="The service owns the server lifecycle; everything else observes one state machine.",
    ),
    Task(
        id=13,
        slug="port-configuration",
        title="Configurable port with collision handling",
        goal="Make the port owner-editable (default 8787), validate it, and offer the next free port when the chosen one is taken.",
        deps=[12, 5],
        est="40-80 min",
        skills=[
            ("android-platform", "acceptable-port-range validation and a real bind probe"),
            ("testing", "validation table tests plus a collision case"),
        ],
        deliverables=[
            "`server/PortAllocator.kt` — validation (1024–65535) and next-free-port search",
            "DataStore-backed port setting with validation errors surfaced to the UI",
        ],
        steps=[
            "Validate the range and reject privileged and reserved ports with specific messages.",
            "Probe by binding and immediately releasing; never by guessing from a static list.",
            "Offer the next free port when the chosen one is busy, but never change the setting without consent.",
            "Update `scripts/termux-setup.sh` guidance shown in the UI when the port changes.",
        ],
        accept=[
            "Setting 80 or 70000 is rejected with a message naming the valid range",
            "With a busy port the app suggests the next free one and the suggestion actually binds",
            "The persisted port survives a process restart",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*PortAllocator*'",
            "grep -n '8787' app/src/main/kotlin/com/droidroute/store/SettingsStore.kt",
        ],
        state="The default port is 8787, owner-editable, validated, and collision-safe.",
    ),
    Task(
        id=14,
        slug="bind-modes-and-auth-floor",
        title="Bind modes and the enforced auth floor",
        goal=(
            "Implement the three bind modes from docs/05-security.md and enforce, in code, that a "
            "non-local bind can never run without an API key."
        ),
        deps=[13],
        est="45-90 min",
        skills=[
            ("security-audit", "attack the floor: prove no code path reaches a LAN bind with auth=none"),
            ("testing", "unit tests for every (bind mode × auth mode) combination"),
        ],
        deliverables=[
            "`server/BindPolicy.kt` — the matrix and the refusal path",
            "Refusal recorded through the app logger with a clear reason",
        ],
        steps=[
            "Encode the matrix: local allows none/api_key/oauth; lan and external require api_key or oauth.",
            "Refuse at start time, not at request time, and report the refusal in the notification and the UI.",
            "Require the explicit confirmation for external mode (checkbox in the UI, persisted as consent).",
            "Write the matrix tests so a future refactor cannot lower the floor silently.",
        ],
        accept=[
            "Every (bind mode × auth mode) pair behaves as documented, asserted by tests",
            "An attempt to run LAN + none fails to start and logs the refusal",
            "External mode without recorded consent does not start",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*BindPolicy*'",
        ],
        state="The app cannot be tricked into exposing an unauthenticated port.",
    ),
    Task(
        id=15,
        slug="auth-gate-middleware",
        title="Auth gate middleware",
        goal=(
            "Install one middleware that enforces the configured auth mode for every route: no header, "
            "api-key bearer, or OAuth-issued short-lived token."
        ),
        deps=[14],
        est="45-90 min",
        skills=[
            ("ktor-server", "route interceptor, timing-safe comparison, 401 shape per protocol surface"),
            ("security-audit", "constant-time comparison and no key material in error bodies"),
        ],
        deliverables=[
            "`server/AuthGate.kt` — accepts `Authorization: Bearer` and `x-api-key`",
            "401 responses shaped per calling surface (OpenAI, Anthropic, Gemini)",
        ],
        steps=[
            "Hash incoming keys with the stored salt and compare in constant time.",
            "Exempt nothing except `/health` in local mode; in any non-local mode exempt nothing at all.",
            "Shape the 401 body for the surface that was called so clients parse it correctly.",
            "Never echo the presented key or its prefix in the response or the log.",
        ],
        accept=[
            "With api-key mode, a request without or with a wrong key gets a 401 in the correct dialect",
            "A correct key is accepted within 5 ms overhead (measured in a test)",
            "No response body or log line contains any part of the presented key",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*AuthGate*'",
        ],
        state="Every route is behind one gate with one policy source.",
    ),
    Task(
        id=16,
        slug="client-api-keys",
        title="Client API key generation, hashing and revocation",
        goal="Let the owner mint named client keys (`dr_…`), stored hashed, individually revocable, with last-used tracking.",
        deps=[15, 6],
        est="50-100 min",
        skills=[
            ("security-audit", "salted hashing, one-time display, no plaintext retention"),
            ("persistence-room", "Room entity + DAO for client keys and their usage timestamps"),
        ],
        deliverables=[
            "`store/ClientKeyEntity.kt` + DAO (name, salt, hash, created, lastUsed, revoked)",
            "`server/ClientKeyService.kt` — mint (returns plaintext once), verify, revoke, list",
        ],
        steps=[
            "Generate `dr_` + 32 random characters using a cryptographically secure source.",
            "Store salt + SHA-256 hash only; return the plaintext exactly once from the mint call.",
            "Update `lastUsed` at most once per minute per key to avoid write amplification.",
            "Revocation takes effect immediately for new requests and is logged with the key name, never the value.",
        ],
        accept=[
            "The plaintext key is returned once and is unrecoverable afterwards",
            "A revoked key is rejected while other keys keep working",
            "`lastUsed` updates are visible in the UI within a minute of use",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ClientKey*'",
        ],
        state="Client authentication is per-machine and per-agent, revocable without restarting the server.",
    ),
    Task(
        id=17,
        slug="request-logging-middleware",
        title="Request logging, request ids and redaction",
        goal=(
            "Log every request with a `request_id`, latency, result and provider attempts, through the "
            "shared redactor, and return the id in `x-droidroute-request-id`."
        ),
        deps=[15, 8],
        est="45-90 min",
        skills=[
            ("ktor-server", "call interception, id propagation into the routing context"),
            ("testing", "canary test: a key sent as a header must not appear in any log line"),
        ],
        deliverables=[
            "`server/RequestIdPlugin.kt` + `logging/RequestLog.kt`",
            "Log record schema documented in handbooks/05-logging-standard.md (extended with `request_id`)",
        ],
        steps=[
            "Generate the id at the gate, attach it to the call attributes and to every subsequent log record.",
            "Log the outcome once per request (not per byte) with status, latency and attempt count.",
            "Apply the redactor to headers and body excerpts before logging them.",
            "Add the canary test that sends an `x-api-key` header and greps the log output for it.",
        ],
        accept=[
            "Every response carries `x-droidroute-request-id` matching a log record",
            "A request with a key header leaves no trace of the key in the logs",
            "Logging adds under 5 ms to a request (measured)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*RequestLog*'",
        ],
        state="Every request is traceable end to end without leaking a credential.",
    ),
    Task(
        id=18,
        slug="config-persistence-rehydration",
        title="Configuration persistence and post-mortem rehydration",
        goal="After a process kill, the server restarts with the same port, bind mode, auth mode and enabled providers, and says so in a start record.",
        deps=[12, 5, 6],
        est="40-80 min",
        skills=[
            ("persistence-room", "read-on-start transaction, consistent snapshot"),
            ("android-platform", "process-death detection and restart policy"),
        ],
        deliverables=[
            "`server/StartupSnapshot.kt` — reads settings, providers and keys before binding",
            "Startup log record stating what was restored and what failed to restore",
        ],
        steps=[
            "Read the whole configuration before binding the socket so the first request already has a full context.",
            "Handle partially corrupt state (unknown provider id, missing key) by disabling that entry and logging it.",
            "Record a start line in the log with port, bind mode, auth mode and provider count.",
            "Test by force-killing the process and restarting the service.",
        ],
        accept=[
            "After `am force-stop` and restart, the same port and enabled providers are active",
            "A deliberately corrupted provider row is disabled with a logged reason, and the server still starts",
            "The startup record exists in the app log",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*StartupSnapshot*'",
            "adb shell am force-stop com.droidroute.app",
        ],
        state="The server is crash-tolerant: a kill changes nothing the owner has to re-enter.",
    ),
    Task(
        id=19,
        slug="graceful-rebind",
        title="Graceful rebind on configuration change",
        goal="Changing port or bind mode while running performs a drain → rebind → resume instead of a hard restart.",
        deps=[18, 13],
        est="40-80 min",
        skills=[
            ("ktor-server", "drain semantics, readiness flag, minimal client-visible gap"),
            ("testing", "test that an in-flight request completes across a rebind"),
        ],
        deliverables=[
            "`server/Rebind.kt` implementing the drain/rebind/resume sequence",
            "Readiness flag reflected in `/health` during the gap",
        ],
        steps=[
            "Stop accepting new connections, let in-flight requests finish within a bounded window.",
            "Release the old socket, bind the new configuration, flip readiness back on.",
            "If the new bind fails, return to the previous working configuration and report the failure.",
            "Log one record per rebind with old and new configuration.",
        ],
        accept=[
            "An in-flight request completes successfully across a rebind",
            "A failing rebind rolls back to the previous configuration, still serving",
            "The rebind is logged with both configurations",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Rebind*'",
        ],
        state="Port and bind-mode changes are safe to make while agents are connected.",
    ),
    Task(
        id=20,
        slug="autostart-and-doze",
        title="Optional autostart and doze resilience",
        goal="Offer opt-in start-on-boot, and keep the server responsive under doze without draining the battery.",
        deps=[18],
        est="45-90 min",
        skills=[
            ("android-platform", "BOOT_COMPLETED receiver, doze behaviour, wake-lock discipline"),
            ("performance-android", "measure idle battery cost and set a bounded expectation"),
        ],
        deliverables=[
            "`server/BootReceiver.kt` gated by an explicit owner setting (default off)",
            "Documented idle behaviour: what sleeps, what stays responsive, measured drain",
        ],
        steps=[
            "Register the boot receiver and respect the setting: never autostart without opt-in.",
            "Ensure long SSE streams survive doze by using heartbeats rather than wake locks.",
            "Measure: battery percentage delta per hour with one connected agent and no traffic.",
            "Record the measurement in the component status file.",
        ],
        accept=[
            "With autostart on, the server runs after a reboot without opening the UI",
            "With autostart off, nothing starts after a reboot",
            "Idle drain is measured and recorded with a number, not an adjective",
        ],
        verify=[
            "adb shell dumpsys batterystats --charged com.droidroute.app | head -30",
            "./gradlew :app:testDebugUnitTest --tests '*BootReceiver*'",
        ],
        state="Background behaviour is the owner's choice and its cost is documented with real numbers.",
    ),
    Task(
        id=21,
        slug="connection-helper",
        title="Connection helper (URLs, snippets, QR)",
        goal="Show the owner exactly what to paste into Claude Code and Freebuff, for the current port and auth mode, including a QR code for a LAN client.",
        deps=[13, 16],
        est="40-80 min",
        skills=[
            ("android-compose-ui", "screen with copy-to-clipboard actions and a QR rendering"),
            ("technical-writing", "snippets that are correct for each auth mode"),
        ],
        deliverables=[
            "`ui/connections/ConnectionHelperScreen.kt`",
            "Copyable snippets: env exports, `curl` health check, MCP client config",
        ],
        steps=[
            "Render the values from the live configuration, never from constants.",
            "Include the auth header in the snippet only when auth is not `none`.",
            "Provide a QR code for the LAN URL when the bind mode allows it.",
            "Add a 'run this to verify' one-liner whose output the owner can paste back.",
        ],
        accept=[
            "Snippets match the running configuration (verified by changing the port and re-reading the screen)",
            "Every snippet copies to the clipboard with one tap",
            "The verification one-liner actually succeeds against the running server",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "curl -fsS http://127.0.0.1:8787/health",
        ],
        state="Connecting an agent is a copy-paste operation with no guessing.",
    ),
    Task(
        id=22,
        slug="admin-endpoints",
        title="Admin endpoints and reload path",
        goal="Provide `/v1/providers` and `/admin/reload` so tooling (and the owner) can inspect and refresh configuration without restarting the app.",
        deps=[17, 18],
        est="30-60 min",
        skills=[
            ("ktor-server", "route design, key-protected admin surface"),
            ("security-audit", "admin routes must never expose key material or bypass the gate"),
        ],
        deliverables=[
            "`server/routes/AdminRoutes.kt` — `/v1/providers`, `/admin/reload`, `/v1/usage` skeleton",
            "Admin routes require api-key auth in every bind mode",
        ],
        steps=[
            "Serve the provider registry without secrets (id, name, tier, enabled, status).",
            "Implement reload: re-read manifests and settings, keep the socket open.",
            "Require api-key auth for admin routes even in local mode.",
            "Return a structured result naming what changed.",
        ],
        accept=[
            "`/v1/providers` lists providers with no key material present",
            "`/admin/reload` picks up a manifest change without a restart",
            "Admin routes reject an unauthenticated request in every bind mode",
        ],
        verify=[
            "curl -fsS http://127.0.0.1:8787/v1/providers",
            "./gradlew :app:testDebugUnitTest --tests '*AdminRoutes*'",
        ],
        state="Configuration is inspectable and reloadable at runtime, under auth, with no secret exposure.",
    ),
    Task(
        id=23,
        slug="core-server-test-suite",
        title="Core server test suite and service lifecycle evidence",
        goal="Consolidate the phase's tests into one suite and prove the service lifecycle on-device with recorded evidence.",
        deps=[11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
        est="60-120 min",
        skills=[
            ("testing", "fill coverage gaps, remove duplication, keep the suite fast"),
            ("android-platform", "instrumented service lifecycle test with an evidence capture"),
        ],
        deliverables=[
            "`app/src/test/…/server/` suite covering gate, policy, port, rebind, keys, logging",
            "`app/src/androidTest/…/ServiceLifecycleTest.kt` with a recorded evidence snippet",
        ],
        steps=[
            "Run the whole suite and close the gaps the phase's tasks left open.",
            "Add the instrumented test that starts the service, hits `/health`, stops it, and asserts the port is free.",
            "Store the evidence output under `logs/` as part of the task log.",
            "Remove any test that asserts nothing meaningful.",
        ],
        accept=[
            "`./gradlew testDebugUnitTest` passes with the new suite",
            "The instrumented test passes on the device or an emulator, with output recorded",
            "No test depends on network access or the owner's credentials",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest",
            "./gradlew :app:connectedDebugAndroidTest",
        ],
        state="Phase 1 is provable: the server, its gate, its policy and its lifecycle all have evidence.",
    ),
]
