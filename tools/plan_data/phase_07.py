"""Phase 07 — UI: a router that is configurable in a minute without hiding what it is doing."""

from common import Phase, Task

PHASE = Phase(
    number=7,
    slug="ui",
    title="UI",
    summary="Compose shell, dashboard, provider and key management, routing controls, settings, onboarding.",
)

TASKS = [
    Task(
        id=91,
        slug="app-shell-navigation",
        title="App shell and navigation",
        goal="Create the Material 3 shell with bottom navigation across Dashboard, Providers, Routing, Local, Settings, and a service-state banner shown everywhere.",
        deps=[7, 12],
        est="60-120 min",
        skills=[
            ("android-compose-ui", "navigation host, scaffold, state hoisting"),
            ("performance-android", "keep the state banner from recomposing the whole tree per request"),
        ],
        deliverables=[
            "`ui/DroidRouteApp.kt` with the navigation graph and five destinations",
            "A persistent service-state banner (running, failed with reason, stopped)",
        ],
        steps=[
            "Build the scaffold with bottom navigation and per-destination view models.",
            "Show the server state as a banner, tappable to start/stop.",
            "Keep every screen reachable in one tap from the shell — no nested menus.",
            "Add a Compose preview for each destination.",
        ],
        accept=[
            "Every destination is reachable and keeps its own scroll/state",
            "The banner shows the real service state, including a failure reason",
            "Screens render in previews",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "./gradlew :app:lintDebug",
        ],
        state="The navigation skeleton exists and later screens plug into it.",
    ),
    Task(
        id=92,
        slug="theme-and-visuals",
        title="Theme, dark/light and typography",
        goal="A coherent Material 3 theme with dynamic colour, proper dark mode, and a typographic scale that stays readable on a phone.",
        deps=[91],
        est="40-80 min",
        skills=[
            ("android-compose-ui", "colour scheme, dynamic colour, typography scale"),
            ("performance-android", "no overdraw, no recomposition from theme objects"),
        ],
        deliverables=[
            "`ui/theme/` with light, dark and dynamic variants",
            "Status colours for provider health that are distinguishable in both modes",
        ],
        steps=[
            "Define light/dark schemes and enable dynamic colour on Android 12+ with a static fallback.",
            "Give health states a colour plus a shape or label, so colour is never the only signal.",
            "Verify contrast ratios for text on both schemes.",
            "Document the palette in the design note inside the theme package.",
        ],
        accept=[
            "Both modes render every screen without unreadable text",
            "Health states are distinguishable without relying on colour alone",
            "Text contrast meets the documented ratio",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
        ],
        state="The app looks intentional in both modes and stays legible.",
    ),
    Task(
        id=93,
        slug="localisation-de-en",
        title="Localisation: German default, English available",
        goal="Ship both languages through Android resources, with German as the default and no hard-coded user-facing strings.",
        deps=[91],
        est="50-100 min",
        skills=[
            ("android-compose-ui", "string resources, plural handling, per-locale formatting"),
            ("technical-writing", "German copy that is plain and correct, not machine-literal"),
        ],
        deliverables=[
            "`values/strings.xml` (German default) and `values-en/strings.xml`",
            "A lint rule or check that fails on hard-coded user-facing text",
        ],
        steps=[
            "Extract every user-facing string; no literals in composables.",
            "Write the German copy first as the default resource set, then the English translations.",
            "Use plurals and locale-aware formatting for counts, numbers and timestamps.",
            "Add the check so future work cannot bypass localisation.",
        ],
        accept=[
            "Switching the device language switches the UI",
            "No user-facing string literal remains in a composable (checked)",
            "German copy reads naturally to a native speaker, with technical terms kept as they are",
        ],
        verify=[
            "./gradlew :app:lintDebug",
            "grep -rn 'Text(\"' app/src/main/kotlin/com/droidroute/ui | head",
        ],
        state="The owner reads German by default and English is one setting away.",
    ),
    Task(
        id=94,
        slug="dashboard-screen",
        title="Dashboard screen",
        goal="Show the state of the whole system at a glance: server, bind mode, connected clients, per-provider tokens, errors, latency.",
        deps=[92, 32, 89],
        est="80-150 min",
        skills=[
            ("android-compose-ui", "dense but readable layout, honest empty states"),
            ("performance-android", "refresh cadence that does not drain the battery in the foreground"),
        ],
        deliverables=[
            "`ui/dashboard/DashboardScreen.kt` with live sections and pull-to-refresh",
            "Empty state that says what to do first (connect a provider)",
        ],
        steps=[
            "Render server state, port, bind mode and current client keys in use.",
            "Render per-provider tokens today, error count and p50/p95 latency from `/v1/usage`.",
            "Show parked keys with their reset times so a quiet provider is explainable.",
            "Poll at a sane interval (e.g. 5 s in the foreground, paused in the background).",
        ],
        accept=[
            "Numbers on the dashboard match `/v1/usage` for the same window",
            "A parked key is visible with its reset time",
            "The empty state names the next action instead of showing zeros",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "curl -fsS http://127.0.0.1:8787/v1/usage",
        ],
        state="The owner can see what the gateway is doing without reading logs.",
    ),
    Task(
        id=95,
        slug="usage-charts",
        title="Daily and weekly usage views",
        goal="Show token consumption and estimated cost per provider for today and the last seven days.",
        deps=[94, 81],
        est="60-120 min",
        skills=[
            ("android-compose-ui", "simple, readable charts without a heavy charting dependency"),
            ("kotlin-core", "aggregation queries and caching that stay cheap on a phone"),
        ],
        deliverables=[
            "`ui/dashboard/UsageSection.kt` with a 7-day view and a per-provider breakdown",
            "Cost shown as estimated, explicitly labelled when prices are unknown",
        ],
        steps=[
            "Aggregate from the usage table with a bounded query (indexed by timestamp).",
            "Show free providers with an explicit '0 (free)' rather than hiding them.",
            "Mark estimates as estimates; never present a guess as a measurement.",
            "Add a test comparing the aggregate with a hand-computed fixture.",
        ],
        accept=[
            "The aggregate matches a fixture dataset exactly",
            "Unknown pricing is labelled, not filled with a fabricated number",
            "The query stays under 50 ms for a month of records (measured)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*UsageAggregat*'",
        ],
        state="Consumption is visible per provider and day, with costs labelled honestly.",
    ),
    Task(
        id=96,
        slug="providers-list",
        title="Providers list, filters and one-click connect",
        goal="List every provider with its state and give free providers a one-tap connect flow that validates before enabling.",
        deps=[25, 31, 33],
        est="80-150 min",
        skills=[
            ("android-compose-ui", "list rendering with filters, search and clear per-row state"),
            ("provider-integration", "the one-click sequence: open key page, return, validate, enable"),
        ],
        deliverables=[
            "`ui/providers/ProvidersScreen.kt` with tier/tag filters and search",
            "One-click connect flow for providers tagged `one-click`",
        ],
        steps=[
            "Show per row: name, tier, state (enabled, needs-key, parked, breaker open), model count.",
            "Implement connect: open the key page, accept the returned key, validate, then enable on success.",
            "Never enable a provider whose validation failed; show the reason instead.",
            "Add the custom-provider entry point at the top of the list.",
        ],
        accept=[
            "A failing validation leaves the provider disabled with the reason visible",
            "Filters and search work across tier and tags",
            "A successful one-click connect results in a working provider in one flow",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
        ],
        state="Connecting a free provider takes one flow instead of a research session.",
    ),
    Task(
        id=97,
        slug="provider-detail",
        title="Provider detail screen",
        goal="Everything about one provider in one place: models, keys, quota windows, health numbers, event history.",
        deps=[96, 32, 82],
        est="60-120 min",
        skills=[
            ("android-compose-ui", "information density with a clear hierarchy"),
            ("llm-routing", "present quota and health numbers in a way that explains routing decisions"),
        ],
        deliverables=[
            "`ui/providers/ProviderDetailScreen.kt`",
            "Actions: refresh models, validate keys, disable provider, delete custom provider",
        ],
        steps=[
            "Show the model list with capability tags (tools, vision, embeddings, free).",
            "Show keys masked, with status and last-used timestamps.",
            "Show quota state per key including whether the window is known or estimated.",
            "Link to the explain view filtered to this provider.",
        ],
        accept=[
            "All displayed values are live, not cached placeholders",
            "A disabled provider's detail screen explains why it is disabled",
            "Destructive actions require confirmation",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
        ],
        state="Any provider question is answerable from one screen.",
    ),
    Task(
        id=98,
        slug="custom-provider-form",
        title="Custom provider form with discovery",
        goal="Add an arbitrary OpenAI- or Anthropic-compatible endpoint through a form that validates as it goes.",
        deps=[33, 96],
        est="60-120 min",
        skills=[
            ("android-compose-ui", "form state, inline validation, keyboard types"),
            ("security-audit", "the key field must behave like a secret from the first keystroke"),
        ],
        deliverables=[
            "`ui/providers/CustomProviderForm.kt`",
            "Inline validation for URL, compat type and model list",
        ],
        steps=[
            "Validate the URL shape live and reject non-loopback plaintext http immediately.",
            "Offer a discover-models action that reports what it found or why it failed.",
            "Keep the key field masked with an explicit reveal, and clear it from memory on cancel.",
            "On save, run validation and report the result without closing the screen on failure.",
        ],
        accept=[
            "A provider added through the form answers a request",
            "Validation failures are shown inline and distinct from network errors",
            "The key field is masked by default and never logged",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
        ],
        state="Custom providers are a form-filling exercise, not a config-file edit.",
    ),
    Task(
        id=99,
        slug="keys-screen",
        title="Keys screen: masking, one-time reveal, clipboard",
        goal="Implement the key handling UX exactly as documented: masked by default, revealed once, device-credential protected on repeat reveal, clipboard auto-clear.",
        deps=[6, 16, 96],
        est="60-120 min",
        skills=[
            ("android-compose-ui", "the interaction details that make masking trustworthy"),
            ("security-audit", "FLAG_SECURE, clipboard timer, no key in a toast or snackbar"),
        ],
        deliverables=[
            "`ui/keys/KeysScreen.kt` with add, validate, mask, reveal, revoke",
            "Screenshot protection on this screen only",
        ],
        steps=[
            "Show `first5••••last5` and nothing more until an explicit reveal.",
            "Require device-credential confirmation for a second reveal and log the action (not the value).",
            "Copy to clipboard with a visible 60-second countdown and an immediate clear action.",
            "Never place a key in a notification, a snackbar, or an intent extra.",
        ],
        accept=[
            "The masked form is the default on every entry to the screen",
            "A repeated reveal requires the device credential",
            "The clipboard is cleared after 60 seconds without requiring the app to stay open",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
        ],
        state="Key handling is safe to demonstrate to someone looking over your shoulder.",
    ),
    Task(
        id=100,
        slug="routing-screen",
        title="Routing screen: strategies, aliases, key chains",
        goal="Let the owner control routing: pick a strategy (globally or per model), define aliases, and build multi-provider key chains.",
        deps=[80, 83, 84],
        est="90-180 min",
        skills=[
            ("android-compose-ui", "an editor for a nested structure without a wall of inputs"),
            ("llm-routing", "prevent configurations that cannot work (cycles, disabled providers, empty chains)"),
        ],
        deliverables=[
            "`ui/routing/RoutingScreen.kt` with strategy picker, alias editor and chain builder",
            "Validation feedback for impossible configurations",
        ],
        steps=[
            "Offer the eight strategies with a one-line explanation of each and a composed default.",
            "Build an alias editor with candidate reordering and per-alias strategy override.",
            "Build the key-chain editor: add links from any provider, reorder, label the chain.",
            "Reject invalid configurations inline before saving.",
        ],
        accept=[
            "A change to the strategy takes effect without restarting the server",
            "An alias and a chain can each be created, saved and used from a client",
            "Invalid configurations are blocked with a reason",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "curl -fsS 'http://127.0.0.1:8787/v1/routing/explain?model=my-best'",
        ],
        state="The owner's headline routing requirement is fully controllable from the phone.",
    ),
    Task(
        id=101,
        slug="routing-explain-viewer",
        title="Routing explain viewer",
        goal="Surface `/v1/routing/explain` in the UI so a surprise routing decision can be understood in seconds.",
        deps=[89, 100],
        est="40-80 min",
        skills=[
            ("android-compose-ui", "present a candidate list with skip reasons compactly"),
            ("technical-writing", "reason labels that are precise, not vague ('parked until 00:00', not 'unavailable')"),
        ],
        deliverables=[
            "`ui/routing/ExplainSheet.kt` reachable from the dashboard and provider detail",
            "Reason vocabulary shared with the backend, not re-invented in the UI",
        ],
        steps=[
            "Render the ordered candidate list with the reason each skipped candidate was skipped.",
            "Show the strategy chain that produced the order.",
            "Let the owner re-run the explanation after a change without leaving the screen.",
        ],
        accept=[
            "Reasons match the API's reason strings exactly",
            "Skipped candidates are visually distinct from usable ones",
            "Refreshing the explanation reflects a just-made configuration change",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
        ],
        state="Routing is explained in the UI, backed by the same data the router used.",
    ),
    Task(
        id=102,
        slug="settings-server-and-keys",
        title="Settings: server, access and client keys",
        goal="Own the server configuration from the app: port, bind mode, auth mode, client keys, and the connection helper.",
        deps=[13, 14, 16, 21],
        est="60-120 min",
        skills=[
            ("android-compose-ui", "settings that show the consequence of a choice before it is applied"),
            ("security-audit", "the auth-floor warning must be unmissable and un-bypassable"),
        ],
        deliverables=[
            "`ui/settings/ServerSettingsScreen.kt`",
            "Client key management (create, name, revoke, last used)",
        ],
        steps=[
            "Change the port with live validation and a clear note that agents must be re-pointed.",
            "Change the bind mode with the auth consequence stated inline; require the explicit consent checkbox for external.",
            "Manage client keys with the plaintext returned exactly once.",
            "Link to the connection helper with values matching the current configuration.",
        ],
        accept=[
            "Port and bind changes apply without a full restart (via the rebind path)",
            "External mode cannot be enabled without the consent checkbox",
            "A new client key is shown once and appears masked afterwards",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
        ],
        state="All server access configuration lives in one place with its consequences stated.",
    ),
    Task(
        id=103,
        slug="settings-integrations",
        title="Settings: tunnel checklists and Termux permission",
        goal=(
            "Give the owner the two access-extension paths: a tunnel checklist for LAN and external use, and the "
            "Termux RUN_COMMAND permission request with an accurate statement of what is and is not available."
        ),
        deps=[91, 21, 14],
        est="60-120 min",
        skills=[
            ("android-platform", "requesting the Termux RUN_COMMAND permission and detecting its absence"),
            ("technical-writing", "tunnel setup steps that match each provider's current documentation"),
        ],
        deliverables=[
            "`ui/settings/IntegrationsScreen.kt`",
            "Tunnel checklists for Tailscale and Cloudflare Tunnel with a live reachability check",
            "Termux availability and permission state, with the degraded path explained",
        ],
        steps=[
            "Detect whether Termux and its permission are available; state the degraded path when they are not.",
            "Show the tunnel checklist with a verification step the owner can run and paste back.",
            "Show the current external URL when a tunnel is detected.",
            "Never enable an external bind as a side effect of enabling a tunnel — keep the two decisions separate.",
        ],
        accept=[
            "The screen states accurately whether Termux and its permission are available",
            "The tunnel checklist ends with a verification that actually proves reachability",
            "Enabling a tunnel does not silently change the bind mode",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
        ],
        state="Integrations are enabled with proof, not with hope.",
    ),
    Task(
        id=104,
        slug="logs-viewer",
        title="Logs viewer with redaction indicator and export",
        goal="Read the gateway's own logs in the app, with a visible assurance that they are redacted, and export them for the repository.",
        deps=[8, 17],
        est="60-120 min",
        skills=[
            ("android-compose-ui", "paging through large logs without loading them all"),
            ("security-audit", "an export must not be a new leak path"),
        ],
        deliverables=[
            "`ui/logs/LogsScreen.kt` with filters (level, provider, task) and export",
            "A redaction badge stating that the redactor ran on every line",
        ],
        steps=[
            "Stream/paginate log reads so a large file does not exhaust memory.",
            "Filter by level, provider id and request id.",
            "Export through the share sheet after re-running the redactor over the content.",
            "Never offer an export that bypasses redaction.",
        ],
        accept=[
            "A large log file can be browsed without an out-of-memory crash",
            "Exported content passes the secrets preflight",
            "Filters work on real records",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "scripts/preflight-secrets.sh",
        ],
        state="Logs are readable on the phone and safe to export.",
    ),
    Task(
        id=105,
        slug="onboarding",
        title="First-run onboarding",
        goal="Take a fresh install to a working endpoint in under five minutes with an honest, short flow.",
        deps=[96, 99, 102],
        est="60-120 min",
        skills=[
            ("android-compose-ui", "a short flow that never lies about what it set up"),
            ("performance-android", "no blocking work on the main thread during setup"),
        ],
        deliverables=[
            "`ui/onboarding/OnboardingFlow.kt`: notification permission → port → connect a free provider → verify",
            "A final verification step that makes a real request and shows the result",
        ],
        steps=[
            "Ask for the notification permission with the reason stated in one sentence.",
            "Default the port to 8787 and explain how to change it later.",
            "Offer one-click connect for a free provider and allow skipping.",
            "End with a real request whose output is shown; never claim success without it.",
        ],
        accept=[
            "A fresh install reaches a verified working endpoint through the flow",
            "Skipping the provider connect leaves the app in a clear, functional state",
            "The final step performs a real call, not a simulated one",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
        ],
        state="A new install is productive in minutes and the app never overstates what it configured.",
    ),
    Task(
        id=106,
        slug="accessibility-adaptive",
        title="Accessibility and adaptive layout pass",
        goal="Make every screen usable with a screen reader, large fonts, one hand, and on a tablet or folded device.",
        deps=[91, 92, 93, 94, 96, 97, 98, 99, 100, 102, 103, 104, 105],
        est="80-150 min",
        skills=[
            ("android-compose-ui", "content descriptions, focus order, adaptive layouts"),
            ("performance-android", "no layout thrash at large font scales"),
        ],
        deliverables=[
            "Content descriptions on every interactive element",
            "Layout bookkeeping in the UI component status file",
        ],
        steps=[
            "Audit each screen with a screen reader; fix missing or misleading descriptions.",
            "Test at 200 % font scale and fix truncation and overlap.",
            "Add tablet-width layouts where a list+detail split is clearly better (providers, logs).",
            "Verify minimum touch target sizes.",
        ],
        accept=[
            "Every interactive element has a meaningful description",
            "No screen breaks at 200 % font scale",
            "Touch targets meet the documented minimum size",
        ],
        verify=[
            "./gradlew :app:lintDebug",
        ],
        state="The UI works for a one-handed user with large fonts and for a screen reader.",
    ),
]
