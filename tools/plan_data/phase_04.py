"""Phase 04 — Accounts & OAuth: subscriptions connected honestly, with clear failure states.

The owner holds a Google AI Pro subscription and a Perplexity Pro subscription. This
phase connects what has a supported programmatic path, and labels what does not.
"""

from common import Phase, Task

PHASE = Phase(
    number=4,
    slug="accounts-oauth",
    title="Accounts & OAuth",
    summary="OAuth flows, token refresh, subscription accounts, Perplexity Sonar search.",
)

TASKS = [
    Task(
        id=55,
        slug="oauth-framework",
        title="OAuth framework (PKCE, browser intent, redirect)",
        goal=(
            "Build the shared OAuth machinery once: authorization-code with PKCE, a Custom Tab / browser intent, "
            "a loopback or custom-scheme redirect, and vault-backed token storage."
        ),
        deps=[6, 30],
        est="90-180 min",
        skills=[
            ("oauth-device-flow", "PKCE, state parameter, redirect handling on Android"),
            ("security-audit", "no token in logs, no implicit flow, state verified on every callback"),
        ],
        deliverables=[
            "`provider/oauth/OAuthEngine.kt` — start(providerId), handleCallback(uri), refresh(accountId)",
            "Token storage via the vault: access token, refresh token, expiry, scopes",
        ],
        steps=[
            "Implement PKCE with S256 and a random state that is verified on return.",
            "Open the authorization URL in a Custom Tab; accept the callback through a claimed intent filter.",
            "Store tokens in the vault and expose only account metadata (scopes, expiry) elsewhere.",
            "Collect a per-provider client id/secret from settings — never ship one in the repo.",
        ],
        accept=[
            "A mock provider completes the full flow and the token lands in the vault",
            "A callback with a wrong state parameter is rejected and logged",
            "No token value appears in any log line (canary test)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*OAuthEngine*'",
        ],
        state="One OAuth implementation serves every account provider; adding one is configuration.",
    ),
    Task(
        id=56,
        slug="oauth-google",
        title="Google account (AI Pro / Gemini)",
        goal="Connect the owner's Google AI Pro account through OAuth so Gemini models are usable under the subscription.",
        deps=[55, 49],
        est="90-180 min",
        skills=[
            ("oauth-device-flow", "Google OAuth specifics: scopes, consent screen, refresh semantics"),
            ("provider-integration", "which endpoint the subscription actually grants access to"),
        ],
        deliverables=[
            "`assets/providers/google-account.json` with `auth.type: oauth-google`",
            "Setup doc `docs/accounts/google.md` covering client id creation and consent-screen configuration",
        ],
        steps=[
            "Determine from Google's current documentation which API surface the subscription grants, and record it.",
            "Request the minimum scopes needed for that surface.",
            "Complete the flow, then make one real call and record which models answered.",
            "Document clearly what the subscription does and does not unlock for programmatic use.",
        ],
        accept=[
            "A real call succeeds through the OAuth account, or the limitation is documented with evidence",
            "Requested scopes are the minimum needed",
            "The setup doc lists every step the owner must perform in the Google console",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*google*'",
        ],
        state="The Google subscription is connected where it can be, and the limits are documented where it cannot.",
    ),
    Task(
        id=57,
        slug="token-refresh-and-failure-states",
        title="Token refresh scheduler and failure states",
        goal="Refresh tokens before expiry, back off on failure, and surface `needs_attention` instead of failing requests mysteriously.",
        deps=[55, 56],
        est="50-100 min",
        skills=[
            ("kotlin-core", "scheduled refresh without wake-lock abuse; single-flight refresh per account"),
            ("testing", "expiry, refresh failure, revoked refresh token, clock skew"),
        ],
        deliverables=[
            "`provider/oauth/TokenRefresher.kt` with exponential backoff and jitter",
            "Account state enum: connected, expiring, refreshing, needs_attention(reason)",
        ],
        steps=[
            "Refresh 5 minutes before expiry and on any 401 from the provider.",
            "Single-flight per account so ten parallel requests cause one refresh, not ten.",
            "On `invalid_grant`, mark `needs_attention` and stop retrying until the owner re-authorises.",
            "Log every refresh outcome with provider, account label and reason.",
        ],
        accept=[
            "An expiring token is refreshed without a failed request",
            "Concurrent requests trigger exactly one refresh (asserted by a test)",
            "A revoked refresh token results in `needs_attention`, not a retry storm",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*TokenRefresher*'",
        ],
        state="Subscription accounts stay connected across restarts and degrade visibly, never silently.",
    ),
    Task(
        id=58,
        slug="oauth-github",
        title="GitHub account (Copilot / Models)",
        goal="Connect a GitHub account via OAuth so Copilot- and Models-backed providers can use it without a pasted token.",
        deps=[55, 51],
        est="60-120 min",
        skills=[
            ("oauth-device-flow", "GitHub OAuth app setup and scope minimisation"),
            ("security-audit", "the account grants repository access — keep scopes minimal and document them"),
        ],
        deliverables=[
            "`assets/providers/github-account.json` with `auth.type: oauth-github`",
            "Setup doc with the exact OAuth app settings and required scopes",
        ],
        steps=[
            "Request the minimum scopes needed for the models endpoint; avoid repository scopes entirely if possible.",
            "Complete the flow and validate with a models call.",
            "Document that the token is stored in the vault and revocable from GitHub's side.",
        ],
        accept=[
            "A live call succeeds through the OAuth account, or the blocker is documented",
            "No repository scope is requested unless proven necessary",
            "The setup doc names every scope and why it is needed",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*github*'",
        ],
        state="GitHub-backed models are reachable without a hand-pasted personal access token.",
    ),
    Task(
        id=59,
        slug="oauth-huggingface",
        title="HuggingFace account",
        goal="Connect HuggingFace via OAuth so hosted inference models are available under the owner's account.",
        deps=[55],
        est="45-90 min",
        skills=[
            ("oauth-device-flow", "HuggingFace OAuth endpoints and token handling"),
            ("provider-integration", "which inference endpoint the account grants"),
        ],
        deliverables=[
            "`assets/providers/huggingface-account.json` with `auth.type: oauth-hf`",
            "Setup doc with the OAuth app configuration",
        ],
        steps=[
            "Implement the flow using the documented endpoints and scopes.",
            "Validate with a call to the inference surface and record which models responded.",
            "Record whether the account also unlocks dataset or repo scopes that DroidRoute does not need.",
        ],
        accept=[
            "The flow completes and a live inference call succeeds, or the blocker is logged",
            "Only inference-related scopes are requested",
            "The account appears in the UI as its own entity, distinct from a pasted HF token",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*huggingface*'",
        ],
        state="HuggingFace models are reachable under the owner's own account.",
    ),
    Task(
        id=60,
        slug="perplexity-sonar-api",
        title="Perplexity Sonar through the official API",
        goal=(
            "Implement the supported path: the Perplexity API key with the Sonar model family, search-mode fields, "
            "and citations preserved in the response."
        ),
        deps=[27, 29],
        est="60-120 min",
        skills=[
            ("provider-integration", "Sonar model names and the search-specific request fields"),
            ("testing", "fixtures that include a citations array"),
        ],
        deliverables=[
            "`assets/providers/perplexity.json` with base `https://api.perplexity.ai` and models `sonar`, `sonar-pro`, `sonar-reasoning`, `sonar-deep-research`",
            "`search_mode` handling adding `search_recency_filter`, `search_domain_filter`, `return_citations`",
        ],
        steps=[
            "Extend the OpenAI-compatible adapter with an opt-in `search_mode` that adds the search fields.",
            "Preserve `citations` in the normalised response instead of dropping unknown fields.",
            "Record which Sonar models the owner's key can actually reach.",
        ],
        accept=[
            "A real Sonar call returns an answer with a non-empty citations array, or the blocker is logged",
            "`search_mode` is opt-in and never applied to non-search models",
            "Citations survive the normalisation step (asserted in a test)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*perplexity*'",
        ],
        state="Perplexity search works through the supported API, with citations intact.",
    ),
    Task(
        id=61,
        slug="search-endpoint",
        title="`POST /v1/search` convenience endpoint",
        goal="Expose DroidRoute's own search façade returning `{answer, citations[], model, provider}` so agents can search without knowing the provider.",
        deps=[60, 15],
        est="40-80 min",
        skills=[
            ("llm-gateway-protocols", "a stable, documented response shape"),
            ("testing", "routing to the search-capable provider, error when none is available"),
        ],
        deliverables=[
            "`server/routes/SearchRoutes.kt`",
            "Documentation in docs/02-protocols.md including the response schema",
        ],
        steps=[
            "Route the request to providers declaring search capability, honouring the active strategy.",
            "Return a clear `no_provider_available` error when no search-capable provider is enabled.",
            "Include `request_id` and the provider used so the answer is traceable.",
            "Document the endpoint with a request and response example that were both actually executed.",
        ],
        accept=[
            "The endpoint returns an answer with citations from a real provider",
            "Without a search provider it returns the documented error, not a 500",
            "The documented example matches a real captured response",
        ],
        verify=[
            "curl -fsS -X POST http://127.0.0.1:8787/v1/search -d '{\"query\":\"test\"}'",
            "./gradlew :app:testDebugUnitTest --tests '*SearchRoutes*'",
        ],
        state="Agents have a provider-independent search entry point.",
    ),
    Task(
        id=62,
        slug="perplexity-account-mode-experimental",
        title="Perplexity account mode (experimental, off by default)",
        goal=(
            "Honour the owner's request to explore using the Pro subscription directly, while keeping it strictly opt-in, "
            "clearly labelled, and never used automatically by routing."
        ),
        deps=[60],
        est="90-180 min",
        skills=[
            ("security-audit", "session material is equivalent to a password — store it like one and document the risk"),
            ("provider-integration", "assess honestly whether the web session can be driven at all"),
        ],
        deliverables=[
            "`provider/experimental/SessionAccountAdapter.kt` behind `settings.experimentalAccountMode`",
            "A warning screen stating what this is, what it is not, and what can break",
        ],
        steps=[
            "Assess the approach and document the finding: is a session-driven call technically feasible and stable?",
            "If it is not feasible, record that decision in status/DECISIONS.md and stop — do not ship a fake path.",
            "If it is, implement it behind the flag with session material in the vault and mandatory owner confirmation.",
            "Never place this adapter in the automatic routing candidate list.",
        ],
        accept=[
            "The feature is off by default and reachable only after an explicit, informed confirmation",
            "Routing never selects it automatically (asserted by a test)",
            "Either a working path or a documented negative finding exists — no half-implementation",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*SessionAccount*'",
        ],
        state="The experimental account mode exists as a labelled, opt-in risk — or as a documented 'not feasible' finding.",
    ),
    Task(
        id=63,
        slug="account-state-ui-data",
        title="Account state model and `needs_attention` surfacing",
        goal="Give the UI everything it needs to show account health without exposing tokens: state, expiry, scopes, last error.",
        deps=[57, 58, 59],
        est="40-80 min",
        skills=[
            ("kotlin-core", "state model without token leakage; expiry formatting"),
            ("android-compose-ui", "the shape the account screen needs, defined before the screen is built"),
        ],
        deliverables=[
            "`provider/oauth/AccountState.kt` and its exposure through `/v1/providers`",
            "Account list data source for the UI (no secrets)",
        ],
        steps=[
            "Model per account: provider id, label, state, expiry, scopes, last refresh result.",
            "Expose it through the existing provider endpoint rather than a new one.",
            "Add a test asserting the serialised account contains no token-shaped value.",
        ],
        accept=[
            "Accounts appear with their real state in `/v1/providers`",
            "An expiring account is visible before it fails",
            "No token material is present in the API response (canary test)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*AccountState*'",
            "curl -fsS http://127.0.0.1:8787/v1/providers | grep -c token",
        ],
        state="Account health is visible and safe to display.",
    ),
    Task(
        id=64,
        slug="oauth-test-suite",
        title="OAuth test suite with a mock provider",
        goal="Test the whole OAuth path offline against a mock authorization server, including the failure cases that are painful to reproduce live.",
        deps=[55, 56, 57, 58, 59, 62],
        est="60-120 min",
        skills=[
            ("testing", "mock authorization server, token expiry, refresh failure, state mismatch"),
            ("security-audit", "assert the dangerous cases are rejected, not merely untested"),
        ],
        deliverables=[
            "`app/src/test/…/oauth/` suite with a local mock server",
            "Documented coverage list inside the test file header",
        ],
        steps=[
            "Stand up an embedded mock server implementing the authorization-code exchange.",
            "Test: happy path, wrong state, expired code, refresh success, refresh `invalid_grant`, clock skew.",
            "Assert that no test writes a token to the log or the database in plaintext.",
            "Keep the suite offline and fast.",
        ],
        accept=[
            "All OAuth failure modes are covered and asserted",
            "The suite runs offline in under 30 seconds",
            "The token-canary assertion is present and passes",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*oauth*'",
        ],
        state="OAuth is provable without touching a real account.",
    ),
    Task(
        id=65,
        slug="accounts-documentation-de",
        title="Account setup documentation for the owner",
        goal="Write the German-language setup guidance the owner needs for each account, since every OAuth app registration happens outside this repository.",
        deps=[64],
        est="40-80 min",
        skills=[
            ("technical-writing", "precise console steps, no filler, screenshots only if genuinely needed"),
            ("oauth-device-flow", "verify every step is current before writing it down"),
        ],
        deliverables=[
            "`docs/accounts/README.md` (English, canonical) plus a German summary section per provider",
            "An entry in docs/glossary-de.md for any new term introduced",
        ],
        steps=[
            "For each account (Google, GitHub, HuggingFace, Perplexity), list: where to register the app, which scopes, which redirect, where to paste the client id.",
            "State explicitly which steps the owner must do and which the app does.",
            "Note what happens if a step is skipped.",
            "Keep English as the canonical text and add the German short version, consistent with the project's language rule.",
        ],
        accept=[
            "Every account has a complete, ordered setup list",
            "Each step names the exact screen or command",
            "No step is described that the code does not actually require",
        ],
        verify=[
            "python3 tools/check_links.py",
        ],
        state="The owner can register every OAuth app without guessing, and a future agent can follow the same doc.",
    ),
]
