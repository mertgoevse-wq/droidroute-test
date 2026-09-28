"""Phase 03 — Provider catalog: Tier 1 free gateways first, then the majors.

Every provider task obeys the same rule: read the provider's own documentation and
validate with a live call. A guessed base URL is a bug, not a placeholder.
"""

from common import Phase, Task

PHASE = Phase(
    number=3,
    slug="provider-catalog",
    title="Provider catalog",
    summary="Manifest + live validation for each Tier 1 free gateway, then the Tier 2 majors.",
)

_VERIFY_DOCS = "Read the provider's current documentation; do not reuse the URL from any other source."

TASKS = [
    Task(
        id=37,
        slug="provider-bynara",
        title="Provider: Bynara / NaraRouter (priority)",
        goal=(
            "Wire the owner's highest-priority gateway first: free tier, ~7M tokens/day, ~50 models, "
            "OpenAI-compatible. Manifest, one-click connect, live validation."
        ),
        deps=[27, 29, 31],
        est="40-80 min",
        skills=[
            ("provider-integration", "confirm base URL, auth header and model list from the provider's own site"),
            ("testing", "fixture plus a live validation call, skipped cleanly without a key"),
        ],
        deliverables=[
            "`assets/providers/bynara.json` with `tier: 1`, `auth.type: bearer`, discovery on `/models`",
            "`quota.window: daily` with the documented hint",
        ],
        steps=[
            f"{_VERIFY_DOCS} Base URL is documented as `https://router.bynara.id/v1` — confirm it before committing.",
            "Register the provider in docs/03-providers.md with its tag `free` and `one-click`.",
            "Validate a real key with a models-list call and record the model count in the task log.",
            "Record the quota reset behaviour observed from the provider's response headers.",
        ],
        accept=[
            "The provider appears in `/v1/providers` as Tier 1 with `free` and `one-click` tags",
            "A live key validates and lists a non-zero model count (or the task logs why it could not be tested)",
            "The manifest contains no hard-coded model list that contradicts discovery",
        ],
        verify=[
            "python3 tools/check_providers.py",
            "./gradlew :app:testDebugUnitTest --tests '*bynara*'",
        ],
        state="The owner's primary free gateway is connected, validated and routable.",
    ),
    Task(
        id=38,
        slug="provider-freellmapi",
        title="Provider: FreeLLMAPI",
        goal="Support the self-hosted FreeLLMAPI instance that pools many free provider tiers behind one endpoint.",
        deps=[27, 31],
        est="40-80 min",
        skills=[
            ("provider-integration", "self-hosted base URL configuration and its onboarding flow"),
            ("technical-writing", "the Termux/Debian steps to run the instance locally"),
        ],
        deliverables=[
            "`assets/providers/freellmapi.json` with a loopback default base URL",
            "`docs/providers/freellmapi.md` — how to run it, where its keys live, how to verify it",
        ],
        steps=[
            f"{_VERIFY_DOCS} Record the default local port and the path prefix it serves.",
            "Allow an http:// loopback base URL (the manifest validator already permits loopback).",
            "Document that its upstream keys are managed by the FreeLLMAPI instance, not by DroidRoute.",
            "Validate with a models call against a running instance, or log that none was reachable.",
        ],
        accept=[
            "A loopback base URL is accepted while remote plaintext http is still rejected",
            "The doc explains the split of responsibilities between DroidRoute and FreeLLMAPI",
            "Validation either succeeds or records the exact reason it could not run",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="The free-tier aggregator is usable as a normal provider.",
    ),
    Task(
        id=39,
        slug="provider-apinex",
        title="Provider: APInex",
        goal="Connect the APInex gateway with daily-reset free model limits.",
        deps=[27, 31],
        est="30-60 min",
        skills=[
            ("provider-integration", "confirm base URL and the daily limit semantics"),
            ("testing", "fixture plus rate-limit body handling"),
        ],
        deliverables=[
            "`assets/providers/apinex.json` with `quota.window: daily` and tag `free`",
            "A fixture reproducing its daily-limit response so the router can park the key",
        ],
        steps=[
            f"{_VERIFY_DOCS} Confirm the base URL (documented as `https://apinex.bond/v1`).",
            "Capture a real rate-limit response and turn it into a fixture for the error taxonomy.",
            "Confirm whether the limit resets on a fixed clock or a rolling window and record it.",
        ],
        accept=[
            "The provider validates and lists models",
            "The limit response maps to `QuotaExceeded` in a test",
            "The recorded reset semantics match what the provider documents",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*apinex*'",
            "python3 tools/check_providers.py",
        ],
        state="A daily-limited free gateway is connected and the router knows how to park it.",
    ),
    Task(
        id=40,
        slug="provider-gorouter",
        title="Provider: GoRouter",
        goal="Connect GoRouter, which offers both an OpenAI-compatible and an Anthropic-compatible surface.",
        deps=[27, 28, 31],
        est="40-80 min",
        skills=[
            ("provider-integration", "two surfaces from one account — one provider, two manifests or one dual manifest"),
            ("testing", "call both surfaces and assert consistent behaviour"),
        ],
        deliverables=[
            "`assets/providers/gorouter.json` declaring both surfaces",
            "Decision record if the dual-surface shape needs an extension to the manifest schema",
        ],
        steps=[
            f"{_VERIFY_DOCS} Confirm both endpoint paths and whether one key covers both.",
            "If two surfaces are needed, register them as `gorouter` and `gorouter-anthropic` with a shared account note.",
            "Validate both with a live call and record latency for each.",
        ],
        accept=[
            "Both surfaces work or the unusable one is explicitly disabled with a reason",
            "The routing engine can use either surface for the same logical model",
            "Latency of both is recorded in the task log",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*gorouter*'",
        ],
        state="A dual-surface gateway is fully available to both protocol families.",
    ),
    Task(
        id=41,
        slug="provider-tokenrouter",
        title="Provider: TokenRouter",
        goal="Connect TokenRouter as a credit gateway with discovery-first model handling.",
        deps=[27, 31],
        est="30-60 min",
        skills=[
            ("provider-integration", "confirm base URL and credit-account semantics"),
            ("testing", "discovery fixture and an insufficient-credit error fixture"),
        ],
        deliverables=[
            "`assets/providers/tokenrouter.json`",
            "Fixture for its insufficient-credit response (maps to `QuotaExceeded`)",
        ],
        steps=[
            f"{_VERIFY_DOCS} The base URL is not public knowledge — do not guess it; leave the task blocked and logged if it cannot be confirmed.",
            "Add the credit-exhausted response to the taxonomy fixtures.",
            "Record how credits are displayed so the dashboard can show remaining balance when the provider exposes it.",
        ],
        accept=[
            "The manifest uses only a confirmed base URL",
            "Credit exhaustion parks the key instead of marking it invalid",
            "Any uncertainty about the provider's API is recorded in the task log, not papered over",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="TokenRouter is either working with confirmed details, or explicitly blocked with evidence.",
    ),
    Task(
        id=42,
        slug="provider-tokenreply",
        title="Provider: TokenReply",
        goal="Connect TokenReply following the same evidence rule as TokenRouter.",
        deps=[27, 31],
        est="30-60 min",
        skills=[
            ("provider-integration", "confirm base URL, auth header, model list"),
            ("testing", "fixture set for success and quota errors"),
        ],
        deliverables=[
            "`assets/providers/tokenreply.json`",
            "Fixtures for its success and error shapes",
        ],
        steps=[
            f"{_VERIFY_DOCS}",
            "Validate a key and record the model count.",
            "Note any deviation from the OpenAI standard (extra required fields, different auth header).",
        ],
        accept=[
            "Only a confirmed base URL is committed",
            "A live validation ran or the blocker is logged",
            "Any non-standard requirement is captured as a manifest field, not as adapter special-case code",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="TokenReply is connected or explicitly blocked with a reason a later agent can act on.",
    ),
    Task(
        id=43,
        slug="provider-fastrouter",
        title="Provider: FastRouter",
        goal="Connect FastRouter, a latency-oriented router front-end.",
        deps=[27, 31],
        est="30-60 min",
        skills=[
            ("provider-integration", "confirm base URL and whether it proxies other gateways"),
            ("performance-android", "it claims low latency — measure it rather than repeat the claim"),
        ],
        deliverables=[
            "`assets/providers/fastrouter.json`",
            "A latency measurement from a real call, recorded in the task log",
        ],
        steps=[
            f"{_VERIFY_DOCS}",
            "Measure time-to-first-byte for a short prompt and store the number.",
            "Confirm whether it needs any special header to select an upstream model family.",
        ],
        accept=[
            "The manifest uses only confirmed values",
            "A measured latency number exists (or the blocker is logged)",
            "No marketing claim from the provider is repeated in the docs as fact",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="FastRouter is connected with a measured latency figure, not an assumed one.",
    ),
    Task(
        id=44,
        slug="provider-xkiro",
        title="Provider: xKiro",
        goal="Connect xKiro, the 'every leading model, one API key' gateway, and validate its model breadth.",
        deps=[27, 31],
        est="30-60 min",
        skills=[
            ("provider-integration", "confirm base URL and auth from the provider's own docs"),
            ("testing", "discovery fixture and one live validation"),
        ],
        deliverables=[
            "`assets/providers/xkiro.json` with `tier: 1`, tag `credits`",
            "Recorded model count and confirmed base URL in the task log",
        ],
        steps=[
            f"{_VERIFY_DOCS}",
            "Validate a key, record the model count and any model-id naming quirks.",
            "Note whether the provider reports usage for cost accounting.",
        ],
        accept=[
            "The provider validates and lists models, or the blocker is logged",
            "Base URL and auth header are confirmed, not assumed",
            "Usage reporting availability is recorded",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="xKiro is available to routing with confirmed connection details.",
    ),
    Task(
        id=45,
        slug="provider-experiential-labs",
        title="Provider: Experiential Labs",
        goal="Connect Experiential Labs, including its ability to front the owner's own keys or a local model.",
        deps=[27, 31],
        est="40-80 min",
        skills=[
            ("provider-integration", "confirm the API surface and the bring-your-own-key behaviour"),
            ("technical-writing", "document the two ways to use it (their keys vs the owner's keys)"),
        ],
        deliverables=[
            "`assets/providers/experiential.json` with base `https://api.experientiallabs.ai/v1` confirmed",
            "Documentation of the bring-your-own-key mode and how it interacts with DroidRoute's own keys",
        ],
        steps=[
            f"{_VERIFY_DOCS}",
            "Test a plain call and, if the mode exists, a call through a key DroidRoute itself stores.",
            "Record whether its response includes trace or simulation identifiers worth surfacing.",
        ],
        accept=[
            "A live call succeeds or the blocker is logged",
            "The bring-your-own-key interaction is documented without ambiguity about who holds the secret",
            "No assumed field name is parsed without a fixture proving it",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="Experiential Labs is connected and its key-ownership model is documented honestly.",
    ),
    Task(
        id=46,
        slug="provider-openrouter",
        title="Provider: OpenRouter with free-model tagging",
        goal="Connect OpenRouter and tag its free models so the `free_first` strategy can prefer them.",
        deps=[27, 29, 32],
        est="40-80 min",
        skills=[
            ("provider-integration", "the free/paid distinction in its model list and the correct attribution headers"),
            ("llm-routing", "how the free tag feeds candidate ordering"),
        ],
        deliverables=[
            "`assets/providers/openrouter.json` with base `https://openrouter.ai/api/v1`",
            "Model tagging so `:free` variants are recognised without hard-coded id lists",
        ],
        steps=[
            "Derive free-ness from the model metadata when available; otherwise from the documented id suffix.",
            "Send the optional attribution headers the provider requests.",
            "Confirm that the free subset is visible in `/v1/models` with the free tag.",
        ],
        accept=[
            "Free models are tagged and preferred under `free_first`",
            "No free model id is hard-coded; tagging survives a model-list refresh",
            "Attribution headers are sent when configured",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*openrouter*'",
        ],
        state="A large free model pool is available and correctly prioritised.",
    ),
    Task(
        id=47,
        slug="provider-groq",
        title="Provider: Groq",
        goal="Connect Groq's free tier, which is the strongest candidate for the `fastest` strategy.",
        deps=[27, 32],
        est="30-60 min",
        skills=[
            ("provider-integration", "free-tier limits and the correct base URL"),
            ("performance-android", "measure the actual latency advantage instead of assuming it"),
        ],
        deliverables=[
            "`assets/providers/groq.json` with base `https://api.groq.com/openai/v1`",
            "A latency measurement recorded for comparison with other providers",
        ],
        steps=[
            "Validate a key and record the model list.",
            "Measure time-to-first-byte for a short streaming prompt.",
            "Record its rate-limit headers so the quota ledger can learn the window.",
        ],
        accept=[
            "A live validation succeeds or the blocker is logged",
            "Latency is recorded as a number",
            "Rate-limit header names are recorded for the ledger task",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="A low-latency provider is connected with evidence for the `fastest` strategy.",
    ),
    Task(
        id=48,
        slug="provider-cerebras",
        title="Provider: Cerebras",
        goal="Connect Cerebras's free tier and record its throughput characteristics.",
        deps=[27, 32],
        est="30-60 min",
        skills=[
            ("provider-integration", "base URL, key handling, model list"),
            ("testing", "fixture coverage for its error shapes"),
        ],
        deliverables=[
            "`assets/providers/cerebras.json` with base `https://api.cerebras.ai/v1`",
            "Recorded model list and rate-limit headers",
        ],
        steps=[
            "Validate a key and record the model list, noting any model-id naming that differs from upstream names.",
            "Record the rate-limit headers and the documented free-tier window.",
            "Measure time-to-first-byte and tokens/second for a short response.",
        ],
        accept=[
            "The provider validates and its models appear in the catalog",
            "Throughput numbers are recorded",
            "Model naming quirks are captured so aliases can map them later",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="A high-throughput free provider is available to routing.",
    ),
    Task(
        id=49,
        slug="provider-google-ai-studio",
        title="Provider: Google AI Studio (free-tier key)",
        goal="Connect the Gemini API free tier via API key — separate from the AI Pro OAuth account handled in Phase 4.",
        deps=[28, 30],
        est="40-80 min",
        skills=[
            ("provider-integration", "the Gemini API surface and its key parameter style"),
            ("testing", "fixture for its error envelope, which differs from OpenAI's"),
        ],
        deliverables=[
            "`assets/providers/google-ai-studio.json` with base `https://generativelanguage.googleapis.com/v1beta`",
            "Gemini-style error parsing in the adapter path",
        ],
        steps=[
            "Support key-in-header and key-in-query styles, choosing the documented modern one.",
            "Normalise the Gemini error envelope into the taxonomy (it is not OpenAI-shaped).",
            "Confirm that this key and the Phase 4 OAuth account are distinct entities in the UI.",
        ],
        accept=[
            "A live call succeeds or the blocker is logged",
            "Gemini-shaped errors map correctly in a test",
            "The UI can hold both the API key account and the OAuth account without conflating them",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*google*'",
        ],
        state="Google models are available both through the free key tier and (later) the Pro subscription.",
    ),
    Task(
        id=50,
        slug="provider-mistral",
        title="Provider: Mistral",
        goal="Connect Mistral's API including its free experimental tier.",
        deps=[27, 29],
        est="30-60 min",
        skills=[
            ("provider-integration", "free-tier model naming and rate limits"),
            ("testing", "discovery fixture and one live validation"),
        ],
        deliverables=[
            "`assets/providers/mistral.json` with base `https://api.mistral.ai/v1`",
            "Free-tier models tagged so `free_first` can prefer them",
        ],
        steps=[
            "Validate a key and record the model list.",
            "Tag the free-tier models from the documented naming.",
            "Record the rate-limit headers and window.",
        ],
        accept=[
            "The provider validates and its models appear",
            "Free-tier models are tagged without hard-coding ids that could change",
            "Rate-limit header names are recorded",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="Mistral is connected with its free tier preferred by the free-first strategy.",
    ),
    Task(
        id=51,
        slug="provider-github-models",
        title="Provider: GitHub Models",
        goal="Connect GitHub Models using a GitHub token, reusing the OAuth work where a token is already available.",
        deps=[27, 30],
        est="30-60 min",
        skills=[
            ("provider-integration", "token requirements and the models endpoint"),
            ("security-audit", "a GitHub token is powerful — store it in the vault and scope it minimally"),
        ],
        deliverables=[
            "`assets/providers/github-models.json` with base `https://models.inference.ai.azure.com`",
            "A note in docs/05-security.md about the minimum token scope this provider needs",
        ],
        steps=[
            "Register the provider expecting a fine-grained token, not a broad personal access token.",
            "Validate with a models call and record the model list.",
            "Document the scope requirement and the reason.",
        ],
        accept=[
            "The provider validates with a minimally scoped token",
            "The token is stored only in the vault",
            "The required scope is documented",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="GitHub-hosted models are available without a wide-scoped credential.",
    ),
    Task(
        id=52,
        slug="provider-cloudflare-workers-ai",
        title="Provider: Cloudflare Workers AI",
        goal="Connect Cloudflare Workers AI, whose base URL embeds an account id.",
        deps=[27, 33],
        est="30-60 min",
        skills=[
            ("provider-integration", "account-scoped base URL template"),
            ("kotlin-core", "template substitution in the manifest without string concatenation bugs"),
        ],
        deliverables=[
            "`assets/providers/cloudflare-workers-ai.json` with an account-id placeholder",
            "Manifest support for a templated base URL with a required setting",
        ],
        steps=[
            "Allow a `{account_id}` placeholder resolved from provider settings at load time.",
            "Fail with a specific message when the setting is missing, rather than producing a broken URL.",
            "Validate a key and record the free daily allowance.",
        ],
        accept=[
            "A missing account id produces a clear error and disables the provider",
            "With the id present, a live call succeeds or the blocker is logged",
            "No other manifest's base URL is templated, keeping the feature narrowly scoped",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Template*'",
        ],
        state="Account-scoped providers can be expressed as data without per-provider code.",
    ),
    Task(
        id=53,
        slug="provider-nvidia-nim",
        title="Provider: NVIDIA NIM",
        goal="Connect NVIDIA NIM and record its credit model so the dashboard can show remaining balance where exposed.",
        deps=[27, 32],
        est="30-60 min",
        skills=[
            ("provider-integration", "base URL, auth, model list"),
            ("testing", "fixture for the credit-exhausted path"),
        ],
        deliverables=[
            "`assets/providers/nvidia-nim.json` with base `https://integrate.api.nvidia.com/v1`",
            "Credit-state handling if the API exposes it",
        ],
        steps=[
            "Validate a key and record the model list.",
            "Check whether remaining credits are queryable; if yes, wire that into the provider status.",
            "Add the exhausted path to the router's quota fixtures.",
        ],
        accept=[
            "The provider validates and its models appear",
            "Credit state is either surfaced from real data or explicitly marked unavailable",
            "The exhausted path is covered by a test",
        ],
        verify=[
            "python3 tools/check_providers.py",
        ],
        state="A credit-based provider is connected with honest balance reporting.",
    ),
    Task(
        id=54,
        slug="provider-tier2-majors",
        title="Provider: Tier 2 majors batch",
        goal=(
            "Add manifests for the paid and subscription providers the owner may hold keys for: OpenAI, Anthropic, "
            "Gemini, xAI, DeepSeek, DashScope/Qwen, Together, Fireworks, DeepInfra, Novita, Hyperbolic, Nebius, "
            "SambaNova, Cohere, AI21, Scaleway, Chutes, Kluster."
        ),
        deps=[27, 28, 29],
        est="90-180 min",
        skills=[
            ("provider-integration", "confirm each base URL from its own documentation; batch the work but verify each"),
            ("testing", "one fixture per provider family plus a sweep test asserting every manifest loads"),
        ],
        deliverables=[
            "One manifest per provider in `assets/providers/`",
            "A test that loads every shipped manifest and asserts it validates",
        ],
        steps=[
            "Work in batches of four providers; confirm each base URL and auth style before writing its manifest.",
            "Mark providers whose details could not be confirmed as `draft: true` and keep them disabled by default.",
            "Add each entry to the docs/03-providers.md table in the same commit.",
            "Run the sweep test so a typo in any manifest fails the build.",
        ],
        accept=[
            "`tools/check_providers.py` passes with the docs in sync",
            "Every manifest validates; unconfirmed ones are marked draft and disabled",
            "No base URL was copied from another manifest without confirmation",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ManifestSweep*'",
            "python3 tools/check_providers.py",
        ],
        state="The provider catalogue is broad, validated and honest about what is unconfirmed.",
    ),
]
