"""Phase 06 — Routing: candidates, strategies, quota-aware key rotation, failover."""

from common import Phase, Task

PHASE = Phase(
    number=6,
    slug="routing",
    title="Routing",
    summary="Candidate resolution, strategies, quota ledgers, multi-key chaining, failover and explainability.",
)

TASKS = [
    Task(
        id=79,
        slug="candidate-resolution",
        title="Candidate resolution and canonical model ids",
        goal="Turn a requested model name into an ordered candidate list of `(provider, model)` pairs, deterministically.",
        deps=[29, 25],
        est="60-120 min",
        skills=[
            ("llm-routing", "resolution rules and canonical id format"),
            ("testing", "resolution table tests including ambiguous and unknown names"),
        ],
        deliverables=[
            "`routing/CandidateResolver.kt`",
            "Canonical id rule implemented: `provider/model`, with bare names resolved through aliases",
        ],
        steps=[
            "Resolve `provider/model` exactly; reject a disabled provider with a clear reason.",
            "Resolve a bare model name across every provider offering it, then order by the active strategy.",
            "Return an empty list with a reason (not an exception) when nothing matches, so the error mapper can shape it.",
            "Keep resolution pure and side-effect free so it is trivially testable.",
        ],
        accept=[
            "Resolution is deterministic for identical inputs (asserted by repeated calls in a test)",
            "An unknown model produces a `no_candidate` reason naming the model",
            "An ambiguous bare name resolves across all providers, not just the first",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*CandidateResolver*'",
        ],
        state="Every request has a defined candidate list before any network call happens.",
    ),
    Task(
        id=80,
        slug="aliases-and-model-groups",
        title="Aliases and model groups",
        goal="Let the owner define names like `my-best` that expand into a prioritised candidate list with its own strategy.",
        deps=[79],
        est="50-100 min",
        skills=[
            ("llm-routing", "alias semantics, precedence, and strategy override per alias"),
            ("persistence-room", "alias storage and validation"),
        ],
        deliverables=[
            "`routing/AliasResolver.kt` + Room entity for aliases",
            "Validation preventing alias cycles and self-reference",
        ],
        steps=[
            "Define an alias as `{name, candidates[], strategy?, pinnedProvider?}`.",
            "Reject cycles at save time with a readable message instead of failing at request time.",
            "Expose aliases in the model list so clients can request them like any model.",
            "Never let an alias silently fall back to a model the owner did not list.",
        ],
        accept=[
            "An alias request routes to the first working candidate in its order",
            "A cyclic alias definition is rejected at save time",
            "Aliases appear in `/v1/models` and resolve through `/v1/routing/explain`",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*AliasResolver*'",
        ],
        state="The owner can express intent ('best free model') once and reuse it everywhere.",
    ),
    Task(
        id=81,
        slug="key-pool-quota-ledger",
        title="Key pool and quota ledger",
        goal="Track per-key quota windows, park exhausted keys with a reset time, and select keys by remaining quota then latency.",
        deps=[30, 32],
        est="90-180 min",
        skills=[
            ("llm-routing", "ledger semantics: windows, unknown windows, reset detection"),
            ("testing", "window mathematics and parking/resume tests"),
        ],
        deliverables=[
            "`routing/QuotaLedger.kt` (daily, hourly, monthly, unknown windows)",
            "`routing/KeySelector.kt` with the documented ordering rule",
        ],
        steps=[
            "Model a window as `{type, start, limit, used, reset_at}`; treat `unknown` as learn-on-the-fly.",
            "Park rather than delete an exhausted key; a parked key is skipped and shown with its reset time.",
            "Order selection by remaining quota, then latency, then oldest last-use.",
            "Persist the ledger so a restart does not forget today's consumption.",
        ],
        accept=[
            "An exhausted key is parked with a reset time and skipped by selection (asserted)",
            "After the window resets the key becomes selectable again without a restart",
            "Ledger state survives a restart (asserted with a reload test)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*QuotaLedger*'",
        ],
        state="Quotas are tracked rather than discovered by failure.",
    ),
    Task(
        id=82,
        slug="quota-learning",
        title="Quota learning from `429` and rate-limit headers",
        goal="Learn windows the manifests do not know, from real responses, without ever trusting a guess over evidence.",
        deps=[81, 77],
        est="60-120 min",
        skills=[
            ("llm-routing", "which headers and bodies reliably indicate a limit and a reset"),
            ("testing", "fixtures for three providers' limit dialects"),
        ],
        deliverables=[
            "`routing/QuotaLearner.kt` updating the ledger from responses",
            "Fixtures covering `Retry-After`, `x-ratelimit-*` and body-only limit signals",
        ],
        steps=[
            "Prefer explicit reset timestamps, then relative retry hints, then a conservative default.",
            "Record the evidence that produced each learned value so the dashboard can show where it came from.",
            "Never lower a known limit because a provider was lenient once.",
            "Test with fixtures from at least three different dialects.",
        ],
        accept=[
            "A `429` with `Retry-After` parks the key for that duration and records the evidence",
            "A `429` without headers parks for a conservative default and marks the value as estimated",
            "Learned values persist and are visible in `/v1/usage`",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*QuotaLearner*'",
        ],
        state="The ledger improves from experience and shows its sources.",
    ),
    Task(
        id=83,
        slug="multi-provider-key-chaining",
        title="Multi-provider key chaining",
        goal=(
            "The owner's headline requirement: bind a model to keys from several different providers so an exhausted quota "
            "automatically hands over to the next one."
        ),
        deps=[81, 82, 80],
        est="90-180 min",
        skills=[
            ("llm-routing", "chain semantics: a logical model backed by heterogeneous candidates"),
            ("testing", "end-to-end chain test: first key exhausted → second provider answers"),
        ],
        deliverables=[
            "`routing/KeyChain.kt` — an ordered chain of `(provider, key, model)` with per-link quota and health",
            "UI-facing chain model and validation rules",
        ],
        steps=[
            "Allow a chain to mix providers and model ids, since gateways expose different names for equivalent models.",
            "Evaluate each link's usability before the request (parked key, open breaker, disabled provider).",
            "Fail over within the chain before considering unrelated candidates.",
            "Test a three-link chain where the first two are exhausted and the third answers.",
        ],
        accept=[
            "With two exhausted links the third answers, and the switch is visible in the attempt list",
            "A chain entry pointing at a disabled provider is skipped, not fatal",
            "The chain's behaviour is asserted by an automated test, not only observed by hand",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*KeyChain*'",
        ],
        state="One logical model can be backed by a pool spanning multiple gateways, switching automatically.",
    ),
    Task(
        id=84,
        slug="routing-strategies",
        title="Routing strategies",
        goal="Implement the eight documented strategies and allow them to be composed.",
        deps=[79, 81, 32],
        est="90-180 min",
        skills=[
            ("llm-routing", "ordering rules as pure comparators, composable without ambiguity"),
            ("testing", "one test per strategy plus a composition test"),
        ],
        deliverables=[
            "`routing/strategy/` — free_first, fastest, cheapest, most_quota, healthiest, round_robin, priority, manual",
            "Composition mechanism so a chain of comparators is expressible as data",
        ],
        steps=[
            "Implement each strategy as a comparator over a candidate view (quota, latency, cost, health, tier).",
            "Make composition explicit and ordered; document that the first comparator wins ties.",
            "Default for Tier 1 to `free_first → most_quota → fastest`.",
            "Test each strategy with synthetic candidate sets, including ties.",
        ],
        accept=[
            "Every strategy has a passing test with a deterministic expectation",
            "A composed chain resolves ties by the documented rule",
            "Changing the strategy changes ordering without restarting the server",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Strategy*'",
        ],
        state="Routing behaviour is owner-selectable and each option is proven.",
    ),
    Task(
        id=85,
        slug="health-scoring",
        title="Health scoring and persistence",
        goal="Compute the composite health score documented in docs/04-routing.md and persist it across restarts.",
        deps=[32, 81],
        est="60-120 min",
        skills=[
            ("llm-routing", "weighting, decay and normalisation that behave sensibly at the extremes"),
            ("testing", "boundary tests: all success, all failure, one slow outlier"),
        ],
        deliverables=[
            "`routing/HealthScore.kt` with the documented weights",
            "Persisted scores with a decay policy on load",
        ],
        steps=[
            "Implement the score exactly as documented or update the doc in the same commit — never both drift.",
            "Decay stale penalties so a recovered provider is not permanently punished.",
            "Test the extreme cases so the score cannot exceed its range or divide by zero.",
            "Expose the score components, not only the aggregate.",
        ],
        accept=[
            "Score stays within [0,1] for the boundary inputs (asserted)",
            "A provider recovering after failures returns to a competitive score within the documented decay period",
            "The implementation and docs/04-routing.md agree",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*HealthScore*'",
        ],
        state="Health is a single, documented number that routing and the dashboard both trust.",
    ),
    Task(
        id=86,
        slug="circuit-breaker-retry",
        title="Circuit breaker and retry policy",
        goal="Open a provider after repeated failures, half-open it with a probe, and retry with bounded exponential backoff.",
        deps=[85],
        est="60-120 min",
        skills=[
            ("llm-routing", "breaker states and transitions without flapping"),
            ("testing", "state machine tests including the half-open probe"),
        ],
        deliverables=[
            "`routing/CircuitBreaker.kt` (closed, open, half-open)",
            "Retry policy with jitter, bounded attempts, and no retry on quota or auth errors",
        ],
        steps=[
            "Open after the configured consecutive failures; record the reason and time.",
            "Half-open with one probe after the cooldown; close on success, reopen on failure with a longer cooldown.",
            "Never retry the same key after a quota error; retry transient network errors with jitter.",
            "Expose breaker state in `/v1/providers`.",
        ],
        accept=[
            "A failing provider is skipped after the threshold, without a request to it (asserted by call counting)",
            "A recovered provider is used again after the probe succeeds",
            "No retry happens after `QuotaExceeded` or `AuthError` (asserted)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*CircuitBreaker*'",
        ],
        state="Broken providers stop costing latency and quota.",
    ),
    Task(
        id=87,
        slug="failover-loop",
        title="Failover loop and mid-stream policy",
        goal="Walk the candidate list on failure, and define exactly what happens when a stream dies after the first byte.",
        deps=[84, 86, 68, 71],
        est="90-180 min",
        skills=[
            ("llm-routing", "attempt bookkeeping and the mid-stream decision"),
            ("testing", "failure-injection tests for each failure point: before, during and after the first byte"),
        ],
        deliverables=[
            "`routing/FailoverExecutor.kt`",
            "Documented mid-stream policy: restart once on the next candidate, then surface an error naming all attempts",
        ],
        steps=[
            "Iterate candidates, skipping unusable ones, with retries only where the policy allows.",
            "Before the first byte, failover is invisible to the client.",
            "After the first byte, follow the documented policy and never present a truncated answer as complete.",
            "Record every attempt in the response's `droidroute` object and in the log.",
        ],
        accept=[
            "A failure before the first byte transparently fails over (asserted)",
            "A mid-stream failure restarts once, then returns an error naming every attempt (asserted)",
            "The attempt list is present in the response for a failing chain",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*FailoverExecutor*'",
        ],
        state="Failover is defined precisely, including the hard case, and is provable.",
    ),
    Task(
        id=88,
        slug="hedging-optional",
        title="Optional request hedging",
        goal="Offer the opt-in hedge described in docs/04-routing.md, off by default, because it spends quota twice.",
        deps=[87],
        est="60-120 min",
        skills=[
            ("llm-routing", "cancellation semantics for the losing request"),
            ("testing", "assert exactly one upstream is charged when the hedge wins"),
        ],
        deliverables=[
            "`routing/Hedging.kt` behind a setting (default off)",
            "A clear UI warning that hedging multiplies quota consumption",
        ],
        steps=[
            "Start a second candidate if no first byte arrives within the configured delay.",
            "Cancel the slower request and prove in a test that its usage is not recorded as a completed request.",
            "Never hedge on providers whose quota is nearly exhausted.",
            "Keep the feature off unless the owner enables it.",
        ],
        accept=[
            "With hedging off, exactly one upstream call is made (asserted)",
            "With hedging on, the winner is returned and the loser is cancelled (asserted)",
            "The setting default is off and the warning is shown in the UI",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Hedging*'",
        ],
        state="A latency optimisation exists for the owner to opt into, with its cost stated.",
    ),
    Task(
        id=89,
        slug="routing-explain",
        title="`/v1/routing/explain` and decision logging",
        goal="Answer 'why did it pick that?' for any model, both as an API and as structured log records.",
        deps=[87, 84],
        est="60-120 min",
        skills=[
            ("llm-routing", "explanation content that is actually useful for debugging"),
            ("technical-writing", "document the endpoint honestly, including what it does not reveal"),
        ],
        deliverables=[
            "`/v1/routing/explain?model=…` returning candidates, order, strategy and per-candidate reasons",
            "One structured log record per routing decision",
        ],
        steps=[
            "Explain skipped candidates with the precise reason (parked until, breaker open, disabled, no quota).",
            "Include the strategy chain that produced the order.",
            "Expose the same information used at request time — explanations must not be reconstructed afterwards.",
            "Log the decision with the request id so the two can be joined.",
        ],
        accept=[
            "For a model with three candidates the endpoint names each one and its reason for skipped ones",
            "The explanation matches what the failover loop actually did for a real request",
            "The decision log record contains the request id",
        ],
        verify=[
            "curl -fsS 'http://127.0.0.1:8787/v1/routing/explain?model=my-best'",
        ],
        state="Routing is debuggable without reading code or guessing.",
    ),
    Task(
        id=90,
        slug="routing-test-suite",
        title="Routing test suite with failure injection",
        goal="Consolidate the phase's tests into a fault-injection suite that proves the chain behaves under every failure mode.",
        deps=[79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
        est="80-150 min",
        skills=[
            ("testing", "fault injection matrix, determinism, no flaky timing assertions"),
            ("llm-routing", "identify the scenarios that matter and drop the ones that only look thorough"),
        ],
        deliverables=[
            "`app/src/test/…/routing/` suite with a fake provider harness",
            "A scenario table documented in the suite header: quota, auth, timeout, mid-stream, hedging",
        ],
        steps=[
            "Build a fake provider that can be scripted to fail at a chosen point.",
            "Cover: quota exhaustion mid-chain, auth revocation, timeout before first byte, failure after first byte, breaker flapping.",
            "Ensure the suite is deterministic — no sleeps, use virtual time.",
            "Run it in CI and record the timing.",
        ],
        accept=[
            "Every scenario in the table has a test",
            "The suite is deterministic across 20 consecutive runs",
            "No test depends on a real provider or the network",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*routing*'",
        ],
        state="The routing engine's failure behaviour is proven, which is the point of the whole component.",
    ),
]
