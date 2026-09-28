"""Phase 09 — MCP, plugins and connectors: discover what exists, then use it instead of rebuilding it."""

from common import Phase, Task

PHASE = Phase(
    number=9,
    slug="mcp-plugins",
    title="MCP & plugins",
    summary="Discover MCP servers from the host environment, aggregate them, and bridge tool calls over the local API.",
)

TASKS = [
    Task(
        id=118,
        slug="mcp-discovery",
        title="MCP configuration discovery",
        goal="Read the MCP configuration of Claude Code, Freebuff/Codex-style tools and Cursor-style projects, tolerating format differences.",
        deps=[107],
        est="90-180 min",
        skills=[
            ("mcp-protocol", "the real configuration shapes of each host tool"),
            ("security-audit", "configuration files contain environment secrets — read names, never values"),
        ],
        deliverables=[
            "`mcp/Discovery.kt` covering the paths listed in docs/07-mcp-plugins.md",
            "A tolerant parser that reports 'unknown format' with the file and line instead of dropping a server",
        ],
        steps=[
            "Read each candidate path through the Termux bridge (or shared storage where accessible).",
            "Parse both JSON and TOML shapes; extract id, transport, command/url, env key names, enabled state.",
            "Never copy an environment value into DroidRoute's storage — names only.",
            "Report per-file results so a missing file is distinguishable from a parse failure.",
        ],
        accept=[
            "Servers from at least two different host formats are discovered",
            "A malformed file produces a specific error naming the file and the reason",
            "No environment value is copied (asserted with a canary value in a fixture)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Discovery*'",
        ],
        state="Existing MCP servers are found from where they already live.",
    ),
    Task(
        id=119,
        slug="mcp-registry",
        title="Aggregated MCP registry with change watching",
        goal="Merge discovered servers into one registry with source precedence, and refresh when a watched file changes.",
        deps=[118, 5],
        est="60-120 min",
        skills=[
            ("mcp-protocol", "precedence rules and id collision handling"),
            ("kotlin-core", "file watching without busy looping or draining battery"),
        ],
        deliverables=[
            "`mcp/Registry.kt` writing `~/.droidroute/mcp.registry.json`",
            "Precedence: bundled defaults < host configs < owner-defined entries",
        ],
        steps=[
            "Merge with deterministic precedence and record the source of every entry.",
            "Watch the configuration files with a debounce so a burst of writes causes one refresh.",
            "Keep owner-defined entries when a host config disappears.",
            "Write the registry atomically so a crash cannot leave a truncated file.",
        ],
        accept=[
            "Owner-defined entries override host entries with the same id",
            "Editing a host configuration refreshes the registry within a few seconds",
            "The registry file is never left partially written (asserted by writing under fault injection)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Registry*'",
        ],
        state="One registry is the single truth about which MCP servers exist.",
    ),
    Task(
        id=120,
        slug="mcp-bridge-api",
        title="MCP bridge API",
        goal="Serve the registry and pass JSON-RPC through: `/mcp/servers`, `/mcp/tools`, `/mcp/{id}`, `/mcp/refresh`.",
        deps=[119, 15, 22],
        est="90-180 min",
        skills=[
            ("mcp-protocol", "JSON-RPC framing, `initialize`, `tools/list`, `tools/call`"),
            ("security-audit", "the bridge must not become an unauthenticated command channel"),
        ],
        deliverables=[
            "`server/routes/McpRoutes.kt`",
            "A flattened tool index at `/mcp/tools` with server attribution",
        ],
        steps=[
            "Implement the four endpoints with the documented shapes.",
            "Require api-key auth for `tools/call`, regardless of bind mode.",
            "Support `?server=` on `/mcp/tools` to filter the index.",
            "Return tool-level errors as MCP errors, not as DroidRoute errors, so clients parse them correctly.",
        ],
        accept=[
            "A `tools/call` reaches a real server and returns its result",
            "`tools/call` without a key is rejected in every bind mode",
            "The tool index attributes every tool to its server",
        ],
        verify=[
            "curl -fsS http://127.0.0.1:8787/mcp/servers",
            "./gradlew :app:testDebugUnitTest --tests '*McpRoutes*'",
        ],
        state="Agents can discover and call every connected MCP tool through one endpoint.",
    ),
    Task(
        id=121,
        slug="mcp-stdio-transport",
        title="stdio transport launcher with timeouts and reaping",
        goal="Launch stdio MCP servers inside Termux/Debian, keep them alive, and never let a stuck process block a task.",
        deps=[120],
        est="90-180 min",
        skills=[
            ("mcp-protocol", "stdio framing, newline-delimited JSON-RPC, stderr capture"),
            ("kotlin-core", "process supervision with hard timeouts and guaranteed reaping"),
        ],
        deliverables=[
            "`mcp/StdioTransport.kt` with per-server process supervision",
            "A hard request timeout and a kill-on-timeout policy with logging",
        ],
        steps=[
            "Start the server command in the Termux/Debian environment and keep stdin/stdout open.",
            "Frame requests correctly and read responses without deadlocking on a chatty server.",
            "Enforce per-call timeouts; kill and report rather than hanging.",
            "Reap processes on shutdown and on server removal.",
        ],
        accept=[
            "A stdio server starts once and serves multiple calls",
            "A server that never responds is killed after the timeout and reported (asserted with a stub that sleeps)",
            "No orphan process remains after the app stops (verified on device)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*StdioTransport*'",
        ],
        state="stdio MCP servers are usable without risking a hung gateway.",
    ),
    Task(
        id=122,
        slug="mcp-http-transport",
        title="HTTP and SSE transport",
        goal="Call remote MCP servers over HTTP and consume SSE streams where a server uses them.",
        deps=[120],
        est="60-120 min",
        skills=[
            ("mcp-protocol", "HTTP transport semantics and the SSE variant"),
            ("security-audit", "remote servers may need a token — store it in the vault like any other credential"),
        ],
        deliverables=[
            "`mcp/HttpTransport.kt` and `mcp/SseTransport.kt`",
            "Per-server authentication configured through the vault",
        ],
        steps=[
            "Implement request/response over HTTP with correct headers and error propagation.",
            "Consume SSE where the server sends a stream, without buffering indefinitely.",
            "Store any server token in the vault and never in the registry file.",
            "Test against a local stub server, not a third-party service.",
        ],
        accept=[
            "Both transports work against a local stub",
            "A server token is absent from the registry file (asserted)",
            "Timeouts behave as documented",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*HttpTransport*'",
        ],
        state="Remote MCP servers are usable without weakening credential handling.",
    ),
    Task(
        id=123,
        slug="connectors-screen",
        title="Connectors screen",
        goal="Show every connector (provider, GitHub, tunnel, search) with its real state, and let the owner enable or disable it.",
        deps=[120, 103],
        est="60-120 min",
        skills=[
            ("android-compose-ui", "a screen that shows health honestly, including 'configured but unreachable'"),
            ("technical-writing", "one line per connector explaining what it enables"),
        ],
        deliverables=[
            "`ui/connectors/ConnectorsScreen.kt`",
            "Per-connector state source wired to real checks, not to optimistic flags",
        ],
        steps=[
            "List connectors with their state and the last check time.",
            "Provide a 'test' action per connector that performs a real check and shows the result.",
            "Distinguish 'not configured' from 'configured but failing' — they need different owner actions.",
            "Link each connector to the relevant setup documentation.",
        ],
        accept=[
            "Every connector's state comes from a real check",
            "A failing connector names the failure, not just a red dot",
            "Enabling a connector never silently changes another setting",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
        ],
        state="The owner can see the whole integration surface and its real health.",
    ),
    Task(
        id=124,
        slug="plugin-inventory",
        title="Plugin and skill inventory endpoint",
        goal="Expose what the host environment offers — skills, plugins, agent capabilities — so an agent does not guess or shell out.",
        deps=[120, 31],
        est="60-120 min",
        skills=[
            ("mcp-protocol", "what can be read reliably from a host environment"),
            ("security-audit", "an inventory must not expose secrets or private paths unnecessarily"),
        ],
        deliverables=[
            "`GET /plugins` returning discovered skills/plugins with their source and availability",
            "Documentation of what is and is not reliable to detect",
        ],
        steps=[
            "Read host skill directories and plugin manifests through the bridge where paths are known.",
            "Report only names, sources and availability — no file contents, no credentials.",
            "Mark unreliable detections as such instead of guessing.",
        ],
        accept=[
            "`/plugins` returns the host inventory, or states precisely why it is unavailable",
            "No file contents or secrets appear in the response",
            "The docs state which detections are reliable",
        ],
        verify=[
            "curl -fsS http://127.0.0.1:8787/plugins | head -20",
        ],
        state="An agent can see what tooling it has without leaving the gateway.",
    ),
    Task(
        id=125,
        slug="mcp-tests",
        title="MCP test suite",
        goal="Prove discovery, registry precedence, both transports and the auth rules, including the dead-server path.",
        deps=[118, 119, 120, 121, 122, 123, 124],
        est="80-150 min",
        skills=[
            ("testing", "fixtures for each host config format, stub servers, dead-server behaviour"),
            ("security-audit", "assert the auth rule and the absence of environment values in the registry"),
        ],
        deliverables=[
            "`app/src/test/…/mcp/` suite with config fixtures and stub servers",
            "A canary test for environment values",
        ],
        steps=[
            "Add fixtures for each supported configuration format, including one malformed file.",
            "Add stub stdio and HTTP servers to drive both transports offline.",
            "Assert: precedence, auth requirement on `tools/call`, timeout kill, reaping, redaction.",
            "Keep the suite offline and deterministic.",
        ],
        accept=[
            "All MCP behaviour is covered by offline tests",
            "The canary test proves no environment value reaches the registry",
            "A dead server degrades gracefully in a test rather than hanging",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*mcp*'",
        ],
        state="MCP federation is proven, including the paths that only fail in production otherwise.",
    ),
    Task(
        id=126,
        slug="mcp-documentation-de",
        title="MCP documentation and owner guide",
        goal="Document, in the owner's language as well, how MCP servers are discovered, what the app does with them, and how to add one permanently.",
        deps=[125],
        est="40-80 min",
        skills=[
            ("technical-writing", "accurate, complete, no filler"),
            ("mcp-protocol", "verify every claim against the implementation"),
        ],
        deliverables=[
            "`docs/07-mcp-plugins.md` finalised against the implementation",
            "German summary entries in docs/glossary-de.md for any new term",
        ],
        steps=[
            "Walk through each documented behaviour and verify it matches the code.",
            "Add the 'how to add a server permanently' recipe with a worked example.",
            "Document the degraded behaviour when Termux is unavailable.",
        ],
        accept=[
            "Every statement in the doc is verifiable in the implementation",
            "The recipe produces a working server when followed literally",
            "No term appears in the doc that the glossary does not explain",
        ],
        verify=[
            "python3 tools/check_links.py",
            "./gradlew :app:testDebugUnitTest --tests '*mcp*'",
        ],
        state="MCP usage is documented for both an agent and the owner, and the doc is true.",
    ),
]
