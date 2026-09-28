"""Phase 11 — Delivery: prove it, harden it, ship it, and leave the repository operable."""

from common import Phase, Task

PHASE = Phase(
    number=11,
    slug="delivery",
    title="Delivery",
    summary="Performance and security hardening, the acceptance run, the release pipeline and owner documentation.",
)

TASKS = [
    Task(
        id=136,
        slug="performance-pass",
        title="Performance pass",
        goal="Measure and improve the three costs that matter on a phone: idle battery, memory ceiling and cold start.",
        deps=[109, 94, 106],
        est="90-180 min",
        skills=[
            ("performance-android", "measure before changing anything; keep the before/after numbers"),
            ("kotlin-core", "reduce allocations and recompositions in the hot paths found"),
        ],
        deliverables=[
            "A before/after measurement table recorded in status/components/core-server.md",
            "Fixes for the worst offenders, each with its own measurement",
        ],
        steps=[
            "Measure idle drain with one connected agent and no traffic over an hour.",
            "Measure peak memory with a local model loaded and with a long stream in flight.",
            "Measure cold start to a listening socket.",
            "Fix the largest cost first and re-measure; do not batch unfocused changes.",
        ],
        accept=[
            "All three metrics are recorded with real numbers and the measurement method",
            "At least the largest measured cost is improved, with the delta stated",
            "No optimisation is claimed without a measurement",
        ],
        verify=[
            "adb shell dumpsys batterystats --charged com.droidroute.app | head -20",
            "adb shell dumpsys meminfo com.droidroute.app | head -20",
        ],
        state="Performance claims are numbers in the repository, not adjectives in a commit message.",
    ),
    Task(
        id=137,
        slug="security-review",
        title="Security review against docs/05-security.md",
        goal="Verify every security claim in the documentation is true in the code, and fix what is not.",
        deps=[99, 120, 112],
        est="90-180 min",
        skills=[
            ("security-audit", "adversarial review: assume each control is broken until proven otherwise"),
            ("testing", "turn each verified control into an automated assertion"),
        ],
        deliverables=[
            "A control-by-control review table committed to the component status file",
            "Automated assertions for the redaction canary, auth floor, key masking and admin auth",
        ],
        steps=[
            "Walk each claim in docs/05-security.md and find its enforcing code path.",
            "Attempt to break: unauthenticated admin call, non-local bind without a key, key leak into a log, key in an exported file.",
            "Where a claim is not enforced, either enforce it or correct the documentation — never leave a false claim.",
            "Add a test per control so a regression is caught.",
        ],
        accept=[
            "Every documented control has an enforcing test",
            "Each attempted break failed, or was fixed in this task",
            "No documentation claim is left unverified",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Security*'",
            "scripts/preflight-secrets.sh",
        ],
        state="The security documentation is verified against behaviour, control by control.",
    ),
    Task(
        id=138,
        slug="dependency-licence-review",
        title="Dependency and licence review",
        goal="Know exactly what ships, under which licence, and record any obligation the owner takes on.",
        deps=[136, 137],
        est="60-120 min",
        skills=[
            ("security-audit", "check for known-vulnerable versions before release"),
            ("technical-writing", "a licence inventory that a non-lawyer can read"),
        ],
        deliverables=[
            "A dependency inventory with versions, licences and purpose",
            "A decision entry recording anything with an obligation (attribution, copyleft, commercial limits)",
        ],
        steps=[
            "List runtime dependencies from the Gradle report and record each licence.",
            "Check each against its project's current licence text, not against a memory of it.",
            "Record any obligation that affects how the owner may distribute the APK.",
            "Remove any dependency that is unused — an unused dependency is pure liability.",
        ],
        accept=[
            "Every runtime dependency has a recorded licence and purpose",
            "Obligations are written down in status/DECISIONS.md",
            "No unused dependency remains",
        ],
        verify=[
            "./gradlew :app:dependencies --configuration releaseRuntimeClasspath | head -40",
        ],
        state="What ships is known, and its obligations are recorded before release.",
    ),
    Task(
        id=139,
        slug="test-suite-consolidation",
        title="Test suite consolidation and coverage review",
        goal="One coherent suite: fast unit tests, meaningful instrumented tests, no redundant or flaky ones.",
        deps=[136, 138],
        est="80-150 min",
        skills=[
            ("testing", "remove duplicates, fix flakiness, keep runtime honest"),
            ("technical-writing", "document what is tested and, more usefully, what is not"),
        ],
        deliverables=[
            "A consolidated suite with recorded runtime",
            "A coverage note stating known gaps in plain terms",
        ],
        steps=[
            "Run the full suite repeatedly to surface flakiness; fix or delete flaky tests rather than retrying.",
            "Remove tests whose assertions could not fail.",
            "Record the run time and the intentional gaps.",
            "Make sure CI runs the same suite the developer runs locally.",
        ],
        accept=[
            "The full suite passes ten consecutive runs",
            "Runtime is recorded and reasonable for CI",
            "Gaps are documented honestly",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --rerun-tasks",
        ],
        state="The suite is trustworthy, which means a failure now means something.",
    ),
    Task(
        id=140,
        slug="acceptance-run-1",
        title="Acceptance run A1–A3 (server, agents, providers)",
        goal="Prove criteria A1 to A3 from docs/10-acceptance.md with raw evidence.",
        deps=[139, 21, 96],
        est="90-180 min",
        skills=[
            ("testing", "run each criterion exactly as written and capture raw output"),
            ("technical-writing", "record evidence so a third party can reproduce it"),
        ],
        deliverables=[
            "Evidence entries for A1, A2 and A3 in logs/tasks/T-140.log plus the acceptance document ticks",
        ],
        steps=[
            "A1: change the port, restart, confirm `/health` on the new port.",
            "A2: point Claude Code and Freebuff at the server and complete one real prompt each.",
            "A3: list the provider coverage, add a custom provider through the form, and use one-click connect.",
            "Capture the raw command output for each, not a summary of it.",
        ],
        accept=[
            "A1, A2 and A3 are ticked with commands and raw output in the log",
            "Anything that failed is recorded as failed with the reason, not skipped",
            "A3 names exactly which providers the owner's credentials could validate",
        ],
        verify=[
            "curl -fsS http://127.0.0.1:8787/health",
            "tail -n 40 logs/tasks/T-140.log",
        ],
        state="The first three acceptance criteria have reproducible evidence.",
    ),
    Task(
        id=141,
        slug="acceptance-run-2",
        title="Acceptance run A4–A6 (accounts, failover, dashboard)",
        goal="Prove criteria A4 to A6, including a real failover and a real key rotation.",
        deps=[140],
        est="90-180 min",
        skills=[
            ("testing", "inject a 401 and an exhausted quota without breaking the working setup"),
            ("llm-routing", "interpret the attempt list and confirm it explains the observed behaviour"),
        ],
        deliverables=[
            "Evidence entries for A4, A5 and A6",
        ],
        steps=[
            "A4: connect the Google account and run a Perplexity search returning citations.",
            "A5: revoke a key temporarily and confirm the request still succeeds through the next candidate.",
            "A6: compare the dashboard numbers with `/v1/usage` for the same window.",
            "Record the attempt list from a failed-then-succeeded request.",
        ],
        accept=[
            "A4, A5 and A6 are ticked with evidence",
            "The failover evidence shows the specific next candidate that answered",
            "Dashboard figures match the API exactly",
        ],
        verify=[
            "curl -fsS -X POST http://127.0.0.1:8787/v1/search -d '{\"query\":\"test\"}'",
            "curl -fsS http://127.0.0.1:8787/v1/usage",
        ],
        state="Failover and account connectivity are proven, which is the core of the product's value.",
    ),
    Task(
        id=142,
        slug="acceptance-run-3",
        title="Acceptance run A7–A9 (local models, MCP, repository)",
        goal="Prove criteria A7 to A9: local inference, MCP federation, and the repository's own integrity.",
        deps=[141],
        est="90-180 min",
        skills=[
            ("testing", "run the criteria literally, including the memory-warning case"),
            ("mcp-protocol", "verify the discovered server list against the host's own configuration"),
        ],
        deliverables=[
            "Evidence entries for A7, A8 and A9",
        ],
        steps=[
            "A7: load a model at or under 4 GB, get a completion, then attempt an oversized model and capture the warning.",
            "A8: compare `/mcp/servers` with the host configuration and call one tool end to end.",
            "A9: confirm the repository is private, has ≥135 task files, and one commit per completed task.",
            "Attach the screenshots A7 and A3 require.",
        ],
        accept=[
            "A7, A8 and A9 are ticked with evidence",
            "The MCP list matches the host configuration entry by entry",
            "The repository checks are run as commands, not asserted from memory",
        ],
        verify=[
            "gh repo view --json isPrivate,name",
            "find plan -name 'T-*.md' | wc -l",
            "git log --oneline | head -20",
        ],
        state="Local models, MCP and repository integrity are proven together.",
    ),
    Task(
        id=143,
        slug="acceptance-run-4",
        title="Acceptance run A10–A12 (handover, build, hygiene)",
        goal="Prove the last three criteria, including that a different model can take over from the repository alone.",
        deps=[142, 133],
        est="90-180 min",
        skills=[
            ("testing", "the takeover drill must be genuinely cold, with no session memory"),
            ("ci-cd-github-actions", "verify the artifact path end to end from the workflow run"),
        ],
        deliverables=[
            "Evidence entries for A10, A11 and A12",
        ],
        steps=[
            "A10: in a fresh session, complete one task end to end using only repository artefacts.",
            "A11: download the CI-built APK, install it on the device, and run the local build once as the fallback proof.",
            "A12: run the secrets preflight, confirm the cleanup workflow ran, and check every README link.",
            "Record all of it in the task log.",
        ],
        accept=[
            "A10, A11 and A12 are ticked with evidence",
            "The takeover was done without consulting any chat history",
            "The APK installed from CI runs the same build sha that `/health` reports",
        ],
        verify=[
            "gh run list --workflow=build-apk.yml --limit 3",
            "python3 tools/check_links.py",
            "scripts/preflight-secrets.sh",
        ],
        state="All twelve acceptance criteria are satisfied with evidence.",
    ),
    Task(
        id=144,
        slug="release-pipeline",
        title="Release pipeline and first tagged release",
        goal="Cut the first real release: signing configured, workflow verified, artifacts and checksums published.",
        deps=[143],
        est="60-120 min",
        skills=[
            ("ci-cd-github-actions", "tag → build → sign → release, with a rollback path"),
            ("security-audit", "confirm signing material is only in repository secrets and never logged"),
        ],
        deliverables=[
            "A `v0.1.0` release with APK and SHA256SUMS",
            "CHANGELOG entry for the release",
        ],
        steps=[
            "Confirm the signing secrets exist and that the workflow refuses to build without them.",
            "Tag the release through `scripts/step-commit.sh --tag`.",
            "Verify the published artifact's checksum against a local download.",
            "Record how to roll back to the previous APK.",
        ],
        accept=[
            "The release exists with an installable signed APK and a checksum file",
            "The checksum of the downloaded file matches",
            "No signing material appears in any log or artifact",
        ],
        verify=[
            "gh release view v0.1.0",
            "gh release download v0.1.0 --pattern '*.apk' -D /tmp/droidroute-release && sha256sum /tmp/droidroute-release/*.apk",
        ],
        state="DroidRoute has shipped a verifiable release, built by CI from a tagged commit.",
    ),
    Task(
        id=145,
        slug="owner-documentation",
        title="Owner documentation in German",
        goal="Document for the owner, in plain German, how to install, configure and use the app day to day.",
        deps=[144],
        est="80-150 min",
        skills=[
            ("technical-writing", "plain German, technical terms kept and explained"),
            ("technical-writing", "verify every step was actually performed at least once"),
        ],
        deliverables=[
            "`docs/owner-guide-de.md`: install, first run, connect Claude Code and Freebuff, add a provider, local models, MCP, troubleshooting",
            "Glossary additions for any new term",
        ],
        steps=[
            "Write for a reader who has the app installed but has forgotten the setup.",
            "Include the exact commands with the real default port, and the German explanation of what each does.",
            "Add a troubleshooting section from real failures encountered during the build.",
            "Keep every step tested: mark any untested step as untested rather than implying it was verified.",
        ],
        accept=[
            "Every step was executed at least once and is described accurately",
            "The German text uses plain words with technical terms explained",
            "The troubleshooting section lists failures that actually occurred",
        ],
        verify=[
            "python3 tools/check_links.py",
        ],
        state="The owner can operate DroidRoute without reading the source or asking an agent.",
    ),
    Task(
        id=146,
        slug="repository-beauty-pass",
        title="Repository presentation pass",
        goal="Make the repository welcoming and accurate for a human: README, description, topics, templates, badges that reflect reality.",
        deps=[145],
        est="60-120 min",
        skills=[
            ("technical-writing", "remove any claim that is not true; no marketing filler"),
            ("ci-cd-github-actions", "confirm badges point at workflows that actually exist and pass"),
        ],
        deliverables=[
            "Final README with accurate badges, structure and quick start",
            "Repository description and topic list set on GitHub, issue and PR templates present",
        ],
        steps=[
            "Verify every badge URL resolves and its workflow exists.",
            "Update the README's repository layout section against the real tree.",
            "Set the repository description and topics through `gh repo edit`.",
            "Confirm the templates render and match the actual process.",
        ],
        accept=[
            "No badge is broken and none claims a state that is not true",
            "The layout section matches the real directory tree",
            "Description and topics are set on the repository",
        ],
        verify=[
            "gh repo view --json description,repositoryTopics",
            "python3 tools/check_links.py",
        ],
        state="The repository explains itself accurately to a human visitor and to an agent.",
    ),
    Task(
        id=147,
        slug="chain-closure",
        title="Chain closure and final handover statement",
        goal="Close the plan honestly: states what is complete, what is not, what is risky, and what a future agent should do next.",
        deps=[146],
        est="60-120 min",
        skills=[
            ("technical-writing", "a closing statement without self-congratulation, stating gaps plainly"),
            ("testing", "final verification run of the whole chain tooling"),
        ],
        deliverables=[
            "`status/CLOSURE.md`: what shipped, verification summary, known limitations, recommended next work",
            "Final status regeneration so PROGRESS, NEXT and HANDOVER reflect the closed chain",
        ],
        steps=[
            "Run the full verification set: tests, chain verification, link check, secrets preflight, plan check.",
            "State every known limitation and every unverified claim explicitly.",
            "Recommend the three most valuable next tasks with the reason each matters.",
            "Regenerate the status artefacts and commit the closure.",
        ],
        accept=[
            "Every verification tool is run and its result recorded",
            "Limitations are stated without hedging, and unverified items are labelled as such",
            "The closure document names the next three tasks with reasons",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest",
            "python3 tools/verify_chain.py",
            "python3 tools/generate_plan.py --check",
            "scripts/preflight-secrets.sh",
        ],
        state="The plan is closed with an honest account of what exists, what was proven, and what remains.",
    ),
]
