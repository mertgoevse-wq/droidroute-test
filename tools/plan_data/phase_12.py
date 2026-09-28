"""Phase 12 — OmniRoute parity and power features (the v0.2 milestone).

Phase 11 ships v0.1. This phase closes the parity matrix in docs/12-omniroute-parity.md
and delivers the owner's extra wishes: combos, the full strategy set, compression,
cost telemetry, guardrails, memory, A2A, and the tooling wiring for the build agents.
"""

from common import Phase, Task

PHASE = Phase(
    number=12,
    slug="parity-power",
    title="OmniRoute parity & power features",
    summary="Combos, all 19 strategies, fusion/pipeline, compression, cost telemetry, guardrails, memory, A2A, tooling wiring.",
)

TASKS = [
    Task(
        id=148,
        slug="combo-engine",
        title="Combo engine and virtual auto models",
        goal=(
            "Implement combos — named chains of `(provider, model)` steps routed across automatically — and the virtual "
            "models `auto`, `auto/coding`, `auto/fast`, `auto/cheap`, `auto/offline`, `auto/smart`, `auto/lkgp`."
        ),
        deps=[83, 84, 89],
        est="120-240 min",
        skills=[
            ("droidroute-routing", "combo semantics, step ordering, and how a combo differs from an alias"),
            ("droidroute-verification", "virtual-model behaviour tests, including an exhausted-first-step case"),
        ],
        deliverables=[
            "`routing/combo/ComboEngine.kt` and the virtual auto models with their scoring presets",
            "Combo pins at the top of `/v1/models`, and `/v1/routing/explain` shows the resolved step",
        ],
        steps=[
            "Model a combo as ordered steps with per-step strategy overrides and a failure policy.",
            "Implement the virtual presets from documentation, not from intuition: each one names its optimisation target.",
            "Preserve last-known-good stickiness for `auto/lkgp` and keep `auto/chaos` explicitly experimental.",
            "Test: first step exhausted → second answers; all steps failing → one error naming every step.",
        ],
        accept=[
            "A requested virtual model resolves to a documented, explainable step",
            "Quota exhaustion moves the combo to the next step without a client-visible failure",
            "`auto/lkgp` reuses the last successful step when it is healthy (asserted)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Combo*'",
            "curl -fsS 'http://127.0.0.1:8787/v1/routing/explain?model=auto/fast'",
        ],
        state="The flagship OmniRoute capability — combos and zero-config auto models — is available.",
    ),
    Task(
        id=149,
        slug="full-strategy-set",
        title="Complete the 19-strategy set",
        goal=(
            "Add the strategies not covered by T-084 — fill-first, weighted, p2c, least-used, random, strict-random, "
            "reset-window, reset-aware, context-relay, context-optimized, cache-optimized — and document every one."
        ),
        deps=[148],
        est="120-240 min",
        skills=[
            ("droidroute-routing", "comparators over the candidate view; keep them pure and composable"),
            ("droidroute-verification", "deterministic expectation per strategy, including ties and single-candidate cases"),
        ],
        deliverables=[
            "`routing/strategy/` completed to 19 strategies",
            "`docs/04-routing.md` table matching the code exactly",
        ],
        steps=[
            "Implement each remaining strategy as a pure comparator over quota, latency, cost, health, reset time and context fit.",
            "For randomised ones (random, strict-random, p2c, weighted), seed the generator so tests are deterministic.",
            "Implement context-relay honestly: it hands off context, so state clearly what is preserved across the handoff.",
            "Extend the strategy tests to cover all 19 with ties and a single candidate.",
        ],
        accept=[
            "All 19 strategies exist, each with a deterministic test",
            "`docs/04-routing.md` lists exactly the implemented set (checked by a test or the doc table)",
            "Randomised strategies are reproducible under a fixed seed",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Strategy*'",
        ],
        state="Strategy parity with OmniRoute is complete and documented, not approximated.",
    ),
    Task(
        id=150,
        slug="fusion-and-pipeline",
        title="Fusion and pipeline strategies",
        goal="Implement the two multi-model strategies: fusion (panel plus judge) and pipeline (each step feeds the next).",
        deps=[149],
        est="120-240 min",
        skills=[
            ("droidroute-routing", "fan-out, cancellation and the judge protocol"),
            ("droidroute-verification", "cost assertions: exactly N calls for a panel of N, and cancellation on partial failure"),
        ],
        deliverables=[
            "`routing/strategy/Fusion.kt` and `Pipeline.kt`",
            "Usage accounting that records every panel member's cost separately",
        ],
        steps=[
            "Fan out to the panel with a shared deadline; cancel stragglers rather than waiting indefinitely.",
            "Send the panel answers to a judge model with an explicit, documented prompt contract.",
            "For pipeline, pass each step's output as the next step's input and record intermediate artefacts in the log.",
            "Make both strategies refuse to run silently expensive combinations without an explicit opt-in.",
        ],
        accept=[
            "Fusion calls exactly the panel size plus one judge (asserted by call counting)",
            "A failed panel member does not fail the whole fusion request unless all fail",
            "Pipeline passes output forward correctly, and every step's usage is recorded",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Fusion*' --tests '*Pipeline*'",
        ],
        state="Multi-model routing is available with explicit cost accounting.",
    ),
    Task(
        id=151,
        slug="auto-scoring-engine",
        title="Multi-factor auto scoring engine",
        goal="Implement the live scoring engine behind the virtual `auto` models: weighted factors over health, quota, cost, latency, capability fit and session availability.",
        deps=[148, 85, 82],
        est="120-240 min",
        skills=[
            ("droidroute-routing", "factor weighting, normalisation and stability of the score"),
            ("android-profiler", "scoring must be cheap enough to run per request on a phone"),
        ],
        deliverables=[
            "`routing/auto/AutoScorer.kt` with an explicit, documented factor list and weights",
            "A per-request log line showing the factor contributions for the chosen candidate",
        ],
        steps=[
            "Define the factors and their weights in one place; the docs and code must agree in the same commit.",
            "Normalise each factor into [0,1] and reject inputs that would divide by zero or exceed the range.",
            "Cache the score briefly so a burst of requests does not recompute it per request.",
            "Expose the factor breakdown through `/v1/routing/explain`, because an unexplainable score is a debugging trap.",
        ],
        accept=[
            "The score stays in range for boundary inputs (asserted)",
            "Each factor's contribution is visible in the explain output",
            "Scoring a candidate set of 50 costs under 5 ms (measured)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*AutoScorer*'",
        ],
        state="The `auto` models make decisions that a human can inspect and argue with.",
    ),
    Task(
        id=152,
        slug="admission-control",
        title="Adaptive admission, overload protection and rolling leases",
        goal=(
            "Queue heavyweight requests instead of rejecting them, enforce per-connection rolling RPM leases, and support "
            "a reverse-proxy base path."
        ),
        deps=[87],
        est="120-240 min",
        skills=[
            ("ktor-server", "admission queueing, backpressure and bounded waiting"),
            ("droidroute-verification", "overload tests: burst above the limit, queue drain, lease rollover"),
        ],
        deliverables=[
            "`server/Admission.kt` with a bounded queue, explicit wait policy and a truthful 429 only when the queue is full",
            "Rolling RPM leases per client key, enforced with per-request atomic accounting",
            "Configurable base path for reverse-proxy deployments",
        ],
        steps=[
            "Model admission as a bounded queue with a documented maximum wait; never wait unbounded.",
            "Implement the rolling lease so a burst is spread rather than rejected, and log every throttled decision.",
            "Honour a configured base path on every route and in generated snippets.",
            "Test a burst above the limit and assert that queued requests complete rather than fail.",
        ],
        accept=[
            "A burst above the RPM limit drains through the queue instead of 503-ing",
            "The queue has a hard bound and a 429 that names the limit when exceeded",
            "The base path works for all four protocol surfaces",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Admission*'",
        ],
        state="The gateway stays useful under load instead of failing loudly at the first spike.",
    ),
    Task(
        id=153,
        slug="token-compression",
        title="Token compression engines",
        goal=(
            "Reduce prompt cost measurably: lossless-first filters for code and logs, optional lossy packs, an inflation "
            "guard, per-request opt-out, and a reported savings number."
        ),
        deps=[68, 81],
        est="120-240 min",
        skills=[
            ("droidroute-routing", "where compression may be applied without changing the answer's meaning"),
            ("droidroute-verification", "savings measurement plus a fidelity test proving no semantic change for the lossless path"),
        ],
        deliverables=[
            "`protocol/compression/` engine set with an explicit engine list and per-engine enable flags",
            "`X-DroidRoute-Tokens-Saved` style reporting and an inflation guard",
        ],
        steps=[
            "Implement lossless filters first (whitespace, duplicate log lines, repeated boilerplate) — they are safe and provable.",
            "Add lossy packs behind explicit opt-in with a fidelity gate: if the check fails, send the original.",
            "Never compress tool schemas or system instructions in a way that changes behaviour; document the exclusions.",
            "Measure savings on a real request and record the number in the task log.",
        ],
        accept=[
            "Lossless compression is provably reversible (round-trip test)",
            "The inflation guard prevents a compressed prompt from being larger than the original",
            "Savings are reported per request and measured in the task log",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Compression*'",
        ],
        state="Prompt cost drops measurably without surprising changes to answers.",
    ),
    Task(
        id=154,
        slug="prompt-cache-pinning",
        title="Prompt-cache pinning and cache-hit telemetry",
        goal="Pin reusable prompt prefixes to the same account so provider-side caches hit, and report the resulting savings.",
        deps=[149, 81],
        est="90-180 min",
        skills=[
            ("droidroute-routing", "prefix stability as a routing constraint, and when it must yield to availability"),
            ("droidroute-verification", "cache-hit accounting tests, including the case where the pinned key is parked"),
        ],
        deliverables=[
            "`routing/CachePinner.kt` with a documented precedence against quota and health",
            "Cache-hit and savings fields in the usage record and the response headers",
        ],
        steps=[
            "Hash the reusable prefix and remember which key served it successfully.",
            "Prefer that key while it is usable; fall back to availability rules the moment it is not.",
            "Record cache-hit savings separately from token savings so the numbers are not conflated.",
            "Expose the pin state in the explain output.",
        ],
        accept=[
            "Repeated requests with the same prefix prefer the same key (asserted)",
            "A parked pinned key falls back without failing the request",
            "Cache-hit savings appear in usage and headers",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*CachePinner*'",
        ],
        state="Provider-side caching is actively used instead of accidentally missed.",
    ),
    Task(
        id=155,
        slug="cost-telemetry",
        title="Cost telemetry headers and per-key USD budgets",
        goal="Report tokens, cost and savings on every response, and let the owner cap spend per client key and per provider.",
        deps=[95, 81, 17],
        est="90-180 min",
        skills=[
            ("droidroute-routing", "cost attribution: which key, which provider, which price list"),
            ("droidroute-verification", "budget enforcement tests, including the hard stop and the recorded reason"),
        ],
        deliverables=[
            "`X-DroidRoute-*` response headers: tokens in/out, cost estimate, cache savings, provider, attempt count",
            "Per-key and per-provider USD budgets with a hard stop and a clear error body",
        ],
        steps=[
            "Derive cost from the usage record and the manifest price list; mark unknown pricing as unknown rather than guessing.",
            "Enforce budgets at admission time so a request that would exceed the cap is refused with a reason.",
            "Keep subscription providers at $0 in cost analytics while still showing the notional value.",
            "Test: a budget of $0.00 blocks paid providers but not free ones.",
        ],
        accept=[
            "Headers carry the documented fields on every successful response",
            "A key over budget is refused with a message naming the budget and the reset",
            "Unknown pricing is labelled unknown, never estimated silently",
        ],
        verify=[
            "curl -fsS -D - -o /dev/null http://127.0.0.1:8787/health | grep -i droidroute",
            "./gradlew :app:testDebugUnitTest --tests '*Budget*'",
        ],
        state="The owner can see and cap what the gateway spends, per key and per provider.",
    ),
    Task(
        id=156,
        slug="quota-share",
        title="Quota-Share across pooled keys",
        goal="Split one shared account's quota fairly across pooled keys, work-conserving, so idle slices are lent out instead of wasted.",
        deps=[81, 83],
        est="120-240 min",
        skills=[
            ("droidroute-routing", "fair-share scheduling with lending, and the guarantee that lending never strands a slice"),
            ("droidroute-verification", "fairness assertions under skew: one heavy consumer, several light ones, all bounded"),
        ],
        deliverables=[
            "`routing/QuotaShare.kt` with a documented lending rule",
            "Explain output showing each key's slice, usage and lent amount",
        ],
        steps=[
            "Define slices per key over the shared window and track usage against the slice, not only the account total.",
            "Lend unused slice capacity to the key that needs it, and reclaim it when the owner returns.",
            "Never exceed the account's real limit while lending — the shared cap is a hard ceiling.",
            "Test a skewed load and assert that no key is starved and no window is overspent.",
        ],
        accept=[
            "Skewed load does not starve any key (asserted)",
            "The shared account cap is never exceeded (asserted)",
            "The lending state is visible per key",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*QuotaShare*'",
        ],
        state="Shared accounts are used efficiently without one consumer eating the pool.",
    ),
    Task(
        id=157,
        slug="memory-subsystem",
        title="Memory subsystem (opt-in, local)",
        goal="Optional project memory: store reusable facts and decisions locally, retrieve them into prompts, and allow a per-request off switch.",
        deps=[66, 6],
        est="120-240 min",
        skills=[
            ("ai-governors", "memory is user data: consent, transparency, deletion and control"),
            ("droidroute-verification", "isolation tests: memory never leaks between client keys, and off means off"),
        ],
        deliverables=[
            "`memory/` store with an on/off setting (default off), per-request opt-out and a delete-everything action",
            "Documented retrieval rule stating exactly what may be injected and when",
        ],
        steps=[
            "Store entries locally with a type (fact, preference, decision) and a decay policy.",
            "Inject only when the request opts in and never silently for unrelated clients.",
            "Implement and test the off switch as a hard gate, not a default-value convention.",
            "Document the privacy boundary in docs/05-security.md and the German glossary.",
        ],
        accept=[
            "Memory is off by default and a request with the opt-out flag never receives injected content (asserted)",
            "Delete-everything removes all entries and is logged",
            "The retrieval rule in the docs matches the implementation",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Memory*'",
        ],
        state="Memory exists as a controlled feature with a stated boundary, not an invisible side channel.",
    ),
    Task(
        id=158,
        slug="prompt-injection-guard",
        title="Prompt-injection guard",
        goal="Screen inbound content for instruction-injection patterns on every LLM route, without pretending the heuristics are perfect.",
        deps=[66, 77],
        est="90-180 min",
        skills=[
            ("ai-governors", "how to warn and block proportionately instead of silently mangling user content"),
            ("droidroute-verification", "a red-team corpus: tool-result injection, role confusion, delimiter escape"),
        ],
        deliverables=[
            "`protocol/guard/InjectionGuard.kt` with a documented pattern set and an action per severity",
            "A red-team test corpus stored as fixtures and run in the suite",
        ],
        steps=[
            "Detect patterns in untrusted positions (tool results, retrieved documents) rather than in the owner's own text.",
            "Choose per severity: annotate, warn in the response, or refuse — never silently rewrite the content.",
            "Document the limits honestly: this reduces risk, it does not eliminate it.",
            "Run the red-team fixtures and record the detection rate.",
        ],
        accept=[
            "Every fixture in the red-team corpus produces the documented action",
            "Owner-authored text is not modified (asserted with a control fixture)",
            "The scope and limits are documented without overstating the protection",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*InjectionGuard*'",
        ],
        state="Injection attempts in untrusted content are handled proportionately and measurably.",
    ),
    Task(
        id=159,
        slug="credential-masking-guardrail",
        title="Credential-masking guardrail",
        goal="Redact secrets that would otherwise flow outwards in prompts or back in responses, using the same rules as the repository's own redactor.",
        deps=[8, 66],
        est="90-180 min",
        skills=[
            ("android-intent-security", "treat every outbound path as hostile until proven filtered"),
            ("droidroute-verification", "canary tests in both directions plus a false-positive check on ordinary code"),
        ],
        deliverables=[
            "`protocol/guard/CredentialMasker.kt` shared with the logging redactor's pattern set",
            "A documented note about false positives and how to see what was masked",
        ],
        steps=[
            "Reuse one pattern source for log redaction and outbound masking so the two cannot drift.",
            "Mask in both directions and log the occurrence by type only, never the value.",
            "Test false positives against real code samples: masking must not mangle ordinary identifiers.",
            "Document the feature's off switch and its default.",
        ],
        accept=[
            "A canary key is masked in outbound content and in inbound content (asserted)",
            "Ordinary code samples pass through unchanged (asserted)",
            "The masking event is logged by type, never by value",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*CredentialMasker*'",
        ],
        state="A leaked key in a prompt does not become a leaked key in a response, and the rule has one source.",
    ),
    Task(
        id=160,
        slug="modality-bridge",
        title="Modality bridge (vision, audio, video)",
        goal="Route non-text requests to a capable model automatically, converting between modality shapes where the provider differs.",
        deps=[75, 73, 26],
        est="120-240 min",
        skills=[
            ("droidroute-routing", "capability-driven candidate selection for non-text traffic"),
            ("droidroute-verification", "conversion round trips and the incapable-provider error path"),
        ],
        deliverables=[
            "`protocol/bridge/ModalityBridge.kt` for vision, audio and video inputs",
            "Capability declarations extended with modality granularity per model",
        ],
        steps=[
            "Detect the modality of each content part and require the candidate to declare it.",
            "Convert between dialect shapes (base64 inline data, URLs, file references) without corrupting bytes.",
            "Reject unsupported combinations with a capability error naming what is missing.",
            "Test each modality against a capable and an incapable provider.",
        ],
        accept=[
            "An image, an audio clip and a video reference each route to a capable model or fail with a precise reason",
            "Binary payloads survive conversion (checksum compared in a test)",
            "Capability declarations are per model, not per provider",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ModalityBridge*'",
        ],
        state="Non-text requests are first-class and routed by capability rather than by guessing.",
    ),
    Task(
        id=161,
        slug="ocr-audio-translation-websearch",
        title="OCR, audio translation and web-search fallback",
        goal="Complete the media surface: document OCR, speech translation, and an optional last-resort web search that does not depend on one provider.",
        deps=[75, 160],
        est="120-240 min",
        skills=[
            ("droidroute-provider-manifest", "add the capable providers with confirmed endpoints"),
            ("droidroute-verification", "each endpoint works or reports a precise unsupported error"),
        ],
        deliverables=[
            "`/v1/ocr`, `/v1/audio/translations`, and a web-search fallback used only when no search provider is enabled",
            "Manifest entries for the providers that serve each capability",
        ],
        steps=[
            "Implement OCR against capable providers, preserving page and layout metadata where the provider returns it.",
            "Implement audio translation as transcription plus translation with the two steps visible in the log.",
            "Implement the search fallback with explicit rate limiting and a clear statement of what it sends where.",
            "Document each endpoint with an example that was actually executed.",
        ],
        accept=[
            "Each endpoint returns a real result or a precise unsupported error",
            "The search fallback is opt-in and rate-limited",
            "Documented examples match captured output",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Ocr*' --tests '*Translation*'",
        ],
        state="The media surface is complete enough that a client does not need a second gateway.",
    ),
    Task(
        id=162,
        slug="video-generation",
        title="Video generation endpoint",
        goal="Add a video generation surface with provider-specific mapping and an honest handling of long-running jobs.",
        deps=[160, 75],
        est="120-240 min",
        skills=[
            ("droidroute-provider-manifest", "which providers offer video and how their job model works"),
            ("droidroute-verification", "job polling, timeout and cancellation behaviour"),
        ],
        deliverables=[
            "`/v1/videos/generations` with a documented job lifecycle",
            "Per-provider mapping for asynchronous jobs where the provider needs polling",
        ],
        steps=[
            "Model the job lifecycle explicitly: submitted, running, ready, failed, cancelled.",
            "Never hold a request open indefinitely; return a job handle and poll on demand.",
            "Handle provider quotas and cost differences, and report them before submission.",
            "Test with a stub provider that exercises both the ready and the failed path.",
        ],
        accept=[
            "A job can be submitted, polled and fetched (or the provider gap is logged with evidence)",
            "A failed job surfaces the provider's reason",
            "No request blocks for the full generation time",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*VideoJob*'",
        ],
        state="Video generation is available without holding HTTP connections open for minutes.",
    ),
    Task(
        id=163,
        slug="a2a-server",
        title="A2A server for agent delegation",
        goal="Let other agents delegate to the DroidRoute fleet: advertise capabilities on an agent card and accept inbound A2A tasks.",
        deps=[120, 151],
        est="120-240 min",
        skills=[
            ("ai-trust-builders", "delegation is a trust boundary: what is advertised, what is accepted, what is refused"),
            ("ai-governors", "inbound autonomy needs limits and an audit trail the owner can inspect"),
        ],
        deliverables=[
            "`server/a2a/AgentCard.kt` and the inbound task endpoint",
            "An audit record per delegated task, naming the requester and the outcome",
        ],
        steps=[
            "Publish an agent card listing the capabilities DroidRoute will actually perform, with no overstatement.",
            "Accept inbound tasks only from configured clients and inside the budget rules from T-155.",
            "Record every delegated task in the log with requester, cost and outcome.",
            "Refuse anything outside the advertised capability set with a specific error.",
        ],
        accept=[
            "The agent card matches the implemented capabilities",
            "An unconfigured requester is rejected and the attempt is logged",
            "Every accepted delegation produces an audit record",
        ],
        verify=[
            "curl -fsS http://127.0.0.1:8787/.well-known/agent-card",
            "./gradlew :app:testDebugUnitTest --tests '*AgentCard*'",
        ],
        state="DroidRoute can act as a controlled delegate inside an agent fleet.",
    ),
    Task(
        id=164,
        slug="models-ordering-and-free-tier-view",
        title="Canonical model ordering and free-tier catalogue view",
        goal="Serve `/v1/models` in a stable, provider-grouped order with combos pinned first, and show the free-tier catalogue with real reset semantics.",
        deps=[69, 82, 95],
        est="90-180 min",
        skills=[
            ("droidroute-routing", "stable ordering that does not reshuffle per request"),
            ("droidroute-compose-ui", "a catalogue screen that states what is free and when it resets"),
        ],
        deliverables=[
            "Deterministic `/v1/models` ordering: combos, then tier 1 grouped by provider, then the rest",
            "Free-tier screen: provider, models, window, reset time, remaining quota or an honest unknown",
        ],
        steps=[
            "Sort deterministically and test that two consecutive calls return identical order.",
            "Show reset times in local time and mark learned windows as learned rather than published.",
            "Never present an unknown remaining quota as a number.",
            "Add the screen to the dashboard navigation.",
        ],
        accept=[
            "Model ordering is stable across calls (asserted)",
            "The free-tier screen matches `/v1/usage` for the same window",
            "Unknown values are labelled unknown",
        ],
        verify=[
            "curl -fsS http://127.0.0.1:8787/v1/models | head -30",
            "./gradlew :app:testDebugUnitTest --tests '*ModelOrder*'",
        ],
        state="Clients see a stable catalogue and the owner sees the real free-tier picture.",
    ),
    Task(
        id=165,
        slug="cli-setup-and-remote-mode",
        title="CLI setup helpers and remote mode with scoped tokens",
        goal="Make connecting a client one command, and make a remote DroidRoute instance reachable with narrow tokens instead of full access.",
        deps=[16, 21, 22],
        est="90-180 min",
        skills=[
            ("droidroute-provider-manifest", "the connection details each client actually needs"),
            ("android-intent-security", "scoped tokens must be strictly narrower than the main key"),
        ],
        deliverables=[
            "`scripts/setup-client.sh` supporting Claude Code, Freebuff/Codex-style, Gemini CLI and generic OpenAI clients",
            "Scoped tokens: read-only, model-restricted, budget-capped, expiring",
        ],
        steps=[
            "Generate the exact environment exports per client from the live configuration, never from constants.",
            "Implement scoped tokens with a documented capability list and a hard expiry.",
            "Test that a read-only token cannot perform an admin action or call a model outside its list.",
            "Document the remote-mode flow for the tailnet and tunnel cases from docs/11-tbc-resolutions.md.",
        ],
        accept=[
            "One command configures each supported client and the result works",
            "A scoped token is refused outside its scope (asserted per scope type)",
            "Scoped tokens expire and cannot be extended by the holder",
        ],
        verify=[
            "bash scripts/setup-client.sh --client claude-code --dry-run",
            "./gradlew :app:testDebugUnitTest --tests '*ScopedToken*'",
        ],
        state="Connecting a client is one command, and remote access never needs the master key.",
    ),
    Task(
        id=166,
        slug="build-agent-tooling-wiring",
        title="Build-agent tooling wiring (skills, plugins, MCP)",
        goal=(
            "Keep the build agents fully wired: the generated tooling inventory stays current, project skills and subagents "
            "cover every phase, MCP servers are used when present, and CI fails when the inventory is stale."
        ),
        deps=[131],
        est="60-120 min",
        skills=[
            ("droidroute-skill-scout", "verify the inventory matches the installed libraries and fill gaps"),
            ("karpathy-audit", "audit the instruction files for contradictions and dead weight after the growth"),
        ],
        deliverables=[
            "`status/TOOLING.md` regenerated, with `--check` wired into CI and `--check-fresh` documented for local use",
            "Project skills and subagents reviewed against the 13 phases; gaps filled or explicitly noted",
        ],
        steps=[
            "Run `python3 scripts/discover_tooling.py` and commit the refreshed inventory.",
            "Confirm the CI step validates structure (`--check`) and that freshness is a local duty (`--check-fresh`) — a runner without agent configuration must not fail the build for a reason it cannot control.",
            "Walk each phase in `handbooks/03-skills-catalog.md` and confirm a real skill exists for its primary and verification stream.",
            "Verify the docs point at the inventory rather than repeating skill names that may drift.",
        ],
        accept=[
            "CI fails when `status/TOOLING.md` is malformed, and passes on a runner with no agent configuration (proven once for each, then reverted)",
            "`--check-fresh` fails on the device when the inventory is out of date (proven once, then reverted)",
            "Every phase names skills that exist in the inventory",
        ],
        verify=[
            "python3 scripts/discover_tooling.py --check",
            "python3 scripts/discover_tooling.py --check-fresh",
            "python3 tools/check_links.py",
        ],
        state="The build agents can always see, and are required to use, the skills and tools that exist.",
    ),
]
