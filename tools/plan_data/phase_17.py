"""Phase 17 — One-tap access, key issuing and tooling coverage.

The owner asked for three things this phase delivers: getting started free with one
tap and no account, issuing DroidRoute's own keys that nobody — including the owner —
can read back, and proving that the build agents use every applicable plugin, skill
and MCP server instead of the few they remember.
"""

from common import Phase, Task

PHASE = Phase(
    number=17,
    slug="access-and-tooling",
    title="One-tap access, key issuing & tooling coverage",
    summary="One-tap free start, device-code sign-in, local-only key issuing for DroidRoute itself, tooling coverage proof, the reusable workflow plugin, and the clone-from-scratch freeze.",
)

TASKS = [
    Task(
        id=203,
        slug="one-tap-free-start",
        title="One-tap free start with no account",
        goal=(
            "Get a working gateway with one button and no sign-up: probe the bundled no-auth and free-tier providers in a "
            "fixed order, validate with a real call, enable the first that answers, and say honestly what was picked and what "
            "its limits are."
        ),
        deps=[96, 105, 169],
        est="120-240 min",
        skills=[
            ("droidroute-provider-manifest", "which free providers exist, what they permit and how their limits are stated"),
            ("droidroute-verification", "a real validation call per candidate, and an honest failure when none works"),
        ],
        deliverables=[
            "A `Gratis starten` action in onboarding and on the Dashboard's empty state",
            "A probe sequence with a per-candidate outcome, so a failure names every candidate and why it failed",
        ],
        steps=[
            "Order the candidates by the measured health and latency from earlier runs, not by a hardcoded preference.",
            "Validate each candidate with a real, minimal call before enabling it — a provider that answers `/models` but not a completion is not working.",
            "Show the chosen provider, its model and its stated limit right after success, with a link to change it.",
            "If no candidate answers, say so with the per-candidate reasons and offer the manual path — never enable a provider that failed.",
            "Record the outcome in the log so later free-tier decisions are based on evidence.",
        ],
        accept=[
            "On a fresh install, one tap reaches a verified working endpoint with no account and no key typed",
            "A failing candidate never becomes an enabled provider, and its reason is visible",
            "If every candidate fails, the screen states it and points at the manual path",
            "The free-tier limits shown match what the provider's response actually said",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*FreeStart*'",
            "curl -fsS http://127.0.0.1:8787/v1/models | head -20",
        ],
        state="Starting costs one tap and no identity, and the app never pretends a dead provider works.",
    ),
    Task(
        id=204,
        slug="device-code-sign-in",
        title="One-tap sign-in with the device code flow",
        goal=(
            "Sign in to the providers that support it with one tap — show a short code, the owner confirms on a page, done — "
            "instead of hunting for an API key. Where a provider has no such flow, say so and fall back without pretending."
        ),
        deps=[57, 171],
        est="150-300 min",
        skills=[
            ("oauth-device-flow", "the real device-authorization flow, its polling rules and its error states"),
            ("ai-governors", "a login that silently uses an account would be a defect — the owner confirms, always"),
        ],
        deliverables=[
            "A reusable device-code sign-in that onboarding, the provider list and provider detail can all open",
            "The sign-in screen: the code, a copy action, the verification address, remaining time, and a cancel that actually stops the polling",
        ],
        steps=[
            "Implement the flow once and reuse it: request a code, show it, poll at the interval the provider specified, handle slow-down and expiry.",
            "Store the result in the vault under the account's label, never in a shared blob, and name the account so multi-account rotation (T-171) applies.",
            "Handle the honest failures: expired code, denied consent, no such flow, offline.",
            "State on screen what the sign-in grants and what it does not, before the owner confirms.",
            "Cancel must stop the polling immediately, with no background attempt afterwards.",
        ],
        accept=[
            "Signing in from onboarding takes one tap plus one confirmation on a page (demonstrated once)",
            "Expired and denied flows show a precise message and leave no half-configured account",
            "Cancel stops all network activity for that flow (verified in the log)",
            "A provider without this flow is labelled as such and offers the key path instead",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*DeviceCode*'",
            "python3 tools/check_plan_consistency.py",
        ],
        state="Accounts are connected by confirming a code, not by copying a secret into a text field.",
    ),
    Task(
        id=205,
        slug="local-only-key-issuing",
        title="DroidRoute key issuing, readable by nobody",
        goal=(
            "Let the owner issue DroidRoute's own API keys — created on the device, stored only encrypted, shown exactly once, "
            "and unreadable afterwards by anyone, including the owner. No export path exists, by design."
        ),
        deps=[16, 21, 99, 165, 193],
        est="180-360 min",
        skills=[
            ("security-audit", "a secret that cannot be read back needs its storage claims tested, not documented"),
            ("droidroute-verification", "proving the absence of a read-back path, which is harder than proving a feature works"),
        ],
        deliverables=[
            "`ui/keys/IssueKeyScreen.kt` — scope, expiry, label, then one-time reveal",
            "`keys/Issuer.kt` — generation, hashing, scope enforcement, revocation, with no retrieval API",
            "A test suite that fails if any code path can reproduce a stored key",
        ],
        steps=[
            "Generate keys with a cryptographically secure source and store only what verification needs — never the key itself.",
            "Show the full key exactly once, with an explicit \"this is the only time you will see it\" and a copy action that uses the 60-second clipboard timer.",
            "Store afterwards only what is needed to mask (`first5••••last5`) — the mask is metadata, not the secret.",
            "Support scope (models, read-only, budget, expiry) and revocation that takes effect without a restart.",
            "Write the test that would catch a regression: search the storage layer and the API for any path that returns a stored key, and assert there is none.",
        ],
        accept=[
            "A newly issued key works against the gateway and appears masked afterwards",
            "After the one-time reveal, no API, screen, export or log can reproduce it (asserted by a test that fails if a read-back path is added)",
            "Revocation invalidates the key immediately (asserted)",
            "Scope and expiry are enforced, and a scoped key cannot exceed its scope (asserted)",
            "The documentation states plainly that a lost key is replaced, never recovered",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*KeyIssuer*'",
            "scripts/preflight-secrets.sh",
        ],
        state="DroidRoute's own keys are usable by its clients and readable by nobody — enforced by tests, not by intent.",
    ),
    Task(
        id=206,
        slug="tooling-coverage-proof",
        title="Proof that every applicable skill, plugin and MCP server is used",
        goal=(
            "Stop the build agents from using the three tools they remember. Decide, per installed skill, plugin and MCP "
            "server, whether it applies — and record used / declined-with-reason for each, with CI failing on \"undecided\"."
        ),
        deps=[166, 190],
        est="150-300 min",
        skills=[
            ("droidroute-skill-scout", "matching an installed tool to the work it actually improves"),
            ("droidroute-verification", "a coverage report that can be re-run and compared, not a narrative"),
        ],
        deliverables=[
            "`tools/tooling_coverage.py` — joins `status/tooling.json` with a committed decisions file and reports undecided entries",
            "`status/TOOLING-COVERAGE.md` — every installed skill, plugin and MCP server with used / declined + reason, and where it was used",
            "CI step that fails while any entry is undecided",
        ],
        steps=[
            "Generate the candidate list from the inventory, grouped by domain, so nothing is missed by not being remembered.",
            "For each candidate, record a decision: `used` with the phase and task id where it applied, or `declined` with a one-line reason.",
            "Make the report check itself: an entry present in the inventory but absent from the decisions fails, and so does a decision for a tool that is no longer installed.",
            "Review the declined list once with fresh eyes — a tool declined in phase 3 may apply in phase 12, and the reason must say why not.",
        ],
        accept=[
            "Every installed skill, plugin and MCP server has a decision with a reason",
            "Every `used` entry names where it was used (phase or task id)",
            "CI fails while an entry is undecided (proven once, then reverted)",
            "The report is regenerated in the same commit as any inventory change",
        ],
        verify=[
            "python3 tools/tooling_coverage.py --check",
            "python3 tools/check_plan_consistency.py",
        ],
        state="Tool usage is a reviewed decision per tool instead of a habit — and the gaps are named.",
    ),
    Task(
        id=207,
        slug="workflow-plugin-and-publish",
        title="Reusable build workflow: consume it here, publish it as `routin`",
        goal=(
            "Turn this repository's agent workflow into a reusable, installable artefact — skills, subagents, gate scripts and "
            "templates — use it from this project, and publish it in its own private repository named `routin`, "
            "containing nothing project-specific."
        ),
        deps=[166, 206],
        est="240-480 min",
        skills=[
            ("droidroute-skill-scout", "what belongs in a reusable workflow and what is only true for this project"),
            ("git-workflow", "keeping two repositories honest without copying files between them"),
        ],
        deliverables=[
            "A workflow plugin (manifest + skills + subagents + gate scripts + templates) that installs into any project",
            "This repository consuming the plugin, with the duplicated parts removed and referenced instead",
            "The private GitHub repository `routin`, containing the workflow only — asserted by a leak check",
        ],
        steps=[
            "Separate the workflow from the project: the loop, the gates, the log protocol and the handover rules are generic; the design tokens, providers and acceptance criteria are not (TBC-11).",
            "Create the repository as `routin`, private, with the local working copy under that name — not beside this project's files, so a stray path can never publish the wrong tree.",
            "Package the generic part as a plugin with a manifest, so another agent can install it rather than copy it.",
            "Make this repository consume the plugin and delete its own copies of anything the plugin now owns — two sources of truth is the failure mode to avoid.",
            "Prove it runs: install it in a scratch project and complete one small task with it, recording the run.",
            "Add a leak check to the plugin repository: no project name, no credential, no file from this project may appear in it.",
        ],
        accept=[
            "The plugin installs in a scratch project and completes a task end to end (recorded)",
            "This repository has no duplicate copy of anything the plugin owns",
            "`routin` is private and contains no project-specific file, name or secret (asserted by its own check)",
            "`gh repo view mertgoevse-wq/routin --json name,visibility` reports `PRIVATE`",
            "Both repositories are private, and each documents how the other is updated",
        ],
        verify=[
            "python3 tools/check_plan_consistency.py",
            "gh repo view --json name,visibility",
        ],
        state="The build workflow is reusable and published on its own as `routin`, while this project consumes it instead of forking it.",
    ),
    Task(
        id=208,
        slug="clone-from-scratch-freeze",
        title="Clone-from-scratch verification and freeze",
        goal=(
            "Prove the handover works from nothing: clone into an empty directory, run the bootstrap, pass every check, and "
            "complete one task end to end as a fresh agent. Then freeze it and state what is not finished."
        ),
        deps=[202, 205, 207],
        est="120-240 min",
        skills=[
            ("git-workflow", "a clean clone, a clean tree and a push that loses nothing"),
            ("droidroute-verification", "the drill: does a stranger with only the repository succeed?"),
        ],
        deliverables=[
            "A recorded clone-from-scratch run: clone → `scripts/bootstrap.sh` → every check green → one task completed",
            "The freeze statement in `status/PROGRESS.md`, with the exact commit and the open items",
            "Owner instructions updated for the new folder name and the clone path",
        ],
        steps=[
            "Clone the repository into an empty directory under the new name and run the bootstrap exactly as documented.",
            "Run every checker and paste the raw output into the task log — including the design gate's self-test.",
            "Dispatch a fresh agent with only the repository: it reads the state files and completes one task from the plan.",
            "Record the drill as a document a future agent can repeat, including what was confusing about it.",
            "Freeze: name the commit, list what is unfinished, and update the owner instructions.",
        ],
        accept=[
            "A fresh clone passes `scripts/bootstrap.sh` with no manual step (paste the output)",
            "A fresh agent completed one task using only the repository (recorded)",
            "The new folder name appears in every instruction and no stale path remains",
            "The freeze statement names what is unfinished instead of implying completion",
        ],
        verify=[
            "bash scripts/bootstrap.sh",
            "python3 tools/check_plan_consistency.py",
            "python3 tools/generate_plan.py --check",
        ],
        state="Someone with nothing but the clone URL can take over, and the repository says truthfully where it stands.",
    ),
]
